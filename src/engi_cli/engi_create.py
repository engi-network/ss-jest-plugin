"""Engi Create

Usage:
  engi create [options] <repo>
  engi (-h | --help)
  engi --version

Options:
  -h --help       Show this screen
  -n, --dry-run   Dry run
  -v, --verbose   Be verbose
"""

from docopt import docopt


def main():
    args = docopt(__doc__)
    repo = args["<repo>"]
    print(f"{repo=}")


if __name__ == "__main__":
    main()
