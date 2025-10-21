import turtle
import math
import random


def calculate_side_length(num_hexagons: int) -> float:
    """
    Calculate the side length of hexagons to fit within 500px canvas.
    
    Args:
        num_hexagons: Number of hexagons in one row
        
    Returns:
        Calculated side length for each hexagon
    """
    return 500.0 / (num_hexagons * 1.5 + 0.5)


def calculate_hexagon_height(side_len: float) -> float:
    """
    Calculate the height of a regular hexagon.
    
    Args:
        side_len: Length of one side of the hexagon
        
    Returns:
        Height of the hexagon
    """
    return side_len * (3 ** 0.5)


def hex_to_rgb(color_name: str) -> tuple:
    """
    Convert color name to RGB tuple.
    
    Args:
        color_name: Name of the color
        
    Returns:
        RGB tuple representation of the color
    """
    colors = {
        'red': (255, 0, 0),
        'blue': (0, 0, 255),
        'green': (0, 128, 0),
        'yellow': (255, 255, 0),
        'purple': (128, 0, 128),
        'orange': (255, 165, 0),
        'pink': (255, 192, 203),
        'cyan': (0, 255, 255)
    }
    return colors.get(color_name, (128, 128, 128))


def rgb_to_hex(rgb: tuple) -> str:
    """
    Convert RGB tuple to hexadecimal color code.
    
    Args:
        rgb: Tuple containing RGB values (0-255)
        
    Returns:
        Hexadecimal color code string
    """
    return '#{:02x}{:02x}{:02x}'.format(
        max(0, min(255, rgb[0])),
        max(0, min(255, rgb[1])),
        max(0, min(255, rgb[2]))
    )


def interpolate_color(color1: str, color2: str, factor: float) -> str:
    """
    Interpolate between two colors based on factor.
    
    Args:
        color1: First color name
        color2: Second color name
        factor: Interpolation factor (0.0 to 1.0)
        
    Returns:
        Interpolated color as hexadecimal code
    """
    rgb1 = hex_to_rgb(color1)
    rgb2 = hex_to_rgb(color2)
    
    r = int(rgb1[0] + (rgb2[0] - rgb1[0]) * factor)
    g = int(rgb1[1] + (rgb2[1] - rgb1[1]) * factor)
    b = int(rgb1[2] + (rgb2[2] - rgb1[2]) * factor)
    
    return rgb_to_hex((r, g, b))


def get_gradient_color(color1: str, color2: str, row: int, col: int, 
                      total_rows: int, total_cols: int) -> str:
    """
    Generate gradient color based on position in the grid.
    
    Args:
        color1: Starting color
        color2: Ending color
        row: Current row index
        col: Current column index
        total_rows: Total number of rows
        total_cols: Total number of columns
        
    Returns:
        Gradient color as hexadecimal code
    """
    x_norm = col / (total_cols - 1) if total_cols > 1 else 0.5
    y_norm = row / (total_rows - 1) if total_rows > 1 else 0.5
    factor = (x_norm + y_norm) / 2
    return interpolate_color(color1, color2, factor)


def get_color_choice(prompt: str) -> str:
    """
    Get color choice from user with validation.
    
    Args:
        prompt: Message to display to user
        
    Returns:
        Selected color name in English
    """
    colors = {
        'красный': 'red',
        'синий': 'blue', 
        'зеленый': 'green',
        'желтый': 'yellow',
        'фиолетовый': 'purple',
        'оранжевый': 'orange',
        'розовый': 'pink',
        'голубой': 'cyan'
    }
    
    print("Доступные цвета:")
    for color_name in colors.keys():
        print(f"  {color_name}")
    
    while True:
        choice = input(prompt).strip().lower()
        if choice in colors:
            return colors[choice]
        else:
            print("Недопустимый цвет. Попробуйте снова.")


