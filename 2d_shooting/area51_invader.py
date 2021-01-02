
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
        screen.blit(playerImg, (self.x,self.y))


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

class enemy(object):

    def __init__(self):

        # Enemy random respawn  -- Moving to right
        self.rx = random.randint(0, 768)
        self.ry = random.randint(60, 150)
        self.rx_chg = 0
        self.statusr = True
        self.respawnr = 300
        self.firer = True
        self.firel = True

        # Enemy random respawn  -- Moving to left
        self.lx = random.randint(0, 768)
        self.ly = random.randint(60, 150)
        self.lx_chg = 0
        self.statusl = True
        self.respawnl = 300


    def draw_enemy_r(self):
        enemyImg = pygame.image.load("enemy.png")
        screen.blit(enemyImg, (self.rx, self.ry))

    def draw_enemy_l(self):
        enemyImg = pygame.image.load("enemy.png")
        screen.blit(enemyImg, (self.lx, self.ly))

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
    font = pygame.font.SysFont('freemono', 16)
    scoreImg = font.render(f"{label} : {points}", True, (0, 0, 255))
    screen.blit(scoreImg, (x, y))

def gameover():
    font = pygame.font.SysFont('freemono', 64)
    gameoverImg = font.render("Game Over", True, (255, 0 ,0))
    screen.fill((0, 0, 0))
    screen.blit(gameoverImg,(204.5, 260))

def startgame(countdown):
    font = pygame.font.SysFont('Constantia', 128)
    startgameImg = font.render(str(countdown), True, (255, 0, 0))
    screen.blit(startgameImg,(350,220))

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
    enemy = enemy()
    enemybulletr = enemybullet(enemy.rx, enemy.ry)
    enemybulletl = enemybullet(enemy.lx, enemy.ly)

    while running:

        # Background
        background = pygame.image.load("51.png")
        screen.blit(background, (0, 0))

        # Draws player
        drawplayer = player.draw()

        # Draws enemy moving right
        if enemy.statusr == False and enemy.respawnr < 300:
            enemy.rx = 1900
            enemy.ry = 1900
            enemy.respawnr += 1
        else:
            drawenemyr = enemy.draw_enemy_r()
            enemy.respawnr = 300
            enemy.statusr = True

        # Draws enemy moving left
        if enemy.statusl == False and enemy.respawnl < 300:
            enemy.lx = 1900
            enemy.ly = 1900
            enemy.respawnl += 1
        else:
            drawenemyl = enemy.draw_enemy_l()
            enemy.respawnl = 300
            enemy.statusl = True

        # Score
        score("Player Score", 10, 10, points)
        score("Enemy Score", 10, 30, enemypoints)

        # Start game counter
        if counter > 0:
            startgame(counter)
            time_now = pygame.time.get_ticks()
            player.x = 370
            player.y = 480
            player.status = False
            enemy.statusr = False
            enemy.statusl = False
            enemy.firer = False
            enemy.firel = False
            if time_now - last_count > 1000:
                counter -=1
                last_count = time_now
        elif counter == 0:
            enemy.firer = True
            enemy.firel = True
            player.status = True
            #enemy.statusr = True
            #enemy.statusl = True

        # Keyboard input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
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

            if  event.type == pygame.KEYUP and player.status == True:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.x_chg = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player.y_chg = 0

        # EnemyR Movement
        if enemy.statusr == True:

            if enemy.rx >=0 and enemy.rx <=768:
                enemy.rx_chg = 0.5
            else:
                enemy.rx = random.randint(0, 768)
                enemy.ry = random.randint(60, 150)
            enemy.rx += enemy.rx_chg

        # Fires EnemyR Bullet
        if enemybulletr.y < 600 and enemy.firer == True:
            enemybulletr.y -= enemybulletr.y_chg
            enemybulletr.draw()
        if enemybulletr.y > 595 and enemy.firer == True:
            enemybulletr.x = enemy.rx
            enemybulletr.y = enemy.ry

        # EnemyL Movement
        if enemy.statusl == True:
            if enemy.lx <=736 and enemy.lx >=0:
                enemy.lx_chg = -0.5
            else:
                enemy.lx = random.randint(0, 768)
                enemy.ly = random.randint(60, 150)
            enemy.lx += enemy.lx_chg

        # Fires EnemyL Bullet
        if enemybulletl.y < 600 and enemy.firel == True:
            enemybulletl.y -= enemybulletl.y_chg
            enemybulletl.draw()
        if enemybulletl.y > 595:
            enemybulletl.x = enemy.lx
            enemybulletl.y = enemy.ly

        # Player Movement
        player.x += player.x_chg
        player.y += player.y_chg

        # Player movement boundary
        if player.status == True:
            if player.x <= 0:
                player.x = 0
            if player.x >=736:
                player.x = 736
            if player.y <= 0:
                player.y = 0
            if player.y >= 536:
                player.y = 536

        # Bullet Movement
        if bullet.fire == True and player.status == True:
            bullet.draw()
            bullet.y -= bullet.y_chg
        if bullet.y <=0:
            bullet.x = player.x
            bullet.y = player.y
            bullet.fire = False

        # Collision
        hitr = isHit(enemy.rx, enemy.ry, bullet.x, bullet.y)
        hitl = isHit(enemy.lx, enemy.ly, bullet.x, bullet.y)
        enemyhitr = isEnemyHit(player.x, player.y, enemybulletr.x, enemybulletr.y)
        enemyhitl = isEnemyHit(player.x, player.y, enemybulletl.x, enemybulletl.y)
        collisionr = isCollision(player.x, player.y, enemy.rx, enemy.ry)
        collisionl = isCollision(player.x, player.y, enemy.lx, enemy.ly)

        # Player hits the enemy moving right
        if hitr and player.status == True:

            bullet.y = 480
            bullet.fire = False
            points += 1
            explosionSound = pygame.mixer.Sound("explosion.wav")
            explosionSound.play()
            enemy.statusr = False
            enemy.respawnr = 0

        # Player hits the enemy moving left
        if hitl and player.status == True:

            bullet.y = 480
            bullet.fire = False
            points += 1
            explosionSound = pygame.mixer.Sound("explosion.wav")
            explosionSound.play()
            enemy.statusl = False
            enemy.respawnl = 0

        # Enemy moving right hits the player
        if (enemyhitr or collisionr) and player.status == True:
            enemypoints += 1
            enemybulletr.x = enemy.rx
            enemybulletr.y = enemy.ry
            explosionSound = pygame.mixer.Sound("explosion.wav")
            explosionSound.play()
            player.status = False
            player.respawn = 0
            counter = 5

        # Enemy moving left hits the player
        if (enemyhitl or collisionl) and player.status == True:
            enemypoints += 1
            enemybulletl.x = enemy.lx
            enemybulletl.y = enemy.ly
            explosionSound = pygame.mixer.Sound("explosion.wav")
            explosionSound.play()
            player.status = False
            player.respawn = 0
            counter = 6

        # Game over
        if enemypoints >= 3:
            gameover()
            player.status = False
            enemy.statusr = False
            enemy.statusl = False
            enemy.firer = False
            enemy.firel = False
            enemy.rx = 1900
            enemy.ry = 1900
            enemy.lx = 1900
            enemy.ly = 1900
            enemybulletr.x = enemy.rx
            enemybulletr.y = enemy.ry
            enemybulletl.x = enemy.lx
            enemybulletl.y = enemy.ly


        pygame.display.update()
