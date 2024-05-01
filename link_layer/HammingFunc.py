import random

FRAME_ERROR_ODDS = 0.1
FRAME_LOST_ODDS = 0.02
INFORMATION_BITS = 4
CONTROL_BITS = 3

# single_error_counter = 0
# double_errors_counter = 0
# lost_frames_counter = 0


def encoding_hamming_code_7_4(segment):
    remainder_: int = len(segment) % 4

    # если не хватает информационных битов, то заполним их нулями
    if remainder_ != 0:
        segment += "0" * (4 - remainder_)
    full_segment = str()
    # part_segment = list()

    # разделение сегментов на кадры
    for frame_index_end in range(4, len(segment) + 1, 4):
        print(segment)
        part_segment = list(segment[frame_index_end - 4:frame_index_end])

        # вставка нерассчитанных контрольных битов
        for control_bit_position in range(CONTROL_BITS):
            part_segment.insert(2 ** control_bit_position - 1, '0')
        # print(part_segment)

        # установка значений контрольных битов
        # для 1 контрольного бита
        control_bit = 0
        for position in range(2, INFORMATION_BITS + CONTROL_BITS, 2):
            control_bit ^= int(part_segment[position])
        part_segment[0] = str(control_bit)

        # для 2 контрольного бита
        control_bit = 0
        position = 1
        while position < INFORMATION_BITS + CONTROL_BITS:
            control_bit ^= int(part_segment[position]) ^ int(part_segment[position + 1])
            position += 4
        part_segment[1] = str(control_bit)

        # для 3 контрольного бита
        # print(part_segment)
        control_bit = 0
        for position in range(4, INFORMATION_BITS + CONTROL_BITS):
            control_bit ^= int(part_segment[position])
        part_segment[3] = str(control_bit)

        full_segment += ''.join(part_segment)
        # высчитываем бит четности
        bit_parity = int(part_segment[0])
        for bit in part_segment[1:7]:
            bit_parity ^= int(bit)
        full_segment += str(bit_parity)

    return full_segment, remainder_


def decoding_hamming_code_7_4(segment, remainder_):
    # global lost_frames_counter
    if random.random() < FRAME_LOST_ODDS:
        return ""
    full_segment = str()
    # разделение сегментов на кадры
    for frame_index_end in range(8, len(segment) + 1, 8):
        part_segment = list(segment[frame_index_end - 8:frame_index_end])
        check_part_segment = part_segment.copy()

        # обнуляем проверочные биты
        check_part_segment[0] = '0'
        check_part_segment[1] = '0'
        check_part_segment[3] = '0'

        # проверка значений контрольных битов
        # для 1 контрольного бита
        control_bit = 0
        for position in range(2, INFORMATION_BITS + CONTROL_BITS, 2):
            control_bit ^= int(check_part_segment[position])
        check_part_segment[0] = str(control_bit)

        # для 2 контрольного бита
        control_bit = 0
        position = 1
        while position < INFORMATION_BITS + CONTROL_BITS:
            control_bit ^= int(check_part_segment[position]) ^ int(check_part_segment[position + 1])
            position += 4
        check_part_segment[1] = str(control_bit)

        # для 3 контрольного бита
        control_bit = 0
        for position in range(4, INFORMATION_BITS + CONTROL_BITS):
            control_bit ^= int(check_part_segment[position])
        check_part_segment[3] = str(control_bit)

        # проверяем контрольные биты на наличие ошибок
        list_error_index = []
        if check_part_segment[0] != part_segment[0]:
            list_error_index.append(1)
        if check_part_segment[1] != part_segment[1]:
            list_error_index.append(2)
        if check_part_segment[3] != part_segment[3]:
            list_error_index.append(4)

        # bit_parity_received = int(part_segment[7])
        bit_parity_received = int(part_segment[0])
        print(part_segment)
        for bit in part_segment[1:]:
            bit_parity_received ^= int(bit)

        if bit_parity_received:
            print("Обнаружена 1 ошибка")
            print(list_error_index)
        else:
            if list_error_index:
                print("2 ошибки, исправление невозможно")
            else:
                print("Ошибок не обнаружено")
            print(list_error_index)
            full_segment += "".join(check_part_segment[2:3] + check_part_segment[4:7])
            continue

        # исправление ошибки
        errors_index = sum(list_error_index)
        check_part_segment[errors_index - 1] = str(int(check_part_segment[errors_index - 1]) ^ 1)

        full_segment += "".join(check_part_segment[2:3] + check_part_segment[4:7])

    # уберем лишние нули
    if remainder_ != 0:
        full_segment = full_segment[:len(full_segment) - (4 - remainder_)]

    return full_segment


def corrupt_hamming_code(segment):

    index_error_ = random.randrange(0, len(segment))
    segment = segment[:index_error_] + str(int(segment[index_error_]) ^ 1) + segment[index_error_ + 1:]

    return segment
