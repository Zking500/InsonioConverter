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
        # Componentes UI con manejadores de cambio - guardar como atributos
        self.enc_dropdown = self._crear_dropdown(
            "Encoder por defecto", 
            self.settings['encoders_list'], 
            self.settings['default_encoder'],
            on_change=self._on_encoder_change
        )
        self.fmt_dropdown = self._crear_dropdown(
            "Formato de Salida", 
            self.settings['formats_list'], 
            self.settings['default_format'],
            on_change=self._on_format_change
        )
        self.bit_dropdown = self._crear_dropdown("Bitrate Objetivo", self.settings['bitrates_list'], self.settings['default_bitrate'])
        
        # Hardware acceleration dropdown
        self.hw_dropdown = self._crear_dropdown(
            "Aceleración por Hardware", 
            self.settings.get('hardware_list', ["cpu", "cuda", "opencl", "qsv"]), 
            self.settings.get('hardware_acceleration', 'cpu'),
            on_change=self._on_hardware_change
        )
        
        # Ruta de guardado (Simulada visualmente)
        path_field = ft.TextField(
            label="Carpeta de Salida", 
            value=self.settings['save_location'], 
            read_only=True, 
            suffix_icon="folder",
            expand=True
        )

        # Descripciones dinámicas
        self.enc_description = ft.Text(
            self.settings['encoder_descriptions'].get(self.settings['default_encoder'], ""),
            size=12, color="grey", italic=True
        )
        self.fmt_description = ft.Text(
            self.settings['format_descriptions'].get(self.settings['default_format'], ""),
            size=12, color="grey", italic=True
        )
        self.hw_description = ft.Text(
            self.settings['hardware_descriptions'].get(self.settings.get('hardware_acceleration', 'cpu'), ""),
            size=12, color="grey", italic=True
        )

        return ft.Column([
            ft.Text("⚙️ Configuración del Motor", size=30, weight="bold", 
                   color=ft.Colors.CYAN if self.page.theme_mode == ft.ThemeMode.DARK else ft.Colors.BLUE),
            ft.Divider(),
            
            ft.Text("Opciones de Video", size=20, weight="bold"),
            ft.Container(
                content=ft.Column([
                    self.enc_dropdown, self.enc_description,
                    self.fmt_dropdown, self.fmt_description,
                    self.bit_dropdown,
                    self.hw_dropdown, self.hw_description
                ], spacing=10),
                padding=20,
                bgcolor=ft.Colors.with_opacity(0.05, "white"),
                border_radius=10,
                animate=ft.Animation(300, "easeOut")
            ),

            ft.Text("Almacenamiento", size=20, weight="bold"),
            ft.Row([path_field, ft.ElevatedButton("Cambiar", on_click=lambda _: print("Abrir picker"))]),

            ft.Container(height=20),
            ft.ElevatedButton(
                "Guardar Cambios", 
                icon="save", 
                style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_600, color="white"),
                on_click=self._guardar_config
            )
        ], spacing=15, scroll=ft.ScrollMode.HIDDEN)

    def _crear_dropdown(self, label, opciones, valor_actual, on_change=None):
        return ft.Dropdown(
            label=label,
            options=[ft.dropdown.Option(o) for o in opciones],
            value=valor_actual,
            border_color=ft.Colors.OUTLINE,
            focused_border_color=ft.Colors.CYAN,
            on_change=on_change
        )

    def _on_encoder_change(self, e):
        # Actualizar descripción del encoder
        encoder = e.control.value
        if hasattr(self, 'enc_description'):
            self.enc_description.value = self.settings['encoder_descriptions'].get(encoder, "")
            self.enc_description.update()

    def _on_format_change(self, e):
        # Actualizar descripción del formato
        format_ext = e.control.value
        if hasattr(self, 'fmt_description'):
            self.fmt_description.value = self.settings['format_descriptions'].get(format_ext, "")
            self.fmt_description.update()

    def _on_hardware_change(self, e):
        # Actualizar descripción del hardware
        hardware = e.control.value
        if hasattr(self, 'hw_description'):
            self.hw_description.value = self.settings['hardware_descriptions'].get(hardware, "")
            self.hw_description.update()

    def _guardar_config(self, e):
        # Guardar configuración en el JSON
        from utils.config_loader import save_config
        
        # Actualizar valores en APP_DATA usando las referencias guardadas
        APP_DATA['settings']['default_encoder'] = self.enc_dropdown.value
        APP_DATA['settings']['default_format'] = self.fmt_dropdown.value
        APP_DATA['settings']['default_bitrate'] = self.bit_dropdown.value
        APP_DATA['settings']['hardware_acceleration'] = self.hw_dropdown.value
        
        # Guardar en archivo
        save_config()
        
        self.page.snack_bar = ft.SnackBar(ft.Text("✅ Configuración guardada en JSON"))
        self.page.snack_bar.open = True
        self.page.update()