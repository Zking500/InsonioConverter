import flet as ft

def CreditsView():
    return ft.Column([
        ft.Icon(ft.icons.ROCKET_LAUNCH, size=50, color="orange"),
        ft.Text("Z-Converter Pro", size=30, weight="bold"),
        ft.Text("Desarrollado por Z King @ S&O Systems", italic=True),
        ft.Divider(),
        ft.Text("Si esta herramienta te ahorró tiempo, considera donar:"),
        ft.ElevatedButton("☕ Comprar un café", url="https://paypal.me/tucuenta", icon=ft.icons.PAYMENT),
        ft.Text("v1.0.0 - Hecho con Python & Flet")
    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)