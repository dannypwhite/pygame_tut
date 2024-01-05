#Import pygame module
import pygame

# Import pygame.locals for easier access to key coordinates

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Define constatnts for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()

# Move the sprite pased on user keypress
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)        

#Initialize pygame
pygame.init()

# Create the screen object

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Instantiate a player. Right now, this is just a rectangle
player = Player()

# Variable to keep main loop running
running = True

# Main loop
while running:
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False
        # Did the user click the window close button? If so stop the loop.
        elif event.type == QUIT:
            running = False
    # Get the set of keys pressed and ckeck for user input
    pressed_keys = pygame.key.get_pressed()

    # Update the player sprite based on user keypress
    player.update(pressed_keys)
    

    # Fill the screen with black
    screen.fill((0, 0, 0))
    # Draw the player on the screen
    screen.blit(player.surf, player.rect)

    
    pygame.display.flip()