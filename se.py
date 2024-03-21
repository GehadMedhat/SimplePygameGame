import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FRUIT_SIZE = 30
BASKET_SIZE = 100

# Load Background Image
background = pygame.image.load('background.jpg') 
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Create the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Winnie the Pooh Honey Harvest')


# Clock for controlling the FPS
clock = pygame.time.Clock()

# Load images
player_img = pygame.image.load('player.png')  
honey_img = pygame.image.load('honey.png')  

# Scale the images to desired dimensions
player_img = pygame.transform.scale(player_img, (BASKET_SIZE, BASKET_SIZE))
honey_img = pygame.transform.scale(honey_img, (FRUIT_SIZE, FRUIT_SIZE))

# Font for displaying score
font = pygame.font.Font(None, 36)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50)
        self.speed = 8

    def update(self):
        keys = pygame.key.get_pressed()
        self.rect.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * self.speed
        self.rect.x = max(min(self.rect.x, WIDTH - BASKET_SIZE), 0)

# Modify the Honey class
class Honey(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = honey_img
        self.image = pygame.transform.scale(honey_img, (40, 40))  # Change size of honey image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - FRUIT_SIZE)
        self.rect.y = random.randint(-200, -FRUIT_SIZE)  # Adjust starting position
        self.speed = random.randint(1, 2)  # Reduce falling speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - FRUIT_SIZE)
            self.rect.y = random.randint(-200, -FRUIT_SIZE)  # Adjust respawn position
            self.speed = random.randint(1, 2)  # Change falling speed


# Sprite groups
all_sprites = pygame.sprite.Group()
honey_list = pygame.sprite.Group()

# Add basket to sprite group
basket = Player()
all_sprites.add(basket)

# Game variables
score = 0

# Game loop
running = True
while running:
    # Keep loop running at the right speed
    clock.tick(FPS)

    # Process input/events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    # Create new honey occasionally
    if random.randint(1, 10) == 1:
        new_honey = Honey()
        all_sprites.add(new_honey)
        honey_list.add(new_honey)

    # Check for collisions between basket and honey
    caught_honey = pygame.sprite.spritecollide(basket, honey_list, True)
    score += len(caught_honey)

    # Render/Clear
    screen.blit(background, (0, 0))  # Draw the background image

    all_sprites.draw(screen)

    # Display score on the screen
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()
