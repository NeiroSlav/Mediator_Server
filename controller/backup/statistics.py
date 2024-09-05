from controller.backup.init import database, dialogs
from const import NEED_BACKUP
from sqlalchemy import func, select
from datetime import time, date


class Statist:

    # добавление новой записи в базу
    @staticmethod
    async def add(
        date: date,
        start_time: time,
        answer_rate: time,
        finish_rate: time,
        user: str,
    ):
        if not NEED_BACKUP:
            return

        await database.connect()
        query = dialogs.insert().values(
            date=date,
            start_time=start_time,
            answer_rate=answer_rate,
            finish_rate=finish_rate,
            user=user,
        )
        await database.execute(query)
        await database.disconnect()

    # получение количества записей в таблице
    async def count() -> int:
        if not NEED_BACKUP:
            return 0

        await database.connect()

        # Правильный запрос на получение количества записей
        query = select(func.count()).select_from(dialogs)
        count_result = await database.fetch_one(query)

        await database.disconnect()

        # Извлекаем количество из результата
        return count_result[0] if count_result else 0
