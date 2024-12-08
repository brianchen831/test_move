import pygame, sys

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pos = [100, 100]
        self.sprites = [pygame.image.load(f'run_{i}.png') for i in range(1, 9)] #sprite list for run animation
        self.idle_image = pygame.image.load('idle.png')
        self.current_sprite = 0
        self.run_animation = False
        self.image = self.idle_image
        self.rect = self.image.get_rect(topleft=self.pos)

    def run(self):
        self.run_animation = True

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.pos[0] -= 5
        if keys[pygame.K_d]:
            self.pos[0] += 5
        if keys[pygame.K_s]:
            self.pos[1] += 5
        if keys[pygame.K_w]:
            self.pos[1] -= 5

        self.rect.topleft = self.pos
        self.run_animation = any(keys[key] for key in (pygame.K_a, pygame.K_d, pygame.K_s, pygame.K_w)) #if wasd pressed run animation=true

    def update(self, speed):
        if self.run_animation:
            self.current_sprite += speed
            if int(self.current_sprite) >= len(self.sprites):
                self.current_sprite = 0
            self.image = self.sprites[int(self.current_sprite)]
        else:
            self.image = self.idle_image


pygame.init()
clock = pygame.time.Clock()
screen_width, screen_height = 1600, 900
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("game animation test")

# Creating the sprites and groups
moving_sprites = pygame.sprite.Group()
player = Player()
moving_sprites.add(player)

#game loop
game_loop = True
while game_loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    player.move()

    #draw
    screen.fill((0, 0, 0))
    moving_sprites.draw(screen)
    moving_sprites.update(0.25)
    pygame.display.flip()
    clock.tick(60)
