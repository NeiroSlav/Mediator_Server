from pprint import pprint
from controller import bot_topic, MessageDTO
from const import SOCIAL_COLORS
from structures.utils import get_color


# класс работы с топиком
class GroupTopic:
    answered: bool
    closed: bool
    color: str
    name: str
    id: int

    # фабричный метод восстановления из бекапа
    @classmethod
    def restore(cls, **kwargs):
        self = cls()
        self.answered = kwargs.get('answered')
        self.closed = kwargs.get('closed')
        self.color = kwargs.get('color')
        self.name = kwargs.get('name')
        self.id = kwargs.get('id')
        return self

    # фабричный метод создания объекта
    @classmethod
    async def create(cls, name: str, social: str):
        id = await bot_topic.create(
            f'{get_color("green")} {name}',
            image_color=SOCIAL_COLORS[social],
        )
        self = cls()
        self.answered = False
        self.closed = False
        self.color = 'green'
        self.name = str(name)
        self.id = id
        return self

    # отправка сообщения в топик
    async def send(self, message_dto: MessageDTO):
        message_dto.chat_id = self.id
        await bot_topic.send(message_dto)

    # смена цвета перед именем топика
    async def set_color(self, color: str):
        if self.color == color:
            return
        self.color = color

        await bot_topic.set_name(
            topic_id=self.id,
            name=f'{get_color(color)} {self.name}',
        )        

    # закрытие топика
    async def close(self):
        self.closed = True
        await bot_topic.close(topic_id=self.id)

    # открытие топика
    async def reopen(self):
        self.closed = False
        await bot_topic.reopen(topic_id=self.id)
