import random
import pygame as pg
from pygame.locals import *

pg.init()
screen = pg.display.set_mode([800, 600])
pg.display.set_caption("Space Wars")

icon = pg.image.load("img/icon.png")
pg.display.set_icon(icon)

background = pg.image.load("img/bg.png")
playerimg = pg.image.load("img/arcade.png")
imageheart = pg.image.load("img/heart.png")
alienimg = pg.image.load("img/enemy.png")
bulletimg = pg.image.load("img/bullet.png")
bigbossimg = pg.image.load("img/bigboss.png")
playbtn = pg.image.load("img/play.png")
exitbtn = pg.image.load("img/exit.png")
winnerimg = pg.image.load("img/winner.png")
gameover = pg.image.load("img/game_over.png")

playbtn = pg.transform.scale(playbtn, (200, 70))
exitbtn = pg.transform.scale(exitbtn, (200, 70))

winnerimg = pg.transform.scale(winnerimg, (700, 500))
gameover = pg.transform.scale(gameover, (800, 600))

game_sound = pg.mixer.Sound("sound/background.wav")
bullet_sound = pg.mixer.Sound("sound/laser.wav")
explosion_sound = pg.mixer.Sound("sound/explosion.wav")
countdown_sound = pg.mixer.Sound("sound/count.wav")
add_life_sound = pg.mixer.Sound("sound/addlives.wav")
winner_sound = pg.mixer.Sound("sound/winner.wav")
game_over_sound = pg.mixer.Sound("sound/game_over.wav")

player_x = 370
player_y = 500
player_speed = 5

bullet_speed = 7
bullets = []
bullet_cooldown = 250
last_bullet_time = pg.time.get_ticks()

score = 0
lives = 5
max_lives = 5
scoreX = 10
scoreY = 10

font = pg.font.Font(None, 30)
countdown_font = pg.font.Font(None, 300)

alien_speed = 1
num_aliens = 3


aliens = []
for _ in range(num_aliens):
    alien_x = random.randint(0, 730)
    alien_y = random.randint(-100, 150)
    aliens.append([alien_x, alien_y])


bigboss_x = random.randint(0, 730)
bigboss_y = random.randint(-500, -150)
bigboss_speed = 1
bigboss_active = False


def start_game():
    global run
    countdown()
    run = True


def exit_game():
    pg.quit()
    quit()


def game_over():
    global run, keys
    run = False
    game_over_sound.play()
    screen.blit(background, (0, 0))
    screen.blit(gameover, (0, 0))
    pg.display.update()

    start_time = pg.time.get_ticks()
    wait_time = 5000

    play_rect, exit_rect = draw_buttons()

    while True:
        current_time = pg.time.get_ticks()
        elapsed_time = current_time - start_time

        if elapsed_time >= wait_time:
            screen.blit(background, (0, 0))
            play_rect, exit_rect = draw_buttons()
            pg.display.update()
            start_time = pg.time.get_ticks()

        for event in pg.event.get():
            if event.type == pg.QUIT or keys[pg.K_ESCAPE]:
                exit_game()
                return
            elif event.type == pg.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    reset_game()
                    return
                elif exit_rect.collidepoint(event.pos):
                    exit_game()
                    return

        pg.time.delay(10)


def winner():
    global run, keys
    run = False
    winner_sound.play()
    winner_img = winnerimg.get_rect(center=(400, 300))
    screen.blit(background, (0, 0))
    screen.blit(winnerimg, winner_img)
    pg.display.update()

    start_time = pg.time.get_ticks()
    wait_time = 5000

    play_rect, exit_rect = draw_buttons()

    while True:
        current_time = pg.time.get_ticks()
        elapsed_time = current_time - start_time

        if elapsed_time >= wait_time:
            screen.blit(background, (0, 0))
            play_rect, exit_rect = draw_buttons()
            pg.display.update()
            start_time = pg.time.get_ticks()

        for event in pg.event.get():
            if event.type == pg.QUIT or keys[pg.K_ESCAPE]:
                exit_game()
                return
            elif event.type == pg.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    reset_game()
                    return
                elif exit_rect.collidepoint(event.pos):
                    exit_game()
                    return

        pg.time.delay(10)


def lives_score():
    for i in range(lives):
        screen.blit(imageheart, (heartX + i * (imageheart.get_width() + 10), heartY))


def move_left():
    global player_x
    player_x -= player_speed
    if player_x < 0:
        player_x = 0


def move_right():
    global player_x
    player_x += player_speed
    if player_x > 800 - playerimg.get_width():
        player_x = 800 - playerimg.get_width()


def player():
    screen.blit(playerimg, (player_x, player_y))


def update_aliens():
    global lives, score
    for alien in aliens[:]:
        alien[1] += alien_speed

        if (
            player_x < alien[0] < player_x + playerimg.get_width()
            or player_x
            < alien[0] + alienimg.get_width()
            < player_x + playerimg.get_width()
        ) and (
            player_y < alien[1] < player_y + playerimg.get_height()
            or player_y
            < alien[1] + alienimg.get_height()
            < player_y + playerimg.get_height()
        ):
            lives -= 1
            aliens.remove(alien)
            alien_x = random.randint(0, 730)
            alien_y = random.randint(-100, 150)
            aliens.append([alien_x, alien_y])
            explosion_sound.play()

        elif alien[1] > 600:
            alien[1] = random.randint(-100, 150)
            alien[0] = random.randint(0, 730)

        screen.blit(alienimg, (alien[0], alien[1]))


