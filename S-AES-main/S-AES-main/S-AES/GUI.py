import binascii
import numpy as np
import S_AES
import test
import time
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from test import find_keys
from test import int_to_arr
from test import arr_to_int


def spl_bin(input):
    cip = []
    for i in range(len(input)):
        cip.append(int(input[i]))
    return cip


def spl_bin1(input):
    cip = []
    input = str(input).split(',')
    for i in range(len(input)):
        cip.append(int(input[i]))
    print(cip)
    return cip


def choose():
    def change1():
        root0.destroy()
        one()

    def change2():
        root0.destroy()
        two()

    def change3():
        root0.destroy()
        three_1()

    def change4():
        root0.destroy()
        four()

    def change5():
        root0.destroy()
        five()

    # 创建主窗口
    root0 = tk.Tk()
    root0.title('S-AES系统')

    # 获取屏幕宽度和高度
    screen_width = root0.winfo_screenwidth()
    screen_height = root0.winfo_screenheight()

    # 计算窗口左上角坐标使其居中
    x = (screen_width - 400) // 2
    y = (screen_height - 600) // 2

    # 设置窗口大小和位置
    root0.geometry('400x550+{}+{}'.format(x, y))

    # 创建一个Frame来容纳按钮，并使其在窗口中垂直居中
    frame = tk.Frame(root0)
    frame.pack(expand=True, fill=tk.BOTH)
    # 添加背景图片
    background_image = Image.open("background.jpeg")  # 替换成你的背景图片文件路径
    background_image = background_image.resize((400, 550), Image.LANCZOS)  # 调整大小
    background_photo = ImageTk.PhotoImage(background_image)
    background_label = tk.Label(frame, image=background_photo)
    background_label.place(relwidth=1, relheight=1)

    # 创建并设置按钮的外观
    btn01 = tk.Button(frame, text="二进制加解密", command=change1, font=('宋体', 15), width=20, height=2)
    btn01.pack(pady=25, padx=3, anchor='center')

    btn02 = tk.Button(frame, text="字符加解密", command=change2, font=('宋体', 15), width=20, height=2)
    btn02.pack(pady=25, padx=3, anchor='center')

    btn03 = tk.Button(frame, text="多重加解密", command=change3, font=('宋体', 15), width=20, height=2)
    btn03.pack(pady=25, padx=3, anchor='center')

    btn04 = tk.Button(frame, text="中间相遇攻击", command=change4, font=('宋体', 15), width=20, height=2)
    btn04.pack(pady=25, padx=3, anchor='center')

    btn05 = tk.Button(frame, text="CBC加解密", command=change5, font=('宋体', 15), width=20, height=2)
    btn05.pack(pady=25, padx=3, anchor='center')

    root0.mainloop()


