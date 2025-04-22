"""
# Copyright 2021 HLHT Studio .  All Right Reserved.
You CAN NOT copy this program by any way.
You can call or e-mail us.
TEL:+86-028-85469778
E-mail:hlht2013@foxmail.com
If you have any question,you can ask us at any time.
By Hold Wind and Andy Long.
"""
#//Pygame2.0//#
#//HLHT Studio ©2021//#
#
#[Import]
import pygame
import sys,time,random,math
import time as t
import random as r
from pygame.locals import *
# with open("assets\\record\\screen.scrs","r") as file:
        # S_WIDTH = int(file.readline())
        # S_HEIGHT = int(file.readline())
#[Definition]
# prints text using the supplied font
def loadin(images,alpha=True):
    try:
        if alpha:
            master_image=pygame.image.load(images).convert_alpha()
        else:
            master_image=pygame.image.load(images).convert()
    except:
        master_image=None
    return master_image
def print_text(font,x,y,text,color=(255,255,255)):
    imgText=font.render(text,True,color)
    screen=pygame.display,get_surface()
    screen.blit(imgText,(x,y))
# calculates angle between two points
def target_angle(x1,y1,x2,y2):
    delta_x=x2-x1
    delta_y=y2-y1
    angle_radians=math,atan2(delta_y,delta_x)
    angle_degress=ath.degress(angle_radians)
    return angle_degress
# calculates distance between two points
def distance(point1,point2):
    delta_x=point1.x-point2.x
    delta_y=point1.y-point2.y
    dist=math.sqrt(delta_x**2+delta_y**2)
    return dist
