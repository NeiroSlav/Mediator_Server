from pydantic import BaseModel
from aiogram import types
from controller.bot.init import bot
from const import BOT_TOKEN

class MessageDTO(BaseModel):
    social: str
    chat_id: int
    sender_name: str
    text: str | None
    image: str | None
    meta: dict

    @classmethod
    async def parce_tg(cls, message: types.Message):
        chat_id = message.chat.id
        if message.message_thread_id:
            chat_id = message.message_thread_id

        text = ''
        image = None
        meta = {}

        if message.photo:  # если есть фото, берёт его id и подпись
            file_id = message.photo[-1].file_id
            file = await bot.get_file(file_id)
            image = f'https://api.telegram.org/file/bot{BOT_TOKEN}/{file.file_path}'
            text = message.caption

        elif message.text:  # или если есть просто текст, берёт его 
            text = message.text

        elif message.animation:  # или если есть анимация, берёт id
            meta['animation'] = message.animation.file_id

        elif message.sticker:  # или если есть стикер, берёт id
            meta['sticker'] = message.sticker.file_id
            

        return cls(
            social = 'tg',
            chat_id = chat_id,
            sender_name = message.from_user.full_name,
            text = text,
            image = image,
            meta = meta,
        )

    @classmethod
    def new(cls, text: str, chat_id: int = 0, image: str = None):
        return cls(
            social = '--',
            chat_id = chat_id,
            sender_name = 'MEDIATOR',
            text = text,
            image = None,
            meta = {},
        )