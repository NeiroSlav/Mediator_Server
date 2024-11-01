from const import GREETING_TEXT, ABON_GOT_TEXT, AUTO_CLOSE_TIME
from controller import MessageDTO, aliaser
from structures import ChatLink
from model.scheduler import Scheduler
from model.commands.suffix import suffix


# приветствие абонента
async def greet_abon(chat_link: ChatLink):
    text = GREETING_TEXT

    # если включен режим суфикса,
    if suffix["enabled"]:  # добавляет его текст к приветствию
        text += f'\n\n{suffix["text"]}'

    # формирует приветственное сообщение абоненту
    message_dto = MessageDTO.new(text)
    notification = MessageDTO.new(ABON_GOT_TEXT.format(text=text))

    await chat_link.abon_chat.send(message_dto)  # отправка абону приветственного текста
    await chat_link.topic.send(
        notification
    )  # отправка в топик информации о приветствии


# отложит процесс автозакрытия топика
def try_schedule_close(chat_link: ChatLink):
    # если установлено время автозакрытия топика, и топик не удержан
    if AUTO_CLOSE_TIME and not chat_link.topic.meta.hold:
        Scheduler.sch_dialog_close(chat_link)
        Scheduler.sch_dialog_finish(chat_link)
