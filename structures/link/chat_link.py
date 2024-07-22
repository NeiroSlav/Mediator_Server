from pprint import pprint

from structures.link.chats.abonchat import AbonChat
from structures.link.chats.topic import GroupTopic


# класс связи лички абонента и топика группы
class ChatLink:
    abon_chat: AbonChat
    topic: GroupTopic
    answered: bool

    # фабричный метод загрузки для загрузки данных из бекапа
    @classmethod
    def restore(cls, abon_chat: dict, topic: dict):
        self = cls()
        self.abon_chat = AbonChat.restore(**abon_chat)
        self.topic = GroupTopic.restore(**topic)
        return self

    # фабричный метод создания объекта класса
    @classmethod
    async def create(cls, social: str, chat_id: int, name: str):
        self = cls()
        self.abon_chat = AbonChat(social, chat_id)
        self.topic = await GroupTopic.create(name, social)
        self.answered = False
        return self

    def __str__(self) -> str:
        return f'  чат: {self.abon_chat.id}\nтопик: {self.topic.id}'

    def to_dict(self) -> dict:
        return {
            'abon_chat': self.abon_chat.__dict__,
            'topic': self.topic.__dict__,
        }
