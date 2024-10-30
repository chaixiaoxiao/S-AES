# S-AES
A simple implementation of the S-AES.
## 一、项目简介
Simplified Advanced Encryption Standard (S-AES) 是一种简化版本的高级加密标准（AES）算法，用于加密和解密数据。本程序提供了一个基于 S-AES算法的加解密功能。

## 二、算法原理
S-AES算法是一种简化的AES加密算法实现，它通过以下几个关键步骤来实现数据的加密和解密：

1. **密钥扩展**：将初始密钥扩展成多轮使用的子密钥，使用轮常量（Rcon）和S盒（Sbox）来生成每一轮的密钥。
2. **初始轮密钥添加**：将扩展出的第一轮密钥与初始状态矩阵进行异或操作，开始加密过程。
3. **多轮加密**：每一轮加密包括以下步骤：
   - **字节替换（SubBytes）**：使用S盒对状态矩阵中的每个字节进行替换。
   - **行移位（ShiftRows）**：对状态矩阵的行进行循环移位。
   - **列混淆（MixColumns）**：在Galois域上对状态矩阵的列进行复杂的数学运算，增加数据的混淆性。
   - **轮密钥添加（AddRoundKey）**：将当前轮的密钥与状态矩阵进行异或操作。
4. **最后一轮加密**：最后一轮加密省略列混淆步骤，只进行字节替换、行移位和轮密钥添加。
5. **解密过程**：解密是加密的逆过程，包括逆向的字节替换、行移位、列混淆和轮密钥添加，使用逆S盒（InvSbox）和逆轮常量进行操作。

## 三、关键代码实现
1. **加密函数（encrypt）**
   ```python
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
    ```
2. **解密函数（decrypt）**
   ```python
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
   ```
3. **字节替换（sub_bytes）**
 ```python
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

   ```
4. **Galois 域加法和乘法（gf_4_addition 和 gf_4_multiply）**
 ```python
def gf_4_addition(a, b):
    modulus = 0b10011
    return a ^ b


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

   ```
5. **列混淆（mix_columns）**
 ```python
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
   ```
6. **密钥扩展（key_expansion）**
 ```python
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

   ```
7. **轮密钥添加（add_round_key）**
```python
   def add_round_key(state, key_schedule, rnd):
    for col in range(nk):
        s0 = state[0][col] ^ binary_array_to_int(key_schedule[2 * rnd + col][:4])
        s1 = state[1][col] ^ binary_array_to_int(key_schedule[2 * rnd + col][4:])

        state[0][col] = s0
        state[1][col] = s1

    return state
 ```

## 四、项目测试
   
