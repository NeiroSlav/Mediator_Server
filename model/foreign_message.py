from structures import ChatLinksHandler, ChatLink
from controller import MessageDTO, bot_topic
from const import GREETING_TEXT, ABON_GOT_TEXT


async def handle_foreign_message(message_dto: MessageDTO):

    # пытаемся достать сессию (линк) чатов
    abon_chat_id = message_dto.chat_id
    chat_link = ChatLinksHandler.get_by_abon_id(abon_chat_id)
    
    # если абонент обращается в первый раз
    if not chat_link:
        chat_link = await ChatLink.create(
            social=message_dto.social,
            chat_id=abon_chat_id,
            name=message_dto.sender_name
        )
        await ChatLinksHandler.add(chat_link)
        await bot_topic.log(f'Топик "{chat_link.topic.name}" создан')
        await ChatLinksHandler.backup()
        await greet_abon(chat_link)

    # если абонент когда-то обращался, но топик уже закрыт
    elif chat_link.topic.closed:
        await chat_link.topic.reopen()
        await ChatLinksHandler.backup()
        await greet_abon(chat_link)
        await chat_link.topic.set_color('green')

    # пересылка сообщения абонента в топик
    message_dto.chat_id = chat_link.topic.id
    await chat_link.topic.send(message_dto)


# приветствие абонента
async def greet_abon(chat_link: ChatLink):
    message_dot = MessageDTO.new(GREETING_TEXT)
    notification = MessageDTO.new(ABON_GOT_TEXT.format(text=GREETING_TEXT))

    await chat_link.abon_chat.send(message_dot)  # отправка абону приветственного текста
    await chat_link.topic.send(notification)     # отправка в топик информации о приветствии
