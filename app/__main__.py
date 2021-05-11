import sys
from typing import Sequence
from app import Application


def main(argv: Sequence[str]) -> None:
    app = Application()
    app(argv)


if __name__ == "__main__":
    main(sys.argv[1:])
