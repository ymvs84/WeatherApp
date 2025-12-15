import requests
from .config import Config

class WeatherService:
    @staticmethod
    def get_weather_data(city: str) -> dict:
        """
        Llama a la API y devuelve un diccionario limpio con los datos.
        Maneja errores de red aquí para no ensuciar la UI.
        """
        api_key = Config.get_api_key()

        params = {
            "q": city,
            "appid": api_key,
            "units": "metric",
            "lang": "es"
        }

        try:
            response = requests.get(Config.BASE_URL, params=params, timeout=10)
            response.raise_for_status() # Lanza error si es 404, 500...
            return response.json()

        except requests.exceptions.HTTPError:
            if response.status_code == 404:
                raise ValueError(f"La ciudad '{city}' no fue encontrada.")
            raise ConnectionError(f"Error del servidor (Código: {response.status_code})")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Error de conexión: {str(e)}")

    @staticmethod
    def get_icon_data(icon_code: str) -> bytes:
        """Descarga la imagen del icono."""
        url = f"{Config.ICON_URL}{icon_code}@2x.png"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.content
        except Exception:
            return b"" # Retorna vacío si falla la imagen
