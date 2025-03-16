import pygame
import pygame.gfxdraw
import sys
import random
import os
import imageio.v3 as iio
from PIL import Image
import numpy as np

# Initialize Pygame and font
pygame.init()
pygame.font.init()
if not pygame.font.get_init():
    print("Font initialization failed!")
    sys.exit(1)

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Create window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Animated Bears Test")
clock = pygame.time.Clock()

class BouncingBear:
    def __init__(self):
        self.bears = []
        self.colors = [
            (255, 150, 150),  # Salmon pink
            (150, 200, 255),  # Sky blue
            (255, 200, 150),  # Peach
            (200, 255, 150),  # Lime
            (255, 150, 255)   # Light purple
        ]
        self.animations = self.load_animations()
        for _ in range(6):
            self.add_bear()

    def load_animations(self):
        animations = []
        gif_files = ['bear1.gif', 'bear2.gif', 'bear3.gif']
        
        for gif_file in gif_files:
            gif_path = os.path.join('assets', 'images', 'bears', gif_file)
            if os.path.exists(gif_path):
                frames = []
                try:
                    gif = iio.imread(gif_path)
                    if len(gif.shape) == 3:
                        # Single frame
                        pil_image = Image.fromarray(gif)
                        pil_image = pil_image.resize((64, 64))
                        mode = pil_image.mode
                        size = pil_image.size
                        data = pil_image.tobytes()
                        frames.append(pygame.image.fromstring(data, size, mode).convert_alpha())
                    else:
                        # Multiple frames
                        for frame in gif:
                            pil_image = Image.fromarray(frame)
                            pil_image = pil_image.resize((64, 64))
                            mode = pil_image.mode
                            size = pil_image.size
                            data = pil_image.tobytes()
                            frames.append(pygame.image.fromstring(data, size, mode).convert_alpha())
                    if frames:
                        animations.append(frames)
                except Exception as e:
                    print(f"Error loading {gif_file}: {e}")
        return animations

    def add_bear(self):
        if not self.animations:
            return
            
        animation = random.choice(self.animations)
        bear = {
            'x': random.randint(0, SCREEN_WIDTH),
            'y': random.randint(0, SCREEN_HEIGHT),
            'dx': random.uniform(-2, 2),
            'dy': random.uniform(-2, 2),
            'frames': animation,
            'current_frame': 0,
            'animation_speed': random.uniform(0.1, 0.3),
            'last_update': pygame.time.get_ticks(),
            'size': random.randint(40, 60),
            'color': random.choice(self.colors),
            'rotation': 0,
            'rotation_speed': random.uniform(-2, 2)
        }
        self.bears.append(bear)

    def update(self):
        current_time = pygame.time.get_ticks()
        
        for bear in self.bears:
            # Update position
            bear['x'] += bear['dx']
            bear['y'] += bear['dy']
            
            # Bounce off walls
            if bear['x'] < 0 or bear['x'] > SCREEN_WIDTH:
                bear['dx'] *= -1
            if bear['y'] < 0 or bear['y'] > SCREEN_HEIGHT:
                bear['dy'] *= -1
            
            # Update animation frame
            if current_time - bear['last_update'] > bear['animation_speed'] * 1000:
                bear['current_frame'] = (bear['current_frame'] + 1) % len(bear['frames'])
                bear['last_update'] = current_time
            
            # Update rotation
            bear['rotation'] += bear['rotation_speed']

    def draw(self, screen):
        for bear in self.bears:
            if not bear['frames']:
                continue
            # Get current frame
            frame = bear['frames'][bear['current_frame']]
            
            # Scale the frame
            scaled = pygame.transform.scale(frame, (bear['size'], bear['size']))
            
            # Color tint the frame
            colored = scaled.copy()
            colored.fill(bear['color'], special_flags=pygame.BLEND_RGBA_MULT)
            
            # Rotate
            rotated = pygame.transform.rotate(colored, bear['rotation'])
            
            # Get position accounting for rotation
            rect = rotated.get_rect()
            rect.center = (bear['x'], bear['y'])
            
            # Draw
            screen.blit(rotated, rect)

def main():
    # Create bouncing bears
    bears = BouncingBear()

    # Main game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Update
        bears.update()

        # Draw
        screen.fill((10, 10, 25))  # Dark background
        bears.draw(screen)
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

