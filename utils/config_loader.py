import json
import os

def load_config():
    try:
        # Forzamos utf-8 para leer tildes y ñ sin errores
        with open('config.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error cargando config: {e}")
        # Configuración de respaldo por si explota el archivo
        return {
            "app_info": {"name": "Insonio (Safe Mode)", "version": "Error", "company": "S&O", "developer": "Z King"},
            "urls": {"donation": "", "website": ""},
            "settings": {"window_width": 800, "window_height": 600, "encoders_list": ["libx264"]}
        }

APP_DATA = load_config()