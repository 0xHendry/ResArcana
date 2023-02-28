from src.components.components import Components
from src.settings.settings import Settings
from src.game.actions.actions import Actions
from src.game.info.info import player_mage_choice_info, player_item_choice_info

from utils import (generate_hand, generate_deck, generate_mages,
                   generate_monuments_deck, generate_places_of_power, generate_monuments, shuffle_deck)


class Game(Settings):
    def __init__(self):
        super().__init__()
        self.all_components = Components().get_all_components
        self.actions = Actions()

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
            [self.game_components['artifacts'].remove(artifact) for artifact in sheet['deck']]
            [self.game_components['mages'].remove(artifact) for artifact in sheet['mages']]
            for essence in sheet['essences']:
                sheet['essences'][essence] = 1  # set all start essences on 1

    def first_phase(self):
        for sheet in self.sheets:
            player_mage_choice_info(sheet, self.monuments, self.places_of_power)  # show current player game information
            self.actions.player_mage_choice(sheet)  # player choose mage

    def second_phase(self):
        player_sheets = self.sheets[:]
        player_sheets[1:len(player_sheets)] = player_sheets[1:len(player_sheets)][::-1]  # change order on item choice
        for sheet in player_sheets:
            sheet['hand'] = generate_hand(sheet['deck'])  # randomize player hand from deck
            [sheet['deck'].remove(card) for card in sheet['hand']]  # remove player cards which received in hand
            player_item_choice_info(sheet, self.monuments, self.places_of_power, self.game_components.get('items'))
            shuffle_deck(sheet['deck'])  # shuffle deck
            self.actions.player_item_choice(sheet, self.game_components.get('items'))  # choose item
        self.sheets = sorted(player_sheets, key=lambda x: x['number'])  # returned correct players order

    def third_phase(self):
        for sheet in self.sheets:
            self.actions.get_player_essences_from_card_hold(sheet)
            sheet['essences'] = self.actions.get_player_essences_after_income(sheet)
            # add income and start playing
            pass

    def launch(self):
        self.first_phase()
        self.second_phase()
        self.third_phase()

    def start(self):
        self.configuration()
        self.setup_components()
        self.preparation()
        self.launch()


if __name__ == '__main__':
    Game().start()
