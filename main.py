from p5 import *
import pandas as pd
from utility import Utility

SCREEN_WIDTH, SCREEN_HEIGHT = 2560, 1600-50

class Player():
    def __init__(self, name, id=Utility.generate_random_hash(), score=0):
        self.id = id
        self.name = name
        self.score = score

def state_machine(key=None):
    # implements the state machine
    new_state = None
    game_state = get_item("game_state")
    current_player = get_item("current_player")
    top_player = get_item("top_player")
    input_buffer = get_item("input_buffer")
    if game_state == "WAITING" and key:
        if input_buffer:
            new_state = "PREP"
            set_item("current_player",Player(input_buffer))
    elif game_state == "PREP":
        new_state = "IN_GAME"
    elif game_state == "IN_GAME" and key:
        new_state = "GAME_OVER"
        players = get_players()
        players.append(current_player)
        save_players(players)
    elif game_state == "GAME_OVER" and key:
        setup()
    if new_state:
        print(f"Changing state from {game_state} to {new_state}")
        game_state = new_state
        set_item("game_state", game_state)

def get_players(csv_path="record.csv"):
    players = []
    df = pd.read_csv(csv_path)
    # Iterate over rows as namedtuples
    for row in df.itertuples(index=False):
        players.append(Player(row[1], row[0], row[2]))
    return players

def save_players(players, csv_path="record.csv"):
    players_df = pd.DataFrame([{"id":player.id, "name": player.name, "score": player.score} for player in players ])
    players_df.to_csv(csv_path, index=False)

def setup():

    clear_storage()

    # load from file
    players = get_players()
    if not players:
        players.append(Player(name="Zero", score=1))

    # get top player
    top_player = None
    for player in players:
        if not top_player:
            top_player = player
        elif int(player.score) > int(top_player.score):
            top_player = player

    game_state = "WAITING"

    set_item("game_state", game_state)
    set_item("top_player", top_player)

    size(SCREEN_WIDTH, SCREEN_HEIGHT)
    no_stroke()

    global FONT_ROBOTO_BOLD
    FONT_ROBOTO_BOLD = load_font('fonts/Roboto/Roboto-Black.ttf')

    game_initialized = True
    set_item("game_initialized", game_initialized)
    print(f"top player {top_player}")
    print(f"game state {game_state}")

def draw():
    game_initialized = get_item("game_initialized")
    game_state = get_item("game_state")
    current_player = get_item("current_player")
    top_player = get_item("top_player")

    if game_initialized:
        if game_state == "WAITING":
            generate_display_waiting(top_player)
        elif game_state == "PREP":
            generate_display_prep()
        elif game_state == "IN_GAME":
            generate_display_ingame(current_player, top_player)
        elif game_state == "GAME_OVER":
            generate_display_game_over(current_player, top_player)

def key_pressed(event):
    # handles key presses
    input_buffer = get_item("input_buffer")
    game_initialized = get_item("game_initialized")
    game_state = get_item("game_state")
    if game_initialized:
        if event.key == "ENTER":
            state_machine(event.key)
        elif event.key == "UP" and game_state == "IN_GAME":
            current_player = get_item("current_player")
            current_player.score += 1
            set_item("current_player",current_player)
        elif game_state == "WAITING":
            if str(event.key) in ["SHIFT", "CRTL", "ALT"]:
                return
            if input_buffer:
                input_buffer = input_buffer + str(event.key)
            else:
                input_buffer = str(event.key)
            set_item("input_buffer", input_buffer)

def generate_display_waiting(top_player):

    background(0,191,255)
    text_font(FONT_ROBOTO_BOLD)
    fill(255)

    prompt = f"Waiting for player..."
    prompt_size = 200    
    text_size(prompt_size)
    text(prompt, SCREEN_WIDTH/2-(text_width(prompt)/2), 1*(SCREEN_HEIGHT/4)-(prompt_size/2))

    # generate highest score
    top_player_banner = f"Highest scorer: {top_player.name} - {top_player.score} cm"
    top_player_size = 100
    text_font(FONT_ROBOTO_BOLD)
    text_size(top_player_size)
    text(top_player_banner, SCREEN_WIDTH/2-(text_width(top_player_banner)/2), SCREEN_HEIGHT-(top_player_size)-30)

    input_buffer = get_item("input_buffer")
    if input_buffer:
        player_prompt = f"{input_buffer}"
        player_prompt_size = 150
        fill(255)
        text_size(player_prompt_size)
        text(player_prompt, SCREEN_WIDTH/2-(text_width(player_prompt)/2), 2*(SCREEN_HEIGHT/4)-(player_prompt_size/2))

