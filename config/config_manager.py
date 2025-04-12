import json
import os

def load_config():
    try:
        with open("config/config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
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

def save_config(config):
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4) 