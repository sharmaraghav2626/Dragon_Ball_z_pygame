import pygame
import random
from pygame import *
import os
import time
# from base import Base
pygame.init()
pygame.mixer.init()


gravity=0.6

# Colors
black = (0,0,0)
white = (255,255,255)
red = (255, 0, 0)
blue = (0, 0, 128)

# Display
screen_width=700
screen_height=350
screen_size=(screen_width,screen_height)
screen=pygame.display.set_mode(screen_size)
pygame.display.set_caption("Dragon Ball Z")
clock=pygame.time.Clock()

fps=80

font=pygame.font.SysFont(name=None,size=30,italic=1)

# Sounds
jump_sound = pygame.mixer.Sound('sprites/sounds/jump.wav')
die_sound = pygame.mixer.Sound('sprites/sounds/die.wav')
checkPoint_sound = pygame.mixer.Sound('sprites/sounds/checkPoint.wav')
power_sound=pygame.mixer.Sound('sprites/sounds/power.wav')

# To blit Text on screen
def text_screen(text,color,x,y):
    text=font.render(text,True,color)
    screen.blit(text,(x,y))

# Function that load image and return image file and image.rect
def loadimage(name,sizex=-1,sizey=-1,colorkey=None):
    fullname=os.path.join('sprites',name)
    image=pygame.image.load(fullname).convert_alpha()

    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)


    if sizex != -1 or sizey != -1:
        image=pygame.transform.scale(image,(sizex,sizey))
    return (image,image.get_rect())

# Function to load spritesheett and return image flie list 
def loadspritesheet(name,nx=1,ny=1,sizex=-1,sizey=-1,colorkey=None):
    
    fullname = os.path.join('sprites',name)
    sheet = pygame.image.load(fullname)
    sheet = sheet.convert_alpha()
    sheet_rect = sheet.get_rect()

    sprites = []

    size_nx = sheet_rect.width/nx
    size_ny = sheet_rect.height/ny

    for i in range(0,ny):
        for j in range(0,nx):
            rect = pygame.Rect((j*size_nx,i*size_ny,size_nx,size_ny))
            image = pygame.Surface(rect.size)
            image = image.convert()
            image.blit(sheet,(0,0),rect)

            if colorkey is not None:
                if colorkey is -1:
                    colorkey = image.get_at((0,0))
                image.set_colorkey(colorkey,RLEACCEL)

            if sizex != -1 or sizey != -1:
                image = pygame.transform.scale(image,(sizex,sizey))

            sprites.append(image)

    sprite_rect = sprites[0].get_rect()

    return sprites,sprite_rect


class Base :
    def __init__(self,name='base1',screen=None,speed=-4):
    
        self.image,self.rect = loadimage(name,screen_width+100,100,None)
        self.image1,self.rect1 = loadimage(name,screen_width+100,100,None)
        self.rect.bottom = screen_height
        self.rect1.bottom = screen_height
        self.rect1.left = self.rect.right
        self.speed = speed*1.27

    def draw(self):
        screen.blit(self.image,self.rect)
        screen.blit(self.image1,self.rect1)

    def update(self):
        self.rect.left += self.speed
        self.rect1.left += self.speed

        if self.rect.right < 0:
            self.rect.left = self.rect1.right

        if self.rect1.right < 0:
            self.rect1.left = self.rect.right
    
