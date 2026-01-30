import flet as ft
from utils.config_loader import APP_DATA, save_config # Necesitarás crear save_config en utils
from views.single_view import SingleVideoView
from views.batch_view import BatchVideoView
from views.credits_view import CreditsView
from views.config_view import ConfigView # Nueva vista
from views.processing_view import ProcessingView # Nueva vista

def main(page: ft.Page):
    # --- Configuración Visual Global ---
    page.title = APP_DATA['app_info']['name']
    page.window_width = APP_DATA['settings']['window_width']
    page.window_height = APP_DATA['settings']['window_height']
    page.theme_mode = ft.ThemeMode.DARK # Empezamos en Dark
    
    # Fuentes y temas modernos
    page.theme = ft.Theme(
        color_scheme_seed=ft.colors.CYAN,
        visual_density=ft.VisualDensity.COMFORTABLE,
        font_family="Roboto" # O la que prefieras
    )

    # --- Estado de la App (Variables compartidas) ---
    state = {
        "current_view": None, # Referencia a la clase de la vista actual
        "selected_file": None,
        "batch_files": []
    }

    # --- Manejador Drag & Drop Global ---
    def on_file_drop(e: ft.FilePickerResultEvent):
        # Obtenemos la ruta del primer archivo soltado
        file_path = e.files[0].path if e.files else None
        if not file_path: return

        # Lógica inteligente: ¿A dónde va el archivo?
        if isinstance(state["current_view"], SingleVideoView):
            state["current_view"].set_file(file_path)
            mostrar_alerta(f"📂 Archivo cargado: {e.files[0].name}", "green")
        elif isinstance(state["current_view"], BatchVideoView):
            state["current_view"].add_file(file_path)
            mostrar_alerta(f"📂 Añadido a la cola: {e.files[0].name}", "green")
        else:
            mostrar_alerta("⚠️ Ve a la pestaña 'Convertir' o 'Lote' para soltar archivos.", "amber")

    page.on_file_drop = on_file_drop 

    # --- Sistema de Alertas Moderno ---
    def mostrar_alerta(texto, color):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(texto, color="white", weight="bold"),
            bgcolor=color,
            behavior=ft.SnackBarBehavior.FLOATING,
            shape=ft.RoundedRectangleBorder(radius=10),
            show_close_icon=True
        )
        page.snack_bar.open = True
        page.update()

    # --- Navegación ---
    def change_view(e):
        idx = e.control.selected_index
        main_content.content = None
        
        # Animación de salida (opcional, simplificada aquí)
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

    # Callback para cambiar a pantalla de carga desde las vistas
    def change_to_processing(mode, file_path, options):
        state["current_view"] = ProcessingView(page, mode, file_path, options, on_finish=lambda: rail.on_change(ft.ControlEvent(control=rail)))
        main_content.content = state["current_view"]
        main_content.update()

    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(icon="movie_creation_outlined", selected_icon="movie_creation", label="Convertir"),
            ft.NavigationRailDestination(icon="queue_play_next_outlined", selected_icon="queue_play_next", label="Lote"),
            ft.NavigationRailDestination(icon="settings_outlined", selected_icon="settings", label="Ajustes"),
            ft.NavigationRailDestination(icon="info_outlined", selected_icon="info", label="Info"),
        ],
        on_change=change_view
    )

    # Botón Flotante para cambiar Tema (Blanco/Negro)
    def toggle_theme(e):
        page.theme_mode = ft.ThemeMode.LIGHT if page.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        e.control.icon = "dark_mode" if page.theme_mode == ft.ThemeMode.LIGHT else "light_mode"
        page.update()

    theme_btn = ft.IconButton(icon="light_mode", on_click=toggle_theme, tooltip="Cambiar Tema")

    main_content = ft.Container(expand=True, padding=20)
    # Inicializar vista
    state["current_view"] = SingleVideoView(page, change_to_processing)
    main_content.content = state["current_view"]

    # Layout Principal
    page.add(
        ft.Row(
            [
                ft.Column([rail, ft.Container(content=theme_btn, padding=10)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.VerticalDivider(width=1, color=ft.colors.with_opacity(0.1, "grey")),
                main_content
            ],
            expand=True,
        )
    )

if __name__ == "__main__":
    ft.app(target=main)