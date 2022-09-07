"""Engi User

Given a user name and password, create a new account on the Engi network. On
successful creation, print a JSON object to stdout containing the new wallet
address and recovery mnemonic.

Usage:
  engi user create <name> <password>
  engi (-h | --help)
  engi --version

Options:
  -h --help       Show this screen
  -n, --dry-run   Dry run
  -v, --verbose   Be verbose
"""

import asyncio

from docopt import docopt

from engi_cli.blockchain_api import GraphQLUser
from engi_cli.helpful_scripts import setup_logging

log = setup_logging()


async def main():
    args = docopt(__doc__)
    log.info(f"{args=}")
    password = args["<password>"]
    manager = GraphQLUser(args["<name>"], password, password)
    if manager.error:
        log.error(f"error creating new user, {manager=}")
    else:
        await manager.create()
        print(manager.json())


if __name__ == "__main__":
    asyncio.run(main())
