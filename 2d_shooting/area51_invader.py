#!/usr/bin/env python3

import pygame
import random
import math


class player(object):

    # Player initial coordinates
    def __init__(self):
        self.x = 370
        self.y = 480
        self.x_chg = 0
        self.y_chg = 0
        self.status = True
        self.respawn = 300

    # Draws Player
    def draw(self):
        playerImg = pygame.image.load("spaceship.png")
        screen.blit(playerImg, (self.x, self.y))


class bullet(object):

    # Bullet initial coordinates
    def __init__(self):
        self.x = 370
        self.y = 480
        self.y_chg = 10
        self.fire = False

    # Draws Bullet
    def draw(self):
        bulletImg = pygame.image.load("bullet.png")
        screen.blit(bulletImg, (self.x, self.y))


class enemyr(object):
    def __init__(self, x, y):

        # Enemy random respawn  -- Moving to right
        self.x = x
        self.y = y
        self.x_chg = 0
        self.status = True
        self.respawn = 300
        self.fire = True

    def draw(self):
        enemyImg = pygame.image.load("enemy.png")
        screen.blit(enemyImg, (self.x, self.y))


class enemyl(object):
    def __init__(self, x, y):
        # Enemy random respawn  -- Moving to left
        self.x = random.randint(0, 768)
        self.y = random.randint(60, 150)
        self.x_chg = 0
        self.status = True
        self.respawn = 300
        self.fire = True

    def draw(self):
        enemyImg = pygame.image.load("enemy.png")
        screen.blit(enemyImg, (self.x, self.y))


