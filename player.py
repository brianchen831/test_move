import pygame
import spritesheet


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
            print ('hit by fruit')
            return self.check_death()
        else:
            return True

    def check_death(self):
        if self.hp < 0:
            print("you died") #finish later
            return False
        return True
