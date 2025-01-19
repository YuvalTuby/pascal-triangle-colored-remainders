VERSION = "v-0.0.10"
GITHUB_USERNAME = "YuvalTuby"

import pygame
import sys
from tkinter import Tk
from tkinter.filedialog import asksaveasfilename
from datetime import datetime
from pathlib import Path

# Gets hold of file directory
FILE_DIR = Path(__file__).resolve().parent

# Window size
WINDOW_SIZE = 1000;

# Cell size and rows constants as tuples
CELL_SIZES_AND_ROWS = {
    "Big": (20, 48),
    "Medium": (10, 97),
    "Small": (5, 194),
    "Super Small": (2, 485),
    "Smallest": (1, WINDOW_SIZE - 200),
    "Primes": (1, WINDOW_SIZE - 200),
    "Increasing": (1, WINDOW_SIZE - 200)
}

# Accessing cell size and rows
BIG_CELL_SIZE, BIG_CELL_ROWS = CELL_SIZES_AND_ROWS["Big"]
MEDIUM_CELL_SIZE, MEDIUM_CELL_ROWS = CELL_SIZES_AND_ROWS["Medium"]
SMALL_CELL_SIZE, SMALL_CELL_ROWS = CELL_SIZES_AND_ROWS["Small"]
SUPER_SMALL_CELL_SIZE, SUPER_SMALL_CELL_ROWS = CELL_SIZES_AND_ROWS["Super Small"]
SMALLEST_CELL_SIZE, SMALLEST_CELL_ROWS = CELL_SIZES_AND_ROWS["Smallest"]

# UI Color Constants
BUTTON_COLOR = (240, 240, 240)  # Light gray
BUTTON_HOVER_COLOR = (180, 180, 180)  # Darker gray for hover
TEXT_COLOR = (0, 0, 0)  # Black

# Color palette for remainder values
# colors = [
#     (50, 168, 82),   # Green
#     (0, 0, 0),       # Black for remainder 1
#     (219, 68, 55),   # Red
#     (66, 133, 244),  # Blue
#     (123, 31, 162),  # Purple
#     (255, 128, 0),   # Orange
#     (0, 188, 212)    # Cyan
# ]

def change_window_size():
    global WINDOW_SIZE
    # Get system screen info
    info = pygame.display.Info()
    screen_height = info.current_h
    print(f"Detected screen height: {screen_height}")
    
    if screen_height > 1000:
        WINDOW_SIZE = 1000

    elif screen_height <= 1000:
        WINDOW_SIZE = min(1000, screen_height - 40)  # Limit to 1000 pixels wide, or minus 40 for title bar ~32px
        # print(WINDOW_SIZE)
    
    # For Testing    
    # WINDOW_SIZE = screen_height - 40
    
    
    print(f"Adjusted window size: {WINDOW_SIZE}")
    return WINDOW_SIZE  # Return proper window size


def generate_color_palette(divisor):
    """Generate a color palette based on the divisor."""
    num_remainders = divisor  # Possible remainder values range from 0 to divisor-1
    palette = []
    
    # Set a specific green color for remainder 0
    #palette.append((50, 168, 82))  # Green for remainder 0
    palette.append((0,0,0))  # Black for remainder 0
    
    # Generate colors for remaining values
    for i in range(1, num_remainders):
        # Use HSV color space to generate distinct, evenly spaced colors
        hue = i / (num_remainders - 1)  # Scale hue from 0 to 1, excluding 0
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
    result = binomial_coefficient(n - 1, k - 1) + binomial_coefficient(n - 1, k) # Recursive call of nCk
    binomial_cache[(n, k)] = result
    return result

def simulate_large_pascals_triangle(screen, cell_size, divisor, max_rows=5000, displayed_rows=800):
    """
    Simulates how a large Pascal's Triangle would look by scaling down the rows.
    
    Args:
        screen: The pygame screen to draw on.
        cell_size: Size of each cell.
        divisor: Modulus for coloring.
        max_rows: Total number of rows to simulate.
        displayed_rows: Number of rows to actually render.
    """
    scaling_factor = max_rows / displayed_rows
    colors = generate_color_palette(divisor)  # Use the existing function to generate colors
    start_x = WINDOW_SIZE // 2
    start_y = 20

    for displayed_row in range(displayed_rows):
        # Calculate the corresponding "real" row
        real_row = int(displayed_row * scaling_factor)
        for k in range(real_row + 1):
            value = binomial_coefficient(real_row, k)
            remainder = value % divisor
            color = colors[remainder]
            
            # Calculate position
            x = start_x + (k - real_row / 2) * cell_size
            y = start_y + displayed_row * cell_size
            
            # Draw cell
            pygame.draw.rect(screen, color, (x, y, cell_size, cell_size))
        
        # Update display every few rows for smoother drawing
        if displayed_row % 100 == 0:
            pygame.display.flip()

