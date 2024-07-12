#!/usr/bin/python3
""" module that converts markdown to html """

import sys
import os
import hashlib
import re

def md5_hash(content):
    """Convert content to MD5 hash (lowercase)."""
    return hashlib.md5(content.encode()).hexdigest()

def remove_c(content):
    """Remove all 'c' characters (case insensitive) from content."""
    return re.sub(r'[cC]', '', content)

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
                line = line.replace('**', '<b>', 1)
                line = line.replace('**', '</b>', 1)
                line = line.replace('__', '<em>', 1)
                line = line.replace('__', '</em>', 1)

                if '[[' in line and ']]' in line:
                    content = re.search(r'\[\[(.*?)\]\]', line).group(1)
                    hashed_content = md5_hash(content)
                    line = re.sub(r'\[\[(.*?)\]\]', hashed_content, line)

                if '((' in line and '))' in line:
                    content = re.search(r'\(\((.*?)\)\)', line).group(1)
                    transformed_content = remove_c(content)
                    line = re.sub(r'\(\((.*?)\)\)', transformed_content, line)
                    line = line.strip()
                if line.startswith('#'):
                    if paragraph:
                        f2.write('</p>\n')
                        paragraph = False
                    count = len(line) - len(line.lstrip('#'))
                    f2.write('<h{}>{}</h{}>\n'
                             .format(count, line[count:]
                                     .strip(), count))

                elif line.startswith('- ') or line.startswith('* '):
                    if paragraph:
                        f2.write('</p>\n')
                        paragraph = False
                    if line.startswith('* '):
                        if not ordered:
                            if in_list:
                                f2.write('</ul>\n')
                                in_list = False
                            f2.write('<ol>\n')
                            ordered = True
                    elif line.startswith('- '):
                        if not in_list:
                            if ordered:
                                f2.write('</ol>\n')
                                ordered = False
                            f2.write('<ul>\n')
                            in_list = True
                    f2.write('<li>{}</li>\n'.format(line[2:].strip()))

                elif line == '':
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
                    f2.write('{}'.format(line))

            if in_list:
                f2.write('</ul>\n')
            if ordered:
                f2.write('</ol>\n')
            if paragraph:
                f2.write('</p>\n')

    sys.exit(0)
