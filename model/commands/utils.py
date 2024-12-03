import re
from structures import ChatLinksHandler, ChatLink
from controller import bot_topic


# пытаемся достать сессию (линк) чатов
async def try_get_chat_link(topic_id: int) -> ChatLink | None:
    chat_link = ChatLinksHandler.get_by_topic_id(topic_id)

    if chat_link:
        return chat_link

    # если её нет - удаляем сам топик
    await bot_topic.delete(topic_id)

    # эта ошибка поймается на слое контроллера
    raise PermissionError


# убирает префикс /command или /command@botname
def strip_arguments(text: str) -> str:
    pattern = r"/[A-z0-9_\-@]+"
    founded = re.search(pattern, text)

    if not founded:
        return text

    command = founded.group()
    text = text.replace(command, "")
    return text.strip()
