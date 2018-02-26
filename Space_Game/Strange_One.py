import pygame, sys
from pygame.locals import *
import os;
import random;
import math;
import threading
import time;

#Set up pygame
pygame.init()
w = 1960;
h = 1080;
#Set up the window
windowSurface = pygame.display.set_mode((w, h))
pygame.display.set_caption('Space Explorer')

myfont1 = pygame.font.SysFont("monospace", 30, True)
myfont2 = pygame.font.Font(os.path.join('pixelart.ttf'), 22)
myfont3 = pygame.font.Font(os.path.join('pixelart.ttf'), 16)

score=0

BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)

basicFont = pygame.font.SysFont(None, 48)

clock = pygame.time.Clock()

windowSurface.fill(BLACK)
#Draw a blue poligon onto the surface
#pygame.draw.polygon(windowSurface, BLUE, ((650, 0), (500,600),(650,400), (0,600) ))
#Draw a green poligon onto the surface}}}
'''
for i in range(50):
    x = random.randint(0, w)
    y = random.randint(0, h)
    pygame.draw.polygon(windowSurface, WHITE, [[x, y], [x+10, y-10], [x+60, y-10], [x+30, y], [x+30, y+10], [x+60, y+60], [x+10, y+60], [x, y+10]], 1)
for i in range(150):
    x = random.randint(0, w)
    y = random.randint(0, h)
    pygame.draw.polygon(windowSurface, WHITE, [[x+random.randint(-10, 10), y+random.randint(-10, 10)], [x+10+random.randint(-10, 10), y-10+random.randint(-10, 10)], [x+60+random.randint(-10, 10), y-10+random.randint(-10, 10)], [x+30+random.randint(-10, 10), y+random.randint(-10, 10)], [x+30+random.randint(-10, 10), y+10+random.randint(-10, 10)], [x+60+random.randint(-10, 10), y+60+random.randint(-10, 10)], [x+10+random.randint(-10, 10), y+60+random.randint(-10, 10)], [x+random.randint(-10, 10), y+10+random.randint(-10, 10)]], 1)
'''
#Draw a red circle onto the surface
#pygame.draw.circle(windowSurface, RED, (650,600), 165)
 #Get a pixel array of the surface
def set_timeout(func, sec):
    global t;
    t.cancel();
    def func_wrapper():
        func()
        t.cancel()
    t = threading.Timer(sec, func_wrapper)
    t.start()

t = threading.Timer(1, set_timeout);
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

def d6r(d):
    """Convert degrees into radians."""
    return math.radians(d)

images = []
fileNumber_expl=-1
for file_name in os.listdir('images'):
    sub1=file_name
    images.append([])
    fileNumber_expl+=1
    i=0
    for file_name in os.listdir('images/'+str(file_name)):
        fileN = str(file_name)
        image = pygame.image.load('images/' + sub1 + '/' + str(i) + '.' + fileN[len(fileN)-3] + fileN[len(fileN)-2] + fileN[len(fileN)-1]).convert()
        images[int(sub1)].append(image)
        i+=1

planets_images = []
planets_images.append([])
planets_images.append([])
planets_images.append([])
planets_images.append([])
planets_images.append([])
planets_images.append([])
planets_images.append([])
planets_images.append([])
planets_images.append([])
planets_images.append([])
planets_images.append([])
planets_images.append([])
planets_images.append([])
planets_images.append([])
planets_images.append([])
planets_images.append([])
planets_images.append([])
planets_images.append([])
fileNumber_plan=-1
for file_name in os.listdir('planets'):
    sub1=file_name
    fileNumber_plan+=1
    i=0
    for file_name in os.listdir('planets/'+str(file_name)):
        fileN = str(file_name)
        image = pygame.image.load('planets/' + sub1 + '/' + str(i) + '.' + fileN[len(fileN)-3] + fileN[len(fileN)-2] + fileN[len(fileN)-1]).convert()
        str(i) + '.' + fileN[len(fileN)-3] + fileN[len(fileN)-2] + fileN[len(fileN)-1]
        planets_images[int(sub1)].append(image)
        i+=1
