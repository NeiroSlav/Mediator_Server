from structures import ChatLinksHandler
from controller import MessageDTO, bot_topic


# обрабатывает сбор информации о топике
async def handle_topic_status(message_dto: MessageDTO):

    # пытаемся достать сессию (линк) чатов
    topic_id = message_dto.chat_id
    chat_link = ChatLinksHandler.get_by_topic_id(topic_id)

    # если её нет - удаляем сам топик
    if not chat_link:
        await bot_topic.delete(topic_id)
        return

    # преобразуем инфу линка в слвоварь, красиво собираем
    status_info = ''
    for key, elem in chat_link.to_dict().items():
        status_info += f"{key}:\n{elem}\n\n"

    message_dto.text = status_info.strip()
    await chat_link.topic.send(message_dto)
