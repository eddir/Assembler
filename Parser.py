import re


class Parser:
    """Инкапсулирует доступ к входному коду. Читает команду языка ассемблер, разделяет ее на компоненты
    (поля и символы) и предоставляет удобный доступ к ним. Дополнительно, удаляет все пробелы и комментарии.
    """

    # Входной файл Prog.asm
    file = None

    # Текущая обрабатываемая строка
    current_line = None

    # Текущая обрабатываемая команда
    current_command = None

    # Типы команд
    A_COMMAND = 1  # @Xxx, где Xxx есть либо символ, либо десятичное число
    C_COMMAND = 2  # dest=comp;jump
    L_COMMAND = 3  # (Xxx), где Xxx есть символ. В действительности псевдокоманда

    def __init__(self, path: str):
        """Открывает входной файл/поток и приготавливается к его обработке
        """
        self.file = open(path)

    def __del__(self):
        """Закрытие потока файла при завершении программы
        """
        if self.file:
            self.file.close()

    def hasMoreCommands(self):
        """Есть ли еще команды на входе?
        """

        # Команды читаются из предоставленного файла
        # К сожалению (или к счастию?), в языке Python нет встроенного метода EOF, который мог бы сообщать о
        # достижении курсором конца файла. Вместо этого предлагается считывать файл построчно до получения пустой
        # строки.
        next_line = True
        while next_line:
            self.current_line = self.file.readline()

            # Игнорируются комментарии, начинающийся со //
            next_line = self.current_line != "" and (self.current_line[:2] == "//" or self.current_line == "\n")

        # Команды прекращаются, когда достигнут конец файла, то есть чтение файла вернуло пустую строку
        return self.current_line != ""

    def advance(self):
        """Читает следующую команду из входа и делает ее следующей командой. Вызывается только если hasMoreCommands()
        есть true. Первоначально текущей команды нет.
        """

        # Игнорируются комментарии
        if "//" in self.current_line:
            self.current_line = self.current_line[:self.current_line.find("//")]

        # Текущая команда извлекается путём удаления из строки знаков табуляции слева и справа.
        self.current_command = self.current_line.strip()

    def commandType(self):
        """Возвращает тип текущей команды:
        * A_COMMAND для @Xxx, где Xxx есть либо символ, либо десятичное число
        * C_COMMAND для dest=comp;jump
        * L_COMMAND (в действительности псевдокоманда) для (Xxx), где Xxx есть символ.
        """

        if self.current_command.startswith('@'):
            return self.A_COMMAND

        # Регулярное выражение проверяет все 3 случая для C_COMMAND:
        # Поля dest или jump могут быть пустыми.
        # Если dest пусто, то «=» опускается.
        # Если jump пусто, то «;» опускается.
        elif re.match(r'^(([A-Z0-9]*=)?[-\\!]?([A-Z0-9])*([+-\\&|][A-Z0-9])?(;[A-Z0-9]*)?)$', self.current_command):
            return self.C_COMMAND

        elif re.match(r'^\([A-Za-z0-9_\\.:$]*\)$', self.current_command):
            return self.L_COMMAND

        return False

    def symbol(self):
        """Возвращает символ или десятичное Xxx текущей команды @Xxx или (Xxx). Вызывается только тогда,
        когда commandType() есть A_COMMAND или L_COMMAND.
        """

        return re.sub('[@()]', '', self.current_command)

    def dest(self):
        """Возвращает мнемонику dest в текущей С-команде (8 возможных вариантов). Вызывается только когда commandType()
        есть C_COMMAND.
        """

        # Если знака равно нет, то dest отсутствует
        if '=' in self.current_command:
            return self.current_command.split('=', 1)[0]

        return ""

    def comp(self):
        """ Возвращает мнемонику comp в текущей С-команде (28 возможных вариантов). Вызывается только когда
        commandType() есть C_COMMAND.
        """
        delimiter1 = 0
        delimiter2 = len(self.current_command)

        if '=' in self.current_command:
            delimiter1 = self.current_command.find('=') + 1

        if ';' in self.current_command:
            delimiter2 = self.current_command.find(';')

        return self.current_command[delimiter1:delimiter2]

    def jump(self):
        """ Возвращает мнемонику jump в текущей С-команде (8 возможных вариантов). Вызывается только когда commandType()
        есть C_COMMAND.
        """

        if ';' in self.current_command:
            return self.current_command.split(';')[1]

        return ""
