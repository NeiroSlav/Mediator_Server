from controller import MessageDTO, bot_topic, aliaser
from const import SUFFIX_COMMAND_TEXT, BROADCAST_ID, SUFFIX_STATE, SUFFIX_ALIAS_NAME
from model.commands.utils import strip_arguments


# обрабатывает команду /suffix
async def handle_suffix_command(message_dto: MessageDTO):

    argument = strip_arguments(message_dto.text)

    if argument == "enable":
        SUFFIX_STATE["enabled"] = True

    elif argument == "disable":
        SUFFIX_STATE["enabled"] = False

    elif argument:
        aliaser.set(SUFFIX_ALIAS_NAME, argument)

    # формирует текст ответа на команду /suffix
    text = SUFFIX_COMMAND_TEXT.format(
        status=SUFFIX_STATE["enabled"], text=aliaser.get(SUFFIX_ALIAS_NAME)
    )
    # отправляет в чат ответ на команду
    return await bot_topic.send(
        message_dto=MessageDTO.new(text=text, chat_id=BROADCAST_ID)
    )
