from controller import MessageDTO
from structures import ChatLinksHandler, ChatLink
from controller import MessageDTO


async def redirect_helper_message(message_dto: MessageDTO):

    # пытаемся достать сессию (линк) чатов
    chat_link: ChatLink = ChatLinksHandler.get_by_topic_id(
        message_dto.chat_id,
    )
    await chat_link.abon_chat.send(message_dto)
