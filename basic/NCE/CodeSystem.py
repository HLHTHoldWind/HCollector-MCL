import sys
import os

runpath = os.getcwd()
sys.path.append(f'{runpath}\\system\\Python\\Lib\\win32_python_mainlib.cdl')
from basic.ifv import *
from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter.constants import RIGHT, LEFT, Y, BOTH, END
from idlelib.colorizer import ColorDelegator, color_config
from idlelib.percolator import Percolator
import random as r, sys as sys, tkinter.ttk as ttk, tkinter.tix as tix
import zipfile
import math
import getpass
# import assets.languages.english as eng
# import assets.languages.pyccknn as pyc
# import assets.languages.schinese as schi
# import assets.languages.tchinese as tchi
# import assets.languages.japanese as jap
import base64 as b64

modTF = os.path.exists(f'{runpath}\\system\\adminMod.pyc')
if modTF:
    import adminMod as mod

# Codes
modes = ['Caesar', 'HlhtCode', 'RandomCode']
NUMLIST = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
LETTER = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
          'w', 'x', 'y', 'z']
LETTERUP = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
            'V', 'W', 'X', 'Y', 'Z']
CODES = ['.', ',', '(', ')', '*', '&', '^', '%', '$', '#', '@', '!', '~', '`', '[', ']', '\\', '{', '}', '|', ':', ';',
         "'", '"', '<', '>', '?', '/', '-', '=', '_', '+', ' ']
LETTERNUM = LETTER + NUMLIST + LETTERUP + CODES
user = getpass.getuser()
dataPath = f'C:\\Users\\{user}\\AppData\\Local\\HLHT\\Coder++\\locals'
# try:
#     lang = readINI(f'{dataPath}\\languages.ini', 'lang')
# except:
#     with open(f'{dataPath}\\languages.ini', 'w') as file:
#         file.write('[LANG]\n')
#         file.write('eng')
#     lang = readINI('locals\\languages.ini', 'lang')
# if lang == 'eng':
#     lang = eng
# elif lang == 'pyc':
#     lang = pyc
# elif lang == 'schi':
#     lang = schi
# elif lang == 'tchi':
#     lang = tchi
# elif lang == 'jap':
#     lang = jap


def caes(text, key):
    text = list(text)
    final = ''
    for i in text:
        if i.lower() == i:
            up = False
        else:
            up = True
        i = i.lower()
        old = locInList(i, LETTER)
        if old != None:
            listLen = len(LETTER) - 1
            if old + key > listLen:
                new = old + key - listLen - 1
            else:
                new = old + key
            new = LETTER[new]
        else:
            new = i
        if up:
            new = new.upper()
        final += new
    return final


def creatRandKey(num=95):
    keyint = list(str(randFromSize(num)))
    times = 0
    for i in keyint:
        if int(i) < 5:
            keyint[times] = r.randint(5, 9)
        times += 1
    keyfinal = []
    for i in keyint:
        keyfinal.append(str(randFromSize(int(i))))
    times = 0
    times2 = 0
    for i in keyfinal:
        key_loca = keyfinal
        for a in key_loca:
            if i in a or a in i:
                while i in a or a in i:
                    a = str(randFromSize(len(a)))
            keyfinal[times2] = a
            times2 += 1
        times2 = 0
        times += 1
    final = ''
    for i in keyfinal:
        final += i
    return keyint, final


def randCodeR(text, key1, key2):
    try:
        key1 = list(key1.strip())
    except:
        key1 = list(key1)
    key2 = list(str(key2))
    time1 = 0
    time2 = 0
    loca = ''
    final = ''
    key = []
    for i in key1:
        for a in range(int(i)):
            loca += key2.pop(0)
            time2 += 1
        key.append(loca)
        loca = ''
    loca = ''
    for i in text:
        i = list(i)
        for a in i:
            if a in NUMLIST:
                loca += a
            if loca in key:
                # # print(f"LEFTTER{len(LETTERNUM)}")
                final += LETTERNUM[locInList(loca, key)]
                loca = ''
            if a not in NUMLIST:
                final += a
                loca = ''
    return final


global trytime
trytime = 0
font_size = 10


