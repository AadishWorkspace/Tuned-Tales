import random
from .print import print_game_setup, print_error

# Function to get the story length from the user
def get_story_length():
    length_options = {
        "1": "20",
        "2": "50",
        "3": "100"
    }

    prompt_message = """
Please choose your story length:

1- Short
2- Medium
3- Long
    """

    print_game_setup(prompt_message)

    # Loop until valid input is received
    while True:
        user_input = input().strip()
        if user_input not in length_options:
            print_error("Your input must be one of 1, 2, or 3")
        else:
            return int(length_options[user_input])

# Function to get the story setting from the user
def get_story_setting():
    prompt_message = """
Please input your story setting (castle, village, abandoned house, space, island, etc...)
leave blank if you want the AI to select a random setting:
    """

    print_game_setup(prompt_message)
    user_input = input().strip()
    return user_input if user_input else None

# Function to get the story theme from the user
def get_story_theme():
    prompt_message = """
Please input your story theme (escape, survival, romance, etc...)
leave blank if you want the AI to select a random theme:
    """

    print_game_setup(prompt_message)
    user_input = input().strip()
    return user_input if user_input else None

# Function to get side characters from the user
def get_side_characters():
    additional_character_prompt = """
If you would like to add more, please describe another character, else type 'no'.
    """

    initial_prompt = """
Please input a side character that you would like to insert into the story, describe your character briefly such as your relationship to them, their age, profession etc...
Valid input example is "Emily, My Spouse, age 24, doctor"
leave blank if you do not want to insert a side character:
    """

    print_game_setup(initial_prompt)
    characters = []

    # Loop to get multiple side characters
    while True:
        user_input = input().strip()
        if not user_input:
            return []
        elif user_input.lower() == 'no':
            return characters
        characters.append(user_input)
        print_game_setup(additional_character_prompt)

# Function to get the narration mechanism from the user
def get_narration_mechanism():
    mechanism_options = {
        "1": "free_text",
        "2": "choice_based",
    }

    prompt_message = """
Please choose your narrative type
1- Free text:       Resembles an old school text based adventure where you type your action to advance the plot
2- Choice based:    Choose your action based on a list of choices to advance the plot
    """

    print_game_setup(prompt_message)

    # Loop until valid input is received
    while True:
        user_input = input().strip()
        if user_input not in mechanism_options:
            print_error("Your input must be one of 1, or 2")
        else:
            return mechanism_options[user_input]

# Function to assign side characters with their occurrence rounds
def get_side_characters_with_occurrence(story_length, side_characters):
    rounds = story_length - 1

    # Helper function to decrease a value by a percentage
    def decrease_by_percentage(value, percentage):
        return round(value - value * percentage)

    # Helper function to get the decrease percentage based on length
    def get_decrease_percentage(length):
        percentage = 100 / (0.1 * length + 1)
        return round(percentage * 0.01, 2)

    round_numbers = list(range(1, rounds + 1))
    weights = [5 for _ in range(len(round_numbers))]
    decrease_percentage = get_decrease_percentage(len(side_characters))

    weights[0] = 0

    result = []

    # Assign occurrence rounds to each side character
    for character in side_characters:
        selected_round = random.choices(round_numbers, weights, k=1)[0]
        selected_round_index = round_numbers.index(selected_round)
        weights[selected_round_index] = decrease_by_percentage(weights[selected_round_index], decrease_percentage)
        result.append({"character": character, "occurrence": selected_round})

    return result

# Function to get side characters for the current round
def get_round_side_characters(current_round, side_characters):
    return [character for character in side_characters if character["occurrence"] == current_round]