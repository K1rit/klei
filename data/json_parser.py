import json
from data.datatype import Datatype

"""
    Объект можно не создавать, парсит указанный в filename файл.
    Файл должен быть в json-формате следующего вида:
{
    "THEMES": [
        {
        "CATEGORY": "",
        "WORDS": [
            {
                "words_en": "",
                "words_ru": ""
            },
            {
                "words_en": "",
                "words_ru": ""
            },
            {
                "words_en": "",
                "words_ru": ""
            }
            ]
        }
        ]

"""


class JSONParser:

    # view = True, если нужно посмотреть содержимое
    def get_list(self, filename, view=False):
        res = []
        with open(filename, encoding="UTF-8") as jsf:
            data = json.load(jsf)
            for txt in data["THEMES"]:
                for task in txt['WORDS']:
                    res.append(Datatype(txt['CATEGORY'], task['words_en'], task['words_ru']))
                    # print(txt['CATEGORY'], " ", end="")
                    # print(task['words_en'], "/", task['words_ru'])

        if view:
            for i in range(len(res)):
                print(i, res[i])

        return res

if __name__ == "__main__":
    n = JSONParser().get_list("database.txt", False)
