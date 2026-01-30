import flet as ft
from utils.config_loader import APP_DATA
from views.single_view import SingleVideoView
from views.batch_view import BatchVideoView
from views.credits_view import CreditsView

def main(page: ft.Page):
    # Configuración visual
    page.title = f"{APP_DATA['app_info']['name']} {APP_DATA['app_info']['version']}"
    page.window_width = APP_DATA['settings']['window_width']
    page.window_height = APP_DATA['settings']['window_height']
    page.theme_mode = ft.ThemeMode.DARK
    
    main_content = ft.Container(expand=True, padding=20)

    def change_view(e):
        idx = e.control.selected_index
        main_content.content = None
        
        if idx == 0:
            main_content.content = SingleVideoView(page)
        elif idx == 1:
            main_content.content = BatchVideoView(page)
        elif idx == 2:
            main_content.content = CreditsView()
        
        main_content.update()

    # SOLUCIÓN DE ÍCONOS: Usamos strings ("texto") en lugar de ft.icons.XXX
    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon="play_arrow",              # <--- STRING
                selected_icon="play_arrow",     # <--- STRING
                label="Convertir"
            ),
            ft.NavigationRailDestination(
                icon="folder",                  # <--- STRING
                selected_icon="folder_open",    # <--- STRING
                label="Lote"
            ),
            ft.NavigationRailDestination(
                icon="info",                    # <--- STRING
                selected_icon="info_outline",   # <--- STRING
                label="Créditos"
            ),
        ],
        on_change=change_view
    )

    main_content.content = SingleVideoView(page)

    page.add(
        ft.Row(
            [rail, ft.VerticalDivider(width=1), main_content],
            expand=True,
        )
    )

if __name__ == "__main__":
    # SOLUCIÓN ARRANQUE: Usamos target=main explícitamente
    ft.app(target=main)