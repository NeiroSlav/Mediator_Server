from controller.api.init import app
from controller.message_dto import MessageDTO
from model import handle_foreign_message, redirect_helper_message, handle_topic_message


# апи для входящего сообщения на сервер
@app.post("/")
async def get_foreign_message(message_dto: MessageDTO):
    await handle_foreign_message(message_dto)


# апи для входящего сообщения на сервер
@app.post("/redir")
async def get_foreign_message(message_dto: MessageDTO):
    await handle_topic_message(message_dto)
