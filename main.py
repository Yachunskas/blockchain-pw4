# Функція для перетворення шістнадцяткового числа на двійкове
def hex_to_bin(hex_num):
    decimal_num = int(hex_num, 16)
    binary_num = bin(decimal_num)[2:]
    return binary_num

# Функція для перетворення двійкового числа на шістнадцяткове
def binary_to_hex(binary_str):
    try:
        decimal_value = int(binary_str, 2)
        hex_value = hex(decimal_value)
        return hex_value[2:].upper()
    except ValueError:
        return "Invalid binary number"

# Функція для розділення блоку даних на дві тетради, які перетворюються в координати для матриці
def byte_to_coordinates(byte_str):
    if len(byte_str) != 2:
        raise ValueError("Рядок має містити рівно 2 символи.")

    x = int(byte_str[0], 16)
    y = int(byte_str[1], 16)  
    arr = [x, y]
    if not (0 <= x <= 15 and 0 <= y <= 15):
        raise ValueError("Символи повинні бути шістнадцятковими значеннями (0-9, A-F).")
    
    return arr

#  Таблиця блоків та індексів для перетворення на координати
# 
#         0   1   2   3   4   5   6   7   8   9   a   b   c   d   e   f 
#         0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15
#  0 0
#  1 1
#  2 2
#  3 3 
#  4 4
#  5 5
#  6 6
#  7 7
#  8 8 
#  9 9
#  a 10
#  b 11
#  c 12 
#  d 13
#  e 14 
#  f 15


# Матриця прямого перетворення
forward_rijndael = [
    [ '63', '7c', '77', '7b', 'f2', '6b', '6f', 'c5', '30', '01', '67', '2b', 'fe', 'd7', 'ab', '76' ], 
    [ 'ca', '82', 'c9', '7d', 'fa', '59', '47', 'f0', 'ad', 'd4', 'a2', 'af', '9c', 'a4', '72', 'c0' ], 
    [ 'b7', 'fd', '93', '26', '36', '3f', 'f7', 'cc', '34', 'a5', 'e5', 'f1', '71', 'd8', '31', '15' ], 
    [ '04', 'c7', '23', 'c3', '18', '96', '05', '9a', '07', '12', '80', 'e2', 'eb', '27', 'b2', '75' ], 
    [ '09', '83', '2c', '1a', '1b', '6e', '5a', 'a0', '52', '3b', 'd6', 'b3', '29', 'e3', '2f', '84' ], 
    [ '53', 'd1', '00', 'ed', '20', 'fc', 'b1', '5b', '6a', 'cb', 'be', '39', '4a', '4c', '58', 'cf' ], 
    [ 'd0', 'ef', 'aa', 'fb', '43', '4d', '33', '85', '45', 'f9', '02', '7f', '50', '3c', '9f', 'a8' ], 
    [ '51', 'a3', '40', '8f', '92', '9d', '38', 'f5', 'bc', 'b6', 'da', '21', '10', 'ff', 'f3', 'd2' ], 
    [ 'cd', '0c', '13', 'ec', '5f', '97', '44', '17', 'c4', 'a7', '7e', '3d', '64', '5d', '19', '73' ], 
    [ '60', '81', '4f', 'dc', '22', '2a', '90', '88', '46', 'ee', 'b8', '14', 'de', '5e', '0b', 'db' ], 
    [ 'e0', '32', '3a', '0a', '49', '06', '24', '5c', 'c2', 'd3', 'ac', '62', '91', '95', 'e4', '79' ], 
    [ 'e7', 'c8', '37', '6d', '8d', 'd5', '4e', 'a9', '6c', '56', 'f4', 'ea', '65', '7a', 'ae', '08' ], 
    [ 'ba', '78', '25', '2e', '1c', 'a6', 'b4', 'c6', 'e8', 'dd', '74', '1f', '4b', 'bd', '8b', '8a' ], 
    [ '70', '3e', 'b5', '66', '48', '03', 'f6', '0e', '61', '35', '57', 'b9', '86', 'c1', '1d', '9e' ], 
    [ 'e1', 'f8', '98', '11', '69', 'd9', '8e', '94', '9b', '1e', '87', 'e9', 'ce', '55', '28', 'df' ], 
    [ '8c', 'a1', '89', '0d', 'bf', 'e6', '42', '68', '41', '99', '2d', '0f', 'b0', '54', 'bb', '16' ], 
]

