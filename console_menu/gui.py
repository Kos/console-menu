import curses

import six

from .definitions import from_args, from_string, Definition
from .selection import Selection

stdscr = None


def start():
    global stdscr
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    stdscr.keypad(1)


def stop():
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()


class UserAbort(Exception):
    pass


class GUI(object):
    def __init__(self):
        pass

    def __enter__(self):
        start()
        return self

    def __exit__(self, *args):
        stop()

    def select_from_list(self, str, *args):
        return self.select(from_args(str, *args))

    def select_from_string(self, string):
        return self.select(from_string(string))

    def select(self, definition):
        if not isinstance(definition, Definition):
            definition = Definition(definition)

        self.definition = definition
        self.selections = definition.selections
        self.selection = 0
        self.paint()
        while True:
            key = stdscr.getch()
            if key in (curses.KEY_DOWN, curses.KEY_UP, curses.KEY_RIGHT, curses.KEY_LEFT):
                self.selection = self.definition.advance_selection(self.selection, key)
            elif key in [ord('q'), 27]:
                raise UserAbort()
            elif key in [curses.KEY_ENTER, 10]:
                break
            else:
                continue
            self.paint()

        stdscr.clear()
        if not self.selections:
            return None
        return self.selections[self.selection].value

    def paint(self):
        y, x = 0, 0
        selection_index = 0
        for line in self.definition.lines:
            for bit in line:
                if isinstance(bit, six.string_types):
                    stdscr.addstr(y, x, bit)
                    x += len(bit)
                elif isinstance(bit, Selection):
                    style = curses.A_REVERSE if selection_index == self.selection else curses.A_UNDERLINE
                    stdscr.addstr(y, x, bit.label, style)
                    x += len(bit.label)
                    selection_index += 1
            y += 1
            x = 0
