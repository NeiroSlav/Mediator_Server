from controller.backup.init import database, abonents
from const import NEED_BACKUP


class Backuper:

    # добавление новой записи в базу
    @staticmethod
    async def add(
        topic_id: int, topic_name: str, state: str, abon_id: int, social: str
    ):
        if not NEED_BACKUP:
            return

        await database.connect()
        query = abonents.insert().values(
            topic_id=topic_id,
            topic_name=topic_name,
            state=state,
            abon_id=abon_id,
            social=social,
        )
        await database.execute(query)
        await database.disconnect()

    # обновление состояния топика в базе
    @staticmethod
    async def update_state(topic_id: int, new_state: str):
        if not NEED_BACKUP:
            return

        await database.connect()
        query = (
            abonents.update()
            .where(abonents.c.topic_id == topic_id)
            .values(state=new_state)
        )
        await database.execute(query)
        await database.disconnect()

    # вытягивание всех чатов
    @staticmethod
    async def fetch_all() -> list[dict]:
        if not NEED_BACKUP:
            return []

        await database.connect()
        query = abonents.select()
        results = await database.fetch_all(query)
        await database.disconnect()
        return [dict(result) for result in results]