def one():
    def encrypt():
        k = spl_bin(str(entry.get()))
        pla = spl_bin1(str(en1.get()))
        
        crypted_part = S_AES.encrypt(pla, k)
        print(crypted_part)
        messagebox.showinfo("密文",crypted_part)

    def solve():
        k = spl_bin(str(entry.get()))
        crypted_part = spl_bin1(str(en2.get()))
        d = S_AES.decrypt(crypted_part, k)
        print(d)
        messagebox.showinfo("明文",d)

    def back():
        root1.destroy()
        choose()

    # 创建主窗口
    root1 = tk.Tk()
    root1.title('二进制加解密')

    # 获取屏幕宽度和高度
    screen_width = root1.winfo_screenwidth()
    screen_height = root1.winfo_screenheight()

    # 计算窗口左上角坐标使其居中
    x = (screen_width - 400) // 2
    y = (screen_height - 600) // 2

    # 设置窗口大小和位置
    root1.geometry('400x600+{}+{}'.format(x, y))

    # 添加背景图片
    background_image = Image.open("background.jpeg")
    background_image = background_image.resize((400, 600), Image.LANCZOS)  # 调整大小
    background_photo = ImageTk.PhotoImage(background_image)
    background_label = tk.Label(root1, image=background_photo)
    background_label.place(relwidth=1, relheight=1)

    # 创建文本变量
    v1 = tk.StringVar()

    # 创建输入框
    # 创建文本变量
    v1 = tk.StringVar()
    lab00 = tk.Label(root1, text='你的密钥(16bit)', bg='#E3CF57', font=('宋体', 12))
    lab00.place(x=130, y=10)
    # 创建输入框并设置字体和大小
    entry = tk.Entry(root1, textvariable=v1, font=('宋体', 12), width=40)
    v1.set("0010110101010101")
    entry.place(x=35, y=50)

    # 创建标签并设置字体、大小和背景颜色
    lab01 = tk.Label(root1, text='你的明文(16bit)', bg='#E3CF57', font=('宋体', 12))
    lab01.place(x=130, y=100)

    # 创建明文输入框并设置字体和大小
    en1 = tk.Entry(root1, font=('宋体', 12), width=40)
    en1.place(x=35, y=140)

    # 创建加密按钮，设置字体、大小和背景颜色
    button1 = tk.Button(root1, text="加密", command=encrypt, font=('宋体', 15), bg='#873324', width=20, height=2)
    button1.place(x=100, y=190)

    # 创建标签并设置字体、大小和背景颜色
    lab02 = tk.Label(root1, text='你的密文(16bit)', bg='#E3CF57', font=('宋体', 12))
    lab02.place(x=130, y=300)

    # 创建密文输入框并设置字体和大小
    en2 = tk.Entry(root1, font=('宋体', 12), width=40)
    en2.place(x=35, y=340)

    # 创建解密按钮，设置字体、大小和背景颜色
    button2 = tk.Button(root1, text="解密", command=solve, font=('宋体', 15), bg='#873324', width=20, height=2)
    button2.place(x=100, y=390)

    # 创建返回按钮，设置字体、大小和背景颜色
    button3 = tk.Button(root1, text="返回", command=back, font=('宋体', 15), bg='#3D59AB', width=20, height=2)
    button3.place(x=100, y=490)

    root1.mainloop()