def get_placement_choice() -> str:
    """
    Get color placement choice from user.
    
    Returns:
        Placement type: 'alternating' or 'gradient'
    """
    while True:
        choice = input("Выберите вариант размещения цветов (1-чередование, 2-градиент): ").strip()
        if choice == '1':
            return 'alternating'
        elif choice == '2':
            return 'gradient'
        else:
            print("Неверный выбор! Введите 1 или 2.")


def get_num_hexagons() -> int:
    """
    Get number of hexagons from user with validation.
    
    Returns:
        Number of hexagons in one row (4-20)
    """
    while True:
        try:
            n = int(input("Введите количество шестиугольников в ряду (4-20): "))
            if 4 <= n <= 20:
                return n
            else:
                print("Число должно быть от 4 до 20!")
        except ValueError:
            print("Неверный ввод! Введите число.")


def hexagon_vertices(center_x: float, center_y: float, side_len: float) -> list:
    """
    Calculate vertices coordinates for a regular hexagon.
    
    Args:
        center_x: X coordinate of hexagon center
        center_y: Y coordinate of hexagon center
        side_len: Length of hexagon side
        
    Returns:
        List of vertex coordinates
    """
    vertices = []
    for i in range(6):
        angle_rad = math.radians(60 * i)
        x = center_x + side_len * math.cos(angle_rad)
        y = center_y + side_len * math.sin(angle_rad)
        vertices.append((x, y))
    return vertices


def draw_hexagon_at(t: turtle.Turtle, center_x: float, center_y: float, 
                   side_len: float, color: str) -> None:
    """
    Draw a single hexagon at specified position.
    
    Args:
        t: Turtle object for drawing
        center_x: X coordinate of hexagon center
        center_y: Y coordinate of hexagon center
        side_len: Length of hexagon side
        color: Fill color for the hexagon
    """
    verts = hexagon_vertices(center_x, center_y, side_len)
    t.penup()
    t.goto(verts[0])
    t.pendown()
    
    t.fillcolor(color)
    t.begin_fill()
    for (x, y) in verts[1:]:
        t.goto(x, y)
    t.goto(verts[0])
    t.end_fill()


def draw_tessellation(num_hexagons: int, color1: str, color2: str, 
                     placement: str) -> None:
    """
    Draw hexagonal tessellation with specified colors and placement.
    
    Args:
        num_hexagons: Number of hexagons in one row
        color1: First color
        color2: Second color
        placement: Color placement type ('alternating' or 'gradient')
    """
    side_len = calculate_side_length(num_hexagons)
    hex_height = calculate_hexagon_height(side_len)

    dx = 1.5 * side_len
    dy = hex_height

    total_width = dx * (num_hexagons - 1) + side_len * 2
    total_height = dy * (num_hexagons - 1) + hex_height

    start_x = -total_width / 2 + side_len
    start_y = total_height / 2 - hex_height / 2

    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    t.pensize(1)
    t.pencolor("black")

    turtle.tracer(0, 0)

    for col in range(num_hexagons):
        for row in range(num_hexagons):
            cx = start_x + col * dx
            cy = start_y - row * dy

            if col % 2 == 1:
                cy -= hex_height / 2

            if placement == 'alternating':
                color = color1 if (row + col) % 2 == 0 else color2
            else:
                color = get_gradient_color(color1, color2, row, col, 
                                         num_hexagons, num_hexagons)

            draw_hexagon_at(t, cx, cy, side_len, color)

    turtle.tracer(1, 10)
    turtle.update()


def main() -> None:
    """Main function to run the hexagonal mosaic program."""
    print("=== Шестиугольная мозаика ===")
    
    color1 = get_color_choice("Выберите первый цвет: ")
    color2 = get_color_choice("Выберите второй цвет: ")
    placement = get_placement_choice()
    num_hexagons = get_num_hexagons()

    screen = turtle.Screen()
    screen.setup(width=500, height=500)
    screen.title("Шестиугольная мозаика")
    screen.bgcolor("white")
    screen.colormode(255)

    draw_tessellation(num_hexagons, color1, color2, placement)

    print("\nМозаика готова! Нажмите на окно для выхода.")
    screen.exitonclick()


if __name__ == "__main__":
    main()
