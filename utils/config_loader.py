import json
import os

def load_config():
    """
    Carga la configuración desde el archivo JSON.
    Retorna un diccionario de Python.
    """
    try:
        # Buscamos el archivo en la ruta actual
        with open('config.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        # Fallback de emergencia si borras el archivo por error
        return {
            "app_info": {"name": "Error Config", "version": "0.0"},
            "urls": {"donation": ""},
            "settings": {"encoders_list": ["libx264"]}
        }

# Variable global para usarla en todo el proyecto
APP_DATA = load_config()