**本组编程是基于四bit为一组，16比特划分为4组进行加解密的，结果呈现也将以四bit为一组形式呈现。**
1. **第1关：基本测试**： 根据S-AES算法编写和调试程序，提供GUI解密支持用户交互。输入可以是16bit的数据和16bit的密钥，输出是16bit的密文。

 [![image](https://imgur.la/images/2024/10/30/image5041fd833a17cad3.md.png)](https://imgur.la/image/image.CyRKN)
 [![image](https://imgur.la/images/2024/10/30/image38542db652f124d2.md.png)](https://imgur.la/image/image.CyzkQ)


经测试，用户可以通过输入明文和密钥得到密文，也可以输入密文和密钥得到明文，结果相一致。

3. **第2关：交叉测试**：考虑到是"算法标准"，所有人在编写程序的时候需要使用相同算法流程和转换单元(替换盒、列混淆矩阵等)，以保证算法和程序在异构的系统或平台上都可以正常运行。设有A和B两组位同学(选择相同的密钥K)；则A、B组同学编写的程序对明文P进行加密得到相同的密文C；或者B组同学接收到A组程序加密的密文C，使用B组程序进行解密可得到与A相同的P。
  
[![image](https://imgur.la/images/2024/10/30/image751d1b4d14cfdf9e.md.png)](https://imgur.la/image/image.CygAU)
[![image](https://imgur.la/images/2024/10/30/image1b9e762a897a67cc.md.png)](https://imgur.la/image/image.CyvKz)
   
4. **第3关：扩展功能**：虑到向实用性扩展，加密算法的数据输入可以是ASII编码字符串(分组为2 Bytes)，对应地输出也可以是ACII字符串(很可能是乱码)。


[![image](https://imgur.la/images/2024/10/30/image8f00d3acde194f51.md.png)](https://imgur.la/image/image.CyIfZ)


5. **第4关：多重加密**
     - **3.4.1** 双重加密将S-AES算法通过双重加密进行扩展，分组长度仍然是16 bits，但密钥长度为32 bits。
 
 [![image](https://imgur.la/images/2024/10/30/image9816bce78f9101ef.md.png)](https://imgur.la/image/image.Cy3Oa)
[![image](https://imgur.la/images/2024/10/30/imagefb2e4f07fe8ce35f.md.png)](https://imgur.la/image/image.Cyukq)
     - **3.4.2** 中间相遇攻击：假设你找到了使用相同密钥的明、密文对(一个或多个)，请尝试使用中间相遇攻击的方法找到正确的密钥Key(K1+K2)。(给定明密文对后，暴力破解会得出很多对密钥，但是密钥数量比较多，没法全部展示，所以只显示输出了key1等于给定密钥1的密钥对)
 
   [![image](https://imgur.la/images/2024/10/30/imagee1e1aeab0ed1090c.md.png)](https://imgur.la/image/image.CMthU)
 
      - **3.4.2**  三重加密将S-AES算法通过三重加密进行扩展，下面两种模式选择一种完成：(1)按照32 bits密钥Key(K1+K2)的模式进行三重加密解密，(2)使用48bits(K1+K2+K3)的模式进行三重加解密。

[![image](https://imgur.la/images/2024/10/30/image6e5d5e203571cb04.md.png)](https://imgur.la/image/image.CyZm9)
[![image](https://imgur.la/images/2024/10/30/imagefdc96c02646e7bc3.md.png)](https://imgur.la/image/image.Cyfvb)

7. **第5关：工作模式**:基于S-AES算法，使用密码分组链(CBC)模式对较长的明文消息进行加密。注意初始向量(16 bits) 的生成，并需要加解密双方共享。在CBC模式下进行加密，并尝试对密文分组进行替换或修改，然后进行解密，请对比篡改密文前后的解密结果。

[![image](https://imgur.la/images/2024/10/30/image7156ad6e5ea40b78.md.png)](https://imgur.la/image/image.CNrov)
[![image](https://imgur.la/images/2024/10/30/imagea284f0a278546a34.md.png)](https://imgur.la/image/image.CNSgy)

## 五、用户指南


#### 1. 功能概述
本程序提供以下四个主要功能：
- （1）对二进制文本进行加解密操作。
- （2）对 Ascii 编码下的字符文本进行加解密操作。
- （3）通过双重加密和三重加密的方式对文本进行加解密操作。
- （4）使用密码分组链(CBC)模式对较长的明文消息进行加解密操作。

#### 2. 使用方法
运行 GUI 界面里的 `choose()` 函数，可以展示 UI 界面，下面进行功能展示。
- 主页面：选择需要加解密的文本格式、二进制加解密、Ascii 编码字节文本加解密、多重加解密算法、CBC 密码链模式加密。
[![image](https://imgur.la/images/2024/10/30/imaged288dd61ea42dddc.md.png)](https://imgur.la/image/image.CNXIc)
[![image](https://imgur.la/images/2024/10/30/image84cd8e60a9fd42e2.md.png)](https://imgur.la/image/image.CNeEQ)


（其他界面可见上面测试部分）
#### 3. 加解密参数
- **密钥**：S-DES 算法使用一个 16 位密钥。确保输入正确的密钥以保证加密解密的一致性。
- **二进制文本**：二进制文本需要保证输入的文本符合二进制格式。
- **字符文本**：字符文本需要保证输入的文本符合 ASCII 码规定。
- **多重加密**：在加密时需要使用两个 16-bit 的密钥进行加解密操作。（注意两次输入密钥的先后顺序）
- **CBC**：给定 16-bit 密钥和初始化向量后，输入符合规定的明文即可进行加解密操作。

#### 4. 注意事项
- （1）确保密钥的安全性，不要将密钥泄露给其他人。
- （2）在使用加解密功能时，需要保证输入的文本符合相对应的格式，不然可能导致结果乱码或者无法加解密。
- （3）在对文本内容进行解密时，应使用本程序生成的密文，否则可能导致解密出的明文部分信息丢失的情况。
- （4）S-AES 算法通过简化密钥长度和加密轮数方便理解，但是加密能力有所不足，易被破解，不宜用于保密等级高的信息传输。

## 六、总结
本项目成功实现了S-AES加密算法，并提供了一个用户友好的图形用户界面（GUI），使得加密和解密过程更加直观和便捷。通过详细的算法描述和关键代码实现，项目满足了课程的基本要求，还通过了基本测试、交叉测试、扩展功能实现、多重加密和工作模式等相关测试。

## 七、开发团队
- **小组**：风雨无组
- **团队成员**：柴钰林、古渲宇、陈芳莹
- **单位**：重庆大学大数据与软件学院