def two():
    def back():
        root2.destroy()
        choose()
    
    def encrypt():
        k = spl_bin(str(entry1.get()))
        pla = test.spl(str(en3.get()))
        print(pla)
        temp = []
        crypted_data = []
        for byte in pla:
            temp.append(test.binary_array_to_int(byte[:4]))
            temp.append(test.binary_array_to_int(byte[4:]))
            if len(temp) == 4:
                crypted_part = S_AES.encrypt(temp, k)
                crypted_data.extend(crypted_part)
                del temp[:]
        else:
            if 0 < len(temp) < 4:
                empty_spaces = 4 - len(temp)
                for i in range(empty_spaces - 1):
                    temp.append(0)
                    temp.append(1)
                    crypted_part = S_AES.decrypt(temp, k)
                    crypted_data.extend(crypted_part)

        print(crypted_data)
        messagebox.showinfo("明文",crypted_data)

    def solve():
        k = spl_bin(str(entry1.get()))
        crypted_data = spl_bin1(str(en4.get()))
        decrypted_data = []
        temp = []
        for byte in crypted_data:
            temp.append(byte)
            if len(temp) == 4:
                decrypted_part = S_AES.decrypt(temp, k)
                decrypted_data.extend(decrypted_part)
                del temp[:]
        else:
            if 0 < len(temp) < 4:
                empty_spaces = 4 - len(temp)
                for i in range(empty_spaces - 1):
                    temp.append(0)
                temp.append(1)
                decrypted_part = S_AES.encrypt(temp, k)
                decrypted_data.extend(decrypted_part)
        decrypted_str = ""
        for i in range(len(decrypted_data)):
            if i % 2 == 0:
                t = 16 * decrypted_data[i] + decrypted_data[i + 1]
                decrypted_str += chr(t)

        print(decrypted_str)
        messagebox.showinfo("明文",decrypted_str)

    root2 = tk.Tk()
    root2.title('字符加解密')

    # 获取屏幕宽度和高度
    screen_width = root2.winfo_screenwidth()
    screen_height = root2.winfo_screenheight()

    # 计算窗口左上角坐标使其居中
    x = (screen_width - 400) // 2
    y = (screen_height - 600) // 2

    # 设置窗口大小和位置
    root2.geometry('400x600+{}+{}'.format(x, y))

    # 添加背景图片
    background_image = Image.open("background.jpeg")
    background_image = background_image.resize((400, 600), Image.LANCZOS)  # 调整大小
    background_photo = ImageTk.PhotoImage(background_image)
    background_label = tk.Label(root2, image=background_photo)
    background_label.place(relwidth=1, relheight=1)

    # 创建文本变量
    v1 = tk.StringVar()

    # 创建输入框
    # 创建文本变量
    v1 = tk.StringVar()
    lab00 = tk.Label(root2, text='你的密钥', bg='#E3CF57', font=('宋体', 12))
    lab00.place(x=160, y=10)
    # 创建输入框并设置字体和大小
    entry1 = tk.Entry(root2, textvariable=v1, font=('宋体', 12), width=40)
    v1.set("0010110101010101")
    entry1.place(x=35, y=50)

    # 创建标签并设置字体、大小和背景颜色
    lab01 = tk.Label(root2, text='你的明文', bg='#E3CF57', font=('宋体', 12))
    lab01.place(x=160, y=100)

    # 创建明文输入框并设置字体和大小
    en3 = tk.Entry(root2, font=('宋体', 12), width=40)
    en3.place(x=35, y=140)

    # 创建加密按钮，设置字体、大小和背景颜色
    button1 = tk.Button(root2, text="加密", command=encrypt, font=('宋体', 15), bg='#873324', width=20, height=2)
    button1.place(x=100, y=190)

    # 创建标签并设置字体、大小和背景颜色
    lab02 = tk.Label(root2, text='你的密文', bg='#E3CF57', font=('宋体', 12))
    lab02.place(x=160, y=300)

    # 创建密文输入框并设置字体和大小
    en4 = tk.Entry(root2, font=('宋体', 12), width=40)
    en4.place(x=35, y=340)

    # 创建解密按钮，设置字体、大小和背景颜色
    button2 = tk.Button(root2, text="解密", command=solve, font=('宋体', 15), bg='#873324', width=20, height=2)
    button2.place(x=100, y=390)

    # 创建返回按钮，设置字体、大小和背景颜色
    button3 = tk.Button(root2, text="返回", command=back, font=('宋体', 15), bg='#3D59AB', width=20, height=2)
    button3.place(x=100, y=490)

    root2.mainloop()


def three_1():
    def back():
        root31.destroy()
        choose()

    def change1():
        root31.destroy()
        three_2()

    def change2():
        root31.destroy()
        three_3()
    # 创建主窗口
    root31 = tk.Tk()
    root31.title('多重加解密')

    # 获取屏幕宽度和高度
    screen_width = root31.winfo_screenwidth()
    screen_height = root31.winfo_screenheight()

    # 计算窗口左上角坐标使其居中
    x = (screen_width - 400) // 2
    y = (screen_height - 600) // 2

    # 设置窗口大小和位置
    root31.geometry('400x600+{}+{}'.format(x, y))

    # 设置主窗口背景颜色
    root31.configure(bg='blue')

    # 创建一个Frame来容纳按钮，并使其在窗口中垂直居中
    frame = tk.Frame(root31)
    frame.pack(expand=True, fill=tk.BOTH)
    # 添加背景图片
    background_image = Image.open("background.jpeg")
    background_image = background_image.resize((400, 600), Image.LANCZOS)  # 调整大小
    background_photo = ImageTk.PhotoImage(background_image)
    background_label = tk.Label(frame, image=background_photo)
    background_label.place(relwidth=1, relheight=1)


    # 创建并设置按钮的外观
    btn01 = tk.Button(frame, text="双重加解密", command=change1, font=('宋体', 15), bg='#873324', width=20, height=2)
    btn01.place(x=100, y=150)

    btn02 = tk.Button(frame, text="三重加解密", command=change2, font=('宋体', 15), bg='#873324', width=20, height=2)
    btn02.place(x=100, y=250)

    btn02 = tk.Button(frame, text="返回", command=back, font=('宋体', 15), bg='#3D59AB', width=20, height=2)
    btn02.place(x=100, y=450)

    root31.mainloop()


