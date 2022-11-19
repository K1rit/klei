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

    def is_complete(self):
        # Вернёт True, если пользователь угадал
        # ВСЕ буквы в слове
        ret = True
        n = 0
        while n < len(self.enabled_chars) and ret:
            ret = ret and self.enabled_chars[n]
            n += 1

        return ret

    def put_char(self, ch):
        # Вернёт, сколько символов угадано
        # 0, если пользователь не угадал ничего
        ret = 0
        tmp = self.words_en.upper()
        for i in range(len(tmp)):
            if ch == tmp[i] and not self.enabled_chars[i]:
                self.enabled_chars[i] = True
                ret += 1
        return ret

    def get_proposal(self):
        # Вернёт строку, которую нужно показывать пользователю
        # на текущем этапе игры
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
