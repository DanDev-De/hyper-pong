import pygame
import sys

pygame.init()
pygame.display.init()

# Create a window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pygame Test")

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill screen with a color
    screen.fill((50, 50, 100))
    
    # Draw a test circle
    pygame.draw.circle(screen, (255, 255, 255), (400, 300), 50)
    
    pygame.display.flip()
    
pygame.quit()

