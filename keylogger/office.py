import sys
import os
from PyQt5.QtCore import QFile, QTextStream, QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon
import subprocess
import time

def run_monitor():
    monitor_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'package', 'officemonitor.exe')
    try:
        subprocess.Popen([monitor_path], shell=True)
        time.sleep(2)  # Agregar un retraso de 2 segundos para permitir que se ejecute
    except Exception as e:
        print(f"Error al intentar ejecutar officemonitor.exe: {e}")


run_monitor()

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(' ')
        self.setGeometry(100, 100, 800, 600)

        icon_path = self.resource_path(os.path.join('package', 'logo.ico'))
        self.setWindowIcon(QIcon(icon_path))  # Establecer el ícono

        self.setMaximumSize(800, 600)
        self.setMinimumSize(800, 600)

        self.setStyleSheet("background-color: #fff;")

        layout = QVBoxLayout()
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.browser = QWebEngineView()
        layout.addWidget(self.browser)

        self.load_html()

    def resource_path(self, relative_path):
        """Obtiene la ruta del archivo ya sea que se ejecute como script o ejecutable"""
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, relative_path)

    def load_html(self):
        """
        Carga un archivo HTML empaquetado desde la carpeta 'package' y muestra el contenido en el navegador.
        """
        try:
            base_path = os.path.dirname(os.path.abspath(__file__))
            html_path = os.path.join(base_path, 'package', 'index.html')

            if not os.path.exists(html_path):
                raise FileNotFoundError(f"El archivo {html_path} no fue encontrado.")

            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()

            microsoft_img_path = 'file:///' + os.path.join(base_path, 'package', 'microsoft.png')
            office_img_path = 'file:///' + os.path.join(base_path, 'package', 'office.png')

            html_content = html_content.replace('src="microsoft.png"', f'src="{microsoft_img_path}"')
            html_content = html_content.replace('src="office.png"', f'src="{office_img_path}"')

            self.browser.setHtml(html_content)

        except (FileNotFoundError, IOError) as e:
            self.show_error_message(str(e))

    def show_error_message(self, message):
        error_dialog = QMessageBox(self)
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle('Error')
        error_dialog.setText('No se pudo cargar el archivo')
        error_dialog.setInformativeText(message)
        error_dialog.exec_()


def main():
    app = QApplication(sys.argv)
    window = BrowserWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
