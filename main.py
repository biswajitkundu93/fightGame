import pygame
from pygame.locals import *
import random
import button
import time



pygame.init()

clock = pygame.time.Clock()
fps = 60

#game window
bottom_pannel = 150
screen_width = 800
screen_height = 400 + bottom_pannel

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Fight by Biswajit Kundu")


#define game veriable
current_fighter = 1
total_fighter = 3
action_cooldown = 0
action_wait_time = 90
clicked = False
attack = False
potion = False
potion_effect = 15
game_over = 0



#defind font
font = pygame.font.SysFont("Times New Roman", 26)

#defind color
red = (255, 0, 0)
green = ( 0, 255, 0)
blue = ( 0, 0, 255)
white = (255, 255, 255)

#load all image 
#background
background_img = pygame.image.load("img/Background/background.png").convert_alpha()
#panel image
pannel_img = pygame.image.load("img/Icons/panel.png").convert_alpha()

#sword image
sword_img = pygame.image.load("img/Icons/sword.png").convert_alpha()
sword_img = pygame.transform.scale(sword_img,(int(sword_img.get_width()*0.5), int(sword_img.get_height()*0.5)))


#victory and defeat image
victory_img = pygame.image.load("img/Icons/victory.png").convert_alpha()
defeat_img = pygame.image.load("img/Icons/defeat.png").convert_alpha()


#button image
potion_img = pygame.image.load('img/Icons/potion.png')
restart_img = pygame.image.load('img/Icons/restart.png')

#create function for text
def draw_text(text, font, text_col, x, y):  
    img = font.render(text,True,text_col)
    screen.blit(img, (x,y))


#function for background show
def draw_background():  
    screen.blit(background_img, (0, 0)) 

#function for pannel show
def draw_pannel():  
    screen.blit(pannel_img, (0, screen_height-bottom_pannel))
    draw_text(f"{knight.name} HP : {knight.hp}", font, white, 100, screen_height-bottom_pannel+10 )
    for count, i in enumerate(bandit_list):  
        draw_text(f"{i.name} HP : {i.hp}", font, blue, 550, (screen_height-bottom_pannel+10) + count*60 )



#fighter class 
class Fighter():  
    def __init__(self, x, y, name, max_hp, strength, potions):  
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.potions = potions
        self.start_potions = potions
        self.alive = True 

        self.animation_list = []
        self.action = 0 
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        #loads Ideal images
        temp_list = []
        for i in range(8):
            image = pygame.image.load(f'img/{self.name}/Idle/{i}.png')
            image = pygame.transform.scale(image, (int(image.get_width()*1.5), int(image.get_height()*1.5) ))
            temp_list.append(image)
        self.animation_list.append(temp_list)
        
        #loads attract images
        temp_list = []
        for i in range(8):
            image = pygame.image.load(f'img/{self.name}/Attack/{i}.png')
            image = pygame.transform.scale(image, (int(image.get_width()*1.5), int(image.get_height()*1.5) ))
            temp_list.append(image)
        self.animation_list.append(temp_list)
        
        #loads Hurt images
        temp_list = []
        for i in range(3):
            image = pygame.image.load(f'img/{self.name}/Hurt/{i}.png')
            image = pygame.transform.scale(image, (int(image.get_width()*1.5), int(image.get_height()*1.5) ))
            temp_list.append(image)
        self.animation_list.append(temp_list)

        #loads Death images
        temp_list = []
        for i in range(10):
            image = pygame.image.load(f'img/{self.name}/Death/{i}.png')
            image = pygame.transform.scale(image, (int(image.get_width()*1.5), int(image.get_height()*1.5) ))
            temp_list.append(image)
        self.animation_list.append(temp_list)
        


        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        animation_cooldown = 100
        #handel animation
        #update image 
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown: 
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        
        if self.frame_index >= len(self.animation_list[self.action]):  
            if self.action == 3:  
                self.frame_index = len(self.animation_list[self.action])-1
            else : 
                self.idle()

    
    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    
    def hurt(self):
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    
    def death(self):
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def reset(self):
        self.alive = True
        self.potions = self.start_potions
        self.frame_index = 0
        self.hp = self.max_hp
        self.action = 0
        self.update_time = pygame.time.get_ticks()       

    def attack(self, target):
        # self.rect.center = target.rect.center
        rand = random.randint(-5,5)
        damge = self.strength + rand
        target.hp -= damge
        target.hurt()
        if target.hp < 1:
            target.hp = 0
            target.death()
            target.alive = False
        damage_text = DamageText(target.rect.centerx, target.rect.y, str(damge), red)
        damage_text_group.add(damage_text)
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        
    def draw(self):  
        screen.blit(self.image, self.rect)

