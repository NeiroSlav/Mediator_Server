from structures.backuper import Backuper
from structures.link.chat_link import ChatLink


# класс хранения и управления линками
class ChatLinksHandler:
    _all_chat_links: list[ChatLink] = list(map(
        lambda x: ChatLink.restore(**x), Backuper.read()
    ))

    @classmethod
    async def backup(cls):
        await Backuper.save(cls._all_chat_links[:])

    @classmethod  # добавление линка в список
    async def add(cls, link: ChatLink) -> bool:
        if link in cls._all_chat_links:
            return False
        cls._all_chat_links.append(link)
        return True

    @classmethod  # поиск линка по id абонента
    def get_by_abon_id(cls, chat_id: int) -> ChatLink | None:
        filtered = list(filter(
            lambda x: x.abon_chat.id == chat_id,
            cls._all_chat_links
        ))
        if filtered:
            return filtered[0]

    @classmethod  # поиск линка по id топика
    def get_by_topic_id(cls, topic_id: int) -> ChatLink | None:
        filtered = list(filter(
            lambda x: x.topic.id == topic_id,
            cls._all_chat_links
        ))
        if filtered:
            return filtered[0]

    @classmethod  # отдаёт копию списка всех чатов
    def get_all_links(cls) -> list[ChatLink]:
        return cls._all_chat_links[:]

