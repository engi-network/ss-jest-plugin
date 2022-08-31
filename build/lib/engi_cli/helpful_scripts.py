import asyncio
import importlib
import inspect
import json
import logging
import os
import re
import tempfile
from asyncio.subprocess import PIPE
from contextlib import contextmanager
from pathlib import Path
from shlex import quote as sh_quote
from subprocess import call
from time import perf_counter

import coloredlogs

import engi_cli


def json_dumps(obj):
    return json.dumps(obj, indent=4)


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
    if proc.returncode != raise_code:
        raise CmdError(cmd, cmd_exit)
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


async def github_checkout(repo, dest, github_token=None, branch=None, commit=None):
    dest_path = Path(dest)
    if not (dest_path / ".git").exists():
        (github_cmd, github_opts) = get_github_cmd(github_token)
        log_cmd = f"{github_cmd} repo clone {repo} {dest_path}"
        await run(f"{log_cmd} {github_opts}", log_cmd=log_cmd)
    else:
        log.warning(f"{dest} exists, skipping GitHub checkout")
    if branch:
        await run(f"{github_cmd} repo sync --branch {branch}")
    if commit:
        await run(f"git checkout {commit}")


async def github_linguist(dest):
    cmd_exit = await run(f"github-linguist -j {dest}")
    return json.loads(cmd_exit.stdout)


def get_language_module(language):
    log.info(f"importing engi_cli.analyse.{language}")
    return importlib.import_module(f"engi_cli.analyse.{language}")


class RepoAnalyser(object):
    def __init__(self, repo, *args, **kwargs):
        self.repo = repo
        self.language = None
        self.docker = None
        self.failing_tests = None
        self.json = None
        self.error = None
        self.language_helper = None
        self.args = args
        self.kwargs = kwargs

    def set_language(self, language):
        self.language = language
        try:
            self.language_helper = get_language_module(language).LanguageHelper(
                self.repo, self.args, self.kwargs
            )
        except ModuleNotFoundError:
            log.info(f"failied to import helper for {language}")
        return self.language_helper is not None

    def set_docker(self, docker):
        self.docker = docker

    def set_failing_tests(self, failing_tests):
        self.failing_tests = failing_tests

    def analyse(self):
        if self.language_helper is not None and self.docker and self.failing_tests:
            (self.json, self.error) = (1, 0)
        else:
            (self.json, self.error) = (0, 1)

    def __repr__(self):
        return f"{self.repo=} {self.language=} {self.docker=} {self.failing_tests=} {self.json=} {self.error=}"


class GitHubRepoAnalyser(RepoAnalyser):
    async def analyse(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            await github_checkout(self.repo, tmpdir)
            with set_directory(tmpdir):
                breakdown = await github_linguist(".")
                for language, _ in sorted(
                    breakdown.items(), key=lambda item: item[1]["size"], reverse=True
                ):
                    if self.set_language(language):
                        break
                if "Dockerfile" in breakdown:
                    self.set_docker(1)
                await self.language_helper.run_tests()
                self.set_failing_tests(await self.language_helper.parse_failing_tests())
            super().analyse()
            log.info(f"{self=}")
