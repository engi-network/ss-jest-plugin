"""Engi Submission

Usage:
  engi submission [options] execute <path> <type> [<args>...]
  engi (-h | --help)
  engi --version

Options:
  -h --help       Show this screen
  -n, --dry-run   Dry run
  -v, --verbose   Be verbose
"""

from docopt import docopt

from engi_cli.helpful_scripts import run_script


def main():
    # options_first so that program we're dispatching to can handle options like -h
    args = docopt(__doc__, options_first=True)
    typ = args["<type>"]
    argv = [typ, args["<path>"]] + args["<args>"]
    return run_script(typ, argv)


if __name__ == "__main__":
    main()
