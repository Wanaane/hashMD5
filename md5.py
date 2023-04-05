import math
import struct
import os
import hashlib

# Định nghĩa các hằng số
T = [int(2**32 * abs(math.sin(i+1))) & 0xFFFFFFFF for i in range(64)]
s = [7, 12, 17, 22] * 4 + [5, 9, 14, 20] * 4 + [4, 11, 16, 23] * 4 + [6, 10, 15, 21] * 4

# Định nghĩa các hàm trợ giúp
def left_rotate(x : int, y :int) -> int:
    return ((x << (y & 0xffffffff)) | ((x & 0xffffffff) >> (32 - (y & 0xffffffff)))) & 0xffffffff


def md5(data):
    # Khởi tạo biến
    a0 = 0x67452301
    b0 = 0xEFCDAB89
    c0 = 0x98BADCFE
    d0 = 0x10325476

    # Thêm padding
    data = bytearray(data)
    original_len = (8 * len(data))

    # Padding 1
    data.append(0x80)

    # Padding 0
    while len(data) % 64 != 56:
        data.append(0x00)

    # Padding length
    data += original_len.to_bytes(8, byteorder="little")

    # Tính toán hash value cho từng khối 64 byte
    hash_value = b""
    for i in range(0, len(data), 64):
        block = data[i:i+64]
        # Khởi tạo giá trị ban đầu của các biến
        a, b, c, d = a0, b0, c0, d0
        
        # Chia block dữ liệu thành các từ 32 bit
        words = struct.unpack("<16I", block)

        # Vòng lặp tính toán
        for i in range(64):
            if i < 16:
                f = (b & c) | ((~b) & d)
                g = i
            elif i < 32:
                f = (d & b) | ((~d) & c)
                g = (5 * i + 1) % 16
            elif i < 48:
                f = b ^ c ^ d
                g = (3 * i + 5) % 16
            else:
                f = c ^ (b | (~d))
                g = (7 * i) % 16

            temp = d
            d = c
            c = b
            b = (b + left_rotate((a + f + T[i] + words[g]), s[i])) & 0xffffffff
            a = temp

            # Cộng giá trị ban đầu với giá trị mới tính được
        a0 = (a0 + a) & 0xffffffff
        b0 = (b0 + b) & 0xffffffff
        c0 = (c0 + c) & 0xffffffff
        d0 = (d0 +d) & 0xffffffff

    hash_value = (a0.to_bytes(4, byteorder="little") + b0.to_bytes(4, byteorder="little") +
                 c0.to_bytes(4, byteorder="little") + d0.to_bytes(4, byteorder="little"))
    return hash_value.hex()





def main():
    os.system("cls")
    data = input("Nhap chuoi: ")
    data = data.encode("utf-8")

    hash_value1 = hashlib.md5(data).hexdigest()
    hash_value2 = md5(data)

    print("\nHashlib: " + hash_value1)
    print("\nMe:      " + hash_value2)

    
   

if __name__ == '__main__':
    main()
