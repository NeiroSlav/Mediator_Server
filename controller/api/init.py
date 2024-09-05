from fastapi import FastAPI
from const import SERVER_PORT
import asyncio


# инициализация сервера для api
app = FastAPI()


# процесс запуска сервера
async def run_server():
    import uvicorn

    config = uvicorn.Config(app, host="0.0.0.0", port=SERVER_PORT)
    server = uvicorn.Server(config)
    await server.serve()


# запуск сервера
def start_fastapi():
    loop = asyncio.get_event_loop()
    loop.create_task(run_server())
