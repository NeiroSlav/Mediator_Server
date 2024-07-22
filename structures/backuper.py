import json
from pprint import pprint
from const import BACKUP


# класс бекапа связок чатов, и возвращения из бекапа
class Backuper:
    file_name: str = 'backup.json'

    @classmethod
    async def save(cls, all_chats: list):
        if not BACKUP:
            print('Бекап выключен')
            return

        data = list(map(lambda x: x.to_dict(), all_chats))
        try:
            with open(cls.file_name, 'w') as backup_file:
                json.dump(data, backup_file)
            print('Бекап сохранён')
        except Exception as e:
            # await Logger.add(f'Ошибка сохранения бекапа: {e}')
            print(f'Ошибка сохранения бекапа: {e}')

    @classmethod
    def read(cls) -> list:
        if not BACKUP:
            print('Бекап выключен')
            return []
        
        try:
            with open(cls.file_name) as backup_file:
                data = json.load(backup_file)
            pprint(data)
            print('Бекап успешно считан')
            return data

        except Exception as e:
            # await Logger.add(f'Ошибка чтения бекапа: {e}')
            print(f'Ошибка чтения бекапа: {e}')
            return []
