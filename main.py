#Import pygame module
import pygame

# Import random for random numbers
import random
# Import pygame.locals for easier access to key coordinates

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_s
)

# Define constatnts for the screen width and height
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# Define a player object by extending pygame.sprite.Sprite
# Use an image for a better looking sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("assets/jet.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

# Move the sprite pased on user keypress
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)   

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0     
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH     
        if self.rect.top <= 0:
            self.rect.top = 0     
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# Define enemy object by extending pygame.sprite.Sprite
# Use an image for the sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("assets/missile.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen 
    # Increase score by 10 for each enemy that leaves the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            scoreboard.increase(10)
            self.kill()

# Define the cloud object by extending pygame.sprite.Sprite
# Use an image for the sprite
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("assets/cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting process is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
    # Move the cloud based on a constant speed
    # Remove the cloud when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

# Create a scoreboard class to keep track of score
class Scoreboard:
    def __init__(self, screen):
        self.screen = screen
        self.score = 0
        self.font = pygame.font.SysFont('Arial', 28)
        # Initialize high score
        try:
            high_score_file = open("game_data.txt", "r")
            high_score_str = high_score_file.read()
            self.high_score = int(high_score_str)
            high_score_file.close()
        except FileNotFoundError:
            self.high_score = 0
        except ValueError:
            self.high_score = 0
    # Draws the scoreboard on the screen
    def draw(self):
        score_text = f"Score: {self.score}"
        highscore_text = f"High Score: {self.high_score}"
        score_surf = self.font.render(score_text, True, (255, 255, 255))
        highscore_surf = self.font.render(highscore_text, True, (255, 255, 255))
        self.screen.blit(score_surf, (10, SCREEN_HEIGHT - 80))
        self.screen.blit(highscore_surf, (10, SCREEN_HEIGHT - 40))

        # Check current score to high score
        if self.score > self.high_score:
            self.high_score = self.score

    # Increases the score when called
    def increase(self, points):
        self.score += points

# Setup for sounds.  Defaults are good
pygame.mixer.init() 

#Initialize pygame
pygame.init()

# Create the screen object

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Create scoreboard
scoreboard = Scoreboard(screen)


# Load and play background music
# Sound source: http://ccmixter.org/files/Apoxode/59262
# License: https://creativecommons.org/licenses/by/3.0/
pygame.mixer.music.load("assets/Apoxode_-_Electric_1.mp3")
pygame.mixer.music.play(loops=-1)

# Load all sound files
# Sound source: Jon Fincher
move_up_sound = pygame.mixer.Sound("assets/Rising_putter.ogg")
move_down_sound = pygame.mixer.Sound("assets/Falling_putter.ogg")
collision_sound = pygame.mixer.Sound("assets/Collision.ogg")
# Game loop
def game_loop():
    running = True
    # Create a custom event for adding a new enemy + clouds
    ADDENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDENEMY, 250)
    ADDCLOUD = pygame.USEREVENT + 2
    pygame.time.set_timer(ADDCLOUD, 1000)

    # Setup the clock for a decent framerate
    clock = pygame.time.Clock()

    # Instantiate a player. Right now, this is just a rectangle
    player = Player()

    # Create groups to hold enemy sprites and all sprites
    # - enemies is used for collision detection and position updates
    # - all_sprites is used for rendering
    enemies = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    

    while running:

        # Look at every event in the queue
        for event in pygame.event.get():
            # Did the user hit a key?
            if event.type == KEYDOWN:
                # Was it the Escape key? If so, stop the loop.
                if event.key == K_ESCAPE:
                    running = False
                    menu_active = True
            # Did the user click the window close button? If so stop the loop.
            elif event.type == QUIT:
                running = False

            # Add a new enemy?
            elif event.type == ADDENEMY:
                # Create the new enemy and add it to sprite groups
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)

            # Add a new cloud
            elif event.type == ADDCLOUD:
                # Create a new cloud and add it to groups
                new_cloud = Cloud()
                clouds.add(new_cloud)
                all_sprites.add(new_cloud)
                
        # Get the set of keys pressed and check for user input
        pressed_keys = pygame.key.get_pressed()

        # Update the player sprite based on user keypress
        player.update(pressed_keys)

        # Update enemy position
        enemies.update()
        clouds.update()
        

        # Fill the screen with blue sky
        screen.fill((135, 206, 250))

        # Draw scoreboard
        scoreboard.draw()

        # Draw all sprites
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        # Check if any enemies have collided with the player
        if pygame.sprite.spritecollideany(player, enemies):
            # Check if there is a new high score, if so save to file
            if scoreboard.score >= scoreboard.high_score:
                high_score_file = open("game_data.txt", "w")
                high_score_str = str(scoreboard.score)
                high_score_file.write(high_score_str)
                high_score_file.close()
            # set current score back to 0
            scoreboard.score = 0
            # then remove player and stop loop
            player.kill()

            # Stop any moving sounds and play the collision sound
            move_down_sound.stop()
            move_up_sound.stop()
            collision_sound.play()

            # Stop the loop
            running = False
            # Run the menu
            menu_loop()
        
        pygame.display.flip()

        # Ensure the program maintains a rate of 30 frames per second
        clock.tick(30)
# Menu loop
def menu_loop():
    # Load the current high score
    current_high_score = 0
    try:
        high_score_file = open("game_data.txt", "r")
        high_score_str = high_score_file.read()
        current_high_score = int(high_score_str)
        high_score_file.close()
    except FileNotFoundError:
        current_high_score = 0
    except ValueError:
        current_high_score = 0
    #Variable for the menu loop
    menu_active =True
    while menu_active:
        
        # Fill screen with black
        screen.fill((0,0,0))

        # Draw title text
        title_font = pygame.font.SysFont(None, 84)
        title_text = title_font.render("MISSILE MAX", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/4))
        screen.blit(title_text, title_rect)

        # Draw other menu text
        menu_font = pygame.font.SysFont(None, 48) 
        menu_text = menu_font.render("PRESS 'S' TO START OR 'ESC' TO QUIT", True, (255,255,255))
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        screen.blit(menu_text, menu_rect)

        # Draw the high score text
        score_font = pygame.font.SysFont(None, 36)
        score_text = score_font.render(f"CURRENT HIGH SCORE: {current_high_score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH/2, (SCREEN_HEIGHT*(3/4))))
        screen.blit(score_text, score_rect)


        #Check for keypresses
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    menu_active = False
                elif event.key == K_s:
                    menu_active = False
                    game_loop()
            # Did the user click the window close button? If so stop the loop.
            elif event.type == QUIT:
                menu_active = False

        pygame.display.flip()

menu_loop()

# All done! Stop and quit the mixer.
pygame.mixer.music.stop()
pygame.mixer.quit()