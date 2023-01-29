from src.components.components import Components
from src.settings.settings import Settings
from utils import (generate_hand, generate_deck, generate_mages,
                   generate_monuments_deck, generate_places_of_power, generate_monuments, shuffle_deck)
from info import format_deck_info, player_choice_info


class Game(Settings):
    def __init__(self):
        super().__init__()
        self.all_components = Components().get_all_components

    # configure players for game session
    def configuration(self):
        while self.settings_mode is None:
            self.settings_mode = input(self.settings_msg['description'])
            self.set_mode(self.settings_mode)
        while self.players_count is None:
            try:
                self.players_count = int(input(self.settings_msg['players']))
            except ValueError:
                print('Please enter the correct number.')
            if self.players_count:
                self.set_players(self.players_count)
        self.show_settings()
        self.game_components = self.all_components(self.expansions)
        self.set_player_sheets(self.game_components.get('sheet'),
                               self.set_player_names(int(self.players_count)))

    # setup components for game session
    def setup_components(self):
        self.monuments_deck = generate_monuments_deck(self.game_components.get('monuments'), self.monuments_count)
        self.monuments = generate_monuments(self.monuments_deck)
        self.places_of_power = generate_places_of_power(self.game_components.get('places_of_power'),
                                                        self.places_of_power_count)
        [self.monuments_deck.remove(monument) for monument in self.monuments]

    # prepare deck for every player
    def preparation(self):
        shuffle_deck(self.sheets)
        player_queue = 0
        for sheet in self.sheets:
            player_queue += 1
            sheet['number'] = player_queue
            sheet['deck'] = generate_deck(self.game_components.get('artifacts'))
            sheet['mages'] = generate_mages(self.game_components.get('mages'))
            [self.game_components.get('artifacts').remove(artifact) for artifact in sheet['deck']]
            [self.game_components.get('mages').remove(artifact) for artifact in sheet['mages']]
            for essence in sheet['essences']:
                sheet['essences'][essence] += 1

    def player_choices(self):
        for sheet in self.sheets:
            player_choice_info(sheet)

    def launch(self):
        self.player_choices()

    def start(self):
        self.configuration()
        self.setup_components()
        self.preparation()
        self.launch()




if __name__ == '__main__':
    Game().start()
