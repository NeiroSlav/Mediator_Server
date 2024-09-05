from const import STATE_COLORS
import emoji
from datetime import datetime, time, timedelta
from time import sleep
from controller import Statist
from pprint import pprint


# класс для всей сторонней
# информации о топике
class TopicMeta:

    def __init__(self, name: str):
        self.name = name
        self.sign = ""
        self.user = None
        self.hold = False
        self.start_time = None
        self.answer_time = None
        self.finish_time = None
        self.backuped = False

    def reset(self):
        self.user = None
        self.hold = False
        self.start_time = None
        self.answer_time = None
        self.finish_time = None
        self.backuped = False

    def set_start(self):
        print("\nStarted")
        self.start_time = datetime.now()

    def set_answer(self):
        self.answer_time = datetime.now()

    def set_finish(self):
        self.finish_time = datetime.now()
        if not self.answer_time:
            self.answer_time = self.finish_time
        if not self.user:
            self.user = "nobody"

    # преобразует данные, пихает в базу статистики
    async def backup_stats(self):
        if self.backuped:
            return
        try:
            stats = {
                "date": self.start_time.date(),
                "start_time": self.start_time.time().replace(microsecond=0),
                "answer_rate": delta_to_time(self.answer_time - self.start_time),
                "finish_rate": delta_to_time(self.finish_time - self.start_time),
                "user": self.user,
            }
            await Statist.add(**stats)
        except Exception:
            pass
        self.backuped = True

    # создаёт новое название (саму подпись) топика
    def new_sign(self, state: str) -> str | None:
        last_sign = self.sign

        color = get_color(STATE_COLORS[state])
        self.sign = f"{color} {self.name}"
        if self.user:
            self.sign = f"{self.user} {self.sign}"

        # если запись изменилась, то вернёт новую
        if self.sign != last_sign:
            return self.sign


# возвращает кружок нужного цвета
def get_color(color: str):
    try:
        e = emoji.emojize(f":{color}_circle:")
        if not emoji.is_emoji(e):
            raise KeyError
        return e
    except KeyError:  # если такого цвета нет, вернёт клоуна
        return emoji.emojize(":clown_face:")


def delta_to_time(timedelta: timedelta) -> time:
    # получение часов, минут и секунд
    total_seconds = timedelta.total_seconds()
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    # создание объекта time
    return time(int(hours), int(minutes), int(seconds))
