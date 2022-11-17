"""
    Класс для хранения пары англ+рус фразы.
"""


class Datatype:

    def __init__(self, en, ru):
        self._words_en = en
        self._words_ru = ru

    def __str__(self):
        return f"{self.words_en} / {self.words_ru}"

    @property
    def words_en(self):
        return self._words_en

    @words_en.setter
    def words_en(self, s):
        self._words_en = s

    @property
    def words_ru(self):
        return self._words_ru

    @words_ru.setter
    def words_ru(self, value):
        self._words_ru = value