print(fileNumber_plan);

class Explosion:
    def __init__(self, x, y, size):
        global fileNumber;
        self.size = size
        self.list = images[random.randint(0,fileNumber_expl)]
        self.image = self.list[0]
        self.x = x
        self.y = y
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 20
    def update(self):
        now = pygame.time.get_ticks()
        windowSurface.blit(self.image,(self.x,self.y));
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            if (self.frame != len(self.list)):
                self.frame += 1
            if self.frame != len(self.list):
                self.image = pygame.transform.scale(self.list[self.frame], (self.size*2, self.size*2))

class Bullet:
    def __init__(self, x, y, angle, speed):
        self.x = x+31
        self.y = y+31
        self.angle = angle
        self.speed = speed
        self.lifetime = 0
    def show(self):
        self.lifetime += 1;
        pygame.draw.circle(windowSurface, WHITE, (int(self.x), int(self.y)), 2, 0);
    def refreshPos(self):
        self.x += (self.x - calculate_new_x(self.x, self.speed, d6r(-(self.angle-90))));
        self.y += (self.y - calculate_new_y(self.y, self.speed, d6r(-(self.angle-90))));

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
        self.maxSpeed = 12;
    def show(self):
        windowSurface.blit(rot_center(self.img, self.angle),(self.x,self.y));
    def move(self):
        #print(int(self.dirX), int(self.dirY))
        if (self.angle > 360):
            self.angle = 0;
        if (self.angle < 0):
            self.angle = 360;
        for i in range(len(asteroids)):
            self.dirX = (self.x - calculate_new_x(self.x, self.speed, d6r(-(self.angle + 90))));
            self.dirY = (self.y - calculate_new_y(self.y, self.speed, d6r(-(self.angle + 90))));
            asteroids[i].x += self.dirX;
            asteroids[i].y += self.dirY;
        for i in range(len(explosions)):
            explosions[i].x += self.dirX;
            explosions[i].y += self.dirY;
        for i in range(len(planets)):
            planets[i].x += self.dirX;
            planets[i].y += self.dirY;
        for i in range(len(stars)):
            stars[i].x += ((self.dirX * stars[i].z)/2000)*30;
            stars[i].y += ((self.dirY * stars[i].z)/2000)*30;
        global score;
        score=score+0.1*self.speed
        if (pressed_up and self.speed <= self.maxSpeed):
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
        if (self.dirX <= self.maxSpeed/2 and self.dirX >= -self.maxSpeed/2 and self.dirY > 0):
            self.dir = "up";
        elif (self.dirX <= self.maxSpeed/2 and self.dirX >= -self.maxSpeed/2 and self.dirY < 0):
            self.dir = "down";
        elif (self.dirX <= self.maxSpeed+1 and self.dirX >= -self.maxSpeed/2 and self.dirY <= self.maxSpeed/6 and self.dirY >= -self.maxSpeed/2):
            self.dir = "left";
        elif (self.dirX >= -self.maxSpeed-1 and self.dirX <= -self.maxSpeed/2 and self.dirY <= self.maxSpeed/6 and self.dirY >= -self.maxSpeed/2):
            self.dir = "right";
        return self.dir;
    def shoot(self):
        if (pressed_bar):
            now = pygame.time.get_ticks()
            if (now - self.last_used >= self.cooldown):
                self.last_used = now
                bullets.append(Bullet(self.x, self.y, self.angle, 15));
    def notControlable(self):
        self.dirX = -self.dirX
        self.dirY = -self.dirY;
    def rotateSetTo(self, boole):
        self.rotate = boole;