# 双重加密窗口
def three_2():
    def back():
        root32.destroy()
        three_1()

    def encrypt():
        key1 = spl_bin(str(entry1.get()))
        key2 = spl_bin(str(entry2.get()))
        pla = spl_bin1(str(en1.get()))
        cip = S_AES.encrypt(pla,key1)
        cip1 = S_AES.decrypt(cip,key2)
        print(cip1)
        messagebox.showinfo("密文",cip1)

    def solve():
        key1 = spl_bin(str(entry1.get()))
        key2 = spl_bin(str(entry2.get()))
        cip = spl_bin1(str(en2.get()))
        dec = S_AES.encrypt(cip,key2)
        dec1 = S_AES.decrypt(dec,key1)
        print(dec1)
        messagebox.showinfo("明文",dec1)

    root32 = tk.Tk()
    root32.title('双重加解密')

    # 获取屏幕宽度和高度
    screen_width = root32.winfo_screenwidth()
    screen_height = root32.winfo_screenheight()

    # 计算窗口左上角坐标使其居中
    x = (screen_width - 400) // 2
    y = (screen_height - 600) // 2

    # 设置窗口大小和位置
    root32.geometry('400x600+{}+{}'.format(x, y))

    # 添加背景图片
    background_image = Image.open("background.jpeg")
    background_image = background_image.resize((400, 600), Image.LANCZOS)  # 调整大小
    background_photo = ImageTk.PhotoImage(background_image)
    background_label = tk.Label(root32, image=background_photo)
    background_label.place(relwidth=1, relheight=1)

    # 创建文本变量
    v1 = tk.StringVar()

    # 创建输入框
    # 创建文本变量
    v1 = tk.StringVar()
    v2 = tk.StringVar()
    lab00 = tk.Label(root32, text='请分别输入两个密钥', bg='#E3CF57', font=('宋体', 12))
    lab00.place(x=120, y=10)
    # 创建输入框并设置字体和大小
    entry1 = tk.Entry(root32, textvariable=v1, font=('宋体', 12), width=40)
    v1.set("0010110101010101")
    entry1.place(x=35, y=50)

    entry2 = tk.Entry(root32, textvariable=v2, font=('宋体', 12), width=40)
    v2.set("0000111100001111")
    entry2.place(x=35, y=90)

    # 创建标签并设置字体、大小和背景颜色
    lab01 = tk.Label(root32, text='你的明文', bg='#E3CF57', font=('宋体', 12))
    lab01.place(x=160, y=150)

    # 创建明文输入框并设置字体和大小
    en1 = tk.Entry(root32, font=('宋体', 12), width=40)
    en1.place(x=35, y=190)

    # 创建加密按钮，设置字体、大小和背景颜色
    button1 = tk.Button(root32, text="加密", command=encrypt, font=('宋体', 15), bg='#873324', width=20, height=2)
    button1.place(x=100, y=230)

    # 创建标签并设置字体、大小和背景颜色
    lab02 = tk.Label(root32, text='你的密文', bg='#E3CF57', font=('宋体', 12))
    lab02.place(x=160, y=310)
    # 创建密文输入框并设置字体和大小
    en2 = tk.Entry(root32, font=('宋体', 12), width=40)
    en2.place(x=35, y=350)

    # 创建解密按钮，设置字体、大小和背景颜色
    button2 = tk.Button(root32, text="解密", command=solve, font=('宋体', 15), bg='#873324', width=20, height=2)
    button2.place(x=100, y=400)

    # 创建返回按钮，设置字体、大小和背景颜色
    button3 = tk.Button(root32, text="返回", command=back, font=('宋体', 15), bg='#3D59AB', width=20, height=2)
    button3.place(x=100, y=490)

    root32.mainloop()


