from structures import ChatLinksHandler
from controller import MessageDTO, bot_topic
from const import UNBANNING_LOG


# обрабатывает разбан абонента
async def handle_topic_unban(message_dto: MessageDTO):

    # пытаемся достать сессию (линк) чатов
    topic_id = message_dto.chat_id
    chat_link = ChatLinksHandler.get_by_topic_id(topic_id)

    # если её нет - удаляем сам топик
    if not chat_link:
        await bot_topic.delete(topic_id)
        return

    if not chat_link.topic.state == "banned":
        raise PermissionError

    # если сессия есть - закрываем топик, пишем в лог
    await chat_link.topic.close()

    # логирование информации о бане абонента
    await bot_topic.log(
        UNBANNING_LOG.format(name=message_dto.sender_name, topic=chat_link.topic.name)
    )
