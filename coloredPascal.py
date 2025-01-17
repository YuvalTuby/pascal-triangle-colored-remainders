import pygame
import sys
from tkinter import Tk
from tkinter.filedialog import asksaveasfilename
from datetime import datetime

# Cell_Size Constants
BIG_CELL_SIZE = 20
MEDIUM_CELL_SIZE = 10
SMALL_CELL_SIZE = 5
SUPER_SMALL_CELL_SIZE = 2

# UI Color Constants
BUTTON_COLOR = (240, 240, 240)  # Light gray
BUTTON_HOVER_COLOR = (180, 180, 180)  # Darker gray for hover
TEXT_COLOR = (0, 0, 0)  # Black

# Color palette for remainder values
colors = [
    (50, 168, 82),   # Green
    (0, 0, 0),       # Black for remainder 1
    (219, 68, 55),   # Red
    (66, 133, 244),  # Blue
    (123, 31, 162),  # Purple
    (255, 128, 0),   # Orange
    (0, 188, 212)    # Cyan
]

def generate_color_palette(divisor):
    """Generate a color palette based on the divisor."""
    num_remainders = divisor  # Possible remainder values range from 0 to divisor-1
    palette = []
    
    # Generate a color for each remainder
    for i in range(num_remainders):
        # Use HSV color space to generate distinct, evenly spaced colors
        hue = i / num_remainders  # Scale hue from 0 to 1
        color = pygame.Color(0)  # Create a blank color object
        color.hsva = (hue * 360, 100, 100)  # Set the color in HSV (Hue, Saturation, Value)
        palette.append(color)
    
    return palette


# Memoization dictionary to store binomial coefficients
binomial_cache = {}

# Function to calculate the binomial coefficient with memoization
def binomial_coefficient(n, k):
    if k == 0 or k == n:
        return 1
    if (n, k) in binomial_cache:
        return binomial_cache[(n, k)]
    result = binomial_coefficient(n - 1, k - 1) + binomial_coefficient(n - 1, k)
    binomial_cache[(n, k)] = result
    return result

def draw_pascals_triangle(screen, divisor, cell_size, show_rem=False):
    
    """Draw Pascal's triangle with updated color palette."""
    # Generate the dynamic color palette based on the divisor
    colors = generate_color_palette(divisor)
    
    if cell_size == BIG_CELL_SIZE:
        rows = 45
    elif cell_size == MEDIUM_CELL_SIZE:
        rows = 93
    elif cell_size == SMALL_CELL_SIZE:
        rows = 180
    elif cell_size == SUPER_SMALL_CELL_SIZE:
        rows = 465
    
    """Draw Pascal's triangle with updated color palette."""
    start_x = 500
    start_y = 50

    for n in range(rows):
        for k in range(n + 1):
            value = binomial_coefficient(n, k)
            remainder = value % divisor
            color = colors[remainder % len(colors)]  # Cycle through colors
            x = start_x + (k - n / 2) * cell_size
            y = start_y + n * cell_size
            pygame.draw.rect(screen, color, (x, y, cell_size, cell_size))
            if show_rem or cell_size == 20:
                # Optionally add text inside each cell
                font = pygame.font.Font(None, 24)
                text = font.render(str(remainder), True, (255, 255, 255))  # White text
                text_rect = text.get_rect(center=(x + cell_size / 2, y + cell_size / 2))
                screen.blit(text, text_rect)

def get_input(prompt, x, y):
    pygame.font.init()
    font = pygame.font.Font(None, 36)
    input_box = pygame.Rect(x, y, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((30, 30, 30), input_box)
        txt_surface = font.render(prompt + text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()

    return text

def draw_button(screen, text, x, y, width, height, color):
    # Get mouse position and create button rectangle
    mouse_pos = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, width, height)
    
    # Check if mouse is hovering over button
    is_hovered = button_rect.collidepoint(mouse_pos)
    
    # Draw button with appropriate color
    pygame.draw.rect(screen, BUTTON_HOVER_COLOR if is_hovered else color, button_rect)
    
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)
    # screen.blit(text_surface, (x + (width - text_surface.get_width()) // 2, y + (height - text_surface.get_height()) // 2))
    # Return both rectangle and hover state for click detection
    return button_rect, is_hovered