def randCodeW(text, turnKey=False):
    text_old = ''
    trytime = 0
    for i in text:
        text_old += i
    while True:
        text = list(text_old)
        key11, key22 = creatRandKey()
        key1 = key11
        key2 = list(str(key22))
        time1 = 0
        time2 = 0
        loca = ''
        final = ''
        key = []
        for i in key1:
            for a in range(int(i)):
                loca += key2.pop(0)
                time2 += 1
            key.append(loca)
            loca = ''
        for i in text:
            i = list(i)
            for a in i:
                if a in LETTERNUM:
                    final += key[locInList(a, LETTERNUM)]
                else:
                    final += str(a)
        aaa = randCodeR(final, key11, key22)
        if aaa == text_old:
            break
        else:
            del final
            continue
    if turnKey:
        key1 = ''
        for i in key11:
            key1 += str(i)
        return final, key1, key22
    else:
        return final


def creatFileKey(file):
    try:
        with open(file, 'r') as file:
            texts = file.read()
        texts = list(texts)
    except:
        texts = list(str(file))
    total = []
    for i in texts:
        if i in total:
            pass
        else:
            total.append(str(i))
    key1, final1 = creatRandKey(len(total))
    return key1, final1, total


def HlhtCodeW(text, turnKey=False):
    text_old = ''
    for i in list(text):
        text_old += i
    while True:
        key11, key22, total = creatFileKey(text)
        key1 = key11
        key2 = list(str(key22))
        time1 = 0
        time2 = 0
        loca = ''
        final = ''
        key = []
        for i in key1:
            for a in range(int(i)):
                loca += key2.pop(0)
                time2 += 1
            key.append(loca)
            loca = ''
        for i in text:
            i = list(i)
            for a in i:
                if a in total:
                    final += key[locInList(a, total)]
                else:
                    final += str(a)
        aaa = HlhtCodeR(final, key11, key22, total)
        if aaa == text_old:
            break
        else:
            del final
            continue
    if turnKey:
        key1 = ''
        for i in key11:
            key1 += str(i)
        return final, key1, key22, total
    else:
        return final


def HlhtCodeR(text, key1, key2, codeList):
    try:
        key1 = list(key1.strip())
    except:
        key1 = list(key1)
    key2 = list(str(key2))
    time1 = 0
    time2 = 0
    loca = ''
    final = ''
    key = []
    for i in key1:
        for a in range(int(i)):
            loca += key2.pop(0)
            time2 += 1
        key.append(loca)
        loca = ''
    loca = ''
    for i in text:
        i = list(i)
        for a in i:
            if a in NUMLIST:
                loca += a
            if loca in key:
                final += codeList[locInList(loca, key)]
                loca = ''
            if a not in NUMLIST:
                final += a
                loca = ''
    return final


def AllR(file, retMode=False):
    file_first = file
    if checkFileType(file_first, '.cod') or checkFileType(file_first, '.code'):
        mode, final = CodR(file_first)
        global code_mode
        code_mode = 'code'
    else:
        code_mode = 'common'
        with open(file, 'r') as file:
            texts = file.readlines()
        ort = texts
        key = str(list(texts[0])[0])
        mode = str(list(texts[0])[1] + list(texts[0])[2] + list(texts[0])[3])
        key = locInList(key.lower(), LETTER)
        mode = caes(mode, key)
        key1 = texts[0]
        del texts[0]
        final = ''
        if mode.upper() == 'CAE':
            for i in texts:
                final += caes(i, key)
        if list(key1)[0] in NUMLIST and mode.upper() != 'HLH':
            mode = 'ran'
            key2 = texts[0]
            del texts[0]
            final = randCodeR(texts, key1, key2)
        if mode.upper() == 'HLH':
            mode = 'hlht'
            final = HlhtR(file_first)
        if mode.upper() == 'REV':
            mode = 'reve'
            final = ReverseR(file_first)
        if mode.upper() == 'TRA':
            mode = 'tran'
            final = TranR(file_first)
        if ort[0] in NUMLIST and modTF:
            mode = 'admin'
            final = mod.read(file_first)
    if retMode:
        return final, mode.lower(), code_mode
    return final


