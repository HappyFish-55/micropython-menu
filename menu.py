# ИЮЛЬ 2020
# Меню реализация в виде класса


class Menu:

    name = ''  # имя группы настроек (на каждый инструмент своя группа)
    parameter = []  # указатель выбранного параметра (для изменения настроек)
    value_count = 3  # указатель для элемента перебора параметров "VAR"
    select = 0
    settings_list = []

    def __init__(self, data):
        """ data - .txt file """
        self.data = data
        # имя теперь берется из названия файла (что разумно)
        self.name = data[0:-4]  # удаление расширения '.txt'
        self.read()

    def read(self):
        with open(self.data) as file:
            self.settings_list = (file.read()).split()
            file.close()
            for i in range(len(self.settings_list)):
                self.settings_list[i] = self.settings_list[
                    i].split(',')  # формирование списка настроек

    def save(self):
        """saving changed values of parameters"""
        with open(self.data, 'w') as file:
            for setting in self.settings_list:
                file.write(','.join(setting) + '\n')
            file.close()

    def cursor(self, cursor_pos, parameter):
        if cursor_pos == 0:
            if parameter[0] == self.settings_list[-1][0]:
                cursor_form = '< '
            elif parameter[0] == self.settings_list[0][0]:
                cursor_form = ' >'
            else:
                cursor_form = '<>'
        elif cursor_pos == 1:
            if parameter[2] == parameter[-1]:
                cursor_form = '< '
            elif parameter[2] == parameter[3]:
                cursor_form = ' >'
            else:
                cursor_form = '<>'
        return cursor_form

    def change(self, cursor_pos, direction):
        """cursor pos: 0 - parameters, 1 - values
        direction: left or right"""
        if cursor_pos == 0:
            if (direction == 'right' and self.select < (len(self.settings_list) - 1)):
                self.select += 1
            elif (direction == 'left' and self.select > 0):
                self.select -= 1
            self.parameter = self.settings_list[self.select]
            cursor_form = self.cursor(cursor_pos, self.parameter)

        if cursor_pos == 1:

            if self.parameter[1] == 'inc':  # элемент меню - численное значение
                self.parameter[2] = int(self.parameter[2])
                self.parameter[3] = int(self.parameter[3])
                self.parameter[4] = int(self.parameter[4])
                if direction == 'right':
                    # проверка на максимальное значение
                    if self.parameter[2] < self.parameter[4]:
                        self.parameter[2] += 1
                if direction == 'left':
                    # проверка на минимальное значение
                    if self.parameter[2] > self.parameter[3]:
                        self.parameter[2] -= 1
                self.parameter[2] = str(self.parameter[2])
                self.parameter[3] = str(self.parameter[3])
                self.parameter[4] = str(self.parameter[4])

            if self.parameter[1] == 'switch':  # элемент меню - переключатель
                if direction == 'right':
                    if self.parameter[2] == self.parameter[3]:
                        self.parameter[2] = self.parameter[4]
                if direction == 'left':
                    if self.parameter[2] == self.parameter[4]:
                        self.parameter[2] = self.parameter[3]

            if self.parameter[1] == 'var':  # элемент меню - перебор вариантов
                self.value_count = self.parameter.index(self.parameter[2], 3)
                if direction == 'right':
                    if self.value_count < (len(self.parameter) - 1):
                        self.value_count += 1
                        self.parameter[2] = self.parameter[self.value_count]
                if direction == 'left':
                    if self.value_count > 3:
                        self.value_count -= 1
                        self.parameter[2] = self.parameter[self.value_count]
            # определение формы курсора
            cursor_form = self.cursor(cursor_pos, self.parameter)
        return self.name, self.parameter[0], self.parameter[2], cursor_form
