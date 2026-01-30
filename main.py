# main.py
import flet as ft
from views.single_view import SingleVideoView
from views.batch_view import BatchVideoView
from views.credits_view import CreditsView
from utils.config_loader import APP_DATA

def main(page: ft.Page):
    page.title = f"{APP_DATA['app_info']['name']} - {APP_DATA['app_info']['version']}"
    page.window_width = APP_DATA['settings']['window_width']
    page.window_height = APP_DATA['settings']['window_height']
    page.theme_mode = ft.ThemeMode.DARK
    # Contenedor principal donde cambiaremos el contenido
    main_content = ft.Container(expand=True, padding=20)

    def change_view(e):
        selected = e.control.selected_index
        main_content.content = None # Limpiar
        
        if selected == 0:
            main_content.content = SingleVideoView(page)
        elif selected == 1:
            main_content.content = BatchVideoView(page)
        elif selected == 2:
            main_content.content = CreditsView()
        
        main_content.update()

    # Barra lateral de navegación
    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=400,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(icon=ft.icons.MOVIE, label="1 Video"),
            ft.NavigationRailDestination(icon=ft.icons.VIDEO_LIBRARY, label="Lote"),
            ft.NavigationRailDestination(icon=ft.icons.INFO, label="Créditos"),
        ],
        on_change=change_view
    )

    # Inicializar con la primera vista
    main_content.content = SingleVideoView(page)

    # Layout Principal: Barra a la izquierda, contenido a la derecha
    page.add(
        ft.Row(
            [rail, ft.VerticalDivider(width=1), main_content],
            expand=True,
        )
    )

ft.app(target=main)