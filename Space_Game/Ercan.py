import pygame, sys
from pygame.locals import *
import os;
import random;
import math;
import threading
import time;
#Set up pygame
pygame.init()
w = 1920;
h = 1080;
#Set up the window
windowSurface = pygame.display.set_mode((w, h))
pygame.display.set_caption('Space Explorer')


BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)

basicFont = pygame.font.SysFont("monospace", 48)

clock = pygame.time.Clock()

windowSurface.fill(BLACK)
#Draw a blue poligon onto the surface
#pygame.draw.polygon(windowSurface, BLUE, ((250, 0), (500,200),(250,400), (0,200) ))
#Draw a green poligon onto the surface}}}
'''
for i in range(50):
    x = random.randint(0, w)
    y = random.randint(0, h)
    pygame.draw.polygon(windowSurface, WHITE, [[x, y], [x+10, y-10], [x+20, y-10], [x+30, y], [x+30, y+10], [x+20, y+20], [x+10, y+20], [x, y+10]], 1)
for i in range(150):
    x = random.randint(0, w)
    y = random.randint(0, h)
    pygame.draw.polygon(windowSurface, WHITE, [[x+random.randint(-10, 10), y+random.randint(-10, 10)], [x+10+random.randint(-10, 10), y-10+random.randint(-10, 10)], [x+20+random.randint(-10, 10), y-10+random.randint(-10, 10)], [x+30+random.randint(-10, 10), y+random.randint(-10, 10)], [x+30+random.randint(-10, 10), y+10+random.randint(-10, 10)], [x+20+random.randint(-10, 10), y+20+random.randint(-10, 10)], [x+10+random.randint(-10, 10), y+20+random.randint(-10, 10)], [x+random.randint(-10, 10), y+10+random.randint(-10, 10)]], 1)
'''
#Draw a red circle onto the surface
#pygame.draw.circle(windowSurface, RED, (250,200), 125)
HUD = basicFont.render("bonjour je suis du texte", 1, (255,255,0))
 #Get a pixel array of the surface
def set_timeout(func, sec):
    t = None
    def func_wrapper():
        func()
        t.cancel()
    t = threading.Timer(sec, func_wrapper)
    t.start()

def returnEdgeDist():
	center = [w/2, h/2];
	dist_to_CENTER = [math.fabs(ship.x - center[0]), math.fabs(ship.y - center[1])];
	return  dist_to_CENTER;
def rot_center(image, angle):
    loc = image.get_rect().center
    rot_sprite = pygame.transform.rotate(image, angle)
    rot_sprite.get_rect().center = loc
    return rot_sprite

def calculate_new_x(old_x,speed,angle_in_radians):
    new_x = old_x + (speed*math.cos(angle_in_radians))
    return new_x
def calculate_new_y(old_y,speed,angle_in_radians):
    new_y = old_y + (speed*math.sin(angle_in_radians))
    return new_y
def d2r(d):
    """Convert degrees into radians."""
    return math.radians(d)
class Bullet:
    def __init__(self, x, y, angle, speed):
        self.x = x+31
        self.y = y+31
        self.angle = angle
        self.speed = speed
        self.lifetime = 0
    def show(self):
        self.lifetime += 1;
        pygame.draw.circle(windowSurface, WHITE, (int(self.x), int(self.y)), 5, 1);
    def refreshPos(self):
        self.x += (self.x - calculate_new_x(self.x, self.speed, d2r(-(self.angle-90))));
        self.y += (self.y - calculate_new_y(self.y, self.speed, d2r(-(self.angle-90))));
