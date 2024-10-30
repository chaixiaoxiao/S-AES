nb = 2  # 状态矩阵的列数。在 AES中，通常为 4，S_AES使用 2 进行简化
nr = 2  # 进行加密的轮数。在AES中，通常为 10 轮
nk = 2  # 密钥长度，以 32 位字为单位

# 字典，用于将十六进制符号转换为整数
hex_symbols_to_int = {'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15}

# 加密时使用的替换表
sbox = [
    [0x9, 0x4, 0xa, 0xb],
    [0xd, 0x1, 0x8, 0x5],
    [0x6, 0x2, 0x0, 0x3],
    [0xc, 0xe, 0xf, 0x7]
]
# 解密时使用的替换表
inv_sbox = [
    [0xa, 0x5, 0x9, 0xb],
    [0x1, 0x7, 0x8, 0xf],
    [0x6, 0x0, 0x2, 0x3],
    [0xc, 0x4, 0xd, 0xe]

]
#  轮常量，用于密钥扩展，帮助生成每一轮的子密钥
rcon = [[1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 0, 0]]


# 接收输入字节和密钥，执行加密操作
def encrypt(input_bytes, key):
    state = [[input_bytes[0], input_bytes[2]], [input_bytes[1], input_bytes[3]]]
    key_schedule = key_expansion(key)
    state = add_round_key(state, key_schedule, 0)
    rnd = 1
    state = sub_bytes(state)
    state = shift_rows(state)
    state = mix_columns(state)
    state = add_round_key(state, key_schedule, rnd)
    rnd += 1
    state = sub_bytes(state)
    state = shift_rows(state)
    state = add_round_key(state, key_schedule, rnd)
    output = [state[0][0], state[1][0], state[0][1], state[1][1]]

    return output


# 解密操作
def decrypt(cipher, key):
    state = [[cipher[0], cipher[2]], [cipher[1], cipher[3]]]

    key_schedule = key_expansion(key)
    state = add_round_key(state, key_schedule, nr)
    rnd = nr - 1
    state = shift_rows(state)
    state = sub_bytes(state, inv=True)
    state = add_round_key(state, key_schedule, rnd)
    state = mix_columns(state, inv=True)
    rnd -= 1
    state = shift_rows(state)
    state = sub_bytes(state, inv=True)
    state = add_round_key(state, key_schedule, rnd)

    output = [state[0][0], state[1][0], state[0][1], state[1][1]]

    return output


# 替换状态矩阵中的每个字节
def sub_bytes(state, inv=False):
    if inv == False:  # encrypt
        box = sbox
    else:  # decrypt
        box = inv_sbox

    for i in range(len(state)):
        for j in range(len(state[i])):
            binary_str1 = bin(state[i][j])[2:]
            binary_str1 = binary_str1.zfill(4)
            binary_array1 = [int(bit) for bit in binary_str1]
            row = 2 * binary_array1[0] + binary_array1[1]
            col = 2 * binary_array1[2] + binary_array1[3]
            box_elem = box[row][col]
            state[i][j] = box_elem

    return state


# 实现行移位操作
def shift_rows(state):
    temp = state[1][0]
    state[1][0] = state[1][1]
    state[1][1] = temp

    return state


# 实现 Galois 域的加法，使用异或运算
def gf_4_addition(a, b):
    modulus = 0b10011
    return a ^ b


# 实现 Galois 域的乘法，使用位移和模运算
def gf_4_multiply(a, b):
    modulus = 0b10011

    result = 0
    for _ in range(4):
        if b & 1:
            result ^= a
        a <<= 1
        if (a & 0b10000) != 0:
            a ^= modulus
        b >>= 1

    return result


# 对列进行混合操作
def mix_columns(state, inv=False):
    for i in range(nb):
        if inv == False:
            s0 = gf_4_addition(gf_4_multiply(1, state[0][i]), gf_4_multiply(4, state[1][i]))
            s1 = gf_4_addition(gf_4_multiply(4, state[0][i]), gf_4_multiply(1, state[1][i]))
        else:  # decryption
            s0 = gf_4_addition(gf_4_multiply(9, state[0][i]), gf_4_multiply(2, state[1][i]))
            s1 = gf_4_addition(gf_4_multiply(2, state[0][i]), gf_4_multiply(9, state[1][i]))

        state[0][i] = s0
        state[1][i] = s1

    return state


# 实现两个数组的逐位异或运算，确保长度相同
def xor_arrays(arr1, arr2):
    if len(arr1) != len(arr2):
        raise ValueError("数组长度不相同")

    result = [bit1 ^ bit2 for bit1, bit2 in zip(arr1, arr2)]
    return result


# 密钥扩展
def key_expansion(key):
    w0 = key[:8]
    w1 = key[8:]
    # 初始化存储生成密钥的列表
    expanded_key = [w0, w1]
    w_temp = w1[4:] + w1[:4]
    w_x1 = 2 * w_temp[0] + w_temp[1]
    w_y1 = 2 * w_temp[2] + w_temp[3]
    number1 = sbox[w_x1][w_y1]
    binary_str1 = bin(number1)[2:]
    binary_str1 = binary_str1.zfill(4)
    binary_array1 = [int(bit) for bit in binary_str1]
    w_x2 = 2 * w_temp[4] + w_temp[5]
    w_y2 = 2 * w_temp[6] + w_temp[7]
    number2 = sbox[w_x2][w_y2]
    binary_str2 = bin(number2)[2:]
    binary_str2 = binary_str2.zfill(4)
    binary_array2 = [int(bit) for bit in binary_str2]
    binary_array = binary_array1 + binary_array2
    w2 = xor_arrays(xor_arrays(w0, rcon[0]), binary_array)
    w3 = xor_arrays(w2, w1)
    w_temp = w3[4:] + w3[:4]
    w_x1 = 2 * w_temp[0] + w_temp[1]
    w_y1 = 2 * w_temp[2] + w_temp[3]
    number1 = sbox[w_x1][w_y1]
    binary_str1 = bin(number1)[2:]
    binary_str1 = binary_str1.zfill(4)
    binary_array1 = [int(bit) for bit in binary_str1]
    w_x2 = 2 * w_temp[4] + w_temp[5]
    w_y2 = 2 * w_temp[6] + w_temp[7]
    number2 = sbox[w_x2][w_y2]
    binary_str2 = bin(number2)[2:]
    binary_str2 = binary_str2.zfill(4)
    binary_array2 = [int(bit) for bit in binary_str2]
    binary_array = binary_array1 + binary_array2
    w4 = xor_arrays(xor_arrays(w2, rcon[1]), binary_array)
    w5 = xor_arrays(w3, w4)
    expanded_key.append(w2)
    expanded_key.append(w3)
    expanded_key.append(w4)
    expanded_key.append(w5)

    return expanded_key


# 将 4 位二进制数组转换为整数
def binary_array_to_int(binary_array):
    if len(binary_array) != 4:
        raise ValueError("二进制数组长度必须为4位")

    decimal_value = 0
    for bit in binary_array:
        decimal_value = (decimal_value << 1) | bit

    return decimal_value


# 将轮密钥添加到状态矩阵中
def add_round_key(state, key_schedule, rnd):
    for col in range(nk):
        s0 = state[0][col] ^ binary_array_to_int(key_schedule[2 * rnd + col][:4])
        s1 = state[1][col] ^ binary_array_to_int(key_schedule[2 * rnd + col][4:])

        state[0][col] = s0
        state[1][col] = s1

    return state
