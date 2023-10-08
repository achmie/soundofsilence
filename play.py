import pygame
import sys
import random
import math

pygame.init()

width, height, depth = 1280, 720, 5000
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Sound of Silence - Sonification")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

sound0 = pygame.mixer.Sound("sound/nasa1.mp3")
sound1 = pygame.mixer.Sound("sound/C8.mp3")
sound2 = pygame.mixer.Sound("sound/D8.mp3")
sound3 = pygame.mixer.Sound("sound/F8.mp3")
sound4 = pygame.mixer.Sound("sound/G8.mp3")
sound5 = pygame.mixer.Sound("sound/A8.mp3")
sound6 = pygame.mixer.Sound("sound/C9.mp3")
redsound1 = pygame.mixer.Sound("sound/nasa2.mp3")
redsound2 = pygame.mixer.Sound("sound/nasa3.mp3")
redsound3 = pygame.mixer.Sound("sound/nasa4.mp3")
redsound4 = pygame.mixer.Sound("sound/nasa5.mp3")

pygame.mixer.init()
pygame.mixer.set_num_channels(500)

stars = []

# Projection constant.
proj = 50

def angleToSound(a):
    p = math.pi / 5
    if a < -4*p:
        return sound3
    elif a < -3*p:
        return sound2
    elif a < -2*p:
        return sound1
    elif a < -1*p:
        return sound2
    elif a < 0*p:
        return sound3
    elif a < 1*p:
        return sound4
    elif a < 2*p:
        return sound5
    elif a < 3*p:
        return sound6
    elif a < 4*p:
        return sound5
    else:
        return sound4

def angleToLeft(a):
    if a < 0:
        return -a/math.pi
    else:
        return a/math.pi

class Star:
    def __init__(self, red=False, sound=None, channel=0):
        self.x = random.randint(0, width)
        self.y = random.randint(0, height)
        self.z = random.randint(0, 0.2*depth)
        self.s = random.randint(0, 5)
        self.w = 30 + random.randint(0, 70)
        self.channel = channel
        a = math.atan2(height/2-self.y, width/2-self.x)
        self.left = angleToLeft(a)
        self.right = 1 - self.left
        if sound is None:
            self.sound = angleToSound(a)
        else:
            self.sound = sound
        if (red):
            self.s = 50
            self.w = 100
        self.red = red
    
    def __lt__(self, other):
        return self.z < other.z
    
    def draw(self, z):
        dx = width/2 - self.x
        dy = height/2 - self.y
        soundPower = 0
        if ((self.z - z)*(self.z - z) < 20000):
            soundPower = 1 - (self.z - z)*(self.z - z) / 20000
        if ((z == 0) and self.red):
            pygame.mixer.Channel(self.channel).play(self.sound)
        if ((self.z - z == proj) and not self.red):
            soundPower = 1 - (dx*dx+dy*dy) / (width*width/4 + height*height/4)
            pygame.mixer.Channel(self.channel).play(self.sound)
            pygame.mixer.Channel(self.channel).set_volume(0.05*soundPower*self.left, 0.05*soundPower*self.right)
        if (self.red):
            pygame.mixer.Channel(self.channel).set_volume(0.3*soundPower*self.left, 0.3*soundPower*self.right)
        if (z >= self.z):
            return
        d2 = dx*dx + dy*dy + (self.z - z)*(self.z - z)
        dx = proj*dx / (self.z - z)
        dy = proj*dy / (self.z - z)
        x = width/2 + dx
        y = height/2 + dy
        s = proj*self.s / (self.z - z)
        light = (self.w / 100) * (1 - d2 / (width*width + height*height + 0.04*depth*depth))
        c = 255 * light
        if (self.red):
            pygame.draw.circle(screen, (c,0,0), (x, y), s)
        elif (self.z - z < proj/2):
            pygame.draw.circle(screen, (0,0,c), (x, y), s)
        else:
            pygame.draw.circle(screen, (c,c,c), (x, y), s)

# Star generator.
def generate_stars(num_stars):
    stars.append(Star(red=True,sound=redsound1,channel=1))
    stars.append(Star(red=True,sound=redsound2,channel=2))
    stars.append(Star(red=True,sound=redsound3,channel=3))
    stars.append(Star(red=True,sound=redsound4,channel=4))
    for i in range(num_stars):
        stars.append(Star(channel=i+5))

# 300 standard stars and 4 red giants. 
generate_stars(300)
stars.sort()

running = True
clock = pygame.time.Clock()

z = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    for star in stars:
       star.draw(z)

    pygame.display.flip()

    z += 1

    clock.tick(30)

pygame.quit()
sys.exit()