def draw_ui(divisor=None, cell_size=None):
    """Redraw the static UI components, including the entered values."""
    # Display entered divisor
    font = pygame.font.Font(None, 36)

    # Draw buttons and store both rectangles and hover states
    big_rect, big_hover = draw_button(screen, "Big", 50, 150, 200, 50, BUTTON_COLOR)
    med_rect, med_hover = draw_button(screen, "Medium", 50, 220, 200, 50, BUTTON_COLOR)
    small_rect, small_hover = draw_button(screen, "Small", 50, 290, 200, 50, BUTTON_COLOR)
    super_rect, super_hover = draw_button(screen, "Super Small", 50, 360, 200, 50, BUTTON_COLOR)

    return (big_rect, big_hover), (med_rect, med_hover), (small_rect, small_hover), (super_rect, super_hover)

def draw_reset_text():
    font = pygame.font.Font(None, 36)
    text = font.render("Press ESC\Enter to Reset", True, (255, 255, 255))
    text_rect = text.get_rect(center=(800, 200))  # Center on right side
    screen.blit(text, text_rect)

def main():
    pygame.init()
    global screen
    screen = pygame.display.set_mode((1000, 1000))
    pygame.display.set_caption("Pascal's Triangle")


    while True:
        screen.fill((20, 20, 40)) # Dark blue-gray background
        
        # Draw UI elements
        buttons = draw_ui()
        pygame.display.flip()
        
        # Get divisor input while keeping buttons visible
        divisor = int(get_input("Divisor: ", 50, 100))
        
        # Wait for the user to click a button
        button_clicked = False
        while not button_clicked:
            # Get button states
            buttons = draw_ui(divisor=divisor)
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for (rect, hover), size in zip(buttons, 
                        [BIG_CELL_SIZE, MEDIUM_CELL_SIZE, SMALL_CELL_SIZE, SUPER_SMALL_CELL_SIZE]):
                        if rect.collidepoint(mouse_pos):
                            cell_size = size
                            button_clicked = True
                            break
        
        # Clear only triangle area (right side of screen)
        pygame.draw.rect(screen, (20, 20, 40), (300, 0, 700, 1000))

        # Draw triangle
        rows = {BIG_CELL_SIZE: 45, MEDIUM_CELL_SIZE: 93, SMALL_CELL_SIZE: 180, SUPER_SMALL_CELL_SIZE: 465}[cell_size]
        draw_pascals_triangle(screen, divisor, cell_size)
        draw_reset_text()  # Add reset text
        pygame.display.flip()
        
        # Add Save Option
        save_button_rect, save_hover = draw_button(screen, "Press 'S' to Save", 750, 300, 220, 50, BUTTON_COLOR)
        pygame.display.flip()

        # Wait for Enter key
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE):
                    waiting = False
                    pygame.display.flip()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                        save_triangle_as_image(divisor, cell_size, rows)
                    
                    
# Function to save the triangle
def save_triangle_as_image(divisor, cell_size, rows):
    """Save the Pascal's Triangle as an image."""
    # Create an off-screen surface
    width, height = 1000, 1000  # Adjust dimensions as needed
    save_surface = pygame.Surface((width, height))
    
    # Fill the background color
    save_surface.fill((20, 20, 40))  # Dark blue-gray background
    
    # Draw the Pascal's Triangle on the save_surface
    draw_pascals_triangle(save_surface, divisor, cell_size, show_rem=False)
    
    # Initialize Tkinter root window (hidden)
    Tk().withdraw()  # Hide the root window
    # Open the save file dialog
    filename = asksaveasfilename(defaultextension=".png",
                                 filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                                 title="Save Pascal's Triangle")
    
    # If the user selected a file
    if filename:
        pygame.image.save(save_surface, filename)
        print(f"Triangle saved as {filename}")
    else:
        print("Save cancelled.")

if __name__ == "__main__":
    main()