from pprint import pprint
from controller import bot_topic, MessageDTO
from const import SOCIAL_COLORS, STATE_COLORS
from controller import Backuper
from structures.link.chats.topic_utils import TopicMeta


# класс работы с топиком
# любые действия с топиком через него
class GroupTopic:
    meta: TopicMeta
    state: str
    name: str
    id: int

    # фабричный метод восстановления из бекапа
    @classmethod
    def restore(cls, **kwargs):
        self = cls()
        self.state = kwargs.get("state")
        self.name = kwargs.get("topic_name")
        self.id = kwargs.get("topic_id")
        self.meta = TopicMeta(self.name)
        return self

    # фабричный метод создания объекта
    @classmethod
    async def create(cls, name: str, social: str):
        self = cls()
        self.name = str(name)
        self.meta = TopicMeta(self.name)
        self.state = "opened"
        self.id = await bot_topic.create(
            name=self.meta.new_sign(self.state),
            image_color=SOCIAL_COLORS[social],
        )
        self.meta.set_start()
        return self

    # отправка сообщения в топик
    async def send(self, message_dto: MessageDTO):
        message_dto.chat_id = self.id
        await bot_topic.send(message_dto)

    # смена юзера и цвета перед именем топика
    async def update_sign(self):
        new_sign = self.meta.new_sign(self.state)
        if new_sign:
            await bot_topic.set_name(topic_id=self.id, name=new_sign)

    # закрытие топика
    async def close(self):
        self.state = "closed"
        self.meta.set_finish()
        await self.meta.backup_stats()
        self.meta.reset()
        try:
            await self.update_sign()
            # await bot_topic.close(topic_id=self.id)
        except:
            pass
        await self._backup()

    # открытие топика
    async def reopen(self):
        self.state = "opened"
        self.meta.set_start()
        await self.update_sign()
        await bot_topic.reopen(topic_id=self.id)
        await self._backup()

    # бан топика
    async def ban(self):
        self.state = "banned"
        self.meta.reset()
        await self.update_sign()
        await self._backup()

    # бан топика
    async def answer(self, user: str):
        self.state = "answered"
        self.meta.set_answer()
        self.meta.user = user
        await self.update_sign()
        await self._backup()

    # бекап состояния в базу
    async def _backup(self):
        await Backuper.update_state(topic_id=self.id, new_state=self.state)
