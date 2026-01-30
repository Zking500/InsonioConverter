import flet as ft
from utils.ffmpeg_engine import run_conversion

def SingleVideoView(page: ft.Page):
    # Variables de estado
    selected_file = ft.Text("Ningún archivo seleccionado")
    
    def on_file_picked(e: ft.FilePickerResultEvent):
        if e.files:
            selected_file.value = e.files[0].path
            selected_file.update()

    file_picker = ft.FilePicker(on_result=on_file_picked)
    page.overlay.append(file_picker) # Importante para que funcione el popup

    encoder_dd = ft.Dropdown(
        label="Encoder",
        options=[ft.dropdown.Option("libx264"), ft.dropdown.Option("libx265")],
        value="libx264"
    )

    def convert_click(e):
        if "Ningún" in selected_file.value:
            return
        
        res, msg = run_conversion(selected_file.value, ".mp4", encoder_dd.value)
        page.snack_bar = ft.SnackBar(ft.Text(msg))
        page.snack_bar.open = True
        page.update()

    return ft.Column([
        ft.Text("Convertir un solo video", size=20, weight="bold"),
        ft.ElevatedButton("Seleccionar Video", icon=ft.icons.VIDEO_FILE, on_click=lambda _: file_picker.pick_files()),
        selected_file,
        encoder_dd,
        ft.ElevatedButton("¡Convertir!", on_click=convert_click, bgcolor=ft.colors.BLUE_600, color="white")
    ], spacing=20)