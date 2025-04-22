"""
IFV is a module by HLHT Stuido

Copyright (C) 2021 HLHT Studio All Right Reserved

Latest version:final_1.1.0.

Download the later version from "http://www.hlht2013.org".

This is main py.

Another file "How to use.txt" can tell you what can it do.
"""
__version__ = "1.1.0"
import sys
from .version import *
sysver1 = sys.version_info[0]
sysver2 = sys.version_info[1]
sysver3 = sys.version_info[2]
#Import
import turtle as tur
import random
import time
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.scrolledtext as tkst
import zipfile
from idlelib.percolator import Percolator
from .pythagoras import *
from .WARS import *
from .COLOR import *
from idlelib.undo import *

# __all__ = ["IfvTkinter", "Servant", "hlht_title", "ivx", "print_e",
           # "print_lebyle","settlement_bar","seasons_colors","yin_yang",
           # "writing","python_servant","abs","round_e","randfloat",
           # "readINI","getItemInfo","getINI","writeInZip"]


#Variable
seasons = ['spring','summer','autumn','fall','winter']
yeno = ['yes','no']
servant_ans = ['play a math_game'
               ,'draw a yin&yang picture'
               ,'pour a cup of tea for you'
               ,"show i am cute"
               ,"nothing"
               ,"write a txt"]
NormalNumberListTotal = [0,1,2,3,4,5,6,7,8,9]
StrNormalNumberListTotal = ['0','1','2','3','4','5','6','7','8','9']
NumberPointInIfv = '.'
NUMLIST=['0','1','2','3','4','5','6','7','8','9']
LETTER=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
LETTERUP=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
def randFromSize(size):
    key1=(10**size)-1
    key2=10**(size-1)
    final=random.SystemRandom().randint(key2,key1)
    return final
def checkFileType(file, types):
    """Check the file is or not 'type'"""
    if types.startswith('.'):
        types=types[1:]
    if str(file).rstrip('.'+types)!=str(file):
        return True
    else:
        return False
def intList(data):
    data = list(data)
    final = []
    for i in data:
        i = int(i)
        final.append(i)
    return final
def floatList(data):
    data = list(data)
    final = []
    for i in data:
        i = float(i)
        final.append(i)
    return final
def strList(data):
    data = list(data)
    final = []
    for i in data:
        i = str(i)
        final.append(i)
    return final
def splitLines(string,keepLF=False):
    """Split string by lines"""
    aaa=string.split(sep='\r\n')
    bbb=string.split(sep='\n')
    if len(aaa)==1:
        final=bbb
        if keepLF:
            for i in final:
                if not i.endswith('\n') and i not in ['\n','\r','',None] and '\n' in string:
                    final[locInList(i,final)]=final[locInList(i,final)]+'\n'
    if '\r' in bbb[0]:
        final=aaa
        if keepLF:
            for i in final:
                if not i.endswith('\r\n') and i not in ['\n','\r','',None] and '\r\n' in string:
                    final[locInList(i,final)]=final[locInList(i,final)]+'\r\n'
    if string.endswith('\n'):
        del final[-1]
    if not string.endswith('\n'):
        final[-1]=final[-1].rstrip()
    return final
def decodeList(lists,decoding='ascii'):
    """Decode all items in list"""
    final=[]
    for i in lists:
        if type(i)==type(b'a'):
            final.append(i.decode(decoding))
        else:
            final.append(i)
    return final
def encodeList(lists,decoding='ascii'):
    """Encode all items in list"""
    final=[]
    for i in lists:
        if type(i)==type('a'):
            final.append(i.encode(decoding))
        else:
            final.append(i)
    return final
def makeMenu(master,name,function,fonts,lines,unders):
    times=0
    if lines!=None:
        lines=list(lines)
    menu=tk.Menu(master)
    for i in name:
        if lines!=None and times in lines:
            menu.add_separator()
        menu.add_command(label=i, underline=unders[times],
                         font=fonts, command=function[times])
        times+=1
    return menu
