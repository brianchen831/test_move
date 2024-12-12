import pygame, sys
import random
from player import Player
from slash import Slash
from fruit import Fruit


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
moving_sprites.add(Fruit(random.choice(['apple','strawberry','melon','apple'])))

# Start screen
game_name = test_font.render('Fruit Ninja',False,(38,38,38))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = test_font.render('Press R to start the game',False,(38,38,38))
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
                moving_sprites.add(Fruit(random.choice(['apple','strawberry','melon','apple'])))
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_active = True
                    player_group.sprites()[0].hp = 100
                    player.score = 0


    if game_active:
        for fruit in moving_sprites.sprites():
            collide_fp = player_group.sprites()[0].get_hitbox().colliderect(fruit.get_hitbox())
            fruit.check_collision(collide_fp)
            alive = player_group.sprites()[0].check_collision(collide_fp)
            if not alive:
                game_active = False
                moving_sprites.empty()

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

        # for a in moving_sprites.sprites():
        #     pygame.draw.rect(screen, (12, 155, 0), a.get_hitbox(), 3)

        # pygame.draw.rect(screen, (0,0,255), slash.get_hitbox(), 2)
        # for p in player_group.sprites():
        #     pygame.draw.rect(screen, (111, 0, 80), p.get_hitbox(), 3)
        
        player_group.draw(screen)
        player_group.update(0.25)

        moving_sprites.draw(screen)
        moving_sprites.update()
        
        score_message = test_font.render(f'score: {player.score}',False,(29, 191, 48))
        score_message_rect = score_message.get_rect(center = (1050,30))
        hp_message = test_font.render(f'health: {player_group.sprites()[0].hp}',False,(29, 191, 48))
        hp_message_rect = hp_message.get_rect(center = (1050,60))
        screen.blit(score_message, score_message_rect)
        screen.blit(hp_message, hp_message_rect)


    else:
        screen.fill(((47, 189, 104)))
        score_message = test_font.render(f'Your score: {player.score}',False,(38, 38, 38))
        score_message_rect = score_message.get_rect(center = (400,330))
        screen.blit(game_name,game_name_rect)
        
        if player.score == 0 and player_group.sprites()[0].hp == 100: 
            screen.blit(game_message,game_message_rect)
        else: 
            screen.blit(score_message,score_message_rect)

    pygame.display.update()
    clock.tick(60)