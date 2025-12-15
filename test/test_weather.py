import pytest
from PySide6.QtWidgets import QMessageBox
# Importamos desde nuestra nueva estructura src
from src.ui import WeatherWindow
# No importamos requests, porque vamos a mockear el Servicio, no la red

@pytest.fixture
def app(qtbot):
    # Usamos la nueva clase WeatherWindow
    test_app = WeatherWindow()
    qtbot.addWidget(test_app)
    return test_app

def test_empty_input(app, monkeypatch):
    # Mockeamos el popup de error para que no bloquee el test
    monkeypatch.setattr(QMessageBox, "warning", lambda parent, title, text: None)

    app.city_input.setText("")
    # En la nueva UI el método se llama load_weather, no get_weather
    app.load_weather()

    # Verificamos el estado inicial (o el de error controlado)
    assert "Clima: N/A" in app.weather_label.text()

def test_successful_weather_fetch(app, monkeypatch):
    # --- DATOS FALSOS ---
    fake_weather_data = {
        "main": {"temp": 20.5, "humidity": 65},
        "weather": [{"description": "cielo despejado", "icon": "01d"}]
    }

    # --- MOCKING (La magia) ---
    # En lugar de hackear 'requests', hackeamos nuestro 'WeatherService'
    # Esto le dice al test: "Cuando la UI pida datos, dale este diccionario, no vayas a internet"
    monkeypatch.setattr("src.services.WeatherService.get_weather_data", lambda city: fake_weather_data)
    monkeypatch.setattr("src.services.WeatherService.get_icon_data", lambda icon: b"") # Bytes vacíos para el icono

    # --- ACCIÓN ---
    app.city_input.setText("Madrid")
    app.load_weather() # Método nuevo

    # --- VERIFICACIÓN ---
    # Nota: Ajustamos el texto esperado al formato de tu nueva UI
    assert "Clima: Cielo despejado" in app.weather_label.text()
    assert "Temperatura: 20.5°C" in app.weather_label.text()
    assert "Humedad: 65%" in app.weather_label.text()
    assert app.current_city == "Madrid"

def test_add_to_favorites(app, monkeypatch):
    fake_weather_data = {
        "main": {"temp": 20.5, "humidity": 65},
        "weather": [{"description": "cielo despejado", "icon": "01d"}]
    }
    monkeypatch.setattr("src.services.WeatherService.get_weather_data", lambda city: fake_weather_data)
    monkeypatch.setattr("src.services.WeatherService.get_icon_data", lambda icon: b"")

    app.city_input.setText("Madrid")
    app.load_weather()
    app.add_to_favorites()

    assert app.favorites_list.count() == 1
    assert app.favorites_list.item(0).text() == "Madrid"

def test_load_favorite_weather(app, monkeypatch):
    fake_weather_data = {
        "main": {"temp": 15.0, "humidity": 70},
        "weather": [{"description": "nublado", "icon": "04d"}]
    }
    monkeypatch.setattr("src.services.WeatherService.get_weather_data", lambda city: fake_weather_data)
    monkeypatch.setattr("src.services.WeatherService.get_icon_data", lambda icon: b"")

    app.favorites_list.addItem("Barcelona")
    # Simulamos el clic
    app.favorites_list.itemClicked.emit(app.favorites_list.item(0))

    assert "Clima: Nublado" in app.weather_label.text()
