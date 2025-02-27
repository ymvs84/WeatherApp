import sys
import requests
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QLineEdit, QPushButton, QLabel, QListWidget, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

# Autor: Yago Menéndez de la Vega
class WeatherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WeatherApp")
        self.setGeometry(100, 100, 450, 600)

        # Widget central y layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        # Estilo general de la ventana
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                            stop:0 #a1c4fd, stop:1 #c2e9fb);
            }
            QLabel {
                font-family: 'Segoe UI';
                font-size: 16px;
                color: #333;
            }
        """)

        # Componentes de la interfaz
        self.city_input = QLineEdit(self)
        self.city_input.setPlaceholderText("Ingresa una ciudad (ej. Madrid)...")
        self.city_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #87aafd;
                border-radius: 10px;
                font-size: 14px;
                background: white;
                color: #333;
            }
            QLineEdit:focus {
                border: 2px solid #5a85f7;
            }
            QLineEdit:placeholder {
                color: #999;
            }
        """)

        self.search_button = QPushButton("Buscar Clima", self)
        self.search_button.setStyleSheet("""
            QPushButton {
                background-color: #5a85f7;
                color: white;
                padding: 10px;
                border-radius: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4268d6;
            }
        """)

        self.weather_label = QLabel("Clima: N/A\nTemperatura: N/A\nHumedad: N/A", self)
        self.weather_label.setAlignment(Qt.AlignCenter)
        self.weather_label.setStyleSheet("""
            QLabel {
                background: rgba(255, 255, 255, 0.8);
                padding: 15px;
                border-radius: 10px;
                font-size: 18px;
                color: #2c3e50;
            }
        """)

        self.weather_icon = QLabel(self)
        self.weather_icon.setAlignment(Qt.AlignCenter)
        self.weather_icon.setStyleSheet("""
            QLabel {
                padding: 10px;
                border: 1px solid #dfe6e9;
                border-radius: 10px;
                background: white;
            }
        """)

        self.favorite_button = QPushButton("Añadir a Favoritas", self)
        self.favorite_button.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                padding: 10px;
                border-radius: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)

        self.favorites_label = QLabel("Ciudades Favoritas", self)
        self.favorites_label.setAlignment(Qt.AlignCenter)
        self.favorites_list = QListWidget(self)
        self.favorites_list.setStyleSheet("""
            QListWidget {
                background: white;
                border: 1px solid #dfe6e9;
                border-radius: 10px;
                padding: 5px;
                font-size: 14px;
                color: #333;
            }
            QListWidget::item:selected {
                background: #87aafd;
                color: white;
            }
        """)

        # Añadir nombre del autor
        self.author_label = QLabel("Creado por: Yago Menéndez de la Vega", self)
        self.author_label.setAlignment(Qt.AlignCenter)
        self.author_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #666;
                padding: 5px;
            }
        """)

        # Añadir componentes al layout
        self.layout.addWidget(self.city_input)
        self.layout.addWidget(self.search_button)
        self.layout.addWidget(self.weather_label)
        self.layout.addWidget(self.weather_icon)
        self.layout.addWidget(self.favorite_button)
        self.layout.addWidget(self.favorites_label)
        self.layout.addWidget(self.favorites_list)
        self.layout.addWidget(self.author_label)
        self.layout.addStretch()

        # Conectar señales
        self.search_button.clicked.connect(self.get_weather)
        self.city_input.returnPressed.connect(self.get_weather)
        self.favorite_button.clicked.connect(self.add_to_favorites)
        self.favorites_list.itemClicked.connect(self.load_favorite_weather)

        # API Key
        self.api_key = "db77de7b9dbe2ba3bdb4bdd1ced40645"  # Reemplaza con tu clave
        self.current_city = None

    def get_weather(self):
        city = self.city_input.text().strip()
        if not city:
            self.show_error_popup("Por favor, ingresa una ciudad.")
            return

        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric&lang=es"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            description = data["weather"][0]["description"].capitalize()
            icon_code = data["weather"][0]["icon"]

            self.weather_label.setText(
                f"Clima: {description}\nTemperatura: {temp}°C\nHumedad: {humidity}%"
            )
            self.load_weather_icon(icon_code)
            self.current_city = city
        except requests.exceptions.RequestException:
            self.show_error_popup(f"No se pudo encontrar el clima para '{city}'. Verifica el nombre o tu conexión.")
            self.weather_icon.clear()

    def load_weather_icon(self, icon_code):
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        try:
            response = requests.get(icon_url, timeout=5)
            response.raise_for_status()
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            self.weather_icon.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))
        except requests.exceptions.RequestException:
            self.weather_icon.setText("Ícono no disponible")

    def add_to_favorites(self):
        if self.current_city and self.current_city not in [self.favorites_list.item(i).text() for i in range(self.favorites_list.count())]:
            self.favorites_list.addItem(self.current_city)
        elif not self.current_city:
            self.show_error_popup("Busca una ciudad primero.")
        else:
            self.show_error_popup(f"'{self.current_city}' ya está en tus favoritas.")

    def load_favorite_weather(self, item):
        self.city_input.setText(item.text())
        self.get_weather()

    def show_error_popup(self, message):
        popup = QMessageBox(self)
        popup.setWindowTitle("Error")
        popup.setText(message)
        popup.setStandardButtons(QMessageBox.Ok)
        popup.setStyleSheet("""
            QMessageBox {
                background-color: #f7f7f7;
                font-size: 14px;
            }
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 5px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        popup.exec()

def run_app():
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    run_app()