def draw_pascals_triangle(screen, divisor, cell_size, show_rem=False):
    
    """Draw Pascal's triangle with updated color palette."""
    # Generate the dynamic color palette based on the divisor
    colors = generate_color_palette(divisor)
    rows = 10
    
    for size, (size_value, row_value) in CELL_SIZES_AND_ROWS.items():
        if cell_size == size_value:
            rows = row_value
            break
    
    """Draw Pascal's triangle with updated color palette."""
    start_x = WINDOW_SIZE // 2
    start_y = 20

    for n in range(rows):
        for k in range(n + 1):
            value = binomial_coefficient(n, k)
            remainder = value % divisor
            color = colors[remainder % len(colors)]  # Cycle through colors
            x = start_x + (k - n / 2) * cell_size
            y = start_y + n * cell_size
            
            pygame.draw.rect(screen, color, (x, y, cell_size, cell_size))
            if show_rem or cell_size == BIG_CELL_SIZE:
                # Optionally add text inside each cell
                font = pygame.font.Font(None, 24)
                text = font.render(str(remainder), True, (255, 255, 255))  # White text
                text_rect = text.get_rect(center=(x + cell_size / 2, y + cell_size / 2))
                screen.blit(text, text_rect)
              
        # # For SMALLEST_CELL_SIZE, update display every few rows for smoother drawing  
        # if n % 100 == 0:
        #     pygame.display.flip()
                
def draw_prime_pascal_triangles(screen, divisor, cell_size, show_rem=False):
    # Draw pascale triangles of prime numbers with delay
    for i in range(2, divisor + 1):
        if is_prime(i):
            draw_pascals_triangle(screen, i, cell_size, show_rem)
            draw_divisor_and_rows_text(i, CELL_SIZES_AND_ROWS["Super Small"][1])
            pygame.display.flip()
            pygame.time.wait(700)
            pygame.draw.rect(screen, (20, 20, 40), (300, 0, 700, 1000))
            draw_basad_text()
            
def draw_increasing_pascal_triangles(screen, divisor, cell_size):
    # Draw pascale triangles of numbers in increasing order
    for i in range(2, divisor + 1):
        draw_pascals_triangle(screen, i, cell_size)
        draw_divisor_and_rows_text(i, CELL_SIZES_AND_ROWS["Super Small"][1])
        pygame.display.flip()
        #pygame.time.wait(100)
        
        ## Fix problem when trying to add delay in paramaters
        
        pygame.draw.rect(screen, (20, 20, 40), (300, 0, 700, 1000))
        draw_basad_text()
            
            
def is_prime(n):
    if n == 1:
        return False
    i = 2
    while i*i <= n:
        if n % i == 0:
            return False
        i += 1
    return True

def get_input(prompt, x, y):
    pygame.font.init()
    font_size = int(WINDOW_SIZE * 0.036)  # 3.6% of window size
    font = pygame.font.Font(None, font_size)
    input_box = pygame.Rect(x, y, font_size * 5, font_size * 1.05)
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
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()

    return text

def draw_button(screen, text, x, y, width, height, color, font_size=36):
    # Get mouse position and create button rectangle
    mouse_pos = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, width, height)
    
    # Check if mouse is hovering over button
    is_hovered = button_rect.collidepoint(mouse_pos)
    
    # Draw button with appropriate color
    pygame.draw.rect(screen, BUTTON_HOVER_COLOR if is_hovered else color, button_rect)
    
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)
    
    # Return both rectangle and hover state for click detection
    return button_rect, is_hovered, text

