import numpy as np
import S_AES
import time
import binascii


# 将输入字符串转换为二进制数组
def spl(input):
    transform = []
    for i in range(len(input)):
        transform.append(ord(input[i]))
    data = []
    for i in range(len(transform)):
        b = bin(transform[i]).replace('0b', '')
        b = b.zfill(8)
        for j in range(len(b)):
            data.append(int(b[j]))
    data1 = np.array(data)
    data1.resize((len(input), 8))
    return data1


# 将 4 位二进制数组转换为整数
def binary_array_to_int(binary_array):
    if len(binary_array) != 4:
        raise ValueError("二进制数组长度必须为4位")
    decimal_value = 0
    for bit in binary_array:
        decimal_value = (decimal_value << 1) | bit

    return decimal_value


print("二进制加解密测试：")
# 默认密钥
key = [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0]
# 常规加解密
pla = [0, 0, 0, 0]
crypted_part = S_AES.encrypt(pla, key)
d = S_AES.decrypt(crypted_part, key)
print(f"明文为：{pla}，密钥为：{key}，加密结果为：{crypted_part}")
print(f"密文为：{crypted_part}，密钥为：{key}，解密结果为：{d}")

# ascii加解密
print("字符加解密测试：")
pla_str = "abcd"
pla = spl(pla_str)
# 将每个字节的前4位和后4位分别转化为整数，并进行加密
temp = []
crypted_data = []
for byte in pla:
    temp.append(binary_array_to_int(byte[:4]))
    temp.append(binary_array_to_int(byte[4:]))
    if len(temp) == 4:
        crypted_part = S_AES.encrypt(temp, key)
        crypted_data.extend(crypted_part)
        del temp[:]
else:
    if 0 < len(temp) < 4:
        empty_spaces = 4 - len(temp)
        for i in range(empty_spaces - 1):
            temp.append(0)
        temp.append(1)
        crypted_part = S_AES.decrypt(temp, key)
        crypted_data.extend(crypted_part)
print(f"明文为：{pla_str}，密钥为：{key}，加密结果为：{crypted_data}")


# 对密文进行解密并恢复原字符串
decrypted_data = []
temp = []
for byte in crypted_data:
    temp.append(byte)
    if len(temp) == 4:
        decrypted_part = S_AES.decrypt(temp, key)
        decrypted_data.extend(decrypted_part)
        del temp[:]
else:
    if 0 < len(temp) < 4:
        empty_spaces = 4 - len(temp)
        for i in range(empty_spaces - 1):
            temp.append(0)
        temp.append(1)
        decrypted_part = S_AES.encrypt(temp, key)
        decrypted_data.extend(decrypted_part)
decrypted_str = ""
for i in range(len(decrypted_data)):
    if i % 2 == 0:
        t = 16 * decrypted_data[i] + decrypted_data[i + 1]
        decrypted_str += chr(t)
print(f"密文为：{crypted_data}，密钥为：{key}，解密结果为：{decrypted_str}")


