#!/usr/bin/python3
""" module that converts markdown to html """

import sys
import os

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html",
              file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(sys.argv[1]):
        print("Missing {}".format(sys.argv[1]), file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        with open(sys.argv[2], 'w') as f2:
            in_list = False
            ordered = False
            paragraph = False

            for line in f:
                stripped_line = line.strip()

                if stripped_line.startswith('#'):
                    if paragraph:
                        f2.write('</p>\n')
                        paragraph = False
                    count = len(stripped_line) - len(stripped_line.lstrip('#'))
                    f2.write('<h{}>{}</h{}>\n'.format(count, stripped_line[count:].strip(), count))

                elif stripped_line.startswith('- ') or stripped_line.startswith('* '):
                    if paragraph:
                        f2.write('</p>\n')
                        paragraph = False
                    if stripped_line.startswith('* '):
                        if not ordered:
                            if in_list:
                                f2.write('</ul>\n')
                                in_list = False
                            f2.write('<ol>\n')
                            ordered = True
                    elif stripped_line.startswith('- '):
                        if not in_list:
                            if ordered:
                                f2.write('</ol>\n')
                                ordered = False
                            f2.write('<ul>\n')
                            in_list = True
                    f2.write('<li>{}</li>\n'.format(stripped_line[2:].strip()))

                elif stripped_line == '':
                    if paragraph:
                        f2.write('</p>\n')
                        paragraph = False
                    elif in_list:
                        f2.write('</ul>\n')
                        in_list = False
                    elif ordered:
                        f2.write('</ol>\n')
                        ordered = False

                else:
                    if in_list:
                        f2.write('</ul>\n')
                        in_list = False
                    if ordered:
                        f2.write('</ol>\n')
                        ordered = False
                    if not paragraph:
                        f2.write('<p>')
                        paragraph = True
                    else:
                        f2.write('<br/>')
                    f2.write('{}'.format(stripped_line))

            if in_list:
                f2.write('</ul>\n')
            if ordered:
                f2.write('</ol>\n')
            if paragraph:
                f2.write('</p>\n')

    sys.exit(0)