asteroids_name = ["1 Ceres", "4 Vesta", "6 Pallas", "10 Hygiea", "704 Interamnia", "56 Europa", "511 Davida",
"65 Cybele", "15 Eunomia", "3 Juno", "31 Euphrosyne", "664 Hektor", "88 Thisbe", "364 Bamberga", "451 Patienta",
"536 Herculina", "48 Doris", "375 Ursula", "107 Camilla", "45 Eugenia", "7 Iris", "69 Amphirite", "463 Diotima",
"19 Fortuna", "13 Egeria", "64 Themis", "94 Aurora", "706, Alauda", "161 Hermione", "Aletheia", "376 Palma", "168 Nemenios"]
class Asteroid:
    def __init__(self, x, y, size):
        self.x = x;
        self.y = y;
        self.spawnX = x;
        self.spawnY = y;
        self.size = size;
        self.maxlife = int(size/20)
        self.life = self.maxlife
        self.dist = 1;
        self.toDisplay='Required'
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
        self.name = asteroids_name[random.randint(0, len(asteroids_name)-1)]
    def refreshPos(self):
        # generation de la forme de base de l'hexagon
        self.v1 = [self.x            , self.y];
        self.v2 = [self.x+self.size  , self.y-self.size];
        self.v3 = [self.x+self.size*2, self.y-self.size];
        self.v4 = [self.x+self.size*3, self.y];
        self.v5 = [self.x+self.size*3, self.y+self.size];
        self.v6 = [self.x+self.size*2, self.y+self.size*2];
        self.v7 = [self.x+self.size  , self.y+self.size*2];
        self.v8 = [self.x            , self.y+self.size];

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

        self.toDisplay=False
        if (self.v1[0]>0 and self.v1[0]<w and self.v6[1]>0 and self.v1[1]<h):
            self.toDisplay=True
        elif (self.v6[0]>0 and self.v6[0]<w and self.v6[1]>0 and self.v6[1]<h):
            self.toDisplay=True
        elif (self.v3[0]>0 and self.v3[0]<w and self.v3[1]>0 and self.v3[1]<h):
            self.toDisplay=True
        elif (self.v4[0]>0 and self.v4[0]<w and self.v4[1]>0 and self.v4[1]<h):
            self.toDisplay=True
        elif (self.v5[0]>0 and self.v5[0]<w and self.v5[1]>0 and self.v5[1]<h):
            self.toDisplay=True
        elif (self.v6[0]>0 and self.v6[0]<w and self.v6[1]>0 and self.v6[1]<h):
            self.toDisplay=True
        elif (self.v7[0]>0 and self.v7[0]<w and self.v7[1]>0 and self.v7[1]<h):
            self.toDisplay=True
        elif (self.v8[0]>0 and self.v8[0]<w and self.v8[1]>0 and self.v8[1]<h):
            self.toDisplay=True
        if (self.toDisplay):
            self.toDisplay=False

            pygame.draw.polygon(windowSurface, self.color, [self.v1, self.v2, self.v3, self.v4, self.v5, self.v6, self.v7, self.v8], 4)
            if (self.size > 100):
                NAME = myfont3.render(self.name, 1, (255, 255, 0))
                windowSurface.blit(NAME, (self.mostInRight, (self.y+self.size)))

                SIZE = myfont3.render("SIZE  " + str(self.size), 1, (255, 255, 0))
                windowSurface.blit(SIZE, (self.mostInRight, (self.y+self.size+self.size/4)))
        #pygame.draw.line(windowSurface, (255, 255, 255), (self.spawnX, self.spawnY), ((self.x, self.y )))
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
            health = (self.life * self.size / self.maxlife)
            #health = (self.life * self.size / self.maxlife)/10
            pygame.draw.rect(windowSurface, GREEN, (self.mostInLeft, self.bestY, health*(self.mostInRight-self.mostInLeft)/70,  self.size/3))

