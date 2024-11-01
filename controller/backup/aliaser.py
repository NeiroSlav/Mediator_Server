import json


class Aliaser:
    def __init__(self):
        self.file_path = "../aliases.json"
        # инициализируем пустой файл, если он не существует
        try:
            with open(self.file_path, "r") as file:
                json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            with open(self.file_path, "w") as file:
                json.dump({}, file)

    # возвращает значение по ключу
    def get(self, alias: str) -> str | None:
        with open(self.file_path, "r") as file:
            data = json.load(file)
        return data.get(alias, None)

    # добавляет или обновляет значение по ключу
    def set(self, alias: str, value: str):
        with open(self.file_path, "r") as file:
            data = json.load(file)

        data[alias] = value

        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)

    # удаляет значение и ключ
    def delete(self, alias: str):
        with open(self.file_path, "r") as file:
            data = json.load(file)

        if alias in data:
            del data[alias]
            with open(self.file_path, "w") as file:
                json.dump(data, file, indent=4)