class Ship:
    def __init__(self, x, y):
        self.x = x;
        self.y = y;
        self.angle = 0;
        self.speed= 0;
        self.vel = 0.1;
        self.img = pygame.image.load('ship.png');
        self.dirX = 0;
        self.dirY = 0;
        self.last_used = pygame.time.get_ticks()
        self.cooldown = 200
    def show(self):
        windowSurface.blit(rot_center(self.img, self.angle),(self.x,self.y));
    def move(self):
        #print(int(self.dirX), int(self.dirY))
        if (self.angle > 360):
            self.angle = 0;
        if (self.angle < 0):
            self.angle = 360;
        for i in range(len(asteroids)):
            self.dirX = (self.x - calculate_new_x(self.x, self.speed, d2r(-(self.angle + 90))));
            self.dirY = (self.y - calculate_new_y(self.y, self.speed, d2r(-(self.angle + 90))));
            asteroids[i].x += self.dirX;
            asteroids[i].y += self.dirY;
        for i in range(len(planets)):
            planets[i].x += self.dirX;
            planets[i].y += self.dirY;
        for i in range(len(stars)):
            stars[i].x += ((self.dirX * stars[i].z)/2000)*10;
            stars[i].y += ((self.dirY * stars[i].z)/2000)*10;
        if (pressed_up and self.speed <= 100):
            self.speed += 0.1;
        if (not pressed_up and self.speed >= 0.1):
            self.speed -= 0.1;
        if (not pressed_down and self.speed <= 0.1):
            self.speed += 0.1;
        if (pressed_down and self.speed >= -5):
            self.speed -= 0.1;
        if (pressed_left):
            self.angle += 4;
        if (pressed_right):
            self.angle -= 4;
    def returnDir(self):
       self.dir = "";
       if (self.dirX <= 5 and self.dirX >= -5 and self.dirY > 0):
        self.dir = "up";
       elif (self.dirX <= 5 and self.dirX >= -5 and self.dirY < 0):
        self.dir = "down";
       if (self.dirX <= 11 and self.dirX >= -5 and self.dirY <= 5 and self.dirY >= -5):
        self.dir = "left";
       elif (self.dirX >= -11 and self.dirX <= -5 and self.dirY <= 5 and self.dirY >= -5):
        self.dir = "right";
       return self.dir;
    def shoot(self):
        if (pressed_bar):
            now = pygame.time.get_ticks()
            if (now - self.last_used >= self.cooldown):
                self.last_used = now
                bullets.append(Bullet(self.x, self.y, self.angle, 15));