def draw_ui(divisor=None, cell_size=None):
    """Redraw the static UI components, including the entered values."""
    # Display entered divisor
    font_size = int(WINDOW_SIZE * 0.036)  # 3.6% of window size
    
    first_button_y = int(WINDOW_SIZE * 0.15)  # 2% from the top
    buttons_x = int(WINDOW_SIZE * 0.02)  # 2% from the left
    
    # Draw buttons and store both rectangles and hover states
    big_rect, big_hover, big_text = (
        draw_button(screen, "Big", buttons_x, 
        first_button_y, 
        font_size * 5, 
        font_size * 1.05, BUTTON_COLOR, font_size))
    
    med_rect, med_hover, med_text = (
        draw_button(screen, "Medium", buttons_x, 
        first_button_y + font_size*1.25, 
        font_size * 5, 
        font_size * 1.05, BUTTON_COLOR, font_size))
    
    small_rect, small_hover, small_text = (
        draw_button(screen, "Small", buttons_x, 
        first_button_y + font_size*2.5, 
        font_size * 5, 
        font_size * 1.05, BUTTON_COLOR, font_size))
    
    super_rect, super_hover, super_text = (
        draw_button(screen, "Super Small", buttons_x, 
        first_button_y + font_size*3.75, 
        font_size * 5, 
        font_size * 1.05, BUTTON_COLOR, font_size))
    
    smallest_rect, smallest_hover, smallest_text = (
        draw_button(screen, "Smallest", buttons_x, 
        first_button_y + font_size*5, 
        font_size * 5, 
        font_size * 1.05, BUTTON_COLOR, font_size))
    
    primes_rect, primes_hover, primes_text = (
        draw_button(screen, "Primes", buttons_x, 
        first_button_y + font_size*6.25, 
        font_size * 5, 
        font_size * 1.05, BUTTON_COLOR, font_size))
    
    increasing_rect, increasing_hover, increasing_text = (
        draw_button(screen, "Increasing", buttons_x, 
        first_button_y + font_size*7.5, 
        font_size * 5, 
        font_size * 1.05, BUTTON_COLOR, font_size))
    
    print(big_text)
    print(med_text)

    return ((big_rect, big_hover, big_text),
            (med_rect, med_hover, med_text),
            (small_rect, small_hover, small_text),
            (super_rect, super_hover, super_text),
            (primes_rect, primes_hover, primes_text),
            (increasing_rect, increasing_hover, increasing_text),
            (smallest_rect, smallest_hover, smallest_text))

def draw_reset_text():
    font_size = int(WINDOW_SIZE * 0.036)  # 3.6% of window size
    font = pygame.font.Font(None, font_size)
    text = font.render("Press ESC\Enter to Reset", True, (255, 255, 255))
    
    # Position text proportionally to window
    text_x = int(WINDOW_SIZE * 0.8)  # 75% from left, matching save button
    text_y = int(WINDOW_SIZE * 0.20)  # 20% from top
    
    text_rect = text.get_rect(center=(text_x, text_y))  # Center on right side
    screen.blit(text, text_rect)
    
def draw_save_button():
    font_size = int(WINDOW_SIZE * 0.036)  # 3.6% of window size

    # Define the button dimensions as a proportion of the window size
    button_width = int(WINDOW_SIZE * 0.22)  # 22% of the window width
    button_height = int(WINDOW_SIZE * 0.05)  # 5% of the window height
    
    # Define the button position (you can tweak these percentages as needed)
    button_x = int(WINDOW_SIZE * 0.765)  # 75% from the left
    button_y = int(WINDOW_SIZE * 0.45)  # 30% from the top
    
    # Draw the button
    save_button_rect, save_hover, _ = draw_button(screen, "Press 'S' to Save", button_x, button_y, button_width, button_height, BUTTON_COLOR, font_size)
    return save_button_rect, save_hover

def draw_divisor_and_rows_text(divisor, rows=None):
    font_size = int(WINDOW_SIZE * 0.036)  # 3.6% of window size
    font = pygame.font.Font(None, font_size)
    text = font.render(f"mod: {divisor} , rows: {rows}", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WINDOW_SIZE * 0.72, WINDOW_SIZE * 0.065))
    screen.blit(text, text_rect)
    
