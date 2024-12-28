from aiogram.types import Message
from aiogram.filters import Command
import asyncio

from controller.bot.init import dp
from controller.bot.filters import MyTopicFilter
from controller.backup.statistics import Statist
from controller import bot_topic
from controller.message_dto import MessageDTO

from model import *


# пытается выполнить команду, ловит и гасит ошибку
async def try_execute(command: callable, message: Message):
    try:
        message_dto = await MessageDTO.parse_tg(message)
        await command(message_dto)
    except PermissionError:
        pass


# далее команды сотрудников из обычных топиков


# хендлер команды /close из топика
@dp.message(MyTopicFilter(), Command("close"))
async def get_topic_close(message: Message):
    await try_execute(handle_close_command, message)


# хендлер команды /hold из топика
@dp.message(MyTopicFilter(), Command("hold"))
async def get_topic_hold(message: Message):
    await try_execute(handle_hold_command, message)


# хендлен команды /status из топика
@dp.message(MyTopicFilter(), Command("status"))
async def get_topic_status(message: Message):
    await try_execute(handle_status_command, message)


# хендлер команды /ban из топика
@dp.message(MyTopicFilter(), Command("ban"))
async def get_topic_ban(message: Message):
    await try_execute(handle_ban_command, message)


# хендлер команды /unban из топика
@dp.message(MyTopicFilter(), Command("unban"))
async def get_topic_unban(message: Message):
    await try_execute(handle_unban_command, message)


# далее сообщения из обычных топиков


# хендлер элиаса сотрудника из топика
@dp.message(MyTopicFilter(alias=True))
async def get_topic_alias(message: Message):
    await try_execute(handle_topic_alias, message)


# хендлер сообщения сотрудника из топика
@dp.message(MyTopicFilter())
async def get_topic_message(message: Message):
    await try_execute(handle_topic_message, message)


# хендлер сообщения бота из топика
@dp.message(MyTopicFilter(from_bot=True))
async def get_topic_bot_message(message: Message):
    if message.forum_topic_edited:
        await asyncio.sleep(10)
        await bot_topic.delete_message(message.message_id)


# далее команды из топика управления


# хендлер элиаса сотрудника из топика
@dp.message(MyTopicFilter(broadcast=True), Command("alias"))
async def get_topic_alias(message: Message):
    await try_execute(handle_controll_aliases, message)


# хендлер сообщения /broadcast из чата бродкаста
@dp.message(MyTopicFilter(broadcast=True), Command("broadcast"))
async def get_broadcast_message(message: Message):
    message_dto = await MessageDTO.parse_tg(message)
    await handle_broadcast_command(message_dto)


# хендлер сообщения /neiro из чата бродкаста
@dp.message(MyTopicFilter(broadcast=True), Command("neiro"))
async def get_neiro_message(message: Message):
    message_dto = await MessageDTO.parse_tg(message)
    await handle_neiro_command(message_dto)


# хендлер сообщения /statist из чата бродкаста
@dp.message(MyTopicFilter(broadcast=True), Command("statist"))
async def get_statist_message(message: Message):
    data = await Statist.count()
    await message.answer(f"count: {data}")


# хендлер сообщения /suffix из чата бродкаста
@dp.message(MyTopicFilter(broadcast=True), Command("suffix"))
async def get_suffix_message(message: Message):
    message_dto = await MessageDTO.parse_tg(message)
    await handle_suffix_command(message_dto)