def CodR(file):
    with zipfile.ZipFile(file, 'r') as zipf:
        with zipf.open('key.key', 'r') as keyf:
            texts = keyf.readlines()
        with zipf.open('code.body', 'r') as bodyf:
            body = bodyf.readlines()
        key11 = texts[0].decode(encoding='ascii')
        key22 = texts[1].decode(encoding='ascii')
        del texts[0]
        del texts[0]
        aaa = str(randCodeR(texts[0].decode(encoding='ascii'), key11, key22))
        keyT = texts[1].decode(encoding='ascii')
        key = aaa[0]
        mode = aaa[1:4]
        key = locInList(key.lower(), LETTER)
        mode = caes(mode, key)
        key1 = texts[0]
        del texts[0]
        final = ''
        bodyy = ''
        for i in body:
            bodyy += i.decode(encoding='ascii')
        if mode.upper() == 'CAE':
            for i in bodyy:
                final += caes(str(i), key)
        if mode == 'ran':
            mode = 'ran'
            key1 = texts[0]
            key2 = texts[1]
            body.insert(0, key1)
            body.insert(1, key2)
            final = RandR(decodeList(body))
        if mode.upper() == 'HLH':
            mode = 'hlht'
            key1 = texts[0]
            key2 = texts[1]
            key3 = texts[2]
            key4 = texts[3]
            key5 = texts[4]
            key6 = texts[5]
            key7 = texts[6]
            key8 = texts[7]
            key9 = texts[8]
            body.insert(0, key1)
            body.insert(1, key2)
            body.insert(2, key3)
            body.insert(3, key4)
            body.insert(4, key5)
            body.insert(5, key6)
            body.insert(6, key7)
            body.insert(7, key8)
            body.insert(8, key9)
            final = HlhtR(decodeList(body))
        if mode.upper() == 'REV':
            mode = 'reve'
            body = decodeList(body)
            body.insert(0, keyT)
            final = ReverseR(text=body)
        if mode.upper() == 'TRA':
            mode = 'tran'
            body = decodeList(body)
            body.insert(0, keyT)
            final = TranR(text=body)

    return mode, final


def CodW(file, mode, texts, key1=None, key2=None, show=True):
    try:
        if not file.endswith('.cod') and not file.endswith('.code'):
            file += '.cod'
        texts = list(texts)
        key = r.randint(1, 25)
        keyfirst = key
        tail = ''
        for i in range(r.randint(1, 10)):
            tail += LETTER[r.randint(0, 25)]
        title = LETTER[key].upper() + caes('cae', inverse(key)) + tail + '\n'
        title2 = LETTER[key].upper() + caes('ran', inverse(key)) + tail + '\n'
        title3 = LETTER[key].upper() + caes('hlht', inverse(key)) + tail + '\n'
        title4 = LETTER[key].upper() + caes('reve', inverse(key)) + tail + '\n'
        title5 = LETTER[key].upper() + caes('tran', inverse(key)) + tail + '\n'
        with zipfile.ZipFile(file, 'w') as zipf:
            with zipf.open('key.key', 'w') as keyf:
                if mode.lower() == 'cae':
                    key = title
                    final, key1, key2 = randCodeW(key, turnKey=True)
                    keyf.write((key1 + '\n').encode(encoding='ascii'))
                    keyf.write((key2 + '\n').encode(encoding='ascii'))
                    keyf.write(key.encode(encoding='ascii'))
                elif mode.lower() == 'ran':
                    key = title2
                    final, key1, key2 = randCodeW(key, turnKey=True)
                    keyf.write((key1 + '\n').encode(encoding='ascii'))
                    keyf.write((key2 + '\n').encode(encoding='ascii'))
                    keyf.write(final.encode(encoding='ascii'))
                    key, final = RandW2(texts)
                    keyf.write(key.encode(encoding='ascii'))
                elif mode.lower() == 'hlht':
                    key = title3
                    final, key1, key2 = randCodeW(key, turnKey=True)
                    keyf.write((key1 + '\n').encode(encoding='ascii'))
                    keyf.write((key2 + '\n').encode(encoding='ascii'))
                    keyf.write(final.encode(encoding='ascii'))
                    key, final = HlhtW2(texts)
                    keyf.write(key.encode(encoding='ascii'))
                elif mode.lower() == 'reve':
                    key = title4
                    final, key1, key2 = randCodeW(key, turnKey=True)
                    keyf.write((key1 + '\n').encode(encoding='ascii'))
                    keyf.write((key2 + '\n').encode(encoding='ascii'))
                    keyf.write(final.encode(encoding='ascii'))
                    key, final = ReverseW2(texts)
                    keyf.write((key + '\n').encode(encoding='ascii'))
                elif mode.lower() == 'tran':
                    key = title5
                    final, key1, key2 = randCodeW(key, turnKey=True)
                    keyf.write((key1 + '\n').encode(encoding='ascii'))
                    keyf.write((key2 + '\n').encode(encoding='ascii'))
                    keyf.write(final.encode(encoding='ascii'))
                    key, final = TranW2(texts)
                    keyf.write((key + '\n').encode(encoding='ascii'))
            with zipf.open('code.body', 'w') as bodyf:
                if mode.lower() == 'cae':
                    body = caes(texts, inverse(keyfirst))
                    bodyf.write(body.rstrip().encode(encoding='ascii'))
                else:
                    bodyf.write(final.rstrip().encode(encoding='ascii'))
    except UnicodeEncodeError:
        showerror(title='Fatal Error',
                  message='UnicodeEncodeError:\nTranslation or Reverse modes in\n.cod file can\'t include\nNON-ENGLISH CHARACTER')
        showerror(title='Fatal Error', message='The document is corrupted.')

    # if show:
    # showinfo(title=lang.COMPLETED, message=lang.COMPLETED_WRITING_FILE)


