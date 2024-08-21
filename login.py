from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')

# Preguntar si se quiere utilizar una sesión existente o nueva
use_existing_session = input("¿Quieres utilizar una sesión existente? (s/n): ").strip().lower()

if use_existing_session == 's':
    session_string = input("Introduce tu string session: ")
    client = TelegramClient(StringSession(session_string), api_id, api_hash)
else:
    client = TelegramClient(StringSession(), api_id, api_hash)

async def main():
    me = await client.get_me()
    print(f"Conectado como {me.first_name} ({me.username})")
    session_string = client.session.save()
    print(f"Tu sesión ha sido guardada. String session: {session_string}")

with client:
    client.loop.run_until_complete(main())