class Obstacles(pygame.sprite.Sprite):
    def __init__(self,speed=-4,sizex=-1,sizey=-1):
        pygame.sprite.Sprite.__init__(self,self.containers)
        
        self.images,self.rect = loadspritesheet('cacti-small.png',3,1,sizex,sizey,-1)
        self.imagesb1, self.rectb1 = loadspritesheet('cacti-big.png', 2, 1, int(sizex*1.5), int(sizey*1.2), -1)
        self.imagesb2, self.rectb2 = loadspritesheet('cacti-big.png', 2, 1, int(sizex * 1.7),int(sizey*1.2), -1)
        self.imageo1,self.recto1 = loadimage('obstacle1.png',int(sizex*1.5),int(sizey*1.2),-1)
        self.imageo2, self.recto2 = loadimage('obstacle2.png',int(sizex*1.5),int(sizey*1.2), -1)
        
        self.rect.bottom = int(0.98*screen_height-90)
        self.rect.left = screen_width + self.rect.width
        self.rectb1.bottom = int(0.98 * screen_height-90)
        self.rectb1.left = screen_width + self.rect.width
        self.rectb2.bottom = int(0.98 * screen_height-90)
        self.rectb2.left = screen_width + self.rect.width
       
        image_list=[self.imagesb1[0] , self.images[random.randrange(0,3)] , self.imagesb2[1]]
        self.image = random.choice(image_list)
        self.movement = [-1*speed,0]

    def draw(self):
        screen.blit(self.image,self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)

        if self.rect.right < 0:
            self.kill()

