from telethon import TelegramClient

class Serie:
    def __init__(self, nombre):
        self.nombre = nombre
        self.volumes = []
        self.chapters = []
        self.messages = []

    def agregar_enlace(self, enlace, tipo):
        if tipo == 'v':
            self.volumes.append(enlace)
        elif tipo == 'c':
            self.chapters.append(enlace)

    async def generar_mensajes_toc(self, client: TelegramClient, channel):
        total_links = self.volumes + self.chapters
        num_parts = (len(total_links) + 49) // 50

        for i in range(0, len(total_links), 50):
            part_num = i // 50 + 1
            toc_message = f"**{self.nombre}**\n"
            if num_parts > 1:
                toc_message += f"Parte {part_num}\n\n"
            for j in range(i, min(i + 50, len(total_links)), 10):
                toc_message += ' '.join(total_links[j:j+10]) + '\n'
            toc_message += "#tableOfContents"

            message = await client.send_message(channel, toc_message)
            if num_parts == 1:
                self.messages.append(f"https://t.me/c/{channel.id}/{message.id}")
            else:
                self.messages.append(f"[Parte {part_num}](https://t.me/c/{channel.id}/{message.id})")

    def obtener_enlace(self):
        if len(self.messages) == 1:
            return f"📚 **[{self.nombre}]({self.messages[0]})**"
        else:
            return f"📚 **{self.nombre}** " + ' '.join(self.messages)