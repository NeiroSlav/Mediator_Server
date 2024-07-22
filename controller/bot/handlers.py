from aiogram.types import Message
from aiogram.filters import Command
import asyncio

from controller.bot.init import dp
from controller.bot.filters import MyTopicFilter
from controller import bot_topic
from controller.message_dto import MessageDTO

from model import handle_topic_close, handle_topic_message, handle_broadcast_message


# хендлер команды /close из топика
@dp.message(MyTopicFilter(), Command("close"))
async def get_topic_close(message: Message):
    message_dto = MessageDTO.parce_tg(message)
    await handle_topic_close(message_dto)


# хендлер сообщения сотрудника из топика
@dp.message(MyTopicFilter())
async def get_topic_message(message: Message):
    message_dto = MessageDTO.parce_tg(message)
    await handle_topic_message(message_dto)


# хендлер сообщения бота из топика
@dp.message(MyTopicFilter(from_bot=True))
async def get_topic_bot_message(message: Message):
    if message.forum_topic_edited:
        await asyncio.sleep(5)
        await bot_topic.delete_message(message.message_id)

# хендлер сообщения /broadcast из чата бродкаста
@dp.message(MyTopicFilter(broadcast=True), Command("broadcast"))
async def get_broadcast_message(message: Message):
    message_dto = MessageDTO.parce_tg(message)
    await handle_broadcast_message(message_dto)
