import os
import re
import sys
from telethon import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
string_session = os.getenv('STRING_SESSION')
channel_invite_link = os.getenv('CHANNEL_INVITE_LINK')

# Crear una sesión de Telegram usando el número de teléfono
client = TelegramClient(StringSession(string_session), api_id, api_hash)

# Definir el patrón de búsqueda para el nombre del archivo
pattern = re.compile(r"Jujutsu Kaisen (\d{3}) .*\.mobi")

async def check_connection():
    try:
        channel = await client.get_entity(channel_invite_link)
        print(f"Conexión exitosa al canal: {channel.title}")
        return True
    except Exception as e:
        print(f"Error al conectarse al canal: {e}")
        return False

async def preview_or_edit_captions(write=False):
    channel = await client.get_entity(channel_invite_link)

    async for message in client.iter_messages(channel):
        if message.media and message.file:  # Asegurarse de que el mensaje tiene un archivo adjunto
            file_name = message.file.name
            match = pattern.match(file_name)
            if match:
                version = match.group(1)  # Extraer los dos dígitos de la versión
                new_caption = f"Jujutsu Kaisen c{version}"
                if write:
                    # Editar el caption si el archivo es .mobi y cumple con el patrón
                    await client.edit_message(channel, message.id, new_caption)
                    print(f"Mensaje {message.id} con archivo {file_name} editado a '{new_caption}'")
                else:
                    # Mostrar previsualización
                    print(f"Previsualización: Mensaje {message.id} con archivo {file_name} tendría el caption '{new_caption}'")

if __name__ == "__main__":
    with client:
        # Iniciar sesión usando el número de teléfono
        client.start()

        # Verificar la conexión al canal antes de continuar
        if client.loop.run_until_complete(check_connection()):
            write_mode = len(sys.argv) > 1 and sys.argv[1].lower() == 'write'
            client.loop.run_until_complete(preview_or_edit_captions(write=write_mode))