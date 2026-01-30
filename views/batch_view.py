import flet as ft
from utils.ffmpeg_engine import run_conversion

def BatchVideoView(page: ft.Page):
    files_list = ft.Column() # Aquí mostraremos la lista visual
    stored_files = [] # Aquí guardamos las rutas reales

    def on_files_picked(e: ft.FilePickerResultEvent):
        if e.files:
            for f in e.files:
                stored_files.append(f.path)
                files_list.controls.append(ft.Text(f"📂 {f.name}"))
            files_list.update()

    file_picker = ft.FilePicker(on_result=on_files_picked)
    page.overlay.append(file_picker)

    def process_all(e):
        for file_path in stored_files:
            run_conversion(file_path, ".mp4", "libx264")
        
        page.snack_bar = ft.SnackBar(ft.Text(f"✅ Se procesaron {len(stored_files)} videos"))
        page.snack_bar.open = True
        page.update()

    return ft.Column([
        ft.Text("Procesamiento por Lote (Batch)", size=20, weight="bold"),
        ft.ElevatedButton("Añadir Videos", icon=ft.icons.LIBRARY_ADD, on_click=lambda _: file_picker.pick_files(allow_multiple=True)),
        ft.Container(content=files_list, height=150, border=ft.border.all(1, "grey"), border_radius=10, padding=10),
        ft.ElevatedButton("Procesar Todo", on_click=process_all, bgcolor=ft.colors.GREEN_600, color="white")
    ], spacing=20)