import sys
from PySide6.QtWidgets import QApplication
from src.ui import WeatherWindow

def main():
    app = QApplication(sys.argv)

    try:
        window = WeatherWindow()
        window.show()
        sys.exit(app.exec())
    except ValueError as e:
        print(e)
        # Aquí podrías mostrar un popup de error antes de cerrar si falla la config
        sys.exit(1)

if __name__ == "__main__":
    main()
