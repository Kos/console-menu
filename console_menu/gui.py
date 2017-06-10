import six
import curses

from .selection import Selection
from .definitions import from_args, from_string

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
    def __init__(self, mock=False):
        if mock:
            from mock import MagicMock
            global curses
            curses = MagicMock()

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
        print('!!', definition)
        self.definition = definition
        # TODO definition.get_selections()
        self.selections = [bit for line in definition for bit in line
                           if isinstance(bit, Selection)]
        self.selection = 0
        self.paint()
        while True:
            key = stdscr.getch()
            if key == curses.KEY_DOWN:
                self.selection += 1
            elif key == curses.KEY_UP:
                self.selection -= 1
            elif key == curses.KEY_RIGHT:
                self.selection += 1
            elif key == curses.KEY_LEFT:
                self.selection -= 1
            elif key in [ord('q'), 27]:
                raise UserAbort()
            elif key in [curses.KEY_ENTER, 10]:
                break
            else:
                continue
            self.selection = (self.selection + len(self.selections)) % len(self.selections)
            self.paint()

        stdscr.clear()
        if not self.selections:
            return None
        return self.selections[self.selection].value

    def paint(self):
        y, x = 0, 0
        selection_index = 0
        for line in self.definition:
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
