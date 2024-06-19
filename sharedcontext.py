from game import Game
class SharedContext:
    def __init__(self, screen, background_color = "BROWN", text_color = "WHITE", button_color = "GRAY", engine_strength = 1000, game = Game(), flipped_board = False):
        self.screen = screen
        self.game = game
        self.player_data = {}
        self.game_settings = {"bcolor": background_color,"tcolor": text_color, "button_color": button_color, "estrength": engine_strength}
        self.current_score = 0

        self.colors = {"WHITE":(255, 255, 255), "BLACK":(100, 100, 100), "BLUE": (0, 0, 255), 
                       "GRAY":(180, 180, 180)        , "GREEN": (0, 255, 0), "BROWN": (150, 75, 0)}