class Cloud(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image,self.rect = loadimage('cloud.png',int(90*30/42),30,-1)
        self.speed = 1
        self.rect.left = x
        self.rect.top = y
        self.movement = [-1*self.speed,0]

    def draw(self):
        screen.blit(self.image,self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)
        if self.rect.right < 0:
            self.kill()

class Ptera(pygame.sprite.Sprite):
    def __init__(self,speed=5,sizex=-1,sizey=-1):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.images,self.rect = loadspritesheet('ptera.png',2,1,sizex,sizey,-1)
        self.ptera_height =[screen_height*0.35, screen_height*0.65 , screen_height*0.51]
        self.rect.centery = self.ptera_height[random.randrange(0,3)]
        self.rect.left = screen_width + self.rect.width
        self.image = self.images[0]
        self.movement = [-1*speed,0]
        self.index = 0
        self.counter = 0

    def draw(self):
        screen.blit(self.image,self.rect)

    def update(self):
        if self.counter % 10 == 0:
            self.index = (self.index+1)%2
        self.image = self.images[self.index]
        self.rect = self.rect.move(self.movement)
        self.counter = (self.counter + 1)
        if self.rect.right < 0:
            self.kill()

class Player():
    def __init__(self,sizex=-1,sizey=-1):
        self.images,self.rect = loadspritesheet('player1.png',4,1,sizex,sizey,-1)
        self.images1,self.rect1 = loadspritesheet('player1.png',4,1,int(sizex*0.6),int(sizey*0.6),-1)
        self.rect.bottom = int(screen_height-82)
        self.rect.left = 19
        self.rect1.bottom = int(screen_height-82)
        self.rect1.left = 19        
        self.image = self.images[0]
        self.index = 0
        self.counter = 0
        self.isjumping = False
        self.isDead = False
        self.isdown = False
        self.movement = [0,0]
        self.jumpspeed = 15
        self.isWaterFall=False
        self.stand_size=(sizex,sizey)
        self.down_size=(int(sizex*0.6),int(sizey*0.6))
        
    def draw(self):
        screen.blit(self.image,self.rect)

    def checkbounds(self):
        if self.rect.bottom > int(screen_height-85):
            self.rect.bottom = int(screen_height-82)
            self.isJumping = False
            self.movement[1]=0
    def update(self):
        
        if self.isjumping:
            self.movement[1] = self.movement[1] + gravity
        

        if not self.isdown:
            self.image = self.images[self.index]
            self.rect.width,self.rect.height = self.stand_size
            self.jumpspeed=15
        else:
            self.image = self.images1[(self.index)]
            self.rect.width ,self.rect.height= self.down_size
            self.jumpspeed=12


        
        if self.counter % 12 == 0:
            self.index = (self.index + 1)%3
        
        self.rect = self.rect.move(self.movement)
        self.checkbounds()    
        self.counter = (self.counter + 1)

class Themes:
    
    def __init__(self,speed):
        self.gamespeed=speed
        self.theme=['bg1 base1','bg2 base2','bg3 base3','bg4 base4']
        self.background=[]
        self.base=[]
        for i in range(len(self.theme)):
            self.name=self.theme[i].split(' ')
            self.bg,self.bg_rect=loadimage('background\\'+self.name[0]+'.jpg',screen_width,screen_height, None) 
            self.bs=Base('background\\'+self.name[1]+'.jpg',screen,-1*self.gamespeed)
            self.background.append(self.bg)
            self.base.append(self.bs)
        
        self.bgimage=self.background[0]
        self.bsimage=self.base[0]
        self.index=0
        self.counter=0
        self.bg_rect.top=0
        self.bg_rect.left=0
                
    def draw(self):
        screen.blit(self.bgimage,self.bg_rect)                
        self.bsimage.draw()
        
    def update(self):        
        
                
        if self.counter %400 == 0 and self.counter !=0:
            
            if self.index<(len(self.theme)-1):
                self.index=self.index+1
            else:
                self.index=0         
        
        self.bgimage=self.background[self.index]
        self.bsimage=self.base[self.index]
        self.bsimage.update()    
        self.counter=self.counter+1
        
class Coins(pygame.sprite.Sprite):

    def __init__(self,speed=4,sizex=-1,sizey=-1):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.images,self.rect = loadspritesheet('coin.png',6,1,sizex,sizey,-1)
        self.image=self.images[0]
        self.index=0
        self.counter=0    
        self.rect.left = screen_width + self.rect.width
        self.imageheight=[screen_height*0.35, screen_height*0.65 , screen_height*0.51]
        self.rect.top=self.imageheight[random.randrange(0,3)]
        self.movement = [-1*speed,0]

    def draw(self):
        screen.blit(self.image,self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)
        if self.counter % 7 ==0:
            self.index=self.index+1
            if self.index == len(self.images):
                self.index=0        
        
        self.image=self.images[self.index]
        if self.rect.right < 0:
            self.kill()
        self.counter=self.counter+1

class Waterfall(pygame.sprite.Sprite):

    def __init__(self,speed=4):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.images,self.rect = loadspritesheet('waterfall.png',4,1,80,105,-1)
        self.index=0
        self.counter=0
        self.image=self.images[0]    
        self.rect.left = screen_width + self.rect.width
        self.rect.bottom=screen_height
        self.movement = [-1*speed,0]

    def draw(self):
        screen.blit(self.image,self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)
        if self.counter % 5 == 0:
            self.index=self.index+1
            if self.index == len(self.images):
                self.index=0        
        
        self.image=self.images[self.index]
        if self.rect.right < 0:
            self.kill()
        self.counter=self.counter+1
  
class Power:
    def __init__(self,speed):
        self.images,self.rect=loadspritesheet('power.png',4,2,85,80,-1)
        self.index=0
        self.rect.left=35
        self.rect.bottom=int(screen_height-95)
        self.image=self.images[0]
        self.counter=0
        self.movement=[speed,0]
        self.isPower=False
    def draw(self):
        if self.isPower:
            screen.blit(self.image,self.rect)

    def update(self):
        if self.isPower:
            if(self.counter % 12) == 0:
                self.index=self.index+1
                if self.index == len(self.images):
                    self.index=0       
            self.image=self.images[self.index]
            self.rect=self.rect.move(self.movement)
            self.counter=self.counter+1 
            if self.rect.left > screen_width:
                self.rect.left=35
                self.counter=0
                self.isPower=False    

class Asset(pygame.sprite.Sprite):
    def __init__(self,speed=5):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image,self.rect=loadimage('shootpower.png',40,40,-1)
        self.rect.left=screen_width
        self.heights=random.randrange(int(screen_height*0.35),int(screen_height*0.65))
        self.rect.bottom=self.heights   
        self.movement=[-1*speed,0]
    def draw(self):
        screen.blit(self.image,self.rect)
    
    def update(self):
        self.rect=self.rect.move(self.movement)
        if self.rect.right<0:
            self.kill()


# Function for Welcome Screen
def introScreen():
    pass
    exitscreen=False
    isGameStart=False
    
    musicplayed=False    

    str='Press Enter To Play'

    while not exitscreen:


        background,background_rect=loadimage('introbackground.jpg',screen_width,screen_height,-1)
        background_rect.left=0
        background_rect.top=0

        logo,logo_rect=loadimage('logo.png',200,70,-1)
        logo_rect.centerx=screen_width*0.2
        logo_rect.centery=screen_height*0.2
        
        player,player_rect=loadimage('playerintro.png',140,250,-1)
        player_rect.centerx=screen_width*0.76
        player_rect.centery=screen_height*0.45
        
        for event in pygame.event.get():   
            if event.type == pygame.QUIT:
                exitscreen=True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN or event.key == pygame.K_UP:
                    isGameStart=True

        if pygame.display.get_surface() != None:
            screen.blit(background,background_rect)
            screen.blit(player,player_rect)
            screen.blit(logo,logo_rect)
            text_screen(str,blue,screen_width*0.7,screen_height*0.93)

        if(pygame.mixer.get_init() !=None and musicplayed==False):
            musicplayed=True
            pygame.mixer.music.load('sprites/sounds/welcome.mp3')
            pygame.mixer.music.play()
        
        
        pygame.display.update()
        clock.tick(fps)
        if isGameStart:
            pygame.mixer.music.stop()
            return True    

#Game Loop Starts here
def gameLoop():
    exitgame=False
    game_over=False
    
    gamespeed=4
    
    
    theme=Themes(gamespeed)
    score=0
    counter=0


    isShootpower=False
    shootpowercounter=0
    
    player=Player(60,110)
    power=Power(gamespeed)
    player.isjumping=True
    player.movement[1] = -1*player.jumpspeed
    last_obstacle = pygame.sprite.Group()
    obstacle=pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    pteras=pygame.sprite.Group()
    coins=pygame.sprite.Group()
    waterfall=pygame.sprite.Group()
    assets=pygame.sprite.Group()

    Waterfall.containers=waterfall
    Coins.containers=coins
    Obstacles.containers=obstacle
    Cloud.containers=clouds
    Ptera.containers=pteras
    Asset.containers=assets

    # Check if hiscore file exists
    if (not os.path.exists("hiscore.txt")):
        with open("hiscore.txt", "w") as f:
            f.write("0")

    with open("hiscore.txt", "r") as f:
        hiscore = int(f.read())

    
    
    while not exitgame:
                   
        if game_over:
            text_screen("Game Over! Press Enter To Continue", red, 250, 300)

            with open("hiscore.txt", "w") as f:
                f.write(str(hiscore))

            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:  
                    exitgame = True
                    break
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key==pygame.K_SPACE or event.key == pygame.K_UP:
                        die_sound.play()
                        gameLoop()

        else:
            for event in pygame.event.get():
                if(event.type==pygame.QUIT):
                    exitgame=True
                    break
                if event.type==pygame.KEYDOWN:
                    
                    if event.key == pygame.K_DOWN:
                        player.isdown=True
                    
                    if event.key==pygame.K_UP or event.key==pygame.K_SPACE:
                        if player.rect.bottom > 250 :
                            player.isjumping=True
                            if pygame.mixer.get_init() != None:
                                    jump_sound.play()
                            player.movement[1] = -1*player.jumpspeed
                    if event.key==pygame.K_RIGHT and isShootpower:
                        power.isPower=True
                        if pygame.mixer.get_init() != None:
                            power_sound.play()

                if event.type==pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        player.isdown=False            
            
            for c in obstacle:
                c.movement[0] = -1*gamespeed
                if  pygame.sprite.collide_mask(power,c) and power.isPower==True:
                    c.kill()
                if pygame.sprite.collide_mask(player,c):
                    player.isDead = True
                    if pygame.mixer.get_init() != None:
                        die_sound.play()
            
            for p in pteras:
                p.movement[0] = -1*gamespeed
                if  pygame.sprite.collide_mask(power,p) and power.isPower==True:
                    p.kill()
                if pygame.sprite.collide_mask(player,p):
                    player.isDead = True
                    if pygame.mixer.get_init() != None:
                        die_sound.play()
            for c in coins:
                c.movement[0] = -1*gamespeed
                if pygame.sprite.collide_mask(player,c):
                    c.kill()
                    score=score+10   
                    if pygame.mixer.get_init() != None:
                        checkPoint_sound.play()
            
            for w in waterfall:
                w.movement[0]=-1*gamespeed
                if pygame.sprite.collide_mask(player,w):
                    player.isWaterFall=True
                    player.isDead=True    
                    if pygame.mixer.get_init() != None:
                        die_sound.play()

            for a in assets:
                a.movement[0]=-1*gamespeed
                if pygame.sprite.collide_mask(player,a):
                    a.kill()
                    isShootpower=True
                    if pygame.mixer.get_init()!= None:
                        checkPoint_sound.play()    

            if len(clouds) < 5  and random.randrange(0,300) == 10:
                Cloud(screen_width,random.randrange(screen_height/5,screen_height/2))
            
            if len(obstacle) < 3:
                if len(obstacle) == 0:
                    last_obstacle.empty()
                    last_obstacle.add(Obstacles(gamespeed,40,40))
                else:
                    for l in last_obstacle:
                        if l.rect.right < screen_width*0.8 and random.randrange(0,100) == 10:
                            last_obstacle.empty()
                            last_obstacle.add(Obstacles(gamespeed, 40, 40))


            if len(pteras) == 0 and random.randrange(0,300) == 10 and counter > 400 :
                
                for l in last_obstacle:
                    if l.rect.right < screen_width*0.8:
                        last_obstacle.empty()
                        last_obstacle.add(Ptera(gamespeed, 46, 40))

            if len(coins) < 12 and random.randrange(0,600) == 10:
                Coins(gamespeed,30,30)
            
            if len(waterfall) ==0 and random.randrange(0,50) == 10:    
                for l in last_obstacle:
                    if l.rect.right < screen_width*0.8:
                        last_obstacle.empty()
                        last_obstacle.add(Waterfall(gamespeed))

            if len(assets) == 0 and random.randrange(0,1000) == 10:
                Asset(gamespeed)    
            
            if shootpowercounter < 400 and isShootpower:
                shootpowercounter=shootpowercounter+1
            else:
                shootpowercounter=0
                isShootpower=False

            obstacle.update()
            theme.update()
            clouds.update()
            pteras.update()
            player.update()
            coins.update()
            waterfall.update()
            power.update()
            assets.update()
            
            if pygame.display.get_surface() !=None:
                theme.draw()
                clouds.draw(screen)
                obstacle.draw(screen)
                pteras.draw(screen)    
                player.draw()
                coins.draw(screen)
                waterfall.draw(screen)
                power.draw()            
                assets.draw(screen)    
            if counter % 399==0:
                gamespeed=gamespeed+1
            
            if counter%15==0:
                if score %50 ==0:
                    checkPoint_sound.play()
                score=score+1
                if(hiscore<score): hiscore=score
            text_screen("Score: " + str(score) + "  Hiscore: " + str(hiscore), white,400 , 20)

            if player.isDead:
                game_over=True
            counter=counter+1    
        pygame.display.update()
        clock.tick(fps)
    pygame.quit()
    quit()


if __name__ == "__main__":
    isGameStart=introScreen()
    if isGameStart:
        gameLoop()
    