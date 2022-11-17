import json
from data.datatype import Datatype

"""
    Объект можно не создавать, парсит указанный в filename файл.
    Файл должен быть в json-формате следующего вида:
    { "WORKS": 
        [ {
            "words_en": "I have the computer",
            "words_ru": "У меня есть компьютер"
        },		
        {
            "words_en": "I have the computer",
            "words_ru": "У меня есть компьютер"
        } ]
    }
"""


class JSONParser:

    # view = True, если нужно посмотреть содержимое
    def get_list(self, filename, view=False):
        res = []
        with open(filename, encoding="UTF-8") as jsf:
            data = json.load(jsf)
            for p in data['WORKS']:
                res.append(Datatype(p['words_en'], p['words_ru']))

        if view:
            for i in range(len(res)):
                print(i, res[i])

        return res


if __name__ == "__main__":
    n = JSONParser().get_list("database.txt", True)
