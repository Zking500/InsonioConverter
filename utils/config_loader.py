import json
import os

# Ruta absoluta para evitar problemas al ejecutar desde otros lados
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, 'config.json')

def load_config():
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        print(f"⚠️ Error cargando config: {e}")
        return {} # Retorna vacío o valores por defecto si falla

APP_DATA = load_config()