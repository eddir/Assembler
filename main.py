import os
import sys
import time

import Code
from Parser import Parser
from SymbolTabel import SymbolTable


class Assembler:
    """
    Основная программа, урпавляющая всем трансляционным процессом
    """

    def __init__(self):
        """Открытие выходного потока и задание параметров
        """

        self.input_file = "Prog.asm"

        if len(sys.argv) > 1:
            self.input_file = sys.argv[1]

        self.ASM_FILE = os.path.abspath(self.input_file)  # Входной поток
        self.HACK_FILE = os.path.abspath("Prog.hack")  # Выходной поток

        # Открываем файл для записи результирующего бинарного файла
        self.output = open(self.HACK_FILE, 'w')

    def __del__(self):
        """По завершению главное закрыть открытые потоки
        :return:
        """
        if self.output:
            print("Завершено")
            self.output.close()

    def assembler(self):
        try:
            # Первый проход. Строим таблицу символов
            table = SymbolTable()
            parser = Parser(self.ASM_FILE)
            instruction_address = 0
            while parser.hasMoreCommands():
                parser.advance()
                command_type = parser.commandType()

                if command_type in (parser.A_COMMAND, parser.C_COMMAND):
                    instruction_address += 1
                elif command_type == parser.L_COMMAND:
                    # Сохраняем адрес для новой псевдокоманды
                    table.addEntry(parser.symbol(), instruction_address)

            # Второй проход.
            parser = Parser(self.ASM_FILE)
            while parser.hasMoreCommands():
                parser.advance()
                command_type = parser.commandType()

                if command_type == parser.A_COMMAND:
                    symbol = parser.symbol()

                    if symbol.isnumeric():
                        command = "0" + bin(int(symbol))[2:].rjust(15, '0')  # Заполняем нулями недостающие биты
                    else:
                        if table.contains(symbol):
                            command = table.GetAddress(symbol)
                        else:
                            # Найдена неизвестная псевдокоманда. Запрашиваем адрес для неё.
                            command = table.addEntry(symbol)

                    self.output.write("%s\n" % command)

                elif command_type == parser.C_COMMAND:
                    command = '111' + Code.comp(parser.comp()) + Code.dest(parser.dest()) + Code.jump(parser.jump())
                    self.output.write("%s\n" % command)

                elif command_type != parser.L_COMMAND:
                    raise ValueError("Invalid command %s" % parser.current_command)

        except IOError:
            print("Файл {0} не удалось открыть. Мы ожидаем, что он лежит по пути: {1} . Пожалуйста, "
                  "удостоверьтесь, что по указанному пути существует этот файл и на него прописаны права для чтения."
                  .format(self.input_file, self.ASM_FILE))
        finally:
            # Закрываем файл, чтобы сохранить изменения
            self.output.close()


if __name__ == '__main__':
    print("***\nПрограмма ассемблер, выполненная по инструкций от nand2tetris, студента группы бПИНЖ21 Росткова Э.А.\n***\n")
    print('Запуск ассемблера...')

    time.sleep(0.5)

    asm = Assembler()
    asm.assembler()

    print("Выполнение завершено. Нажмите enter для выхода.")
    input()
