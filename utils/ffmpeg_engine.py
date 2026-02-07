import subprocess
import os
import sys

def get_ffmpeg_path():
    """Busca el ejecutable de ffmpeg."""
    if getattr(sys, 'frozen', False):
        # Si estamos en el ejecutable compilado (PyInstaller)
        # El archivo ffmpeg.exe se extrae en la carpeta temporal sys._MEIPASS
        path = os.path.join(sys._MEIPASS, 'ffmpeg.exe')
        if os.path.exists(path):
            return path
            
    # Si estamos en desarrollo o no se encontró en _MEIPASS
    # Buscar en el directorio actual
    local_path = os.path.join(os.getcwd(), 'ffmpeg.exe')
    if os.path.exists(local_path):
        return local_path
        
    # Por defecto, confiar en el PATH del sistema
    return 'ffmpeg'

def run_conversion(input_path, output_path, encoder="libx264", quality_preset="Auto"):
    """
    Ejecuta la conversión usando FFmpeg.
    Detecta automáticamente si es audio, video o imagen según la extensión de salida.
    quality_preset: "Auto", "High (1080p)", "Medium (720p)", "Low (480p)"
    """
    
    ffmpeg_exe = get_ffmpeg_path()
    
    # Determinar tipo de archivo por extensión
    ext = os.path.splitext(output_path)[1].lower()
    
    audio_exts = ['.mp3', '.wav', '.aac', '.flac', '.m4a', '.ogg', '.wma']
    image_exts = ['.jpg', '.jpeg', '.png', '.bmp', '.webp', '.gif', '.tiff']
    
    is_audio = ext in audio_exts
    is_image = ext in image_exts
    
    comando = [
        ffmpeg_exe,
        '-y',               # Sobrescribir
        '-i', input_path,   # Archivo entrada
    ]

    if is_image:
        # Configuración para imágenes
        # FFmpeg maneja esto bastante bien por defecto
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
        
        # Ajuste de preset según encoder
        if "libx264" in encoder or "libx265" in encoder:
            comando.extend(['-preset', 'fast'])
        elif "amf" in encoder:
            # AMD AMF usa quality (speed, balanced, quality)
            comando.extend(['-quality', 'balanced'])
        elif "nvenc" in encoder:
            # NVIDIA NVENC soporta preset p1-p7, pero 'p4' es un buen balance (medium)
            # También acepta palabras clave en versiones recientes, probemos p4 que es seguro
            comando.extend(['-preset', 'p4'])
        elif "qsv" in encoder:
            # Intel QSV soporta preset (veryfast...veryslow)
            comando.extend(['-preset', 'fast'])
        
        # Calidad / Resolución
        if quality_preset == "High (1080p)":
             comando.extend(['-vf', 'scale=-2:1080'])
        elif quality_preset == "Medium (720p)":
             comando.extend(['-vf', 'scale=-2:720'])
        elif quality_preset == "Low (480p)":
             comando.extend(['-vf', 'scale=-2:480'])
        
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