def update_bullets():
    global score, lives, bigboss_active, bigboss_x, bigboss_y, max_lives
    for bullet in bullets[:]:
        bullet[1] -= bullet_speed
        if bullet[1] < 0:
            bullets.remove(bullet)
        else:
            screen.blit(bulletimg, (bullet[0], bullet[1]))

            for alien in aliens:
                if (
                    alien[0] < bullet[0] < alien[0] + alienimg.get_width()
                    and alien[1] < bullet[1] < alien[1] + alienimg.get_height()
                ):
                    score += 1
                    bullets.remove(bullet)
                    alien[1] = random.randint(-100, 150)
                    alien[0] = random.randint(0, 730)
                    explosion_sound.play()
                    break

            if (
                bigboss_active
                and bigboss_x < bullet[0] < bigboss_x + bigbossimg.get_width()
                and bigboss_y < bullet[1] < bigboss_y + bigbossimg.get_height()
            ):
                lives = min(lives + 1, max_lives)
                bullets.remove(bullet)
                bigboss_y = random.randint(-500, -150)
                bigboss_x = random.randint(0, 730)
                bigboss_active = False
                add_life_sound.play()


def update_bigboss():
    global lives, bigboss_active, bigboss_x, bigboss_y, max_lives
    if bigboss_active:
        bigboss_y += bigboss_speed

        if (
            player_x < bigboss_x < player_x + playerimg.get_width()
            or player_x
            < bigboss_x + bigbossimg.get_width()
            < player_x + playerimg.get_width()
        ) and (
            player_y < bigboss_y < player_y + playerimg.get_height()
            or player_y
            < bigboss_y + bigbossimg.get_height()
            < player_y + playerimg.get_height()
        ):
            lives = min(lives + 1, max_lives)
            bigboss_y = random.randint(-500, -150)
            bigboss_x = random.randint(0, 730)
            bigboss_active = False
            add_life_sound.play()

        elif bigboss_y > 600:
            bigboss_y = random.randint(-500, -150)
            bigboss_x = random.randint(0, 730)
            bigboss_active = False

        screen.blit(bigbossimg, (bigboss_x, bigboss_y))
    else:

        if lives < 5 and random.random() < 0.001:
            bigboss_active = True


def draw_buttons():
    play_rect = playbtn.get_rect(center=(400, 250))
    exit_rect = exitbtn.get_rect(center=(400, 350))
    screen.blit(playbtn, play_rect.topleft)
    screen.blit(exitbtn, exit_rect.topleft)
    return play_rect, exit_rect


def countdown():
    countdown_sound.play()
    for i in range(3, -1, -1):
        screen.blit(background, (0, 0))
        text = countdown_font.render(str(i), True, (255, 255, 255))
        screen.blit(
            text,
            (
                screen.get_width() // 2 - text.get_width() // 2,
                screen.get_height() // 2 - text.get_height() // 2,
            ),
        )
        pg.display.update()
        pg.time.delay(1000)


def reset_game():
    global player_x, player_y, score, lives, bullets, bigboss_active, bigboss_x, bigboss_y
    player_x = 370
    player_y = 500
    score = 0
    lives = 5
    bullets = []
    bigboss_active = False
    bigboss_x = random.randint(0, 730)
    bigboss_y = random.randint(-500, -150)
    start_game()


run = False
menu = True
while menu:
    screen.blit(background, (0, 0))

    play_rect, exit_rect = draw_buttons()
    keys = pg.key.get_pressed()

    for event in pg.event.get():
        if event.type == pg.QUIT or keys[pg.K_ESCAPE]:
            exit_game()
        elif event.type == pg.MOUSEBUTTONDOWN:
            if play_rect.collidepoint(event.pos):
                start_game()
                menu = False
            elif exit_rect.collidepoint(event.pos):
                exit_game()

    pg.display.update()


while run:
    screen.blit(background, (0, 0))

    keys = pg.key.get_pressed()
    for event in pg.event.get():
        if event.type == pg.QUIT or keys[pg.K_ESCAPE]:
            exit_game()

    if keys[pg.K_LEFT]:
        move_left()
    if keys[pg.K_RIGHT]:
        move_right()
    if keys[pg.K_SPACE]:

        current_time = pg.time.get_ticks()
        if current_time - last_bullet_time >= bullet_cooldown:
            bullet_x = (
                player_x + playerimg.get_width() // 2 - bulletimg.get_width() // 2
            )
            bullet_y = player_y - bulletimg.get_height()
            bullets.append([bullet_x, bullet_y])
            last_bullet_time = current_time
            bullet_sound.play()

    player()
    update_bullets()
    update_aliens()
    update_bigboss()

    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (scoreX, scoreY))

    heartX = 630
    heartY = 10
    lives_score()

    if lives <= 0:
        game_over()

    if score == 100:
        winner()

    if score >= 40 and score <= 50:
        alien_speed = 2
        num_aliens = 4
        bigboss_speed = 2
        
    elif score >= 60 and score <= 70:
        alien_speed = 3
        num_aliens = 5
        bigboss_speed = 3
    elif score >= 80:
        alien_speed = 4
        num_aliens = 6
        bigboss_speed = 4

    pg.display.update()

pg.quit()
