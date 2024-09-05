from const import STATE_COLORS
import emoji


class TopicMeta:

    def __init__(self, name):
        self.sign = ""
        self.user = None
        self.hold = False
        self.start_time = None
        self.finish_time = None

    def reset(self):
        self.user = None
        self.hold = False
        self.start_time = None
        self.finish_time = None

    def set_hold(self):
        self.hold = True

    def set_user(self, user: str):
        if self.user != user:
            self.user = user
            return True
        return False

    def new_sign(self, name: str, state: str) -> str:
        color = get_color(STATE_COLORS[state])
        self.sign = f"{color} {name}"
        if self.user:
            self.sign = f"{self.user} {self.sign}"
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