# 双重加密
print("双重加解密测试：")
key1 = [0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
key2 = [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1]
pla = [10, 4, 7, 9]
# 加密
cip = S_AES.encrypt(pla, key1)
cip = S_AES.decrypt(cip, key2)
print(f"明文为：{pla}，密钥为：{key1}、{key2}，加密结果为：{cip}")
# 解密
dec = S_AES.encrypt(cip, key2)
dec = S_AES.decrypt(dec, key1)
print(f"密文为：{cip}，密钥为：{key1}、{key2}，解密结果为：{dec}")


# 暴力破解
# 整数转二进制数组
def int_to_binary_array(n):
    # 将整数转化为二进制字符串，然后填充零以达到指定的位数
    binary_str = bin(n)[2:].zfill(16)
    # 将二进制字符串转化为整数列表
    binary_array = [int(bit) for bit in binary_str]

    return binary_array


# 数组转整数
def arr_to_int(arr):
    sum = 0
    for i in range(len(arr)):
        sum += arr[i] * pow(2, 4 * (3 - i))
    return sum


def int_to_arr(n):
    arr = []
    for i in range(0, 4):
        arr.append(n // pow(2, 4 * (3 - i)))
        n = n % pow(2, 4 * (3 - i))
    return arr


def binary_search_first_column(sorted_2d_array, target):
    left, right = 0, len(sorted_2d_array) - 1

    while left <= right:
        mid = left + (right - left) // 2  # 防止整数溢出

        if sorted_2d_array[mid][0] == target:
            return mid
        elif sorted_2d_array[mid][0] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1  # 没有找到目标元素


def find_keys(known_plain, known_cipher):
    possible_keys = []
    encrypt_result = []
    for key1 in range(0, 65536):
        encrypt_result.append([arr_to_int(S_AES.encrypt(known_plain, int_to_binary_array(key1))), key1])
    sorted_list = sorted(encrypt_result, key=lambda x: x[0])
    for key2 in range(0, 65536):
        encrypt1 = arr_to_int(S_AES.encrypt(known_cipher, int_to_binary_array(key2)))
        pos = binary_search_first_column(sorted_list, encrypt1)
        if pos != -1:
            possible_keys.append([sorted_list[pos][1], key2])
    return possible_keys


# 密码分组链模式
# 加密函数（CBC模式）
def encrypt_cbc(plain_text, key, iv):
    ciphertext = []
    previous_block = iv

    for block in plain_text:
        # CBC模式下，每个明文块先与前一个密文块异或
        block = [a ^ b for a, b in zip(block, previous_block)]
        # 然后使用密钥进行加密
        encrypted_block = S_AES.encrypt(block, key)
        # 密文块添加到结果中
        ciphertext.append(encrypted_block)
        # 更新前一个密文块
        previous_block = encrypted_block

    return ciphertext


# 解密函数（CBC模式）
def decrypt_cbc(ciphertext, key, iv):
    plain_text = []
    previous_block = iv

    for block in ciphertext:
        # 使用密钥进行解密
        decrypted_block = S_AES.decrypt(block, key)
        # 在CBC模式下，解密后的块再与前一个密文块异或
        plain_block = [a ^ b for a, b in zip(decrypted_block, previous_block)]
        # 明文块添加到结果中
        plain_text.append(plain_block)
        # 更新前一个密文块
        previous_block = block

    return plain_text


key = [0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
IV = [5, 6, 7, 8]
pla_text = 'abcdefghijklmnopqrs'
pla = spl(pla_text)
converted_list = []
print(pla_text)
for i in range(0, len(pla), 2):
    if i + 1 < len(pla):
        combined_values = [
            int(''.join(map(str, pla[i, :4])), 2),
            int(''.join(map(str, pla[i, 4:])), 2),
            int(''.join(map(str, pla[i + 1, :4])), 2),
            int(''.join(map(str, pla[i + 1, 4:])), 2)
        ]
        converted_list.append(combined_values)
    else:
        combined_values = [
            int(''.join(map(str, pla[i, :4])), 2),
            int(''.join(map(str, pla[i, 4:])), 2),
            0,
            0
        ]
        converted_list.append(combined_values)

ciphertext = encrypt_cbc(converted_list, key, IV)
encrypted_str = ""
for i in range(len(ciphertext)):
    for j in range(len(ciphertext[0])):
        if j % 2 == 0:
            t = 16 * ciphertext[i][j] + ciphertext[i][j + 1]
            encrypted_str += chr(t)
print(encrypted_str)
platext = decrypt_cbc(ciphertext, key, IV)
decrypted_str = ""
for i in range(len(platext)):
    for j in range(len(platext[0])):
        if j % 2 == 0:
            t = 16 * platext[i][j] + platext[i][j + 1]
            decrypted_str += chr(t)
print(decrypted_str)