# 三重加密窗口
def three_3():
    def back():
        root33.destroy()
        three_1()

    def encrypt():
        key1 = spl_bin(str(entry1.get()))
        key2 = spl_bin(str(entry2.get()))
        pla = spl_bin1(str(en1.get()))
        cip = S_AES.encrypt(pla,key1)
        cip = S_AES.decrypt(cip,key2)
        cip = S_AES.encrypt(cip,key1)
        print(cip)
        messagebox.showinfo("密文",cip)

    def solve():
        key1 = spl_bin(str(entry1.get()))
        key2 = spl_bin(str(entry2.get()))
        cip = spl_bin1(str(en2.get()))
        dec = S_AES.decrypt(cip,key1)
        dec = S_AES.encrypt(dec,key2)
        dec = S_AES.decrypt(dec,key1)
        print(dec)
        messagebox.showinfo("明文",dec)

    root33 = tk.Tk()
    root33.title('三重加解密')

    # 获取屏幕宽度和高度
    screen_width = root33.winfo_screenwidth()
    screen_height = root33.winfo_screenheight()

    # 计算窗口左上角坐标使其居中
    x = (screen_width - 400) // 2
    y = (screen_height - 600) // 2

    # 设置窗口大小和位置
    root33.geometry('400x600+{}+{}'.format(x, y))

    # 添加背景图片
    background_image = Image.open("background.jpeg")  # 替换成你的背景图片文件路径
    background_image = background_image.resize((400, 600), Image.LANCZOS)  # 调整大小
    background_photo = ImageTk.PhotoImage(background_image)
    background_label = tk.Label(root33, image=background_photo)
    background_label.place(relwidth=1, relheight=1)

    # 创建文本变量
    v1 = tk.StringVar()

    # 创建输入框
    # 创建文本变量
    v1 = tk.StringVar()
    v2 = tk.StringVar()
    lab00 = tk.Label(root33, text='请分别输入两个密钥',  bg='#E3CF57', font=('宋体', 12))
    lab00.place(x=120, y=10)

    # 创建输入框并设置字体和大小
    entry1 = tk.Entry(root33, textvariable=v1, font=('宋体', 12), width=40)
    v1.set("0010110101010101")
    entry1.place(x=35, y=50)

    entry2 = tk.Entry(root33, textvariable=v2, font=('宋体', 12), width=40)
    v2.set("0000111100001111")
    entry2.place(x=35, y=90)

    # 创建标签并设置字体、大小和背景颜色
    lab01 = tk.Label(root33, text='你的明文', bg='#E3CF57', font=('宋体', 12))
    lab01.place(x=160, y=150)

    # 创建明文输入框并设置字体和大小
    en1 = tk.Entry(root33, font=('宋体', 12), width=40)
    en1.place(x=35, y=190)

    # 创建加密按钮，设置字体、大小和背景颜色
    button1 = tk.Button(root33, text="加密", command=encrypt, font=('宋体', 15), bg='#873324', width=20, height=2)
    button1.place(x=100, y=230)

    # 创建标签并设置字体、大小和背景颜色
    lab02 = tk.Label(root33, text='你的密文', bg='#E3CF57', font=('宋体', 12))
    lab02.place(x=160, y=310)

    # 创建密文输入框并设置字体和大小
    en2 = tk.Entry(root33, font=('宋体', 12), width=40)
    en2.place(x=35, y=350)

    # 创建解密按钮，设置字体、大小和背景颜色
    button2 = tk.Button(root33, text="解密", command=solve, font=('宋体', 15), bg='#873324', width=20, height=2)
    button2.place(x=100, y=400)

    # 创建返回按钮，设置字体、大小和背景颜色
    button3 = tk.Button(root33, text="返回", command=back, font=('宋体', 15), bg='#3D59AB', width=20, height=2)
    button3.place(x=100, y=490)

    root33.mainloop()