class ScrolledText(tk.Text):
    def __init__(self, master=None, **kw):
        global undo
        self.frame = tk.Frame(master)
        self.vbar = ttk.Scrollbar(self.frame)
        self.hbar = ttk.Scrollbar(self.frame,orient=tk.HORIZONTAL)
        self.vbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.hbar.pack(side=tk.BOTTOM, fill=tk.X)

        kw.update({'yscrollcommand': self.vbar.set})
        kw.update({'xscrollcommand': self.hbar.set})
        tk.Text.__init__(self, self.frame,wrap='none', **kw)
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.vbar['command'] = self.yview
        self.hbar['command'] = self.xview
        p = Percolator(self)
        undo = UndoDelegator()
        p.insertfilter(undo)
        self.undo_block_start=undo.undo_block_start
        self.undo_block_stop = undo.undo_block_stop
        self.undo_block_start()
        # Copy geometry methods of self.frame without overriding Text
        # methods -- hack!
        
        text_meths = vars(tk.Text).keys()
        methods = vars(tk.Pack).keys() | vars(tk.Grid).keys() | vars(tk.Place).keys()
        methods = methods.difference(text_meths)
        #print(methods)
        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self.frame, m))
                #print(setattr(self, m, getattr(self.frame, m)))

    def __str__(self):
        return str(self.frame)
class ScrolledText2(tk.Text):
    def __init__(self, master=None, **kw):
        self.frame = tk.Frame(master)
        self.vbar = ttk.Scrollbar(self.frame)
        self.hbar = ttk.Scrollbar(self.frame,orient=tk.HORIZONTAL)
        self.vbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.hbar.pack(side=tk.BOTTOM, fill=tk.X)

        kw.update({'yscrollcommand': self.vbar.set})
        kw.update({'xscrollcommand': self.hbar.set})
        tk.Text.__init__(self, self.frame,wrap='none', **kw)
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.vbar['command'] = self.yview
        self.hbar['command'] = self.xview
        # Copy geometry methods of self.frame without overriding Text
        # methods -- hack!
        
        text_meths = vars(tk.Text).keys()
        methods = vars(tk.Pack).keys() | vars(tk.Grid).keys() | vars(tk.Place).keys()
        methods = methods.difference(text_meths)
        #print(methods)
        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self.frame, m))
                #print(setattr(self, m, getattr(self.frame, m)))

    def __str__(self):
        return str(self.frame)
def IfvScrolledText(master=None,**keys):
    t = tk
    frame = t.Frame(master)
    vbar = ttk.Scrollbar(frame)
    hbar = ttk.Scrollbar(frame,orient=t.HORIZONTAL)
    vbar.pack(side=t.RIGHT, fill=t.Y)
    hbar.pack(side=t.BOTTOM, fill=t.X)
    text = t.Text(frame,wrap='none',**keys)
    text.pack(side='left',fill='both',expand=True)
    vbar['command']=text.yview
    hbar['command']=text.xview
    text['yscrollcommand'] = vbar.set
    text['xscrollcommand'] = hbar.set
    
    text_meths = vars(t.Text).keys()
    methods = vars(t.Pack).keys() | vars(t.Grid).keys() | vars(t.Place).keys()
    methods = methods.difference(text_meths)
    for m in methods:
        if m[0] != '_' and m != 'config' and m != 'configure':
            setattr(text, m, getattr(frame, m))
    return frame
def setStr(target):
    return target
def deleteUntil(string,key,side='right'):
    """Delete string until key"""
    try:
        strings=list(string)
        now='abbababababbbababbbababababab'
        if side=='right':
            while now!=key:
                now=strings[-1]
                del strings[-1]
        if side=='left':
            while now!=key:
                now=strings[0]
                del strings[0]
        final=''
        for i in strings:
            final+=i
    except:
        final=string
    return final
class ScrolledList(tk.Listbox):
    def __init__(self, master=None, **kw):
        self.frame = tk.Frame(master)
        self.vbar = ttk.Scrollbar(self.frame)
        self.hbar = ttk.Scrollbar(self.frame,orient=tk.HORIZONTAL)
        self.vbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.hbar.pack(side=tk.BOTTOM, fill=tk.X)

        kw.update({'yscrollcommand': self.vbar.set})
        kw.update({'xscrollcommand': self.hbar.set})
        tk.Listbox.__init__(self, self.frame, **kw)
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.vbar['command'] = self.yview
        self.hbar['command'] = self.xview
        # Copy geometry methods of self.frame without overriding Text
        # methods -- hack!
        
        text_meths = vars(tk.Listbox).keys()
        methods = vars(tk.Pack).keys() | vars(tk.Grid).keys() | vars(tk.Place).keys()
        methods = methods.difference(text_meths)
        #print(methods)
        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self.frame, m))
                #print(setattr(self, m, getattr(self.frame, m)))

    def __str__(self):
        return str(self.frame)
    
        
