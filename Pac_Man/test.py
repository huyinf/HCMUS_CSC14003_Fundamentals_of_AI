import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Image Position Example")

# Load your image
image = pygame.image.load("images/wall.png")

# Get the rect (position and size) of the image
image_rect = image.get_rect()

print(image_rect)
# Set the initial position of the image
image_rect.x = 0
image_rect.y = 0

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((0, 0, 0))

    # Blit (draw) the image onto the screen
    screen.blit(image, image_rect)

    # Update the display
    pygame.display.update()

pygame.quit()
sys.exit()