# 中间相遇攻击
def four():
    def back():
        root4.destroy()
        choose()

    def crack_keys():
        try:
            plain_text = list(map(int, entry_plain.get().split(',')))
            cipher_text = list(map(int, entry_cipher.get().split(',')))
            key_text1 = list(map(int, entry_key1.get().split(',')))
            start = time.time()
            possible_keys = find_keys(plain_text, cipher_text)
            end = time.time()
            key1 = arr_to_int(key_text1)
            filtered_results = [
                (pk[0], pk[1]) for pk in possible_keys if pk[0] == key1
            ]
            if filtered_results:
                results = "\n".join(f"{int_to_arr(pk[0])},  {int_to_arr(pk[1])}" for pk in filtered_results)
                messagebox.showinfo("破解结果", f"破解时间: {end - start:.2f}秒\n找到的密钥:\n{results}")
            else:
                messagebox.showinfo("破解结果", "未找到匹配的密钥。")

        except Exception as e:
            messagebox.showerror("错误", f"发生错误: {str(e)}")

    # 创建主窗口
    root4 = tk.Tk()
    root4.title('中间相遇攻击')

    screen_width = root4.winfo_screenwidth()
    screen_height = root4.winfo_screenheight()

    x = (screen_width - 400) // 2
    y = (screen_height - 600) // 2

    root4.geometry('400x450+{}+{}'.format(x, y))

    frame = tk.Frame(root4)
    frame.pack(expand=True, fill=tk.BOTH)

    background_image = Image.open("background.jpeg")
    background_image = background_image.resize((400, 450), Image.LANCZOS)
    background_photo = ImageTk.PhotoImage(background_image)
    background_label = tk.Label(frame, image=background_photo)
    background_label.place(relwidth=1, relheight=1)

    label_plain = tk.Label(frame, text="你的明文 (英文逗号分隔):", bg='#E3CF57', font=('宋体', 12), width=25)
    label_plain.place(x=100, y=10)
    entry_plain = tk.Entry(frame, font=('宋体', 12), width=30)
    entry_plain.place(x=80, y=50)

    label_cipher = tk.Label(frame, text="你的密文 (英文逗号分隔):", bg='#E3CF57', font=('宋体', 12), width=25)
    label_cipher.place(x=100, y=100)
    entry_cipher = tk.Entry(frame, font=('宋体', 12), width=30)
    entry_cipher.place(x=80, y=140)

    label_key1 = tk.Label(frame, text="你的密钥1(英文逗号分隔):", bg='#E3CF57', font=('宋体', 12), width=25)
    label_key1.place(x=100, y=190)
    entry_key1 = tk.Entry(frame, font=('宋体', 12), width=30)
    entry_key1.place(x=80, y=230)

    btn_crack = tk.Button(frame, text="中间相遇攻击", command=crack_keys, bg='#873324', font=('宋体', 15), width=20, height=2)
    btn_crack.place(x=100, y=280)

    button3 = tk.Button(frame, text="返回", command=back, font=('宋体', 15), bg='#3D59AB', width=20, height=2)
    button3.place(x=100, y=350)

    root4.mainloop()


