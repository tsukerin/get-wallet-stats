import flet as ft
import sqlite3

def main(page: ft.Page):
    page.title = 'Test'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_height = 800
    page.window_width = 500

    def account(e):
        pass

    def auth(e):
        db = sqlite3.connect('db')
        cur = db.cursor()

        cur.execute(
            f'select * from users where login = {login_field.value} and password = {password_field.value}'
        )
        print(cur.fetchone())
        login_field.value = ''
        password_field.value = ''
        confirm_pass_field.value = ''
        if cur.fetchone() != None:
            notify_text.value = 'Auththorization successful!'
        else:
            notify_text.value = 'The username or password is incorrect'

        db.commit()
        db.close()

        page.navigation_bar.destinations.append(
            ft.NavigationDestination(icon=ft.icons.ACCOUNT_BOX, label='Account', selected_icon=ft.icons.ACCOUNT_BOX_OUTLINED)
        )

        page.update()

    def register(e):
        db = sqlite3.connect('db')
        cur = db.cursor()
        if login_field.value in cur.fetchall():
            notify_text.value = 'Login already exists!'
        else:
            if confirm_pass_field.value == password_field.value:
                cur.execute(
                    '''
                    create table if not exists users(
                    id integer primary key,
                    login text,
                    password text
                    )
                    '''
                )
                cur.execute(f"insert into users values(null, '{login_field.value}', '{password_field.value}')")

                db.commit()
                db.close()

                login_field.value = ''
                password_field.value = ''
                confirm_pass_field.value = ''
                notify_text.value = 'Registration successful!'
            else:
                notify_text.value = 'Passwords do not match!'

        
        page.update()

    def validate(e):
        if login_field.value and password_field.value:
            confirm_signup_btn.disabled, confirm_signin_btn.disabled = False, False
        else:
            confirm_signin_btn.disabled, confirm_signup_btn.disabled = True, True

        page.update()

    def navigate(e):
        page.clean()

        if page.navigation_bar.selected_index == 0:
            page.add(greets)
        if page.navigation_bar.selected_index == 1:
            page.add(register)
        if page.navigation_bar.selected_index == 2:
            page.add(auth)
        if page.navigation_bar.selected_index == 3:
            page.add(lc)

    login_field = ft.TextField(label='Login', width=200, height=50, on_change=validate)
    password_field = ft.TextField(label='Password', password=True, width=200, height=50, on_change=validate)
    confirm_pass_field = ft.TextField(label='Confirm password', password=True, width=200, height=50, on_change=validate)
    confirm_signup_btn = ft.OutlinedButton(text='Sign up', width=200, disabled=True, on_click=register)
    confirm_signin_btn = ft.OutlinedButton(text='Sign in', width=200, disabled=True, on_click=auth)
    notify_text = ft.Text(value='', text_align=ft.TextAlign.CENTER)

    register = ft.Row(
            [
                ft.Column(
                    [
                        ft.Text('Sign up'),
                        login_field,
                        password_field,
                        confirm_pass_field,
                        confirm_signup_btn,
                        notify_text
                    ]
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    auth = ft.Row(
            [
                ft.Column(
                    [
                        ft.Text('Sign in'),
                        login_field,
                        password_field,
                        confirm_signin_btn,
                        notify_text
                    ]
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    greets = ft.Row([
        ft.Column([
            ft.Text(value='Welcome to simulator "Auth and register"!', size=24)
        ])
    ], alignment=ft.MainAxisAlignment.CENTER)
    lc = ft.Row([
        ft.Column([
            ft.Text(value='Account')
        ])
    ], alignment=ft.MainAxisAlignment.CENTER)
    
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.HOME, label='Home'),
            ft.NavigationDestination(icon=ft.icons.ACCESSIBILITY_NEW, label='Sign up'),
            ft.NavigationDestination(icon=ft.icons.LOGIN, label='Sign in'),
        ], on_change=navigate, height=80
    )

    page.add(greets)

ft.app(target=main)