class IfvTkinter():
    """HLHT's Tkinter(C) package"""
    
    def __init__(self,master=None):
        self.master=master
        self.BAR=tk.Menu(self.master,relief=tk.RAISED,borderwidth=2)
    
    def scrollWin(self,width=None,height=None,text='',bg='white',font=None,textRe=False):
        """A scrolledtext window in Tkinter(C)"""
        master=self.master
        texts = ScrolledText(bg=bg,width=width,height=height,master=master,font=font)
        texts.insert('end',text)
        global undo
        if textRe:
            return texts,undo
        return texts
    def scrollWin2(self,width=None,height=None,text=None,bg='white',font=None,textRe=False):
        """A scrolledtext window in Tkinter(C)"""
        master=self.master
        texts = ScrolledText2(bg=bg,width=width,height=height,master=master,font=font)
        texts.insert('end',text)
        global undo
        if textRe:
            return texts,undo
        return texts
    def scrollList(self,width=None,height=None,bg='white',font=None):
        """A scrolledtext window in Tkinter(C)"""
        master=self.master
        texts = ScrolledList(master=master,bg=bg,width=width,height=height,font=font)
        return texts
    def displayMenu(self,text,font,fun_name,*functions,line=(None,),Punder=None,under=(None,)):
        """Add menu to display"""
        if len(fun_name)!=len(functions):
            raise LengthError(""+
                              "fun_name's length != functions' length.")
        if under==(None,):
            under=[]
            for i in range(len(fun_name)):
                under.append(0)
        under=tuple(under)
        master = self.master
        BAR=self.BAR
        BAR.add_cascade(menu=makeMenu(BAR,fun_name,functions,font,lines=line,unders=under),label=text, underline=Punder)
        self.master['menu'] = BAR
    

def write_sys_init():
    name_file = 'name.txt'
    __init = open(name_file,'a')
    __init.close()

def locInList(key,lists):
    times=0
    for i in lists:
        if key==i:
            return times
        times+=1
    return None

def inverse(num):
    return -1*num

pyth = Pythagoras()

#Definitions
def hlht_title():
    h_title = """
    HLHT Studio ©2021.  All Right Reserved.
    You CAN NOT copy this program by any way.
    You can call or e-mail us.
    TEL:+86-028-85469778
    E-mail:hlht2013@foxmail.com
    If you have any question,you can ask us at any time.
    By Hold Wind and Andy Long.
    """
    print(h_title)

def iv(num):
    if num<4:
        nnn=int(num)*'I'
        return nnn
    elif num==4:
        nnn='IV'
        return nnn
    elif num >4 and num<9:
        num=num-5
        nnn='V'+int(num)*'I'
        return nnn
    elif num==9:
        nnn='IX'
        return nnn
def ivx(num):
    """Accept a int and return this int's Roman numerals form.
    
    If this num is not a int, it will not output Error."""
    if type(num)!=type(1):
        try:
            num=int(num)
        except:
            pass
    num_list = list(str(num))
    for i in num_list:
        if i not in StrNormalNumberListTotal:
            raise IvxTypeError(''+
                               'Invalid parameter: num"'+
                               str(num)+'" expect an integer but got other.')
    num = int(num)
    if num<10:
        nnn=iv(num)
        return nnn
    elif 10<=num<20:
        num=num-10
        nnn=iv(num)
        nnn='X'+nnn
        return nnn
    else :
        chaos=num/10
        chaos=int(chaos)
        zhens=chaos*10
        num=num-zhens
        nnn=iv(num)
        nnn=chaos*'X'+nnn
        return nnn

    
def print_e(txt,times,line) :
    """Print (txt) for (times) times at first.
    Print (line) lines and every line's words will add 1."""
    for txts in range(line) :
        print(txt*times)
        times += 1

