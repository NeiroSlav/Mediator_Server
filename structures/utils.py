import emoji


# возвращает кружок нужного цвета
def get_color(color: str):
    try:
        e = emoji.emojize(f':{color}_circle:')
        if not emoji.is_emoji(e):
            raise KeyError
        return e
    except KeyError:  # если такого цвета нет, вернёт клоуна
        return emoji.emojize(':clown_face:')
