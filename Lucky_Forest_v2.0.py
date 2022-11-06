
import pygame,os,numpy
import random
sizen = 64
WIDTH = sizen*16
HEIGHT = int(sizen*11.9999) 
FPS = 75

# Создаем игру и окно
WHITE = ((255,255,255))
RED = ((255,0,0))
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lucky Forest v1.0")
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')

def rotate( xc, yc, mouse_x, mouse_y):
    dy = mouse_y - yc
    dx = mouse_x - xc
    angle = numpy.arctan2(dy, dx)
    return angle/numpy.pi *180
def si(f,n,x,y):
    
    t  = '.bmp'
    if n == 'None':
        t = '.png'
    p = pygame.image.load(os.path.join(f,n + t)).convert()
    p = pygame.transform.scale(p,(x,y))
    return p
n_img = si(img_folder,'None',sizen,sizen)
ni_img = si(img_folder,'None',0,0)

grassimg = si(img_folder,'Grass',sizen,sizen)
treeimg = si(img_folder,'Tree',sizen,sizen)
tree2img = si(img_folder,'Tree2',sizen,sizen)

Pimg = si(img_folder,'Man2',sizen,sizen)
Pimg2 = pygame.transform.flip(Pimg,True,False)
Pimg3 = si(img_folder,'Man3',sizen,sizen)
Pimg4 = si(img_folder,'Man4',sizen,sizen)

Himg = si(img_folder,'Heart',sizen,sizen)
Himg2 = si(img_folder,'Heart2',sizen,sizen)
Himg3 = si(img_folder,'Heart3',sizen,sizen)


