from typing import Any
from aiogram.filters import BaseFilter
from aiogram.types import Message

from const import GROUP_ID, BROADCAST_ID, BOT_ID, ALIAS_SYMBOL, COMMENT_SYMBOL


# класс фильтрации топика
class MyTopicFilter(BaseFilter):
    def __init__(
        self, broadcast: bool = False, from_bot: bool = False, alias: bool = False
    ):
        self.broadcast = broadcast
        self.from_bot = from_bot
        self.alias = alias

    async def __call__(self, message: Message) -> bool:

        # если чат не группа, или супергруппа
        if message.chat.type not in ("group", "supergroup"):
            return False

        # если сообщение не из нужной группы
        if message.chat.id != GROUP_ID:
            return False

        # если сообщение от бота, но флаг сообщения от бота False
        elif message.from_user.id == BOT_ID and not self.from_bot:
            return False

        # если сообщение из чата бродкаста, но флаг сообщения бродкаста False
        elif message.message_thread_id == BROADCAST_ID and not self.broadcast:
            return False

        # если сообщение начинается с символа элиаса, но флаг элиаса не установлен (и наоборот)
        elif message.text.startswith(ALIAS_SYMBOL) != self.alias:
            return False

        return True