def ApartR(file):
    keyloc = askopenfilename(title="OPEN_CODE_KEY", filetypes=[("Key Files", "*.key")])
    with open(keyloc, 'r') as keyf:
        texts = keyf.readlines()
    with open(file, 'r') as bodyf:
        body = bodyf.readlines()
    key11 = texts[0]
    key22 = texts[1]
    del texts[0]
    del texts[0]
    aaa = str(randCodeR(texts[0], key11, key22))
    keyT = texts[1]
    # # print(keyT)
    key = aaa[0]
    mode = aaa[1:4]
    key = locInList(key.lower(), LETTER)
    mode = caes(mode, key)
    key1 = texts[0]
    del texts[0]
    final = ''
    bodyy = ''
    for i in body:
        bodyy += i
    if mode.upper() == 'CAE':
        for i in bodyy:
            final += caes(str(i), key)
    if mode == 'ran':
        mode = 'ran'
        key1 = texts[0]
        key2 = texts[1]
        body.insert(0, key1)
        body.insert(1, key2)
        final = RandR(body)
    if mode.upper() == 'HLH':
        mode = 'hlht'
        key1 = texts[0]
        key2 = texts[1]
        key3 = texts[2]
        key4 = texts[3]
        key5 = texts[4]
        key6 = texts[5]
        key7 = texts[6]
        key8 = texts[7]
        key9 = texts[8]
        body.insert(0, key1)
        body.insert(1, key2)
        body.insert(2, key3)
        body.insert(3, key4)
        body.insert(4, key5)
        body.insert(5, key6)
        body.insert(6, key7)
        body.insert(7, key8)
        body.insert(8, key9)
        final = HlhtR(body)
    if mode.upper() == 'REV':
        mode = 'reve'
        body.insert(0, keyT)
        final = ReverseR(text=body)
    if mode.upper() == 'TRA':
        mode = 'tran'
        body.insert(0, keyT)
        final = TranR(text=body)
    code_mode = 'apart'
    return final, mode, code_mode


def ApartW(file, mode, texts, show=True):
    texts = list(texts)
    key = r.randint(1, 25)
    keyloc = asksaveasfilename(title="lang.SAVE_KEY", initialfile='Untitled.key', filetypes=[("Key Files", "*.key")])
    keyfirst = key
    tail = ''
    for i in range(r.randint(1, 10)):
        tail += LETTER[r.randint(0, 25)]
    title = LETTER[key].upper() + caes('cae', inverse(key)) + tail + '\n'
    title2 = LETTER[key].upper() + caes('ran', inverse(key)) + tail + '\n'
    title3 = LETTER[key].upper() + caes('hlht', inverse(key)) + tail + '\n'
    title4 = LETTER[key].upper() + caes('reve', inverse(key)) + tail + '\n'
    title5 = LETTER[key].upper() + caes('tran', inverse(key)) + tail + '\n'
    with open(keyloc, 'w') as keyf:
        if mode.lower() == 'cae':
            key = title
            final, key1, key2 = randCodeW(key, turnKey=True)
            keyf.write((key1 + '\n'))
            keyf.write((key2 + '\n'))
            keyf.write(key)
        elif mode.lower() == 'ran':
            key = title2
            final, key1, key2 = randCodeW(key, turnKey=True)
            keyf.write((key1 + '\n'))
            keyf.write((key2 + '\n'))
            keyf.write(final)
            key, final = RandW2(texts)
            keyf.write(key)
        elif mode.lower() == 'hlht':
            key = title3
            final, key1, key2 = randCodeW(key, turnKey=True)
            keyf.write((key1 + '\n'))
            keyf.write((key2 + '\n'))
            keyf.write(final)
            key, final = HlhtW2(texts)
            keyf.write(key)
        elif mode.lower() == 'reve':
            key = title4
            final, key1, key2 = randCodeW(key, turnKey=True)
            keyf.write((key1 + '\n'))
            keyf.write((key2 + '\n'))
            keyf.write(final)
            key, final = ReverseW2(texts)
            keyf.write(key + '\n')
        elif mode.lower() == 'tran':
            key = title5
            final, key1, key2 = randCodeW(key, turnKey=True)
            keyf.write((key1 + '\n'))
            keyf.write((key2 + '\n'))
            keyf.write(final)
            key, final = TranW2(texts)
            keyf.write(key + '\n')

    with open(file, 'w') as bodyf:
        if mode.lower() == 'cae':
            body = caes(texts, inverse(keyfirst))
            bodyf.write(body.rstrip())
        else:
            bodyf.write(final.rstrip())
    # if show:
    # showinfo(title=lang.COMPLETED, message=lang.COMPLETED_WRITING_FILE)


