from structures import ChatLinksHandler
from controller import MessageDTO, bot_topic
from const import BANNING_LOG


# обрабатывает бан абонента
async def handle_topic_ban(message_dto: MessageDTO):

    # пытаемся достать сессию (линк) чатов
    topic_id = message_dto.chat_id
    chat_link = ChatLinksHandler.get_by_topic_id(topic_id)

    # если её нет - удаляем сам топик
    if not chat_link:
        await bot_topic.delete(topic_id)
        return
    
    if chat_link.topic.banned:
        raise PermissionError

    # если сессия есть - меняем цвет, ставим флаг "забанен", пишем в лог
    await chat_link.topic.set_color('black')
    chat_link.topic.banned = True
    await ChatLinksHandler.backup()

    # логирование информации о бане абонента
    await bot_topic.log(
        BANNING_LOG.format(
            name=message_dto.sender_name,
            topic=chat_link.topic.name
    ))
