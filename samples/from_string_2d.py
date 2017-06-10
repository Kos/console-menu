from console_menu import GUI, Selection

query = '''\
Pick some numbers if you're brave enough.

    [{:3}] [{:3}] [{:3}] [{:3}] [{:3}] [{:3}]  
    [{:3}] [{:3}] [{:3}] [{:3}] [{:3}] [{:3}]  
    [{:3}] [{:3}] [{:3}] [{:3}] [{:3}] [{:3}]  
    [{:3}] [{:3}] [{:3}] [{:3}] [{:3}] [{:3}]  
    [{:3}] [{:3}] [{:3}] [{:3}] [{:3}] [{:3}]  
'''


if __name__ == '__main__':
    with GUI() as gui:
        gui.select_from_string(query.format(*range(6*5)))
