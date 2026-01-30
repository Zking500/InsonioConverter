import flet as ft
import subprocess
import os
import json

# --- 1. CONFIGURACIÓN ---
try:
    with open('config.json', 'r', encoding='utf-8') as f:
        CONFIG = json.load(f)
except:
    CONFIG = {
        "app_info": {"name": "Insonio Converter", "version": "Rescue Mode"},
        "settings": {"encoders_list": ["libx264", "libx265", "vp9"]}
    }

# --- 2. LÓGICA DE FFMPEG ---
def run_ffmpeg(input_path, encoder):
    base_name = os.path.splitext(input_path)[0]
    output_file = f"{base_name}_converted.mp4"
    
    comando = [
        'ffmpeg', '-y', '-i', input_path,
        '-c:v', encoder, '-preset', 'fast', output_file
    ]
    
    try:
        # Configuración para ocultar ventana CMD en Windows
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        subprocess.run(comando, startupinfo=startupinfo, check=True)
        return True, f"✅ Éxito: {os.path.basename(output_file)}"
    except Exception as e:
        return False, f"❌ Error: {str(e)}"

# --- 3. INTERFAZ GRÁFICA ---
def main(page: ft.Page):
    # Ajustes básicos de ventana
    page.title = "Insonio Converter - Z King"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 500
    page.window_height = 600
    page.padding = 20

    # Variables visuales
    txt_ruta = ft.Text("Ningún archivo seleccionado", italic=True, color="grey")
    
    dd_encoder = ft.Dropdown(
        label="Encoder",
        width=250,
        options=[ft.dropdown.Option(x) for x in CONFIG['settings']['encoders_list']],
        value="libx264"
    )

    # --- EVENTOS ---
    
    # CORRECCIÓN 1: Quitamos ": ft.FilePickerResultEvent"
    def al_seleccionar_archivo(e): 
        if e.files:
            txt_ruta.value = e.files[0].path
            txt_ruta.color = "white"
            txt_ruta.weight = "bold"
            page.update()

    def al_click_convertir(e):
        if "Ningún" in txt_ruta.value:
            page.snack_bar = ft.SnackBar(ft.Text("⚠️ Selecciona un video"))
            page.snack_bar.open = True
            page.update()
            return
        
        btn_convertir.text = "Procesando..."
        btn_convertir.disabled = True
        page.update()

        # Llamar a FFmpeg
        ok, msg = run_ffmpeg(txt_ruta.value, dd_encoder.value)

        btn_convertir.text = "¡Convertir Video!"
        btn_convertir.disabled = False
        
        # Feedback
        color_msg = "green" if ok else "red"
        page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=color_msg)
        page.snack_bar.open = True
        page.update()

    # --- FILE PICKER ---
    # CORRECCIÓN 2: Lo creamos vacío primero
    selector = ft.FilePicker()
    # Y le asignamos la función después
    selector.on_result = al_seleccionar_archivo
    page.overlay.append(selector)

    # --- DISEÑO ---
    page.add(
        ft.Column([
            ft.Text("Insonio Converter", size=30, weight="bold", color="cyan"),
            ft.Divider(),
            
            ft.Text("Paso 1: Archivo"),
            ft.ElevatedButton(
                "Buscar Video", 
                icon="folder_open", 
                on_click=lambda _: selector.pick_files()
            ),
            txt_ruta,
            
            ft.Divider(),
            
            ft.Text("Paso 2: Configuración"),
            dd_encoder,
            
            ft.Container(height=20), # Espacio vacío
            
            ft.ElevatedButton(
                "¡Convertir Video!", 
                icon="play_circle", 
                bgcolor="blue", 
                color="white",
                height=50,
                width=250,
                on_click=al_click_convertir
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15)
    )

# CORRECCIÓN 3: Usamos run() para versiones nuevas
if __name__ == "__main__":
    ft.app(main)