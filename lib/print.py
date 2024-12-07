from termcolor import cprint

# Function to print game setup messages in cyan color with a blue background
print_game_setup = lambda message: cprint(message, "cyan", "on_blue")

# Function to print error messages in magenta color with a blue background
print_error = lambda message: cprint(message, "magenta", "on_blue")

# Function to print narrator messages in blue color on white background
print_narrator = lambda message: cprint(message, "blue", "on_white", end='')

# Function to print player messages in light blue color with a blue background
print_player = lambda message: cprint(message, "light_blue", "on_blue")

# Function to print game end messages in white color on blue background with bold and underline attributes
print_game_end = lambda message: cprint(message, "white", "on_blue", attrs=["bold", "underline"])