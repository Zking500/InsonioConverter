import flet as ft
from utils.ffmpeg_engine import run_conversion

def BatchVideoView(page: ft.Page):
    files_view = ft.Column(scroll=ft.ScrollMode.AUTO)
    stored_paths = []

    def on_files_picked(e):
        if e.files:
            for f in e.files:
                stored_paths.append(f.path)
                files_view.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(name="movie", color="blue"),
                            ft.Text(f.name)
                        ]),
                        padding=5,
                        # CORREGIDO: Usamos Hex con Alpha (#1A es ~10% opacidad)
                        bgcolor="#1AFFFFFF", 
                        border_radius=5
                    )
                )
            files_view.update()

    file_picker = ft.FilePicker()
    file_picker.on_result = on_files_picked
    page.overlay.append(file_picker)

    def process_batch(e):
        if not stored_paths:
            return

        prog_bar = ft.ProgressBar(width=400, color="amber")
        files_view.controls.append(prog_bar)
        files_view.update()

        count = 0
        for path in stored_paths:
            run_conversion(path, ".mp4", "libx264")
            count += 1
        
        files_view.controls.remove(prog_bar)
        page.snack_bar = ft.SnackBar(ft.Text(f"✅ Se completaron {count} videos"))
        page.snack_bar.open = True
        page.update()

    return ft.Column([
        ft.Text("Modo Lote (Batch)", size=25, weight="bold"),
        ft.Text("Convierte múltiples videos a MP4 (h.264)."),
        ft.Row([
            ft.ElevatedButton("Añadir Videos", icon="add", on_click=lambda _: file_picker.pick_files(allow_multiple=True)),
            ft.ElevatedButton("Limpiar Lista", icon="delete", color="red", on_click=lambda _: None)
        ]),
        ft.Container(
            content=files_view,
            height=300,
            border=ft.border.all(1, "grey"),
            border_radius=8,
            padding=10
        ),
        ft.ElevatedButton("Procesar Todo", icon="rocket_launch", on_click=process_batch, bgcolor="green", color="white")
    ], spacing=15)