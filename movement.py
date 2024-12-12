import pygame, sys
import spritesheet
import random
import math


class Fruit(pygame.sprite.Sprite): #might just do a boss run game cuz swarms r boring
    def __init__(self):
        super().__init__()
        temp = random.randint(1, 2)
        if temp == 1:
            self.pos = [random.randint(20,1180), 20]
        else:
            self.pos = [20, random.randint(20, 780)]
        self.image = pygame.image.load('graphics/apple.png').convert_alpha()
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
        
    
class Slash():
    def __init__(self, x, y, face_right):
        
        super().__init__()
        self.pos = [x,y]
        self.facing_right = face_right
        if self.facing_right:
            self.hitbox = pygame.Rect(self.pos[0] + 100, self.pos[1] + 55, 100, 70)
        else:
            self.hitbox = pygame.Rect(self.pos[0], self.pos[1] + 55, 100, 70)

        self.initial = pygame.time.get_ticks()
    
    def get_hitbox(self):
        return self.hitbox
    
    def set_pos(self, x, y):
        self.pos = [x, y]
        self.hitbox = pygame.Rect(self.pos[0] + 100, self.pos[1] + 55, 90, 70)
    
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pos = [100, 100]
        self.score = 0
        
        # self.run_sprites = [pygame.image.load(f'run_{i}.png') for i in range(1, 9)]#sprites for run animation
        # self.attack_sprites = [pygame.image.load(f'attack_{i}.png') for i in range(1,6)]

        run_spritesheet_image = pygame.image.load('graphics/run_spritesheet.png')
        run_spritesheet = spritesheet.SpriteSheet(run_spritesheet_image)
        self.run_sprites = []
        for i in range(8):
            self.run_sprites.append(run_spritesheet.get_image(i, 200, 200, 1, (0, 0, 0)))

        attack_spritesheet_image = pygame.image.load('graphics/attack_spritesheet.png')
        attack_spritesheet = spritesheet.SpriteSheet(attack_spritesheet_image)
        self.attack_sprites = []
        for i in range(3):
            self.attack_sprites.append(attack_spritesheet.get_image(i+2, 200, 200, 1, (0, 0, 0)))

        self.idle_image = pygame.image.load('graphics/idle.png')
        self.current_sprite = 0
        self.run_animation = False
        self.attack_animation = False
        self.facing_right = True
        self.image = self.idle_image
        self.rect = self.image.get_rect(topleft=self.pos)

        self.hitbox = pygame.Rect(self.pos[0] + 106 - (37/2), self.pos[1] + 106 - (52/2), 29, 46)

        self.hp = 100
    
    def attack(self):
        global slash
        self.attack_animation = True
        self.run_animation = False
    
    def move(self):
        #if not self.attack_animation:
        keys = pygame.key.get_pressed()
        if not keys[pygame.K_SPACE]:
            if keys[pygame.K_a]: 
                self.pos[0] -= 5
                self.rect.x -= 5
                if self.facing_right: 
                    self.facing_right = False
                    self.flip_sprites()
            if keys[pygame.K_d]: 
                self.pos[0] += 5
                self.rect.x += 5
                if not self.facing_right:
                    self.facing_right = True
                    self.flip_sprites()
            if keys[pygame.K_s]:
                self.pos[1] += 5
                self.rect.y += 5
            if keys[pygame.K_w]:
                self.pos[1] -= 5
                self.rect.y -= 5
        else:
            self.attack()
        self.rect.topleft = self.pos
        self.run_animation = any(keys[key] for key in (pygame.K_a, pygame.K_d, pygame.K_s, pygame.K_w)) #if wasd pressed animation=true
        if (self.run_animation):
            self.attack_animation = False
        #else:
        #    self.attack()
        
        self.hitbox = pygame.Rect(self.rect.x + 106 - (37/2), self.rect.y + 106 - (52/2), 29, 46)
        
    #im gonna make it so that if you are attacking it disables reading keyboard inputs

    def flip_sprites(self): #flips all images
        self.run_sprites = [pygame.transform.flip(sprite, True, False).convert_alpha() for sprite in self.run_sprites]
        self.attack_sprites = [pygame.transform.flip(sprite, True, False).convert_alpha() for sprite in self.attack_sprites]
        self.idle_image = pygame.transform.flip(self.idle_image, True, False).convert_alpha()

    def update(self, speed):
        self.move()
        if self.run_animation:
            self.current_sprite += speed
            if int(self.current_sprite) >= len(self.run_sprites):
                self.current_sprite = 0
            self.image = self.run_sprites[int(self.current_sprite)]
        elif self.attack_animation:
            speed = 0.125
            self.current_sprite += speed
            if int(self.current_sprite) >= len(self.attack_sprites):
                self.current_sprite = 0 
                self.attack_animation = False
            self.image = self.attack_sprites[int(self.current_sprite)]
        else:
            self.image = self.idle_image
            self.current_sprite = 0


    def get_hitbox(self):
        return self.hitbox
    
    def get_attack_anim(self):
        return self.attack_animation
    
    def get_pos(self):
        return self.pos
    
    def get_facing_right(self):
        return self.facing_right
    
    def check_collision(self, collide):
        if collide:
            self.hp -= 15
            print(self.hp)
            self.check_death()
            print ('hit by fruit')

    def check_death(self):
        global game_active
        if self.hp < 0:
            game_active = False
            moving_sprites.empty()
            print("you died") #finish later


