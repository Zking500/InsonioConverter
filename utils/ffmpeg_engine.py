import subprocess
import os

def run_conversion(input_path, output_ext, encoder):
    base_name = os.path.splitext(input_path)[0]
    output_file = f"{base_name}_converted{output_ext}"
    
    # Comando construído dinámicamente
    comando = [
        'ffmpeg',
        '-y',               # Sobrescribir
        '-i', input_path,   # Archivo entrada
        '-c:v', encoder,    # Codec seleccionado
        '-preset', 'fast',  # Preset de velocidad (puedes cambiarlo a medium)
        output_file         # Archivo salida
    ]
    
    try:
        # Configuración para ocultar la ventana negra de CMD en Windows
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        
        # Ejecutamos
        subprocess.run(comando, startupinfo=startupinfo, check=True)
        return True, f"✅ Listo: {os.path.basename(output_file)}"
    except subprocess.CalledProcessError:
        return False, "❌ Error: Falló FFmpeg (¿Archivo corrupto?)"
    except FileNotFoundError:
        return False, "❌ Error: No encuentro ffmpeg.exe en el sistema"