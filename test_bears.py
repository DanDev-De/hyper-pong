import pygame
import imageio.v3 as iio
from PIL import Image
import numpy as np
import os

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

def load_gif_frames(gif_path):
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
        print(f"Successfully loaded {len(frames)} frames from {gif_path}")
    except Exception as e:
        print(f"Error loading {gif_path}: {e}")
    return frames

# Load GIFs
gif_files = ['bear1.gif', 'bear2.gif', 'bear3.gif']
animations = []
for gif_file in gif_files:
    gif_path = os.path.join('assets', 'images', 'bears', gif_file)
    if os.path.exists(gif_path):
        frames = load_gif_frames(gif_path)
        if frames:
            animations.append(frames)

if not animations:
    print("No animations loaded!")
    pygame.quit()
    exit()

# Main loop
running = True
current_frame = 0
last_update = pygame.time.get_ticks()
animation_speed = 100  # milliseconds between frames

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    current_time = pygame.time.get_ticks()
    if current_time - last_update > animation_speed:
        current_frame = (current_frame + 1) % len(animations[0])
        last_update = current_time

    screen.fill((0, 0, 0))

    # Draw all animations
    x_offset = 100
    for animation in animations:
        if current_frame < len(animation):
            frame = animation[current_frame]
            scaled = pygame.transform.scale(frame, (128, 128))
            screen.blit(scaled, (x_offset, 250))
            x_offset += 200

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

