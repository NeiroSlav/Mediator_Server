from bot_config import BOT_TOKEN, BOT_ID, GROUP_ID, BROADCAST_ID

# порт api сервера медиатора
SERVER_PORT = 5010

# порты api клиентов медиатора
CLIENT_PORTS = {
    'tg': 5011,
    'vk': 5012,
}

# если нужны бекапы, и восстановление, то True
BACKUP = False

# текстовики
GREETING_TEXT = 'Приветствуем! Мы ответим Вам при первой возможности.'
ABON_GOT_TEXT = 'Абоненту отправлено сообщение:\n\n{text}'
CREATING_LOG = 'Топик "{topic}" создан'
CLOSING_LOG = '{name} закрыл топик "{topic}"'
BROADCAST_LOG = '{name}\n\nвсем ожидающим:\n\n{text}'
POST_ERROR_LOG = 'Клиент Mediator_{social} недоступен:\n{error}'

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
