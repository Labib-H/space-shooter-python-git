# Arcade-style space shooter inspired by Galaga and Spacer Invaders.
# Made for the purpose of teaching git version control to beginners.

import pygame as pg



### Setup ###
pg.init()
clock = pg.time.Clock()

screen = pg.display.set_mode((400,600))
pg.display.set_caption("Space Shooter")

# Spaceship character
ship_images = []
for i in range(3):
    img = pg.image.load(f"images/ship_{i}.png")
    ship_images.append(img)
ship_x = 200 
ship_y = 500
ship_w = ship_images[0].get_rect().size[0]
ship_h = ship_images[0].get_rect().size[1]

# Alien character
alien_images = []
for i in range(2):
    img = pg.image.load(f"images/alien_{i}.png")
    alien_images.append(img)

aliens = []
for i in range(5):
    alien1 = {'x': 50*i + 50 , 'y': 0}
    alien2 = {'x': 50*i + 50, 'y': 50}
    aliens.append(alien1)
    aliens.append(alien2)

alien_w = alien_images[0].get_rect().size[0]
alien_h = alien_images[0].get_rect().size[1]

# Projectiles 
projectile_fired = False
projectiles = []
projectile_w = 4 
projectile_h = 8

# Keypress status
left_pressed = False
right_pressed = False

# Sound: weapon / laser 
# https://sfxr.me/#34T6Pm25W5VunHtL14gUxhLx6MqNduzaeRPcUbqtT4RN55w6nP9NipaUrx5ZBBvohWwXgMrd5BS2e7HwRwEVyzmKM3FV8LiU7Gh5ob2VvvMi6ftqdhbVB54ZM 
sound_laser = pg.mixer.Sound("sounds/cannon-shot-14799.mp3")

# Font for scoreboard
# https://fonts.google.com/specimen/Press+Start+2P/about
font_scoreboard = pg.font.Font("fonts/PressStart2P-Regular.ttf", 20)
class Aliens:

    def __init__(self, x, y, speed, img):
        self.aliens = []
        self.x = x
        self.y = y
        self.speed = speed
        self.img = img


def wave_fill(list,n):
    for i in range(n):
        list.append(Aliens(x=50+i*50,y=100,speed=3))

def showListInfo(list):
        for element in list:
            print(f"(x = {element.x} , y = {element.y})")

            
class Alienwaves:
    def __init__(self,n):
            self.list = self.__createWave(n) 

    def __createWave(self,n):
        list = []
        for i in range(n):
            list.append(Aliens(x=50+i*50,y=100,speed=3))
        return list
    
    def move(self):
        for element in self.list:
            element.move()
    
    def showInfo(self):
        for element in self.list:
            print(f"(x = {element.x} , y = {element.y})")

### Game loop ###
running = True
tick = 0
score = 0
kills = 0
while running:

    ## Event loop  (handle keypresses etc.) ##
    events = pg.event.get()
    for event in events:

        # Close window (pressing [x], Alt+F4 etc.)
        if event.type == pg.QUIT:
            running = False
        
        # Keypresses
        elif event.type == pg.KEYDOWN:

            if event.key == pg.K_ESCAPE:
                running = False

            elif event.key == pg.K_LEFT:
                left_pressed = True

            elif event.key == pg.K_RIGHT:
                right_pressed = True

            elif event.key == pg.K_SPACE:
                projectile_fired = True

        # Keyreleases
        elif event.type == pg.KEYUP:

            if event.key == pg.K_LEFT:
                left_pressed = False 

            elif event.key == pg.K_RIGHT:
                right_pressed = False 


    ## Updating (movement, collisions, etc.) ##

    # Alien
    for alien in aliens:
        alien['y'] += 1


    # Spaceship
    if left_pressed:
        ship_x -= 8

    if right_pressed:
        ship_x += 8

    # Projectile movement
    # Reverse iteration needed to handle each projectile correctly
    # in cases where a projectile is removed.
    for projectile in reversed(projectiles):
        projectile['y'] -= 8 

        # Remove projectiles leavning the top of the screen
        if projectile['y'] < 0:
            projectiles.remove(projectile)

    # Alien / projectile collision 
    # Test each projectile against each alien
    for projectile in reversed(projectiles):
        for alien in aliens:

            # Horizontal (x) overlap
            if (alien['x'] < projectile['x'] + projectile_w and 
                projectile['x'] < alien['x']+alien_w):
                
                # Vertical (y) overlap 
                if (projectile['y'] < alien['y'] + alien_h and 
                    alien['y'] < projectile['y'] + projectile_h):

                    # Alien is hit
                    kills = kills + 1
                    projectiles.remove(projectile)
                    aliens.remove(alien)
                    #alien['y'] = -10

                    score=score+10


                    # No further aliens can be hit by this projectile 
                    # so skip to the next projectile 
                    break 

    # Firing (spawning new projectiles)
    if projectile_fired:
        sound_laser.play()

        projectile = {'x': ship_x + ship_w/2 - projectile_w/2, 
                      'y': ship_y}
        projectiles.append(projectile)
        projectile_fired = False


    ## Drawing ##
    screen.fill((0,0,0)) 

    # 3 images --> tick % 3
    # 100% animation speed: tick % 3
    # 25% animation speed: int(tick/4) % 3
    r = int(tick/4) % 3 
    screen.blit(ship_images[r], (ship_x, ship_y))

    # Alien
    r = int(tick/8) % 2
    for alien in aliens:
        screen.blit(alien_images[r], (alien['x'], alien['y']))

    # Projectiles
    for projectile in projectiles:
        rect = (projectile['x'], projectile['y'], projectile_w, projectile_h)
        pg.draw.rect(screen, (255, 0, 0), rect) 

   

    # Scoreboard
    text = font_scoreboard.render(f"{score:04d}", True, (255,255,255))
    screen.blit(text, (10,560))

    # Update window with newly drawn pixels
    pg.display.flip()

    # Limit/fix frame rate (fps)
    clock.tick(50)
    tick += 1