def print_lebyle(txt,times=0.1,English=True) :
    """Print (txt) and every-letter-print will wait for (times) seconds."""
    if English:
        for i in txt:
            print(i,end='',flush=True)
            time.sleep(times)
    else:
        for i in txt:
            print(i,end='',flush=True)
            time.sleep(times)
orderPrint = print_lebyle

def printUp(text):
    text=list(text)
    for i in text:
        now = ''
        times = 0
        if i in NUMLIST:
            while now!=i:
                now = NUMLIST[times]
                print(now,end='',flush=True)
                t.sleep(0.001)
                print('\b',end='',flush=True)
                times+=1
            print(i,end='',flush=True)
        elif i in LETTER:
            while now!=i:
                now = LETTER[times]
                print(now,end='',flush=True)
                t.sleep(0.001)
                print('\b',end='',flush=True)
                times+=1
            print(i,end='',flush=True)
        elif i in LETTERUP:
            while now!=i:
                now = LETTERUP[times]
                print(now,end='',flush=True)
                t.sleep(0.001)
                print('\b',end='',flush=True)
                times+=1
            print(i,end='',flush=True)
        else:
            print(i,end='',flush=True)

def settlement_bar():
    print('$',end='',flush=True)
    time.sleep(0.01)
    print('\b',end='',flush=True)
    print('%',end='',flush=True)
    time.sleep(0.01)
    print('\b',end='',flush=True)
    print('#',end='',flush=True)
    time.sleep(0.01)
    print('\b',end='',flush=True)
    print('&',end='',flush=True)
    time.sleep(0.01)
    print('\b',end='',flush=True)
    print('@',end='',flush=True)
    time.sleep(0.01)
    print('\b',end='',flush=True)
    print('£',end='',flush=True)
    time.sleep(0.01)
    print('\b',end='',flush=True)
    print('¾',end='',flush=True)
    time.sleep(0.01)
    print('\b',end='',flush=True)
    print('¥',end='',flush=True)
    time.sleep(0.01)
    print('\b',end='',flush=True)
    print('§',end='',flush=True)
    time.sleep(0.01)
    print('\b',end='',flush=True)
    print('█',end='',flush=True)
    time.sleep(0.01)

        
def seasons_colors() :
    """Ask the seasons to know what colors peoples like."""
    while True :
        color = str(input("What's your favorite season?"))
        colors = color.lower()
        
        if colors == seasons[0] :
            print('Oh,I know you must like green!')
        elif colors == seasons[1] :
            print('Oh,I know you must like red!')
        elif colors == seasons[2] :
            print('Oh,I know you must like gold!')
        elif colors == seasons[3] :
            print('Oh,I know you must like gold!')
        elif colors == seasons[4] :
            print('Oh,I know you must like white!')
        else :
            print("Oh,you don't know what is the seasons?")
            print("""
            Seasons are
            Spring
            Summer
            Autumn/Fall
            Winter
            Now you understand?
            """
            )
        
        again = input('Do you want to play again?(yes/no)')
        again = again.lower()
        if again == yeno[0]:
            pass
        elif again == yeno[1]:
            break
        else :
            print("""
            You're kidding me!
            I won't give you another chance!
            Let's play again!:)
            """
            )

def yin_yang (speed,big,small) :
    """(speed,big circle's size,small circle's size)drawing an ugly Yin&Yang picture."""
    #start
    tur.pensize(5)
    tur.speed(10)
    tur.ht()
    #black
    tur.up()
    tur.rt(90)
    tur.fd(big)
    tur.lt(90)
    tur.color('black','black')
    tur.down()
    tur.begin_fill()
    tur.circle(big,180)
    tur.circle(big/2,180)
    tur.rt(180)
    tur.circle(big/2,-180)
    tur.end_fill()
    #white
    tur.circle(big,-180)
    #white circle
    tur.up()
    tur.lt(90)
    tur.fd(big/2 + small)
    tur.rt(90)
    tur.down()
    tur.color('white','white')
    tur.begin_fill()
    tur.circle(small*-1)
    tur.end_fill()
    #black circle
    tur.up()
    tur.lt(90)
    tur.fd(big)
    tur.lt(90)
    tur.down()
    tur.color('black','black')
    tur.begin_fill()
    tur.circle(small)
    tur.end_fill()
    #end
    tur.up()
