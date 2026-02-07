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
    '--add-binary=ffmpeg.exe;.',  # Incluir FFmpeg en la raíz del exe
    '--add-data=config.json;.',   # Incluir config base por si acaso
    '--hidden-import=flet',
])

print("\n✅ Compilación completada con éxito.")
print("📁 El ejecutable está en la carpeta 'dist/'.")
print("⚠️ Recuerda: Este ejecutable YA INCLUYE FFmpeg, funcionará en cualquier PC.")
