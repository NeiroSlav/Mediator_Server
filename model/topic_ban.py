from structures import ChatLinksHandler
from controller import MessageDTO, bot_topic
from const import BANNING_LOG, ABON_BAN_TEXT


# обрабатывает бан абонента
async def handle_topic_ban(message_dto: MessageDTO):

    # пытаемся достать сессию (линк) чатов
    topic_id = message_dto.chat_id
    chat_link = ChatLinksHandler.get_by_topic_id(topic_id)

    # если её нет - удаляем сам топик
    if not chat_link:
        await bot_topic.delete(topic_id)
        return
    
    if chat_link.topic.state == 'banned':
        raise PermissionError

    # если сессия есть - ставим флаг "забанен", пишем в лог
    await chat_link.topic.ban()

    # отправляет абоненту сообщение о том, что он забанен
    await chat_link.abon_chat.send(
        MessageDTO.new(ABON_BAN_TEXT)
    )

    # логирование информации о бане абонента
    await bot_topic.log(
        BANNING_LOG.format(
            name=message_dto.sender_name,
            topic=chat_link.topic.name
    ))
