#!/usr/bin/env python3

"""Generate passphrases."""

import argparse
import math
import random
import string
import sys
from typing import Callable, Sequence

__version__ = '2.0.0'

CONSOLE_SCRIPT = 'keysmith'

POPULATIONS = {
    'alphanumeric': string.ascii_letters + string.digits,
    'ascii_letters': string.ascii_letters,
    'digits': string.digits,
    'printable': string.printable,
}

SYS_ARGV = tuple(sys.argv[1:])


def build_cli(parser: argparse.ArgumentParser) -> None:
    """Build a parser for CLI arguments and options."""
    parser.add_argument(
        '-d', '--delimiter',
        help='a delimiter for the samples (teeth) in the key',
        default=' ',
    )
    parser.add_argument(
        '-n', '--nsamples',
        help='the number of random samples to take',
        type=int,
        default=6,
        dest='nteeth',
    )
    parser.add_argument(
        '-p', '--population',
        help='{0}, or a path to a file of line-delimited items'.format(
            ', '.join(POPULATIONS.keys()),
        ),
        default='/usr/share/dict/words',
    )
    parser.add_argument(
        '--encoding',
        help='the encoding of the population file',
        default='utf-8',
    )
    parser.add_argument(
        '--stats',
        help='show statistics for the key',
        default=False,
        action='store_true',
    )
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s {0}'.format(__version__),
    )


def cli() -> argparse.ArgumentParser:
    """Create a parser for CLI arguments and options."""
    parser = argparse.ArgumentParser(
        prog=CONSOLE_SCRIPT,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    build_cli(parser)
    return parser


def key(
        seq: Sequence,
        tooth: Callable[[Sequence], str] = (
            lambda seq: str(random.SystemRandom().choice(seq)).strip()
        ),
        nteeth: int = 6,
        delimiter: str = ' ',
):
    """Concatenate strings generated by the tooth function."""
    return delimiter.join(tooth(seq) for _ in range(nteeth))


def main(argv: Sequence[str] = SYS_ARGV):
    """Execute CLI commands."""
    args = cli().parse_args(argv)

    seq = POPULATIONS.get(args.population)  # type: Sequence
    if seq is None:
        try:
            with open(args.population, 'r', encoding=args.encoding) as file_:
                seq = list(file_)
        except (OSError, UnicodeError) as ex:
            print(ex, file=sys.stderr)
            return 1

    main_key = key(seq=seq, nteeth=args.nteeth, delimiter=args.delimiter)
    print(main_key)

    if args.stats:
        print('*', len(main_key), 'characters')
        print('*', args.nteeth, 'samples from a population of', len(seq))
        print(
            '* entropy {sign} {nbits} bits'.format(
                sign='<' if len(args.delimiter) < 1 else '~',
                nbits=round(math.log(len(seq), 2) * args.nteeth, 2),
            ),
        )

    return 0


if __name__ == '__main__':
    sys.exit(main())
