import re

from .selection import Selection


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
    return lines


def from_string(string):
    lines = string.splitlines()

    def convert(s):
        bits = re.split('(\[[^]]+\])', s)
        for i, bit in enumerate(bits):
            if i % 2 == 1:
                yield Selection(bit, bit[1:-1])
            else:
                yield bit

    return [
        list(convert(line))
        for line in lines
    ]
