import flet as ft
import os
from utils.config_loader import APP_DATA

class SingleVideoView(ft.Container):
    def __init__(self, page, on_process_callback):
        super().__init__()
        self.page = page
        self.on_process_callback = on_process_callback # Función para ir a la pantalla de carga
        self.file_path = None
        
        # Elementos UI referenciados
        self.drop_zone_icon = ft.Icon(name="cloud_upload", size=60, color="grey")
        self.drop_text = ft.Text("Arrastra tu video/imagen aquí o haz click", size=18, color="grey")
        self.btn_convert = ft.ElevatedButton(
            "Configurar y Convertir", 
            icon="settings", 
            disabled=True, 
            on_click=self._open_options_dialog,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=20,
                bgcolor=ft.Colors.CYAN_700,
                color="white"
            )
        )
        
        self.picker = ft.FilePicker(on_result=self._on_picker_result)
        self.save_picker = ft.FilePicker(on_result=self._on_save_result)
        self.page.overlay.append(self.picker)
        self.page.overlay.append(self.save_picker)
        self.page.update()  # Actualizar el overlay
        self.content = self._build_ui()

        # Variables temporales para la configuración elegida en el diálogo
        self.selected_format = None
        self.selected_bitrate = None

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
                border=ft.border.all(2, ft.Colors.GREY_400),
                border_radius=20,
                on_click=lambda _: self.picker.pick_files(),
                animate=ft.Animation(300, "bounceOut"),
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_left,
                    end=ft.alignment.bottom_right,
                    colors=[ft.Colors.with_opacity(0.1, "blue"), ft.Colors.with_opacity(0.1, "purple")]
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

    def _open_options_dialog(self, e):
        # Detectar tipo de archivo
        ext = os.path.splitext(self.file_path)[1].lower()
        image_exts = ['.jpg', '.jpeg', '.png', '.bmp', '.webp', '.gif', '.tiff']
        is_image = ext in image_exts
        
        # Dropdowns
        if is_image:
            formats = ["png", "jpg", "webp", "bmp", "tiff"]
            default_fmt = "png"
            bitrates = [] # No aplica para imágenes en este convertidor simple
        else:
            formats = ["mp4", "avi", "mkv", "mov", "mp3", "wav", "aac", "flac"]
            default_fmt = "mp4"
            bitrates = ["Auto", "High (1080p)", "Medium (720p)", "Low (480p)"]

        self.dd_format = ft.Dropdown(
            label="Formato de Salida", 
            options=[ft.dropdown.Option(f) for f in formats], 
            value=default_fmt
        )
        
        content_controls = [self.dd_format]
        
        if not is_image:
            self.dd_bitrate = ft.Dropdown(
                label="Bitrate / Calidad", 
                options=[ft.dropdown.Option(b) for b in bitrates], 
                value="Auto"
            )
            content_controls.append(self.dd_bitrate)

        def close_dlg(e):
            self.dialog.open = False
            self.page.update()

        def proceed(e):
            self.selected_format = self.dd_format.value
            if not is_image:
                self.selected_bitrate = self.dd_bitrate.value
            
            self.dialog.open = False
            self.page.update()
            self._start_save_process()

        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Opciones de Conversión"),
            content=ft.Column(content_controls, height=150, tight=True),
            actions=[
                ft.TextButton("Cancelar", on_click=close_dlg),
                ft.TextButton("Continuar", on_click=proceed),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()

    def _start_save_process(self):
        # Pedir ubicación de guardado con la extensión seleccionada
        ext = self.selected_format
        if not ext.startswith('.'):
            ext = f".{ext}"
            
        self.save_picker.save_file(
            dialog_title="Guardar archivo convertido como...",
            file_name=f"output{ext}",
            allowed_extensions=[ext.replace('.', '')]
        )

    def _on_save_result(self, e):
        if e.path:
            # Obtenemos config actual (que ya tiene el hardware seleccionado en ConfigView)
            options = APP_DATA['settings'].copy()
            options['output_path'] = e.path
            
            # Sobrescribir con lo elegido en el diálogo
            # Nota: El engine usa 'encoder' desde options, pero el formato lo deduce de la extensión del output_path
            # El bitrate podríamos pasarlo si el engine lo soportara explícitamente, 
            # pero por ahora el engine es simple y usa presets.
            # Podríamos modificar options['default_bitrate'] si quisieramos usarlo luego.
            if self.selected_bitrate:
                options['default_bitrate'] = self.selected_bitrate
            
            self.on_process_callback("single", self.file_path, options)
