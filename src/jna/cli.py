import argparse
import sys
from pathlib import Path

from .lexer import tokenize, LexerError
from .parser import parse, ParserError
from .interpreter import interpret
from .runtime import RuntimeErrorJNA


def run_file(filename):
    path = Path(filename)

    if not path.is_file():
        print(f"JNA Error: File ora ditemokake: {filename}", file=sys.stderr)
        return 1

    try:
        source = path.read_text(encoding="utf-8")

        tokens = tokenize(source)
        program = parse(tokens)
        interpret(program)

        return 0

    except (LexerError, ParserError, RuntimeErrorJNA) as error:
        print(f"JNA Error: {error}", file=sys.stderr)
        return 1

    except RecursionError:
        print("JNA Error: Panggilan fungsi kejero banget", file=sys.stderr)
        return 1

    except UnicodeDecodeError:
        print("JNA Error: File kudu nganggo UTF-8", file=sys.stderr)
        return 1


def main():
    parser = argparse.ArgumentParser(
        prog="jna",
        description="JNA - Jawa Ngapak Absurd Programming Language"
    )

    parser.add_argument(
        "file",
        help="File program JNA (.jna)"
    )

    args = parser.parse_args()

    if not args.file.endswith(".jna"):
        print("JNA Error: Ekstensi file kudu .jna", file=sys.stderr)
        return 1

    return run_file(args.file)


if __name__ == "__main__":
    sys.exit(main())
