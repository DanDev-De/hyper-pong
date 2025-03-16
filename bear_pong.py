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
import cv2
from enum import Enum

# Initialize pygame and its modules
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Set up logging
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
BALL_SIZE = 30
PADDLE_SPEED = 8
BALL_SPEED = 7.0
FPS = 60
WINNING_SCORE = 5  # Score needed to win the game

# Colors
WHITE = (255, 255, 255)
BLACK = (10, 10, 25)
NEON_PINK = (255, 20, 147)
NEON_BLUE = (30, 144, 255)
NEON_GREEN = (57, 255, 20)
NEON_CYAN = (0, 255, 255)
NEON_YELLOW = (255, 255, 0)

class GameState(Enum):
    MENU = 1
    PLAYING = 2
    GAME_OVER = 3
def create_simple_background():
    logger.info("Creating simple background surface")
    surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Create gradient background
    for y in range(SCREEN_HEIGHT):
        color_value = int(255 * (y / SCREEN_HEIGHT))
        pygame.draw.line(surface, (0, color_value, color_value), 
                      (0, y), (SCREEN_WIDTH, y))
    
    # Draw center line
    for i in range(0, SCREEN_HEIGHT, 20):
        pygame.draw.rect(surface, NEON_GREEN, (SCREEN_WIDTH//2 - 2, i, 4, 10))
    
    return surface

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 6)
        self.velocity_x = random.uniform(-2, 2)
        self.velocity_y = random.uniform(-2, 2)
        self.life = random.randint(20, 40)
    
    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.life -= 1
        self.size = max(0, self.size - 0.1)
        return self.life > 0
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))

def create_particle_effect(x, y, color, count=10):
    particles = []
    for _ in range(count):
        particles.append(Particle(x, y, color))
    return particles

def update_particles(particles):
    return [p for p in particles if p.update()]

def draw_particles(screen, particles):
    for particle in particles:
        particle.draw(screen)
        
def draw_menu(screen, background, title_font, menu_font):
    # Draw background
    screen.blit(background, (0, 0))
    
    # Draw title with glow effect
    title = title_font.render("BEAR PONG", True, NEON_GREEN)
    title_rect = title.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))
    
    # Add glow effect
    glow_size = 3
    for offset in range(1, glow_size+1):
        glow_surface = title_font.render("BEAR PONG", True, (0, min(255, 50+offset*50), 0))
        for dx, dy in [(o, p) for o in (-offset, 0, offset) for p in (-offset, 0, offset)]:
            if dx == 0 and dy == 0:
                continue
            screen.blit(glow_surface, (title_rect.x + dx, title_rect.y + dy))
    
    screen.blit(title, title_rect)
    
    # Draw instructions
    start_text = menu_font.render("Press SPACE to Start", True, WHITE)
    start_rect = start_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT*2//3))
    screen.blit(start_text, start_rect)
    
    controls1 = menu_font.render("Player 1: W/S keys", True, NEON_PINK)
    controls1_rect = controls1.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT*2//3 + 50))
    screen.blit(controls1, controls1_rect)
    
    controls2 = menu_font.render("Player 2: UP/DOWN arrows", True, NEON_BLUE)
    controls2_rect = controls2.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT*2//3 + 100))
    screen.blit(controls2, controls2_rect)

def draw_game_over(screen, background, title_font, menu_font, winner_idx, winner_color):
    # Draw background
    screen.blit(background, (0, 0))
    
    # Draw winner message with glow effect
    title = title_font.render(f"Player {winner_idx} Wins!", True, winner_color)
    title_rect = title.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))
    
    # Add glow effect
    glow_size = 3
    for offset in range(1, glow_size+1):
        glow_surface = title_font.render(f"Player {winner_idx} Wins!", True, 
                                    tuple(max(0, c - 100) for c in winner_color))
        for dx, dy in [(o, p) for o in (-offset, 0, offset) for p in (-offset, 0, offset)]:
            if dx == 0 and dy == 0:
                continue
            screen.blit(glow_surface, (title_rect.x + dx, title_rect.y + dy))
    
    screen.blit(title, title_rect)
    
    # Draw instructions
    restart_text = menu_font.render("Press SPACE to Restart", True, WHITE)
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT*2//3))
    screen.blit(restart_text, restart_rect)
    
    menu_text = menu_font.render("Press ESC for Menu", True, WHITE)
    menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT*2//3 + 50))
    screen.blit(menu_text, menu_rect)

