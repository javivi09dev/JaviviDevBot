import json
import os

def load_config():
    if not os.path.exists('config.json'):
        config = {
            "ticket_categories": {},
            "ticket_channel": None,
            "welcome_channel": None,
            "announcements_channel": None,
            "terms_channel": None
        }
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
        return config
    else:
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f)

def save_config(config):
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4) 