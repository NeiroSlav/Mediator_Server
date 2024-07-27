from structures import ChatLinksHandler
from controller import MessageDTO, bot_topic
from const import ABON_GOT_TEXT, BROADCAST_LOG


async def handle_broadcast_message(message_dto: MessageDTO):

    # убирает префикс /broadcast
    message_dto.text = message_dto.text.replace('/broadcast', '').strip()
    if not message_dto.text:  # если в сообщение не было текста
        return
    
    notification = MessageDTO.new(  # создаётся сообщение для топика, 
        ABON_GOT_TEXT.format(       # о том, что абонент получил сообщение
            text=message_dto.text
    ))

    # перебирает все линки
    all_chat_links = ChatLinksHandler.get_all_links()
    for chat_link in all_chat_links:

        # если топик отвеченный, или закрытый, или забаненный - его не трогает
        if chat_link.topic.answered or chat_link.topic.closed or chat_link.topic.banned:
            continue

        await chat_link.abon_chat.send(message_dto)  # отправляет сообщение абону
        await chat_link.topic.send(notification)     # отправляет инфу в топик
        await chat_link.topic.set_color('yellow')    # меняет цвет топика

    await bot_topic.log(  # логгирует информацию о команде бродкаста
        BROADCAST_LOG.format(
            name=message_dto.sender_name,
            text=message_dto.text
    ))
