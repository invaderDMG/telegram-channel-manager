from telethon import TelegramClient
from serie import Serie
import re

class TablaDeContenidos:
    def __init__(self):
        self.series = {}

    def agregar_serie(self, nombre):
        if nombre not in self.series:
            self.series[nombre] = Serie(nombre)
        return self.series[nombre]

    async def generar_toc_general(self, client: TelegramClient, channel):
        series_links = []
        for serie in sorted(self.series.values(), key=lambda s: s.nombre.lower()):
            await serie.generar_mensajes_toc(client, channel)
            series_links.append(serie.obtener_enlace())

        # Dividir la tabla de contenidos general en dos si es muy larga
        mid_point = len(series_links) // 2
        toc_overview_message_1 = "📖 **TABLA DE CONTENIDOS DE SERIES (1)**\n#tableOfContents\n\n" + "\n".join(series_links[:mid_point])
        toc_overview_message_2 = "📖 **TABLA DE CONTENIDOS DE SERIES (2)**\n#tableOfContents\n\n" + "\n".join(series_links[mid_point:])

        print("Tabla de Contenidos de Series generada:")
        print(toc_overview_message_1)
        print(toc_overview_message_2)

        # Enviar las dos partes de la tabla de contenidos general al canal y fijar ambos mensajes
        toc_overview_msg_1 = await client.send_message(channel, toc_overview_message_1)
        toc_overview_msg_2 = await client.send_message(channel, toc_overview_message_2)
        
        await client.pin_message(channel, toc_overview_msg_1, notify=False)
        await client.pin_message(channel, toc_overview_msg_2, notify=False)
        print(f"Tablas de contenidos generales fijadas (mensajes {toc_overview_msg_1.id} y {toc_overview_msg_2.id}).")