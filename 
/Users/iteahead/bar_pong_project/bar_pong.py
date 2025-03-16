    def update(self):
        # Update frame counter for animation timing
        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            self.frame_counter = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            
            # Increase frequency of screen character changes
            if random.random() < 0.6:  # Increased from 0.3 to 0.6
                frame = self.frames[self.frame_index]
                # Randomly change characters on multiple screen lines
                for screen_line in range(3, 5):  # Lines with "screen" content
                    if screen_line < len(frame):
                        chars = list(frame[screen_line])
                        # More binary characters changing
                        for i in range(9, 14):  # Expanded range of positions
                            if i < len(chars):
                                chars[i] = random.choice(self.matrix_chars)
                        frame[screen_line] = ''.join(chars)
        
        # Update pulsing glow effect
        self.pulse_counter += 1
        if self.pulse_counter % 3 == 0:  # Slower cycle for smooth effect
            self.glow_intensity += 0.05 * self.glow_direction
            if self.glow_intensity >= 1.0:
                self.glow_intensity = 1.0
                self.glow_direction = -1
            elif self.glow_intensity <= 0.2:
                self.glow_intensity = 0.2
                self.glow_direction = 1
        
        # Update matrix drops with more dynamic behavior
        for drop in self.matrix_drops:
            drop['y'] += drop['speed']
            # Randomly change characters as they fall
            if random.random() < 0.08:
                drop['char'] = random.choice(self.matrix_chars)
                drop['alpha'] = random.randint(150, 255)
            
            # Reset drops when they fall out of view or randomly
            if drop['y'] > 20 or random.random() < 0.005:
                drop['y'] = random.randint(-15, 2)
                drop['x'] = random.randint(-20, 60)
                drop['char'] = random.choice(self.matrix_chars)
                drop['speed'] = random.uniform(0.3, 0.8)
                drop['size'] = random.uniform(0.8, 1.2)
                drop['alpha'] = random.randint(150, 255)
    def draw(self, surface, font):
        # Get current frame
        current_frame = self.frames[self.frame_index]
        
        # Draw matrix effect first (background) with enhanced visibility
        for drop in self.matrix_drops:
            # Enhanced matrix effect with variable brightness and size
            alpha_value = int(drop['alpha'])
            # Brighter green for better visibility
            matrix_color = (20, min(255, int(180 + self.glow_intensity * 75)), 20, alpha_value)
            
            # Render with size variation for more dynamic effect
            size_factor = drop['size']
            matrix_font = pygame.font.Font(None, int(30 * size_factor))
            matrix_char = matrix_font.render(drop['char'], True, matrix_color)
            
            x_pos = self.x + drop['x'] * 10
            y_pos = self.y + drop['y'] * 20
            
            # Enhanced glow effect
            glow_surf = pygame.Surface((30, 30), pygame.SRCALPHA)
            glow_surf.fill((0, 0, 0, 0))  # Transparent
            
            # Add pulsing glow to matrix characters
            for glow in range(3):
                glow_size = glow * 2
                glow_alpha = int(80 * self.glow_intensity) - (glow * 20)
                if glow_alpha > 0:
                    glow_color = (20, min(255, int(180 + self.glow_intensity * 75)), 20, glow_alpha)
                    pygame.draw.circle(glow_surf, glow_color, 
                                     (15, 15), 
                                     int(8 * size_factor) + glow_size)
            
            # Draw the character with glow
            matrix_rect = matrix_char.get_rect(center=(15, 15))
            glow_surf.blit(matrix_char, matrix_rect)
            surface.blit(glow_surf, (x_pos, y_pos))
        
        # Draw ASCII bear with laptop
        line_height = 24
        for i, line in enumerate(current_frame):
            # Special processing for laptop screen lines (add pulsing glow)
            is_screen_line = 3 <= i <= 4  # Lines containing the laptop screen
            
            # Calculate more intense glow for laptop screen
            if is_screen_line:
                # Dynamic color for pulsing laptop screen
                screen_intensity = self.glow_intensity
                base_color = (
                    int(100 + screen_intensity * 155), 
                    int(200 + screen_intensity * 55), 
                    int(255)
                )
            else:
                # Regular bear color
                base_color = (200, 230, 255)
            
            # Base text
            text_surf = font.render(line, True, base_color)
            text_rect = text_surf.get_rect(center=(self.x + 100, self.y + i * line_height))
            
            # Enhanced glow effect
            if is_screen_line:
                # More intense glow effect for laptop screen
                for offset in [5, 4, 3, 2, 1]:
                    glow_intensity = self.glow_intensity
                    glow_color = (
                        int(50 + glow_intensity * 100), 
                        int(100 + offset * 30 + glow_intensity * 50), 
                        int(200 + offset * 10 + glow_intensity * 30), 
                        int((50 + offset * 30) * glow_intensity)
                    )
                    glow_surf = font.render(line, True, glow_color)
                    glow_rect = glow_surf.get_rect(center=(self.x + 100, self.y + i * line_height))
                    
                    # Create a surface with per-pixel alpha
                    s = pygame.Surface((glow_rect.width + 20, glow_rect.height + 20), pygame.SRCALPHA)
                    s.fill((0, 0, 0, 0))  # Transparent
                    s.blit(glow_surf, (10, 10))
                    
                    # Apply blur effect by scaling down and up
                    s = pygame.transform.scale(s, (glow_rect.width // 2, glow_rect.height // 2))
                    s = pygame.transform.scale(s, (glow_rect.width + 20, glow_rect.height + 20))
                    surface.blit(s, (glow_rect.left - 10, glow_rect.top - 10))
            else:
                # Regular glow for the rest of the bear
                for offset in [3, 2, 1]:
                    glow_color = (50, 100 + offset * 50, 200 + offset * 20, 50 + offset * 50)
                    glow_surf = font.render(line, True, glow_color)
                    glow_rect = glow_surf.get_rect(center=(self.x + 100, self.y + i * line_height))