def TranW(file, loc, show=True, text=None):
    while True:
        try:
            with open(file, 'r') as file:
                texts = file.read()
        except:
            pass
        if text != None:
            texts = text
        ori = texts
        key = r.randint(1, 25)
        key2 = r.randint(3, 8)
        tail = ''
        for i in range(r.randint(1, 10)):
            tail += LETTER[r.randint(0, 25)]
        title = LETTER[key].upper() + caes('tran', inverse(key)) + tail + LETTER[key2]
        texts = list(texts)
        final = ''
        times = 0
        # print(key2)
        for i in range(key2):
            now = times
            while now <= len(texts):
                try:
                    final += texts[now]
                except:
                    pass
                now += key2
            times += 1
        with open(loc, 'w') as file:
            file.write(title + '\n')
            file.write(final)
        decoded = TranR(loc)
        if decoded != ori:
            continue
        else:
            break
    # if show:


def TranW2(texts, show=True, text=None):
    ori = texts
    key = r.randint(1, 25)
    key2 = r.randint(3, 8)
    tail = ''
    for i in range(r.randint(1, 10)):
        tail += LETTER[r.randint(0, 25)]
    title = LETTER[key].upper() + caes('tran', inverse(key)) + tail + LETTER[key2]
    texts = list(texts)
    final = ''
    times = 0
    # print(key2)
    for i in range(key2):
        now = times
        while now <= len(texts):
            try:
                final += texts[now]
            except:
                pass
            now += key2
        times += 1
    # print(title)
    return title, final


def TranR(file=None, text=None):
    if file is not None:
        with open(file, 'r') as file:
            texts = file.readlines()
    elif text is not None:
        texts = text
    else:
        return
    key = locInList(texts[0].rstrip()[-1], LETTER)
    # print(key)
    del texts[0]
    mid = ''
    for i in texts:
        mid += i
    # length = len(mid) / key
    # dotLoc = locInList('.', list(str(length)))
    # if str(length)[dotLoc+1] != 0: length = int(length)
    # else: length = int(length)-1
    # # print(length)
    # final = ''
    # times = 0
    # for i in range(length):
    # now = times
    # while now <= len(mid):
    # try:
    # final += mid[now]
    # except: pass
    # now += length
    # times += 1
    # # print(final)
    columns = int(math.ceil(len(mid) / float(key)))
    disabledBox = (columns * key) - len(mid)
    mid_mid = [''] * columns
    column = 0
    row = 0
    for i in mid:
        mid_mid[column] += i
        column += 1
        if (column == columns) or (column == columns - 1 and row >= key - disabledBox):
            column = 0
            row += 1
    final = ''
    for i in mid_mid:
        final += i
    return final


def ReverseW(file, loc, show=True, text=None):
    try:
        with open(file, 'r') as file:
            texts = file.read()
    except:
        pass
    if text != None:
        texts = text
    key = r.randint(1, 25)
    tail = ''
    for i in range(r.randint(1, 10)):
        tail += LETTER[r.randint(0, 25)]
    title = LETTER[key].upper() + caes('reve', inverse(key)) + tail
    texts = list(texts)
    final = ''
    for i in range(len(texts)):
        final += texts[-1]
        del texts[-1]
    with open(loc, 'w') as file:
        file.write(title + '\n')
        file.write(final)
    # if show:
    # showinfo(title=lang.COMPLETED, message=lang.COMPLETED_WRITING_FILE)


def ReverseW2(text, show=True):
    texts = text
    key = r.randint(1, 25)
    tail = ''
    for i in range(r.randint(1, 10)):
        tail += LETTER[r.randint(0, 25)]
    title = LETTER[key].upper() + caes('reve', inverse(key)) + tail
    texts = list(texts)
    final = ''
    for i in range(len(texts)):
        final += texts[-1]
        del texts[-1]
    return title, final


def ReverseR(file=None, text=None):
    if file is not None:
        with open(file, 'r') as file:
            texts = file.readlines()
    elif text is not None:
        texts = text
    else:
        return
    del texts[0]
    mid = ''
    for i in texts:
        mid += i
    mid = list(mid)
    final = ''
    for i in range(len(mid)):
        final += mid[-1]
        del mid[-1]
    return final


