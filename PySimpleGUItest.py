import PySimpleGUI as sg


def enter(users):
    layout = [  [sg.Button('Новый пользователь', font=('Helvetica', 16))],
                [sg.Combo(users, font=('Helvetica', 16))],
                [sg.Text('Пароль:', font=('Helvetica', 16)), sg.InputText(password_char='*', font=('Helvetica', 16), size=(20, 1))],
                [sg.Button('Ok', font=('Helvetica', 16)), sg.Button('Cancel', font=('Helvetica', 16))] ]

    window = sg.Window('Window Title', layout, element_justification='center')
    event, values = window.read()

    window.close()
    return event, values


def new_user():
    pass


def login(user, password):
    pass


event, values = enter(users=['user1', 'user2'])