class enemybullet(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.y_chg = -5

    def draw(self):
        enemybulletImg = pygame.image.load("enemybullet.png")
        screen.blit(enemybulletImg, (self.x, self.y))


def isHit(x, y, bulletx, bullety):
    distance = math.sqrt(math.pow(x - bulletx, 2) + (math.pow(y - bullety, 2)))

    if distance < 27:
        return True


def isEnemyHit(x, y, bulletx, bullety):
    distance = math.sqrt(math.pow(x - bulletx, 2) + (math.pow(y - bullety, 2)))

    if distance < 40:
        return True


def isCollision(x, y, enemyx, enemyy):
    distance = math.sqrt(math.pow(x - enemyx, 2) + (math.pow(y - enemyy, 2)))

    if distance < 20:
        return True


def score(label, x, y, points):
    font = pygame.font.SysFont("freemono", 16)
    scoreImg = font.render(f"{label} : {points}", True, (0, 0, 255))
    screen.blit(scoreImg, (x, y))


def gameover():
    font = pygame.font.SysFont("freemono", 64)
    gameoverImg = font.render("Game Over", True, (255, 0, 0))
    screen.fill((0, 0, 0))
    screen.blit(gameoverImg, (204.5, 260))


def startgame(countdown):
    font = pygame.font.SysFont("Constantia", 128)
    startgameImg = font.render(str(countdown), True, (255, 0, 0))
    screen.blit(startgameImg, (350, 220))


if __name__ == "__main__":

    pygame.init()

    screen = pygame.display.set_mode((800, 600))

    running = True
    points = 0
    enemypoints = 0
    last_count = pygame.time.get_ticks()
    counter = 5

    # Icon and game title
    pygame.display.set_caption("Area 51 Invader")
    icon = pygame.image.load("alien.png")
    pygame.display.set_icon(icon)

    # Music
    pygame.mixer.music.load("background.wav")
    pygame.mixer.music.play(-1)

    player = player()
    bullet = bullet()

    enemyr_list = []
    enemyr_bullet_list = []
    enemyl_list = []
    enemyl_bullet_list = []
    gamestatus = True

    for _ in range(5):
        x = random.randint(0, 768)
        y = random.randint(60, 150)
        enemyr_list.append(enemyr(x, y))
        enemyr_bullet_list.append(enemybullet(x, y))
        enemyl_list.append(enemyl(x, y))
        enemyl_bullet_list.append(enemybullet(x, y))

    # Main Loop
    while running:

        # Background
        background = pygame.image.load("51.png")
        screen.blit(background, (0, 0))

        # Draw player on its initial coordinates
        player.draw()

        # Start game counter
        if counter > 0 and gamestatus == True:
            startgame(counter)
            time_now = pygame.time.get_ticks()
            player.x = 370
            player.y = 480
            player.status = False
            if time_now - last_count > 1000:
                counter -= 1
                last_count = time_now

        elif counter == 0:
            player.status = True
            # Draws player after respawn and while moving
            player.draw()

        # Player movement
        player.x += player.x_chg
        player.y += player.y_chg

        # Player movement boundary
        if player.status == True:
            if player.x <= 0:
                player.x = 0
            if player.x >= 736:
                player.x = 736
            if player.y <= 0:
                player.y = 0
            if player.y >= 536:
                player.y = 536

        # Bullet movement
        if bullet.fire == True and player.status == True:
            bullet.draw()
            bullet.y -= bullet.y_chg
        if bullet.y <= 0:
            bullet.x = player.x
            bullet.y = player.y
            bullet.fire = False

        for enemyr, enemybulletr in zip(enemyr_list, enemyr_bullet_list):

            # Draws enemy moving right
            if enemyr.status == False and enemyr.respawn < 300:
                enemyr.x = 1900
                enemyr.y = 1900
                enemyr.respawn += 1
            else:
                enemyr.draw()
                enemyr.respawn = 300
                enemyr.status = True

            # EnemyR Movement
            if enemyr.status == True and player.status == True:

                if enemyr.x >= 0 and enemyr.x <= 768:
                    enemyr.x_chg = 0.5
                else:
                    enemyr.x = random.randint(0, 768)
                    enemyr.y = random.randint(60, 150)
                enemyr.x += enemyr.x_chg

            # Fires EnemyR bullet
            if enemybulletr.y < 600 and player.status == True:
                enemybulletr.y -= enemybulletr.y_chg
                enemybulletr.draw()
            if enemybulletr.y > 595 and player.status == True:
                enemybulletr.x = enemyr.x
                enemybulletr.y = enemyr.y

            # Collision - EnemyR
            hitr = isHit(enemyr.x, enemyr.y, bullet.x, bullet.y)
            enemyhitr = isEnemyHit(
                player.x, player.y, enemybulletr.x, enemybulletr.y
            )
            collisionr = isCollision(player.x, player.y, enemyr.x, enemyr.y)

            # Player hits the EnemyR
            if hitr and player.status == True:

                bullet.y = 480
                bullet.fire = False
                points += 1
                explosionSound = pygame.mixer.Sound("explosion.wav")
                explosionSound.play()
                enemyr.status = False
                enemyr.respawn = 0

            # EnemyR hits player
            if (enemyhitr or collisionr) and player.status == True:
                enemypoints += 1
                enemybulletr.x = enemyr.x
                enemybulletr.y = enemyr.y
                explosionSound = pygame.mixer.Sound("explosion.wav")
                explosionSound.play()
                player.status = False
                player.respawn = 0
                counter = 5

        for enemyl, enemybulletl in zip(enemyl_list, enemyl_bullet_list):

            # Draws enemy moving left
            if enemyl.status == False and enemyl.respawn < 300:
                enemyl.x = 1900
                enemyl.y = 1900
                enemyl.respawn += 1

            else:
                enemyl.draw()
                enemyl.respawn = 300
                enemyl.status = True

            # EnemyL movement
            if enemyl.status == True and player.status == True:
                if enemyl.x <= 736 and enemyl.x >= 0:
                    enemyl.x_chg = -0.5
                else:
                    enemyl.x = random.randint(0, 768)
                    enemyl.y = random.randint(60, 150)
                enemyl.x += enemyl.x_chg

            # Fires EnemyR bullet
            if enemybulletl.y < 600 and player.status == True:
                enemybulletl.y -= enemybulletl.y_chg
                enemybulletl.draw()
            if enemybulletl.y > 595 and player.status == True:
                enemybulletl.x = enemyl.x
                enemybulletl.y = enemyl.y

            # Collision - EnemyL
            hitl = isHit(enemyl.x, enemyl.y, bullet.x, bullet.y)
            enemyhitl = isEnemyHit(
                player.x, player.y, enemybulletl.x, enemybulletl.y
            )
            collisionl = isCollision(player.x, player.y, enemyl.x, enemyl.y)

            # Player EnemyL
            if hitl and player.status == True:
                bullet.y = 480
                bullet.fire = False
                points += 1
                explosionSound = pygame.mixer.Sound("explosion.wav")
                explosionSound.play()
                enemyl.status = False
                enemyl.respawn = 0

            # EnemyL hits player
            if (enemyhitl or collisionl) and player.status == True:
                enemypoints += 1
                enemybulletl.x = enemyl.x
                enemybulletl.y = enemyl.y
                explosionSound = pygame.mixer.Sound("explosion.wav")
                explosionSound.play()
                player.status = False
                player.respawn = 0
                counter = 5

        # Shows score on upper left of the screen
        score("Player Score", 10, 10, points)
        score("Enemy Score", 10, 30, enemypoints)

        # Keyboard input
        for event in pygame.event.get():
            # Player closed the window
            if event.type == pygame.QUIT:
                running = False
            # Player presses keys
            if event.type == pygame.KEYDOWN and player.status == True:
                if event.key == pygame.K_RIGHT:
                    player.x_chg = 5
                elif event.key == pygame.K_LEFT:
                    player.x_chg = -5
                elif event.key == pygame.K_DOWN:
                    player.y_chg = 5
                elif event.key == pygame.K_UP:
                    player.y_chg = -5
                elif event.key == pygame.K_SPACE:
                    if bullet.fire == False:
                        bullet.fire = True
                        bullet.x = player.x + 16
                        bullet.y = player.y
                        bullet.draw()
                        bulletSound = pygame.mixer.Sound("laser.wav")
                        bulletSound.play()

            # Player releases keys
            if event.type == pygame.KEYUP and player.status == True:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.x_chg = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player.y_chg = 0

        # Game over
        if enemypoints >= 3:
            gameover()
            gamestatus = False

        pygame.display.update()
