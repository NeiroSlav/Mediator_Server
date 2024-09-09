from structures import ChatLinksHandler
from controller import MessageDTO, bot_topic
from const import BANNING_LOG, ABON_BAN_TEXT
from model.scheduler import Scheduler
from model.commands.utils import try_get_chat_link


# обрабатывает бан абонента
async def handle_ban_command(message_dto: MessageDTO):

    # пытаемся достать сессию (линк) чатов
    chat_link = await try_get_chat_link(message_dto.chat_id)

    # если сессия есть - ставим флаг "забанен", пишем в лог
    await chat_link.topic.ban()

    # отправляет абоненту сообщение о том, что он забанен
    await chat_link.abon_chat.send(MessageDTO.new(ABON_BAN_TEXT))

    # логирование информации о бане абонента
    await bot_topic.log(
        BANNING_LOG.format(name=message_dto.sender_name, topic=chat_link.topic.name)
    )

    # отменяет закрытие топика (если оно было)
    Scheduler.cancel_dialog_close(chat_link)
