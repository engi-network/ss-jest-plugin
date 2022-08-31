"""Engi CLI

Usage:
  engi <command> [<args>...]
  engi (-h | --help)
  engi --version

Options:
  -h --help     Show this screen.
  --version     Show version.

The most commonly used engi commands are:
   submission   Execute a job.

See `engi <command> help' for more information on a specific command.
"""

from docopt import docopt

from engi_cli.helpful_scripts import CommandNotFoundException, run_script

VERSION = "Engi CLI v0.0.1"


def main():
    args = docopt(__doc__, version=VERSION, options_first=True)

    command = args["<command>"]
    argv = [command] + args["<args>"]
    try:
        return run_script(command, argv)
    except CommandNotFoundException as e:
        print(f"Unsupported command `{command}'")
        print(f"No such file {e}\n\n")
        print(__doc__)
        exit(1)


if __name__ == "__main__":
    main()
