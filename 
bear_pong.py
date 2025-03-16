# Colors
WHITE = (255, 255, 255)
BLACK = (10, 10, 25)
NEON_PINK = (255, 20, 147)
NEON_BLUE = (30, 144, 255)
NEON_GREEN = (57, 255, 20)
NEON_YELLOW = (255, 255, 0)
NEON_PURPLE = (180, 0, 255)
NEON_CYAN = (0, 255, 255)
def create_simple_background():
    logger.info("Creating enhanced background surface")
    surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    # Create a more interesting gradient
    for y in range(SCREEN_HEIGHT):
        # Calculate gradient colors with neon effect
        ratio = y / SCREEN_HEIGHT
        r = int(10 + 20 * ratio)  # Dark blue-black background
        g = int(10 + 40 * ratio)
        b = int(25 + 100 * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (SCREEN_WIDTH, y))
    
    # Add grid lines for a more cyberpunk/neon feel
    grid_color = (30, 30, 80, 30)  # Semi-transparent grid
    grid_spacing = 40
    
    # Create a separate surface for the grid to apply transparency
    grid_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    
    # Horizontal grid lines
    for y in range(0, SCREEN_HEIGHT, grid_spacing):
        pygame.draw.line(grid_surface, grid_color, (0, y), (SCREEN_WIDTH, y), 1)
    
    # Vertical grid lines
    for x in range(0, SCREEN_WIDTH, grid_spacing):
        pygame.draw.line(grid_surface, grid_color, (x, 0), (x, SCREEN_HEIGHT), 1)
    
    # Blend the grid with the background
    surface.blit(grid_surface, (0, 0))
    
    # Add center line
    draw_center_line(surface)
    
    return surface

def draw_center_line(surface):
    """Draw a dashed center line on the given surface"""
    dash_length = 20
    gap_length = 10
    dash_color = NEON_GREEN
    center_x = SCREEN_WIDTH // 2 - 2  # Center position, 4 pixels wide
    
    for y in range(0, SCREEN_HEIGHT, dash_length + gap_length):
        pygame.draw.rect(surface, dash_color, (center_x, y, 4, dash_length))
def draw_menu(screen, background, title_font, menu_font):
    """Draw the main menu screen"""
    # Draw the background
    screen.blit(background, (0, 0))
    
    # Create a pulsating effect for the title
    pulse_value = (math.sin(pygame.time.get_ticks() * 0.005) + 1) * 0.5  # Value between 0 and 1
    title_color = (
        int(NEON_GREEN[0] * pulse_value + NEON_CYAN[0] * (1 - pulse_value)),
        int(NEON_GREEN[1] * pulse_value + NEON_CYAN[1] * (1 - pulse_value)),
        int(NEON_GREEN[2] * pulse_value + NEON_CYAN[2] * (1 - pulse_value))
    )
    
    # Main title with shadow effect
    title_text = "HYPERPONG"
    title_shadow = title_font.render(title_text, True, (0, 0, 0))
    title = title_font.render(title_text, True, title_color)
    
    # Position for the title
    title_y = SCREEN_HEIGHT // 4
    screen.blit(title_shadow, (SCREEN_WIDTH//2 - title_shadow.get_width()//2 + 4, title_y + 4))
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, title_y))
    
    # Instructions
    instructions = [
        {"text": "Press SPACE to Start", "color": WHITE},
        {"text": "Player 1: W/S keys", "color": NEON_PINK},
        {"text": "Player 2: UP/DOWN arrows", "color": NEON_BLUE},
        {"text": "First to 5 points wins!", "color": NEON_YELLOW},
        {"text": "ESC to quit", "color": WHITE}
    ]
    
    start_y = SCREEN_HEIGHT // 2
    for i, instruction in enumerate(instructions):
        text = menu_font.render(instruction["text"], True, instruction["color"])
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, start_y + i * 50))

def draw_game_over(screen, background, title_font, menu_font, winner_idx, winner_color):
    """Draw the game over screen"""
    # Draw the background
    screen.blit(background, (0, 0))
    
    # Winner text with glow effect
    glow_size = int(math.sin(pygame.time.get_ticks() * 0.01) * 10 + 20)  # Pulsating glow
    glow_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    
    winner_text = f"PLAYER {winner_idx} WINS!"
    winner_render = title_font.render(winner_text, True, winner_color)
    
    # Draw glow
    for i in range(glow_size, 0, -2):
        alpha = 40 - i  # Fade out the glow
        if alpha < 0:
            alpha = 0
        glow = pygame.Surface((winner_render.get_width() + i*2, winner_render.get_height() + i*2), pygame.SRCALPHA)
        glow.fill((0, 0, 0, 0))
        pygame.draw.ellipse(glow, (*winner_color, alpha), glow.get_rect())
        screen.blit(glow, (SCREEN_WIDTH//2 - glow.get_width()//2, SCREEN_HEIGHT//3 - glow.get_height()//2))
    
    # Draw main text
    screen.blit(winner_render, (SCREEN_WIDTH//2 - winner_render.get_width()//2, SCREEN_HEIGHT//3))
    
    # Instructions
    instructions = [
        {"text": "Press SPACE to Play Again", "color": WHITE},
        {"text": "Press ESC to Quit", "color": WHITE}
    ]
    
    start_y = SCREEN_HEIGHT * 2 // 3
    for i, instruction in enumerate(instructions):
        text = menu_font.render(instruction["text"], True, instruction["color"])
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, start_y + i * 50))

def create_particle_effect(x, y, color, count=20):
    """Create particles for visual effects"""
    particles = []
    for _ in range(count):
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(2, 8)
        size = random.uniform(2, 6)
        lifetime = random.uniform(30, 60)  # frames
        dx = math.cos(angle) * speed
        dy = math.sin(angle) * speed
        particles.append({
            'x': x, 'y': y, 'dx': dx, 'dy': dy,
            'color': color, 'size': size, 'lifetime': lifetime
        })
    return particles

def update_particles(particles):
    """Update particle positions and lifetimes"""
    updated_particles = []
    for p in particles:
        p['x'] += p['dx']
        p['y'] += p['dy']
        p['lifetime'] -= 1
        p['size'] *= 0.95  # Particles get smaller over time
        
        if p['lifetime'] > 0 and p['size'] > 0.5:
            updated_particles.append(p)
    return updated_particles

def draw_particles(screen, particles):
    """Draw particles on the screen"""
    for p in particles:
        alpha = int(255 * (p['lifetime'] / 60))  # Fade out
        color = (*p['color'], alpha)
        pygame.draw.circle(
            screen, 
            color, 
            (int(p['x']), int(p['y'])), 
            int(p['size'])
        )

def main():
        # Create fonts for different purposes
        title_font = pygame.font.Font(None, 100)
        menu_font = pygame.font.Font(None, 40)
        score_font = pygame.font.Font(None, 74)
        
        # Initialize the game state to MENU
        game_state = GameState.MENU
        
        # Initialize particles list for visual effects
        particles = []
        
        # Add state transition time for smooth transitions
        transition_time = 0
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if game_state == GameState.PLAYING:
                            game_state = GameState.MENU
                        elif game_state == GameState.MENU or game_state == GameState.GAME_OVER:
                            running = False
                    elif event.key == pygame.K_SPACE:
                        if game_state == GameState.MENU:
                            # Reset scores and start a new game
                            player1.score = 0
                            player2.score = 0
                            ball.reset()
                            game_state = GameState.PLAYING
                            # Create particles for transition effect
                            particles = create_particle_effect(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, NEON_GREEN, 50)
                
