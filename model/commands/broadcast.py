from structures import ChatLinksHandler
from controller import MessageDTO, bot_topic
from const import ABON_GOT_TEXT, BROADCAST_LOG
from model.sсheduler import Sсheduler
from model.commands.utils import strip_arguments
import asyncio


# обрабатывает широковещательное сообщение
async def handle_broadcast_command(message_dto: MessageDTO):

    argument = strip_arguments(message_dto.text)
    if not argument:  # если в сообщение не было текста
        return

    notification = MessageDTO.new(  # создаётся сообщение для топика,
        ABON_GOT_TEXT.format(text=argument)  # о том, что абонент получил сообщение
    )

    # перебирает все линки
    all_chat_links = ChatLinksHandler.get_all_links()
    for chat_link in all_chat_links:

        # если топик отвеченный, или закрытый, или забаненный - его не трогает
        if chat_link.topic.state != "opened":
            continue

        await asyncio.sleep(1)
        await chat_link.abon_chat.send(message_dto)  # отправляет сообщение абону
        await chat_link.topic.send(notification)  # отправляет инфу в топик
        await chat_link.topic.answer("broad")  # меняет состояние топика

        # планирует закрытие топика
        await Sсheduler.sсhedule_dialog_close(chat_link)

    await bot_topic.log(  # логгирует информацию о команде бродкаста
        BROADCAST_LOG.format(name=message_dto.sender_name, text=message_dto.text)
    )
