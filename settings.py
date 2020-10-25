from dataclasses import dataclass
import json


settings_file = 'settings.json'


@dataclass
class Settings:
    filename: str = ''
    first_run: bool = True
    yandex_disk: bool = False
    google_disk: bool = False
    dropbox: bool = False

    def save_to_file(self):
        json.dump(self.__dict__, settings_file)

    @classmethod
    def load_from_file(cls):
        data = json.load(open(settings_file))
        cls(**data)
