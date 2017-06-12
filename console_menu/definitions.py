import curses
import re
from collections import namedtuple

import six

from .selection import Selection

PlacedSelection = namedtuple('PlacedSelection', 'sel x y index')


class Definition(object):

    def __init__(self, lines):
        self.lines = list(lines)
        for line in self.lines:
            if not isinstance(line, (list, tuple)):
                raise ValueError("Each line should be a list")
            for bit in line:
                if not isinstance(bit, (Selection)) and not isinstance(bit, six.string_types):
                    raise ValueError("Each line bit should be a string or a Selection")

    @property
    def selections_with_coords(self):
        x = 0
        y = 0
        index = 0
        for line in self.lines:
            for bit in line:
                if isinstance(bit, Selection):
                    yield PlacedSelection(bit, x, y, index)
                    x += len(bit.label)
                    index += 1
                else:
                    x += len(bit)
            y += 1
            x = 0

    @property
    def selections(self):
        return [ps.sel for ps in self.selections_with_coords]

    @property
    def selections_per_line(self):
        y = 0
        tup = []
        for placed_selection in self.selections_with_coords:
            if placed_selection.y != y:
                # reset line
                if tup:
                    yield y, tup
                # re-init
                y = placed_selection.y
                tup = [placed_selection]
            else:
                tup.append(placed_selection)
        if tup:
            yield y, tup

    def advance_selection(self, selection, key):
        if not self.selections:
            return selection

        if key == curses.KEY_DOWN:
            current_coords = self.get_coords(selection)
            selection = self.get_closest(current_coords).index
        elif key == curses.KEY_UP:
            current_coords = self.get_coords(selection)
            selection = self.get_closest_reverse(current_coords).index
        elif key == curses.KEY_RIGHT:
            selection += 1
        elif key == curses.KEY_LEFT:
            selection -= 1

        # Overflow?
        selection = (selection + len(self.selections)) % len(self.selections)
        return selection

    def get_coords(self, index):
        return list(self.selections_with_coords)[index]

    def get_closest(self, placed_selection):
        def distance_to_x(ps):
            return (
                abs(placed_selection.x - ps.x),
                -ps.x # in case of a tie, prefer LARGER x
            )
        for [y, line] in self.selections_per_line:
            if y <= placed_selection.y:
                continue
            return min(line, key=distance_to_x)
        return placed_selection

    def get_closest_reverse(self, placed_selection):
        def distance_to_x(ps):
            return (
                abs(placed_selection.x - ps.x),
                ps.x  # in case of a tie, prefer SMALLER x
            )
        for [y, line] in reversed(list(self.selections_per_line)):
            if y >= placed_selection.y:
                continue
            return min(line, key=distance_to_x)
        return placed_selection


def from_args(str, *args):
    def split_tokens(line):
        while line:
            a, b, line = line.partition('{}')
            yield a
            if b:
                yield b

    def unpack_arg(arg):
        if isinstance(arg, Selection):
            yield arg
        else:
            arg = list(arg)
            while arg:
                yield arg.pop(0)
                if arg:
                    yield ' '

    args = list(args)
    lines = []
    for line in str.splitlines():
        print('Digging line', line)
        line_arr = []
        for token in split_tokens(line):
            if token == '':
                continue
            if token == '{}':
                print('Pop!', len(args))
                line_arr.extend(unpack_arg(args.pop(0)))
            else:
                line_arr.append(token)
        lines.append(line_arr)
    return Definition(lines)


def from_string(string):
    lines = string.splitlines()

    def convert(s):
        bits = re.split('(\[[^]]+\])', s)
        for i, bit in enumerate(bits):
            if i % 2 == 1:
                yield Selection(bit, bit[1:-1])
            else:
                yield bit

    return Definition([
        list(convert(line))
        for line in lines
    ])
