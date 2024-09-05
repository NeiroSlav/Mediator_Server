from structures import ChatLinksHandler
from controller import MessageDTO, bot_topic
from const import HOLDING_LOG
from model.sсheduler import Sсheduler


# обрабатывает удержание топика от закрытия
async def handle_topic_hold(message_dto: MessageDTO):

    # пытаемся достать сессию (линк) чатов
    topic_id = message_dto.chat_id
    chat_link = ChatLinksHandler.get_by_topic_id(topic_id)

    # если её нет - удаляем сам топик
    if not chat_link:
        await bot_topic.delete(topic_id)
        return

    if chat_link.topic.state == "banned":
        raise PermissionError

    # логирование информации об удержании топика
    await bot_topic.log(
        HOLDING_LOG.format(name=message_dto.sender_name, topic=chat_link.topic.name)
    )

    # отменяет закрытие топика (если оно было)
    Sсheduler.cancel_topic_close(chat_link.topic)
    chat_link.topic.meta.hold = True
