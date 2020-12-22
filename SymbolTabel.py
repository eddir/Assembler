class SymbolTable:
    """Хранит соответствие между символическими метками и численными адресами.
    """

    def __init__(self):
        # Создание таблицы меток
        self.table_label = {}
        # Инициализация таблицы переменных
        self.table_vars = {}

        # По соглашению символы хранятся начиная с адреса RAM[16]
        self.free_address = 16

        # Запись стандартных символов
        defaults = {
            'SP': 0,
            'LCL': 1,
            'ARG': 2,
            'THIS': 3,
            'THAT': 4,
            'R0': 0,
            'R1': 1,
            'R2': 2,
            'R3': 3,
            'R4': 4,
            'R5': 5,
            'R6': 6,
            'R7': 7,
            'R8': 8,
            'R9': 9,
            'R10': 10,
            'R11': 11,
            'R12': 12,
            'R13': 13,
            'R14': 14,
            'R15': 15,
            'SCREEN': 16384,
            'KBD': 24576
        }

        # Для читаемости адреса записаны в десятичной системы исчисления. Их нужно сконвертировать.
        for symbol, address in defaults.items():
            self.table_vars[symbol] = bin(int(address))[2:].rjust(16, '0')

    def addEntry(self, symbol: str, address: int = None):
        """Добавляет пару (symbol,address)в таблицу
        :param symbol:
        :param address:
        :return:
        """
        """Важное замечание!
        Целесеобразно разделить этот метод на метод записи меток и метод записи переменных. Однако реализация в задании 
        требует конкретных методов в программном коде. Не исключаю, что это ошибка проектирования ПО, допущенная мною 
        в ходе невнимательного прочтения документации, приложенной к данной лабораторной работе.
        """

        if address is None:
            address = dec_to_address(self.free_address)
            while address in self.table_vars.values():
                self.free_address += 1
                address = dec_to_address(self.free_address)
            self.table_vars[symbol] = address
        else:
            self.table_label[symbol] = dec_to_address(address)

        return address

    def contains(self, symbol: str):
        """Содержит ли таблица имен данный symbol
        :param symbol:
        :return:
        """

        return symbol in self.table_label or symbol in self.table_vars

    def GetAddress(self, symbol: str):
        """Возвращает адрес, ассоциированный с symbol
        :param symbol:
        :return:
        """

        if symbol in self.table_label:
            return self.table_label.get(symbol)
        else:
            return self.table_vars.get(symbol)


def dec_to_address(address):
    """Конвертирует указанный десятичный адрес в бинарную команду
    :param address:
    :return:
    """
    return bin(int(address))[2:].rjust(16, '0')
