from structures import ChatLinksHandler
from controller import MessageDTO, bot_topic
from const import HOLDING_LOG
from model.scheduler import Scheduler
from model.commands.utils import try_get_chat_link


# обрабатывает удержание топика от закрытия
async def handle_hold_command(message_dto: MessageDTO):

    # пытаемся достать сессию (линк) чатов
    chat_link = await try_get_chat_link(message_dto.chat_id)

    # логирование информации об удержании топика
    await bot_topic.log(
        HOLDING_LOG.format(name=message_dto.sender_name, topic=chat_link.topic.name)
    )

    # отменяет закрытие топика (если оно было)
    Scheduler.cancel_dialog_close(chat_link)
    Scheduler.cancel_dialog_finish(chat_link)
    chat_link.topic.meta.hold = True