def generate_display_prep():
    current_player = get_item("current_player")
    prep_counter = get_item("prep_counter")
    prompt_size = 200
    background(239,204,0)
    text_font(FONT_ROBOTO_BOLD)
    fill(255)
    text_size(prompt_size)
    
    if not prep_counter:
        prompt = f"Get ready {current_player.name}..."
        text(prompt, SCREEN_WIDTH/2-(text_width(prompt)/2), SCREEN_HEIGHT/2-(prompt_size/2))
        set_item("prep_counter", 4)
    elif prep_counter == 4:
        prompt = f"3"
        text(prompt, SCREEN_WIDTH/2-(text_width(prompt)/2), SCREEN_HEIGHT/2-(prompt_size/2))
        set_item("prep_counter", 3)
        time.sleep(1)
    elif prep_counter == 3:
        prompt = f"2"
        text(prompt, SCREEN_WIDTH/2-(text_width(prompt)/2), SCREEN_HEIGHT/2-(prompt_size/2))
        set_item("prep_counter", 2)
        time.sleep(1)
    elif prep_counter == 2:
        prompt = f"1"
        text(prompt, SCREEN_WIDTH/2-(text_width(prompt)/2), SCREEN_HEIGHT/2-(prompt_size/2))
        set_item("prep_counter", 1)
        time.sleep(1)
    elif prep_counter == 1:
        state_machine()
        time.sleep(1)

def generate_display_ingame(player, top_player):

    # generate player name
    player_name = f"{player.name}'s turn"
    player_name_size = 200
    background(204)
    text_font(FONT_ROBOTO_BOLD)
    fill(128)
    text_size(player_name_size)
    text(player_name, SCREEN_WIDTH/2-(text_width(player_name)/2), 0)

    # generate player score
    player_score = f"{player.score} cm"
    player_score_size = 500
    text_font(FONT_ROBOTO_BOLD)
    fill(0)
    text_size(player_score_size)
    text(player_score, SCREEN_WIDTH/2-(text_width(player_score)/2), SCREEN_HEIGHT/2-(player_score_size/2))

    # generate highest score
    top_player_banner = f"Highest scorer: {top_player.name} - {top_player.score} cm"
    top_player_size = 100
    text_font(FONT_ROBOTO_BOLD)
    fill(150)
    text_size(top_player_size)
    text(top_player_banner, SCREEN_WIDTH/2-(text_width(top_player_banner)/2), SCREEN_HEIGHT-(top_player_size))

def generate_display_game_over(current_player, top_player):
    background(196,98,16)

    if current_player.score > top_player.score:
        background(60,179,113)
        prompt = f"Congratulation {current_player.name}! You are the new top scorer"
        prompt_size = 100
        fill(255)
        text_size(prompt_size)
        text(prompt, SCREEN_WIDTH/2-(text_width(prompt)/2), 2*SCREEN_HEIGHT/4-(prompt_size/2))
    else:
        prompt = f"{current_player.name}! Your score is {current_player.score} cm"
        prompt_size = 100
        fill(255)
        text_size(prompt_size)
        text(prompt, SCREEN_WIDTH/2-(text_width(prompt)/2), 2*SCREEN_HEIGHT/4-(prompt_size/2))

    prompt = f"Game over"
    prompt_size = 250
    text_font(FONT_ROBOTO_BOLD)
    fill(255)
    text_size(prompt_size)
    text(prompt, SCREEN_WIDTH/2-(text_width(prompt)/2), 1*SCREEN_HEIGHT/4-(prompt_size/2))


if __name__ == "__main__":
    run(sketch_setup=setup, sketch_draw=draw)