# Матриця зворотного перетворення
reverse_rijndael = [
    [ '52', '09', '6a', 'd5', '30', '36', 'a5', '38', 'bf', '40', 'a3', '9e', '81', 'f3', 'd7', 'fb' ], 
    [ '7c', 'e3', '39', '82', '9b', '2f', 'ff', '87', '34', '8e', '43', '44', 'c4', 'de', 'e9', 'cb' ], 
    [ '54', '7b', '94', '32', 'a6', 'c2', '23', '3d', 'ee', '4c', '95', '0b', '42', 'fa', 'c3', '4e' ], 
    [ '08', '2e', 'a1', '66', '28', 'd9', '24', 'b2', '76', '5b', 'a2', '49', '6d', '8b', 'd1', '25' ], 
    [ '72', 'f8', 'f6', '64', '86', '68', '98', '16', 'd4', 'a4', '5c', 'cc', '5d', '65', 'b6', '92' ], 
    [ '6c', '70', '48', '50', 'fd', 'ed', 'b9', 'da', '5e', '15', '46', '57', 'a7', '8d', '9d', '84' ], 
    [ '90', 'd8', 'ab', '00', '8c', 'bc', 'd3', '0a', 'f7', 'e4', '58', '05', 'b8', 'b3', '45', '06' ], 
    [ 'd0', '2c', '1e', '8f', 'ca', '3f', '0f', '02', 'c1', 'af', 'bd', '03', '01', '13', '8a', '6b' ], 
    [ '3a', '91', '11', '41', '4f', '67', 'dc', 'ea', '97', 'f2', 'cf', 'ce', 'f0', 'b4', 'e6', '73' ], 
    [ '96', 'ac', '74', '22', 'e7', 'ad', '35', '85', 'e2', 'f9', '37', 'e8', '1c', '75', 'df', '6e' ], 
    [ '47', 'f1', '1a', '71', '1d', '29', 'c5', '89', '6f', 'b7', '62', '0e', 'aa', '18', 'be', '1b' ], 
    [ 'fc', '56', '3e', '4b', 'c6', 'd2', '79', '20', '9a', 'db', 'c0', 'fe', '78', 'cd', '5a', 'f4' ], 
    [ '1f', 'dd', 'a8', '33', '88', '07', 'c7', '31', 'b1', '12', '10', '59', '27', '80', 'ec', '5f' ], 
    [ '60', '51', '7f', 'a9', '19', 'b5', '4a', '0d', '2d', 'e5', '7a', '9f', '93', 'c9', '9c', 'ef' ], 
    [ 'a0', 'e0', '3b', '4d', 'ae', '2a', 'f5', 'b0', 'c8', 'eb', 'bb', '3c', '83', '53', '99', '61' ], 
    [ '17', '2b', '04', '7e', 'ba', '77', 'd6', '26', 'e1', '69', '14', '63', '55', '21', '0c', '7d' ],
]

###################################################################################################################################################################

# Пряма та зворотна таблиця трансмутації
# 
#  1 2 3 4 5 6 7 8 
# 
#  4 1 3 8 7 5 6 2
# 
P = [4, 1, 3, 8, 7, 5, 6, 2]
P_reverse = [2, 8, 3, 1, 6, 7, 5, 4]

# Функція що виконує трансмутацію
def permute(P, arr):
    arr = list(arr)
    return ''.join([arr[i - 1] for i in P])

# Цикл меню
while True:
        print("\nГоловне меню:")
        print("1. Зашифрувати S-Блоком")
        print("2. Розшифрувати S-Блоком")
        print("3. Зашифрувати P-блоком")
        print("4. Розшифрувати P-блоком")
        print("5. Вихід")
        
        choice = input("Виберіть дію (1-5): ")

        if choice == '1':
            # Ця опція трансформує число спочатку в шістнадцяткове, далі перетворює його на координати матриці, де отримує зашифроване шістнадцяткове число,
            # яке переводиться в двійкове та виводиться на екран
            num = input("\nВведіть 8-бітне число: ")
            num = binary_to_hex(num)
            num = byte_to_coordinates(num)
            print("Зашифрований блок:",hex_to_bin(forward_rijndael[num[0]][num[1]]))
        elif choice == '2':
            # Опція аналогічна першій, використовується інша матриця
            num = input("\nВведіть зашифрований блок: ")
            num = binary_to_hex(num)
            num = byte_to_coordinates(num)
            print("Розшифрований блок:",hex_to_bin(reverse_rijndael[num[0]][num[1]]))
        elif choice == '3':
            # Використовується функція для перестановки бітів з прямою таблицею перестановки
            num = input("\nВведіть 8-бітне число: ")
            print("Зашифрований блок:", permute(P, num))
        elif choice == '4':
            # Аналогічно 3 опції, використовується функція зворотньої перестановки
            num = input("\nВведіть зашифрований блок: ")
            print("Розшифрований блок:", permute(P_reverse, num))
        elif choice == '5':
            print("Вихід з програми...")
            break
        else:
            print("Невірний вибір, спробуйте ще раз.")