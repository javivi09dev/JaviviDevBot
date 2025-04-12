import json
import os
import sys

def load_config():
    try:
        with open("config/config.json", "r", encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # Crear directorio config si no existe
        os.makedirs("config", exist_ok=True)
        default_config = {
            "welcome_channel": None,
            "ticket_channel": None,
            "announcements_channel": None,
            "terms_channel": None,
            "feedback_channel": None,
            "roles": {},
            "ticket_categories": {}
        }
        save_config(default_config)
        return default_config
    except Exception as e:
        print(f"Error al cargar la configuración: {str(e)}", file=sys.stderr)
        return None

def save_config(config):
    try:
        # Asegurarse de que el directorio config existe
        os.makedirs("config", exist_ok=True)
        with open("config/config.json", "w", encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error al guardar la configuración: {str(e)}", file=sys.stderr) 