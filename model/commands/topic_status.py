from controller import MessageDTO
from model.commands.utils import try_get_chat_link


# обрабатывает сбор информации о топике
async def handle_status_command(message_dto: MessageDTO):

    # пытаемся достать сессию (линк) чатов
    chat_link = await try_get_chat_link(message_dto.chat_id)

    # преобразуем инфу линка в слвоварь, красиво собираем
    status_info = ""
    for key, elem in chat_link.to_dict().items():
        status_info += f"{key}:\n{elem}\n\n"

    message_dto.text = status_info.strip()
    await chat_link.topic.send(message_dto)
