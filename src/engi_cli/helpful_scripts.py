import asyncio
import csv
import importlib
import inspect
import json
import logging
import os
import re
import sys
import tempfile
from asyncio.subprocess import PIPE
from contextlib import contextmanager
from io import StringIO
from pathlib import Path
from shlex import quote as sh_quote
from subprocess import call
from time import perf_counter

import coloredlogs

import engi_cli


def json_dumps(obj):
    return json.dumps(obj, indent=4)


def read_json(s):
    """read JSON object from s
    if s is the char `-' then read from stdin
    if s is a valid path then read from file
    else attempt to load directly s
    """
    if s == "-":
        return json.load(sys.stdin)
    p = Path(s)
    if p.exists():
        return json.load(open(s))
    return json.loads(s)


def setup_logging(log_level=logging.INFO):
    frm = inspect.stack()[1]
    mod = inspect.getmodule(frm[0])
    logger = logging.getLogger(mod.__name__)

    # Set log format to dislay the logger name to hunt down verbose logging modules
    fmt = "%(asctime)s %(name)-25s %(levelname)-8s %(message)s"

    coloredlogs.install(level=log_level, fmt=fmt, logger=logger)

    return logger


log = setup_logging()


def replace_all(text, args):
    for key, val in args:
        text = text.replace(key, val)
    return text


def get_kwargs(args):
    """convert a docopt arg dict
    {'--docker-compose': 'docker-compose'} -> {'docker_compose': 'docker-compose'}"""
    return dict(
        [
            (replace_all(key, (("-", "_"), ("__", ""))), val)
            for key, val in args.items()
            if "--" in key
        ]
    )


async def get_lizard_metrics(path):
    """run lizard to get the files, source lines of code and cyclomatic complexity of the code in path"""
    cmd_exit = await run(f"lizard {path} --csv --verbose")
    rows = list(csv.DictReader(StringIO(cmd_exit.stdout)))
    c = [int(r["CCN"]) for r in rows]
    return {
        "files": list(set([r["file"] for r in rows])),
        "sloc": sum([int(r["NLOC"]) for r in rows]),
        "cyclomatic": sum(c) / len(c),
    }


class CommandNotFoundException(RuntimeError):
    pass


def run_script(name, argv):
    script = get_script(name)
    # print(f"{script=} {argv=}")
    return exit(call(["python", script] + argv))


def get_script(name):
    script = Path(engi_cli.__file__).parent / Path(f"engi_{name}.py")
    if not script.exists():
        raise CommandNotFoundException(script)
    return script


def get_scripts():
    return [
        (
            path.stem.split("_")[-1],
            importlib.import_module(f"engi_cli.{path.stem}").__doc__.split("\n")[0],
        )
        for path in Path(engi_cli.__file__).parent.glob("engi_*.py")
    ]


def delete_test_messages(failing_tests):
    # the message often includes trivial differences such as line numbers
    [t.pop("TestMessage") for t in failing_tests]


@contextmanager
def set_directory(path):
    origin = Path().absolute()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(origin)


@contextmanager
def set_tmpdir():
    with tempfile.TemporaryDirectory() as tmpdir:
        with set_directory(tmpdir):
            yield tmpdir


