
# Telegram Channel Manager Scripts

Este repositorio contiene tres scripts principales para gestionar mensajes y contenidos en un canal de Telegram utilizando la biblioteca `Telethon`. Los scripts te permitirán iniciar sesión, editar captions y generar una tabla de contenidos para los archivos compartidos en el canal.

## Requisitos

- Python 3.x
- Telethon
- dotenv
- Una app configurada en https://my.telegram.org/auth para poder obtener un api_id y un api_hash
- el enlace de invitación al canal que quieres gestionar

Puedes instalar las dependencias necesarias utilizando:

```bash
pip install telethon python-dotenv
```

## Configuración

Antes de ejecutar cualquiera de los scripts, asegúrate de tener un archivo `.env` en el directorio raíz con las siguientes variables de entorno:

```plaintext
API_ID=tu_api_id
API_HASH=tu_api_hash
STRING_SESSION=tu_string_session  # Se generará en el primer inicio de sesión
CHANNEL_INVITE_LINK=tu_enlace_de_invitacion_del_canal
```

## Scripts

### 1. `login.py`

Este script se utiliza para iniciar sesión en Telegram y generar una `StringSession`, que se guarda para su uso posterior.

#### Uso:

```bash
python login.py
```

El script te preguntará si deseas usar una sesión existente o crear una nueva. Si eliges crear una nueva, se te pedirá que ingreses tu número de teléfono para la autenticación y luego generará la `StringSession`.

### 2. `edit_captions.py`

Este script permite previsualizar o editar los captions de los mensajes en un canal de Telegram que contienen archivos `.mobi` con un nombre específico.

#### Uso:

- **Previsualización**:

  ```bash
  python edit_captions.py
  ```

- **Editar captions**:

  ```bash
  python edit_captions.py write
  ```

El script buscará archivos `.mobi` cuyo nombre siga el patrón `Jujutsu Kaisen XXX *` y actualizará el caption del mensaje al formato `Jujutsu Kaisen cXXX`.

### 3. `toc.py`

Este script genera una tabla de contenidos para todas las series de archivos compartidos en el canal. Los mensajes se agrupan por series y se generan enlaces a cada volumen o capítulo, organizados cronológicamente.

#### Uso:

```bash
python toc.py
```

El script generará dos tipos de mensajes en el canal:
1. Una tabla de contenidos general con enlaces a cada serie.
2. Una tabla de contenidos específica para cada serie, separando volúmenes y capítulos, y ordenando los enlaces de más antiguo a más nuevo.

## Notas

- Asegúrate de tener permisos de administrador en el canal de Telegram para que los scripts funcionen correctamente.
- Revisa el contenido generado antes de compartirlo en el canal para asegurarte de que todo esté formateado y ordenado como deseas.
