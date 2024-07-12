#!/usr/bin/python3
""" module that converts markdown to html """

import sys
import os
import re

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html",
              file=sys.stderr)
        sys.exit(1)

    if os.path.exists(sys.argv[1]) is False:
        print("Missing {}".format(sys.argv[1]), file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        with open(sys.argv[2], 'w') as f2:
            in_list = False
            for line in f:
                if line[0] == '#':
                    count = 0
                    for i in line:
                        if i == '#':
                            count += 1
                        else:
                            break
                    f2.write('<h{}>'.format(count) + line[count:].strip() +
                             '</h{}>\n'.format(count))
                elif line[0] == '-':
                    if not in_list:
                        f2.write('<ul>\n')
                        in_list = True
                    f2.write('<li>' + line[1:].strip() + '</li>\n')

                else:
                    f2.write(line)
            if in_list:
                f2.write('</ul>\n')
                in_list = False