async def run(cmd, log_cmd=None, raise_code=0):
    """log and run `cmd` optionally log `log_cmd` rather than `cmd` for when `cmd` contains secrets"""
    if log_cmd is None:
        log_cmd = cmd
    # don't log env vars
    log_cmd = re.subn(r"\S+=\S+ ", "", log_cmd)[0]
    log.info(log_cmd)
    t1_start = perf_counter()
    proc = await asyncio.create_subprocess_shell(cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = await proc.communicate()
    stdout = stdout.decode() if stdout else None
    stderr = stderr.decode() if stderr else None
    t1_stop = perf_counter()

    if stdout:
        log.info(f"[stdout]\n{stdout}")
    if stderr:
        log.info(f"[stderr]\n{stderr}")
    log.info(
        f"{log_cmd!r} exited with code {proc.returncode} elapsed {t1_stop - t1_start} seconds"
    )
    cmd_exit = CmdExit(proc.returncode, stdout, stderr)
    if raise_code is not None and proc.returncode != raise_code:
        raise CmdError(log_cmd, cmd_exit)
    return cmd_exit


class CmdExit(object):
    def __init__(self, returncode=None, stdout=None, stderr=None):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


class CmdError(Exception):
    def __init__(self, cmd, cmd_exit):
        self.cmd = cmd
        self.cmd_exit = cmd_exit

    def __repr__(self):
        return (
            f"{self.cmd!r} exited with return code {self.cmd_exit.returncode}\n"
            f"stdout: {self.cmd_exit.stdout}\n"
            f"stderr: {self.cmd_exit.stderr}"
        )


def get_github_cmd(github_token=None):
    if github_token is None:
        github_token = os.environ["GITHUB_TOKEN"]
    github_token = sh_quote(github_token)
    # don't ask 😆
    github_cmd = f"GITHUB_TOKEN='{github_token}' gh"
    github_opts = (
        f"-- -c url.'https://{github_token}:@github.com/'.insteadOf='https://github.com/'"
    )
    # oh, alright then -- the -c option lets us use the GitHub personal access
    # token as the Git credential helper
    return (github_cmd, github_opts)


async def run_github(log_cmd, github_token=None, opts=True):
    (github_cmd, github_opts) = get_github_cmd(github_token)
    if not opts:
        github_opts = ""
    return await run(f"{github_cmd} {log_cmd} {github_opts}", log_cmd=f"gh {log_cmd}")


async def github_sync(branch, commit, github_token=None):
    await run("git stash")
    branch_cmd = f" --branch {branch}" if branch is not None else ""
    await run_github(f"repo sync{branch_cmd}", github_token=github_token, opts=False)
    if commit:
        await run(f"git checkout {commit}")


async def github_checkout(repo, dest, github_token=None):
    """Check out code at GitHub URL <repo> to local path <dest>"""
    assert "github" in repo
    repo_ = "/".join(repo.split("/")[-2:]).replace(".git", "")
    dest_path = Path(dest)
    if (dest_path / ".git").exists():
        log.warning(f"{dest} exists, skipping GitHub checkout")
        return False
    await run_github(f"repo clone {repo_} {dest_path}", github_token=github_token)
    return True


async def github_linguist(dest):
    cmd_exit = await run(f"github-linguist -j {dest}")
    return json.loads(cmd_exit.stdout)


def get_language_module(language):
    log.info(f"importing engi_cli.analyse.{language}")
    return importlib.import_module(f"engi_cli.analyse.{language}")


def sorted_dict(d, key="TestId"):
    return sorted(d, key=lambda d: d[key]) if hasattr(d, "__iter__") else d


def sorted_list(l):
    return sorted(l) if hasattr(l, "__iter__") else l


class RepoAnalyser(object):
    def __init__(self, repo=None, branch=None, commit=None, *args, **kwargs):
        self.repo = repo
        self.branch = branch
        self.commit = commit
        self.language = None
        self.docker = None
        self._failing_tests = None
        self.error = None
        self.language_helper = None
        self._files = None
        self.sloc = None
        self.cyclomatic = None
        self.args = args
        self.kwargs = kwargs

    @property
    def suffix(self):
        return self.repo.split("/")[-1]

    @property
    def failing_tests(self):
        return sorted_dict(self._failing_tests)

    @property
    def files(self):
        return sorted_list(self._files)

    def set_branch(self, branch):
        self.branch = branch

    def set_commit(self, commit):
        self.commit = commit

    def set_language(self, language):
        self.language = language
        try:
            m = get_language_module(language)
            self.language_helper = m.LanguageHelper(self.repo, m, self.args, self.kwargs)
        except ModuleNotFoundError:
            log.info(f"failied to import helper for {language}")
        return self.language_helper is not None

    def set_docker(self, docker):
        self.docker = docker

    def set_metrics(self, files=None, sloc=None, cyclomatic=None):
        self.set_files(files)
        self.sloc = sloc
        self.cyclomatic = cyclomatic

    def set_failing_tests(self, failing_tests):
        self._failing_tests = failing_tests

    def set_files(self, files):
        self._files = files

    @property
    def failing_test_list(self):
        return sorted_list([t["TestId"] for t in self.failing_tests])

    def analyse(self):
        self.error = not (self.language_helper is not None and self.docker and self.failing_tests)

    def __repr__(self):
        return self.json()

    def json(self, **kwargs):
        return json_dumps(
            {
                "Repo": self.repo,
                "Branch": self.branch,
                "Commit": self.commit,
                "Language": self.language,
                "Files": self.files,
                "Complexity": {
                    "SLOC": self.sloc,
                    "Cyclomatic": self.cyclomatic,
                },
                "FailingTests": self.failing_tests,
                **kwargs,
            },
        )

    def load_dict(self, check_obj):
        self.repo = check_obj["Repo"]
        self.branch = check_obj["Branch"]
        self.commit = check_obj["Commit"]
        self._files = check_obj["Files"]
        self.sloc = check_obj["Complexity"]["SLOC"]
        self.cyclomatic = check_obj["Complexity"]["Cyclomatic"]
        self._failing_tests = check_obj["FailingTests"]
        self.language = check_obj["Language"]
        return self

    def loads(self, s):
        return self.load_dict(json.loads(s))


def mkdir(name):
    tmpdir = Path(os.environ.get("TMPDIR", "/tmp"))
    p = tmpdir / name
    if not p.exists():
        os.makedirs(p)
    return p


class GitHubRepoAnalyser(RepoAnalyser):
    async def analyse(self):
        # with tempfile.TemporaryDirectory(self.suffix) as tmpdir:
        tmpdir = mkdir(self.suffix)
        await github_checkout(self.repo, tmpdir)
        with set_directory(tmpdir):
            log.info(f"{self.branch=} {self.commit=}")
            await github_sync(self.branch, self.commit)
            breakdown = await github_linguist(".")
            for language, _ in sorted(
                breakdown.items(), key=lambda item: item[1]["size"], reverse=True
            ):
                if self.set_language(language):
                    break
            if "Dockerfile" in breakdown:
                self.set_docker(1)
            await self.language_helper.run_tests()
            self.set_metrics(**await self.language_helper.get_metrics())
            self.set_failing_tests(await self.language_helper.parse_failing_tests())
        super().analyse()
        log.info(f"{self=}")


def issubset(a, b):
    """return True if a is a subset of b"""
    # log.info(f"{a=} {b=}")
    return set(a) <= set(b)


class JobDraft(object):
    def __init__(self, analyser=None):
        self.analyser = analyser
        self.title = None
        self.amount = None
        self._failing_tests = None
        self.is_editable = None
        self.is_addable = None
        self.is_deletable = None

    def set_title(self, title):
        self.title = title

    def set_amount(self, amount):
        self.amount = amount

    def set_is_editable(self, is_editable):
        self.is_editable = is_editable

    def set_is_addable(self, is_addable):
        self.is_addable = is_addable

    def set_is_deletable(self, is_deletable):
        self.is_deletable = is_deletable

    @property
    def error(self):
        return not (
            self.title
            and self.amount
            and issubset(self.failing_tests, self.analyser.failing_test_list)
        )

    @property
    def failing_tests(self):
        return sorted_list(self._failing_tests)

    def set_failing_tests(self, failing_tests):
        self._failing_tests = failing_tests
        return issubset(self.failing_tests, self.analyser.failing_test_list)

    def json(self):
        return self.analyser.json(
            Draft={
                "FailingTests": self.failing_tests,
                "IsEditable": self.is_editable,
                "IsAddable": self.is_addable,
                "IsDeletable": self.is_deletable,
                "Amount": self.amount,
                "Title": self.title,
            }
        )

    def load_dict(self, check_obj):
        self.analyser = RepoAnalyser()
        self.analyser.load_dict(check_obj)
        self.repo = check_obj["Repo"]
        self.branch = check_obj["Branch"]
        self.commit = check_obj["Commit"]
        self._files = check_obj["Files"]
        self.sloc = check_obj["Complexity"]["SLOC"]
        self.cyclomatic = check_obj["Complexity"]["Cyclomatic"]
        self._failing_tests = check_obj["FailingTests"]
        self.language = check_obj["Language"]
        return self

    def __repr__(self):
        return self.json()


class Job(object):
    def __init__(self, draft, secret=None, tip=None):
        self.draft = draft
        self.secret = secret
        self.tip = tip

    def set_secret(self, secret):
        self.secret = secret

    def set_tip(self, tip):
        self.tip = tip

    async def create(self):
        return {"data": {"createJob": "xyz789"}}
