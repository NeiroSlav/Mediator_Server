from structures import ChatLinksHandler
from controller import MessageDTO, bot_topic
from const import BROADCAST_LOG, OPENED
from model.scheduler import Scheduler
from model.commands.utils import strip_arguments
import asyncio


# обрабатывает широковещательное сообщение
async def handle_broadcast_command(message_dto: MessageDTO):

    argument = strip_arguments(message_dto.text)
    if not argument:  # если в сообщение не было текста
        return
    message_dto.text = argument

    # перебирает все линки
    all_chat_links = ChatLinksHandler.get_all_links()
    for chat_link in all_chat_links:

        # если топик отвеченный, или закрытый, или забаненный - его не трогает
        if chat_link.topic.state != OPENED:
            continue

        await asyncio.sleep(1)
        await chat_link.abon_chat.send(message_dto)  # отправляет сообщение абону
        await chat_link.topic.notify(message_dto.text)  # отправляет инфу в топик
        await chat_link.topic.answer("broad")  # меняет состояние топика

        # планирует закрытие топика
        Scheduler.sch_dialog_close(chat_link)

    await bot_topic.log(  # логгирует информацию о команде бродкаста
        BROADCAST_LOG.format(name=message_dto.sender_name, text=message_dto.text)
    )
