import asyncio
from structures import ChatLink
from const import AUTO_CLOSE_TIME


class Sсheduler:
    # cловарь для хранения таймеров по идентификатору топика
    closing_dialog_timers: dict[int, asyncio.Task] = {}
    # а этот хранит таймеры полного окончания диалога
    finishing_dialog_timers: dict[int, asyncio.Task] = {}

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
    async def sсhedule_dialog_close(
        cls,
        chat_link: ChatLink,
        closing_delay: int = AUTO_CLOSE_TIME,
        finishing_delay: int = AUTO_CLOSE_TIME * 2,
        need_close: bool = True,
        need_finish: bool = True,
    ):
        cls.cancel_dialog_close(chat_link)
        if need_close:
            cls.closing_dialog_timers[chat_link.topic.id] = cls._set_event(
                event=chat_link.say_goodbye, delay=closing_delay
            )
        if need_finish:
            cls.finishing_dialog_timers[chat_link.topic.id] = cls._set_event(
                event=chat_link.finish, delay=finishing_delay
            )

    # отмена таймера для этого топика, если есть
    @classmethod
    def cancel_dialog_close(cls, chat_link: ChatLink):
        try:
            cls.closing_dialog_timers[chat_link.topic.id].cancel()
            cls.finishing_dialog_timers[chat_link.topic.id].cancel()
        except (RuntimeWarning, KeyError):
            pass

    # # планируем закрытие топика через время
    # @classmethod
    # async def sсhedule_dialog_finish(cls, chat: ChatLink, delay=AUTO_CLOSE_TIME):
    #     cls.cancel_dialog_finish(chat)
    #     cls.finishing_dialog_timers[chat.topic.id] = cls._set_event(
    #         event=chat.finish, delay=delay
    #     )

    # # отмена таймера для этого топика, если есть
    # @classmethod
    # def cancel_dialog_finish(cls, chat: ChatLink):
    #     try:
    #         cls.finishing_dialog_timers[chat.topic.id].cancel()
    #     except (RuntimeWarning, KeyError):
    #         pass
