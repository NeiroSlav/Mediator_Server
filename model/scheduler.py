import asyncio
from structures import ChatLink
from const import AUTO_CLOSE_TIME


class Scheduler:
    # cловарь для хранения таймеров по идентификатору топика
    closing_timers: dict[int, asyncio.Task] = {}
    # а этот хранит таймеры полного окончания диалога и бекапа
    finishing_timers: dict[int, asyncio.Task] = {}

    # планируем что-либо через время
    @classmethod
    def abstract_schedule(cls, task_dict, id: int, event: callable, delay: int):
        async def delayed_task():
            await asyncio.sleep(delay)
            await event()

        cls._abstract_cancel(task_dict, id)
        task_dict[id] = asyncio.create_task(delayed_task())

    @classmethod
    def _abstract_cancel(cls, task_dict, id):
        if id in task_dict:
            task_dict[id].cancel()

    # планируем закрытие топика через время
    @classmethod
    def sch_dialog_close(cls, chat_link: ChatLink, delay=AUTO_CLOSE_TIME):
        cls.abstract_schedule(
            cls.closing_timers, chat_link.topic.id, chat_link.say_goodbye, delay
        )

    # планируем бекап топика через время
    @classmethod
    def sch_dialog_finish(cls, chat_link: ChatLink, delay=AUTO_CLOSE_TIME * 2):
        cls.abstract_schedule(
            cls.finishing_timers, chat_link.topic.id, chat_link.finish, delay
        )

    @classmethod
    def cancel_dialog_close(cls, chat_link: ChatLink):
        cls._abstract_cancel(cls.closing_timers, chat_link.topic.id)

    @classmethod
    def cancel_dialog_finish(cls, chat_link: ChatLink):
        cls._abstract_cancel(cls.finishing_timers, chat_link.topic.id)
