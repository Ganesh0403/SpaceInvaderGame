import pygame as py
import random
import math
import os
from pygame import mixer

py.init()

screen = py.display.set_mode((800, 600))

background = py.image.load("background.jpg")

mixer.music.load("background.wav")
mixer.music.play(-1)

#create icon and title
py.display.set_caption("Space Invader")
icon = py.image.load("ufo.png")
py.display.set_icon(icon)

# Player
playerImg = py.image.load("space.png")
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

def player(x,y):
    screen.blit(playerImg, (x, y))

enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemyImg = []
num_of_enemy = 6

for i in range(num_of_enemy):
    enemyImg.append(py.image.load("shredder.png"))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(25,150))
    enemyX_change.append(2.5)
    enemyY_change.append(20)

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

bulletImg = py.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow((enemyX -bulletX),2) + math.pow((enemyY - bulletY),2))
    if distance < 27:
        return True
    else:
        return False
score_value = 0 

font = py.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10

over_font = py.font.Font('freesansbold.ttf',128)

def game_over_text():
    over_text = font.render("Game Over ", True, (255, 255, 255))
    screen.blit(over_text, (300, 250))

if (not os.path.exists("high_score.txt")):
        with open("high_score.txt", 'w') as f:
            f.write("0")

with open("high_score.txt", 'r') as f:
    high_score = f.read()


def show_score(x, y):
    score = font.render(f"Score : {score_value}  Highscore : {high_score}", True, (255, 255, 255))
    screen.blit(score, (x, y))

game_over = False

while not game_over:

    screen.fill((0,0,0))
    screen.blit(background, (0,0))

    for event in py.event.get():
        if event.type == py.QUIT:
            game_over = True

        if event.type == py.KEYDOWN:
            if event.key == py.K_LEFT:
                playerX_change = -5
            if event.key == py.K_RIGHT:
                playerX_change = 5
            if event.key == py.K_UP:
                playerY_change = -5
            if event.key == py.K_DOWN:
                playerY_change = 5
            if event.key == py.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == py.KEYUP:
            if event.key == py.K_LEFT or event.key == py.K_RIGHT:
                playerX_change = 0
            if event.key == py.K_UP or event.key == py.K_DOWN:
                playerY_change = 0

    playerX += playerX_change
    playerY += playerY_change

    if playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536
    
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    if bulletY <= 0:
        bulletY = playerY
        bullet_state = "ready"
    
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    
    for i in range(num_of_enemy):

        if enemyY[i] > playerY - 20:
            for j in range(num_of_enemy):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -5
            enemyY[i] += enemyY_change[i]
    
        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = playerY
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(25,150)
            if score_value > int(high_score):
                high_score = score_value
        with open("high_score.txt", 'w') as f:
            f.write(str(high_score))

        enemy(enemyX[i], enemyY[i], i)

    player(playerX, playerY)
    show_score(textX, textY)
    py.display.update()