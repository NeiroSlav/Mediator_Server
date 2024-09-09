from pprint import pprint
from controller import bot_topic, MessageDTO
from const import SOCIAL_COLORS, OPENED, ANSWERED, CLOSED, BANNED
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
        self.state = OPENED
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

    # окончательное финиширование
    async def finish(self):
        await self.meta.backup_and_reset()

    # закрытие топика
    async def close(self):
        self.state = CLOSED
        self.meta.set_close()
        try:
            await self.update_sign()
            # await bot_topic.close(topic_id=self.id)
        except:
            pass
        await self._backup_state()

    # открытие топика
    async def reopen(self):
        self.state = OPENED
        self.meta.set_start()
        await self.update_sign()
        await bot_topic.reopen(topic_id=self.id)
        await self._backup_state()

    # бан топика
    async def ban(self):
        self.state = BANNED
        self.meta.reset()
        await self.update_sign()
        await self._backup_state()

    # бан топика
    async def answer(self, user: str):
        self.state = ANSWERED
        self.meta.set_answer()
        self.meta.user = user
        await self.update_sign()
        await self._backup_state()

    # бекап состояния в базу
    async def _backup_state(self):
        await Backuper.update_state(topic_id=self.id, new_state=self.state)
