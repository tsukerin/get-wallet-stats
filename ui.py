import flet as ft
from utils import get_jettons, get_wallet_info, get_ton_balance, get_balance
import pandas as pd

def main(page: ft.Page):
    page.title = 'Wallet statistics'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window.width = 500
    page.window.height = 800

    page.fonts = {
        'Roboto Mono': 'fonts/RobotoMono-VariableFont_wght.ttf',
        'Ubuntu Mono': 'UbuntuMono-Bold.ttf'
    }

    input_field = ft.TextField(width=300, height=60)
    response = ft.Text(font_family='Roboto Mono', size=24)

    def create_graph():
        wallet = pd.read_excel('crypto_wallet.xlsx')

        data = [
            ft.LineChartData(
                data_points=[
                    ft.LineChartDataPoint(index, round(row['Сумма'])) for index, row in wallet.iterrows()
                ],
                stroke_width=3,
                color=ft.colors.CYAN,
                curved=True,
                stroke_cap_round=True,
            )
        ]
        chart = ft.LineChart(
            data_series=data,
            border=ft.border.all(3, ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE)),
            horizontal_grid_lines=ft.ChartGridLines(
                interval=1, color=ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE), width=1
            ),
            vertical_grid_lines=ft.ChartGridLines(
                interval=1, color=ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE), width=1
            ),
            left_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(
                        value=row['Сумма'],
                        label=ft.Text(row['Сумма'], size=14, weight=ft.FontWeight.BOLD),
                    )  for index, row in wallet.iterrows()
                ],
                labels_size=40,
            ),
            bottom_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(
                        value=index,
                        label=ft.Container(
                            ft.Text(
                                row['Дата'],
                                size=10,
                                weight=ft.FontWeight.BOLD,
                                color=ft.colors.with_opacity(0.5, ft.colors.ON_SURFACE),
                                rotate=175
                            ),
                            margin=ft.margin.only(top=10),
                        ),
                    ) for index, row in wallet.iterrows()
                ],
                labels_size=32,
            ),
            tooltip_bgcolor=ft.colors.with_opacity(0.8, ft.colors.BLUE_GREY),
            min_y=min(wallet['Сумма']),
            max_y=max(wallet['Сумма']),
            min_x=0,
            max_x=wallet.shape[0],
            animate=5000,
            expand=True,
        )

        page.add(ft.Row([
            ft.Text(value='История ценности кошелька', font_family='Ubuntu Mono')
        ], alignment=ft.MainAxisAlignment.CENTER),
        chart)

    def navigate(e):
        page.clean()

        if page.navigation_bar.selected_index == 0:
            page.add(auth_page, ft.Row([response], alignment=ft.MainAxisAlignment.CENTER))
        if page.navigation_bar.selected_index == 1:
            create_graph()

    def get_net_worth(e):
        wallet = input_field.value
        balances = get_wallet_info(wallet)
        fton, jton = get_ton_balance(wallet)

        jettons = ft.Column(
            height=400,
            width=800,
            scroll=ft.ScrollMode.ALWAYS,
            on_scroll_interval=0,
        )

        page.clean()

        for image, name, jbalance, balance in get_jettons(balances, wallet):
            jettons.controls.append(
                ft.Container(content=ft.Row([
                    ft.Image(src=image, width=45, height=45, border_radius=ft.border_radius.all(50)),
                    ft.Column([
                        ft.Text(value=name, size=13),
                        ft.Row([
                            ft.Text(value=jbalance),
                            ft.Text(value=str(balance) + '$')
                        ])
                    ])
                ]), padding=15, margin=4, width=700, height=85, bgcolor='#161819', border_radius=30)
            )

        page.add(
            ft.Row([
                ft.Text(value='Баланс кошелька', font_family='Ubuntu Mono', size=30),
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([
                ft.Text(value=str(get_balance(balances, wallet)) + '$', font_family='Ubuntu Mono', size=15)
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(content=ft.Row([
                ft.Image(src='https://ton.org/download/ton_symbol.png', width=45, height=45, border_radius=ft.border_radius.all(50)),
                ft.Column([
                    ft.Text(value='Toncoin', size=13),
                    ft.Row([
                        ft.Text(value=jton),
                        ft.Text(value=str(round(fton, 2)) + '$')
                    ])
                ])
            ]), padding=15, margin=4, width=700, height=85, bgcolor='#161819', border_radius=30)
        )

        page.add(jettons)

        page.navigation_bar.destinations.append(
            ft.NavigationBarDestination(icon=ft.icons.BAR_CHART_ROUNDED, selected_icon=ft.icons.BAR_CHART_OUTLINED)
        )

        page.update()

    auth_page = ft.Row([
        ft.Column([
            ft.Text(value='Отображение ценности кошелька', font_family='Ubuntu Mono', size=16),
            input_field,
            ft.ElevatedButton(text='OK', on_click=get_net_worth),
        ])
    ], alignment=ft.MainAxisAlignment.CENTER)

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.icons.HOME, selected_icon=ft.icons.HOME_OUTLINED),
        ], on_change=navigate, height=80
    )

    page.add(auth_page)

ft.app(target=main, view=ft.AppView.FLET_APP)