def CaesarW(file, loc, show=True, text=None):
    try:
        with open(file, 'r') as file:
            texts = file.read()
    except:
        pass
    if text != None:
        texts = text
    key = r.randint(1, 25)
    tail = ''
    for i in range(r.randint(1, 10)):
        tail += LETTER[r.randint(0, 25)]
    title = LETTER[key].upper() + caes('cae', inverse(key)) + tail
    final = title + '\n'
    with open(loc, 'w') as file:
        file.write(final)
        times = 0
        for i in texts:
            if times == len(texts) - 1:
                file.write(caes(i, inverse(key)).rstrip())
            else:
                file.write(caes(i, inverse(key)))
            times += 1
    # if show:
    # showinfo(title=lang.COMPLETED, message=lang.COMPLETED_WRITING_FILE)


def CaesarR(file):
    with open(file, 'r') as file:
        texts = file.readlines()
    key = str(list(texts[0])[0])
    key = locInList(key.lower(), LETTER)
    del texts[0]
    final = ''
    for i in texts:
        final += caes(i, key)
    return final


def RandR(file):
    try:
        with open(file, 'r') as file:
            texts = file.readlines()
    except:
        texts = file
    key1 = texts[0]
    key2 = texts[1]
    del texts[0]
    del texts[0]
    final = ''
    for i in texts:
        final += randCodeR(i, key1, key2)
    return final


def RandW(file, loc, show=True, text=None):
    try:
        with open(file, 'r') as file:
            texts = file.readlines()
    except:
        pass
    if text != None:
        texts = text
    key = r.randint(1, 25)
    tail = ''
    body, key1, key2 = randCodeW(texts, turnKey=True)
    final = str(key1) + '\n' + str(key2) + '\n'
    with open(loc, 'w') as file:
        file.write(final)
        file.write(body.rstrip())
    # if show:
    # showinfo(title=lang.COMPLETED, message=lang.COMPLETED_WRITING_FILE)


def HlhtR(file):
    try:
        with open(file, 'r') as file:
            texts = file.readlines()
    except:
        texts = file
    # # print(texts[3])
    # if type(texts)==type([]):
    # texts[3]=splitLines(texts[3],True)
    del texts[0]
    key1 = texts[1]
    key2 = texts[2]
    key3 = texts[4]
    key4 = texts[5]
    tette = list(randCodeR(texts[3].rstrip(), key3, key4))
    total = list(randCodeR(texts[0], key1, key2))
    letter = []
    for i in tette:
        letter.append(int(i))
    altotal = []
    for i in letter:
        ttt = ''
        for a in range(i):
            ttt += total.pop(0)
        altotal.append(chr(int(ttt)))
    total = altotal
    del texts[0]
    del texts[0]
    del texts[0]
    del texts[0]
    del texts[0]
    del texts[0]
    key1 = texts[0]
    key2 = texts[1]
    del texts[0]
    del texts[0]
    final = HlhtCodeR(texts, key1, key2, total)
    return final


def HlhtW(file, loc, show=True, text=None):
    try:
        with open(file, 'r') as file:
            texts = file.readlines()
    except:
        pass
    if text != None:
        texts = text
    key = r.randint(1, 25)
    tail = ''
    for i in range(r.randint(1, 10)):
        tail += LETTER[r.randint(0, 25)]
    title = LETTER[key].upper() + caes('hlht', inverse(key)) + tail
    final = title + '\n'
    body, key1, key2, total = HlhtCodeW(texts, turnKey=True)
    ttt = ''
    ttx = []
    for i in total:
        ttt += str(ord(str(i)))
        txx = str(len(str(ord(str(i)))))
        ttx.append(txx)
    txx = ''
    for i in ttx:
        txx += i
    aaa, bbb, ccc = randCodeW(str(ttt), True)
    ddd, eee, fff = randCodeW(str(txx), True)
    final = title + '\n' + aaa + '\n' + bbb + '\n' + ccc + '\n' + ddd + '\n' + eee + '\n' + fff + '\n' + str(
        key1) + '\n' + str(key2) + '\n'
    with open(loc, 'w') as file:
        file.write(final)
        file.write(body.rstrip('\r\n'))
    # if show:
    # showinfo(title=lang.COMPLETED, message=lang.COMPLETED_WRITING_FILE)


