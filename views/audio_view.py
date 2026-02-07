import flet as ft
import os
from utils.config_loader import APP_DATA

class AudioView(ft.Container):
    def __init__(self, page, on_process_callback):
        super().__init__()
        self.page = page
        self.on_process_callback = on_process_callback # Función para ir a la pantalla de carga
        self.file_path = None
        
        # Elementos UI referenciados
        self.drop_zone_icon = ft.Icon(name="audiotrack", size=60, color="grey")
        self.drop_text = ft.Text("Arrastra tu audio aquí o haz click", size=18, color="grey")
        self.btn_convert = ft.ElevatedButton(
            "Configurar y Convertir Audio", 
            icon="settings", 
            disabled=True, 
            on_click=self._open_options_dialog,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=20,
                bgcolor=ft.Colors.PINK_700,
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
                on_click=lambda _: self.picker.pick_files(allowed_extensions=["mp3", "wav", "flac", "aac", "ogg", "m4a"]),
                animate=ft.Animation(300, "bounceOut"),
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_left,
                    end=ft.alignment.bottom_right,
                    colors=[ft.Colors.with_opacity(0.1, "pink"), ft.Colors.with_opacity(0.1, "orange")]
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
        try:
            if not self.file_path:
                return

            formats = ["mp3", "wav", "aac", "flac", "ogg", "m4a"]
            default_fmt = "mp3"
            
            # Opciones de bitrate de audio
            bitrates = ["128k", "192k", "256k", "320k", "Lossless"]

            self.dd_format = ft.Dropdown(
                label="Formato de Salida", 
                options=[ft.dropdown.Option(f) for f in formats], 
                value=default_fmt
            )
            
            self.dd_bitrate = ft.Dropdown(
                label="Calidad / Bitrate", 
                options=[ft.dropdown.Option(b) for b in bitrates], 
                value="192k"
            )

            content_controls = [self.dd_format, self.dd_bitrate]

            def close_dlg(e):
                if hasattr(self.page, "close"):
                    self.page.close(self.dialog)
                else:
                    self.dialog.open = False
                    self.page.update()

            def proceed(e):
                self.selected_format = self.dd_format.value
                self.selected_bitrate = self.dd_bitrate.value
                
                if hasattr(self.page, "close"):
                    self.page.close(self.dialog)
                else:
                    self.dialog.open = False
                    self.page.update()
                
                self._start_save_process()

            self.dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Opciones de Audio"),
                content=ft.Column(content_controls, height=150, tight=True),
                actions=[
                    ft.TextButton("Cancelar", on_click=close_dlg),
                    ft.TextButton("Continuar", on_click=proceed),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            
            if hasattr(self.page, "open"):
                self.page.open(self.dialog)
            else:
                self.page.dialog = self.dialog
                self.dialog.open = True
                self.page.update()
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error al abrir opciones: {ex}"))
            self.page.snack_bar.open = True
            self.page.update()

    def _start_save_process(self):
        # Pedir ubicación de guardado con la extensión seleccionada
        ext = self.selected_format
        if not ext.startswith('.'):
            ext = f".{ext}"
            
        self.save_picker.save_file(
            dialog_title="Guardar audio convertido como...",
            file_name=f"audio_output{ext}",
            allowed_extensions=[ext.replace('.', '')]
        )

    def _on_save_result(self, e):
        if e.path:
            # Obtenemos config actual
            options = APP_DATA['settings'].copy()
            options['output_path'] = e.path
            
            # Configurar bitrate de audio en options (el engine necesitará soporte para esto)
            if self.selected_bitrate:
                options['audio_bitrate'] = self.selected_bitrate
            
            self.on_process_callback("single", self.file_path, options)
