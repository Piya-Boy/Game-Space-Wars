import random
import pygame as pg
from pygame.locals import *

pg.init()

# Set up the display
screen = pg.display.set_mode([800, 600])
pg.display.set_caption("Space Wars")

# Load images
icon = pg.image.load("img/icon.png")
pg.display.set_icon(icon)

background = pg.image.load("img/bg.png")
playerimg = pg.image.load("img/arcade.png")
imageheart = pg.image.load("img/heart.png")  # Load heart image
alienimg = pg.image.load("img/enemy.png")
bulletimg = pg.image.load("img/bullet.png")
bigbossimg = pg.image.load("img/bigboss.png")
playbtn = pg.image.load("img/play.png")
exitbtn = pg.image.load("img/exit.png")
winnerimg = pg.image.load("img/winner.png")
gameover = pg.image.load("img/game_over.png")

# size for btn
playbtn = pg.transform.scale(playbtn, (200, 70))
exitbtn = pg.transform.scale(exitbtn, (200, 70))

# size for image winner
winnerimg = pg.transform.scale(winnerimg, (700, 500))
# size for image gameover
gameover = pg.transform.scale(gameover, (800, 600))

# load sound
game_sound = pg.mixer.Sound("sound/background.wav")
bullet_sound = pg.mixer.Sound("sound/laser.wav")
explosion_sound = pg.mixer.Sound("sound/explosion.wav")
countdown_sound = pg.mixer.Sound("sound/count.wav")
add_life_sound = pg.mixer.Sound("sound/addlives.wav")
winner_sound = pg.mixer.Sound("sound/winner.wav")
game_over_sound = pg.mixer.Sound("sound/game_over.wav")

# Player position
player_x = 370
player_y = 500
player_speed = 5

# Bullet settings
bullet_speed = 7
bullets = []  # List to store bullets
bullet_cooldown = 250  # Time in milliseconds between bullets
last_bullet_time = pg.time.get_ticks()

# Set score and lives
score = 0
lives = 5
max_lives = 5
scoreX = 10
scoreY = 10

# Initialize font
font = pg.font.Font(None, 30)
countdown_font = pg.font.Font(None, 300)  # Font for countdown

# Alien settings
alien_speed = 1  # Speed at which the alien moves down
num_aliens = 3

# Initialize aliens with random positions
aliens = []
for _ in range(num_aliens):
    alien_x = random.randint(0, 730)
    alien_y = random.randint(-100, 150)  # Start some aliens above the screen
    aliens.append([alien_x, alien_y])

# Bigboss settings
bigboss_x = random.randint(0, 730)
bigboss_y = random.randint(-500, -150)  # Start bigboss above the screen
bigboss_speed = 1
bigboss_active = False

# Function to start the game
def start_game():
    global run
    countdown()
    run = True

# Function to exit the game
def exit_game():
    pg.quit()
    quit()

# Function to game over
# Function to game over
def game_over():
    global run, keys
    run = False
    game_over_sound.play()
    screen.blit(background, (0, 0))
    screen.blit(gameover, (0, 0))
    pg.display.update()

    # Time when the game over screen is shown
    start_time = pg.time.get_ticks()
    wait_time = 5000  # 5 seconds

    # Display the play again and exit buttons
    play_rect, exit_rect = draw_buttons()

    while True:
        current_time = pg.time.get_ticks()
        elapsed_time = current_time - start_time

        # Check if 5 seconds have passed
        if elapsed_time >= wait_time:
            screen.blit(background, (0, 0))
            play_rect, exit_rect = draw_buttons()
            pg.display.update()
            start_time = pg.time.get_ticks()  # Reset start time for waiting

        for event in pg.event.get():
            if event.type == pg.QUIT or keys[pg.K_ESCAPE]:
                exit_game()
                return  # Exit the game_over function if the game is closed
            elif event.type == pg.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    reset_game()
                    return  # Exit the game_over function after resetting the game
                elif exit_rect.collidepoint(event.pos):
                    exit_game()
                    return  # Exit the game_over function if the user chooses to exit

        pg.time.delay(10)  # Slight delay to avoid high CPU usage

