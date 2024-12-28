import copy
import httpx
from controller.message_dto import MessageDTO
from controller.bot.controll import bot_topic
from const import CLIENT_PORTS, POST_ERROR_LOG


class ForeignApi:

    # отправка сообщения на сторонний сервис, учитывая социальную сеть
    async def send_message_to_client(self, message_dto: MessageDTO):
        port = CLIENT_PORTS[message_dto.social]
        try:
            await self._send_post_request(
                f"http://127.0.0.1:{port}/", 
                message_dto.model_dump_json()
            )
        except Exception as e:
            if not e:
                return

            await bot_topic.log(
                POST_ERROR_LOG.format(
                    social=message_dto.social,
                    error=e,
                )
            )
            raise e


    # отправка сообщения на сервис хелпера
    async def send_message_to_helper(self, message_dto: MessageDTO, to_abon: bool, indefier: str | None = None):
        new_message = copy.deepcopy(message_dto)
        new_message.sender_name = "assistant" if to_abon else "user"
        if indefier:
            new_message.chat_id = indefier

        port = CLIENT_PORTS["helper"]
        try:
            await self._send_post_request(
                f"http://127.0.0.1:{port}/", 
                new_message.model_dump_json(),
                timeout=0.2,
            )
        except Exception as e:
            pass

    # отправка команды удаления сервису хелпера
    async def send_close_to_helper(self, topic_id: int):
        print("CLOSING...")
        port = CLIENT_PORTS["helper"]
        try:
            await self._send_post_request(
                f"http://127.0.0.1:{port}/forget_dialog/{topic_id}",
                timeout=0.2,
            )
        except Exception as e:
            pass


    # отправляет post-запросс по url с указаными данными
    @staticmethod
    async def _send_post_request(url: str, data: str = "", timeout: float = 10):
        async with httpx.AsyncClient() as client:
            return await client.post(url, data=data, timeout=timeout)


foreign_api = ForeignApi()
