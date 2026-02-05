import subprocess
import os

def run_conversion(input_path, output_path, encoder="libx264"):
    """
    Ejecuta la conversión usando FFmpeg.
    Detecta automáticamente si es audio, video o imagen según la extensión de salida.
    """
    
    # Determinar tipo de archivo por extensión
    ext = os.path.splitext(output_path)[1].lower()
    
    audio_exts = ['.mp3', '.wav', '.aac', '.flac', '.m4a', '.ogg', '.wma']
    image_exts = ['.jpg', '.jpeg', '.png', '.bmp', '.webp', '.gif', '.tiff']
    
    is_audio = ext in audio_exts
    is_image = ext in image_exts
    
    comando = [
        'ffmpeg',
        '-y',               # Sobrescribir
        '-i', input_path,   # Archivo entrada
    ]

    if is_image:
        # Configuración para imágenes
        # FFmpeg maneja esto bastante bien por defecto
        # Si es webp o jpg, podríamos querer calidad, pero default está ok
        pass 
        
    elif is_audio:
        # Configuración para audio
        if ext == '.mp3':
            comando.extend(['-c:a', 'libmp3lame', '-q:a', '2'])
        elif ext == '.wav':
             comando.extend(['-c:a', 'pcm_s16le'])
        elif ext == '.aac':
             comando.extend(['-c:a', 'aac', '-b:a', '192k'])
        elif ext == '.flac':
             comando.extend(['-c:a', 'flac'])
        
        # Eliminar video si existe
        comando.append('-vn')
        
    else:
        # Configuración para video
        comando.extend(['-c:v', encoder])
        comando.extend(['-preset', 'fast'])
        # Asegurar audio estéreo AAC para compatibilidad
        comando.extend(['-c:a', 'aac'])

    # Archivo salida
    comando.append(output_path)
    
    try:
        # Configuración para ocultar la ventana negra de CMD en Windows
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        
        # Ejecutamos
        subprocess.run(comando, startupinfo=startupinfo, check=True)
        return True, f"✅ Listo: {os.path.basename(output_path)}"
    except subprocess.CalledProcessError:
        return False, "❌ Error: Falló FFmpeg (¿Archivo corrupto?)"
    except FileNotFoundError:
        return False, "❌ Error: No encuentro ffmpeg.exe en el sistema"
    except Exception as e:
        return False, f"❌ Error: {str(e)}"
