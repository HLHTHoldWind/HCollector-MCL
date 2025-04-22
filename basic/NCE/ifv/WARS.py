import time as t
import random as r


def game_wars() :
 story = """This is made by HLHT_China ©2021.
 Translated by Andy Long."""
 print(story+'\n')
 while 1:
  print('Loading',end='')
  for i in range(3):
      t.sleep(1.25)
      print('.', end='',flush = True)
  print('v1.2.16',sep="")
  print('                 HLHT.@2020017-0816213511HLR 保留其著作权.')
  print('Shinoyume 译制      作者群738469349 作者QQ473090477          BY：Andy long')  #代码未经允许 严禁转载及套用 Andy    
  t.sleep(0.8)
  for i in range(8):
       print('')
       t.sleep(0.2)
  print('                         T',end = "")
  t.sleep(0.5)
  print('H',end = "")
  t.sleep(0.5)
  print('E',end = "")
  t.sleep(0.5)
  print('               ',end = "")
  print('W',end = "")
  t.sleep(0.5)
  print('A',end = "")
  t.sleep(0.5)
  print('R',end = "")
  t.sleep(0.5)
  print('s')
  t.sleep(0.5)
  print('')
  print('               |',end="")
  for i in range(20):
      print( '▉',end="")
      t.sleep(0.2)
  print('|')
  for i in range(4):
       print('')
       t.sleep(0.2)
  print('欢迎来到 the "wars"')
  print('这是个十分简单的回合制游戏')
  print('所有的行动都是随机生成的')
  print('你只需要做一些抉择')
  print('剩下的交给电脑！')
  R=0
  print('准备好了?')
  begin=input('好了/不')
  if begin=='不':
     print('好的，谢谢你的阅读')
     break
  elif begin=='好了':
      print('RULES')
      print("1.谁的HP降到0谁就死了")
      print('2.没什么特别的')
      print('goodluck and have fun')
  else:
       print('你为什么输其他的东西?')
       t.sleep(0.8)
       print('真是太懒了叭!')
       t.sleep(0.8)
  print('                        准备就绪！')
  p=3
  for i in range(3):
    print('游戏将在',p,'秒后开始...')
    t.sleep(1)
    p-=1
    t.sleep(1)
  comhp=100
  playerhp=100
  fire=0
  mg=20
  g=0
  h=0
  while 1:
     
     mg+=1  
 
     if comhp<=0 and playerhp<=0:
         print('>平局<')
         print('本局共计用了',R,'个回合')
         break
     elif playerhp<=0:
         print('-你输了-')
         print('本局共计用了',R,'个回合')
         print('玩家一共造成了',g,'点伤害，而电脑造成了',h,'点伤害')
         break
     elif comhp<=0:
         print('-你赢了-')
         print('本局共计用了',R,'个回合')
         print('玩家一共造成了',g,'点伤害，而电脑造成了',h,'点伤害')
         break
     comdmg=r.randint(1,25)
     R+=1
     print('-'*21,'ROUND',R,'-'*21)
     print('你的 HP:',playerhp)
     print('你的 MG:',mg)
     print("电脑的 HP:",comhp)
     print('你可以行动了')
     playeract=input('攻击(1)/回避(2)/治疗(3)/火魔法(4)')
     if playeract=='1':
         x=r.randint(1,15)
         if x==1:
             print('失误了！')
             print('你造成了',x,'点伤害')
             print('电脑造成了',comdmg,'点伤害')
             comhp-=x
             playerhp-=comdmg
         elif x==15:
             print('你造成了暴击')
             x=25
             print('你造成了',x,'点伤害')
             print('电脑造成了',comdmg,'点伤害')
             comhp-=x
             playerhp-=comdmg
         else:
             print('你造成了',x,'点伤害')
             print('电脑造成了',comdmg,'点伤害')
             comhp-=x
             playerhp-=comdmg
         g+=x
     elif playeract=='2':
         y=r.randint(1,3)
         if y==1:
             print('防御失败')
             print('电脑造成了',comdmg,'点伤害')
             playerhp-=comdmg
         elif y==2:
             print('成功!')
             comdmg=0
             print('电脑只造成了 0 点伤害!')
             playerhp-=comdmg
         else :
             print('大成功')
             print('电脑造成了',comdmg,'点伤害')
             print('电脑错过了一次机会!')
             comhp-=comdmg
             print('伤害反弹了!')
     elif playeract=='3':
         if mg>=4:
              v=r.randint(1,30)
              print('你回复了', v ,'点HP')
              print('消耗了4魔力')
              print('电脑造成了',comdmg,'点伤害')
              playerhp+=v
              mg-=4
              playerhp-=comdmg
         else:
             print('魔力不足!')
             print('电脑造成了',comdmg,'点伤害')
             playerhp-=comdmg
     elif playeract=='4':
         if mg>=8:
           print('玩家使用了火魔法！')
           print('消耗了8魔力')
           m=r.randint(1,4)
           print('电脑获得了',m,'回合的灼烧！')
           fire+=m
           mg-=8
           print('电脑造成了',comdmg,'点伤害')
           playerhp-=comdmg
         else :
           print('魔力不足')
           print('你错失了一回合')
           print('电脑造成了',comdmg,'点伤害')                                                                               #Shinoyume 译制
           playerhp-=comdmg
     else:
          print('你选择跳过回合')
          print('电脑造成了',comdmg,'点伤害')
          playerhp-=comdmg
     if fire>0:
            comhp-=5
            print('火焰灼烧对电脑造成 5 点伤害')
            fire-=1
            g+=5
     else :
            pass
     h+=comdmg
  chi=input('重置?(yes1/no0)')
  if chi=='1':
       print('')
  else :
       break
 print('感谢游玩!')
 t.sleep(2)
    
            
            
if __name__=='__main__':
    game_wars()