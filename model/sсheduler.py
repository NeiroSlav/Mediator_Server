import asyncio
from structures import ChatLink
from const import AUTO_CLOSE_TIME


class Sсheduler:
    closing_dialog_timers = {}  # cловарь для хранения таймеров по идентификатору топика

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
    async def sсhedule_dialog_close(cls, chat: ChatLink, delay=AUTO_CLOSE_TIME):
        cls.cancel_dialog_close(chat)
        cls.closing_dialog_timers[chat.topic.id] = cls._set_event(
            event=chat.say_goodbye, delay=delay
        )

    # отмена таймера для этого топика, если есть
    @classmethod
    def cancel_dialog_close(cls, chat: ChatLink):
        try:
            cls.closing_dialog_timers[chat.topic.id].cancel()
        except (RuntimeWarning, KeyError):
            pass
