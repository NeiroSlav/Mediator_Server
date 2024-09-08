from structures import ChatLinksHandler
from controller import MessageDTO, bot_topic
from const import CLOSING_LOG
from model.sсheduler import Sсheduler
from model.commands.utils import try_get_chat_link


# обрабатывает закрытие топика
async def handle_close_command(message_dto: MessageDTO):

    # пытаемся достать сессию (линк) чатов
    chat_link = await try_get_chat_link(message_dto.chat_id)

    # если сессия есть - закрываем, меняем цвет, ставим флаг "отвечено", пишем в лог
    await chat_link.topic.close()

    # логирование информации о закрытии топика
    await bot_topic.log(
        CLOSING_LOG.format(name=message_dto.sender_name, topic=chat_link.topic.name)
    )

    # отменяет закрытие топика (если оно было)
    Sсheduler.cancel_dialog_close(chat_link)
