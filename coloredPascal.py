import pygame
import sys

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

# Function to draw Pascal's triangle
def draw_pascals_triangle(screen, rows, divisor, cell_size):
    colors = [(255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
    start_x = 500
    start_y = 50

    for n in range(rows):
        for k in range(n + 1):
            value = binomial_coefficient(n, k)
            remainder = value % divisor
            color = colors[remainder % len(colors)]
            x = start_x + (k - n / 2) * cell_size
            y = start_y + n * cell_size
            pygame.draw.rect(screen, color, (x, y, cell_size, cell_size))
            pygame.draw.rect(screen, color, (x, y, cell_size, cell_size))  # Remove gaps by drawing the same color border

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
    pygame.draw.rect(screen, color, (x, y, width, height))
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, (0, 0, 0))
    screen.blit(text_surface, (x + (width - text_surface.get_width()) // 2, y + (height - text_surface.get_height()) // 2))

def main():
    pygame.init()
    global screen
    screen = pygame.display.set_mode((1000, 1000))
    pygame.display.set_caption("Pascal's Triangle")

    while True:
        screen.fill((0, 0, 0))
        rows = int(get_input("Rows: ", 50, 50))
        divisor = int(get_input("Divisor: ", 50, 100))

        # Draw buttons for cell size selection
        draw_button(screen, "Big", 50, 150, 200, 50, (255, 255, 255))
        draw_button(screen, "Medium", 50, 220, 200, 50, (255, 255, 255))
        draw_button(screen, "Small", 50, 290, 200, 50, (255, 255, 255))
        draw_button(screen, "Super Small", 50, 360, 200, 50, (255, 255, 255))
        pygame.display.flip()

        cell_size = 10  # Default to medium if no button is clicked

        # Wait for the user to click a button
        button_clicked = False
        while not button_clicked:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if 50 <= mouse_x <= 250:
                        if 150 <= mouse_y <= 200:
                            cell_size = 20
                            button_clicked = True
                        elif 220 <= mouse_y <= 270:
                            cell_size = 10
                            button_clicked = True
                        elif 290 <= mouse_y <= 340:
                            cell_size = 5
                            button_clicked = True
                        elif 360 <= mouse_y <= 410:
                            cell_size = 2
                            button_clicked = True

        screen.fill((0, 0, 0))  # Clear the screen before drawing
        draw_pascals_triangle(screen, rows, divisor, cell_size)
        pygame.display.flip()

        # Pause to allow the user to see the result
        pause = True
        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    pause = False

if __name__ == "__main__":
    main()