class Asteroid:
    def __init__(self, x, y, size):
        self.x = x;
        self.y = y;
        self.size = size;
        self.maxlife = int(size/20)
        self.life = self.maxlife
        self.dist = 1;
        # generation des variables aleatoires
        self.nbrRandom = [];
        for i in range(16):
            self.nbrRandom.append(random.randint(0, size))

        self.refreshPos();
        if (random.randint(0, 10) <= 8):
            self.color = WHITE
        else:
            self.color = RED
        # chaque asteroide est en mouvement dance l'espace, on genere les directions
        self.moveDir = [random.uniform(-1, 1), random.uniform(-1, 1)]

    def refreshPos(self):
        # generation de la forme de base de l'hexagon
        self.v1 = [self.x			 , self.y];
        self.v2 = [self.x+self.size  , self.y-self.size];
        self.v3 = [self.x+self.size*2, self.y-self.size];
        self.v4 = [self.x+self.size*3, self.y];
        self.v5 = [self.x+self.size*3, self.y+self.size];
        self.v6 = [self.x+self.size*2, self.y+self.size*2];
        self.v7 = [self.x+self.size  , self.y+self.size*2];
        self.v8 = [self.x			 , self.y+self.size];

        # on ajoute nos valeurs aleatoires
        self.v1[0] += self.nbrRandom[0];
        self.v1[1] += self.nbrRandom[1];

        self.v2[0] += self.nbrRandom[2];
        self.v2[1] += self.nbrRandom[3];

        self.v3[0] += self.nbrRandom[4];
        self.v3[1] += self.nbrRandom[5];

        self.v4[0] += self.nbrRandom[6];
        self.v4[1] += self.nbrRandom[7];

        self.v5[0] += self.nbrRandom[8];
        self.v5[1] += self.nbrRandom[9];

        self.v6[0] += self.nbrRandom[10];
        self.v6[1] += self.nbrRandom[11];

        self.v7[0] += self.nbrRandom[12];
        self.v7[1] += self.nbrRandom[13];

        self.v8[0] += self.nbrRandom[14];
        self.v8[1] += self.nbrRandom[15];

    def show(self):
        self.bestY = self.v1[1];
        if (self.v2[1] < self.bestY):
            self.bestY = self.v2[1];
        if (self.v3[1] < self.bestY):
            self.bestY = self.v3[1];
        if (self.v4[1] < self.bestY):
            self.bestY = self.v4[1];

        self.mostInRight = self.v3[0];
        if (self.v4[0] > self.mostInRight):
            self.mostInRight = self.v4[0];
        if (self.v5[0] > self.mostInRight):
            self.mostInRight = self.v5[0];
        if (self.v6[0] > self.mostInRight):
            self.mostInRight = self.v6[0];

        self.mostInLeft = self.v2[0];
        if (self.v1[0] < self.mostInLeft):
            self.mostInLeft = self.v1[0];
        if (self.v8[0] < self.mostInLeft):
            self.mostInLeft = self.v8[0];
        if (self.v7[0] < self.mostInLeft):
            self.mostInLeft = self.v7[0];

        pygame.draw.polygon(windowSurface, self.color, [self.v1, self.v2, self.v3, self.v4, self.v5, self.v6, self.v7, self.v8], 4)
    def move(self):
        if (self.color == WHITE):
            self.x += (self.moveDir[0] * 100)/((self.size)*1);
            self.y += (self.moveDir[1] * 100)/((self.size)*1);
        else :
            self.x += (self.moveDir[0] * 100) / ((self.size) * 30);
            self.y += (self.moveDir[1] * 100) / ((self.size) * 30);
            # Différence des x et différence des y
            dx, dy = self.x - ship.x, self.y - ship.y
            # On cherche l'hypoténuse du triangle formé par dx et dy
            self.dist = math.hypot(dx, dy)

            dx, dy = dx / self.dist, dy / self.dist
            # move along this normalized vector towards the player at current speed
            self.x += -100 * (dx / self.size)
            self.y += -100 * (dy / self.size)
    def health(self):
        if (self.maxlife > 1):
            print(self.life, self.maxlife)
            health = (self.life * self.size / self.maxlife)
            #health = (self.life * self.size / self.maxlife)/10
            pygame.draw.rect(windowSurface, GREEN, (self.mostInLeft, self.bestY, health*(self.mostInRight-self.mostInLeft)/70,  self.size/3))

class Planet:
    def __init__(self, x, y, size):
        self.x = x;
        self.y = y;
        self.size = size;
        self.rdm = random.randint(0, 15);
        if (self.rdm <= 5):
            self.planet = "mars.jpg";
        elif (self.rdm > 5 and self.rdm < 10):
            self.planet = "terre.jpg"
        else :
            self.planet = "lune.png"

        self.img = pygame.image.load(self.planet);
        self.img = pygame.transform.scale(self.img, (self.size, self.size))
        self.COLOR =  [int(random.randint(0, 255)), int(random.randint(0, 255)), int(random.randint(0, 255))];
        self.haloSize = self.size*2;
    def show(self):
        windowSurface.blit(self.img,(self.x,self.y));
        #pygame.draw.circle(windowSurface, self.COLOR, (int(self.x), int(self.y)), self.size, self.size);
        #pygame.draw.circle(windowSurface, self.COLOR, (int(self.x), int(self.y)), self.haloSize, int(self.haloSize/2));

class Star:
    def __init__(self, x, y, z):
        self.x = x;
        self.y = y;
        self.z = z;
    def show(self):
        if (self.z > 0):
            pygame.draw.circle(windowSurface, WHITE, (int(self.x), int(self.y)),int(self.z/100));

