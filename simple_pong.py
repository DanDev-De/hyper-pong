import pygame
import sys
import os
from enum import Enum

# Initialize Pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
BALL_SIZE = 30
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
PADDLE_SPEED = 8
BALL_SPEED = 7
WINNING_SCORE = 5

# Colors
WHITE = (255, 255, 255)
BLACK = (10, 10, 25)
NEON_PINK = (255, 20, 147)
NEON_BLUE = (30, 144, 255)
NEON_GREEN = (57, 255, 20)

class GameState(Enum):
    MENU = 1
    PLAYING = 2
    GAME_OVER = 3

def main():
    # Set up display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Simple Pong")
    clock = pygame.time.Clock()

    # Set up fonts
    title_font = pygame.font.Font(None, 74)
    menu_font = pygame.font.Font(None, 36)

    # Game state
    game_state = GameState.MENU
    running = True

    # Create paddles and ball rectangles
    left_paddle = pygame.Rect(50, SCREEN_HEIGHT//2 - PADDLE_HEIGHT//2, 
                           PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = pygame.Rect(SCREEN_WIDTH - 50 - PADDLE_WIDTH, 
                            SCREEN_HEIGHT//2 - PADDLE_HEIGHT//2,
                            PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect(SCREEN_WIDTH//2 - BALL_SIZE//2,
                    SCREEN_HEIGHT//2 - BALL_SIZE//2,
                    BALL_SIZE, BALL_SIZE)

    # Game variables
    ball_dx = BALL_SPEED
    ball_dy = BALL_SPEED
    left_score = 0
    right_score = 0

    # Load sounds
    try:
        bounce_sound = pygame.mixer.Sound(os.path.join("assets", "audio", "sfx", "bounce.wav"))
        score_sound = pygame.mixer.Sound(os.path.join("assets", "audio", "sfx", "score.wav"))
        pygame.mixer.music.load(os.path.join("assets", "audio", "music", "background.wav"))
        pygame.mixer.music.play(-1)
        sound_enabled = True
    except Exception as e:
        print(f"Error loading sounds: {e}")
        sound_enabled = False

    while running:
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
                        game_state = GameState.PLAYING
                        left_score = right_score = 0
                        ball.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
                    elif game_state == GameState.GAME_OVER:
                        game_state = GameState.MENU

        # Fill background
        screen.fill(BLACK)

        if game_state == GameState.MENU:
            # Draw menu
            title = title_font.render("PONG", True, NEON_GREEN)
            start = menu_font.render("Press SPACE to Start", True, WHITE)
            screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 
                             SCREEN_HEIGHT//3))
            screen.blit(start, (SCREEN_WIDTH//2 - start.get_width()//2, 
                             SCREEN_HEIGHT//2))

        elif game_state == GameState.PLAYING:
            # Move paddles
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] and left_paddle.top > 0:
                left_paddle.y -= PADDLE_SPEED
            if keys[pygame.K_s] and left_paddle.bottom < SCREEN_HEIGHT:
                left_paddle.y += PADDLE_SPEED
            if keys[pygame.K_UP] and right_paddle.top > 0:
                right_paddle.y -= PADDLE_SPEED
            if keys[pygame.K_DOWN] and right_paddle.bottom < SCREEN_HEIGHT:
                right_paddle.y += PADDLE_SPEED

            # Move ball
            ball.x += ball_dx
            ball.y += ball_dy

            # Ball collision with top and bottom
            if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
                ball_dy *= -1
                if sound_enabled:
                    bounce_sound.play()

            # Ball collision with paddles
            if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
                ball_dx *= -1
                if sound_enabled:
                    bounce_sound.play()

            # Score points
            if ball.left <= 0:
                right_score += 1
                ball.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
                if sound_enabled:
                    score_sound.play()
            elif ball.right >= SCREEN_WIDTH:
                left_score += 1
                ball.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
                if sound_enabled:
                    score_sound.play()

            # Check for win
            if left_score >= WINNING_SCORE or right_score >= WINNING_SCORE:
                game_state = GameState.GAME_OVER

            # Draw game objects
            pygame.draw.rect(screen, NEON_PINK, left_paddle)
            pygame.draw.rect(screen, NEON_BLUE, right_paddle)
            pygame.draw.ellipse(screen, WHITE, ball)

            # Draw scores
            score1 = title_font.render(str(left_score), True, NEON_PINK)
            score2 = title_font.render(str(right_score), True, NEON_BLUE)
            screen.blit(score1, (SCREEN_WIDTH//4, 20))
            screen.blit(score2, (3*SCREEN_WIDTH//4, 20))

            # Draw center line
            for i in range(0, SCREEN_HEIGHT, 20):
                pygame.draw.rect(screen, NEON_GREEN, 
                              (SCREEN_WIDTH//2 - 2, i, 4, 10))

        elif game_state == GameState.GAME_OVER:
            # Draw game over screen
            winner = "Player 1" if left_score >= WINNING_SCORE else "Player 2"
            color = NEON_PINK if winner == "Player 1" else NEON_BLUE
            text = title_font.render(f"{winner} Wins!", True, color)
            restart = menu_font.render("Press SPACE to play again", True, WHITE)
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 
                            SCREEN_HEIGHT//2))
            screen.blit(restart, (SCREEN_WIDTH//2 - restart.get_width()//2, 
                               SCREEN_HEIGHT//2 + 50))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

