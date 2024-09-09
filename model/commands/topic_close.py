from controller import MessageDTO, bot_topic
from const import CLOSING_LOG, AUTO_CLOSE_TIME
from model.sсheduler import Sсheduler
from model.commands.utils import try_get_chat_link


# обрабатывает закрытие топика
async def handle_close_command(message_dto: MessageDTO):

    # пытаемся достать сессию (линк) чатов
    chat_link = await try_get_chat_link(message_dto.chat_id)

    # отменяет закрытие топика (если оно было)
    Sсheduler.cancel_dialog_close(chat_link)

    # прощаемся с абонентом, бекапим
    await chat_link.say_goodbye()
    await Sсheduler.sсhedule_dialog_close(
        chat_link, need_close=False, finishing_delay=AUTO_CLOSE_TIME
    )

    # логирование информации о закрытии топика
    await bot_topic.log(
        CLOSING_LOG.format(name=message_dto.sender_name, topic=chat_link.topic.name)
    )