def five():

    def back():
        root5.destroy()
        choose()

    def encrypt():
        key = spl_bin(str(entry.get()))
        IV = spl_bin1(str(entry2.get()))
        pla = test.spl(str(en1.get()))
        converted_list = []
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
        messagebox.showinfo("密文", encrypted_str)

    def solve():
        key = spl_bin(str(entry.get()))
        IV = spl_bin1(str(entry2.get()))
        converted_list = []
        pla = test.spl(str(en1.get()))
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

        platext = decrypt_cbc(ciphertext, key, IV)
        decrypted_str = ""
        for i in range(len(platext)):
            for j in range(len(platext[0])):
                if j % 2 == 0:
                    t = 16 * platext[i][j] + platext[i][j + 1]
                    decrypted_str += chr(t)
        print(decrypted_str)
        messagebox.showinfo("明文", decrypted_str)

    root5 = tk.Tk()
    root5.title('CBC加解密')

    # 获取屏幕宽度和高度
    screen_width = root5.winfo_screenwidth()
    screen_height = root5.winfo_screenheight()

    # 计算窗口左上角坐标使其居中
    x = (screen_width - 400) // 2
    y = (screen_height - 600) // 2

    # 设置窗口大小和位置
    root5.geometry('400x600+{}+{}'.format(x, y))

    # 添加背景图片
    background_image = Image.open("background.jpeg")
    background_image = background_image.resize((400, 600), Image.LANCZOS)  # 调整大小
    background_photo = ImageTk.PhotoImage(background_image)
    background_label = tk.Label(root5, image=background_photo)
    background_label.place(relwidth=1, relheight=1)

    # 创建文本变量
    v1 = tk.StringVar()

    # 创建输入框
    # 创建文本变量
    v1 = tk.StringVar()
    lab00 = tk.Label(root5, text='你的密钥', bg='#E3CF57', font=('宋体', 12))
    lab00.place(x=160, y=10)
    # 创建输入框并设置字体和大小
    entry = tk.Entry(root5, textvariable=v1, font=('宋体', 12), width=40)
    v1.set("0010110101010101")
    entry.place(x=35, y=50)

    v2 = tk.StringVar()
    lab000 = tk.Label(root5,text='请给定初始化向量', bg='#E3CF57', font=('宋体', 12))
    lab000.place(x=130, y=90)
    entry2 = tk.Entry(root5, textvariable=v2, font=('宋体', 12), width=40)
    v2.set("5,6,7,8")
    entry2.place(x=35, y=130)

    # 创建标签并设置字体、大小和背景颜色
    lab01 = tk.Label(root5, text='你的明文', bg='#E3CF57', font=('宋体', 12))
    lab01.place(x=160, y=170)

    # 创建明文输入框并设置字体和大小
    en1 = tk.Entry(root5, font=('宋体', 12), width=40)
    en1.place(x=35, y=210)

    # 创建加密按钮，设置字体、大小和背景颜色
    button1 = tk.Button(root5, text="加密", command=encrypt, font=('宋体', 15), bg='#873324', width=20, height=2)
    button1.place(x=100, y=260)

    # 创建标签并设置字体、大小和背景颜色
    lab02 = tk.Label(root5, text='你的密文', bg='#E3CF57', font=('宋体', 12))
    lab02.place(x=160, y=340)

    # 创建密文输入框并设置字体和大小
    en2 = tk.Entry(root5, font=('宋体', 12), width=40)
    en2.place(x=35, y=380)

    # 创建解密按钮，设置字体、大小和背景颜色
    button2 = tk.Button(root5, text="解密", command=solve, font=('宋体', 15), bg='#873324', width=20, height=2)
    button2.place(x=100, y=420)

    # 创建返回按钮，设置字体、大小和背景颜色
    button3 = tk.Button(root5, text="返回", command=back, font=('宋体', 15), bg='#3D59AB', width=20, height=2)
    button3.place(x=100, y=500)

    root5.mainloop()


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


if __name__ == '__main__':
    choose()
