from console_menu import GUI, Selection

query = '''\
Pick some numbers if you're brave enough.

    {}  {}  {}  {}  {}  {}  {}  {}
    {}  {}  {}  {}  {}  {}  {}  {}
    {}  {}  {}  {}  {}  {}  {}  {}
    {}  {}  {}  {}  {}  {}  {}  {}
    {}  {}  {}  {}  {}  {}  {}  {}
'''


if __name__ == '__main__':
    with GUI() as gui:
        gui.select_from_list(query, *map(Selection, range(5 * 8)))
