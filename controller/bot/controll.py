from controller.bot.init import bot
from controller.message_dto import MessageDTO
from const import GROUP_ID
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import FSInputFile
import requests
import asyncio


class BotTopic:

    # отправка сообщения в топик
    async def send(self, message_dto: MessageDTO):
        
        if message_dto.image:  # если есть изображение из тг
            await bot.send_photo(
                chat_id=GROUP_ID, 
                message_thread_id=message_dto.chat_id, 
                caption=message_dto.text,
                photo=self._load_image(message_dto.image),
            )

        elif message_dto.text:  # если есть текст
            await bot.send_message(
                chat_id=GROUP_ID, 
                message_thread_id=message_dto.chat_id, 
                text=message_dto.text,
            )
        elif message_dto.meta.get('animation'):  # если есть гифка
            await bot.send_animation(
                chat_id=GROUP_ID,
                message_thread_id=message_dto.chat_id,
                animation=message_dto.meta['animation']
            )
        elif message_dto.meta.get('sticker'):  # если есть стикер
            await bot.send_sticker(
                chat_id=GROUP_ID,
                message_thread_id=message_dto.chat_id,
                sticker=message_dto.meta['sticker']
            )

    # открытие нового топика
    async def create(self, name: str, image_color: int) -> int:
        data = await bot.create_forum_topic(GROUP_ID, name, image_color)
        return data.message_thread_id

    # смена имени топика
    async def set_name(self, topic_id: int, name: str):
        try:
            await bot.edit_forum_topic(GROUP_ID, topic_id, name)
        except TelegramBadRequest: pass

    # закрыть топик
    async def close(self, topic_id: int):
        try:
            await bot.close_forum_topic(GROUP_ID, topic_id)
        except TelegramBadRequest: pass

    # открытие закрытого топика
    async def reopen(self, topic_id: int, retry_flag: bool = True):
        try:
            await bot.reopen_forum_topic(GROUP_ID, topic_id)
        except Exception:
            if retry_flag:  # ждёт 3 секунды, рекурсивно вызывает себя один раз
                asyncio.sleep(3)
                await self.reopen(topic_id, retry_flag=False)
            
    # удаление топика
    async def delete(self, topic_id: int):
        await bot.delete_forum_topic(GROUP_ID, topic_id)

    # отправка сообщения в топик лога
    async def log(self, text: str):
        await bot.send_message(GROUP_ID, text)

    # удаление сообщения из чата
    async def delete_message(self, message_id: int):
        try:
            await bot.delete_message(GROUP_ID, message_id=message_id)
        except TelegramBadRequest: pass

    # Скачивание изображения во временный файл
    def _load_image(self, image_url: str):
            response = requests.get(image_url)

            temp_file_path = 'temp_image.jpg'
            with open(temp_file_path, 'wb') as file:
                file.write(response.content)

            return FSInputFile(temp_file_path)

bot_topic = BotTopic()
