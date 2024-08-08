from structures import ChatLinksHandler, ChatLink
from controller import MessageDTO, bot_topic
from const import GREETING_TEXT, ABON_GOT_TEXT, CREATING_LOG
from model.suffix_message import suffix


# обрабатывает сообщение извне, пришедшее по http
async def handle_foreign_message(message_dto: MessageDTO):

    # пытаемся достать сессию (линк) чатов
    chat_link = ChatLinksHandler.get_by_abon_id(
        message_dto.chat_id,
        message_dto.social,
    )
    greeting_flag = False
    
    # если абонент обращается в первый раз
    if not chat_link:
        chat_link = await ChatLink.create(
            social=message_dto.social,
            chat_id=message_dto.chat_id,
            name=message_dto.sender_name
        )
        await ChatLinksHandler.add(chat_link)
        await bot_topic.log(
            CREATING_LOG.format(
                topic=chat_link.topic.name,
                social=message_dto.social,
        ))
        greeting_flag = True

    # если абонент забанен
    elif chat_link.topic.state == 'banned':
        return
    
    # если абонент когда-то обращался, но топик уже закрыт
    elif chat_link.topic.state == 'closed':
        await chat_link.topic.reopen()
        greeting_flag = True

    # пересылка сообщения абонента в топик
    message_dto.chat_id = chat_link.topic.id
    await chat_link.topic.send(message_dto)
    if greeting_flag:
        await greet_abon(chat_link)


# приветствие абонента
async def greet_abon(chat_link: ChatLink):
    text = GREETING_TEXT

    # если включен режим суфикса,
    if suffix['enabled']:  # добавляет его текст к приветствию
        text += f'\n\n{suffix["text"]}'

    # формирует приветственное сообщение абоненту
    message_dto = MessageDTO.new(text)
    notification = MessageDTO.new(
        ABON_GOT_TEXT.format(
            text=text
    ))

    await chat_link.abon_chat.send(message_dto)  # отправка абону приветственного текста
    await chat_link.topic.send(notification)     # отправка в топик информации о приветствии
