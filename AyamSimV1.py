# Pygame sprite Example
import pygame
import random
import os

ASSET_FOLDER = os.path.join(os.getcwd(), 'newchicken')

WIDTH = 600
HEIGHT = 600
FPS = 30

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Player(pygame.sprite.Sprite):
    # sprite for the Player
    def __init__(self):
        # this line is required to properly create the sprite
        pygame.sprite.Sprite.__init__(self)
        # create a plain rectangle for the sprite image

        SPRITE_SIZE = (80, 80)
        self.rw = pygame.transform.scale(
            pygame.image.load(os.path.join(
                ASSET_FOLDER ,
                'ayamidle1.png')).convert_alpha(), SPRITE_SIZE)
        
        self.lw = pygame.transform.scale(
            pygame.image.load(os.path.join(
                ASSET_FOLDER ,
                'ayamidle2kiri.png')).convert_alpha(), SPRITE_SIZE)
        
        self.rj = pygame.transform.scale(
            pygame.image.load(os.path.join(
                ASSET_FOLDER ,
                'ayamjump1.png')).convert_alpha(), SPRITE_SIZE)
        
        self.lj = pygame.transform.scale(
            pygame.image.load(os.path.join(
                ASSET_FOLDER ,
                'ayamjump2kiri.png')).convert_alpha(), SPRITE_SIZE)


        self.image = self.rw 
        self.facing = "right"
        self.last_key = None

 

        # find the rectangle that encloses the image
        self.rect = self.image.get_rect()
        # center the sprite on the screen
        self.rect.center = (WIDTH / 2, HEIGHT)
        self.speed = 0

        
        

    def update(self):
        self.speedx = 0
        self.speedy = 0
        self.gravity = 18
        self.jump_power = -30
        

        self.fall_speed_limit = 100  # Max falling speed
        self.acceleration = 0.5   # For smooth horizontal movement
        self.friction = 0.1       # For gradual stop

        keystate = pygame.key.get_pressed()

        
        if keystate[pygame.K_LEFT]:
            self.speedx = -8

            self.facing = "left"
            self.last_key = "left"

            if self.rect.bottom >= HEIGHT:
                self.image = self.lw
            else:
                self.image = self.lj

            self.image = self.lw if self.rect.bottom >= HEIGHT else self.lj
            


        if keystate[pygame.K_RIGHT]:
            self.speedx = 8

            self.facing = "right"
            self.last_key = "right"

            if self.rect.bottom >= HEIGHT:  
                self.image = self.rw  # Walking
            else:
                self.image = self.rj  # Jumping

            self.image = self.rw if self.rect.bottom >= HEIGHT else self.rj


        if self.rect.bottom >= HEIGHT and self.speedx == 0:
            self.image = self.rw if self.facing == "right" else self.lw

    
        if keystate[pygame.K_LEFT] and keystate[pygame.K_RIGHT]:
             if self.last_key == "left":
              self.speedx = 0

             elif self.last_key == "right":
              self.speedx = 0
       
        
            


        self.rect.x += self.speedx

        if keystate[pygame.K_UP] :
            self.speedy = self.jump_power

            self.image = self.rj if self.facing == "right" else self.lj


        self.speedy += self.gravity


        # Allow controlled jump height by releasing the key
        if not keystate[pygame.K_UP] and self.speedy < 0:
            self.speedy *= 0.  # Cuts upward speed for softer jumps

            if self.rw:
                self.image = self.rj
            
            if self.lw:
                self.image = self.lj


        # Limit falling speed for better control
        self.speedy = min(self.speedy, self.fall_speed_limit)
        
        self.rect.y += self.speedy

        

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        
        if self.rect.top < 0:
            self.rect.top = 0
        
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kandang Ayam Simulator")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    # Draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()