import PySimpleGUI as SG
import VisualFunctions as f

label = SG.Text("Type in a todo")
input_box = SG.InputText(tooltip="Enter todo", key="todo")
b_ADD = SG.Button("Add")
box = SG.Listbox(values=f.get_items, key='todos',
                 enable_events=True, size=[45, 10])
b_EDIT = SG.Button("Edit")

layout = [[label], [input_box, b_ADD], [box, b_EDIT]]

window = SG.Window('My To-Do App', layout=layout, font=("Roboto", 20))
while True:
    event, values = window.read()
    print(f'{event}\n{values}')
    match event:
        case 'Add':
            todos = f.get_items()
            new = values["todo"] + '\n'
            todos.append(new)
            f.write_items(todos)
            window['todos'].update(values=todos)
        case 'Edit':
            to_edit = values['todos'][0]
            new_todo = values['todo'] + '\n'

            todos = f.get_items()
            index = todos.index(to_edit)
            todos[index] = new_todo
            f.write_items(todos)
            window['todos'].update(values=todos)
        case 'todos':
            print(values)
            if values['todos'] != '':
                window['todo'].update(value=values['todos'][0])
            else:
                print('Please add somthing to edit!')
                continue
        case SG.WIN_CLOSED:
            break

window.close()
