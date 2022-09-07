"""Engi Draft

Take the output of the `analyse' command located at <check> and print to stdout
in JSON format, a draft job object ready for posting to the Engi marketplace.

If <check> is the special character `-' then read the JSON object from stdin.
Otherwise, if <check> is a valid path, read the object from the file. If neither
of those two conditions are true, attempt to load the JSON object from the string
<check>.

Optionally filter the list of failing tests using the --test option. If not
specified, assume all tests need to pass.

If optional globs to specify files that may be edited, added and deleted are
omitted, assume all files.

Usage:
  engi draft [options] <check> [--test=<str>]...
  engi (-h | --help)
  engi --version

Options:
  -h --help                Show this screen
  -n, --dry-run            Dry run
  -v, --verbose            Be verbose

  --title=<str>            Job title [default: My job]
  --amount=<int>           Engi payment amount [default: 10]
  --is-editable=<str>      Glob to specify files that may be edited
  --is-addable=<str>       Glob to specify files that may be added
  --is-deletable=<str>     Glob to specify files that may be deleted
"""

from docopt import docopt

from engi_cli.helpful_scripts import JobDraft, RepoAnalyser, read_json, setup_logging

log = setup_logging()


def main():
    args = docopt(__doc__)
    log.info(f"{args=}")
    check_obj = read_json(args["<check>"])
    log.info(check_obj)
    creator = JobDraft(RepoAnalyser().load_dict(check_obj))
    creator.set_title(args["--title"])
    creator.set_amount(int(args["--amount"]))
    tests = args["--test"]
    if not creator.set_failing_tests(tests):
        log.error(f"{tests} not a subset of {creator.analyser.failing_test_list}?")
    for key in ["editable", "addable", "deletable"]:
        key = f"is_{key}"
        getattr(creator, f"set_{key}")(args["--" + key.replace("_", "-")])
    if creator.error:
        log.error(f"did you set an empty title or zero amount?")
    print(creator.json())


if __name__ == "__main__":
    main()
