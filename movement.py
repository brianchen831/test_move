import pygame, sys
import spritesheet
class Fruit(pygame.sprite.Sprite): #might just do a boss run game cuz swarms r boring
    def __init__(self):
        super().__init__()
        self.pos = [500,200]
        self.image = pygame.image.load('apple.png')
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 0.15, self.image.get_height() * 0.15))
        self.rect = self.image.get_rect(topleft=self.pos)
        self.velocity = 10
        self.hitbox = pygame.Rect(self.pos[0], self.pos[1], 32, 36)

    def get_hitbox(self):
        return self.hitbox
    
    def check_collision(self, collide):
        if collide:
            self.hitbox = pygame.Rect(10000, 10000, 32, 36) #is this a stupid way to do things
            self.kill()
    
class Slash():
    def __init__(self, x, y, face_right):
        
        super().__init__()
        self.pos = [x,y]
        self.facing_right = face_right
        if self.facing_right:
            self.hitbox = pygame.Rect(self.pos[0] + 100, self.pos[1] + 55, 90, 70)
        else:
            self.hitbox = pygame.Rect(self.pos[0] + 10, self.pos[1] + 55, 90, 70)

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
        
        # self.run_sprites = [pygame.image.load(f'run_{i}.png') for i in range(1, 9)]#sprites for run animation
        # self.attack_sprites = [pygame.image.load(f'attack_{i}.png') for i in range(1,6)]

        run_spritesheet_image = pygame.image.load('run_spritesheet.png')
        run_spritesheet = spritesheet.SpriteSheet(run_spritesheet_image)
        self.run_sprites = []
        for i in range(8):
            self.run_sprites.append(run_spritesheet.get_image(i, 200, 200, 1, (0, 0, 0)))

        attack_spritesheet_image = pygame.image.load('attack_spritesheet.png')
        attack_spritesheet = spritesheet.SpriteSheet(attack_spritesheet_image)
        self.attack_sprites = []
        for i in range(3):
            self.attack_sprites.append(attack_spritesheet.get_image(i+2, 200, 200, 1, (0, 0, 0)))

        self.idle_image = pygame.image.load('idle.png')
        self.current_sprite = 0
        self.run_animation = False
        self.attack_animation = False
        self.facing_right = True
        self.image = self.idle_image
        self.rect = self.image.get_rect(topleft=self.pos)

        self.hitbox = pygame.Rect(self.pos[0] + 100 - (37/2), self.pos[1] + 100 - (52/2), 37, 52)

        self.hp = 100

    def run(self):
        if not self.attack_animation:
            self.run_animation = True
    
    def attack(self):
        global slash
        self.attack_animation = True
        self.run_animation = False
    
    def move(self):
        if not self.attack_animation:
            keys = pygame.key.get_pressed()
            if not keys[pygame.K_SPACE]:
                if keys[pygame.K_a]: 
                    self.pos[0] -= 5
                    if self.facing_right: 
                        self.facing_right = False
                        self.flip_sprites()
                if keys[pygame.K_d]: 
                    self.pos[0] += 5
                    if not self.facing_right:
                        self.facing_right = True
                        self.flip_sprites()
                if keys[pygame.K_s]:
                    self.pos[1] += 5
                if keys[pygame.K_w]:
                    self.pos[1] -= 5
            else:
                player.attack()

            self.rect.topleft = self.pos
            self.run_animation = any(keys[key] for key in (pygame.K_a, pygame.K_d, pygame.K_s, pygame.K_w)) #if wasd pressed animation=true
        else:
            player.attack()
        self.hitbox = pygame.Rect(self.pos[0] + 100 - (37/2), self.pos[1] + 100 - (52/2), 37, 52)

    def flip_sprites(self): #flips all images
        self.run_sprites = [pygame.transform.flip(sprite, True, False).convert_alpha() for sprite in self.run_sprites]
        self.attack_sprites = [pygame.transform.flip(sprite, True, False).convert_alpha() for sprite in self.attack_sprites]
        self.idle_image = pygame.transform.flip(self.idle_image, True, False).convert_alpha()

    def update(self, speed):
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
            player.check_death()

    def check_death(self):
        if self.hp < 0:
            print("you died") #finish later

pygame.init()
clock = pygame.time.Clock()
screen_width, screen_height = 1200, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("fruit ninja")

# Creating the sprites and groups
moving_sprites = pygame.sprite.Group()
player = Player()
fruit = Fruit()
slash = Slash(90000, 90000, True)
moving_sprites.add(player)
moving_sprites.add(fruit)

ticks_counter = []
#game loop
game_loop = True
while game_loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.attack()
                ticks_counter.clear()

    collide_fp = player.get_hitbox().colliderect(fruit.get_hitbox())
    fruit.check_collision(collide_fp)
    player.check_collision(collide_fp)

    collide_fa = slash.get_hitbox().colliderect(fruit.get_hitbox())
    fruit.check_collision(collide_fa)

    player.move()

    if(player.get_attack_anim()):
        ticks_counter.append(pygame.time.get_ticks())
        if ticks_counter[len(ticks_counter) - 1] - ticks_counter[0] >= 200:
            slash = Slash(player.get_pos()[0], player.get_pos()[1], player.get_facing_right())
    else:
        slash.set_pos(90000, 90000)

    #draw
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255,0,0), player.get_hitbox(),2) #temp drawing hitbox
    pygame.draw.rect(screen, (0,255,0), fruit.get_hitbox(), 2)
    pygame.draw.rect(screen, (0,0,255), slash.get_hitbox(), 2)
    moving_sprites.draw(screen)
    moving_sprites.update(0.25)
    pygame.display.flip()
    clock.tick(60)

    
    
