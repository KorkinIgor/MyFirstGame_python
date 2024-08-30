import pygame
import time

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Моя игра")

icon = pygame.image.load('image/avatar.jpeg')
pygame.display.set_icon(icon)

screen.fill((37, 150, 190))

bg = pygame.image.load('image/bgf.jpg')

walk_right = [
    pygame.image.load('image/walk_right/pl1.png'),
    pygame.image.load('image/walk_right/pl2.png'),
    pygame.image.load('image/walk_right/pl3.png')
]
walk_left = [
    pygame.image.load('image/walk_left/pl1.png'),
    pygame.image.load('image/walk_left/pl2.png'),
    pygame.image.load('image/walk_left/pl3.png')
]
gost = pygame.image.load('image/vrag.png')
gost_x = 1290

player_x = 150
player_y = 450
player_speed = 20
player_count = 0
bg_x = 0

score: int = 0

is_jump = False
jump_count = 10

running = True

gameplay = True
label = pygame.font.Font('Fonts/Kosmos.otf', 40)

lose_label = label.render("Вы проиграли!", False, "White")


retern_label = label.render("Играть занова", False, "White")
retern_label_rect = retern_label.get_rect(topleft=(180, 200))

bg_sound = pygame.mixer.Sound('Audio/aud.mp3')

gost_time = pygame.USEREVENT + 1
pygame.time.set_timer(gost_time, 1500)
gost_list = []


while running:

    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 1280, 0))

    if gameplay:
        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))

        if gost_list:
            for (i, el) in enumerate(gost_list):
                screen.blit(gost, el)
                el.x -= 20

                if el.x < -10:
                    gost_list.pop(i)
                    score += 1

                if player_rect.colliderect(el):
                    gameplay = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a] and player_x > 50:
            player_x -= player_speed
            screen.blit(walk_left[player_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_count], (player_x, player_y))

        if keys[pygame.K_LEFT] or keys[pygame.K_a] and player_x > 50:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d] and player_x < 1000:
            player_x += player_speed

        if not is_jump:
            if keys[pygame.K_SPACE] or keys[pygame.K_w]:
                is_jump = True
        else:
            if jump_count >= -10:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 10

        if player_count == 2:
            player_count = 0
        else:
            player_count += 1

        bg_x -= 20

        if bg_x == -1280:
            bg_x = 0
    else:
        screen.fill("Black")
        screen.blit(lose_label, (180, 100))
        screen.blit(retern_label, retern_label_rect)
        score_label = label.render(f"Счет: {score}", False, "White")
        screen.blit(score_label, (250, 300))
        mouse = pygame.mouse.get_pos()

        if retern_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 150
            score = 0
            gost_list.clear()

    pygame.display.update()
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        if event.type == gost_time:
            gost_list.append(gost.get_rect(topleft=(gost_x, 450)))

    clock.tick(20)
