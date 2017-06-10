from console_menu import GUI

if __name__ == '__main__':
    with GUI() as gui:
        value = gui.select_from_string('''Pick a choice: [Yes] [No]''')
    print("You have selected", value)
