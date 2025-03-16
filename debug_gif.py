import os
import imageio.v3 as iio
from PIL import Image
import pygame
import sys

# Initialize Pygame
pygame.init()
print("Pygame initialized")

# Create window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("GIF Test")
clock = pygame.time.Clock()

# Try to load GIF
gif_path = os.path.join("assets", "images", "bears", "bear1.gif")
print(f"Looking for GIF at: {gif_path}")

if os.path.exists(gif_path):
    print("Found GIF file")
    try:
        # Load the GIF
        gif = iio.imread(gif_path)
        print(f"GIF loaded, shape: {gif.shape}")
        
        # Convert frames
        frames = []
        for i, frame in enumerate(gif):
            pil_image = Image.fromarray(frame)
            pil_image = pil_image.resize((128, 128))
            mode = pil_image.mode
            size = pil_image.size
            data = pil_image.tobytes()
            pygame_frame = pygame.image.fromstring(data, size, mode).convert_alpha()
            frames.append(pygame_frame)
            print(f"Processed frame {i+1}")
        
        print(f"Total frames: {len(frames)}")
        
        # Display animation
        current_frame = 0
        last_update = pygame.time.get_ticks()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            current_time = pygame.time.get_ticks()
            if current_time - last_update > 100:  # 100ms between frames
                current_frame = (current_frame + 1) % len(frames)
                last_update = current_time
            
            screen.fill((10, 10, 25))
            screen.blit(frames[current_frame], (336, 236))  # Center on screen
            pygame.display.flip()
            clock.tick(60)
        
    except Exception as e:
        print(f"Error processing GIF: {e}")
        import traceback
        traceback.print_exc()
else:
    print("GIF file not found!")

pygame.quit()
sys.exit()

