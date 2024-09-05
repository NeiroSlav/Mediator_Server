from structures import ChatLinksHandler
from controller import MessageDTO, bot_topic
from const import GREETING_TEXT, SUFFIX_COMMAND_TEXT, BROADCAST_ID


# текст после приветствия абонента
suffix = {"enabled": False, "text": "тестовое сообщение ивр"}


# обрабатывает команду /suffix
async def handle_suffix_command(message_dto: MessageDTO):

    # убирает префикс /suffix или /suffix@botname
    argument = message_dto.text.split(" ")
    if len(argument) > 1:
        argument = " ".join(argument[1:]).strip()
    else:
        argument = ""

    if argument == "enable":
        suffix["enabled"] = True

    elif argument == "disable":
        suffix["enabled"] = False

    elif argument:
        suffix["text"] = argument

    # формирует текст ответа на команду /suffix
    text = SUFFIX_COMMAND_TEXT.format(status=suffix["enabled"], text=suffix["text"])
    # отправляет в чат ответ на команду
    return await bot_topic.send(
        message_dto=MessageDTO.new(text=text, chat_id=BROADCAST_ID)
    )
