from console_menu import GUI, Selection

query = '''\
Pick some numbers if you're brave enough.
    {}
{}
'''


if __name__ == '__main__':
    with GUI() as gui:
        gui.select(query, map(Selection, range(5)), Selection('Nah'))
        selection = gui.select_list([
            ['Hello, let me ask you a question'],
            ['- ', Selection('foo')],
            ['- ', Selection('bar'), ' or ', Selection('baz')]
        ])

        gui.select_list([
            'You choose %s! Correct?' % selection,
            [Selection('Yes'), ' ', Selection('No')]
        ])
