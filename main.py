import os
import sys
import time

from Parser import Parser


class Assembler:
    """
    Основная программа, урпавляющая всем трансляционным процессом
    """

    def __init__(self):
        self.ASM_FILE = os.path.abspath("./Prog.asm")

    def assembler(self):
        try:
            parser = Parser(self.ASM_FILE)

        except IOError:
            print("Файл Prog.asm не удалось открыть. Мы ожидаем, что он лежит по пути: {0} . Пожалуйста, "
                  "удостоверьтесь, что по указанному пути существует этот файл и на него прописаны права для чтения."
                  .format(self.ASM_FILE))


if __name__ == '__main__':
    print('Запуск ассемблера...')

    time.sleep(0.5)

    asm = Assembler()
    asm.assembler()

    print("Выполнение завершено. Нажмите enter для выхода.")
    input()
