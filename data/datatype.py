import random
"""
    Класс для хранения пары англ+рус фразы.
"""


class Datatype:

    to_prise = ["Здорово!",
                "Супер!",
                "Ты лучший!",
                "Прекрасно!",
                "Жжёшь!",
                "Браво!",
                "Успех!",
                "Гениально!",
                "Круто!",
                "Молодец!",
                "Отлично!",
                "Великолепно!",
                "Талант!",
                "Правильно!",
                "Супер!",
                "Офигенно!",
                "Это пять!",
                "Правильно!",
                ]

    def __init__(self, cat: str, en: str, ru: str):
        self._category = cat
        self._words_en = en
        self._words_ru = ru
        self.multilines = None
        self.enabled_chars = None
        self.reset_data()

    # Надо "перегрузить" строку и убрать открытые буквы
    def reset_data(self):
        self.multilines = None
        self.enabled_chars = []
        tmp = self._words_en.upper()
        p1 = ord("A")
        p2 = ord("Z")
        for i in range(len(tmp)):
            if p1 <= ord(tmp[i]) <= p2:
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
        print(self.words_en.upper())
        for i in range(len(tmp)):
            if ch == tmp[i] and not self.enabled_chars[i]:
                self.enabled_chars[i] = True
                ret += 1
        return ret

    def create_multilines(self, line, size_line):
        line = line.split(" ")
        new_lines = []
        i = 0
        cl = 0
        new_lines.append("")

        while i < len(line):
            while i < len(line) and len(new_lines[cl] + line[i] + " ") <= size_line:
                if len(new_lines[cl] + line[i] + " ") <= size_line:
                    new_lines[cl] += line[i] + " "
                else:
                    new_lines[cl] += line[i]
                i += 1
            if i < len(line):
                new_lines.append("")
                cl += 1

        # print(f"new lines: {new_lines[cl]}")
        if len(new_lines[cl]) == 0:
            del new_lines[cl]

        # for i in range(len(new_lines)):
        #     new_lines[i] = new_lines[i][0:len(new_lines[i]) - 1]

        if new_lines[len(new_lines) - 1][-1] == " ":
            new_lines[len(new_lines) - 1] = new_lines[len(new_lines) - 1][0:len(new_lines[len(new_lines) - 1]) - 1]

        return new_lines

    def get_proposal(self):
        # Вернёт список строк, который нужно показывать пользователю
        # на текущем этапе игры

        # Получить разбитые строки длиной макс=30 символов
        if self.multilines is None:
            self.multilines = self.create_multilines(self.words_en, 30)

        # print(f"У нас {self.multilines}")

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

            # Удалим начальный и хвостовой пробелы, если они есть
            #if self.multilines[i][0] == " ":
            #    self.multilines[i] = self.multilines[i][1:len(self.multilines[i])]
            #if self.multilines[i][-1] == " ":
            #    self.multilines[i] = self.multilines[i][0:len(self.multilines[i]) - 1]

        return self.multilines

    def get_help_char(self):
        num = 0
        find = False
        while num < len(self.enabled_chars) and not find:
            if not self.enabled_chars[num]:
                find = True
            else:
                num += 1

        # print(self.enabled_chars)
        # print(f"Первая найденная неугаданная буква: {num} = {self.words_en[num]}")

        return self.words_en[num].upper()

    #{random.choice(Datatype.to_prise)} 
    def get_translate_ru(self):
        return self.create_multilines(f'"{self.words_ru}"', 50)

    def get_prize_str(self):
        return random.choice(Datatype.to_prise) 

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

