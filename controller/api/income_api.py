from controller.api.init import app
from controller.message_dto import MessageDTO
from model import handle_foreign_message


# апи для входящего сообщения на сервер
@app.post('/')
async def get_foreign_message(message_dto: MessageDTO):
    await handle_foreign_message(message_dto)
