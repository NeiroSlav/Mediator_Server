from controller.post.request import ForeignApi
from controller.bot.controll import BotTopic
from controller.message_dto import MessageDTO

foreign_api = ForeignApi()
bot_topic = BotTopic()


from controller.api.income_api import *
from controller.bot.handlers import *

from controller.bot.init import start_bot
from controller.api.init import start_fastapi