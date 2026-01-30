import json
import os

CONFIG_FILE = 'config.json'

def load_config():
    try:
        # Forzamos utf-8 para leer tildes y ñ sin errores
        with open(CONFIG_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error cargando config: {e}")
        # Configuración de respaldo por si explota el archivo
        return {
            "app_info": {"name": "Insonio (Safe Mode)", "version": "Error", "company": "S&O", "developer": "Z King"},
            "urls": {"donation": "", "website": ""},
            "settings": {
                "window_width": 800, "window_height": 600, "encoders_list": ["libx264"],
                "default_encoder": "libx264", "default_format": ".mp4", "default_bitrate": "Auto", "save_location": "same_as_source"
            }
        }

APP_DATA = load_config()

def save_config():
    """Guarda el diccionario APP_DATA actual en el archivo config.json"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as file:
            json.dump(APP_DATA, file, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error guardando config: {e}")