Kimg = si(img_folder,'Knife',sizen//2,sizen//2)



Skeletimg = si(img_folder,'Skelet',sizen,sizen)
Skeletimg2 = pygame.transform.flip(Skeletimg,True,False)
Skeletimg3 = si(img_folder,'Skelet2',sizen,sizen)
Skeletimg4 = si(img_folder,'Skelet3',sizen,sizen)

Panim = [Pimg,Pimg2,Pimg3,Pimg4]
Skelanim = [Skeletimg,Skeletimg2,Skeletimg3,Skeletimg4]
Heartamin = [Himg,Himg2,Himg3]

ico = si(img_folder,'Chest',sizen//2,sizen//2)

pygame.display.set_icon (ico)
class Button(pygame.sprite.Sprite):
    def __init__(self,n):
        pygame.sprite.Sprite.__init__(self)
        self.image = Heartamin[n%3] 
        self.rect = self.image.get_rect()
        self.rect.center = (sizen/2 + sizen * n,sizen/2)
        self.n = n
        self.pos = self.rect.center
        self.g = 0
        self.image.set_colorkey(WHITE)
        self.prevhp = sett.hp
        self.alp = 255
class Particle(pygame.sprite.Sprite):
    def __init__(self,sizex,sizey,posx,posy,color,plus_alpha,tim,movex,movey,y_tim,alp):
        pygame.sprite.Sprite.__init__(self)
        #20,20
        self.image = pygame.Surface((sizex,sizey))
        #(192 + random.randint(-16,16),0,0)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        #WIDTH/2 + random.randint(-sizen//2,sizen//2),HEIGHT/2 + random.randint(-sizen//2,sizen//2)
        self.rect.center = (posx,posy)
        self.tim = 0
        #random.randint(-5,5)
        self.otklon = movex
        self.tim_life = tim
        #
        self.y_tim = y_tim
        if self.y_tim:
            self.move_y = 0
        else:
            self.move_y = movey   
        self.plus_alpha = plus_alpha
        self.a = alp
    def update(self):
        
        self.tim += 1
        self.a += self.plus_alpha
        self.image.set_alpha(self.a)
        self.rect.centerx += self.otklon
        if self.y_tim:
            self.rect.centery += self.tim
        else:
            self.rect.centery += self.move_y
        if self.tim >= self.tim_life:
            pargr.remove(self)
        
class Lives(pygame.sprite.Sprite):
    def __init__(self,n):
        pygame.sprite.Sprite.__init__(self)
        self.image = Heartamin[n%3] 
        self.rect = self.image.get_rect()
        self.rect.center = (sizen/2 + sizen * n,sizen/2)
        self.n = n
        self.pos = self.rect.center
        self.g = 0
        self.image.set_colorkey(WHITE)
        self.prevhp = sett.hp
        self.alp = 255
        
        
    def update(self):
        self.alp = self.alp + (255 - self.alp)/5
        self.g += sett.risk / 500 + 0.1 + (0.25 - sett.hp/20)
        if sett.hp <= self.n:
            self.rect.center = (-sizen,-sizen)
        else:
            self.rect.center = self.pos
        self.image = Heartamin[(self.n + int(self.g))%3] 
        self.image.set_alpha(self.alp)
        self.image.set_colorkey(WHITE)
        
        if self.prevhp > sett.hp:
            self.alp = -255
        self.prevhp = sett.hp
class Knife(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = ni_img
            
        self.rect = self.image.get_rect()
        self.rect.center = p.rect.center
        self.image.set_colorkey((0,0,0))
        self.vel = 0.0
        x=self.rect.centerx
        y=self.rect.centery

        mouse_x, mouse_y = pygame.mouse.get_pos()
        xc, yc = self.rect.center
        self.angle = -rotate(xc, yc, mouse_x, mouse_y)
            
        imgr = pygame.transform.rotate(Kimg, self.angle)
        self.image = imgr
        self.rect = self.image.get_rect()
            
        self.image.set_colorkey((0,0,0))
        self.rect.center = (x,y)
        self.r=0
        
        self.image.set_colorkey((0,0,0))

        

    def update(self):
        
        self.r += self.vel
        

        self.rect.centerx = p.rect.centerx + self.r*numpy.cos(self.angle/180*numpy.pi)
        self.rect.centery = p.rect.centery -self.r*numpy.sin(self.angle/180*numpy.pi)
        if self.rect.center == p.rect.center:
            self.vel = 0
            self.image = ni_img
            if pygame.mouse.get_pressed()[0] == 1:
                
                

                mouse_x, mouse_y = pygame.mouse.get_pos()
                xc, yc = self.rect.center
                self.angle = -rotate(xc, yc, mouse_x, mouse_y)
                abool = ((self.angle >= 135 or self.angle <= -135) and p.see == 0)
                bbool = ((self.angle >= 45 and self.angle <= 135) and p.see == 1)
                cbool = ((self.angle >= -45 and self.angle <= 45) and p.see == 2)
                dbool = ((self.angle >= -135 and self.angle <= -45) and p.see == 3)

                if abool or bbool or cbool or dbool:
                    self.vel = 12.0
                    x=self.rect.centerx
                    y=self.rect.centery    
                    imgr = pygame.transform.rotate(Kimg, self.angle)
                    self.image = imgr
                    self.rect = self.image.get_rect()
                        
                    self.image.set_colorkey((0,0,0))
                    self.rect.center = (x,y)
                    self.r=0
                    
                    self.image.set_colorkey((0,0,0))
        else:
            self.vel -= 1.0
class SLoi(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = n_img 
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2,HEIGHT/2)
        self.pos = [0,0]
        self.pole = [['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0']]
        for i in range(32):
            self.pole.append(['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'])
        self.r = 0
    def update(self):
        for i in range(1500):
            self.r += 1
            
                
            if self.r <= 811:
                self.pole[self.pos[1]+16][self.pos[0]+16] = '1'
                while True:
                    r = random.randint(1,4)
                    if r == 1 and self.pos[1] != 10:
                        self.rect.center = (self.rect.centerx, self.rect.centery+sizen)
                        self.pos[1]+=1
                        break
                    elif r == 2 and self.pos[0] != 10:
                        self.rect.center = (self.rect.centerx+sizen, self.rect.centery)
                        self.pos[0]+=1
                        break
                    elif r == 3 and self.pos[1] != -10:
                        self.rect.center = (self.rect.centerx, self.rect.centery-sizen)
                        self.pos[1]-=1
                        break
                    elif r == 4 and self.pos[0] != -10:
                        self.rect.center = (self.rect.centerx-sizen, self.rect.centery)
                        self.pos[0]-=1
                        break
                
                '''room = Room(self.pos,grassimg )
                und.add(room)'''
            if self.r == 812:
                for u in range(33):
                    for j in range(33):
                        if self.pole[u][j] == '0':
                            if random.randint(0,1)==0:
                                tyy = treeimg
                            else:
                                tyy = tree2img
                            room = Room([u,j],tyy )
                            und.add(room)
                        if self.pole[u][j] == '1':
                            if random.randint(0,25) == 0 and ((u < 15 or u > 17) or (j < 15 or j > 17)):
                                skel = Skelet([u,j])
                                enem.add(skel)
                            
                            room = Room([u,j],grassimg )
                            und.add(room)
                und.remove(self)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = Pimg3
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2,HEIGHT/2)
        self.possi = self.rect.center
        self.pos = [0,0]
        self.image.set_colorkey(WHITE)
        self.retime = 10
        self.command = [0,0]
        self.see = 3
    def update(self):
        #print(s.pole[self.pos[0]+11][self.pos[1]+11])
        upper = False
        leftper = False
        downper = False
        rightper = False

        self.retime -= 1
        if self.retime <= 0:
            for roo in und:
                if (roo != s) and (roo.index == 0):
                    rp1 = roo.rect.centerx
                    mp1 = self.rect.centerx
                    rp2 = roo.rect.centery
                    mp2 = self.rect.centery
                    if (rp2 + sizen)//3 == mp2//3 and rp1//3 == mp1//3:
                        upper = True
                    if (rp2 - sizen)//3 == mp2//3 and rp1//3 == mp1//3:
                        downper = True
                    if (rp1 + sizen)//3 == mp1//3 and rp2//3 == mp2//3:
                        leftper = True
                    if (rp1 - sizen)//3 == mp1//3 and rp2//3 == mp2//3:
                        rightper = True
            if  (sett.move[0]) and (upper):
                sett.yc -= sizen
                self.pos[1] += 1
                self.retime = 20
                self.image = Panim[3]
                self.see = 1
            if  (sett.move[2]) and (downper):
                sett.yc += sizen
                self.pos[1] -= 1
                self.retime = 20
                self.image = Panim[2]
                self.see = 3
            if  (sett.move[3]) and (rightper):
                sett.xc += sizen
                self.pos[0] -= 1
                self.retime = 20
                self.image = Panim[1]
                self.see = 2
            if  (sett.move[1]) and (leftper):
                sett.xc -= sizen
                self.pos[0] += 1
                self.retime = 20
                self.image = Panim[0]
                self.see = 0
        
        sett.x += (sett.xc - sett.x)/4
        if 0 < (sett.xc - sett.x)/4 < 1:
            sett.x =sett.xc
        sett.y += (sett.yc - sett.y)/4
        if 0 < (sett.yc - sett.y)/4 < 1:
            sett.y =sett.yc

        '''wer = s.pole.copy()
        for ur in wer:
            print()
            for p in ur:
                print(p,end='')
        print()
        wer[self.pos[1]+11][self.pos[0]+11] = '5'
        for ur in wer:
            print()
            for p in ur:
                print(p,end='')'''
        if sett.retaim >0:
            sett.retaim -= 1
        self.image.set_alpha(255 - sett.retaim)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2,HEIGHT/2)
class Skelet(pygame.sprite.Sprite):
    def __init__(self,pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = Skeletimg
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2+(pos[0]-11)*sizen,HEIGHT/2+(pos[1]-11)*sizen)
        self.possi = self.rect.center
        self.possi2 = self.rect.center

        self.pos = pos
        self.img = Skeletimg
        self.image.set_colorkey(WHITE)
        self.retime = 0

        
        
        
    def update(self):
        
        upper = False
        leftper = False
        downper = False
        rightper = False

        self.retime -= 1
        if self.retime <= 0:
            
                
            for roo in und:
                if (roo != s) and (roo.index == 0):
                    
                    rp2 = roo.possi[1]- sett.yc
                    mp2 = self.possi2[1]- sett.yc
                    rp1 = roo.possi[0] - sett.xc
                    mp1 = self.possi2[0] - sett.xc
                    if (rp2 - sizen)//7 == mp2//7 and rp1//7 == mp1//7:
                        upper = True
                    if (rp2 + sizen)//7 == mp2//7 and rp1//7 == mp1//7:
                        downper = True
                    if (rp1 + sizen)//7 == mp1//7 and rp2//7 == mp2//7:
                        leftper = True
                    if (rp1 - sizen)//7 == mp1//7 and rp2//7 == mp2//7:
                        rightper = True
            for i in range(100):
                r = random.randint(1,4)
                mp = self.rect.center
                pp = p.rect.center
                '''print(mp,pp,mp[0] < pp[0],mp[0] > pp[0],mp[1] < pp[1],mp[1] > pp[1])
                r = 0
                if mp[0] < pp[0]:
                    r = 3
                elif mp[0] > pp[0]:
                    r = 4
                elif mp[1] < pp[1]:
                    r = 1
                elif mp[1] > pp[1]:
                    r = 2'''
                
                if  (upper) and (r == 1):
                    self.possi2 = (self.possi2[0],self.possi2[1]+sizen)
                    
                    self.retime = 35
                    self.image = Skelanim[2]
                    break
                elif  (downper) and (r == 2) :
                    self.possi2 = (self.possi2[0],self.possi2[1]-sizen)   
                    
                    self.retime = 35
                    self.image = Skelanim[3]
                    break
                elif  (rightper) and (r == 3) :
                    self.possi2 = (self.possi2[0]+sizen,self.possi2[1])   
                    
                    self.retime = 35
                    self.image = Skelanim[1]
                    break
                elif  (leftper) and (r == 4):
                    self.possi2 = (self.possi2[0]-sizen,self.possi2[1])      
                    
                    self.retime = 35
                    self.image = Skelanim[0]
                    break
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.possi = ((self.possi[0] + (self.possi2[0] - self.possi[0])/4),self.possi[1])
        self.possi = (self.possi[0],(self.possi[1] + (self.possi2[1] - self.possi[1])/4))  
        self.rect.center = (self.possi[0] - sett.x, self.possi[1]- sett.y)  
        '''if 0 < (self.possi[0] + (self.possi2[0] - self.possi[0])/4) < 1 / sizen:
            self.possi = (self.possi2[0],self.possi[1])
        if 0 < (self.possi[1] + (self.possi2[1] - self.possi[1])/4) < 1 / sizen:
            self.possi = (self.possi[0],self.possi2[1])'''
class Room(pygame.sprite.Sprite):
    def __init__(self,pos,img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2+(pos[0]-11)*sizen,HEIGHT/2+(pos[1]-11)*sizen)
        self.possi = self.rect.center
        

        self.pos = pos
        self.img = img
        self.index = int(not(img == grassimg))
        
        
        
    def update(self):

        self.rect.center = (self.possi[0] - sett.x, self.possi[1]- sett.y)
class Settings():
    def __init__(self):
        self.x = 5 * sizen
        self.y = 5 * sizen
        self.xc = 5 * sizen
        self.yc = 5 * sizen
        self.move = [False,False,False,False]
        self.hp = 5
        self.risk = 0
        self.Game_Started = True
        self.retaim = 0
clock = pygame.time.Clock()
und = pygame.sprite.Group()
enem = pygame.sprite.Group()
UI = pygame.sprite.Group()
pargr = pygame.sprite.Group()
sett = Settings()
obj = pygame.sprite.Group()
for i in range(1):
    s = SLoi()
    und.add(s)
for i in range(5):
    h = Lives(i)
    UI.add(h)

p = Player()
k = Knife()
obj.add(k,p)
ru = True

g = False
trim = -1

while ru:  
        
        sett.risk = 0
        distancesk = 9999999
        for sk in enem:
            if (abs(p.rect.centerx - sk.rect.centerx) + abs(p.rect.centery - sk.rect.centery))//sizen < distancesk:
                distancesk = (abs(p.rect.centerx - sk.rect.centerx) + abs(p.rect.centery - sk.rect.centery))//sizen
        if distancesk <= 10:
            sett.risk = (10 - distancesk) / 10 * 100
            if distancesk == 0 and sett.retaim == 0:
                sett.retaim = 100
                sett.hp -= 1
                for y in range(random.randint(3,11)):
                    par = Particle(2,2,WIDTH/2 + random.randint(-sizen//2,sizen//2),
                    HEIGHT/2 + random.randint(-sizen//2,sizen//2),(192 + random.randint(-16,16),0,0),-3,500,random.randint(-5,5),0,True,255)
                    pargr.add(par)
        if sett.hp <= 0 and not(g):
            g = True
            #trim = 150
            #par = Particle(sizen*16,sizen*12,WIDTH/2,
            
            #HEIGHT/2,(0,0,0),2,1000,0,0,False,0)
            #pargr.add(par)
            sett.Game_Started = False
        if trim >= 0:
            trim -= 1
        if trim == 0:
            for y in range(random.randint(3,11)):
                par = Particle(2,2,WIDTH/2 + random.randint(-sizen//2,sizen//2),
                HEIGHT/2 + random.randint(-sizen//2,sizen//2),(192 + random.randint(-16,16),0,0),-3,500,random.randint(-5,5),0,True,255)
                pargr.add(par)
        '''t = False'''
        clock.tick(FPS)
        for event in pygame.event.get():
            # check for closing window
            
            if event.type == pygame.QUIT:
                ru = False
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE):
                ru = False          
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_w):
                sett.move = [False,False,False,False]
                sett.move[0]= True
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_a):
                sett.move = [False,False,False,False]
                sett.move[1]= True
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_s):
                sett.move = [False,False,False,False]
                sett.move[2]= True
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_d):
                sett.move = [False,False,False,False]
                sett.move[3]= True
            if (event.type == pygame.KEYUP) and (event.key == pygame.K_w):
                sett.move[0]= False
            if (event.type == pygame.KEYUP) and (event.key == pygame.K_a):
                sett.move[1]= False
            if (event.type == pygame.KEYUP) and (event.key == pygame.K_s):
                sett.move[2]= False
            if (event.type == pygame.KEYUP) and (event.key == pygame.K_d):
                sett.move[3]= False
             
        if sett.Game_Started:
            und.update()    
            enem.update()   
            obj.update()  
            pargr.update()
            UI.update()  
        screen.fill((0,0,0))
        if sett.Game_Started:
            screen.fill((0,210,0))
            und.draw(screen)
            enem.draw(screen)
            obj.draw(screen)
            pargr.draw(screen)
            UI.draw(screen)
        
        # После отрисовки всего, переворачиваем экран
        pygame.display.flip()