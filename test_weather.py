import pytest
from PySide6.QtWidgets import QApplication
from WeatherApp import WeatherApp
import requests

@pytest.fixture
def app(qtbot):
    test_app = WeatherApp()
    qtbot.addWidget(test_app)
    return test_app

def test_empty_input(app, monkeypatch):
    monkeypatch.setattr("PySide6.QtWidgets.QMessageBox.exec", lambda self: None)
    app.city_input.setText("")
    app.get_weather()
    assert app.weather_label.text() == "Clima: N/A\nTemperatura: N/A\nHumedad: N/A"

def test_successful_weather_fetch(app, monkeypatch):
    fake_response = {
        "main": {"temp": 20.5, "humidity": 65},
        "weather": [{"description": "cielo despejado", "icon": "01d"}]
    }
    monkeypatch.setattr(requests, "get", lambda url, **kwargs: type("Response", (), {
        "json": lambda: fake_response if "data/2.5/weather" in url else {"content": b""},
        "raise_for_status": lambda: None,
        "content": b""
    })())
    app.city_input.setText("Madrid")
    app.get_weather()
    assert "Clima: Cielo despejado" in app.weather_label.text()
    assert "Temperatura: 20.5°C" in app.weather_label.text()
    assert "Humedad: 65%" in app.weather_label.text()
    assert app.current_city == "Madrid"

def test_add_to_favorites(app, monkeypatch):
    fake_response = {
        "main": {"temp": 20.5, "humidity": 65},
        "weather": [{"description": "cielo despejado", "icon": "01d"}]
    }
    monkeypatch.setattr(requests, "get", lambda url, **kwargs: type("Response", (), {
        "json": lambda: fake_response if "data/2.5/weather" in url else {"content": b""},
        "raise_for_status": lambda: None,
        "content": b""
    })())
    app.city_input.setText("Madrid")
    app.get_weather()
    app.add_to_favorites()
    assert app.favorites_list.count() == 1
    assert app.favorites_list.item(0).text() == "Madrid"

def test_load_favorite_weather(app, monkeypatch):
    fake_response = {
        "main": {"temp": 15.0, "humidity": 70},
        "weather": [{"description": "nublado", "icon": "04d"}]
    }
    monkeypatch.setattr(requests, "get", lambda url, **kwargs: type("Response", (), {
        "json": lambda: fake_response if "data/2.5/weather" in url else {"content": b""},
        "raise_for_status": lambda: None,
        "content": b""
    })())
    app.favorites_list.addItem("Barcelona")
    app.load_favorite_weather(app.favorites_list.item(0))
    assert "Clima: Nublado" in app.weather_label.text()
    assert "Temperatura: 15.0°C" in app.weather_label.text()