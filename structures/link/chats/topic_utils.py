from const import STATE_COLORS
import emoji
from datetime import datetime, time, timedelta
from controller import Statist


# класс для всей сторонней
# информации о топике
class TopicMeta:

    def __init__(self, name: str):
        self.name = name
        self.sign = ""
        self.user = "nobody"
        self.hold = False
        self._start_time = None
        self._answer_time = None
        self._finish_time = None
        self.active = False

    def reset(self):
        self.user = "nobody"
        self.hold = False
        self._start_time = None
        self._answer_time = None
        self._finish_time = None
        self.active = False

    # установка стартового времени,
    def set_start(self):
        self.active = True
        if not self._start_time:
            self._start_time = datetime.now()

    # времени ответа
    def set_answer(self):
        if not self._answer_time:
            self._answer_time = datetime.now()

    # времени закрытия топика
    def set_close(self):
        self._finish_time = datetime.now()
        if not self._answer_time:
            self._answer_time = self._finish_time

    # преобразует данные, пихает в базу статистики
    async def backup_and_reset(self):
        if not self.active:
            return
        try:
            stats = {
                "date": self._start_time.date(),
                "start_time": self._start_time.time().replace(microsecond=0),
                "answer_rate": delta_to_time(self._answer_time - self._start_time),
                "finish_rate": delta_to_time(self._finish_time - self._start_time),
                "user": self.user,
            }
            await Statist.add(**stats)
        except Exception:
            pass
        self.reset()

    # создаёт новое название (саму подпись) топика
    def new_sign(self, state: str) -> str | None:
        last_sign = self.sign

        color_emoji = get_color(STATE_COLORS[state])
        if state == "answered":
            self.sign = f"{color_emoji} [{self.user}] {self.name}"
        else:
            self.sign = f"{color_emoji} {self.name}"

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


# преобразует объект timedelta в time
def delta_to_time(timedelta: timedelta) -> time:
    # получение часов, минут и секунд
    total_seconds = timedelta.total_seconds()
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    # создание объекта time
    return time(int(hours), int(minutes), int(seconds))
