from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv
import os
import sys
import asyncio

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

if not api_id or not api_hash:
    print('Falta API_ID o API_HASH en el archivo .env')
    sys.exit(1)

api_id = int(api_id)

# Preguntar si se quiere utilizar una sesión existente o nueva
use_existing_session = input("¿Quieres utilizar una sesión existente? (s/n): ").strip().lower()

# Ensure an asyncio event loop exists (Python 3.10+ / 3.14 environments may not have a running loop).
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

if use_existing_session == 's':
    session_string = input("Introduce tu string session: ").strip()
    client = TelegramClient(StringSession(session_string), api_id, api_hash)
else:
    client = TelegramClient(StringSession(), api_id, api_hash)

# Usamos la API síncrona de Telethon: no hace falta manejar el loop manualmente.
with client:
    me = client.get_me()
    name = getattr(me, 'first_name', None) or getattr(me, 'username', None) or str(me)
    print(f"Conectado como {name}")
    session_string = client.session.save()
    print(f"Tu sesión ha sido guardada. String session: {session_string}")