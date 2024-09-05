from aiogram.types import Message
from aiogram.filters import Command
import asyncio

from controller.bot.init import dp
from controller.bot.filters import MyTopicFilter
from controller.backup.statistics import Statist
from controller import bot_topic
from controller.message_dto import MessageDTO

from model import *


# хендлер команды /close из топика
@dp.message(MyTopicFilter(), Command("close"))
async def get_topic_close(message: Message):
    message_dto = await MessageDTO.parse_tg(message)
    try:
        await handle_topic_close(message_dto)
    except PermissionError:
        await message.delete()


# хендлер команды /hold из топика
@dp.message(MyTopicFilter(), Command("hold"))
async def get_topic_hold(message: Message):
    message_dto = await MessageDTO.parse_tg(message)
    try:
        await handle_topic_hold(message_dto)
    except PermissionError:
        await message.delete()


# хендлен команды /status из топика
@dp.message(MyTopicFilter(), Command("status"))
async def get_topic_status(message: Message):
    message_dto = await MessageDTO.parse_tg(message)
    await handle_topic_status(message_dto)


# хендлер команды /ban из топика
@dp.message(MyTopicFilter(), Command("ban"))
async def get_topic_ban(message: Message):
    message_dto = await MessageDTO.parse_tg(message)
    try:
        await handle_topic_ban(message_dto)
    except PermissionError:
        await message.delete()


# хендлер команды /unban из топика
@dp.message(MyTopicFilter(), Command("unban"))
async def get_topic_unban(message: Message):
    message_dto = await MessageDTO.parse_tg(message)
    try:
        await handle_topic_unban(message_dto)
    except PermissionError:
        await message.delete()


# хендлер сообщения сотрудника из топика
@dp.message(MyTopicFilter())
async def get_topic_message(message: Message):
    message_dto = await MessageDTO.parse_tg(message)
    try:
        await handle_topic_message(message_dto)
    except PermissionError:  # в случае, если топик забанен
        await message.delete()


# хендлер сообщения бота из топика
@dp.message(MyTopicFilter(from_bot=True))
async def get_topic_bot_message(message: Message):
    if message.forum_topic_edited:
        await asyncio.sleep(5)
        await bot_topic.delete_message(message.message_id)


# хендлер сообщения /broadcast из чата бродкаста
@dp.message(MyTopicFilter(broadcast=True), Command("broadcast"))
async def get_broadcast_message(message: Message):
    message_dto = await MessageDTO.parse_tg(message)
    await handle_broadcast_message(message_dto)


# хендлер сообщения /statist из чата бродкаста
@dp.message(MyTopicFilter(broadcast=True), Command("statist"))
async def get_statist_message(message: Message):
    data = await Statist.count()
    await message.answer(f"DB_count: {data}")


# хендлер сообщения /suffix из чата бродкаста
@dp.message(MyTopicFilter(broadcast=True), Command("suffix"))
async def get_suffix_message(message: Message):
    message_dto = await MessageDTO.parse_tg(message)
    await handle_suffix_message(message_dto)
