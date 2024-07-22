BOT_TOKEN: str

BOT_ID: int
GROUP_ID: int
BROADCAST_ID: int  # id топика для бродкаста. Установить 0, если не нужен

# порт api сервера медиатора
SERVER_PORT = 5010

# порты api клиентов медиатора
CLIENT_PORTS = {
    'tg': 5011,
    'vk': 5012,
}

GREETING_TEXT = 'Приветствуем! Мы ответим Вам при первой возможности.'

ABON_GOT_TEXT = 'Абоненту отправлено сообщение:\n\n{text}'

BACKUP = False

# цвета иконок при создании топика
COLORS = {
    'magenta': 13338331,
    'yellow': 16766590,
    'green': 9367192,
    'pink': 16749490,
    'blue': 7322096,
    'red': 16478047,
}

# соответствия цветов соц.сетям
SOCIAL_COLORS = {
    'tg': COLORS['magenta'],
    'vk': COLORS['blue'],
}
