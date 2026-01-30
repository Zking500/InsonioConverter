import flet as ft
from utils.config_loader import APP_DATA
from views.single_view import SingleVideoView
from views.batch_view import BatchVideoView
from views.credits_view import CreditsView
from views.config_view import ConfigView
from views.processing_view import ProcessingView

def main(page: ft.Page):
    # --- Configuración Básica ---
    page.title = APP_DATA['app_info']['name']
    page.window_width = APP_DATA['settings']['window_width']
    page.window_height = APP_DATA['settings']['window_height']
    page.theme_mode = "dark"  # En 0.28.3 usamos string simple "dark" o "light"
    page.padding = 20

    # --- Estado de la App ---
    state = {
        "current_view": None
    }

    # --- Manejador Drag & Drop Global ---
    def on_file_drop(e: ft.FilePickerResultEvent):
        file_path = e.files[0].path if e.files else None
        if not file_path: return

        if isinstance(state["current_view"], SingleVideoView):
            state["current_view"].set_file(file_path)
            mostrar_alerta(f"Archivo cargado: {e.files[0].name}", "green")
        elif isinstance(state["current_view"], BatchVideoView):
            state["current_view"].add_file(file_path)
            mostrar_alerta(f"Añadido a la cola: {e.files[0].name}", "green")
        else:
            mostrar_alerta("Ve a 'Convertir' o 'Lote' para usar archivos.", "amber")

    page.on_file_drop = on_file_drop 

    # --- Sistema de Alertas (Simplificado) ---
    def mostrar_alerta(texto, color):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(texto, color="white"),
            bgcolor=color,
        )
        page.snack_bar.open = True
        page.update()

    # --- Navegación ---
    def change_view(e):
        idx = e.control.selected_index
        main_content.content = None
        
        if idx == 0:
            state["current_view"] = SingleVideoView(page, change_to_processing)
        elif idx == 1:
            state["current_view"] = BatchVideoView(page)
        elif idx == 2:
            state["current_view"] = ConfigView(page)
        elif idx == 3:
            state["current_view"] = CreditsView()
            
        main_content.content = state["current_view"]
        main_content.update()

    def change_to_processing(mode, file_path, options):
        state["current_view"] = ProcessingView(page, mode, file_path, options, on_finish=lambda: print("Fin"))
        main_content.content = state["current_view"]
        main_content.update()

    rail = ft.NavigationRail(
        selected_index=0,
        label_type="all", # En versiones viejas a veces es string o enum simple
        min_width=100,
        min_extended_width=200,
        group_alignment=-0.9,
        expand=True,  # Agregamos expand=True para solucionar el error de altura
        destinations=[
            ft.NavigationRailDestination(icon="movie_creation_outlined", selected_icon="movie_creation", label="Convertir"),
            ft.NavigationRailDestination(icon="queue_play_next_outlined", selected_icon="queue_play_next", label="Lote"),
            ft.NavigationRailDestination(icon="settings_outlined", selected_icon="settings", label="Ajustes"),
            ft.NavigationRailDestination(icon="info_outlined", selected_icon="info", label="Info"),
        ],
        on_change=change_view
    )

    def toggle_theme(e):
        page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
        e.control.icon = "dark_mode" if page.theme_mode == "light" else "light_mode"
        page.update()

    theme_btn = ft.IconButton(icon="light_mode", on_click=toggle_theme, tooltip="Cambiar Tema")

    main_content = ft.Container(expand=True, padding=10)
    
    # Iniciar vista
    state["current_view"] = SingleVideoView(page, change_to_processing)
    main_content.content = state["current_view"]

    page.add(
        ft.Row(
            [
                ft.Column([rail, ft.Container(content=theme_btn, padding=10)], alignment="spaceBetween"),
                ft.VerticalDivider(width=1, color="grey"),
                main_content
            ],
            expand=True,
        )
    )

if __name__ == "__main__":
    ft.app(target=main)