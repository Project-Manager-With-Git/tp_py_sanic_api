import sys
from typing import Sequence
from app import Application


def main(argv: Sequence[str] = sys.argv[1:]) -> None:
    app = Application()
    app(argv)


if __name__ == "__main__":
    main()
