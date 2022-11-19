"""
    Класс для хранения пары англ+рус фразы.
"""


class Datatype:

    def __init__(self, cat: str, en: str, ru: str):
        self._category = cat
        self._words_en = en
        self._words_ru = ru

        self.enabled_chars = []
        tmp = self._words_en.upper()
        p1 = ord("A")
        p2 = ord("Z")
        for i in range(len(tmp)):
            if ord(tmp[i]) >= p1 and ord(tmp[i]) <= p2:
                self.enabled_chars.append(False)
            else:
                self.enabled_chars.append(True)
        # print(self.enabled_chars)

    def put_char(self, ch):
        ret = 0
        return ret

    def get_proposal(self):
        ret = ""
        for i in range(len(self._words_en)):
            if self.enabled_chars[i]:
                ret += self.words_en[i]
            else:
                ret += "_"
        return ret


    def __str__(self):
        return f"{self.category}. {self.words_en} / {self.words_ru}"

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, s):
        self._category = s

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
