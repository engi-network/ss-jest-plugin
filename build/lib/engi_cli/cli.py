from docopt import docopt

from engi_cli.helpful_scripts import CommandNotFoundException, get_scripts, run_script


def str_scripts():
    scripts = get_scripts()
    width = max([len(k) for (k, v) in scripts])
    return "\n  ".join([f"{k.ljust(width)}\t{v}" for (k, v) in scripts])


usage = f"""Engi CLI

Usage:
  engi <command> [<args>...]
  engi (-h | --help)
  engi --version

Options:
  -h --help     Show this screen.
  --version     Show version.

The most commonly used engi commands are:
  {str_scripts()}

See `engi <command> help' for more information on a specific command.
"""

VERSION = "Engi CLI v0.0.1"


def main():
    args = docopt(usage, version=VERSION, options_first=True)

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
