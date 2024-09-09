from structures import ChatLinksHandler, ChatLink
from controller import MessageDTO, bot_topic
from const import CREATING_LOG
from model.messages.utils import greet_abon, try_schedule_close


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
            name=message_dto.sender_name,
        )
        await ChatLinksHandler.add(chat_link)
        await bot_topic.log(
            CREATING_LOG.format(
                topic=chat_link.topic.name,
                social=message_dto.social,
            )
        )
        greeting_flag = True

    # если абонент забанен
    elif chat_link.topic.state == "banned":
        return

    # если абонент когда-то обращался, но топик уже закрыт
    elif chat_link.topic.state == "closed":

        # и если мета топика неактивна (т.е. абонент обращался давно)
        if not chat_link.topic.meta.active:
            greeting_flag = True
        await chat_link.topic.reopen()

    # пересылка сообщения абонента в топик
    message_dto.chat_id = chat_link.topic.id
    await chat_link.topic.send(message_dto)
    if greeting_flag:
        await greet_abon(chat_link)

    await try_schedule_close(chat_link)
