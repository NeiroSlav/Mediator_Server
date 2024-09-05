from structures import ChatLinksHandler
from controller import MessageDTO
from const import AUTO_CLOSE_TIME
from model.sсheduler import Sсheduler


# обрабатывает сообщение из топика
async def handle_topic_message(message_dto: MessageDTO):

    # если сообщение является комментарием, ничего не делать
    if message_dto.text.startswith("/"):
        return

    # пытаемся достать сессию (линк) чатов
    topic_id = message_dto.chat_id
    chat_link = ChatLinksHandler.get_by_topic_id(topic_id=topic_id)

    # если сессии нет, или топик закрыт
    if not chat_link or chat_link.topic.state == "closed":
        return

    if chat_link.topic.state == "banned":
        raise PermissionError

    # если топик ещё не "отвеченный" ставим флаг, меняем цвет
    if chat_link.topic.state != "answered":
        chat_link.topic.user = message_dto.meta["user"]
        await chat_link.topic.answer()

    # или если топик взял новый сотрудник, обновляем эти данные
    elif chat_link.topic.user != message_dto.meta["user"]:
        chat_link.topic.user = message_dto.meta["user"]
        await chat_link.topic.update_sign()

    # присваиваем сообщению id лички абона, отправляем наружу
    message_dto.chat_id = chat_link.abon_chat.id
    await chat_link.abon_chat.send(message_dto)

    # если установлено время автозакрытия топика, и топик не удержан, отложит этот процесс
    if AUTO_CLOSE_TIME and not chat_link.topic.hold:
        await Sсheduler.sсhedule_topic_close(chat_link.topic)
