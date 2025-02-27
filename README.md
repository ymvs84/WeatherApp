# WeatherApp
Una aplicación de escritorio para consultar el clima actual de una ciudad usando la API de OpenWeatherMap, con íconos del clima y una lista de ciudades favoritas.  
**Autor: Yago Menéndez de la Vega**

## Requisitos
- Python 3.8+
- PySide6 (`pip install PySide6`)
- requests (`pip install requests`)
- pytest (`pip install pytest pytest-qt`)

## Instalación
1. Clona el repositorio o descarga los archivos https://github.com/ymvs84/WeatherApp
2. Instala las dependencias: `pip install -r requirements.txt`
3. Obtén una clave API gratuita en [OpenWeatherMap](https://openweathermap.org/) y reemplaza `TU_CLAVE_API_AQUÍ` en `WeatherApp.py`.
4. Ejecuta la aplicación desde el directorio `ProyectoDI/` con: `python WeatherApp.py`

## Uso
- Ingresa el nombre de una ciudad (ej. "Madrid") en el campo de texto y presiona "Buscar Clima" o Enter.
- Verás la temperatura, descripción del clima, humedad y un ícono representativo.
- Haz clic en "Añadir a Favoritas" para guardar la ciudad actual.
- Selecciona una ciudad de la lista de favoritas para cargar su clima.
- Si hay un error (ciudad no encontrada o sin conexión), aparecerá una ventana emergente.

## Pruebas
Desde el directorio donde has descargado los archivos, ejecuta las pruebas unitarias con:  
`pytest test_weather.py -v`

## Conversión a .exe
1. Instala PyInstaller: `pip install pyinstaller`
2. Desde el directorio `ProyectoDI/`, ejecuta: `pyinstaller --onefile --windowed WeatherApp.py`
3. El archivo .exe estará en la carpeta `dist/`.