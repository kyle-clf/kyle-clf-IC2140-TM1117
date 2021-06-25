import pygame
import random
import pygame_gui

from pygame.locals import (
    K_SPACE,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    RLEACCEL,
)


pygame.init()



SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
life = 3
score = 0



screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()
pygame.display.set_caption('TM1117 Game')


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("helmet.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.surf = pygame.transform.scale(self.surf, (50, 50)) 
   


    def update(self, press_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)    
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
            
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
                   
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("popo.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )  
        self.speed = random.randint(5, 20)
        
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

    def sucide(self):
        self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self,w,y):
        super(Bullet,self).__init__()
        self.surf = pygame.image.load("bullet.png").convert()
        self.surf.set_colorkey((0,0,0),RLEACCEL)
     
        self.rect = self.surf.get_rect(center=(
                w,y)
            )
        self.speed = 5
    
    def update(self):
        self.rect.move_ip(self.speed,0)
        if self.rect.right > SCREEN_WIDTH:
                self.kill()
    
    def sucide(self):
        self.kill()



# menu

managerMenu = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
btnMapPoly = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),text='PolyU',manager=managerMenu)

btnMapCity = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275+100), (100, 50)),text='CityU',manager=managerMenu)


def showMenu(e):
    time_delta = clock.tick(60)/1000.0
    background = pygame.Surface((800, 600))
    background.fill(pygame.Color('#000000'))
    

 

    managerMenu.process_events(e)
    managerMenu.update(time_delta)
    screen.blit(background, (0, 0))
    managerMenu.draw_ui(screen)
    pygame.display.update()


# ui overlay
managerUI = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))





def showUI():
    time_delta = clock.tick(60)/1000.0
    pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 0), (100, 50)), text='Life ' + str(life),manager=managerUI)
    pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 50), (100, 50)), text='Score ' + str(score),manager=managerUI)
    

    if isEndGame:
        pygame_gui.elements.UILabel(relative_rect=pygame.Rect((100, 0), (100, 50)), text='!GG!' ,manager=managerUI)
    managerUI.update(time_delta)
   
    managerUI.draw_ui(screen)
    





runningApp = True
runningGame = False
isShowMenu = True
isEndGame = False

player = Player()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)


ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 500)






# sound
pygame.mixer.init()
pygame.mixer.music.load("bgm.mp3")
pygame.mixer.music.play(loops=-1)

collision_sound = pygame.mixer.Sound("col.mp3")

bgImg = ""


# main loop
while runningApp:

 

    
    for event in pygame.event.get():
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == btnMapPoly:
                    bgImg = "polyu.jpg"
                    runningGame = True
                    isShowMenu = False
                    
                if event.ui_element == btnMapCity:
                    bgImg = "cityu.png"
                    runningGame = True
                    isShowMenu = False
        
        if event.type == KEYDOWN:
            
            if event.key == K_ESCAPE:
                runningApp = False
            elif event.key==K_SPACE and runningGame:
                    bullet=Bullet(player.rect.x, player.rect.y)
                    bullets.add(bullet)
                    all_sprites.add(bullet)
                
                
        elif event.type == QUIT:
            runningApp = False
            
        elif event.type == ADDENEMY and runningGame:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        if isShowMenu:
            showMenu(event)

        
            
    if runningGame:
        screen.blit(pygame.image.load(bgImg).convert(), (0,0))        
        showUI()
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        
        if pygame.sprite.groupcollide(bullets,enemies,False,False):
        
            pygame.sprite.groupcollide(bullets,enemies,True,True)
            score = score + 1


        if pygame.sprite.spritecollideany(player, enemies):
            
            collision_sound.play()
            screen.fill((255, 0, 0))
            pygame.display.flip()
            pygame.time.delay(50)
            enemies = pygame.sprite.Group()
            all_sprites = pygame.sprite.Group()
            all_sprites.add(player)
            life = life - 1
        
       
            if life == 0:
                player.kill()
                screen.fill((0, 0, 0))
                runningGame = False
                isEndGame = True

         
                
        
        
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)   
        
        enemies.update()
        bullets.update()
    if isEndGame:
    
        showUI()


    clock.tick(120)
    pygame.display.flip()
    
    
      
    
pygame.quit()
