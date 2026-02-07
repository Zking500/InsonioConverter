import flet as ft
import asyncio
import os
import winsound  # For Windows sound playback
from utils.config_loader import APP_DATA
from utils.welcome_window import WelcomeWindow
from views.single_view import SingleVideoView
from views.audio_view import AudioView
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
        elif isinstance(state["current_view"], AudioView):
            state["current_view"].set_file(file_path)
            mostrar_alerta(f"Audio cargado: {e.files[0].name}", "green")
        elif isinstance(state["current_view"], BatchVideoView):
            state["current_view"].add_file(file_path)
            mostrar_alerta(f"Añadido a la cola: {e.files[0].name}", "green")
        else:
            mostrar_alerta("Ve a 'Convertir' o 'Lote' para usar archivos.", "amber")

    page.on_file_drop = on_file_drop 

    # --- Sistema de Notificaciones con Sonido ---
    def play_notification_sound(sound_type="notification"):
        """Play notification sound based on type"""
        try:
            sound_files = {
                "notification": "assets/notificacion.mp3",
                "complete": "assets/completado.mp3",
                "error": "assets/error.mp3",
                "update": "assets/actualizacion.mp3"
            }
            
            sound_file = sound_files.get(sound_type, "assets/notificacion.mp3")
            
            # Check if file exists
            if os.path.exists(sound_file):
                # Use Windows sound API for MP3 playback
                winsound.PlaySound(sound_file, winsound.SND_FILENAME | winsound.SND_ASYNC)
            else:
                print(f"Sound file not found: {sound_file}")
        except Exception as e:
            print(f"Error playing notification sound: {e}")
    
    def mostrar_alerta(texto, color, sound_type="notification"):
        """Show alert with optional sound notification"""
        # Play sound based on color/type
        if color == "green":
            play_notification_sound("complete")
        elif color == "red":
            play_notification_sound("error")
        elif color == "amber":
            play_notification_sound("update")
        else:
            play_notification_sound(sound_type)
        
        page.snack_bar = ft.SnackBar(
            content=ft.Text(texto, color="white"),
            bgcolor=color,
            duration=2000
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
            ft.NavigationRailDestination(icon="audiotrack_outlined", selected_icon="audiotrack", label="Audio"),
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
            state["current_view"] = AudioView(page, change_to_processing)
        elif idx == 2:
            state["current_view"] = BatchVideoView(page)
        elif idx == 3:
            state["current_view"] = ConfigView(page)
        elif idx == 4:
            state["current_view"] = StoreView(page, set_theme)
        elif idx == 5:
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
            ft.Text("💝 Apoya el desarrollo: ¿Te gusta Insonio Converter? Considera hacer una donación.", size=12, color="white"),
            ft.Text(" [Donar aquí]", size=12, color="blue", weight="bold")
        ], alignment=ft.MainAxisAlignment.CENTER),
        bgcolor=ft.Colors.BLACK54,
        padding=5,
        height=30,
        on_click=lambda _: page.launch_url("https://ko-fi.com/simel")
    )

    # --- Mensaje de Bienvenida Flotante ---
    def show_floating_welcome():
        # Play welcome notification sound
        play_notification_sound("notification")
        
        # Create the floating welcome message
        floating_welcome = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(name="celebration", color=ft.Colors.YELLOW, size=30),
                    ft.Text("¡Bienvenido a Insonio Converter!", size=20, weight="bold", color="white"),
                    ft.Icon(name="celebration", color=ft.Colors.YELLOW, size=30),
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Text("Convierte videos, imágenes y audio con facilidad", size=14, color="white"),
                ft.Row([
                    ft.ElevatedButton(
                        "Apoya con una donación ☕",
                        icon="favorite",
                        on_click=lambda _: page.launch_url("https://ko-fi.com/simel"),
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.PINK,
                            color="white",
                            shape=ft.RoundedRectangleBorder(radius=20),
                            padding=15
                        )
                    ),
                    ft.TextButton(
                        "Cerrar",
                        on_click=lambda e: close_floating_welcome(floating_welcome),
                        style=ft.ButtonStyle(color=ft.Colors.WHITE)
                    )
                ], alignment=ft.MainAxisAlignment.CENTER)
            ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=30,
            border_radius=20,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[ft.Colors.with_opacity(0.9, "purple"), ft.Colors.with_opacity(0.9, "cyan")]
            ),
            border=ft.border.all(2, ft.Colors.WHITE),
            shadow=ft.BoxShadow(
                spread_radius=5,
                blur_radius=15,
                color=ft.Colors.with_opacity(0.3, "black"),
                offset=ft.Offset(0, 5)
            ),
            animate=ft.Animation(600, "easeOut")
        )
        
        def close_floating_welcome(container):
            """Close the floating welcome message"""
            if container in page.overlay:
                page.overlay.remove(container)
                page.update()
        
        page.overlay.append(floating_welcome)
        page.update()
        
        # Auto-close after 8 seconds
        async def auto_close():
            await asyncio.sleep(8)
            if floating_welcome in page.overlay:
                page.overlay.remove(floating_welcome)
                page.update()
        
        page.run_task(auto_close)

    # --- Diálogo de Donación ---
    def show_donation_dialog():
        dlg = ft.AlertDialog(
            title=ft.Text("¡Apoya a Insonio Converter! ☕"),
            content=ft.Column([
                ft.Text("Este programa es financiado por sus donaciones."),
                ft.Text("Si te gusta y quieres desbloquear funciones Premium (futuro) o solo invitarme un café, visita mi Ko-fi.", size=14),
                ft.Image(src="https://storage.ko-fi.com/cdn/brandasset/kofi_button_red.png", width=200, height=50, fit=ft.ImageFit.CONTAIN, src_base64=None)
            ], height=150, tight=True),
            actions=[
                ft.TextButton("Ir a Ko-fi", on_click=lambda _: page.launch_url("https://ko-fi.com/simel")),
                ft.TextButton("Quizás luego", on_click=lambda _: page.close_dialog())
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

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
        
        # Mostrar mensaje de bienvenida flotante al iniciar la app principal
        show_floating_welcome()

    # Mostrar pantalla de bienvenida primero
    from views.welcome_view import WelcomeView
    welcome_view = WelcomeView(page, show_main_app)
    page.add(welcome_view)

if __name__ == "__main__":
    ft.app(target=main)