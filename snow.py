import os
import random
import time
import sys

# Constants
SNOW_DENSITY = 1
DELAY = 0.2
# WIND = 0
WIND_LIMIT = 3
WIND_CHANGE_INTERVAL = 100

time_step_count = 0
WIND = random.randint(-WIND_LIMIT, WIND_LIMIT)

# Unicode characters representing different snowflakes
snowflakes = ['❅', '❆', '❉', '❋', '❊', '❃', '•', '.', '*', '·']

# Get terminal size
term = os.get_terminal_size()
w, h = term.columns, term.lines

# Initialize the grid with empty spaces
grid = [[' '] * w for _ in range(h)]

# Function to create a string representation of the grid
def draw_grid():
    output = ''
    for row in grid:
        output += ''.join(row) + '\n'
    output = output.strip('\n')
    return output

# Function to update the grid with new snowflakes
def update_grid():
    global time_step_count
    global WIND
    global SNOW_DENSITY
    
    # Check if it's time to change the wind direction
    if time_step_count % WIND_CHANGE_INTERVAL == 0:
        # Update wind direction randomly by +/- 1
        WIND += random.choice([-1, 1])
        # Ensure wind is within bounds
        WIND = max(-WIND_LIMIT, min(WIND, WIND_LIMIT))
    
    for i in range(h - 1, 0, -1):
        # Moving every row sideways with the WIND
        grid[i] = grid[i - 1].copy()
        if WIND != 0:
            for _ in range(abs(WIND)):
                grid[i].insert(0 if WIND>0 else w , ' ')
                grid[i].pop(-1 if WIND>0 else 0)
                
        for j, snowflake in enumerate(grid[i]):
            if snowflake != ' ':
                # Adding randomness for each snowflake to move sideways in the breeze
                move_x = random.choices([-1, 0, 1], weights=[0.05, 0.9, 0.05], k=1)[0]
                j_new = max(0, min(w-1, j + move_x))
                grid[i][j] = ' '
                grid[i][j_new] = snowflake

                # Adding randomness on fall sleep for each snowflake
                move_y = random.choices([0, 1], weights=[0.8, 0.2], k=1)[0]
                if move_y == 1:
                    i_new = min(h-1, i + move_y)
                    grid[i][j_new] = ' '
                    grid[i_new][j_new] = snowflake

                
    SNOW_DENSITY += random.choice([-1, 1])
    SNOW_DENSITY = max(1, min(SNOW_DENSITY, 100))          
                
    row = [' '] * w
    for j in range(w):
        if random.random() < SNOW_DENSITY / 100:
            row[j] = random.choice(snowflakes)
    grid[0] = row
    
    time_step_count += 1

# Main function for the snowstorm simulation
def snowstorm(DELAY):
    try:
        while True:
            update_grid()
            output = draw_grid()
            os.system('cls' if os.name == 'nt' else 'clear')
            print(output)
            time.sleep(DELAY)

    except KeyboardInterrupt:
        print('Snowstorm interrupted.')


snowstorm(DELAY)