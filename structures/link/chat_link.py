from pprint import pprint

from structures.link.chats.abonchat import AbonChat
from structures.link.chats.topic import GroupTopic
from const import GOODBYE_TEXT
from controller import Backuper, MessageDTO


# класс связи лички абонента и топика группы
class ChatLink:
    abon_chat: AbonChat
    topic: GroupTopic

    # фабричный метод загрузки для загрузки данных из бекапа
    @classmethod
    def restore(cls, data):
        self = cls()
        self.abon_chat = AbonChat.restore(**data)
        self.topic = GroupTopic.restore(**data)
        return self

    # фабричный метод создания объекта класса
    @classmethod
    async def create(cls, social: str, chat_id: int, name: str):
        self = cls()
        self.abon_chat = AbonChat(social, chat_id)
        self.topic = await GroupTopic.create(name, social)
        await Backuper.add(
            topic_id=self.topic.id,
            topic_name=self.topic.name,
            state=self.topic.state,
            abon_id=self.abon_chat.id,
            social=self.abon_chat.social,
        )
        return self

    # прощание с абонентом, если топик "отвеченный", закрытие
    async def say_goodbye(self):
        # if self.topic.state == "answered":
        #     await self.abon_chat.send(MessageDTO.new(GOODBYE_TEXT))
        await self.topic.close()

    async def finish(self):
        await self.topic.finish()

    def __str__(self) -> str:
        return f"  чат: {self.abon_chat.id}\nтопик: {self.topic.id}"

    def to_dict(self) -> dict:
        return {
            "abon_chat": self.abon_chat.__dict__,
            "topic": self.topic.__dict__,
        }
