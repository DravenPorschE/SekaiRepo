import pygame
import sys
import os
from PIL import Image, ImageSequence

class AnimatedGIF:
    def __init__(self, gif_path, screen_width=480, screen_height=320):
        # Initialize pygame
        pygame.init()
        
        # Set up display
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Animated GIF Display")
        
        # Set background color (white)
        self.bg_color = (255, 255, 255)
        
        # Load GIF
        self.frames = []
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_delay = 50  # milliseconds per frame (20 FPS)
        self.last_time = pygame.time.get_ticks()
        self.running = True
        
        # Try to load the GIF
        try:
            self.load_gif(gif_path)
            print(f"Successfully loaded GIF: {len(self.frames)} frames")
            
            # Center position
            if self.frames:
                frame_rect = self.frames[0].get_rect()
                self.gif_x = (screen_width - frame_rect.width) // 2
                self.gif_y = (screen_height - frame_rect.height) // 2
                print(f"GIF position: ({self.gif_x}, {self.gif_y})")
        except Exception as e:
            print(f"Error loading GIF: {e}")
            self.running = False
            self.show_error(str(e))
    
    def load_gif(self, gif_path):
        """Load GIF frames using PIL and convert to Pygame surfaces"""
        # Construct full path
        full_path = os.path.join("sekai_faces", "happy.GIF")
        print(f"Loading GIF from: {full_path}")
        
        # Open GIF file
        gif = Image.open(full_path)
        
        # Get original dimensions
        original_width, original_height = gif.size
        print(f"Original GIF dimensions: {original_width}x{original_height}")
        
        # Calculate scale to fit screen while maintaining aspect ratio
        max_width = self.screen_width - 40  # 20px padding on each side
        max_height = self.screen_height - 40
        
        scale = min(max_width / original_width, max_height / original_height)
        scale = min(scale, 1.0)  # Don't scale up, only down if too large
        
        new_width = int(original_width * scale)
        new_height = int(original_height * scale)
        print(f"Scaled to: {new_width}x{new_height}")
        
        # Process each frame
        for frame in ImageSequence.Iterator(gif):
            # Convert mode if needed (paletted GIFs need conversion)
            if frame.mode == 'P':
                frame = frame.convert('RGBA')
            elif frame.mode == 'RGB':
                frame = frame.convert('RGBA')
            
            # Resize if necessary
            if scale < 1.0:
                frame = frame.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert PIL Image to Pygame Surface
            mode = frame.mode
            size = frame.size
            data = frame.tobytes()
            
            # Create pygame surface
            py_surface = pygame.image.fromstring(data, size, mode)
            
            # Convert to display format for better performance
            py_surface = py_surface.convert_alpha()
            
            self.frames.append(py_surface)
        
        gif.close()
    
    def show_error(self, error_msg):
        """Display error message on screen"""
        font = pygame.font.SysFont(None, 24)
        
        # Clear screen
        self.screen.fill(self.bg_color)
        
        # Render error text
        lines = [
            "Error loading GIF:",
            error_msg,
            "",
            f"Current directory: {os.getcwd()}",
            "Looking for: sekai_faces/happy.GIF",
            "",
            "Press ESC to exit"
        ]
        
        y_offset = 50
        for line in lines:
            text = font.render(line, True, (255, 0, 0))
            text_rect = text.get_rect(center=(self.screen_width // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 30
        
        pygame.display.flip()
        
        # Wait for user to close
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        waiting = False
    
    def run(self):
        """Main game loop"""
        clock = pygame.time.Clock()
        
        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_SPACE:
                        # Pause/Resume animation
                        self.frame_delay = 0 if self.frame_delay > 0 else 50
                    elif event.key == pygame.K_UP:
                        # Speed up (decrease delay)
                        self.frame_delay = max(10, self.frame_delay - 10)
                        print(f"Speed: {1000/self.frame_delay:.1f} FPS")
                    elif event.key == pygame.K_DOWN:
                        # Slow down (increase delay)
                        self.frame_delay = min(500, self.frame_delay + 10)
                        print(f"Speed: {1000/self.frame_delay:.1f} FPS")
                    elif event.key == pygame.K_r:
                        # Reset to center
                        if self.frames:
                            frame_rect = self.frames[0].get_rect()
                            self.gif_x = (self.screen_width - frame_rect.width) // 2
                            self.gif_y = (self.screen_height - frame_rect.height) // 2
            
            # Update animation frame
            current_time = pygame.time.get_ticks()
            delta_time = current_time - self.last_time
            self.last_time = current_time
            
            if self.frame_delay > 0 and self.frames:
                self.frame_timer += delta_time
                if self.frame_timer >= self.frame_delay:
                    self.current_frame = (self.current_frame + 1) % len(self.frames)
                    self.frame_timer = 0
            
            # Draw everything
            self.screen.fill(self.bg_color)
            
            if self.frames:
                # Draw current frame
                self.screen.blit(self.frames[self.current_frame], (self.gif_x, self.gif_y))
                
                # Display frame info (optional)
                font = pygame.font.SysFont(None, 20)
                info_text = f"Frame: {self.current_frame + 1}/{len(self.frames)}"
                if self.frame_delay > 0:
                    fps = 1000 / self.frame_delay
                    info_text += f" | Speed: {fps:.1f} FPS"
                else:
                    info_text += " | PAUSED"
                
                info_text += " | SPACE: Pause | UP/DOWN: Speed | ESC: Exit"
                
                text_surface = font.render(info_text, True, (50, 50, 50))
                self.screen.blit(text_surface, (10, self.screen_height - 30))
            
            # Update display
            pygame.display.flip()
            
            # Cap frame rate
            clock.tick(60)
        
        # Clean up
        pygame.quit()
        sys.exit()

# Alternative simpler version without class
def simple_pygame_gif():
    """Simpler version for basic GIF display"""
    pygame.init()
    
    # Setup
    screen_width = 480
    screen_height = 320
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Happy GIF Display")
    clock = pygame.time.Clock()
    
    # Colors
    WHITE = (255, 255, 255)
    
    try:
        # Load GIF
        gif_path = os.path.join("sekai_faces", "happy.GIF")
        print(f"Loading: {gif_path}")
        
        gif = Image.open(gif_path)
        frames = []
        
        # Process each frame
        for frame in ImageSequence.Iterator(gif):
            if frame.mode == 'P':
                frame = frame.convert('RGBA')
            
            # Convert to pygame surface
            py_surface = pygame.image.fromstring(
                frame.tobytes(), frame.size, frame.mode
            ).convert_alpha()
            
            # Scale down if too large
            if py_surface.get_width() > screen_width - 40 or py_surface.get_height() > screen_height - 40:
                scale = min(
                    (screen_width - 40) / py_surface.get_width(),
                    (screen_height - 40) / py_surface.get_height()
                )
                new_size = (
                    int(py_surface.get_width() * scale),
                    int(py_surface.get_height() * scale)
                )
                py_surface = pygame.transform.smoothscale(py_surface, new_size)
            
            frames.append(py_surface)
        
        print(f"Loaded {len(frames)} frames")
        
        # Calculate centered position
        if frames:
            gif_x = (screen_width - frames[0].get_width()) // 2
            gif_y = (screen_height - frames[0].get_height()) // 2
        
        current_frame = 0
        frame_delay = 50  # ms
        last_update = pygame.time.get_ticks()
        
        # Main loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
            
            # Update animation
            now = pygame.time.get_ticks()
            if now - last_update > frame_delay:
                current_frame = (current_frame + 1) % len(frames)
                last_update = now
            
            # Draw
            screen.fill(WHITE)
            if frames:
                screen.blit(frames[current_frame], (gif_x, gif_y))
            
            pygame.display.flip()
            clock.tick(60)
        
    except Exception as e:
        print(f"Error: {e}")
        
        # Show error screen
        screen.fill(WHITE)
        font = pygame.font.SysFont(None, 30)
        error_text = font.render(f"Error: {e}", True, (255, 0, 0))
        screen.blit(error_text, (50, 100))
        
        dir_text = font.render(f"Current dir: {os.getcwd()}", True, (0, 0, 0))
        screen.blit(dir_text, (50, 140))
        
        pygame.display.flip()
        
        # Wait for key press
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    waiting = False
    
    pygame.quit()
    sys.exit()

# Choose which version to run
if __name__ == "__main__":
    # For the full featured version with controls:
    # gif_path = "sekai_faces/happy.GIF"
    # app = AnimatedGIF(gif_path, 480, 320)
    # app.run()
    
    # For the simpler version:
    simple_pygame_gif()