from bot_config import BOT_TOKEN, BOT_ID, GROUP_ID, BROADCAST_ID

# порт api сервера медиатора
SERVER_PORT = 5010

# порты api клиентов медиатора
CLIENT_PORTS = {
    "tg": 5011,
    "vk": 5012,
    "helper": 5009,
}

# если нужны бекапы, и восстановление, то True
NEED_BACKUP = True

# время после сообщения, через которое топик закроется
AUTO_CLOSE_TIME = 1800  # если закрытие не нужно - 0

# текстовики
GREETING_TEXT = "Приветствуем! Задайте, пожалуйста, Ваш  вопрос и укажите лицевой счет или адрес Вашего подключения. Мы ответим при первой возможности."
GOODBYE_TEXT = "Спасибо за обращение, всего доброго!"
ABON_GOT_TEXT = "Абоненту отправлено сообщение:\n---\n{text}"
SUFFIX_COMMAND_TEXT = "Режим: {status}\n---\nСообщение:\n---\n{text}"

CREATING_LOG = 'Топик "{topic}" (#{social}) создан'
CLOSING_LOG = '{name} закрыл топик "{topic}"'
HOLDING_LOG = '{name} удержал топик "{topic}"'
BANNING_LOG = '{name} забанил абонента "{topic}"'
UNBANNING_LOG = '{name} разбанил абонента "{topic}"'
BROADCAST_LOG = "{name}\n---\nвсем ожидающим:\n---\n{text}"
POST_ERROR_LOG = "Mediator_{social} помер (или притворяется):\n---\n{error}"

ABON_BAN_TEXT = """
Уважаемый абонент! В данный момент для Вас заблокирована возможность писать сообщения. Обратитесь пожалуйста в нашу службу технической поддержки:

206 - для абонентов-физических лиц
207 - для корпоративных абонентов
"""

COMMENT_SYMBOL = "/"
ALIAS_SYMBOL = "$"
ALIAS_TEXT_ERROR = f'Вы не ввели шаблонный текст после "del"'
ALIAS_SEARCH_ERROR = "Не удалось найти alias ${alias}"
COMMAND_ERROR = "Неизвестная команда"


# цвета иконок при создании топика
ICON_COLORS = {
    "magenta": 13338331,
    "yellow": 16766590,
    "green": 9367192,
    "pink": 16749490,
    "blue": 7322096,
    "red": 16478047,
}

# соответствия цветов соц.сетям
SOCIAL_COLORS = {
    "tg": ICON_COLORS["magenta"],
    "vk": ICON_COLORS["blue"],
}

# глобальное состояние суффикса
SUFFIX_STATE = {"enabled": False}
NEIRO_STATE = {"enabled": True}
SUFFIX_ALIAS_NAME = "suffix"

# литералы состояний топиков
OPENED = "opened"
ANSWERED = "answered"
CLOSED = "closed"
BANNED = "banned"

# цвета в названиях топиков
STATE_COLORS = {
    CLOSED: "red",
    ANSWERED: "yellow",
    OPENED: "green",
    BANNED: "black",
}
