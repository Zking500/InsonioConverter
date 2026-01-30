import flet as ft
from utils.config_loader import APP_DATA

def CreditsView():
    info = APP_DATA['app_info']
    links = APP_DATA['urls']

    return ft.Column([
        # CORREGIDOS TODOS LOS ICONOS A STRINGS
        ft.Icon(name="terminal", size=80, color=ft.colors.CYAN), # "terminal" en lugar de CODE
        ft.Text(info['name'], size=40, weight="bold", color=ft.colors.CYAN),
        ft.Text(f"Versión: {info['version']}", italic=True),
        ft.Divider(thickness=2),
        ft.Text(f"Desarrollador: {info['developer']}"),
        ft.Text(f"Compañía: {info['company']}", weight="bold"),
        ft.Container(height=20),
        ft.Row([
            ft.ElevatedButton("Donar", icon="payment", url=links['donation']),
            ft.ElevatedButton("GitHub", icon="code", url=links['github']),
            ft.ElevatedButton("Web", icon="public", url=links['website']), # "public" es el icono de mundo/web
        ], alignment=ft.MainAxisAlignment.CENTER)
    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)