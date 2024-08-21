import os
import re
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
pattern = re.compile(r"(.+?)\s+[vc](\d{2,3})")  # Captura el nombre de la serie y el número de volumen o capítulo

async def generate_series_toc():
    channel = await client.get_entity(channel_invite_link)

    toc = {}
    
    async for message in client.iter_messages(channel, reverse=True):  # Iterar en orden cronológico (de más antiguo a más nuevo)
        if message.media and message.file and message.message:
            match = pattern.match(message.message)
            if match:
                series_name = match.group(1).strip()
                number = match.group(2)
                link = f"[v{number:02}](https://t.me/c/{channel.id}/{message.id})" if 'v' in match.group(0) else f"[c{number:02}](https://t.me/c/{channel.id}/{message.id})"
                
                if series_name not in toc:
                    toc[series_name] = {'volumes': [], 'chapters': []}
                
                if 'v' in match.group(0):
                    toc[series_name]['volumes'].append(link)
                else:
                    toc[series_name]['chapters'].append(link)

    # Crear y enviar la tabla de contenidos de cada serie
    series_links = []
    for series_name in toc.keys():
        toc_message = f"**{series_name}**\n"

        # Añadir los volúmenes primero, seguidos de los capítulos
        if toc[series_name]['volumes']:
            toc_message += "Volúmenes:\n"
            for i in range(0, len(toc[series_name]['volumes']), 10):
                toc_message += ' '.join(toc[series_name]['volumes'][i:i+10]) + '\n'

        if toc[series_name]['chapters']:
            toc_message += "Capítulos:\n"
            for i in range(0, len(toc[series_name]['chapters']), 10):
                toc_message += ' '.join(toc[series_name]['chapters'][i:i+10]) + '\n'

        series_message = await client.send_message(channel, toc_message)
        series_link = f"📚 **[{series_name}](https://t.me/c/{channel.id}/{series_message.id})**"
        series_links.append(f"• {series_link}")

    # Ordenar la tabla de contenidos general alfabéticamente por nombre de serie
    series_links = sorted(series_links, key=lambda x: x.lower())

    # Crear la tabla de contenidos general con formato y emojis
    toc_overview_message = "📖 **TABLA DE CONTENIDOS DE SERIES**\n\n" + "\n".join(series_links)
    print("Tabla de Contenidos de Series generada:")
    print(toc_overview_message)

    # Enviar la tabla de contenidos general al canal
    await client.send_message(channel, toc_overview_message)

if __name__ == "__main__":
    with client:
        # Iniciar sesión usando la sesión guardada
        client.start()
        client.loop.run_until_complete(generate_series_toc())