def writing(mode,file_name):
    if mode == 'w':
        with open("write down\\"+file_name,'w') as files:
            print("Let's write."+'If you done,write'+
                  '"I AM DONE"to exit and save.')
            while True :
                txt = str(input())
                if txt == 'I AM DONE' :
                    break
                else :
                    files.write(txt+'\n')
    elif mode == 'a' :
        with open('write down\\'+file_name,'a') as files:
            print("Let's write."+'If you are done,write'+
                  '"I AM DONE"to exit and save.')
            while True :
                txt = str(input())
                if txt == 'I AM DONE' :
                    break
                else :
                    files.write(txt+'\n')
    
class Servant() :
    """The python_servant's options."""
    
    def __init__(self,user) :
        self.name = user
        
    def play_game(self) :
        print("Let's play a game,"+self.name.title()+"!")
        remeaning = 3
        for i in range(3) :
            print(remeaning)
            remeaning -=1
            time.sleep(1)
        level = 0
        while True :
            xx = random.randint(1,100)
            yy = random.randint(1,100)
            if level <= 10 :
                print(xx,"+",yy,"=")
                z = int(input())
                a = (int(xx)+int(yy))
            elif level > 10 and level <= 50 :
                print(xx,"*",yy,"=")
                z = int(input())
                a = (int(xx)*int(yy))
            elif level > 50 :
                print(xx,"**",yy,"=")
                z = int(input())
                a = (int(xx)**int(yy))
                
            if z == a :
                print("Yes,you're right!"+self.name.title()+".")
                level += 1
                if level == 10 or level == 50 :
                    print("A Higher Level !")
            else :
                print("Oh,you have lost,"+self.name.title()+".")
            b = input("Try again? (yes/no)")
            b = b.lower()
            if b != 'yes' :
                print("OK!If you want to play again,tell me.")
                break
                
def pour_tea(user_name) :
    print("This is a cup of tea,general-"+user_name.title()+".")
    time.sleep(0.5)
            
        
            
        
def nothing___():
            pass

def writing_ing(user_name) :
        name_name = user_name.title()
        file = str(input("Which txt-file do you want to open?"))
        while True :
            ans = input("What mode do you want to open,"
                        +name_name+"?Covering or Adding?")
            if ans.lower() == 'covering' :
                ans = 'w'
                break
            elif ans.lower() == 'adding' :
                ans = 'a'
                break
            else :
                print("Your answer is not a mode,"
                      +name_name+",answer again,please.")         
        writing(ans,file)
        time.sleep(0.75)

def _final_(user_name) :
    print("OK,see you next time,"+user_name.title()+".")
    time.sleep(1)
            
#
def temp_1(name_file='name.txt') :
    name_load = open(name_file,"w")
    name = input("Who are you?  I'm ")
    name_load.write(name.title())
    name_load.close()
    while True :
        artist = input("OK,Do you like me or my mother(python)?"+
                       "   Answer Yes or No:")
        if artist.lower() == "yes" :
            print("Thanks for your answer,"+name.title()+".")
            break
        elif artist.lower() == "no" :
            print("Oh,that's fine,"+name.title()+".")
            break
        else :
            print("What did you say?")
            print('Answer me again,please.')
    print("Hello,"+name.title()+".This is Python-Servant.")
    names = name.title()

def temp_2(name_file='name.txt') :
    with open(name_file,'r') as name_load :
        names = name_load.read()
        names = names.rstrip()
    while True :
            user_yeno = input("Are you "+names+"?(yes/no)")
            user_yeno = user_yeno.lower()
            if user_yeno == yeno[0] :
                print("Welcome back,"+names+".This is Python-Servant.")
                break
            elif user_yeno == yeno[1] :
                temp_1()
                break
            else :
                continue
       