class Ball:
    def __init__(self, animation_frames):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.speed_x = BALL_SPEED
        self.speed_y = BALL_SPEED
        self.size = BALL_SIZE
        self.frames = animation_frames
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_duration = 50
        self.rect = pygame.Rect(self.x - self.size//2, self.y - self.size//2, 
                              self.size, self.size)
        self.rotation = 0
        self.rotation_speed = 3

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.rect.center = (self.x, self.y)
        self.rotation += self.rotation_speed

    def reset(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.speed_x = BALL_SPEED * random.choice([-1, 1])
        self.speed_y = BALL_SPEED * random.choice([-1, 1])
        self.rect.center = (self.x, self.y)

    def bounce(self, paddle=None):
        if paddle:
            self.speed_x *= -1
            self.speed_y = random.uniform(-BALL_SPEED, BALL_SPEED)
            self.rotation_speed *= -1
        else:
            self.speed_y *= -1

    def draw(self, screen):
        if not self.frames:
            pygame.draw.circle(screen, NEON_GREEN, 
                            (int(self.x), int(self.y)), self.size//2)
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.frame_duration:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_update = current_time

        try:
            frame = self.frames[self.current_frame]
            rotated = pygame.transform.rotate(frame, self.rotation)
            rect = rotated.get_rect()
            rect.center = (self.x, self.y)
            screen.blit(rotated, rect)
        except Exception as e:
            logger.error(f"Error drawing ball frame: {e}")
            pygame.draw.circle(screen, NEON_GREEN, 
                            (int(self.x), int(self.y)), self.size//2)

class Player:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.color = color
        self.score = 0
        self.speed = PADDLE_SPEED

    def move(self, up=True):
        if up and self.rect.top > 0:
            self.rect.y -= self.speed
        elif not up and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

def load_gif_frames(gif_path, size=(64, 64)):
    logger.info(f"Loading animation from {gif_path}")
    if not os.path.exists(gif_path):
        logger.error(f"Animation file not found: {gif_path}")
        return None
    
    try:
        gif = iio.imread(gif_path)
        logger.info(f"GIF loaded with shape: {gif.shape}")
        frames = []
        for frame in gif:
            pil_image = Image.fromarray(frame)
            pil_image = pil_image.resize(size)
            mode = pil_image.mode
            size = pil_image.size
            data = pil_image.tobytes()
            frames.append(pygame.image.fromstring(data, size, mode).convert_alpha())
        logger.info(f"Successfully loaded {len(frames)} frames")
        return frames
    except Exception as e:
        logger.error(f"Error loading GIF: {e}")
        return None
def main():
    try:
        # Set up display
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Bear Pong")
        clock = pygame.time.Clock()

        # Create background
        background = create_simple_background()

        # Load ball animation
        gif_path = os.path.join("assets", "images", "bears", "bear1.gif")
        ball_frames = load_gif_frames(gif_path, (BALL_SIZE * 2, BALL_SIZE * 2))

        # Load sounds
        try:
            bounce_sound = pygame.mixer.Sound("assets/audio/sfx/bounce.wav")
            score_sound = pygame.mixer.Sound("assets/audio/sfx/score.wav")
            pygame.mixer.music.load("assets/audio/music/background.wav")
            pygame.mixer.music.play(-1)
            sound_enabled = True
        except Exception as e:
            logger.error(f"Error loading sounds: {e}")
            sound_enabled = False

        # Create game objects
        player1 = Player(50, SCREEN_HEIGHT//2 - PADDLE_HEIGHT//2, NEON_PINK)
        player2 = Player(SCREEN_WIDTH - 50 - PADDLE_WIDTH, 
                      SCREEN_HEIGHT//2 - PADDLE_HEIGHT//2, NEON_BLUE)
        ball = Ball(ball_frames)

        # Create fonts
        title_font = pygame.font.Font(None, 100)
        menu_font = pygame.font.Font(None, 40)
        score_font = pygame.font.Font(None, 74)

        # Initialize game state and particles
        game_state = GameState.MENU
        particles = []
        transition_alpha = 255  # For fade effects

        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if game_state == GameState.PLAYING:
                            game_state = GameState.MENU
                        else:
                            running = False
                    elif event.key == pygame.K_SPACE:
                        if game_state == GameState.MENU:
                            # Reset game and start playing
                            player1.score = 0
                            player2.score = 0
                            ball.reset()
                            game_state = GameState.PLAYING
                            particles = create_particle_effect(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, NEON_GREEN, 50)
                        elif game_state == GameState.GAME_OVER:
                            game_state = GameState.MENU

            # Update game logic based on state
            if game_state == GameState.MENU:
                draw_menu(screen, background, title_font, menu_font)
            
            elif game_state == GameState.PLAYING:
                # Player controls
                keys = pygame.key.get_pressed()
                if keys[pygame.K_w]:
                    player1.move(up=True)
                if keys[pygame.K_s]:
                    player1.move(up=False)
                if keys[pygame.K_UP]:
                    player2.move(up=True)
                if keys[pygame.K_DOWN]:
                    player2.move(up=False)

                # Move ball
                ball.move()

                # Ball collisions
                if ball.rect.top <= 0 or ball.rect.bottom >= height:
                    ball.velocity[1] = -ball.velocity[1]

    except Exception as e:
        logger.error(f"Error in main game loop: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