def draw_sierpinski_text():
    font_size = int(WINDOW_SIZE * 0.036)  # 3.6% of window size
    font = pygame.font.Font(None, font_size)
    text = font.render("~Sierpiński Triangle!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WINDOW_SIZE * 0.72, WINDOW_SIZE * 0.1))  # Position below version
    screen.blit(text, text_rect)
    
def PyHebText(txtString=''):
    """Convert Hebrew text to text suitable for pygame."""
    # Reverse the string and return it
    return txtString[::-1]
    
def draw_basad_text():
    # Load a font that supports Hebrew
    # Dynamic path to the font file
    font_path = FILE_DIR / "Arial.ttf"  # Replace with the correct path to a Hebrew-supporting font
    font = pygame.font.Font(font_path, 20)
    
    # Hebrew text
    basad = "בס\"ד"
    hebrew_text = PyHebText(basad)
    
    # Render the text with the appropriate font
    text = font.render(hebrew_text, True, (255, 255, 255))  # White color text
    
    # Get the text's rectangle and position it
    text_rect = text.get_rect(center=(WINDOW_SIZE - 50, 30))  # Position near top-right corner
    screen.blit(text, text_rect)
    
def draw_version_and_user():
    """Display the version on the screen."""
    font = pygame.font.Font(None, 25)
    
    # Render version
    version_text = font.render(VERSION, True, (255, 255, 255))
    version_rect = version_text.get_rect(topleft=(10, 10))  # Top left corner
    screen.blit(version_text, version_rect)
    
     # Render GitHub username
    github_user = f"@{GITHUB_USERNAME}"
    user_text = font.render(github_user, True, (255, 255, 255))
    user_rect = user_text.get_rect(topleft=(10, 30))  # Position below version
    screen.blit(user_text, user_rect)

def main():
    pygame.init()
    global screen
    
    # Change appropriate window size
    change_window_size()
    print(WINDOW_SIZE)
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))

    pygame.display.set_caption(f"Pascal's Triangle {VERSION}")


    while True:
        screen.fill((20, 20, 40)) # Dark blue-gray background
        draw_basad_text()
        draw_version_and_user()
        
        # Draw UI elements
        buttons = draw_ui()
        pygame.display.flip()
        
        # Get divisor input while keeping buttons visible
        while True:
            try:
                divisor = int(get_input("Divisor: ", int(WINDOW_SIZE * 0.02), int(WINDOW_SIZE * 0.08)))
                if divisor > 0:  # Ensure positive divisor
                    break
                else:
                    print("Please enter a positive number")
            except ValueError:
                print("Please enter a valid integer")
        
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
                    for rect, hover, text in buttons:
                        if rect.collidepoint(mouse_pos):
                            cell_size = BIG_CELL_SIZE
                            # Determine which button was clicked
                            if text in CELL_SIZES_AND_ROWS:
                                cell_size = CELL_SIZES_AND_ROWS[text][0]
                            
                            button_clicked = True
                            
                            # Clear only triangle area (right side of screen)
                            pygame.draw.rect(screen, (20, 20, 40), (300, 0, 700, 1000))
                            draw_basad_text()

                            # Draw triangle
                            
                            if text == "Big" or text == "Medium" or text == "Small" or text == "Super Small" or text == "Smallest":
                                draw_pascals_triangle(screen, divisor, cell_size)
                                draw_divisor_and_rows_text(divisor, CELL_SIZES_AND_ROWS[text][1])
                                
                                # Check if div=2 for Sierpinski triangle text
                                if(divisor == 2):
                                    draw_sierpinski_text()
                                
                            elif text == "Primes":
                                draw_prime_pascal_triangles(screen, divisor, cell_size)
                                draw_divisor_and_rows_text(divisor, CELL_SIZES_AND_ROWS[text][1])
                            elif text == "Increasing":
                                # TODO:
                                # Show input box to ask for the delay time
                                #delay_input = get_input("Delay (ms): ", int(WINDOW_SIZE * 0.05), int(WINDOW_SIZE * 0.15))
                                draw_increasing_pascal_triangles(screen, divisor, cell_size)
                                draw_divisor_and_rows_text(divisor, CELL_SIZES_AND_ROWS[text][1])
                            
                            draw_pascals_triangle(screen, divisor, cell_size)
                            draw_reset_text()  # Add reset text
                            pygame.display.flip()
                            
                            break
        
        
        
        # Draw Save button
        draw_save_button()
        pygame.display.flip()

        # Wait for Enter key or Save
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
                    save_triangle_as_image(divisor, cell_size)
                    
                    
# Function to save the triangle
def save_triangle_as_image(divisor, cell_size):
    """Save the Pascal's Triangle as an image."""
    # Create an off-screen surface
    width, height = WINDOW_SIZE, WINDOW_SIZE  # Adjust dimensions as needed
    save_surface = pygame.Surface((width, height))
    
    # Fill the background color
    save_surface.fill((20, 20, 40))  # Dark blue-gray background
    
    # Draw the Pascal's Triangle on the save_surface
    draw_pascals_triangle(save_surface, divisor, cell_size, show_rem=False)
    
    # Initialize Tkinter root window (hidden)
    root = Tk()
    root.withdraw()  # Hide the root window
    
    # Create a suggested filename with timestamp and parameters
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    suggested_name = f"pascal_mod_{divisor}.png"
    filename = asksaveasfilename(defaultextension=".png",
                                filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                                title="Save Pascal's Triangle",
                                initialfile=suggested_name)
    if filename:
        pygame.image.save(save_surface, filename)
        print(f"Triangle saved as {filename}")
    else:
        print("Save cancelled.")
        root.destroy()

if __name__ == "__main__":
    main()