# Function to winner
def winner():
    global run, keys
    run = False
    winner_sound.play()
    winner_img = winnerimg.get_rect(center=(400, 300))
    screen.blit(background, (0, 0))
    screen.blit(winnerimg, winner_img)
    pg.display.update()

    # Time when the game over screen is shown
    start_time = pg.time.get_ticks()
    wait_time = 5000  # 5 seconds

    # Display the play again and exit buttons
    play_rect, exit_rect = draw_buttons()

    while True:
        current_time = pg.time.get_ticks()
        elapsed_time = current_time - start_time

        # Check if 5 seconds have passed
        if elapsed_time >= wait_time:
            screen.blit(background, (0, 0))
            play_rect, exit_rect = draw_buttons()
            pg.display.update()
            start_time = pg.time.get_ticks()  # Reset start time for waiting

        for event in pg.event.get():
            if event.type == pg.QUIT or keys[pg.K_ESCAPE]:
                exit_game()
                return  # Exit the game_over function if the game is closed
            elif event.type == pg.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    reset_game()
                    return  # Exit the game_over function after resetting the game
                elif exit_rect.collidepoint(event.pos):
                    exit_game()
                    return  # Exit the game_over function if the user chooses to exit

        pg.time.delay(10)  # Slight delay to avoid high CPU usage

# Function to draw hearts based on remaining lives
def lives_score():
    for i in range(lives):
        screen.blit(imageheart, (heartX + i * (imageheart.get_width() + 10), heartY))

# Move player left
def move_left():
    global player_x
    player_x -= player_speed
    if player_x < 0:
        player_x = 0  # Keep the player within the screen boundary

# Move player right
def move_right():
    global player_x
    player_x += player_speed
    if player_x > 800 - playerimg.get_width():
        player_x = 800 - playerimg.get_width()  # Keep the player within the screen boundary

# Draw player
def player():
    screen.blit(playerimg, (player_x, player_y))

# Draw and update aliens
def update_aliens():
    global lives, score
    for alien in aliens[:]:  # Iterate over a copy of the aliens list
        alien[1] += alien_speed  # Move alien down

        # Check if the alien collides with the player
        if (player_x < alien[0] < player_x + playerimg.get_width() or
            player_x < alien[0] + alienimg.get_width() < player_x + playerimg.get_width()) and \
                (player_y < alien[1] < player_y + playerimg.get_height() or
                 player_y < alien[1] + alienimg.get_height() < player_y + playerimg.get_height()):
            lives -= 1  # Decrease life
            aliens.remove(alien)  # Remove the alien from the list
            alien_x = random.randint(0, 730)
            alien_y = random.randint(-100, 150)
            aliens.append([alien_x, alien_y])  # Add a new alien at a random position
            explosion_sound.play()  # Play explosion sound
        # If alien reaches the bottom of the screen
        elif alien[1] > 600:
            alien[1] = random.randint(-100, 150)  # Reset alien to the top
            alien[0] = random.randint(0, 730)  # New random x position

        screen.blit(alienimg, (alien[0], alien[1]))  # Draw the alien

# Draw and update bullets
def update_bullets():
    global score, lives, bigboss_active, bigboss_x, bigboss_y, max_lives
    for bullet in bullets[:]:
        bullet[1] -= bullet_speed  # Move bullet up
        if bullet[1] < 0:  # Remove bullet if it moves off the screen
            bullets.remove(bullet)
        else:
            screen.blit(bulletimg, (bullet[0], bullet[1]))

            # Check for collision with aliens
            for alien in aliens:
                if alien[0] < bullet[0] < alien[0] + alienimg.get_width() and \
                   alien[1] < bullet[1] < alien[1] + alienimg.get_height():
                    score += 1  # Increase score
                    bullets.remove(bullet)  # Remove bullet
                    alien[1] = random.randint(-100, 150)  # Reset alien to the top
                    alien[0] = random.randint(0, 730)  # New random x position
                    explosion_sound.play()  # Play explosion sound
                    break  # Exit the loop to avoid modifying the list during iteration

            # Check for collision with bigboss
            if bigboss_active and bigboss_x < bullet[0] < bigboss_x + bigbossimg.get_width() and \
               bigboss_y < bullet[1] < bigboss_y + bigbossimg.get_height():
                lives = min(lives + 1, max_lives)  # Increase life, but not exceed 5
                bullets.remove(bullet)  # Remove bullet
                bigboss_y = random.randint(-500, -150)  # Reset bigboss to the top
                bigboss_x = random.randint(0, 730)  # New random x position
                bigboss_active = False  # Deactivate bigboss
                add_life_sound.play()  # Play explosion sound

