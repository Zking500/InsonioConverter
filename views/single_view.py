import flet as ft
from utils.ffmpeg_engine import run_conversion
from utils.config_loader import APP_DATA

def SingleVideoView(page: ft.Page):
    selected_path = ft.Text("Ningún archivo seleccionado", italic=True, color="grey")
    
    def on_file_picked(e):
        if e.files:
            selected_path.value = e.files[0].path
            selected_path.color = "white"
            selected_path.weight = "bold"
            selected_path.update()

    # Inicialización segura del FilePicker
    file_picker = ft.FilePicker()
    file_picker.on_result = on_file_picked
    page.overlay.append(file_picker)

    options_list = [ft.dropdown.Option(enc) for enc in APP_DATA['settings']['encoders_list']]
    encoder_dd = ft.Dropdown(
        label="Encoder de Video",
        options=options_list,
        value=options_list[0].key,
        width=300
    )

    def convert_click(e):
        if "Ningún" in selected_path.value:
            page.snack_bar = ft.SnackBar(ft.Text("⚠️ Selecciona un video primero"))
            page.snack_bar.open = True
            page.update()
            return
        
        btn_action.text = "Procesando..."
        btn_action.disabled = True
        btn_action.update()

        success, msg = run_conversion(selected_path.value, ".mp4", encoder_dd.value)
        
        btn_action.text = "¡Convertir!"
        btn_action.disabled = False
        btn_action.update()

        page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor="green" if success else "red")
        page.snack_bar.open = True
        page.update()

    btn_action = ft.ElevatedButton(
        "¡Convertir!", 
        icon="play_circle", 
        on_click=convert_click,
        bgcolor="blue", # <--- CORREGIDO: Usamos string "blue" en lugar de ft.colors...
        color="white"
    )

    return ft.Column([
        ft.Text("Modo Simple", size=25, weight="bold"),
        ft.Divider(),
        ft.Text("1. Selecciona tu video:"),
        ft.ElevatedButton("Buscar Archivo", icon="folder_open", on_click=lambda _: file_picker.pick_files()),
        selected_path,
        ft.Text("2. Configuración:"),
        encoder_dd,
        ft.Divider(),
        btn_action
    ], spacing=15)