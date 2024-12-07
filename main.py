from dotenv import load_dotenv

# Load local .env file
load_dotenv()

import json
import os

from halo import Halo

# Import functions from other modules
from lib.prompts import prepare_define_story_prompt, prepare_generate_story_prompt, prepare_system_prompt
from lib.gpt import get_gpt_chat_response, get_gpt_response
from lib.print import print_narrator, print_player, print_game_end
from lib.game import get_narration_mechanism, get_side_characters, get_story_setting, get_story_theme, get_story_length, \
    get_side_characters_with_occurrence, get_round_side_characters

# Load the GPT model from environment variables
GPT_MODEL = os.environ['GPT_MODEL']

# Function to clear the terminal screen
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# Initialize spinner for loading indication
spinner = Halo(spinner='dots')

# Get user inputs for story configuration
story_theme = get_story_theme()
clear_terminal()
story_setting = get_story_setting()
clear_terminal()
side_characters = get_side_characters()
clear_terminal()
story_length = get_story_length()
clear_terminal()
narration_mechanism = get_narration_mechanism()
clear_terminal()

# Determine if the narration mechanism is choice-based
with_choices = False
if narration_mechanism == 'choice_based':
    with_choices = True

# Assign side characters with their occurrence rounds if any
if side_characters:
    side_characters = get_side_characters_with_occurrence(story_length, side_characters)

print('\n')
spinner.start('Creating your story...')

# Generate the story definition using GPT
story_definition_response = get_gpt_response(
    prompt=prepare_define_story_prompt(story_theme, story_setting),
    model=GPT_MODEL,
    temperature=1.2
)

# Parse the story definition response
story_definition = json.loads(story_definition_response)

# Prepare initial messages for the GPT chat
messages = [
    {"role": "system", "content": prepare_system_prompt()},
    {"role": "user", "content": prepare_generate_story_prompt(story_definition, with_choices)}
]

spinner.stop()

# Main game loop
while True:
    clear_terminal()

    # Decrease remaining rounds by 1 on every player prompt
    story_length -= 1

    # Print narrator's part of the story
    print_narrator('Narrator: \n')
    response = get_gpt_chat_response(
        messages,
        model=GPT_MODEL,
        stream_output=True,
        output_function=print_narrator,
        temperature=0.2
    )
    messages.append({"role": "assistant", "content": response})

    # End game condition check
    if story_length < 1:
        break

    # Get player's input
    print_player('\nPlayer: \n')
    player_input = input()

    # Add available side characters to the player's input
    available_side_characters = get_round_side_characters(story_length, side_characters)
    if available_side_characters:
        for character in available_side_characters:
            player_input += f". ADD CHARACTER: '{character['character']}'"

    # Add special commands to the player's input based on the remaining rounds
    if story_length == 3:
        player_input += ". DRAW"  # Draw the user close to the ending of the game

    if story_length == 1:
        player_input += ". END"  # Finalize the game, resulting in ending it.

    messages.append({"role": "user", "content": player_input})

# Print the end of the game messages
print_game_end("\n\nTHE END")
print_game_end("\n\n\nThank you for playing!")