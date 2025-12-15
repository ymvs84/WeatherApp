import os
from dotenv import load_dotenv

# Carga el archivo .env si existe
load_dotenv()

class Config:
    # Intenta leer la variable, si no existe devuelve None
    API_KEY = os.getenv("WEATHER_API_KEY")
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
    ICON_URL = "http://openweathermap.org/img/wn/"

    @staticmethod
    def get_api_key():
        if not Config.API_KEY:
            # Esto evita que la app arranque silenciosamente sin clave
            raise ValueError("❌ ERROR: No se encontró WEATHER_API_KEY en el archivo .env o variables de entorno.")
        return Config.API_KEY
