"""
    Класс для хранения пары англ+рус фразы.
"""


class Datatype:

    def __init__(self, cat: str, en: str, ru: str):
        self._category = cat
        self._words_en = en
        self._words_ru = ru
        self.multilines = None

        self.enabled_chars = []
        tmp = self._words_en.upper()
        p1 = ord("A")
        p2 = ord("Z")
        for i in range(len(tmp)):
            if ord(tmp[i]) >= p1 and ord(tmp[i]) <= p2:
                self.enabled_chars.append(False)
            else:
                self.enabled_chars.append(True)


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

    def create_multilines(self, line):
        line = line.split(" ")
        new_lines = []
        i = 0
        cl = 0
        new_lines.append("")

        while i < len(line):
            while i < len(line) and len(new_lines[cl] + line[i] + " ") <= 30:
                new_lines[cl] += line[i] + " "
                i += 1
            new_lines.append("")
            cl += 1

        del new_lines[cl]
        for i in range(len(new_lines)):
            new_lines[i] = new_lines[i][0:len(new_lines[i]) - 1]

        return new_lines

    def get_proposal(self):
        # Вернёт список строк, который нужно показывать пользователю
        # на текущем этапе игры

        # Получить разбитые строки длиной макс=30 символов
        if self.multilines is None:
            self.multilines = self.create_multilines(self.words_en)

        # Обработать вывод, заменив все не открытые буквы подчёркиванием
        # и наоборот, минуя знаки препинания
        count = 0
        for i in range(len(self.multilines)):
            new_line = ""
            for j in range(len(self.multilines[i])):
                if self.enabled_chars[count]:
                    new_line += self.words_en[count]
                else:
                    new_line += "_"
                count += 1
            self.multilines[i] = new_line

        return self.multilines


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
