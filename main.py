import os
import time

import Code
from Parser import Parser


class Assembler:
    """
    Основная программа, урпавляющая всем трансляционным процессом
    """

    def __init__(self):
        """Открытие выходного потока и задание параметров
        """
        self.ASM_FILE = os.path.abspath("./Prog.asm")  # Входной поток
        self.HACK_FILE = os.path.abspath("./Prog.hack")  # Выходной поток

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
            parser = Parser(self.ASM_FILE)
            while parser.hasMoreCommands():
                parser.advance()
                command_type = parser.commandType()

                if command_type in (parser.A_COMMAND, parser.L_COMMAND):
                    symbol = parser.symbol()
                    command = "0" + bin(int(symbol))[2:].rjust(15, '0')  # Заполняем нулями недостающие биты

                elif command_type == parser.C_COMMAND:
                    command = '111' + Code.comp(parser.comp()) + Code.dest(parser.dest()) + Code.jump(parser.jump())

                else:
                    raise ValueError("Invalid command %s" % parser.current_command)

                #print("mnemonic: %s, command: %s" % (command, parser.current_command))
                self.output.write("%s\n" % command)

        except IOError:
            print("Файл Prog.asm не удалось открыть. Мы ожидаем, что он лежит по пути: {0} . Пожалуйста, "
                  "удостоверьтесь, что по указанному пути существует этот файл и на него прописаны права для чтения."
                  .format(self.ASM_FILE))
        finally:
            # Закрываем файл, чтобы сохранить изменения
            self.output.close()


if __name__ == '__main__':
    print('Запуск ассемблера...')

    time.sleep(0.5)

    asm = Assembler()
    asm.assembler()

    print("Выполнение завершено. Нажмите enter для выхода.")
    input()
