"""
Normal Chatting Encryptor

(NCE)

Copyright (C) 2022 HLHT Studio
"""
import hashlib
import random
import time

import basic.ifv as ifv
import base64
import basic.NCE.CodeSystem

NUM_LIST = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
LETTER = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
          'w', 'x', 'y', 'z']
LETTER_UP = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
             'V', 'W', 'X', 'Y', 'Z']
CODES = ['.', ',', '(', ')', '*', '&', '^', '%', '$', '#', '@', '!', '~', '`', '[', ']', '\\', '{', '}', '|', ':', ';',
         "'", '"', '<', '>', '?', '/', '-', '=', '_', '+', ' ']
LETTERS = LETTER + LETTER_UP
LETTER_NUM = list()
BASE64 = NUM_LIST + LETTERS + ["=", "+"]


class STR(str):
    def divide(self, amount=2):
        if amount > len(self):
            raise Exception
        num = 0
        final = []
        for i in range(amount):
            if i == amount - 1:
                final.append(self[round(num):])
            else:
                final.append(self[round(num):round(num + len(self) / amount)])
            num += len(self) / amount
        return final


def update_lm(seed: int):
    global LETTER_NUM
    LETTER_NUM = list()
    random.seed(seed)
    while True:
        cell = random.choice(LETTER + NUM_LIST + CODES + LETTER_UP)
        if cell not in LETTER_NUM:
            LETTER_NUM.append(cell)
        if len(LETTER_NUM) == len(LETTER + NUM_LIST + CODES + LETTER_UP):
            break


def num_to_letter(num: int):
    total = []
    nums = NUM_LIST + LETTER
    while True:
        total.append(nums[num % 36 - 1])
        num = (num - (num % 36)) // 36
        if num == 0:
            break
    total.reverse()
    if total[0] == "0":
        del total[0]
    final = ""
    for i in total:
        final += i
    return final


def check_same(original_list: list, item: str):
    # sample of i (num, "value")
    for i in original_list:
        if str(i[-1]).startswith(item) or item.startswith(str(i[-1])):
            return True

    return False


def create_key(string: str, total: list):
    hash_key = hashlib.sha256(string=string.encode()).hexdigest()

    hash_num = ""

    for i in hash_key:
        hash_num += str((NUM_LIST + LETTER).index(i))
    hash_num = int(hash_num)
    update_lm(hash_num)

    key_list = dict()

    for i in total:
        try_time = 0
        ranges = 3
        while True:
            rand = num_to_letter(rand_size(random.randint(ranges, ranges+4),
                                           LETTER_NUM.index(i) + hash_num + len(total) + try_time))
            item_list = list(key_list.items())
            repeat = False
            for item in key_list.items():
                if any([check_same(item_list, rand), "3714" in rand, rand in "3714"]):
                    try_time += 1
                    if try_time % 2 == 0:
                        ranges += 1
                    repeat = True
                    break
            if repeat:
                continue
            key_list[i] = rand
            break

    return key_list


def rand_size(size: int, seed=random.randint(0, 10000)):
    random.seed(seed)
    key1 = (10 ** size) - 1
    key2 = 10 ** (size - 1)
    final = random.randint(key2, key1)
    return final


def encryption(string: str):
    if len(string) == 0:
        return ""

    key_head = ifv.str(string.splitlines()[0])
    while len(key_head) > 16:
        key_head = key_head.divide(2)[0]

    string64 = base64.b64encode(string.encode())
    total_str = list()
    for i in string64.decode():
        if i not in total_str:
            total_str.append(i)

    key = create_key(key_head, total_str)

    head = base64.b64encode(key_head.encode()).decode()
    total = ""
    for i in total_str:
        total += i

    total = base64.b64encode(total.encode()).decode()

    body, key1, key2 = CodeSystem.randCodeW(f"{head}\n{total}", True)
    title = f"{key1}\n{key2}\n{body}"

    final = f"{title}\n"
    for i in string64.decode():
        final += key[i]

    return final


def encryption_key(string: str, key: str):
    if len(string) == 0:
        return ""

    string64 = base64.b64encode(string.encode())

    key = create_key(base64.b64encode(key.encode()).decode(), BASE64)

    final = f""
    for i in string64.decode():
        final += key[i]

    return final


