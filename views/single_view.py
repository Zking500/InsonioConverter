import flet as ft
from utils.config_loader import APP_DATA

class SingleVideoView(ft.Container):
    def __init__(self, page, on_process_callback):
        super().__init__()
        self.page = page
        self.on_process_callback = on_process_callback # Función para ir a la pantalla de carga
        self.file_path = None
        
        # Elementos UI referenciados
        self.drop_zone_icon = ft.Icon(name="cloud_upload", size=60, color="grey")
        self.drop_text = ft.Text("Arrastra tu video aquí o haz click", size=18, color="grey")
        self.btn_convert = ft.ElevatedButton(
            "Comenzar Conversión", 
            icon="play_arrow", 
            disabled=True, 
            on_click=self._start_conversion,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=20,
                bgcolor=ft.colors.CYAN_700,
                color="white"
            )
        )
        
        self.picker = ft.FilePicker(on_result=self._on_picker_result)
        self.page.overlay.append(self.picker)
        self.content = self._build_ui()

    def _build_ui(self):
        # Tarjeta degradada
        return ft.Column([
            ft.Container(
                content=ft.Column([
                    self.drop_zone_icon,
                    self.drop_text
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                alignment=ft.alignment.center,
                height=300,
                border=ft.border.all(2, ft.colors.GREY_400),
                border_radius=20,
                on_click=lambda _: self.picker.pick_files(),
                animate=ft.animation.Animation(300, "bounceOut"),
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_left,
                    end=ft.alignment.bottom_right,
                    colors=[ft.colors.with_opacity(0.1, "blue"), ft.colors.with_opacity(0.1, "purple")]
                )
            ),
            ft.Container(height=20),
            ft.Row([self.btn_convert], alignment=ft.MainAxisAlignment.CENTER)
        ], alignment=ft.MainAxisAlignment.CENTER)

    # Método público llamado desde main.py cuando arrastras un archivo
    def set_file(self, path):
        self.file_path = path
        self.drop_zone_icon.name = "check_circle"
        self.drop_zone_icon.color = "green"
        self.drop_text.value = f"Listo: {path.split('/')[-1]}"
        self.drop_text.color = "white"
        self.btn_convert.disabled = False
        self.update()

    def _on_picker_result(self, e):
        if e.files:
            self.set_file(e.files[0].path)

    def _start_conversion(self, e):
        # Obtenemos config actual para mandarla al proceso
        options = APP_DATA['settings']
        self.on_process_callback("single", self.file_path, options)