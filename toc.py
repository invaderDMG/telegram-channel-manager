import os
import re
from telethon import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv
from tabla_de_contenidos import TablaDeContenidos

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
string_session = os.getenv('STRING_SESSION')
channel_invite_link = os.getenv('CHANNEL_INVITE_LINK')

# Crear una sesión de Telegram usando el número de teléfono
client = TelegramClient(StringSession(string_session), api_id, api_hash)

async def delete_previous_toc_messages(channel):
    async for message in client.iter_messages(channel):
        if message.text and "#tableOfContents" in message.text:
            await message.delete()
            print(f"Mensaje {message.id} eliminado.")

async def generate_series_toc():
    channel = await client.get_entity(channel_invite_link)

    # Eliminar mensajes previos que contienen "#tableOfContents"
    await delete_previous_toc_messages(channel)

    toc = TablaDeContenidos()

    async for message in client.iter_messages(channel, reverse=True):  # Iterar en orden cronológico (de más antiguo a más nuevo)
        if message.media and message.file and message.message:
            match = re.match(r"(.+?)\s+[vc](\d{2,3})", message.message)
            if match:
                series_name = match.group(1).strip()
                number = match.group(2)
                tipo = 'v' if 'v' in match.group(0) else 'c'
                enlace = f"[{tipo}{number:02}](https://t.me/c/{channel.id}/{message.id})"
                serie = toc.agregar_serie(series_name)
                serie.agregar_enlace(enlace, tipo)

    await toc.generar_toc_general(client, channel)

if __name__ == "__main__":
    with client:
        # Iniciar sesión usando la sesión guardada
        client.start()
        client.loop.run_until_complete(generate_series_toc())