def encryption_b(string: bytes):
    if len(string) == 0:
        return b""

    string = base64.b64encode(string).decode()

    key_head = ifv.str(string.splitlines()[0])
    while len(key_head) > 16:
        key_head = ifv.str(key_head.divide(2)[0])

    string64 = base64.b64encode(string.encode())
    total_str = list()
    for i in string64.decode():
        if i not in total_str:
            total_str.append(i)

    key = create_key(key_head, total_str)

    head = base64.b64encode(key_head.encode()).decode()
    total = ""
    for i in total_str:
        total += i

    total = base64.b64encode(total.encode()).decode()

    body, key1, key2 = CodeSystem.randCodeW(f"{head}\n{total}", True)
    title = f"{key1}\n{key2}\n{body}"

    final = f"{title}\n"
    for i in string64.decode():
        final += key[i]

    return final


def encryption_b_key(string: bytes, key: str):
    if len(string) == 0:
        return b""

    string = base64.b64encode(string).decode()

    string64 = base64.b64encode(string.encode())

    key = create_key(base64.b64encode(key.encode()).decode(), BASE64)

    final = f""
    for i in string64.decode():
        final += key[i]

    return final


def decryption(string: str):
    head_body = [f"{string.splitlines()[2]}\n", string.splitlines()[3]]
    key1 = string.splitlines()[0]
    key2 = string.splitlines()[1]
    head = CodeSystem.randCodeR(head_body, key1, key2)
    key_head = base64.b64decode(head.splitlines()[0]).decode()
    total = base64.b64decode(head.splitlines()[1]).decode()
    texts = string.splitlines()[4]

    total_str = []
    for i in total:
        total_str.append(i)

    en_key = create_key(key_head, total_str)

    key = {}
    for i in en_key.keys():
        key[en_key[i]] = i

    final = ""
    temp = ""
    for i in texts:
        temp += i
        if temp in key.keys():
            final += key[temp]
            temp = ""
    final = base64.b64decode(final.encode()).decode()

    return final


def decryption_key(string: str, key: str):
    texts = string

    en_key = create_key(base64.b64encode(key.encode()).decode(), BASE64)

    key = {}
    for i in en_key.keys():
        key[en_key[i]] = i

    final = ""
    temp = ""
    for i in texts:
        temp += i
        if temp in key.keys():
            final += key[temp]
            temp = ""

    final = base64.b64decode(final.encode()).decode()

    return final


def decryption_b(string: str):
    head_body = [f"{string.splitlines()[2]}\n", string.splitlines()[3]]
    key1 = string.splitlines()[0]
    key2 = string.splitlines()[1]
    head = CodeSystem.randCodeR(head_body, key1, key2)
    key_head = base64.b64decode(head.splitlines()[0]).decode()
    total = base64.b64decode(head.splitlines()[1]).decode()
    texts = string.splitlines()[4]

    total_str = []
    for i in total:
        total_str.append(i)

    en_key = create_key(key_head, total_str)

    key = {}
    for i in en_key.keys():
        key[en_key[i]] = i

    final = ""
    temp = ""
    for i in texts:
        temp += i
        if temp in key.keys():
            final += key[temp]
            temp = ""
    final = base64.b64decode(base64.b64decode(final.encode()))

    return final


def decryption_b_key(string: str, key: str):
    texts = string

    en_key = create_key(base64.b64encode(key.encode()).decode(), BASE64)

    key = {}
    for i in en_key.keys():
        key[en_key[i]] = i

    final = ""
    temp = ""
    for i in texts:
        temp += i
        if temp in key.keys():
            final += key[temp]
            temp = ""
    final = base64.b64decode(base64.b64decode(final.encode()))

    return final


if __name__ == "__main__":
    password = input("Password:")
    uid = str(int(hashlib.sha256(password.encode()).hexdigest(), base=16))
    # with open("C:\\Users\\HoldWind\\Desktop\\test.jpg", "rb") as file:
    #     byte = file.read()
    # now = time.time()
    # num_key = round((uid + now) * (uid ** 0.5))
    # now_key = str(num_key)
    # en = encryption_b_key(byte, now_key)
    # de = decryption_b_key(en, now_key)
    # with open("C:\\Users\\HoldWind\\Desktop\\test2.jpg", "wb") as file:
    #     file.write(de)
    print(encryption_key("cdfxHLHT2013", "3714")[:14])
    while True:
        inp = input("Original: ")
        # now = time.time()
        # num_key = round((uid + now) * (uid ** 0.5))
        # now_key = str(num_key)
        en = encryption_key(inp, uid)
        print(f"Encrypted: {en}")
        de = decryption_key(en, uid)
        print(f"Decrypted: {de}")
