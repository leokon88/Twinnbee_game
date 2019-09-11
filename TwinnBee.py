import pygame

windowHeight =600
windowWidth =400
margin =5 #offset from the edge
playerSpeed=1

wallTop = margin
wallLeft = margin
wallRight =windowWidth - margin
wallBottom =windowHeight - margin

backgroundColor=(50,50,200) #initially set background color -blue

pygame.init()
clock=pygame.time.Clock() 

window = pygame.display.set_mode((windowWidth,windowHeight)) # tuple
pygame.display.set_caption('Twin Bee')

playerImg =pygame.image.load('images/twinbee.png')

class Player:
    def __init__(self, img, speed):
        self.img = img
        self.xcoor= windowWidth/2 -img.get_width()/2  #centering the player
        self.ycoor= windowHeight *.80 # initially set player on 8/10 of the window at bottom
        self.isAlive=True
        self.speed = speed 
        self.ydir=0
        self.xdir=0

    def show(self):
        window.blit(self.img,(self.xcoor,self.ycoor)) #display image onto window

    def move(self):
        newX = self.xcoor + self.xdir*self.speed
        if(newX>=wallLeft and newX <= wallRight-self.img.get_width()):
            self.xcoor =newX
        else:
            self.xcoor=self.xcoor

        newY = self.ycoor + self.ydir*self.speed 
        if(newY>=wallTop and newY <= wallBottom-self.img.get_height()):
            self.ycoor =newY
        else:
            self.ycoor=self.ycoor
        self.show()

player=Player(playerImg, playerSpeed)
leftKeyPressed= False
rightKeyPressed =False
upKeyPressed= False
downKeyPressed =False

quitGame=False

while(True):
    for event in pygame.event.get():
        if event.type==pygame.KEYDOWN:
            if event.key ==pygame.K_ESCAPE:
                quitGame=True
            elif event.key == pygame.K_LEFT:
                player.xdir = -1
                leftKeyPressed = True
            elif event.key  == pygame.K_RIGHT:
                player.xdir = 1
                RightKeyPressed = True
            elif event.key  == pygame.K_UP:
                player.ydir = -1
                upKeyPressed = True
            elif event.key  == pygame.K_DOWN:
                player.ydir = 1
                downKeyPressed = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                upKeyPressed= False
                if not downKeyPressed:
                    player.ydir= 0
            elif event.key == pygame.K_DOWN:
                downKeyPressed= False
                if not upKeyPressed:
                    player.ydir= 0
            elif event.key == pygame.K_LEFT:
                leftKeyPressed= False
                if not rightKeyPressed:
                    player.xdir= 0
            elif event.key == pygame.K_RIGHT:
                rightKeyPressed= False
                if not leftKeyPressed:
                    player.xdir= 0

    window.fill(backgroundColor)
    player.move()
    pygame.display.update()

    clock.tick(60)


 