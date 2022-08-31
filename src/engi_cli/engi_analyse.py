"""Engi Analyse

Usage:
  engi analyse [options] <repo>
  engi (-h | --help)
  engi --version

Options:
  -h --help                Show this screen
  -n, --dry-run            Dry run
  -v, --verbose            Be verbose

  --docker-compose=<str>   Command to run Docker [default: docker-compose]
  --test-output-dir=<str>  Where the test runner writes its output in <repo> [default: .]
"""
import asyncio
import json

from docopt import docopt

from engi_cli.helpful_scripts import (
    GitHubRepoAnalyser,
    get_kwargs,
    json_dumps,
    setup_logging,
)

log = setup_logging()


async def main():
    args = docopt(__doc__)
    log.info(f"{args=}")
    repo = args["<repo>"]
    analyser = GitHubRepoAnalyser(repo, **get_kwargs(args))
    await analyser.analyse()
    print(json_dumps(analyser.failing_tests))


if __name__ == "__main__":
    asyncio.run(main())
