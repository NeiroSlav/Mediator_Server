from controller.post.request import foreign_api
from controller.bot.controll import bot_topic

from controller.backup.backuper import Backuper
from controller.backup.statistics import Statist
from controller.backup.aliaser import Aliaser

aliaser = Aliaser()

from controller.message_dto import MessageDTO

from controller.api.income_api import *
from controller.bot.handlers import *

from controller.bot.init import start_bot
from controller.api.init import start_fastapi
