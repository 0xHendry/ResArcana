class Settings:
    def __init__(self):
        # LAT - Lux at Tenebrae
        # PI - Perlae Imperii
        self.settings_msg = {
            "expansions": f'1: Base - Play only with base expansion | players: 2-4, victory points: 10.\n'
                          f'2: Base and LAT - Play base and LAT expansion | players: 2-5, victory points: 10.\n'
                          f'3: Full - Play base, LAT and PI expansions | players: 2-5, victory points: 13.\n'
                          f'0: Exit.\n'
                          f'Choose your expansions for game.\n',
            "modes": f'1: Draft - Players will pick cards in draft mode by one card at a time starting from 8.\n'
                     f'2: Random - Every player will get 8 random artifacts at a time.\n'
                     f'0: Exit.\n'
                     f'Choose your mode for game.',
            "players": 'Choose number of players. Enter 0 for exit.\n',
            "description_answer": 'Your choice is "{0}".',
            "mode_not_exists": "This mode doesn't exists. Please choose a suggested one."
        }

        self.game_mode, self.settings_mode, self.players_count = None, None, None
        self.victory_points, self.monuments_count, self.places_of_power_count = 10, 7, 2
        self.game_modes = ("Draft", "Random")
        self.expansions = ()
        self.game_components = {}
        self.sheets, self.monuments_deck, self.monuments, self.places_of_power = [], [], [], []

    def show_settings(self):
        print(
            f'Players - {self.players_count}.\n'
            f'Points to victory - {self.victory_points}.\n'
            f'Monuments count - {self.monuments_count}.\n'
            f'Places of powers - {self.places_of_power_count}.\n'
            f'Expansions - {list(self.expansions)}.\n'
        )

    def set_expansion(self, mode: str):
        match mode:
            case "1":
                self.expansions, self.victory_points = ("Base",), 10
                self.print_description_answer(self.expansions)
            case "2":
                self.expansions, self.victory_points = ("LAT", "Base"), 10
                self.print_description_answer(self.expansions)
            case "3":
                self.expansions, self.victory_points = ("PI", "LAT", "Base"), 13
                self.print_description_answer(self.expansions)
            case "0":
                self.print_description_answer('Exit')
                exit()
            case _:
                print(self.settings_msg['mode_not_exists'])
                self.settings_mode = None

    def set_mode(self, mode: str):
        match mode:
            case "1":
                self.game_mode = "Draft"
                self.print_description_answer(self.game_mode)
            case "2":
                self.game_mode = "Random"
                self.print_description_answer(self.game_mode)
            case "0":
                self.print_description_answer('Exit')
                exit()
            case _:
                print(self.settings_msg['mode_not_exists'])
                self.game_mode = None

    def set_players(self, number: int):
        if int(number) == 5 and len(self.expansions) >= 2 or int(number) in (2, 3, 4):
            print(f'You set players number as {number}.')
            self.players_count = number
            self.set_monuments(number)
            self.set_places_of_power(number)
        elif number == 0:
            exit()
        else:
            print('Incorrect players number. Please enter a correct value.')
            self.players_count = None

    def set_monuments(self, number: int):
        if number > 2:
            self.monuments_count = 2 * number + 4

    def set_places_of_power(self, number: int):
        self.places_of_power_count = 2 + number

    def set_player_sheets(self, template: dict, players: list):
        self.sheets = [{k: (player if k == 'name' else v) for k, v in template.items()} for player in players]

    def set_player_names(self, number: int):
        players = []
        for _ in range(number):
            player_name = self.define_unique_name(input(f'Please enter name of player {_ + 1}.'
                                                        f' Or enter "bot" for choose bot as player.\n').capitalize(),
                                                  players)
            players.append(player_name)
        return players

    def define_unique_name(self, player_name, players, name_mark=0):
        if player_name in players:
            player_name += f' ({name_mark + 1})'
            self.define_unique_name(player_name, players, name_mark)
        return player_name

    def print_description_answer(self, format_part):
        print(self.settings_msg['description_answer'].format(format_part))
