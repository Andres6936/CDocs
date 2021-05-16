# This file is part of cldoc.  cldoc is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import os, subprocess, sys

from typing import List

from logger.consolelogger import ConsoleLogger
from logger.ilogger import ILogger


def _extract_include_paths(compilation_flags: str) -> str:
    """
    Generally the compilation flags come with flags that are not used for our
    goal, that is extract all the include path that are used when compiling
    the program. These paths are easily identifiable because they begin
    with '-I/'
    :param compilation_flags: The compilation flags used for compiling the
    program.
    :return: The path of inclusion separated for a space
    """
    arguments: List[str] = compilation_flags.split(' ')
    result: str = str()
    for argument in arguments:
        if argument.startswith('-I/'):
            result += argument + ' '
    # In this point, the string include a space to end of string, with this
    # approximation. remove it space.
    # If the space is present at end of string, CLang will not find the
    # directory and will be ignore it.
    return result[:-1]


def __add_prefix_of_inclusion(paths_of_inclusion: List[str]) -> List[str]:
    return ['-I' + path for path in paths_of_inclusion]


def flags(f: str) -> List[str]:
    logger: ILogger = ConsoleLogger()
    logger.informational("Entering the flag definition")
    logger.informational("The flags defined has been: {}".format(f))
    logger.informational("Opening the devnull device ({})".format(os.devnull))
    devnull = open(os.devnull)

    f = _extract_include_paths(f)

    command: List[str] = ['clang++', '-E', '-xc++', f, '-v', '-']
    logger.informational("The command to execute is: {}".format(command))

    try:
        p = subprocess.Popen(command,
                             stdin=devnull,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    except OSError as e:
        sys.stderr.write(
            "\nFatal: Failed to run clang++ to obtain system include headers, please install clang++ to use cldoc\n")

        message = str(e)

        if message:
            sys.stderr.write("  Error message: " + message + "\n")

        sys.stderr.write("\n")
        sys.exit(1)

    devnull.close()

    lines = p.communicate()[1].splitlines()
    init = False
    paths = []

    for line in lines:
        if line.startswith(b'#include <...>'):
            init = True
        elif line.startswith(b'End of search list.'):
            init = False
        elif init:
            p = line.strip()

            suffix = b' (framework directory)'

            if p.endswith(suffix):
                p = p[:-len(suffix)]

            paths.append(p)
    return __add_prefix_of_inclusion([path.decode('utf-8') for path in paths])

# vi:ts=4:et
