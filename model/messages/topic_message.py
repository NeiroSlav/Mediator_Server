from structures import ChatLinksHandler
from controller import MessageDTO, bot_topic
from model.messages.utils import try_schedule_close


# обрабатывает сообщение из топика
async def handle_topic_message(message_dto: MessageDTO):

    # если сообщение является комментарием, ничего не делать
    if message_dto.text.startswith("/"):
        return

    # пытаемся достать сессию (линк) чатов
    topic_id = message_dto.chat_id
    chat_link = ChatLinksHandler.get_by_topic_id(topic_id=topic_id)

    # если сессии нет, или топик закрыт
    if not chat_link:
        await bot_topic.delete(topic_id)
        return

    if chat_link.topic.state == "banned":
        raise PermissionError

    # если топик ещё не "отвеченный" ставим флаг, меняем цвет
    user = message_dto.meta["user"]
    await chat_link.topic.answer(user)

    # присваиваем сообщению id лички абона, отправляем наружу
    message_dto.chat_id = chat_link.abon_chat.id
    await chat_link.abon_chat.send(message_dto)

    await try_schedule_close(chat_link)