stars = [];
asteroids = [];
asteroids.append(Asteroid(50, 50, 10));
bullets = [];
planets = [];
def spawnAsteroids(xMin,xMax, yMin, yMax):
    for i in range(2):
        for j in range(2):
            x = random.randint(xMin, xMax);
            y = random.randint(yMin, yMax);
            size = random.randint(20, 120);
            asteroids.append(Asteroid(x, y, size));
for i in range(5):
    planets.append(Planet(random.randint(-w*10, w*10), random.randint(-h*10, h*10), 1000));
for i in range(15):
    for j in range(15):
        x = random.randint(0, w);
        y = random.randint(0, h);
        stars.append(Star(x, y, j*i))

spawnAsteroids(0, w, 0, h);
ship = Ship(w/2, h/2);
pressed_left = False;
pressed_right = False;
pressed_up = False;
pressed_down = False;
pressed_bar = False;
score = 0;
SCORE_COOLDOWN = 1000;
SCORE_UP_AMOUNT = 0;
SCORE_UP_SHOW = False;
def scoreUpToFalse():
    global SCORE_UP_SHOW
    SCORE_UP_SHOW = False;
while True:
    global score;
    ast_already_in_screen = False;
    pygame.display.update()
    windowSurface.fill(BLACK)
    SCORE_UP = basicFont.render("+" + str(SCORE_UP_AMOUNT), True, GREEN)

    HUD = basicFont.render( str(score), 1, (255, 255, 0))

    windowSurface.blit(HUD, (100, 100))
    index_bullet_to_remove = [];
    index_asteroid_to_remove = [];
    if (SCORE_UP_SHOW):
        windowSurface.blit(SCORE_UP, (100, 200))
    for i in range(len(planets)):
        planets[i].show();
        distFromCenterX = w/2 - planets[i].x;
        distFromCenterY = h/2 - planets[i].y;
        if (planets[i].x < 0):
            pygame.draw.circle(windowSurface, GREEN, (100, int(planets[i].y)), int(math.fabs(distFromCenterX)/100), 1);
        if (planets[i].x > w):
            pygame.draw.circle(windowSurface, GREEN, (w, int(planets[i].y)), int(math.fabs(distFromCenterX)/100), 1);
        if (planets[i].y < 0):
            pygame.draw.circle(windowSurface, GREEN, (int(planets[i].x), 10), int(math.fabs(distFromCenterY)/100), 1);
        if (planets[i].y > h):
            pygame.draw.circle(windowSurface, GREEN, (int(planets[i].x), h), int(math.fabs(distFromCenterY)/100), 1);

    for i in range(len(asteroids)):
        #pygame.draw.lines(windowSurface, WHITE, False, [[asteroids[i].x, asteroids[i].y], [ship.x, ship.y]], 1)
        asteroids[i].move();
        asteroids[i].refreshPos();
        asteroids[i].show();
        distFromCenterX = w/2 - asteroids[i].x;
        distFromCenterY = h/2 - asteroids[i].y;
        if (asteroids[i].maxlife != asteroids[i].life):
            asteroids[i].health();
        if (asteroids[i].x < 0 and asteroids[i].x > -w*2):
            pygame.draw.circle(windowSurface, asteroids[i].color, (0, int(asteroids[i].y)), int(math.fabs(distFromCenterX)/100), 1);
        elif (asteroids[i].x > w and asteroids[i].x < w*2):
            pygame.draw.circle(windowSurface, asteroids[i].color, (w-10, int(asteroids[i].y)), int(math.fabs(distFromCenterX)/100), 1);
        elif (asteroids[i].y < 0 and asteroids[i].y > -h*2):
            pygame.draw.circle(windowSurface, asteroids[i].color, (int(asteroids[i].x), 10), int(math.fabs(distFromCenterY)/100), 1);
        elif (asteroids[i].y > h and asteroids[i].y < h*2):
            pygame.draw.circle(windowSurface, asteroids[i].color, (int(asteroids[i].x), h-10), int(math.fabs(distFromCenterY)/100), 1);

        if (asteroids[i].x > -w and asteroids[i].x < w and asteroids[i].y > -h and asteroids[i].y < h):
            ast_already_in_screen = True;

        if (ship.x + 31< asteroids[i].v4[0] and ship.x + 31 > asteroids[i].v1[0] and ship.y + 31> asteroids[i].v2[1] and ship.y + 31< asteroids[i].v7[1]):
            print("ATTENTION TU ES DANS ASTEROIDE")

