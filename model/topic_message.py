from structures import ChatLinksHandler
from controller import MessageDTO, bot_topic


async def handle_topic_message(message_dto: MessageDTO):
    # если сообщение является комментарием, ничего не делать
    if message_dto.text and message_dto.text.startswith('/'):
        return

    # пытаемся достать сессию (линк) чатов
    topic_id = message_dto.chat_id
    chat_link = ChatLinksHandler.get_by_topic_id(topic_id=topic_id)

    # если сессии нет, или топик закрыт
    if not chat_link or chat_link.topic.closed:
        return

    # ставим флаг "отвечено", меняем цвет
    chat_link.topic.answered = True
    if chat_link.topic.color != 'yellow':
        await chat_link.topic.set_color('yellow')
        await ChatLinksHandler.backup()

    message_dto.chat_id = chat_link.abon_chat.id
    await chat_link.abon_chat.send(message_dto)
    