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

# Definir el patrón de búsqueda para el título del archivo
pattern = re.compile(r"Astro Boy v(\d{2})")

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
        if message.media and message.message:  # Asegurarse de que el mensaje tiene un caption
            caption = message.message
            match = pattern.match(caption)
            if match:
                volume_number = match.group(1)  # Extraer el número del volumen
                new_caption = f"Astro Boy v{volume_number}"
                if write:
                    # Editar el caption si cumple con el patrón
                    await client.edit_message(channel, message.id, new_caption)
                    print(f"Mensaje {message.id} con caption '{caption}' editado a '{new_caption}'")
                else:
                    # Mostrar previsualización
                    print(f"Previsualización: Mensaje {message.id} con caption '{caption}' tendría el caption '{new_caption}'")

if __name__ == "__main__":
    with client:
        # Iniciar sesión usando el número de teléfono
        client.start()

        # Verificar la conexión al canal antes de continuar
        if client.loop.run_until_complete(check_connection()):
            write_mode = len(sys.argv) > 1 and sys.argv[1].lower() == 'write'
            client.loop.run_until_complete(preview_or_edit_captions(write=write_mode))