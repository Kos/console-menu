# console-menu

a tool for immediate-mode menus, based on `curses`

## immediate what?

Long story short:

- call a function such as GUI.select()
- in the function parameters, describe how the GUI should look like
- the function blocks until the user picks a selection
- you can ask a question, obtain a result and move on:

      value = GUI.select(from_string('''[Yes] [No]'''))
