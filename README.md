# 🌦️ WeatherApp - Desktop Dashboard

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![PySide6](https://img.shields.io/badge/GUI-PySide6-41CD52?style=for-the-badge&logo=qt&logoColor=white)
![Architecture](https://img.shields.io/badge/Design-Clean_Architecture-purple?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-grey?style=for-the-badge)

**Aplicación de escritorio moderna para monitoreo climático.**
Refactorizada implementando **Clean Architecture**, gestión segura de secretos y diseño modular.

[Reportar Bug](https://github.com/ymvs84/WeatherApp/issues) · [Solicitar Feature](https://github.com/ymvs84/WeatherApp/issues)

</div>

---

## 🚀 Características Técnicas

Este proyecto no es solo una calculadora de clima; es una demostración de ingeniería de software robusta:

* **Arquitectura Modular:** Separación estricta de responsabilidades en `src/ui` (Vista), `src/services` (Lógica de Negocio) y `src/config` (Configuración).
* **Seguridad:** Manejo de API Keys mediante variables de entorno (`.env`), evitando credenciales hardcodeadas en el código fuente.
* **Testing:** Suite de pruebas unitarias con `pytest` implementando *mocking* de servicios para aislar la lógica de red.
* **GUI Reactiva:** Interfaz construida con **PySide6 (Qt)** y estilizada con QSS (Qt Style Sheets).

## 📂 Estructura del Proyecto

```text
WeatherApp/
├── src/
│   ├── config.py       # Gestión de variables de entorno
│   ├── services.py     # Lógica de consumo de API (Requests)
│   └── ui.py           # Interfaz Gráfica (PySide6)
├── tests/              # Tests unitarios mockeados
├── main.py             # Punto de entrada (Entry Point)
├── .env                # Archivo de secretos (No se sube al repo)
└── requirements.txt    # Dependencias
````

## 🛠️ Requisitos Previos

  * Python 3.8 o superior.
  * Una API Key gratuita de [OpenWeatherMap](https://openweathermap.org/).

## ⚙️ Instalación y Configuración

Sigue estos pasos para levantar el entorno de desarrollo:

### 1\. Clonar el repositorio

```bash
git clone [https://github.com/ymvs84/WeatherApp.git](https://github.com/ymvs84/WeatherApp.git)
cd WeatherApp
```

### 2\. Crear entorno virtual (Recomendado)

```bash
python -m venv venv
# En Windows:
.\venv\Scripts\activate
# En Mac/Linux:
source venv/bin/activate
```

### 3\. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4\. Configurar Seguridad (.env)

Este proyecto usa `python-dotenv`. Crea un archivo llamado `.env` en la raíz del proyecto y añade tu clave:

```env
WEATHER_API_KEY=tu_clave_de_openweathermap_aqui
```

*(Sin comillas y sin espacios)*

## ▶️ Ejecución

Para iniciar la aplicación, ejecuta el punto de entrada principal:

```bash
python main.py
```

## 🧪 Pruebas (Testing)

El proyecto incluye tests que validan la lógica sin realizar llamadas reales a la API (Mocking).

```bash
pytest -v
```

## 📦 Compilación a Ejecutable (.exe)

Para generar un archivo ejecutable portable para Windows:

```bash
pyinstaller --onefile --windowed --name="WeatherApp" main.py
```

El archivo resultante estará en la carpeta `dist/`.

-----

**Autor:** Yago Menéndez
*Senior Software Engineer & Computer Science Student* [LinkedIn](https://www.google.com/search?q=https://linkedin.com/in/ymenendez) | [GitHub](https://github.com/ymvs84)

```
