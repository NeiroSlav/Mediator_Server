from controller import *

# Запуск процесса поллинга
async def main():
    start_fastapi()
    await start_bot()

if __name__ == "__main__":
    asyncio.run(main())
