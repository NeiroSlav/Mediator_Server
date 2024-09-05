import asyncio
from structures import GroupTopic
from const import AUTO_CLOSE_TIME


class Sсheduler:
    closing_topic_timers = {}  # cловарь для хранения таймеров по идентификатору топика

    # планируем выполнение асинхронной задачи через время
    @staticmethod
    def _set_event(event: callable, delay: int):
        async def delayed_task():
            await asyncio.sleep(delay)
            await event()

        # Возвращаем саму задачу, чтобы можно было её отменить позже
        return asyncio.create_task(delayed_task())

    # планируем закрытие топика через время
    @classmethod
    async def sсhedule_topic_close(cls, topic: GroupTopic, delay=AUTO_CLOSE_TIME):
        cls.cancel_topic_close(topic)
        cls.closing_topic_timers[topic.id] = cls._set_event(topic.close, delay)

    # отмена таймера для этого топика, если есть
    @classmethod
    def cancel_topic_close(cls, topic: GroupTopic):
        if topic.id in cls.closing_topic_timers:
            try:
                cls.closing_topic_timers[topic.id].cancel()
            except RuntimeWarning:
                pass
