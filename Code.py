"""Транслирует мнемоники языка ассемблераHack в бинарные коды
"""


def dest(mnemonic: str):
    """Возвращает бинарный код мнемоники dest.
    :param mnemonic: мнемоника dest, которую необходимо преобразовать в бинарное представление команды
    :return: string
    """
    instructions = {
        'null': "000",
        'M': "001",
        'D': "010",
        'MD': "011",
        'A': "100",
        'AM': "101",
        'AD': "110",
        'AMD': "111"
    }

    return instructions[mnemonic] if mnemonic in instructions else instructions['null']


def comp(mnemonic: str):
    """Возвращает бинарный код мнемоники comp.
    :param mnemonic: мнемоника comp, которую необходимо преобразовать в бинарное представление команды
    :return: string
    """
    instructions_0 = {
        '0': "101010",
        '1': "111111",
        '-1': "111010",
        'D': "001100",
        'A': "110000",
        '!D': "110001",
        '!A': "110001",
        '-D': "001111",
        '-A': "110011",
        'D+1': "011111",
        'A+1': "110111",
        'D-1': "001110",
        'A-1': "110010",
        'D+A': "000010",
        'D-A': "010011",
        'A-D': "000111",
        'D&A': "000000",
        'D|A': "010101",
    }

    instructions_1 = {
        'M': instructions_0['A'],
        '!M': instructions_0['!A'],
        '-M': instructions_0['-A'],
        'M+1': instructions_0['A+1'],
        'M-1': instructions_0['A-1'],
        'D+M': instructions_0['D+A'],
        'D-M': instructions_0['D-A'],
        'M-D': instructions_0['A-D'],
        'D&M': instructions_0['D&A'],
        'D|M': instructions_0['D|A'],
    }

    # Согласно определнию a бит зависит от c битов
    # Сам a бит определяет будет ли использоваться M Илм A
    if mnemonic in instructions_0:
        return '0' + instructions_0[mnemonic]

    if mnemonic in instructions_1:
        return '1' + instructions_1[mnemonic]

    raise ValueError('Invalid mnemonic %s' % mnemonic)


def jump(mnemonic: str):
    """Возвращает бинарный код мнемоники jump.
    :param mnemonic: мнемоника jump, которую необходимо преобразовать в бинарное представление команды
    :return: string
    """
    instructions = {
        'null': "000",
        'JGT': "001",
        'JEQ': "010",
        'JGE': "011",
        'JLT': "100",
        'JNE': "101",
        'JLE': "110",
        'JMP': "111"
    }

    return instructions[mnemonic] if mnemonic in instructions else instructions['null']
