import pygame
import random
import math


class Fruit(pygame.sprite.Sprite): #might just do a boss run game cuz swarms r boring
    def __init__(self, type):
        super().__init__()
        temp = random.randint(1, 2)
        if temp == 1:
            self.pos = [random.randint(20,1180), 20]
        else:
            self.pos = [20, random.randint(20, 780)]

        if type == 'apple':  
            self.image = pygame.image.load('graphics/apple.png').convert_alpha()
        elif type == 'melon':
            self.image = pygame.image.load('graphics/melon.png').convert_alpha()
        else:
            self.image = pygame.image.load('graphics/strawberry.png').convert_alpha()

        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 0.15, self.image.get_height() * 0.15))
        self.rect = self.image.get_rect(topleft=self.pos)
        self.speed = 5
        self.hitbox = pygame.Rect(self.pos[0] + 2, self.pos[1] + 2, 30, 34)
        self.direction = random.randint(0,60)
        self.speed_x = self.speed * math.cos(self.direction * math.pi / 180)
        self.speed_y = self.speed * math.sin(self.direction * math.pi / 180)

    def get_hitbox(self):
        return self.hitbox
    
    def check_collision(self, collide):
        if collide:
            self.hitbox = pygame.Rect(10000, 10000, 32, 36) #is this a stupid way to do things
            print ('hit by player')
            self.kill()

    def fruit_movement(self):
        if self.rect.x <= 0 or self.rect.x >= 1190:
            self.speed_x *= -1
        if self.rect.y <= 0 or self.rect.y >= 575:
            self.speed_y *= -1
        
        self.rect.x += (int)(self.speed_x)
        self.rect.y += (int)(self.speed_y)

        self.hitbox =  pygame.Rect(self.rect.x + 2, self.rect.y + 2, 30, 34)

    def update(self):
        self.fruit_movement()