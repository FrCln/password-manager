import PySimpleGUI as sg


def enter(users):
    layout = [  [sg.Button('Новый пользователь', font=('Helvetica', 16))],
                [sg.Combo(users, font=('Helvetica', 16))],
                [sg.Text('Пароль:', font=('Helvetica', 16)),
                    sg.InputText(password_char='*', font=('Helvetica', 16), size=(20, 1))],
                [sg.Button('Ok', font=('Helvetica', 16)), sg.Button('Cancel', font=('Helvetica', 16))] ]

    window = sg.Window('Вход', layout, element_justification='center')
    event, values = window.read()

    window.close()
    return event, values


def new_user(users):
    layout = [  [sg.Text('Имя пользователя:', font=('Helvetica', 16)),
                    sg.InputText(font=('Helvetica', 16), size=(20, 1))],
                [sg.Text('Пароль:', font=('Helvetica', 16)),
                    sg.InputText(password_char='*', font=('Helvetica', 16), size=(20, 1))],
                [sg.Text('Пароль еще раз:', font=('Helvetica', 16)),
                    sg.InputText(password_char='*', font=('Helvetica', 16), size=(20, 1))],
                [sg.Button('Ok', font=('Helvetica', 16)), sg.Button('Cancel', font=('Helvetica', 16))] ]

    window = sg.Window(
        'Новый пользователь',
        layout,
        element_justification='center',
        # return_keyboard_events=True
    )
    while True:
        event, values = window.read()
        print(event, values)
        if event == 'Cancel' or event is None:
            break
        elif event == 'Ok':
            if values[0] == '':
                sg.Popup(
                    'Введите имя!',
                    font=('Helvetica', 16)
                )
            elif values[0] in users:
                sg.Popup(
                    'Пользователь с таким именем уже существует',
                    font=('Helvetica', 16)
                )

    window.close()
    return event, values


def login(user, password):
    pass


event, values = enter(users=['user1', 'user2'])
if event == 'Новый пользователь':
    event, values = new_user(users=['user1', 'user2'])