pygame.init()
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
screen_width, screen_height = 1200, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("fruit ninja")

player_group =  pygame.sprite.GroupSingle()
player = Player()
player_group.add(Player())

# Creating the sprites and groups
moving_sprites = pygame.sprite.Group()
slash = Slash(90000, 90000, True)
moving_sprites.add(Fruit())

# Start screen
game_name = test_font.render('Apple Ninja',False,(111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = test_font.render('Press space to run',False,(111,196,169))
game_message_rect = game_message.get_rect(center = (400,330))


# Timer 
apple_timer = pygame.USEREVENT + 1
pygame.time.set_timer(apple_timer,1200)

ticks_counter = []
#game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_active:
            if event.type == apple_timer:
                moving_sprites.add(Fruit())
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_active = True
                    player_group.sprites()[0].hp = 100


    if game_active:
        for fruit in moving_sprites.sprites():
            collide_fp = player_group.sprites()[0].get_hitbox().colliderect(fruit.get_hitbox())
            fruit.check_collision(collide_fp)
            player_group.sprites()[0].check_collision(collide_fp)

        if (player_group.sprites()[0].get_attack_anim()):
            for fruit in moving_sprites.sprites():
                collide_fa = slash.get_hitbox().colliderect(fruit.get_hitbox())
                if collide_fa:
                    player.score += 5
                fruit.check_collision(collide_fa)


        if(player_group.sprites()[0].get_attack_anim()):
            ticks_counter.append(pygame.time.get_ticks())
            if ticks_counter[len(ticks_counter) - 1] - ticks_counter[0] >= 200:
                slash = Slash(player_group.sprites()[0].get_pos()[0], player_group.sprites()[0].get_pos()[1], player_group.sprites()[0].get_facing_right())
        else:
            slash.set_pos(90000, 90000)
            ticks_counter.clear()

        #draw
        screen.fill((0, 0, 0))

        # pygame.draw.rect(screen, (0,0,255), slash.get_hitbox(), 2)
        # for p in player_group.sprites():
        #     pygame.draw.rect(screen, (111, 0, 80), p.get_hitbox(), 3)
        
        player_group.draw(screen)
        player_group.update(0.25)

        moving_sprites.draw(screen)
        moving_sprites.update()
        
        # for a in moving_sprites.sprites():
        #     pygame.draw.rect(screen, (12, 155, 0), a.get_hitbox(), 3)

    else:
        screen.fill(((94,129,162)))
        score_message = test_font.render(f'Your score: {player.score}',False,(111,196,169))
        score_message_rect = score_message.get_rect(center = (400,330))
        screen.blit(game_name,game_name_rect)
        
        if player.score == 0 and player_group.sprites()[0].hp == 100: 
            screen.blit(game_message,game_message_rect)
        else: 
            screen.blit(score_message,score_message_rect)

    pygame.display.update()
    clock.tick(60)