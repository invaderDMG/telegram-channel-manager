import os
import re
import time
from telethon import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
string_session = os.getenv('STRING_SESSION')
channel_invite_link = os.getenv('CHANNEL_INVITE_LINK')

# Ruta de la carpeta de subida
uploads_folder = "uploads"

# Crear una sesión de Telegram usando el número de teléfono
client = TelegramClient(StringSession(string_session), api_id, api_hash)

# Función para limpiar el nombre del archivo y obtener el caption
def get_clean_caption(filename):
    # Capturar volúmenes con "vXX"
    volume_pattern = re.compile(r"(.+?)v\s*(\d{2})")
    # Capturar capítulos con "cXXX"
    chapter_pattern = re.compile(r"(.+?)\s+(\d{3})")

    # Verificar si es un volumen
    volume_match = volume_pattern.match(filename)
    if volume_match:
        series_name = volume_match.group(1).strip()
        volume_number = volume_match.group(2).strip()
        return f"{series_name} v{volume_number}"

    # Verificar si es un capítulo
    chapter_match = chapter_pattern.match(filename)
    if chapter_match:
        series_name = chapter_match.group(1).strip()
        chapter_number = chapter_match.group(2).strip()
        return f"{series_name} c{chapter_number}"

    # Si no coincide con ninguno, usar el nombre del archivo sin la extensión
    return os.path.splitext(filename)[0]

# Función de callback para mostrar el progreso y la velocidad de transferencia
def progress_callback(current, total, start_time):
    elapsed_time = time.time() - start_time
    if elapsed_time == 0:
        elapsed_time = 1  # Para evitar división por cero
    speed = current / elapsed_time  # Bytes por segundo
    percentage = current / total * 100
    print(f'\rSubido {current}/{total} bytes ({percentage:.2f}%) a {speed / 1024:.2f} KB/s', end='')

async def upload_files():
    channel = await client.get_entity(channel_invite_link)

    # Obtener todos los archivos en la carpeta de subidas
    files = sorted(os.listdir(uploads_folder))  # Ordenar los archivos alfabéticamente

    for file in files:
        # Saltar el archivo .DS_Store
        if file == '.DS_Store':
            continue

        file_path = os.path.join(uploads_folder, file)
        if os.path.isfile(file_path):  # Asegurarse de que sea un archivo
            caption = get_clean_caption(file)
            print(f"Subiendo {file} con caption '{caption}'...")
            start_time = time.time()
            await client.send_file(
                channel, 
                file_path, 
                caption=caption, 
                progress_callback=lambda current, total: progress_callback(current, total, start_time)
            )
            print(f"\n{file} subido en {time.time() - start_time:.2f} segundos.\n")

    print("Subida de archivos completada.")

if __name__ == "__main__":
    with client:
        # Iniciar sesión usando la sesión guardada
        client.start()
        client.loop.run_until_complete(upload_files())