def HlhtW2(texts, show=True, text=None):
    key = r.randint(1, 25)
    tail = ''
    for i in range(r.randint(1, 10)):
        tail += LETTER[r.randint(0, 25)]
    title = LETTER[key].upper() + caes('hlht', inverse(key)) + tail
    final = title + '\n'
    body, key1, key2, total = HlhtCodeW(texts, turnKey=True)
    ttt = ''
    ttx = []
    for i in total:
        ttt += str(ord(str(i)))
        txx = str(len(str(ord(str(i)))))
        ttx.append(txx)
    txx = ''
    for i in ttx:
        txx += i
    aaa, bbb, ccc = randCodeW(str(ttt), True)
    ddd, eee, fff = randCodeW(str(txx), True)
    final = title + '\n' + aaa + '\n' + bbb + '\n' + ccc + '\n' + ddd + '\n' + eee + '\n' + fff + '\n' + str(
        key1) + '\n' + str(key2) + '\n'
    return final, body.rstrip('\r\n')


def RandW2(texts, show=True, text=None):
    key = r.randint(1, 25)
    tail = ''
    body, key1, key2 = randCodeW(texts, turnKey=True)
    final = str(key1) + '\n' + str(key2) + '\n'
    return final, body.rstrip()


def statistics(texts):
    texts = texts.lower()
    final = {}
    for i in LETTER:
        final[i] = texts.count(i)

    return final


def findTheMost(texts):
    total = statistics(texts)
    final = sorted(total.items(), key=lambda item: item[1], reverse=True)

    return final


def CaesarBrute(texts):
    optionE = ""
    optionA = ""
    optionT = ""
    optionO = ""
    optionTotal = []

    statis = findTheMost(texts)
    letterE = statis[0]
    letterA = statis[1]
    letterT = statis[1]
    letterO = statis[3]

    def solve(cryphLetter, Letter, text):
        key = locInList(Letter, LETTER) - locInList(cryphLetter, LETTER)
        final = caes(text, 26 + key) if key < 0 else caes(text, key)
        return final

    # Solve E
    optionE = solve(letterE[0], "e", texts)
    key = locInList("e", LETTER) - locInList(letterE[0], LETTER)
    keyE = 26 + key if key < 0 else key

    # Solve T
    optionT = solve(letterE[0], "t", texts)
    key = locInList("t", LETTER) - locInList(letterE[0], LETTER)
    keyT = 26 + key if key < 0 else key

    # Solve A
    optionA = solve(letterE[0], "a", texts)
    key = locInList("a", LETTER) - locInList(letterE[0], LETTER)
    keyA = 26 + key if key < 0 else key

    # Solve O
    optionO = solve(letterE[0], "o", texts)
    key = locInList("o", LETTER) - locInList(letterE[0], LETTER)
    keyO = 26 + key if key < 0 else key

    for i in range(26):
        if i not in [keyE, keyA, keyT, keyO]:
            optionTotal.append(caes(texts, i))

    final = [optionE, optionA, optionT, optionO]
    final += optionTotal

    return final


def HlhtR2(file):
    try:
        with open(file, 'r') as file:
            texts = file.readlines()
    except:
        texts = file
    # # print(texts[3])
    # if type(texts)==type([]):
    # texts[3]=splitLines(texts[3],True)
    key1 = texts[1]
    key2 = texts[2]
    key3 = texts[4]
    key4 = texts[5]
    tette = list(randCodeR(texts[3].rstrip(), key3, key4))
    total = list(randCodeR(texts[0], key1, key2))
    letter = []
    for i in tette:
        letter.append(int(i))
    altotal = []
    for i in letter:
        ttt = ''
        for a in range(i):
            ttt += total.pop(0)
        altotal.append(chr(int(ttt)))
    total = altotal
    del texts[0]
    del texts[0]
    del texts[0]
    del texts[0]
    del texts[0]
    del texts[0]
    key1 = texts[0]
    key2 = texts[1]
    del texts[0]
    del texts[0]
    final = HlhtCodeR(texts, key1, key2, total)
    return final


def UpperKey(data):
    b64Key = str(b64.b64encode(data.encode()))
    final = ""
    for i in b64Key:
        final += str(ord(i))
    return final


def LowerKey(data):
    final = str(ord(data))
    return final


def NumKey(data):
    strData = chr(data * 3714)
    b64Key = str(b64.b64encode(strData.encode()))
    final = ""
    for i in b64Key:
        final += str(ord(i))
    return final


def AllKey(data):
    if data in ["\n", "\r"]:
        final = data
    else:
        b64Key = str(b64.b64encode(data.encode()))
        final = ""
        for i in b64Key:
            final += str(ord(i))
    return final


