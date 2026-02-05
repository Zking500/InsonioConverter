import flet as ft
import asyncio
from utils.config_loader import APP_DATA
from utils.welcome_window import WelcomeWindow
from views.single_view import SingleVideoView
from views.batch_view import BatchVideoView
from views.credits_view import CreditsView
from views.config_view import ConfigView
from views.processing_view import ProcessingView
from views.store_view import StoreView

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

    # --- Manejo de Archivos (Drag & Drop) ---
    def on_file_drop(e):
        file_path = e.files[0].path if e.files else None
        if not file_path:
            return
        
        # Simplemente delegamos a la vista activa si soporta archivos
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

    # --- Componentes UI (crearlos antes de las funciones que los usan) ---
    def toggle_theme(e):
        # Función legacy, ahora usamos set_theme
        new_mode = "light" if page.theme_mode == "dark" else "dark"
        set_theme("light" if new_mode == "light" else "dark")

    def set_theme(theme_name):
        if theme_name == "dark":
            page.theme_mode = "dark"
            page.theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE)
        elif theme_name == "light":
            page.theme_mode = "light"
            page.theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE)
        elif theme_name == "red":
            page.theme_mode = "dark"
            page.theme = ft.Theme(color_scheme_seed=ft.Colors.RED)
        
        # Actualizar icono del botón flotante si existe
        if theme_btn:
             theme_btn.icon = "dark_mode" if page.theme_mode == "light" else "light_mode"
        
        page.update()
        mostrar_alerta(f"Tema aplicado: {theme_name.capitalize()}", "green")

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
            ft.NavigationRailDestination(icon="store_outlined", selected_icon="store", label="Tienda"),
            ft.NavigationRailDestination(icon="info_outlined", selected_icon="info", label="Info"),
        ],
        on_change=None  # Lo asignaremos después
    )

    theme_btn = ft.IconButton(icon="light_mode", on_click=toggle_theme, tooltip="Cambiar Tema")
    main_content = ft.Container(expand=True, padding=10)

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
            state["current_view"] = StoreView(page, set_theme)
        elif idx == 4:
            state["current_view"] = CreditsView()
            
        main_content.content = state["current_view"]
        main_content.update()

    def change_to_processing(mode, file_path, options):
        state["current_view"] = ProcessingView(page, mode, file_path, options, on_finish=lambda: print("Fin"))
        main_content.content = state["current_view"]
        main_content.update()

    # Asignar el on_change después de que las funciones estén definidas
    rail.on_change = change_view

    # --- Publicidad Pasiva (Banner Inferior) ---
    ad_bar = ft.Container(
        content=ft.Row([
            ft.Text("📢 Publicidad: ¿Quieres convertirte en un experto en Python? Visita nuestro curso.", size=12, color="white"),
            ft.Text(" [Clic aquí]", size=12, color="blue", weight="bold")
        ], alignment=ft.MainAxisAlignment.CENTER),
        bgcolor=ft.Colors.BLACK54,
        padding=5,
        height=30,
        on_click=lambda _: page.launch_url("https://example.com/ad")
    )

    def show_main_app():
        # Mostrar la interfaz principal después de la bienvenida
        page.controls.clear()
        
        # Iniciar vista
        state["current_view"] = SingleVideoView(page, change_to_processing)
        main_content.content = state["current_view"]

        # Layout principal con barra de publicidad al fondo
        page.add(
            ft.Column([
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Column([rail, ft.Container(content=theme_btn, padding=10)], alignment="spaceBetween"),
                            ft.VerticalDivider(width=1, color="grey"),
                            main_content
                        ],
                        expand=True,
                    ),
                    expand=True
                ),
                ad_bar
            ], expand=True, spacing=0)
        )

    # Mostrar pantalla de bienvenida primero
    from views.welcome_view import WelcomeView
    welcome_view = WelcomeView(page, show_main_app)
    page.add(welcome_view)

if __name__ == "__main__":
    ft.app(target=main)