#!/usr/bin/env python

import pyqrcode
import argparse
import sys


def main():
    """Generate QR code for a given url"""
    args = cli()
    if args.scale is None:
        args.scale = 8
    qr = pyqrcode.create(args.url)
    svg_file_name = ''.join([str(args.url), '.svg'])
    sys.stderr.write(f'generating svg ... {svg_file_name}')
    qr.svg(svg_file_name, args.scale)
    return


def cli():
    """Parse and return command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'url',
        help='the url for which to create a qr code',
    )
    parser.add_argument(
        '-s',
        '--scale',
        type=int,
        help='the scale for the svg output'
    )
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main()
