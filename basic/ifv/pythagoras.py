#Pythagoras

import time

h_title = """Latest Verison:1.1.1
This part is made by Hold Wind.
This is made by HLHT Studio ©2021.
You CAN NOT copy this program by any way.
You can call or e-mail us.
TEL:+86-028-85469778
E-mail:hlht2013@foxmail.com
If you have any question,you can ask us at any time.
By Hold Wind
================================================================================"""
class Pyth2() :

    def __init__(self) :
        pass

    def pythagoras_workout_before(self,a='?',b='?',c='?',_a_=False,_b_=False,_c_=False) :
        if _a_ :
            word_a = float(a)**0.5

        if _b_ :
            word_b = float(b)**0.5
    
        if _c_ :
            word_c = float(c)**0.5
    
        
        word_a = a
        word_b = b
        word_c = c
    
        if word_a != "?"  :
            a = float(word_a)
        if word_b != "?"  :
            b = float(word_b)
        if word_c != "?"  :
            c = float(word_c)
    
        if word_c == "?" and word_b != "?" and word_a != "?" :
            answer = (a**2)+(b**2)
            answer = answer**0.5
            c = answer
        elif word_b == "?" and word_a != "?" and word_c != "?" :
            answer = (c**2)-(a**2)
            answer = answer**0.5
            b = answer
        elif word_a == "?" and word_b != "?" and word_c != "?" :
            answer = (c**2)-(b**2)
            answer = answer**0.5
            a = answer

        self.a = a
        self.b = b
        self.c = c


class Pythagoras(Pyth2) :

    def __init__(self) :
        pass
    def pythagoras_view(self) :
        print(h_title)
        print("Turning up",end='',flush=True)
        for i in range(6) :
            print('.',end='',flush=True)
            time.sleep(0.75)
        print("\n\nVerison:1.1.0")
        print('If you are finished,input"DONE"')
        
        while True:
            question = """
            If angle-C is the Right-Angle,
            Input your question.
            Answer me a number or "?"
            If you want to input √x,input'/'.
            Then input the numbers after √.
            """
            print(question)
            word_a = input("a=")
            word_a = str(word_a)
            if word_a == '/' :
                _word_a = float(input("a=√"))
                word_a = float(_word_a)**0.5
            elif word_a == '' :
                word_a = '?'
            
            word_b = input("b=")
            word_b = str(word_b)
            if word_b == '/' :
                _word_b = float(input("b=√"))
                word_b = (_word_b)**0.5
            elif word_b == '' :
                word_b = '?'
            
            word_c = input("c=")
            word_c = str(word_c)
            if word_c == '/' :
                _word_c = float(input("c=√"))
                word_c = float(_word_c)**0.5
            elif word_c == '' :
                word_c = '?'
            
            word_a = str(word_a)
            word_b = str(word_b)
            word_c = str(word_c)
            
            if word_a != "?" and word_a != "DONE" and word_a != "" :
                a = float(word_a)
            if word_b != "?" and word_b != "DONE" and word_b != "" :
                b = float(word_b)
            if word_c != "?" and word_c != "DONE" and word_c != "" :
                c = float(word_c)
            
            if word_c == "?" and word_b != "?" and word_a != "?" :
                answer = (a**2)+(b**2)
                answer = answer**0.5
                word_c = print("c="+str(round(answer,15)))
                c = answer
            elif word_b == "?" and word_a != "?" and word_c != "?" :
                answer = (c**2)-(a**2)
                answer = answer**0.5
                word_b = print("b="+str(round(answer,15)))
                b = answer
            elif word_a == "?" and word_b != "?" and word_c != "?" :
                answer = (c**2)-(b**2)
                answer = answer**0.5
                word_a = print("a="+str(round(answer,15)))
                a = answer
            elif word_a == "DONE" or word_b == "DONE" or word_c == "DONE" :
                break
            else :
                print("NumberError:I must know 2 numbers.")
                print("Or you can't input more than 2 numbers.")
            txt_1 = (str(a)+'/'+str(b)+'/'+str(c))
            with open("pythagoras.record.txt",'a') as record :
                record.write(txt_1+'\n')
                record.write('\n')
    
        print("Thanks for using.")
        time.sleep(1.25)
        print("Goodbye!")
        time.sleep(1.25)
        print("Shuting down",end='',flush = True)
        for i in range(6) :
            print('.',end='',flush = True)
            time.sleep(0.5)

    def pythagoras_workout(self,a='?',b='?',c='?',_a_=False,_b_=False,_c_=False,radical=False) :
        aa=a
        bb=b
        cc=c
        if _a_ :
            aa=a**0.5
        if _b_ :
            bb=b**0.5
        if _c_ :
            cc=c**0.5
        
        super().pythagoras_workout_before(aa,bb,cc,_a_=False,_b_=False,_c_=False)
        if _a_ and radical:
            a='√'+str(a)
        else:
            a=str(self.a)
        if _b_ and radical:
            b='√'+str(b)
        else:
            b=str(self.b)
        if _c_ and radical:
            c='√'+str(b)
        else:
            c=str(self.c)
        return (a,b,c)

if __name__=='__main__':
    pyth=Pythagoras()
    pyth.pythagoras_view()
