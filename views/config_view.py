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
        
        # Hardware acceleration dropdown
        self.hw_dropdown = self._crear_dropdown(
            "Aceleración por Hardware / Encoder", 
            self.settings.get('hardware_list', ["cpu", "cuda", "opencl", "qsv"]), 
            self.settings.get('hardware_acceleration', 'cpu'),
            on_change=self._on_hardware_change
        )
        
        # Descripciones dinámicas
        self.hw_description = ft.Text(
            self.settings['hardware_descriptions'].get(self.settings.get('hardware_acceleration', 'cpu'), ""),
            size=12, color="grey", italic=True
        )

        return ft.Column([
            ft.Text("⚙️ Configuración del Motor", size=30, weight="bold", 
                   color=ft.Colors.CYAN if self.page.theme_mode == ft.ThemeMode.DARK else ft.Colors.BLUE),
            ft.Divider(),
            
            ft.Text("Rendimiento", size=20, weight="bold"),
            ft.Text("Selecciona si quieres usar el procesador (CPU) o la tarjeta gráfica (GPU).", size=14),
            ft.Container(
                content=ft.Column([
                    self.hw_dropdown, self.hw_description
                ], spacing=10),
                padding=20,
                bgcolor=ft.Colors.with_opacity(0.05, "white"),
                border_radius=10,
                animate=ft.Animation(300, "easeOut")
            ),

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
        APP_DATA['settings']['hardware_acceleration'] = self.hw_dropdown.value
        
        # Mapeo simple de hardware a encoder por defecto (opcional)
        hw = self.hw_dropdown.value
        if hw == 'cuda':
             APP_DATA['settings']['default_encoder'] = 'h264_nvenc'
        elif hw == 'qsv':
             APP_DATA['settings']['default_encoder'] = 'h264_qsv'
        elif hw == 'amd':
             APP_DATA['settings']['default_encoder'] = 'h264_amf'
        else:
             APP_DATA['settings']['default_encoder'] = 'libx264'

        # Guardar en archivo
        save_config()
        
        self.page.snack_bar = ft.SnackBar(ft.Text("✅ Configuración guardada en JSON"))
        self.page.snack_bar.open = True
        self.page.update()
