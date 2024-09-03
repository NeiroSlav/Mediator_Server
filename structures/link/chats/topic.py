from pprint import pprint
from controller import bot_topic, MessageDTO
from const import SOCIAL_COLORS, STATE_COLORS
from structures.utils import get_color
from controller import Backuper


# класс работы с топиком
# любые действия с топиком через него
class GroupTopic:
    hold: bool
    state: str
    name: str
    id: int

    # фабричный метод восстановления из бекапа
    @classmethod
    def restore(cls, **kwargs):
        self = cls()
        self.hold = False
        self.state = kwargs.get('state')
        self.name = kwargs.get('topic_name')
        self.id = kwargs.get('topic_id')
        return self

    # фабричный метод создания объекта
    @classmethod
    async def create(cls, name: str, social: str):
        id = await bot_topic.create(
            f'{get_color(STATE_COLORS["opened"])} {name}',
            image_color=SOCIAL_COLORS[social],
        )
        self = cls()
        self.hold = False
        self.state = 'opened'
        self.name = str(name)
        self.id = id
        return self

    # отправка сообщения в топик
    async def send(self, message_dto: MessageDTO):
        message_dto.chat_id = self.id
        await bot_topic.send(message_dto)

    # смена цвета перед именем топика
    async def _set_color(self, color: str):
        await bot_topic.set_name(
            topic_id=self.id,
            name=f'{get_color(color)} {self.name}',
        )        

    # закрытие топика
    async def close(self):
        self.state = 'closed'
        self.hold = False
        try:
            await self._set_color(STATE_COLORS['closed'])
            await bot_topic.close(topic_id=self.id)
        except:
            pass
        await self._backup()

    # открытие топика
    async def reopen(self):
        self.state = 'opened'
        await self._set_color(STATE_COLORS['opened'])
        await bot_topic.reopen(topic_id=self.id)
        await self._backup()

    # бан топика
    async def ban(self):
        self.state = 'banned'
        await self._set_color(STATE_COLORS['banned'])
        await self._backup()

    # бан топика
    async def answer(self):
        self.state = 'answered'
        await self._set_color(STATE_COLORS['answered'])
        await self._backup()

    # бекап состояния в базу
    async def _backup(self):
        await Backuper.update_state(topic_id=self.id, new_state=self.state)
