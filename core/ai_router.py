import os
import json
from dotenv import load_dotenv
from core.logger import MFOLogger

class AIRouter:
    def __init__(self):
        self.logger = MFOLogger()
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY", "twój_tajny_klucz_tutaj")
        self.config = self.load_config()

    def load_config(self):
        config_path = "config/settings.json"
        try:
            if os.path.exists(config_path):
                with open(config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.logger.info("Konfiguracja z settings.json została pomyślnie wczytana.")
                    return data
            else:
                self.logger.error(f"Brak pliku konfiguracyjnego pod ścieżką: {config_path}")
                return {"project_name": "MFO TURBO AI CENTER (Awaryjny)"}
        except Exception as e:
            self.logger.error(f"Błąd podczas wczytywania konfiguracji: {e}")
            return {"project_name": "MFO TURBO AI CENTER (Błąd)"}

    def status_check(self):
        self.logger.info(f"Sprawdzanie statusu routera. Projekt: {self.config.get('project_name')}")
        if self.api_key and self.api_key != "twój_tajny_klucz_tutaj":
            self.logger.info("Klucz API jest poprawnie skonfigurowany.")
        else:
            self.logger.error("Uwaga: W pliku .env nadal jest domyślny lub pusty klucz API!")

if __name__ == "__main__":
    router = AIRouter()
    router.status_check()
