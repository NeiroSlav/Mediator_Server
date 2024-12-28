from controller import MessageDTO, bot_topic, aliaser, foreign_api
from const import NEIRO_STATE, COMMAND_ERROR, BROADCAST_ID
from model.commands.utils import strip_arguments


async def handle_neiro_command(message_dto: MessageDTO):
    argument = strip_arguments(message_dto.text)


    answer = MessageDTO.new(text=COMMAND_ERROR, chat_id=BROADCAST_ID)

    if not argument:
        answer.text = "Нейро сейчас " + "включен" if NEIRO_STATE["enabled"] else "выключен"

    elif argument == "disable":
        await foreign_api.send_clear_to_helper()
        NEIRO_STATE["enabled"] = False
        answer.text = "Нейро выключен"

    elif argument == "enable":
        NEIRO_STATE["enabled"] = True
        answer.text = "Нейро включен"

    # отправляет в чат ответ на команду
    await bot_topic.send(
        message_dto=answer
    )
