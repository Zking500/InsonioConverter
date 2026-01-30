import flet as ft
from utils.config_loader import APP_DATA

def CreditsView():
    # 1. Extraemos las secciones para escribir menos código
    info = APP_DATA['app_info']
    links = APP_DATA['urls']
    # Usamos etiquetas por defecto si no existen en el config
    labels = APP_DATA.get('ui_labels', {
        'lbl_developer': 'Desarrollador:',
        'lbl_company': 'Empresa:',
        'btn_donate': 'Donar',
        'btn_github': 'GitHub',
        'btn_web': 'Web'
    })

    return ft.Column([
        ft.Icon(name="terminal", size=80, color=ft.Colors.CYAN),
        
        # Usamos info del JSON
        ft.Text(info['name'], size=40, weight="bold", color=ft.Colors.CYAN),
        ft.Text(f"Versión: {info['version']}", italic=True),
        
        ft.Divider(thickness=2),
        
        # Usamos etiquetas (labels) del JSON + datos
        ft.Text(f"{labels['lbl_developer']} {info['developer']}"),
        ft.Text(f"{labels['lbl_company']} {info['company']}", weight="bold"),
        
        ft.Container(height=20),
        
        ft.Row([
            # Botones usando texto y links del JSON
            ft.ElevatedButton(labels['btn_donate'], icon="payment", url=links['donation']),
            ft.ElevatedButton(labels['btn_github'], icon="code", url=links['github']),
            ft.ElevatedButton(labels['btn_web'], icon="public", url=links['website']),
        ], alignment=ft.MainAxisAlignment.CENTER)
        
    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)