def python_servant() :
    """A little servant can paly with you."""
    #Asking action
    name_file = 'name.txt'
    try:
        with open(name_file,'r+') as name_load :
            names = name_load.read(10)
            names = names.rstrip()
    except:
        with open(name_file,'w') as name_load :
            pass
    try:
        with open(name_file,'r+') as name_load :
            names = name_load.read(10)
            names = names.rstrip()
        if names == '' :
            temp_1(name_file)
        else :
            temp_2(name_file)
        with open(name_file,'r+') as name_load :
            names = name_load.read()
            names = names.rstrip()
            time.sleep(0.5)
    except:
        temp_1(name_file)
        with open(name_file,'r+') as name_load :
            names = name_load.read()
            names = names.rstrip()
            time.sleep(0.5)
    while True :
        start_txt = """What do you want me to do?
        Play a math_game;
        Write a txt;
        Draw a yin&yang picture;
        Pour a cup of tea for you;
        Show I am cute;
        Nothing.
        (Don't add the '.' at last)
        """
        print(start_txt)
        ans = str(input())
        ans = ans.lower()
        servant_op = Servant(names)
        if ans == servant_ans[0] :
            servant_op.play_game()
        elif ans == servant_ans[1] :
            size_1 = int(input("The big circle's size:"))
            size_2 = int(input("The small circle's size:"))
            speed_1 = int(input("The drawing speed:"))
            yin_yang(speed_1,size_1,size_2)
        elif ans == servant_ans[2] :
            print("OK.")
            pour_tea(names)
        elif ans == servant_ans[3] :
            print("Look I'm smiling!")
            time.sleep(0.75)
            print("Am I cute? (^ ^)")
            time.sleep(0.75)
        elif ans == servant_ans[4] :
            _final_(names)
            break
        elif ans == servant_ans[5] :
            writing_ing(names)
        else :
            error_input = """
            I don't understand what did you say.
            This is what can I do.
            
            """
            print(error_input)

def readINI(file, key):
    """Read infomation from .ini files"""
    key = [key.upper(), key.title(), key.lower()]
    with open(file,'r') as file:
        texts = file.readlines()
    times = 0
    theNext = False
    final = []
    for i in range(len(texts)):
        if theNext:
            if keys in key:
                ttime = times
                while not nnext:
                    if ttime>len(texts)-1:
                        break
                    if "[" in texts[ttime] and "]" in texts[ttime] and ';' not in  texts[ttime]:
                        keys = texts[ttime].rstrip()
                        keys = keys.strip("[]")
                        nnext = True
                    else:
                        if texts[ttime].strip()!='':
                            final.append(texts[ttime].strip())
                    ttime+=1
            theNext = False
        if "[" in texts[times] and "]" in texts[times] and ';' not in  texts[times]:
            keys = texts[times].rstrip()
            keys = keys.strip("[]")
            theNext = True
            nnext = False
        times+=1
    if len(final) == 1:
        final = final[0]
    else:
        final = tuple(final)
    return final

def getItemInfo(info,*key):
    """Get infomation from a tuple or a list"""
    if len(key)==1 and len(info)==1:
        final = info[0].lstrip(str(key[0])+'=')
        return final
    times = 0
    timess = 0
    final = []
    for a in range(len(key)):
        for i in info:
            if (key[times]+' = ' in i) and (';' not in i):
                final.append(i.lstrip(str(key[times])+' = '))
            elif (key[times]+' =' in i) and (';' not in i):
                final.append(i.lstrip(str(key[times])+' ='))
            elif (key[times]+'= ' in i) and (';' not in i):
                final.append(i.lstrip(str(key[times])+'= '))
            elif (key[times]+'=' in i) and (';' not in i):
                final.append(i.lstrip(str(key[times])+'='))
        times+=1
    if len(final)==1:
        final = final[0]
    else:
        final = tuple(final)
    return final

def getINI(file):
    """To know what item in .ini file"""
    with open(file,'r') as file:
        texts = file.readlines()
    final = []
    for i in texts:
        if "[" in i and "]" in i and ';' not in  i:
            keys = i.rstrip()
            final.append(keys.strip("[]").lower())
    return final

def writeInZip(zfile, wfile, zmode='a', wmode='w', *text):
    """Write text into zipfile"""
    with zipfile.ZipFile(zfile, zmode) as zipf:
        with zipf.open(wfile, wmode) as file:
            for i in text:
                i=str(i)
                try:
                    i=i.encode(encoding='ascii')
                    file.write(i)
                except:
                    raise WriteInFailed(""+
                                        "Failed to write files.")

class GameItem:
    """Used to create a game item."""
    pass

class Error(Exception):
    """Raised for module-specific errors."""

class IvxTypeError(Exception):
    """When you give fuction ivx() a string."""

class LengthError(Exception):
    """When you give a num out of range."""

class WriteInFailed(Exception):
    """Failed to write file"""