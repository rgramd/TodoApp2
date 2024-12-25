import PySimpleGUI as sg
import VisualFunctions as f

label = sg.Text("Type in a todo")
input_box = sg.InputText(tooltip="Enter todo", key="todo")
b_ADD = sg.Button("Add")
lis_box = sg.Listbox(values=f.get_items(), key='todos',
                 enable_events=True, size=[45, 10])
b_EDIT = sg.Button("Edit")
b_COMPLETE = sg.Button("Complete")
b_EXIT = sg.Button("Exit")

layout = [[label], [input_box, b_ADD], [lis_box, b_EDIT, b_COMPLETE], [b_EXIT]]

window = sg.Window('My To-Do App', layout=layout, font=("Roboto", 20))
while True:
    event, values = window.read()
    print(f'{event}\n{values}')
    match event:
        case 'Add':
            todos = f.get_items()
            new = values["todo"]
            todos.append(new)
            f.write_items(todos)
            window['todos'].update(values=todos)
        case 'Edit':
            to_edit = values['todos'][0]
            new_todo = values['todo']

            tasks = f.get_items()
            to_edit_index = tasks.index(to_edit)
            tasks[to_edit_index] = new_todo
            f.write_items(tasks)
            window['todos'].update(values=tasks) #window['todos'] is
            # the listbox that all items are stored in,
            # update will change it on the spot instead of having to refresh the program
        case 'Complete':
            to_complete = values[todos][0]
            tasks = f.get_items()
            tasks.remove(to_complete)
            f.write_items(tasks)
            window['todos'].update(values=tasks)
            window['todo'].update(value='')
        case "Exit":
            break
        case 'todos':
                window['todo'].update(value=values['todos'][0])
        case sg.WIN_CLOSED:
            break

window.close()
