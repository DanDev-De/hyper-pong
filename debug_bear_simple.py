
import pygame
import pygame.gfxdraw
from pygame import mixer
import sys
import random
import math
import os
import imageio.v3 as iio
from PIL import Image
import numpy as np
from enum import Enum

# Debug helper
def debug_print(msg):
    print(f"DEBUG: {msg}")

# Initialize pygame and its modules
debug_print("Starting initialization...")
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

class BouncingBear:
    def __init__(self):
        debug_print("Initializing BouncingBear...")
        self.bears = []
        self.colors = [(255, 150, 150)]  # Just one color for testing
        self.animations = self.load_animations()
        if self.animations:
            debug_print(f"Loaded {len(self.animations)} animations")
            self.add_bear()  # Just add one bear for testing
        else:
            debug_print("No animations loaded")

    def load_animations(self):
        debug_print("Loading animations...")
        animations = []
        gif_files = ["bear1.gif"]  # Just try one file for testing
        
        for gif_file in gif_files:
            gif_path = os.path.join("assets", "images", "bears", gif_file)
            debug_print(f"Trying to load: {gif_path}")
            if os.path.exists(gif_path):
                debug_print(f"Found file: {gif_path}")
                try:
                    gif = iio.imread(gif_path)
                    debug_print(f"GIF loaded with shape: {gif.shape}")
                    frames = []
                    for i, frame in enumerate(gif):
                        pil_image = Image.fromarray(frame)
                        pil_image = pil_image.resize((64, 64))
                        mode = pil_image.mode
                        size = pil_image.size
                        data = pil_image.tobytes()
                        frames.append(pygame.image.fromstring(data, size, mode).convert_alpha())
                        if i % 10 == 0:
                            debug_print(f"Processed {i+1} frames")
                    if frames:
                        animations.append(frames)
                        debug_print(f"Successfully added animation with {len(frames)} frames")
                except Exception as e:
                    debug_print(f"Error loading {gif_file}: {str(e)}")
            else:
                debug_print(f"File not found: {gif_path}")
        return animations

    def add_bear(self):
        if not self.animations:
            debug_print("No animations available to add bear")
                                            # Make the bear larger (128x128 instead of 64x64)
                                            pil_image = pil_image.resize((128, 128))
                                            debug_print(f"Resized frame {i+1} to 128x128")
        animation = self.animations[0]  # Just use the first animation for testing
        bear = {
            "x": SCREEN_WIDTH // 2,
            "y": SCREEN_HEIGHT // 2,
            "dx": 1,
            "dy": 1,
            "frames": animation,
            "current_frame": 0,
            "animation_speed": 0.1,
            "last_update": pygame.time.get_ticks(),
            "size": 64,
            "color": self.colors[0],
            "rotation": 0,
            "rotation_speed": 1
        }
        self.bears.append(bear)
        debug_print("Bear added successfully")

    def update(self):
        current_time = pygame.time.get_ticks()
        for bear in self.bears:
            bear["x"] += bear["dx"]
            bear["y"] += bear["dy"]
            
            if bear["x"] < 0 or bear["x"] > SCREEN_WIDTH:
                bear["dx"] *= -1
                                "animation_speed": 0.05,  # Faster animation
                                "last_update": pygame.time.get_ticks(),
                                "debug_last_frame_update": pygame.time.get_ticks(),  # For debugging
                                "frame_changes": 0  # Count frame changes for debugging
            if current_time - bear["last_update"] > bear["animation_speed"] * 1000:
                bear["current_frame"] = (bear["current_frame"] + 1) % len(bear["frames"])
                bear["last_update"] = current_time

    def draw(self, screen):
        for bear in self.bears:
            if not bear["frames"]:
                continue
            try:
                frame = bear["frames"][bear["current_frame"]]
                rect = frame.get_rect()
                rect.center = (bear["x"], bear["y"])
                screen.blit(frame, rect)
            except Exception as e:
                debug_print(f"Error drawing bear: {str(e)}")

def main():
    debug_print("Starting main...")
    try:
                                    # Update frame change counter
                                    bear["frame_changes"] += 1
                                    
                                    # Debug frame updates
                                    if current_time - bear["debug_last_frame_update"] >= 1000:  # Once per second
                                        debug_print(f"Frame updated: {old_frame} -> {bear['current_frame']} (total changes: {bear['frame_changes']})")
                                        debug_print(f"Animation speed: {bear['animation_speed']*1000}ms, position: ({int(bear['x'])}, {int(bear['y'])})")
                                        bear["debug_last_frame_update"] = current_time
        debug_print("Creating BouncingBear...")
        bears = BouncingBear()
        debug_print("BouncingBear created")

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                                    rect = frame.get_rect()
                                    rect.center = (int(bear["x"]), int(bear["y"]))
                                    screen.blit(frame, rect)
                                    # Draw bounding box for debugging
                                    pygame.draw.rect(screen, (255, 0, 0), rect, 1)
            screen.fill((10, 10, 25))
            bears.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)

    except Exception as e:
        debug_print(f"Error in main: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()

                                # Debug FPS and performance info
                                frame_count += 1
                                if current_time - last_fps_print >= 1000:
                                    debug_print(f"FPS: {frame_count}")
                                    debug_print(f"Bear count: {len(bears.bears)}")
                                    if bears.bears:
                                        bear = bears.bears[0]
                                        debug_print(f"Current frame: {bear['current_frame']}/{len(bear['frames'])-1}")
                                        debug_print(f"Memory usage: {sys.getsizeof(bears.animations[0])//1024}KB for animation")
                                    frame_count = 0
                                    last_fps_print = current_time
