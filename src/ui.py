import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QLineEdit, QPushButton, QLabel, QListWidget, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from .services import WeatherService  # <--- Importamos nuestro servicio limpio

class WeatherWindow(QMainWindow): # Renombrado a Window para ser más semántico
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WeatherApp Pro")
        self.setGeometry(100, 100, 450, 600)

        # Widget central y layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        self._setup_styles()
        self._setup_ui()

        self.current_city = None

    def _setup_styles(self):
        # Movemos los estilos aquí para limpiar el __init__
        self.setStyleSheet("""
            QMainWindow { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #a1c4fd, stop:1 #c2e9fb); }
            QLabel { font-family: 'Segoe UI'; font-size: 16px; color: #333; }
            QLineEdit { padding: 10px; border: 2px solid #87aafd; border-radius: 10px; font-size: 14px; background: white; }
            QLineEdit:focus { border: 2px solid #5a85f7; }
            QPushButton { background-color: #5a85f7; color: white; padding: 10px; border-radius: 10px; font-weight: bold; }
            QPushButton:hover { background-color: #4268d6; }
            QListWidget { background: white; border-radius: 10px; padding: 5px; }
        """)

    def _setup_ui(self):
        self.city_input = QLineEdit(self)
        self.city_input.setPlaceholderText("Ingresa ciudad (ej. Madrid)...")

        self.search_button = QPushButton("Buscar Clima", self)

        self.weather_label = QLabel("Clima: N/A\nTemperatura: N/A\nHumedad: N/A", self)
        self.weather_label.setAlignment(Qt.AlignCenter)
        self.weather_label.setStyleSheet("background: rgba(255, 255, 255, 0.8); padding: 15px; border-radius: 10px;")

        self.weather_icon = QLabel(self)
        self.weather_icon.setAlignment(Qt.AlignCenter)

        self.favorite_button = QPushButton("Añadir a Favoritas", self)
        self.favorite_button.setStyleSheet("background-color: #2ecc71;")

        self.favorites_list = QListWidget(self)

        self.layout.addWidget(self.city_input)
        self.layout.addWidget(self.search_button)
        self.layout.addWidget(self.weather_label)
        self.layout.addWidget(self.weather_icon)
        self.layout.addWidget(self.favorite_button)
        self.layout.addWidget(QLabel("Favoritas", self))
        self.layout.addWidget(self.favorites_list)

        # Conexiones
        self.search_button.clicked.connect(self.load_weather)
        self.city_input.returnPressed.connect(self.load_weather)
        self.favorite_button.clicked.connect(self.add_to_favorites)
        self.favorites_list.itemClicked.connect(lambda item: self.city_input.setText(item.text()) or self.load_weather())

    def load_weather(self):
        city = self.city_input.text().strip()
        if not city:
            self.show_error("Por favor, escribe una ciudad.")
            return

        # --- AQUÍ ESTÁ LA MAGIA DE LA REFACTORIZACIÓN ---
        try:
            # 1. Llamamos al servicio (Lógica pura)
            data = WeatherService.get_weather_data(city)

            # 2. Procesamos datos
            desc = data["weather"][0]["description"].capitalize()
            temp = data["main"]["temp"]
            hum = data["main"]["humidity"]
            icon_code = data["weather"][0]["icon"]

            # 3. Actualizamos UI
            self.weather_label.setText(f"Clima: {desc}\nTemperatura: {temp}°C\nHumedad: {hum}%")
            self.current_city = city

            # 4. Icono
            icon_bytes = WeatherService.get_icon_data(icon_code)
            if icon_bytes:
                pixmap = QPixmap()
                pixmap.loadFromData(icon_bytes)
                self.weather_icon.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))

        except ValueError as e:
            self.show_error(str(e)) # "Ciudad no encontrada"
        except ConnectionError as e:
            self.show_error(str(e)) # "Error de internet"
        except Exception as e:
            self.show_error(f"Error inesperado: {e}")

    def add_to_favorites(self):
        if self.current_city:
            items = [self.favorites_list.item(i).text() for i in range(self.favorites_list.count())]
            if self.current_city not in items:
                self.favorites_list.addItem(self.current_city)

    def show_error(self, message):
        QMessageBox.warning(self, "Atención", message)
