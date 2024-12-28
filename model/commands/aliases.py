from controller import MessageDTO, bot_topic, aliaser
from const import ALIAS_TEXT_ERROR, ALIAS_SEARCH_ERROR, COMMAND_ERROR
from controller import MessageDTO, bot_topic
from model.commands.utils import strip_arguments


async def handle_controll_aliases(message_dto: MessageDTO):

    # убирает из команды /alias или /alias@bot_name
    argument = strip_arguments(message_dto.text)
    argument = argument.replace("set", "set ")  # на случай "set\n"

    # если нет никаких аргументов, выдаст список всех алиасов
    if not argument:
        message_dto.text = "\n".join(aliaser.get_all())
        return await bot_topic.send(message_dto)

    # режет команду на аргументы, достаёт имя алиаса
    alias_command = argument.split(" ")
    alias_name = alias_command.pop(0).strip()

    # если кроме алиаса в команде ничего не указано
    # достаёт алиас по имени, отправляет его текст
    # а если такого имени нет, отписывает ошибку
    if not alias_command:
        message_dto.text = aliaser.get(alias_name)
        if not message_dto.text:
            message_dto.text = ALIAS_SEARCH_ERROR.format(alias=alias_name)
        return await bot_topic.send(message_dto)

    # дотаёт действие и текст алиаса, если есть
    alias_action = alias_command.pop(0)
    alias_text = " ".join(alias_command).strip(" \n")

    # print(alias_name, alias_action, alias_text, sep="\n-\n")

    # если действие - удалить
    if alias_action == "del":
        aliaser.delete(alias_name)
        message_dto.text = f"- ${alias_name}"
        return await bot_topic.send(message_dto)

    # если действие - установить, но текст
    # далее не перенад, сообщит сотруднику об ошибке.
    # если текст передан - установит связку алиаса
    elif alias_action == "set":
        if not alias_text:
            message_dto.text = ALIAS_TEXT_ERROR
            return await bot_topic.send(message_dto)

        aliaser.set(alias_name, alias_text)
        message_dto.text = f"+ ${alias_name}"
        return await bot_topic.send(message_dto)

    # если ни одна из команд не подошла - сообщит об ошибке.
    message_dto.text = COMMAND_ERROR
    return await bot_topic.send(message_dto)
