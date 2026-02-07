import PyInstaller.__main__
import os
import shutil

# Limpiar compilaciones anteriores
if os.path.exists("dist"):
    shutil.rmtree("dist")
if os.path.exists("build"):
    shutil.rmtree("build")

print("🚀 Iniciando compilación de Insonio Converter...")

# Comando de PyInstaller
PyInstaller.__main__.run([
    'main.py',
    '--name=InsonioConverter',
    '--onefile',
    '--windowed',
    '--clean',
    '--icon=InsomnioConverter.ico',  # Icono de la aplicación
    '--add-binary=ffmpeg.exe;.',  # Incluir FFmpeg en la raíz del exe
    '--add-data=config.json;.',   # Incluir config base por si acaso
    '--add-data=assets/*.mp3;assets',  # Incluir sonidos MP3
    '--add-data=assets/*.wav;assets',  # Incluir sonidos WAV
    '--add-data=BarberChop.otf;.',  # Incluir fuente personalizada
    '--hidden-import=flet',
])

print("\n✅ Compilación completada con éxito.")
print("📁 El ejecutable está en la carpeta 'dist/'.")
print("⚠️ Recuerda: Este ejecutable YA INCLUYE FFmpeg, funcionará en cualquier PC.")
