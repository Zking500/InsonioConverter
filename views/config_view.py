import flet as ft
from utils.config_loader import APP_DATA

class ConfigView(ft.Container):
    def __init__(self, page):
        super().__init__()
        self.expand = True
        self.page = page
        self.settings = APP_DATA['settings']
        self.content = self._build_ui()

    def _build_ui(self):
        # Componentes UI
        enc_dropdown = self._crear_dropdown("Encoder por defecto", self.settings['encoders_list'], self.settings['default_encoder'])
        fmt_dropdown = self._crear_dropdown("Formato de Salida", self.settings['formats_list'], self.settings['default_format'])
        bit_dropdown = self._crear_dropdown("Bitrate Objetivo", self.settings['bitrates_list'], self.settings['default_bitrate'])
        
        # Ruta de guardado (Simulada visualmente)
        path_field = ft.TextField(
            label="Carpeta de Salida", 
            value=self.settings['save_location'], 
            read_only=True, 
            suffix_icon="folder",
            expand=True
        )

        return ft.Column([
            ft.Text("⚙️ Configuración del Motor", size=30, weight="bold", 
                   color=ft.colors.CYAN if self.page.theme_mode == ft.ThemeMode.DARK else ft.colors.BLUE),
            ft.Divider(),
            
            ft.Text("Opciones de Video", size=20, weight="bold"),
            ft.Container(
                content=ft.Column([enc_dropdown, fmt_dropdown, bit_dropdown], spacing=20),
                padding=20,
                bgcolor=ft.colors.with_opacity(0.05, "white"),
                border_radius=10,
                animate=ft.animation.Animation(300, "easeOut")
            ),

            ft.Text("Almacenamiento", size=20, weight="bold"),
            ft.Row([path_field, ft.ElevatedButton("Cambiar", on_click=lambda _: print("Abrir picker"))]),

            ft.Container(height=20),
            ft.ElevatedButton(
                "Guardar Cambios", 
                icon="save", 
                style=ft.ButtonStyle(bgcolor=ft.colors.GREEN_600, color="white"),
                on_click=self._guardar_config
            )
        ], spacing=15, scroll=ft.ScrollMode.HIDDEN)

    def _crear_dropdown(self, label, opciones, valor_actual):
        return ft.Dropdown(
            label=label,
            options=[ft.dropdown.Option(o) for o in opciones],
            value=valor_actual,
            border_color=ft.colors.OUTLINE,
            focused_border_color=ft.colors.CYAN
        )

    def _guardar_config(self, e):
        # Aquí llamarías a save_config() para escribir en el JSON
        self.page.snack_bar = ft.SnackBar(ft.Text("✅ Configuración guardada en JSON"))
        self.page.snack_bar.open = True
        self.page.update()