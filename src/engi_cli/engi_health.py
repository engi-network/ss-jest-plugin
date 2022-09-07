"""Engi Health

Print a JSON object to stdout containing Engi network status information.

Usage:
  engi health [options]
  engi (-h | --help)
  engi --version

Options:
  -h --help       Show this screen
  -n, --dry-run   Dry run
  -v, --verbose   Be verbose
"""

import asyncio

from docopt import docopt

from engi_cli.blockchain_api import get_health
from engi_cli.helpful_scripts import json_dumps, setup_logging

log = setup_logging()


async def main():
    args = docopt(__doc__)
    log.info(f"{args=}")
    result = await get_health()
    print(json_dumps(result["health"]))


if __name__ == "__main__":
    asyncio.run(main())