class Planet:
    def __init__(self, x, y, size):
        global fileNumber_plan;
        self.size = size
        self.list = planets_images[random.randint(0,fileNumber_plan)]
        self.image = self.list[0]
        img_size = self.image.get_size()
        self.size_X = int(img_size[0]*(self.size/img_size[0]))
        self.size_Y = int(img_size[1]*(self.size/img_size[0]))
        self.x = x
        self.y = y
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 20
    def update(self):
        now = pygame.time.get_ticks()
        # Différence des x et différence des y
        dx, dy = (self.x)*2 - ship.x, (self.y)*6 - ship.y
        # On cherche l'hypoténuse du triangle formé par dx et dy
        self.dist = math.hypot(dx, dy)
        dx, dy = dx / self.dist, dy / self.dist
        # move along this normalized vector towards the player at current speed
        self.x += -100 * (dx/1000  )
        self.y += -100 * (dy/1000  )
        if (self.x>0-self.size and self.x<w+self.size and self.y>0-self.size and self.y<h+self.size):
            windowSurface.blit(self.image,(self.x,self.y));
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.frame += 1
                if (self.frame == len(self.list)):
                    self.frame = 0
                self.image= pygame.transform.scale(self.list[self.frame], (self.size_X, self.size_Y))

class Star:
    def __init__(self, x, y, z):
        self.x = x;
        self.y = y;
        self.z = z;
    def show(self):
        if (self.z > 0):
            pygame.draw.circle(windowSurface, WHITE, (int(self.x), int(self.y)),int(self.z/100));

def map(n, start1, stop1, start2, stop2):
    newval = (n - start1) / (stop1 - start1) * (stop2 - start2) + start2;
    if (start2 < stop2):
        return max(min(newval, stop2), start2)
        #return this.constrain(newval, start2, stop2);
    else:
        return max(min(newval, start2), stop2)
        #return this.constrain(newval, stop2, start2);
class Minimap:
    def __init__(self, x, y):
        self.x = x;
        self.y = y;
        self.size = 200;
        self.zoomW = render_distance[0]
        self.zoomH = render_distance[1]
    def show(self):
        pygame.draw.rect(windowSurface, [50, 50, 0], (self.x, self.y, self.size, self.size), 12);
        windowSurface.fill(BLACK, rect=[self.x, self.y,  self.size,  self.size])

        pX = self.size/2
        pY = pX

        pygame.draw.circle(windowSurface, BLUE, (int(pX), int(pY)), 5)

        for i in range(len(asteroids)):
            if (asteroids[i].y > -self.zoomH and asteroids[i].y < self.zoomH):
                if (asteroids[i].x < self.zoomW or asteroids[i].x > -self.zoomW):
                    x = map(asteroids[i].x, -self.zoomW, self.zoomW, 0, self.size);
                    y = map(asteroids[i].y, -self.zoomH, self.zoomH, 0, self.size);
                    size = map(asteroids[i].size, 0, max_ast_size, 1, 6);
                    pygame.draw.circle(windowSurface, asteroids[i].color, (int(x*3.32/3.425), int(y*3.32/3.425)), int(size));
        for i in range(len(planets)):
            if (planets[i].y > -self.zoomH and planets[i].y < self.zoomH):
                if (planets[i].x < self.zoomW or planets[i].x > -self.zoomW):
                    x = map(planets[i].x, -self.zoomW, self.zoomW, 0, self.size);
                    y = map(planets[i].y, -self.zoomH, self.zoomH, 0, self.size);
                    size = map(planets[i].size, 0, max_ast_size, 1, 6);
                    pygame.draw.circle(windowSurface, GREEN, (int(x*3.32/3.425), int(y*3.32/3.425)), int(size));

stars = [];
explosions = [];
asteroids = [];
bullets = [];
planets = [];
rdm = 6
render_distance = [w*rdm, h*rdm]
minimap = Minimap(0, 0);

min_ast_size = 40;
max_ast_size = 120;

