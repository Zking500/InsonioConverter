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
                bgcolor=ft.Colors.PURPLE_700,
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
        self.selected_name = None
        self.selected_fps = None
        self.selected_resolution = None
        self.custom_width = None
        self.custom_height = None
        self.selected_crf = None

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
                    colors=[ft.Colors.with_opacity(0.1, "purple"), ft.Colors.with_opacity(0.1, "deeppurple")]
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
            # Detectar tipo de archivo
            if not self.file_path:
                return

            ext = os.path.splitext(self.file_path)[1].lower()
            image_exts = ['.jpg', '.jpeg', '.png', '.bmp', '.webp', '.gif', '.tiff']
            is_image = ext in image_exts
            
            # Dropdowns
            if is_image:
                formats = ["png", "jpg", "webp", "bmp", "tiff"]
                default_fmt = "png"
                bitrates = []
            else:
                formats = ["mp4", "avi", "mkv", "mov"]
                default_fmt = "mp4"
                bitrates = ["Auto", "High (1080p)", "Medium (720p)", "Low (480p)"]

            base_name = os.path.splitext(os.path.basename(self.file_path))[0]
            self.tf_name = ft.TextField(label="Nombre de archivo", value=base_name, dense=True)
            self.dd_format = ft.Dropdown(
                label="Formato de Salida", 
                options=[ft.dropdown.Option(f) for f in formats], 
                value=default_fmt
            )
            
            if is_image:
                self.dd_resolution = ft.Dropdown(
                    label="Tamaño",
                    options=[ft.dropdown.Option(o) for o in ["Mantener", "480p", "720p", "1080p", "1440p", "2160p (4K)", "Personalizado"]],
                    value="Mantener"
                )
                self.tf_width = ft.TextField(label="Ancho", value="", dense=True, keyboard_type=ft.KeyboardType.NUMBER, visible=False)
                self.tf_height = ft.TextField(label="Alto", value="", dense=True, keyboard_type=ft.KeyboardType.NUMBER, visible=False)
                def on_res_change(e):
                    v = self.dd_resolution.value
                    show_custom = v == "Personalizado"
                    self.tf_width.visible = show_custom
                    self.tf_height.visible = show_custom
                    self.page.update()
                self.dd_resolution.on_change = on_res_change
            else:
                self.dd_fps = ft.Dropdown(
                    label="FPS",
                    options=[ft.dropdown.Option(o) for o in ["Mantener", "24", "30", "60", "120"]],
                    value="Mantener"
                )
                self.dd_resolution = ft.Dropdown(
                    label="Resolución",
                    options=[ft.dropdown.Option(o) for o in ["Mantener", "480p", "720p", "1080p", "1440p", "2160p (4K)", "Personalizado"]],
                    value="Mantener"
                )
                self.tf_width = ft.TextField(label="Ancho", value="", dense=True, keyboard_type=ft.KeyboardType.NUMBER, visible=False)
                self.tf_height = ft.TextField(label="Alto", value="", dense=True, keyboard_type=ft.KeyboardType.NUMBER, visible=False)
                def on_res_change(e):
                    v = self.dd_resolution.value
                    show_custom = v == "Personalizado"
                    self.tf_width.visible = show_custom
                    self.tf_height.visible = show_custom
                    self.page.update()
                self.dd_resolution.on_change = on_res_change
                self.dd_quality = ft.Dropdown(
                    label="Calidad",
                    options=[ft.dropdown.Option(b) for b in ["Auto", "High (1080p)", "Medium (720p)", "Low (480p)", "CRF Manual"]],
                    value="Auto"
                )
                self.slider_crf = ft.Slider(min=18, max=28, divisions=10, value=23, label="{value}", visible=False)
                def on_quality_change(e):
                    show_crf = self.dd_quality.value == "CRF Manual"
                    self.slider_crf.visible = show_crf
                    self.page.update()
                self.dd_quality.on_change = on_quality_change
            
            content_controls = [
                ft.Container(
                    content=ft.Column(
                        ([self.tf_name, self.dd_format] +
                         ([self.dd_resolution, self.tf_width, self.tf_height] if is_image else [self.dd_fps, self.dd_resolution, self.tf_width, self.tf_height, self.dd_quality, self.slider_crf])),
                        spacing=10
                    ),
                    padding=15,
                    border_radius=15,
                    gradient=ft.LinearGradient(
                        begin=ft.alignment.top_left,
                        end=ft.alignment.bottom_right,
                        colors=[ft.Colors.with_opacity(0.08, "purple"), ft.Colors.with_opacity(0.08, "deeppurple")]
                    ),
                    animate=ft.Animation(300, "easeOut")
                )
            ]
            
            if not is_image:
                self.dd_bitrate = None

            def close_dlg(e):
                if hasattr(self.page, "close"):
                    self.page.close(self.dialog)
                else:
                    self.dialog.open = False
                    self.page.update()

            def proceed(e):
                self.selected_format = self.dd_format.value
                self.selected_name = self.tf_name.value.strip() if self.tf_name.value else None
                if is_image:
                    self.selected_resolution = self.dd_resolution.value
                    if self.tf_width.value:
                        self.custom_width = self.tf_width.value
                    if self.tf_height.value:
                        self.custom_height = self.tf_height.value
                else:
                    self.selected_fps = self.dd_fps.value
                    self.selected_resolution = self.dd_resolution.value
                    if self.tf_width.value:
                        self.custom_width = self.tf_width.value
                    if self.tf_height.value:
                        self.custom_height = self.tf_height.value
                    self.selected_bitrate = self.dd_quality.value
                    if self.dd_quality.value == "CRF Manual":
                        self.selected_crf = int(self.slider_crf.value)
                
                if hasattr(self.page, "close"):
                    self.page.close(self.dialog)
                else:
                    self.dialog.open = False
                    self.page.update()
                
                self._start_save_process()

            self.dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Opciones de Conversión"),
                content=ft.Column(content_controls, height=250, tight=True),
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
            
        name = self.selected_name if self.selected_name else "output"
        self.save_picker.save_file(
            dialog_title="Guardar archivo convertido como...",
            file_name=f"{name}{ext}",
            allowed_extensions=[ext.replace('.', '')]
        )

    def _on_save_result(self, e):
        if e.path:
            # Obtenemos config actual (que ya tiene el hardware seleccionado en ConfigView)
            options = APP_DATA['settings'].copy()
            options['output_path'] = e.path
            
            # Sobrescribir con lo elegido en el diálogo
            if self.selected_bitrate:
                options['quality_preset'] = self.selected_bitrate
            if self.selected_fps and self.selected_fps != "Mantener":
                options['target_fps'] = int(self.selected_fps)
            if self.selected_resolution and self.selected_resolution != "Mantener":
                options['target_resolution'] = self.selected_resolution
            if self.custom_width:
                options['custom_width'] = int(self.custom_width)
            if self.custom_height:
                options['custom_height'] = int(self.custom_height)
            if self.selected_crf:
                options['crf'] = int(self.selected_crf)
            
            self.on_process_callback("single", self.file_path, options)
