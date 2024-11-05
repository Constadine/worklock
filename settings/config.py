# settings/config.py
import os
from settings.flavors import Flavor

class Settings:
    def __init__(self):
        # Default Settings
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.sounds_dir = os.path.join(self.base_dir, "sounds")
        self.session_log_file = os.path.join(self.base_dir, "session_logs.txt")
        self.daily_totals_file = os.path.join(self.base_dir, "daily_totals.txt")
        self.default_work_duration = 25
        self.default_break_duration = 5
        self.current_flavor = "standard"
        self.flavors = {
            name: flavor_class()
            for name, flavor_class in Flavor.flavors.items()
        }
    def load_from_file(self, file_path="user_settings.json"):
        import json
        import os

        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                user_settings = json.load(file)
                self.current_flavor = user_settings.get("current_flavor", self.current_flavor)

    def get_current_flavor(self) -> Flavor:
        """Retrieve current timer flavor settings."""
        return self.flavors[self.current_flavor]

    def get_available_sounds(self):
        return [f for f in os.listdir(self.sounds_dir) if os.path.isfile(os.path.join(self.sounds_dir, f))]