def ChatEncrypt(s):
    b64en = b64.b64encode(s.encode())
    # if len(str(b64en)) < 13:
    #     final = HlhtW2(s)
    # else:
    keys = b64en.decode()[0:13]
    key = []
    for i in keys:
        if i in LETTERUP:
            key.append(UpperKey(i))
        elif i in LETTER:
            key.append(LowerKey(i))
        elif i in NUMLIST:
            key.append(NumKey(int(i)))
        else:
            key.append(AllKey(i))
    keys = ""
    for i in key:
        keys += i

    key = keys

    total = []
    for i in s:
        if i in total or i in ["\n", "\r"]:
            pass
        else:
            total.append(str(i))
    totalKey = []
    randoms = r.SystemRandom()
    times = 0

    def _randFromSize(Tsize):
        key1 = (10 ** Tsize) - 1
        key2 = 10 ** (Tsize - 1)
        temp = randoms.randint(key2, key1)
        return temp

    sizes = ""
    for i in total:
        if i not in ["\n", "\r"]:
            size = int(key[times]) if int(key[times]) >= 4 else int(key[times]) * 2
            if size == 0:
                size = 4
            size = size if size >= 4 else size * 2
            while True:
                keyNow = str(_randFromSize(size))
                if keyNow not in totalKey:
                    con = False
                    for a in totalKey:
                        if keyNow in a:
                            con = True
                    if not con:
                        totalKey.append(keyNow)
                        sizes += str(size)
                        break
                    else:
                        continue
                else:
                    continue
        else:
            totalKey.append(i)
        times += 1
        if times > len(key):
            times = 0

    strTotalKey = ""
    for i in totalKey:
        strTotalKey += i

    keyDict = {}
    times = 0
    for i in totalKey:
        keyDict[total[times]] = i
        times += 1

    final = ""
    for i in s:
        if i not in ["\n", "\r"]:
            final += keyDict[i]
        else:
            final += i

    """Create Title-key"""
    b64Total = ""
    totals = ""
    for i in total:
        totals += i
    b64Total += b64.b64encode(totals.encode()).decode() + "\n"
    bTotal = b64Total
    b64Total += b64.b64encode(sizes.encode()).decode() + "\n"
    b64Total += b64.b64encode(strTotalKey.encode()).decode() + "\n"
    key, title = HlhtW2(b64Total)
    key = deleteUntil(key, "\n", "left")
    title = title.rstrip() + "\n"
    final = key + title + final

    return final


def ChatDecrypt(file):
    texts = file
    if isinstance(texts, str):
        texts = texts.splitlines(True)
    HlhtTitle = texts[:9]
    texts = texts[9:]
    HlhtTitle = HlhtR2(HlhtTitle)
    HlhtTitle = HlhtTitle.splitlines()
    totals = b64.b64decode(HlhtTitle[0].encode()).decode()
    key = b64.b64decode(HlhtTitle[1].encode()).decode()
    strTotalKey = b64.b64decode(HlhtTitle[2].encode()).decode()

    TotalKey = []
    for i in key:
        TotalKey.append(strTotalKey[:int(i)])
        strTotalKey = strTotalKey[int(i):]

    total = []
    for i in totals:
        total.append(i)
    KeyDict = {}
    times = 0
    for i in TotalKey:
        KeyDict[i] = total[times]
        times += 1

    final = ""
    nowDecode = ""
    text = ""
    for i in texts:
        text += i
    for i in text:
        nowDecode += i
        if nowDecode in list(KeyDict.keys()):
            final += KeyDict[nowDecode]
            nowDecode = ""
        elif nowDecode in ["\n", "\r"]:
            final += nowDecode
            nowDecode = ""

    return final.strip()


def deep_hlht(randed):
    if isinstance(randed, list):
        text = ""
        for i in randed:
            text += i
    elif isinstance(randed, str):
        text = randed
    else:
        return ""

    final = ""
    while True:
        while True:
            size = random.SystemRandom().randint(1, 5)
            part = text[:size]

            try:
                if "\n" in part:
                    part = "\n"
                    size = 1
                    final += part
                else:
                    chr(int(part)).encode()
                    final += chr(int(part))
                break
            except UnicodeEncodeError:
                continue

        text = text[size:]
        if len(text) == 0:
            break

    return final


def deep_read(text):
    final = ""
    for i in text:
        final += str(ord(i))
    return final


if __name__ == '__main__':
    part1, part2 = HlhtW2("Hello World!")
    total_part = part1+part2
    part1 = total_part.splitlines(True)[0]
    part2 = total_part.splitlines(True)[1:]

    print(deep_hlht(part2))