# Draw and update bigboss
def update_bigboss():
    global lives, bigboss_active, bigboss_x, bigboss_y, max_lives
    if bigboss_active:
        bigboss_y += bigboss_speed  # Move bigboss down

        # Check if the bigboss collides with the player
        if (player_x < bigboss_x < player_x + playerimg.get_width() or
            player_x < bigboss_x + bigbossimg.get_width() < player_x + playerimg.get_width()) and \
                (player_y < bigboss_y < player_y + playerimg.get_height() or
                 player_y < bigboss_y + bigbossimg.get_height() < player_y + playerimg.get_height()):
            lives = min(lives + 1, max_lives)  # Increase life, but not exceed 5
            bigboss_y = random.randint(-500, -150)  # Reset bigboss to the top
            bigboss_x = random.randint(0, 730)  # New random x position
            bigboss_active = False  # Deactivate bigboss
            add_life_sound.play()  # Play explosion sound

        # If bigboss reaches the bottom of the screen
        elif bigboss_y > 600:
            bigboss_y = random.randint(-500, -150)  # Reset bigboss to the top
            bigboss_x = random.randint(0, 730)  # New random x position
            bigboss_active = False  # Deactivate bigboss

        screen.blit(bigbossimg, (bigboss_x, bigboss_y))  # Draw the bigboss
    else:
        # Randomly activate bigboss if lives are not full
        if lives < 5 and random.random() < 0.001:  # Adjust the probability as needed
            bigboss_active = True

# Function to draw buttons
def draw_buttons():
    play_rect = playbtn.get_rect(center=(400, 250))
    exit_rect = exitbtn.get_rect(center=(400, 350))
    screen.blit(playbtn, play_rect.topleft)
    screen.blit(exitbtn, exit_rect.topleft)
    return play_rect, exit_rect

# Countdown function
def countdown():
    countdown_sound.play()
    for i in range(3, -1, -1):
        screen.blit(background, (0, 0))  # Draw the background
        text = countdown_font.render(str(i), True, (255, 255, 255))
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2 - text.get_height() // 2))
        pg.display.update()
        pg.time.delay(1000)  # Wait for 1 second

# Function to reset the game
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

# Main loop
run = False
menu = True
while menu:
    screen.blit(background, (0, 0))  # Draw the background

    play_rect, exit_rect = draw_buttons()
    keys = pg.key.get_pressed()

    for event in pg.event.get():
        if event.type == pg.QUIT or keys[pg.K_ESCAPE]:
            exit_game()
        elif event.type == pg.MOUSEBUTTONDOWN:
            if play_rect.collidepoint(event.pos):
                start_game()  # Start the game
                menu = False  # Exit the menu loop
            elif exit_rect.collidepoint(event.pos):
                exit_game()

    pg.display.update()

# Game loop
while run:
    screen.blit(background, (0, 0))  # Draw the background

    # Handle events
    keys = pg.key.get_pressed()
    for event in pg.event.get():
        if event.type == pg.QUIT or keys[pg.K_ESCAPE]:
            exit_game()

    if keys[pg.K_LEFT]:
        move_left()
    if keys[pg.K_RIGHT]:
        move_right()
    if keys[pg.K_SPACE]:
        # Shoot bullet
        current_time = pg.time.get_ticks()
        if current_time - last_bullet_time >= bullet_cooldown:
            bullet_x = player_x + playerimg.get_width() // 2 - bulletimg.get_width() // 2
            bullet_y = player_y - bulletimg.get_height()
            bullets.append([bullet_x, bullet_y])
            last_bullet_time = current_time
            bullet_sound.play()

    # Draw and update game elements
    player()
    update_bullets()
    update_aliens()
    update_bigboss()

    # Draw score and lives
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (scoreX, scoreY))

    heartX = 630
    heartY = 10
    lives_score()  # Draw the hearts for lives

    # Check for game over
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
