"""Engi Figma Submission

Upload a Web design image exported from Figma located at <path> and compare to
the HTML implementation in <repository> by running Storycap in the cloud.

Write status update messages and the final result in JSON format to stdout.

Logging goes to stderr.

Usage:
  engi figma <path> <repository> [options]
  engi (-h | --help)
  engi --version

Options:
  -h --help             Show this screen
  -n, --dry-run         Dry run
  -v, --verbose         Be verbose
  --env=<str>           Environment [default: dev]
  --width=<px>          Image width [default: 800]
  --height=<px>         Image height [default: 600]
  --story=<str>         Storybook story [default: Primary]
  --path=<str>          Storybook path [default: Example]
  --component=<str>     Storybook component [default: Button]
  --branch=<str>        Git branch in <repository>
  --commit=<str>        Git commit in <repository>
  --github-token=<str>  GitHub Personal Access Token
  --no-status           Don't collect status messages
  --delay=<sec>         Print the check_id then sleep before sending request [default: 0]
  --check-id=<str>      Use the given check_id rather than generating one
"""

import time
from pathlib import Path
from uuid import uuid4

from docopt import docopt
from same_story_api.helpful_scripts import Client, setup_env, setup_logging

from engi_cli.helpful_scripts import json_dumps

log = setup_logging()


def get_spec(args):
    check_id = args["--check-id"]
    if check_id is None:
        check_id = str(uuid4())
    spec_d = {"check_id": check_id, "repository": args["<repository>"]}
    for key in Client.SPEC_KEYS:
        key_ = f"--{key}"
        val = args.get(key_)
        if not key in spec_d and val is not None:
            spec_d[key] = args[key_].replace("-", "_")
    return spec_d


def main():
    args = docopt(__doc__, options_first=False)
    log.info(f"{args=}")
    setup_env(args["--env"])
    spec_d = get_spec(args)
    log.info(f"{spec_d=}")
    time.sleep(int(args["--delay"]))
    client = Client()
    path = Path(args["<path>"])
    assert path.exists(), f"{path=} not found"
    # exit(0)
    results_d = client.get_results(
        spec_d, path, callback=lambda msg: print(json_dumps(msg)), no_status=args["--no-status"]
    )
    print(json_dumps(results_d))


if __name__ == "__main__":
    main()
