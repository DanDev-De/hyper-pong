import pygame
import os
import imageio.v3 as iio
from PIL import Image
import sys

print("Initializing...")
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

def load_gif_frames(gif_path):
    print(f"Loading GIF: {gif_path}")
    frames = []
    try:
        gif = iio.imread(gif_path)
        print(f"GIF loaded with shape: {gif.shape}")
        for i, frame in enumerate(gif):
            pil_image = Image.fromarray(frame)
            pil_image = pil_image.resize((128, 128))
            mode = pil_image.mode
            size = pil_image.size
            data = pil_image.tobytes()
            frames.append(pygame.image.fromstring(data, size, mode).convert_alpha())
            if i % 10 == 0:
                print(f"Processed frame {i+1}")
        print(f"Successfully loaded {len(frames)} frames")
        return frames
    except Exception as e:
        print(f"Error loading GIF: {e}")
        return None

def main():
    try:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Bear Animation Test")
        clock = pygame.time.Clock()

        # Load the GIF
        gif_path = os.path.join("assets", "images", "bears", "bear1.gif")
        frames = load_gif_frames(gif_path)
        
        if not frames:
            print("Failed to load frames")
            return

        # Animation variables
        x = SCREEN_WIDTH // 2
        y = SCREEN_HEIGHT // 2
        dx = 2
        dy = 2
        current_frame = 0
        last_update = pygame.time.get_ticks()
        frame_duration = 50  # milliseconds

        running = True
        while running:
            current_time = pygame.time.get_ticks()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

            # Update position
            x += dx
            y += dy
            if x < 0 or x > SCREEN_WIDTH:
                dx *= -1
            if y < 0 or y > SCREEN_HEIGHT:
                dy *= -1

            # Update animation frame
            if current_time - last_update > frame_duration:
                current_frame = (current_frame + 1) % len(frames)
                last_update = current_time
                print(f"Frame: {current_frame}/{len(frames)-1}")

            # Draw
            screen.fill((10, 10, 25))
            frame = frames[current_frame]
            rect = frame.get_rect()
            rect.center = (int(x), int(y))
            screen.blit(frame, rect)
            pygame.display.flip()
            clock.tick(60)

    except Exception as e:
        print(f"Error in main: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