#        for j in range(len(asteroids)):
#            if (j != i):
#                if (asteroids[j].v1[0] <= asteroids[i].v4[0] and asteroids[j].v1[0] >= asteroids[i].v1[0] and asteroids[j].v1[1] >= asteroids[i].v1[1] and asteroids[i].v7[1] <= asteroids[i].v7[1]):
#                    index_asteroid_to_remove.append(i);
#                    index_asteroid_to_remove.append(j);
#
    for i in range(len(bullets)):
        bullets[i].refreshPos();
        bullets[i].show()
        for j in range(len(asteroids)):
            if (bullets[i].x >= asteroids[j].v1[0] and bullets[i].x <= asteroids[j].v4[0]  and bullets[i].y >= asteroids[j].v2[1] and bullets[i].y <= asteroids[j].v7[1]):
                if (asteroids[j].life == 1):
                    index_asteroid_to_remove.append(j);
                    score += asteroids[j].size;
                    SCORE_UP_AMOUNT = asteroids[j].size;
                    SCORE_UP_SHOW = True;
                    set_timeout(scoreUpToFalse, 1)

                    if (asteroids[j].size/2 > 20):
                        asteroids.append(Asteroid(asteroids[j].x, asteroids[j].y, int(asteroids[j].size/2)));
                else :
                    asteroids[j].life -= 1;

                index_bullet_to_remove.append(i);
        if (bullets[i].lifetime > 50 and i not in bullets):
            index_bullet_to_remove.append(i);



    for i in range(len(index_bullet_to_remove)):
        try:
            bullets.remove(bullets[ index_bullet_to_remove[i]]);
        except:
            continue

    for i in range(len(index_asteroid_to_remove)):
        try:
            asteroids.remove(asteroids[ index_asteroid_to_remove[i]])
        except:
            asteroids = [];
            spawnAsteroids(-w*2, w/2, -h*2, -h)
            pass;

    if (not ast_already_in_screen):
        if (pressed_up):
            if (ship.returnDir() == "up"):
                for i in range(10):
                    spawnAsteroids(-w*5, w*5, -h*5, 0);
            if (ship.returnDir() == "down"):
                for i in range(10):
                    spawnAsteroids(-w*5, w*5, 0, h*5);
            if (ship.returnDir() == "left"):
                spawnAsteroids(-w*3, w, -h, h);
            if (ship.returnDir() == "right"):
                spawnAsteroids(w, w*3, -h, h);

    ship.show();
    ship.move();
    ship.shoot();
    for i in range(len(stars)):
        stars[i].x += stars[i].z/1000;
        stars[i].y += stars[i].z/1000;
        stars[i].show();
        if (stars[i].x > w):
            stars[i].x = 0;
        if (stars[i].x < 0):
            stars[i].x = w;

        if (stars[i].y > h):
            stars[i].y = 0;
        if (stars[i].y < 0):
            stars[i].y = h;
    for event in pygame.event.get():
        pressed = pygame.key.get_pressed();
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                pressed_up = True;
            if event.key == pygame.K_DOWN:
                pressed_down = True;
            if event.key == pygame.K_RIGHT:
                pressed_right = True;
            if event.key == pygame.K_LEFT:
                pressed_left = True;
            if event.key == pygame.K_SPACE:
                pressed_bar = True;

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                pressed_up = False;
            if event.key == pygame.K_DOWN:
                pressed_down = False;
            if event.key == pygame.K_RIGHT:
                pressed_right = False;
            if event.key == pygame.K_LEFT:
                pressed_left = False;
            if event.key == pygame.K_SPACE:
                pressed_bar = False;
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    clock.tick(60);
