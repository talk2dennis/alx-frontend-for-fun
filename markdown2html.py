#!/usr/bin/python3
""" module that converts markdown to html """

import sys
import os

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    if os.path.exists(sys.argv[1]) is False:
        print("Missing {}".format(sys.argv[1]), file=sys.stderr)
        sys.exit(1)
