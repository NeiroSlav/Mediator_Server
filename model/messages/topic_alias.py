from structures import ChatLinksHandler
from controller import MessageDTO, bot_topic, aliaser
from const import BANNED, ALIAS_SYMBOL, ABON_GOT_TEXT
from model.messages.utils import try_schedule_close


# обрабатывает сообщение из топика
async def handle_topic_alias(message_dto: MessageDTO):

    # пытаемся достать сессию (линк) чатов
    topic_id = message_dto.chat_id
    chat_link = ChatLinksHandler.get_by_topic_id(topic_id=topic_id)

    # если сессии нет
    if not chat_link:
        await bot_topic.delete(topic_id)
        return

    if chat_link.topic.state == BANNED:
        raise PermissionError

    # пытаемся достать текст сокращения
    alias_text = aliaser.get(message_dto.text.lstrip(ALIAS_SYMBOL))
    if not alias_text:
        raise PermissionError

    message_dto.text = alias_text

    # если топик ещё не "отвеченный" ставим флаг, меняем цвет
    user = message_dto.meta["user"]
    await chat_link.topic.answer(user)

    # присваиваем сообщению id лички абона, отправляем наружу
    message_dto.chat_id = chat_link.abon_chat.id
    await chat_link.abon_chat.send(message_dto)

    # информируем сотрудника об отправленном абоненту сообщении
    info_text = ABON_GOT_TEXT.format(text=alias_text)
    info_message = MessageDTO.new(info_text)
    await chat_link.topic.send(info_message)

    try_schedule_close(chat_link)
