class Parser:
    file = None

    def __init__(self, path):
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
        pass

    def advance(self):
        """Читает следующую команду из входа и делает ее следующей командой. Вызывается только если hasMoreCommands()
        есть true. Первоначально текущей команды нет.
        """
        pass

    def commandType(self):
        """Возвращает тип текущей команды:
        * A_COMMAND для @Xxx, где Xxx есть либо символ, либо десятичное число
        * C_COMMAND для dest=comp;jump
        * L_COMMAND (в действительности псевдокоманда) для (Xxx), где Xxx есть символ.
        """
        pass

    def symbol(self):
        """Возвращает символ или десятичное Xxx текущей команды @Xxx или (Xxx). Вызывается только тогда,
        когда commandType() есть A_COMMAND или L_COMMAND.
        """
        pass

    def dest(self):
        """Возвращает мнемонику dest в текущей С-команде (8 возможных вариантов). Вызывается только когда ommandType()
        есть C_COMMAND.
        """
        pass

    def comp(self):
        """ Возвращает мнемонику comp в текущей С-команде (28 возможных вариантов). Вызывается только когда
        commandType() есть C_COMMAND.
        """
        pass

    def jump(self):
        """ Возвращает мнемонику jump в текущей С-команде (8 возможных вариантов). Вызывается только когда commandType()
        есть C_COMMAND.
        """
        pass