class HealthBar(): 
    def __init__(self, x, y, hp, max_hp): 
        self.x = x
        self.y = y 
        self.hp = hp 
        self.max_hp = max_hp

    def draw(self, hp):
        self.hp = hp 

        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, green, (self.x, self.y, 150*ratio, 20))


class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.counter = 0

    def update(self):  
        self.rect.y -= 1
        self.counter += 1
        if self.counter > 30 :  
            self.kill()

damage_text_group = pygame.sprite.Group()


knight =  Fighter(200, 300, 'Knight', 30, 10, 3)
bandit1 = Fighter(550, 300, 'Bandit', 20, 6, 1)
bandit2 = Fighter(700, 300, 'Bandit', 20, 6, 1)

bandit_list = []
bandit_list.append(bandit1)
bandit_list.append(bandit2)

knight_health_bar = HealthBar(100, screen_height-bottom_pannel+40, knight.hp, knight.max_hp)
bandit1_health_bar = HealthBar(550, screen_height-bottom_pannel+40, bandit1.hp, bandit1.max_hp)
bandit2_health_bar = HealthBar(550, screen_height-bottom_pannel+100, bandit2.hp, bandit2.max_hp)

potion_button = button.Button(screen, 100, screen_height-bottom_pannel+70, potion_img, 64,64)
restart_button = button.Button(screen, 330, 120, restart_img, 120,30)

run = True
while run:  

    clock.tick(fps)

    #draw background
    draw_background()

    #draw pannel
    draw_pannel()
    knight_health_bar.draw(knight.hp)
    bandit1_health_bar.draw(bandit1.hp)
    bandit2_health_bar.draw(bandit2.hp)

    #draw fighter
    knight.draw()
    knight.update()

    #draw bandit_list
    for bandit in bandit_list:  
        bandit.draw()
        bandit.update()

    #damage text
    damage_text_group.update()
    damage_text_group.draw(screen)


    #reset
    attack = False
    potion = False
    target = False

    pygame.mouse.set_visible(True)
    pos = pygame.mouse.get_pos()
    for count, bandit in enumerate(bandit_list):
        if bandit.rect.collidepoint(pos):  
            pygame.mouse.set_visible(False)
            screen.blit(sword_img, pos)
            if clicked == True and bandit.alive == True:  
                attack = True
                target = bandit_list[count]
    
    if potion_button.draw():  
        potion = True

    draw_text(str(knight.potions), font, red, 150, screen_height-bottom_pannel+70)

    if game_over == 0:    
        if knight.alive == True:
            if current_fighter == 1:  
                action_cooldown += 1 
                if action_cooldown > action_wait_time : 
                    if attack == True and target != None:
                        knight.attack(target)
                        current_fighter += 1 
                        action_cooldown = 0
                    if potion == True :  
                        if knight.potions > 0: 
                            if knight.max_hp - knight.hp > potion_effect:  
                                heal_amount = potion_effect
                            else:
                                heal_amount = knight.max_hp - knight.hp
                            knight.hp += heal_amount
                            knight.potions -= 1
                            damage_text = DamageText(knight.rect.centerx, knight.rect.y, str(heal_amount), green)
                            damage_text_group.add(damage_text) 
                            current_fighter += 1
                            action_cooldown = 0
        else :  
            game_over = -1

        for count,bandit in enumerate(bandit_list):
            if current_fighter == 2 + count:  
                if bandit.alive == True:
                    action_cooldown += 1 
                    if action_cooldown >= action_wait_time:
                        if (bandit.hp / bandit.max_hp) < 0.5 and bandit.potions > 0:  
                            if bandit.max_hp - bandit.hp > potion_effect:  
                                heal_amount = potion_effect
                            else:
                                heal_amount = bandit.max_hp - bandit.hp
                            bandit.hp += heal_amount
                            bandit.potions -= 1 
                            damage_text = DamageText(bandit.rect.centerx, bandit.rect.y, str(heal_amount), green)
                            damage_text_group.add(damage_text) 
                            current_fighter += 1
                            action_cooldown = 0
                        else:  
                            bandit.attack(knight)
                            current_fighter += 1
                            action_cooldown = 0
                else : 
                    current_fighter += 1


        if current_fighter > total_fighter: 
            current_fighter = 1

    alive_bandits = 0
    for bandit in bandit_list:
        if bandit.alive == True:  
            alive_bandits += 1
    
    if alive_bandits == 0 :  
        game_over = 1

    if game_over != 0:  
        if game_over == 1:  
            screen.blit(victory_img, (250, 50))
        if game_over == -1:  
            screen.blit(defeat_img, (290, 50))
        if restart_button.draw():  
            knight.reset()
            for bandit in bandit_list:
                bandit.reset()
            current_fighter = 1
            action_cooldown = 0
            game_over = 0
    
    #handel event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        else:  
            clicked = False

    pygame.display.update()
pygame.quit()