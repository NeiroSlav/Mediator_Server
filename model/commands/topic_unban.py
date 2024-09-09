from controller import MessageDTO, bot_topic
from const import UNBANNING_LOG
from model.commands.utils import try_get_chat_link


# обрабатывает разбан абонента
async def handle_unban_command(message_dto: MessageDTO):

    # пытаемся достать сессию (линк) чатов
    chat_link = await try_get_chat_link(message_dto.chat_id)

    # если топик и не забанин
    if not chat_link.topic.state == "banned":
        return

    # если сессия есть - закрываем топик, пишем в лог
    await chat_link.topic.close()

    # логирование информации о бане абонента
    await bot_topic.log(
        UNBANNING_LOG.format(name=message_dto.sender_name, topic=chat_link.topic.name)
    )