def spawnAsteroids(xMin,xMax, yMin, yMax):
    for i in range(2):
        for j in range(2):
            x = random.randint(xMin, xMax);
            y = random.randint(yMin, yMax);
            size = random.randint(min_ast_size, max_ast_size);
            asteroids.append(Asteroid(x, y, size));
for i in range(80):
    planets.append(Planet(random.randint(-w*50, w*50), random.randint(-h*50, h*50), random.randint(500, 900)));
for i in range(1000):
            stars.append(Star(random.randint(0, w), random.randint(0, h), random.randint(1, 140)))

spawnAsteroids(0, w, 0, h);
ship = Ship(w/2, h/2);
pressed_left = False;
pressed_right = False;
pressed_up = False;
pressed_down = False;
pressed_bar = False;

SCORE_COOLDOWN = 1000;
SCORE_UP_AMOUNT = 0;
SCORE_UP_SHOW = False;
def scoreUpToFalse():
    global SCORE_UP_SHOW
    SCORE_UP_SHOW = False;
def set_timeout(func, sec):
    t = None
    def func_wrapper():
        func()
        t.cancel()
    t = threading.Timer(sec, func_wrapper)
    t.start()

while True:
    global score;
    ast_already_in_screen = False;
    pygame.display.update()
    windowSurface.fill(BLACK)
    index_bullet_to_remove = [];
    index_asteroid_to_remove = [];
    index_explosion_to_remove = [];

    for i in range(len(explosions)):
        explosions[i].update();
        if explosions[i].frame == len(explosions[i].list):
            index_explosion_to_remove.append(i);

    for i in range(len(planets)):
        planets[i].update();
        distFromCenterX = w/2 - planets[i].x;
        distFromCenterY = h/2 - planets[i].y;
        radiusX=int(math.fabs(distFromCenterX)/100)
        radiusY=int(math.fabs(distFromCenterY)/100)
        Show = True;
        if radiusX>30000:
            Show = False;
        elif radiusX>150:
            radiusX=150
        if radiusY>30000:
            Show = False;
        elif radiusY>150:
            radiusY=150
        if (Show):
            #Gauche
            if (planets[i].x < 0):
                pygame.draw.circle(windowSurface, GREEN, (0, int(planets[i].y+planets[i].size/2)), radiusX, 1);
            #Droite
            if (planets[i].x > w):
                pygame.draw.circle(windowSurface, GREEN, (w-10, int(planets[i].y+planets[i].size/2)), radiusX, 1);
            #Haut
            if (planets[i].y < 0):
                pygame.draw.circle(windowSurface, GREEN, (int(planets[i].x+planets[i].size/2), 10), radiusY, 1);
            #Bas
            if (planets[i].y > h):
                pygame.draw.circle(windowSurface, GREEN, (int(planets[i].x+planets[i].size/2), h-10), radiusY, 1);

    for i in range(len(asteroids)):
        #pygame.draw.lines(windowSurface, WHITE, False, [[asteroids[i].x, asteroids[i].y], [ship.x, ship.y]], 1)
        asteroids[i].move();
        asteroids[i].refreshPos();
        asteroids[i].show();
        distFromCenterX = w/2 - asteroids[i].x;
        distFromCenterY = h/2 - asteroids[i].y;
        if (math.fabs(distFromCenterX) > render_distance[0]*1.4 and len(asteroids) > 1 or math.fabs(distFromCenterY) > render_distance[1]*1.4 and len(asteroids) > 1):
            index_asteroid_to_remove.append(i);
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
            #random.choice(expl_sounds).play()
            xExpl = asteroids[i].x+asteroids[i].size
            yExpl = asteroids[i].y-2/asteroids[i].size
            explosions.append(Explosion(xExpl,yExpl,asteroids[i].size));
            if (asteroids[i].size/1.8 > 20):
                for e in range(2):
                    asteroids.append(Asteroid(asteroids[i].x, asteroids[i].y, int(asteroids[i].size/1.8)));
            index_asteroid_to_remove.append(i);
            ship.rotateSetTo(True);
            ship.notControlable();
            last_up=-10*asteroids[i].size
            if ((score+last_up)<=0):
                score=0;
            else:
                score+=last_up;
            SCORE_UP_SHOW = True;
            set_timeout(scoreUpToFalse, 1)

    for i in range(len(bullets)):
        bullets[i].refreshPos();
        bullets[i].show()
        for j in range(len(asteroids)):
            if (bullets[i].x >= asteroids[j].v1[0] and bullets[i].x <= asteroids[j].v4[0]  and bullets[i].y >= asteroids[j].v2[1] and bullets[i].y <= asteroids[j].v7[1]):
                #random.choice(expl_sounds).play()
                if (asteroids[j].life==1):
                    xExpl = asteroids[j].x+asteroids[j].size
                    yExpl = asteroids[j].y-2/asteroids[j].size
                    explosions.append(Explosion(xExpl,yExpl,asteroids[j].size));
                    index_asteroid_to_remove.append(j);

                    last_up=10*asteroids[j].size
                    score+=last_up
                    SCORE_UP_SHOW = True;
                    set_timeout(scoreUpToFalse, 1)

                    if (asteroids[j].size/1.8 > 20):
                        for e in range(2):
                            asteroids.append(Asteroid(asteroids[j].x, asteroids[j].y, int(asteroids[j].size/1.8)));
                else:
                    asteroids[j].life-=1
                index_bullet_to_remove.append(i);

        if (bullets[i].lifetime > 70 and i not in bullets):
            index_bullet_to_remove.append(i);


    for i in range(len(index_explosion_to_remove)):
        try:
            explosions.remove(explosions[index_explosion_to_remove[i]]);
        except:
            continue

    for i in range(len(index_bullet_to_remove)):
        try:
            bullets.remove(bullets[ index_bullet_to_remove[i]]);
        except:
            continue

    for i in range(len(index_asteroid_to_remove)):
        try:
            asteroids.remove(asteroids[ index_asteroid_to_remove[i]])
        except:
            spawnAsteroids(-w*2, w/2, -h*2, -h)
            pass;

    if (not ast_already_in_screen):
        if (pressed_up):
            if (ship.returnDir() == "up"):
                for i in range(8):
                    spawnAsteroids(-render_distance[0], render_distance[0], -render_distance[1], 0);
            if (ship.returnDir() == "down"):
                for i in range(8):
                    spawnAsteroids(-render_distance[0], render_distance[0], 0, render_distance[1]);
            if (ship.returnDir() == "left"):
                for i in range(4):
                    spawnAsteroids(-render_distance[0], render_distance[0], -render_distance[1], render_distance[1]);
            if (ship.returnDir() == "right"):
                for i in range(4):
                    spawnAsteroids(-render_distance[0], render_distance[0], -render_distance[1], render_distance[1]);
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
    minimap.show();
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
    scoretext = myfont2.render("SCORE  "+str(round(score)), 1, WHITE)
    windowSurface.blit(scoretext, (w-200, h-110))
    DIRECTION = myfont2.render(ship.returnDir(), 1, (77,255,77))
    windowSurface.blit(DIRECTION, (20, minimap.size+25))
    HUD = myfont3.render("FPS  "+str(round(clock.get_fps(), 2)), 1, WHITE)
    windowSurface.blit(HUD, (w-200, h-70))
    if (SCORE_UP_SHOW):
        if (last_up<=0):
            SCORE_UP = myfont1.render("- "+str(-1*(last_up)), 1, (255,77,77));
        else:
            SCORE_UP = myfont1.render("+ "+str(last_up), 1, (77,255,77));
        windowSurface.blit(SCORE_UP, (w-200, h-150))
    clock.tick(60);
