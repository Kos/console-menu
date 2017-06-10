import curses
import six

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


class Selection(object):
    def __init__(self, label, value=None):
        self.label = str(label)
        self.value = value if value is not None else label

    def __repr__(self):
        return 'Selection(%s)' % self.label


class UserAbort(Exception):
    pass


class GUI(object):
    def __enter__(self):
        start()
        return self

    def __exit__(self, *args):
        stop()

    def select(self, str, *args):
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
            line_arr = []
            for token in split_tokens(line):
                if token == '':
                    continue
                if token == '{}':
                    line_arr.extend(unpack_arg(args.pop(0)))
                else:
                    line_arr.append(token)
            lines.append(line_arr)
        return self.select_list(lines)

    def select_list(self, lines):
        self.lines = lines
        self.selections = [bit for line in lines for bit in line
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

        stdscr.erase()
        if not self.selections:
            return None
        return self.selections[self.selection].value

    def paint(self):
        y, x = 0, 0
        selection_index = 0
        for line in self.lines:
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
