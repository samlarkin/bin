#!/usr/bin/env python
"""Generate a urlsafe secret key of length token_length.

>>> ,key_gen.py -l 20
"""

import secrets
import argparse
import sys


def main():
    """Generate a secret key and print it to stdout"""
    args = cli()
    if args.token_length is None:
        args.token_length = 15
    secret_key = secrets.token_urlsafe(args.token_length)
    sys.stdout.write(''.join([str(secret_key), '\n']))
    return


def cli():
    """Parse and return command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-l',
        '--token_length',
        type=int,
        help='length of token (number of characters)',
    )
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main()
