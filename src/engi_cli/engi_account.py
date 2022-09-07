"""Engi Account

Print a JSON object to stdout containing details for account with wallet address
<id>.

Usage:
  engi account [options] <id>
  engi (-h | --help)
  engi --version

Options:
  -h --help       Show this screen
  -n, --dry-run   Dry run
  -v, --verbose   Be verbose
"""

import asyncio

from docopt import docopt

from engi_cli.blockchain_api import get_account
from engi_cli.helpful_scripts import json_dumps, setup_logging

log = setup_logging()


async def main():
    args = docopt(__doc__)
    log.info(f"{args=}")
    result = await get_account(args["<id>"])
    print(json_dumps(result["account"]))


if __name__ == "__main__":
    asyncio.run(main())
