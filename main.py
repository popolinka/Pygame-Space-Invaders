import pygame
from pygame import mixer

import random
import math

# initialize the pygame
pygame.init()

# create screen
screen = pygame.display.set_mode((800, 600))  # width, height
# starting from the top left of the screen i.e. 0,0 as x,y
# the top right would be 800,0
# bottom left would be 0, 600

# background
background = pygame.image.load("background.png")

# sound setup
# background music
mixer.music.load("background.wav")
mixer.music.play(-1)  # play on loop

explosion_sound = mixer.Sound("explosion.wav")
bullet_sound = mixer.Sound("laser.wav")

# Caption and icon
pygame.display.set_caption("popolin invaders")

icon = pygame.image.load("space-invaders.png")
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load("player.png")
playerX = 370  # player's initial coordinate in the x-axis
playerY = 480

# playerX_change = 10
playerX_change = 0
playerY_change = 0

# enemy
# several enemies
enemyImg = []
enemyX = []
enemyY = []
enemy_speed = 5
enemyX_change = []
enemyY_change = []

num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("monster.png"))
    enemyX.append(random.randint(0, 800))  # player's initial coordinate in the x-axis
    enemyY.append(random.randint(50, 150))
    # enemy_speed.append(10)
    enemyX_change.append(enemy_speed)  # maybe depends on the speed of player's change?
    enemyY_change.append(40)

# bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = playerY

bullet_speed = 30
# bulletX_change = enemy_speed # since bullet's x will not change
bulletY_change = bullet_speed

# ready - you cant see the bullet on the screen
# fire - the bullet is scurently moving
bullet_state = "ready"

# score

score_value = 0
os_indep_font = pygame.font.get_default_font()
font = pygame.font.Font(os_indep_font, 40)

textX = 10
textY = 10

def show_score(x, y):
    score = font.render(f"Score : {str(score_value)}", True, (255, 255, 255))
    screen.blit(score, (x, y))

# game over screen
game_over_font = pygame.font.Font(os_indep_font, 100)
def game_over_text():
    over_text = game_over_font.render("GAME OVER ", True, (255, 255, 255))
    screen.blit(over_text, (80, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))  # basically draw


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))  # basically draw


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x - 3, y - 3))  # middle of the spaceship


def isCollision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((math.pow(enemy_x - bullet_x, 2)) + (math.pow(enemy_y - bullet_y, 2)))
    if distance < 20:
        return True
    else:
        return False


# Game loop
running = True


while running:

    # first the color then the background image
    screen.fill((50, 0, 0))  # RGB Color code - 0 to 255

    # background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():  # get ALL events in the game
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether it is right or left
        if event.type == pygame.KEYDOWN:
            # print("a keystroke is pressed")
            if event.key == pygame.K_LEFT:
                # playerX -= playerX_change
                playerX_change = -10
            if event.key == pygame.K_RIGHT:
                # playerX += playerX_change
                playerX_change = 10
            if event.key == pygame.K_UP:
                # playerX += playerX_change
                playerY_change = -10
            if event.key == pygame.K_DOWN:
                playerY_change = 10
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bullet_sound.play()
                bulletX = playerX  # so that the bullet will not follow the player/spaceship
                bulletY = playerY
                fire_bullet(bulletX, bulletY)
            # if event.key == pygame.K_RIGHT and event.key == pygame.K_UP:
            #    playerX_change = 10
            #    playerY_change = -10
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or pygame.K_DOWN:
                playerY_change = 0

    # checking for boundaries, so it does not go out of bounds/window
    playerX += playerX_change
    playerY += playerY_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 775:  # depends on the size of the player icon
        playerX = 775
    if playerY < 300:
        playerY = 300
    elif playerY > 575:
        playerY = 575

    # same for the enemy
    # enemy movement
    for i in range(num_of_enemies):

        # game over section
        if enemyY[i] > 200:
            for j in range(num_of_enemies):
                enemyY[j] = 2000 # so below the screen size
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX[i] = 0
            enemyX_change[i] = enemy_speed
            enemyY[i] += enemyY_change[i]
            # enemyX_change = enemy_speed

        elif enemyX[i] >= 765:  # must be compatible with rand.int so that...
            enemyX[i] = 765
            enemyX_change[i] = -enemy_speed
            enemyY[i] += enemyY_change[i]
        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound.play()
            bulletY = 480  # reset
            bullet_state = "ready"
            score_value += 5
            enemyX[i] = random.randint(0, 800)  # reset enemy
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bullet_speed

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