# BookSprite class extend pygame.sprite.Sprite
class BookSprite(pygame.sprite.Sprite):
    def __init__(self,target):
        pygame.sprite.Sprite.__init__(self) #extend the base Sprite class
        self.master_image=None
        self.frame=0
        self.old_frame=-1
        self.frame_width=1
        self.frame_height=1
        self.first_frame=0
        self.last_frame=0
        self.columns=1
        self.last_time=0
        self.direction=0
        self.velocity=Point(0,0)
    #X property
    def _getx(self):
        return self.rect.x
    def _setx(self,value):
        self.rect.x=value
    X=property(_getx,_setx)
    #Y property
    def _gety(self):
        return self.rect.y
    def _sety(self,value):
        self.rect.y=value
    Y=property(_gety,_sety)
    #position property
    def _getpos(self):
        return self.rect.topleft
    def _setpos(self,pos):
        self.rect.topleft=pos
    position=property(_getpos,_setpos)
    #load
    def load(self,filename,width=0,height=0,columns=1):
        self.master_image=filename
        self.set_image=(self.master_image,width,height,columns)
        self.frame_width=width
        self.frame_height=height
        self.rect=Rect(0,0,width,height)
        self.columns=columns
        #try to auto-calculate total frames
        rect=self.master_image.get_rect()
        self.last_frame=(rect.width//width)*(rect.height//height)-1
    #update
    def update(self,current_time,rate=30):
        if self.last_frame>self.first_frame:
            #update animation frame number
            if current_time>self.last_time+rate:
                self.frame+=1
                if self.frame>self.last_frame:
                    self.frame=self.first_frame
                self.last_time=current_time
        else:
            self.frame=self.first_frame 
        #build current frame only if it changed
        if self.frame!=self.old_frame:
            frame_x=(self.frame%self.columns)*self.frame_width
            frame_y=(self.frame//self.columns)*self.frame_height
            rect=Rect(frame_x,frame_y,self.frame_width,self.frame_height)
            self.image=self.master_image.subsurface(rect)
            self.old_frame=self.frame
    #set images
    def set_image(self,image,width=0,height=0,columns=1):
        self.master_image=image
        if width==0 and height==0:
            self.frame_width=image.get_width()
            self.frame_height=image.get_height()
        else:
            self.frame_width=width
            self.frame_height=height
            rect=self.master_image,get_rect()
            self.last_frame=(rect.width//width)*(rect.height//height)-1
        self.rect=Rect(0,0,self.frame_width,self.frame_height)
        self.columns=columns
    #
    def __str__(self):
        return str(self.frame)+","+str(self.first_frame)+\
               ","+str(self.last_frame)+","+str(self.frame_width)+\
               ","+str(self.frame_height)+","+str(self.columns)+\
               ","+str(self.rect)
#Point class
class Point(object):
    def __init__(self,x,y):
        self.__x=x
        self.__y=y
    #X property
    def getx(self):
        return self.__x
    def setx(self,x):
        self.__x=x
    x=property(getx,setx)
    #Y property
    def gety(self):
        return self.__y
    def sety(self,y):
        self.__y=y
    y=property(gety,sety)
    #
    def __str__(slef):
        return "{X:"+"{:.0f}".format(self.__x)+\
               ",Y:"+"{:.0f}".format(self.__y)+"}"
#Snake
class SnakeSegment(BookSprite):
    def __init__(self,color=(20,200,20)):
        BookSprite.__init__(self)
        image=pygame.Surface((32,32)).convert_alpha()
        image.fill((255,255,255,0))
        pygame.draw.circle(image,color,(16,16),16,0)
        self.set_image(image)
        BookSprite.update(self,0,30) #create frame image
#Food
class Food(BookSprite):
    def     __init__(self):
        BookSprite.__init__(self)
        image=pygame.Surface((32,32)).convert_alpha()
        image.fill((255,255,255,0))
        pygame.draw.circle(image,(16,16),16,0)
        self.set_image(image)
        BookSprite.update(self,0,30) #create frame image
        self.X=random.randint(0,23)*32
        self.Y=random.randint(0,17)*32
#Tank Battle
class Tank(BookSprite): #NOT FINISH
    def __init__(self,tank_file="tank.png",turret_file="turret.png"):
        BookSprite.__init(self)
        self.load(tank_file,50,60,4)
        self.speed=0.0
        self.scratch=None
        self.float_pos=Point(0,0)
        self.velocity=Point(0,0) 
        self.turret=BookSprite()
        self.turret.load(turrtle_file,32,64,4)
        self.fire_timer=0
def location(image,width,height):
    image_rect = image.get_rect()
    image_rect.center = (width//2,height//2)
    return image_rect
def image_del(image,screen):
    pygame.transform.smoothscale(image,(0,0))
    screen.blit(image,(99999,99999))
def image_app(image,size1,size2):
    pygame.transform.smoothscale(image,(size1,size2))
def sound_back(sound):
    channel=pygame.mixer.find_channel(True)
    background=pygame.mixer.Sound(sound)
    channel.play(background,loops=-1,fade_ms=700)
def print_fps(screen):
    with open("assets\\record\\screen.scrs","r") as file:
        S_WIDTH=int(file.readline())
    # fff=pygame.font.Font(None,int(S_WIDTH/1280)*20)
    # fps=fff.render(str(pygame.time.get_ticks()),True,(0,255,0))
    # screen.blit(fps,(0,0))
def font_size(size=32):
    return pygame.font.Font('assets\\font\\courbd.ttf',size)
def load_page(width,height,screen,center,font=None,load_time=4,out_bar=True):
        width_2 = int(width/1280*900) #WARS
        width_22 = int(width/1024*1280) #Background
        height_22 = int(height/768*1024) #Background
        height_3 = int(height/1024*350)
        height_4 = int(height/1024*75)
        height_2 = int(height/1024*600) #deciding the "WARS"'s size
        background = loadin("assets\\background\\menu.png")
        background = pygame.transform.smoothscale(background,(width_2,height_2))
        
        background_rect = background.get_rect()
        background_rect.center = center
        #screen.blit(background,background_rect)
        title = loadin("assets\\theme\\winter\\WarsTitle.png")
        load_bar = loadin("assets\\background\\loading.png")
        title = pygame.transform.smoothscale(title,(width_2,height_2))
        title_rect = title.get_rect()
        title_rect.center = center #deciding the "WARS"'s location
        screen.blit(title,title_rect)
        
        t.sleep(0.3)
        times = r.randint(load_time*144,(load_time*144)+250)
        ran = 2
        fpsClock = pygame.time.Clock()
        
        line = r.randint(5,14)
        
        with open('assets\\font\\starttext.str','r') as file:
            for lines in range(line):
                text = file.readline()
                text = text.rstrip()
        print(text)
        if line<=7:
            sizs = font_size(int(S_WIDTH/1280)*64)
            tide = sizs.render(text,True,(255,255,255))
            tiderect = tide.get_rect()
            height_6 = (height//2-height_3)
            tiderect.center = (width//2,height_6)
            screen.blit(tide,tiderect)
        else:
            sizs = (int(S_WIDTH/1280)*24)
            tide = font.render(text,True,(255,255,255))
            tiderect = tide.get_rect()
            height_6 = (height//2-height_3)
            tiderect.center = (width//2,height_6)
            screen.blit(tide,tiderect)
        bar_size = int(width/1280*90)
        load_bar = pygame.transform.smoothscale(load_bar,(bar_size,bar_size))
        for i in range(times):
            fpsClock.tick(144)
            load_bar_rota = pygame.transform.rotate(load_bar,ran)
            ran+=2
            
            
            load_bar_rect = load_bar_rota.get_rect()
            load_bar_rect.center = (width//2,height//2+height_3)
            screen.blit(load_bar_rota,load_bar_rect)
            loading = font.render("Loading",True,(255,255,255))
            loadrect = loading.get_rect()
            height_5 = (height//2+(height_3+height_4))
            loadrect.center = (width//2,height_5)
            screen.blit(loading,loadrect)
            pygame.display.update()
        
        
        
        # while True:
            # for event in pygame.event.get():
                # if event.type==QUIT:
                    # pygame.quit()
                    # sys.exit()
                # if event.type==KEYUP:
                    # if event.key==pygame.K_ESCAPE:
                        # pygame.quit()
                        # sys.exit()
                    # elif event.key==pygame.K_SPACE:
                        # pygame.draw.rect(screen,(0,0,0),(0,0,width,height))
                        # pygame.display.update()
                        # break
                    # else:
                        # pass
        pygame.draw.rect(screen,(0,0,0),(0,0,width,height))
        #pygame.display.update()
        libr = BookSprite(screen)
        title_out = libr.load("assets\\theme\\winter\\out.jpg",900,600,42)
        title_out = pygame.transform.smoothscale(title,(width_2,height_2))
        group = pygame.sprite.Group()
        group.add(libr)
        width_out = int(width/1280*450)
        height_out = int(height/1024*300)
        if out_bar:
            for i in range(82):
                fpsClock.tick(42)
                ticks = pygame.time.get_ticks()
                libr.X = (width//2)-(width_2//2)
                libr.Y = (height//2)-(height_2//2)
                group.update(ticks)
                group.draw(screen)
                pygame.display.update()
        else:
            pygame.display.update()
def load_page2(width,height,screen,center,font=None,load_time=4,out_bar=True):
        width_2 = int(width/1280*487) #WARS
        width_22 = int(width/1024*1280) #Background
        height_22 = int(height/768*1024) #Background
        height_3 = int(height/1024*350)
        height_4 = int(height/1024*75)
        height_2 = int(height/1024*600) #deciding the "WARS"'s size
        background = loadin("assets\\background\\menu.png")
        background = pygame.transform.smoothscale(background,(width_2,height_2))
        
        background_rect = background.get_rect()
        background_rect.center = center
        #screen.blit(background,background_rect)
        title = loadin("assets\\theme\\minecraft\\WarsTitle.png")
        load_bar = loadin("assets\\background\\loading.png")
        title = pygame.transform.smoothscale(title,(width_2,height_2))
        title_rect = title.get_rect()
        title_rect.center = center #deciding the "WARS"'s location
        screen.blit(title,title_rect)
        
        t.sleep(0.3)
        times = r.randint(load_time*144,(load_time*144)+250)
        ran = 2
        fpsClock = pygame.time.Clock()
        
        line = r.randint(5,14)
        
        with open('assets\\font\\starttext.str','r') as file:
            for lines in range(line):
                text = file.readline()
                text = text.rstrip()
        print(text)
        if line<=7:
            sizs = font_size(int(S_WIDTH/1280)*64)
            tide = sizs.render(text,True,(255,255,255))
            tiderect = tide.get_rect()
            height_6 = (height//2-height_3)
            tiderect.center = (width//2,height_6)
            screen.blit(tide,tiderect)
        else:
            sizs = (int(S_WIDTH/1280)*24)
            tide = font.render(text,True,(255,255,255))
            tiderect = tide.get_rect()
            height_6 = (height//2-height_3)
            tiderect.center = (width//2,height_6)
            screen.blit(tide,tiderect)
        bar_size = int(width/1280*90)
        load_bar = pygame.transform.smoothscale(load_bar,(bar_size,bar_size))
        for i in range(times):
            fpsClock.tick(144)
            load_bar_rota = pygame.transform.rotate(load_bar,ran)
            ran+=2
            
            
            load_bar_rect = load_bar_rota.get_rect()
            load_bar_rect.center = (width//2,height//2+height_3)
            screen.blit(load_bar_rota,load_bar_rect)
            loading = font.render("Loading",True,(255,255,255))
            loadrect = loading.get_rect()
            height_5 = (height//2+(height_3+height_4))
            loadrect.center = (width//2,height_5)
            screen.blit(loading,loadrect)
            pygame.display.update()
        
        
        
        # while True:
            # for event in pygame.event.get():
                # if event.type==QUIT:
                    # pygame.quit()
                    # sys.exit()
                # if event.type==KEYUP:
                    # if event.key==pygame.K_ESCAPE:
                        # pygame.quit()
                        # sys.exit()
                    # elif event.key==pygame.K_SPACE:
                        # pygame.draw.rect(screen,(0,0,0),(0,0,width,height))
                        # pygame.display.update()
                        # break
                    # else:
                        # pass
        pygame.draw.rect(screen,(0,0,0),(0,0,width,height))
        #pygame.display.update()
        libr = BookSprite(screen)
        title_out = libr.load("assets\\theme\\minecraft\\out.png",487,600,42)
        title_out = pygame.transform.smoothscale(title,(width_2,height_2))
        group = pygame.sprite.Group()
        group.add(libr)
        width_out = int(width/1280*243.5)
        height_out = int(height/1024*300)
        if out_bar:
            for i in range(82):
                fpsClock.tick(42)
                ticks = pygame.time.get_ticks()
                libr.X = (width//2)-(width_2//2)
                libr.Y = (height//2)-(height_2//2)
                group.update(ticks)
                group.draw(screen)
                pygame.display.update()
        else:
            pygame.display.update()
def mouse_click(obj,loc,event):
    mx,my=pygame.mouse.get_pos()
    #mx=event.pos()
    mx=int(mx)
    my=int(my)
    t_pos=obj.get_rect()
    #th_pos=list(t_pos.center)
    tx=t_pos[1]
    ty=t_pos[2]
    a=False
    b=False
    
    c=0
    for abc in loc:
        c+=1
        h=False
        f=False
        tx,ty=abc
        sx,sy=obj.get_size()
        # tx=tx-sx
        # ty=ty-sy
        thx=tx+sx
        thy=ty+sy
        #print(mx)
        #print(my)
        #print(tx,thx)
        #print(ty,thy)
        
        if mx in range(tx,thx):
            a=True
            h=True
        if my in range(ty,thy):
            b=True
            f=True
        if h and f:
            m=c
            
        #for 
    if a and b and m==1:
        #print(m)
        #print('You click AI!')
        #channel = pygame.mixer.find_channel(True)
        #channel.stop()
        return True,'AI'
    elif a and b and m==2:
        #print(m)
        #print('You click NORMAL!')
        return True,'NORMAL'
    elif a and b and m==3:
        #print(m)
        #print('You click SETTING!')
        return True,'SETTING'
    elif a and b and m==4:
        #print(m)
        #print('You click SETTING!')
        return True,'EXIT'
    
    #t_pos=obj.get_rect()
    # if t_pos.collidepoint(event.pos()):
        # return True
    else:
        #print(c)
        #print("No button")
        return False,'NONE'
    #tx,ty=loc[0]

def gifView(screen,picture,width,height,c_width,c_height,fps,fpsClock,background,loc,fpsdraw=0):
    libr = BookSprite(screen)
    title_out = libr.load(picture,width,height,fps)
    background = pygame.transform.smoothscale(background,(c_width,c_height))
    group = pygame.sprite.Group()
    group.add(libr)
    if fpsdraw==0:
        fpsdraw=fps
    for i in range(fpsdraw):
        screen.blit(background,loc)
        fpsClock.tick(fps)
        ticks = pygame.time.get_ticks()
        libr.X,libr.Y = loc
        group.update(ticks)
        group.draw(screen)
        pygame.display.update()