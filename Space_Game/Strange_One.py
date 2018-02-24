import pygame, sys
from pygame.locals import *
import os;
import random;
import math;

#Set up pygame
pygame.init()
w = 1000;
h = 1000;
#Set up the window
windowSurface = pygame.display.set_mode((w, h))
pygame.display.set_caption('Space Explorer')

myfont = pygame.font.SysFont("monospace", 20, True)
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

#Get a pixel array of the surface
def rot_center(image, angle):
	loc = image.get_rect().center
	rot_sprite = pygame.transform.rotate(image, angle)
	rot_sprite.get_rect().center = loc
	return rot_sprite
def awayFromCenter(x,y):
	xCenter=w/2;
	yCenter=h/2;
	dif=math.sqrt(math.pow(x-xCenter,2)+math.pow(y-yCenter,2))
	return dif;
def calculate_new_x(old_x,speedy,angle_in_radians):
	new_x = old_x + (speedy*math.cos(angle_in_radians))
	return new_x
def calculate_new_y(old_y,speedy,angle_in_radians):
	new_y = old_y + (speedy*math.sin(angle_in_radians))
	return new_y
def d2r(d):
	"""Convert degrees into radians."""
	return math.radians(d)
bullets = [];
class Bullet:
	def __init__(self, x, y, angle, speed):
		self.x = x+31
		self.y = y
		self.angle = angle
		self.speed = speed
		self.lifetime = 0
	def show(self):
		pygame.draw.circle(windowSurface, WHITE, (int(self.x), int(self.y)), 2, 0);
		#pygame.draw.line(windowSurface, WHITE, (self.x,self.y), (self.x,self.y), 2)
	def refreshPos(self):
		self.x += (self.x - calculate_new_x(self.x, self.speed, d2r(-(self.angle-90))));
		self.y += (self.y - calculate_new_y(self.y, self.speed, d2r(-(self.angle-90))));
class Ship:
	def __init__(self, x, y):
		self.x = x;
		self.y = y;
		self.angle = 0;
		self.speed=0;
		self.dirX = 0;
		self.dirY = 0;
		self.img = pygame.image.load('ship.png');
	def show(self):
		windowSurface.blit(rot_center(self.img, self.angle),(self.x,self.y));
	def shoot(self):
		if (pressed_bar):
			bullets.append(Bullet(self.x, self.y, self.angle,15));
	def move(self):
		for i in range(len(asteroids)):
			asteroids[i].x += (self.x - calculate_new_x(self.x, self.speed, d2r(-(self.angle + 90))));
			asteroids[i].y += (self.y - calculate_new_y(self.y, self.speed, d2r(-(self.angle + 90))));
		for i in range(len(bullets)):
			bullets[i].x += (self.x - calculate_new_x(self.x, self.speed, d2r(-(self.angle + 90))));
			bullets[i].y += (self.y - calculate_new_y(self.y, self.speed, d2r(-(self.angle + 90))));
		global score;
		score=round(score+0.1*self.speed)
		print(score);
		if (pressed_up and self.speed <= 10):
			self.speed += 0.1;
		if (not pressed_up and self.speed >= 0.1):
			self.speed -= 0.1;
		if (not pressed_down and self.speed <= 0.1):
			self.speed += 0.1;
		if (pressed_down and self.speed >= -5):
			self.speed -= 0.1;
		if (pressed_left):
			self.angle += 5;
		if (pressed_right):
			self.angle -= 5;
	def returnDir(self):
		self.dir = "";
		print(self.dirX, self.dirY);
		if (self.dirX <= 5 and self.dirX >= -5 and self.dirY > 0):
			self.dir += "up";
		elif (self.dirX <= 5 and self.dirX >= -5 and self.dirY < 0):
			self.dir += "down";
		if (self.dirX <= 11 and self.dirX >= -5 and self.dirY <= 5 and self.dirY >= -5):
			self.dir += "left";
		elif (self.dirX >= -11 and self.dirX <= -5 and self.dirY <= 5 and self.dirY >= -5):
			self.dir += "right";
		return self.dir;

class Asteroid:
	def __init__(self, x, y, size):
		self.x = x;
		self.y = y;
		self.size = size;
		# generation des variables aleatoires
		self.nbrRandom = [];
		for i in range(16):
			self.nbrRandom.append(random.randint(0, size))
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
		pygame.draw.polygon(windowSurface, WHITE, [self.v1, self.v2, self.v3, self.v4, self.v5, self.v6, self.v7, self.v8], 2)

	def move(self):
		self.x += (self.moveDir[0] * 100)/((self.size)*30);
		self.y += (self.moveDir[1] * 100)/((self.size)*30);
		'''
		self.x += self.moveDir[0];
		self.y += self.moveDir[1];
		'''
asteroids = [];

ship = Ship(w/2, h/2);
pressed_bar = False;
pressed_left = False;
pressed_right = False;
pressed_up = False;
pressed_down = False;

def spawnAsteroids(xMin,xMax, yMin, yMax):
    for i in range(2):
        for j in range(2):
            x = random.randint(xMin, xMax);
            y = random.randint(yMin, yMax);
            size = random.randint(1, 60);
            asteroids.append(Asteroid(x, y, size));

while True:
	ast_already_in_screen = False;
	pygame.display.update()
	windowSurface.fill(BLACK)

	for i in range(len(bullets)):
		bullets[i].refreshPos();
		bullets[i].show();
	for i in range(len(asteroids)):
		asteroids[i].move();
		asteroids[i].refreshPos();
		asteroids[i].show();
		if (asteroids[i].x > -w and asteroids[i].x < w and asteroids[i].y > -h and asteroids[i].y < h):
			ast_already_in_screen = True;

	if (not ast_already_in_screen):
		if (pressed_up):
			if (ship.returnDir() == "up"):
				for i in range(10):
					spawnAsteroids(-w, w*2, -h*2, 0);
			if (ship.returnDir() == "down"):
				for i in range(10):
					spawnAsteroids(-w, w*2, 0, h*2);
			if (ship.returnDir() == "left"):
				spawnAsteroids(-w*3, w, -h*2, h*2);
			if (ship.returnDir() == "right"):
				spawnAsteroids(w, w*3, -h*2, h*2);
	ship.show();
	ship.move();
	ship.shoot();
	for event in pygame.event.get():
		pressed = pygame.key.get_pressed();
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				pressed_bar = True;
			if event.key == pygame.K_UP:
				pressed_up = True;
			if event.key == pygame.K_DOWN:
				pressed_down = True;
			if event.key == pygame.K_RIGHT:
				pressed_right = True;
			if event.key == pygame.K_LEFT:
				pressed_left = True;
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_SPACE:
				pressed_bar = False;
			if event.key == pygame.K_UP:
				pressed_up = False;
			if event.key == pygame.K_DOWN:
				pressed_down = False;
			if event.key == pygame.K_RIGHT:
				pressed_right = False;
			if event.key == pygame.K_LEFT:
				pressed_left = False;
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
	global score;
	scoretext = myfont.render("DISTANCE: "+str(score), 1, (255,255,255))
	windowSurface.blit(scoretext, (800, 950))
	clock.tick(60);
