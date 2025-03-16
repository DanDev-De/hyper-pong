
import pygame
import pygame.gfxdraw
import sys
import random
import os
import imageio.v3 as iio
from PIL import Image
import numpy as np

# Initialize Pygame
pygame.init()
pygame.font.init()
if not pygame.font.get_init():
    print("Font initialization failed!")
    sys.exit(1)

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

def main():
    try:
        # Create window
        print("Creating display window...")
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Bear Animation Debug")
        clock = pygame.time.Clock()

        # Load single test GIF
        print("
Attempting to load GIF...")
        gif_path = os.path.join("assets", "images", "bears", "bear1.gif")
        if os.path.exists(gif_path):
            print(f"Found GIF at: {gif_path}")
            try:
                gif = iio.imread(gif_path)
                print(f"GIF loaded. Shape: {gif.shape}")
                
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
                
                print(f"Successfully loaded {len(frames)} frames")
                
                # Main loop
                running = True
                current_frame = 0
                last_update = pygame.time.get_ticks()
                while running:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                running = False
                    
                    # Update frame
                    current_time = pygame.time.get_ticks()
                    if current_time - last_update > 100:  # 100ms between frames
                        current_frame = (current_frame + 1) % len(frames)
                        last_update = current_time
                    
                    # Draw
                    screen.fill((10, 10, 25))
                    screen.blit(frames[current_frame], (SCREEN_WIDTH//2 - 64, SCREEN_HEIGHT//2 - 64))
                    pygame.display.flip()
                    clock.tick(FPS)
                
            except Exception as e:
                print(f"Error processing GIF: {str(e)}")
                import traceback
                traceback.print_exc()
        else:
            print(f"GIF not found at: {gif_path}")
    
    except Exception as e:
        print(f"Error in main: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()

