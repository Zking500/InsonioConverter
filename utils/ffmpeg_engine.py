# utils/ffmpeg_engine.py
import subprocess
import os

def run_conversion(input_path, output_ext, encoder):
    """
    Función agnóstica: recibe datos y ejecuta FFmpeg.
    """
    # Obtenemos el nombre base sin extensión
    base_name = os.path.splitext(input_path)[0]
    output_file = f"{base_name}_converted{output_ext}"
    
    # Comando básico
    # En producción usaríamos shlex para escapar espacios, pero esto funciona en Windows simple
    comando = [
        'ffmpeg',
        '-y',               # Sobrescribir si existe
        '-i', input_path,   # Input
        '-c:v', encoder,    # Codec de video
        output_file         # Output
    ]
    
    try:
        # startupinfo oculta la ventana negra de consola en Windows
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        
        subprocess.run(comando, startupinfo=startupinfo, check=True)
        return True, f"✅ Éxito: {output_file}"
    except subprocess.CalledProcessError as e:
        return False, f"❌ Error: {str(e)}"
    except FileNotFoundError:
        return False, "❌ Error: FFmpeg no está instalado o no está en el PATH."