import httpx
import json
from controller.message_dto import MessageDTO
from const import CLIENT_PORTS

class ForeignApi:

    # отправка сообщения на сторонний сервис, учитывая социальную сеть
    async def send_message_out(self, message: MessageDTO):
        port = CLIENT_PORTS[message.social]
        await self._send_post_request(
            f'http://127.0.0.1:{port}/', 
            message.model_dump_json()
        )

    # отправляет post-запросс по url с указаными данными 
    @staticmethod
    async def _send_post_request(url: str, data: json):
        async with httpx.AsyncClient() as client:
            try:
                return await client.post(url, data=data)
            except Exception as e:
                return False
        