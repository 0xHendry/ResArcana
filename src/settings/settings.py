class Settings:
    def __init__(self):
        # LAT - Lux at Tenebrae
        # PI - Perlae Imperii
        self.settings_msg = {
            "description": f'1: Base - Play only with base expansion | players: 2-4, victory points: 10.\n'
                           f'2: Base and LAT - Play base and LAT expansion | players: 2-5, victory points: 10.\n'
                           f'3: Full - Play base, LAT and PI expansions | players: 2-5, victory points: 13.\n'
                           f'0: Exit.\n'
                           f'Choose your mode for game.\n',
            "players": 'Choose number of players. Enter 0 for exit.\n',
            "description_answer": 'Your choice is "{0}".'
        }
        self.settings_mode, self.players_count = None, None
        self.victory_points, self.monuments_count, self.places_of_power_count = 10, 7, 2
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

    def set_mode(self, mode: str):
        match mode:
            case "1":
                print(self.settings_msg['description_answer'].format('Base'))
                self.expansions, self.victory_points = ("Base",), 10
            case "2":
                print(self.settings_msg['description_answer'].format('Base and LAT'))
                self.expansions, self.victory_points = ("LAT", "Base"), 10
            case "3":
                print(self.settings_msg['description_answer'].format('Full'))
                self.expansions, self.victory_points = ("PI", "LAT", "Base"), 13
            case "0":
                print(self.settings_msg['description_answer'].format('Exit'))
                exit()
            case _:
                print("This mode don't exists. Please choose a suggested one.")
                self.settings_mode = None

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
            player_name = self.define_unique_name(input(f'Please enter name of player {_+1}.'
                                                        f' Or enter "bot" for choose bot as player.\n').capitalize(),
                                                  players)
            players.append(player_name)
        return players

    def define_unique_name(self, player_name, players, name_mark=0):
        if player_name in players:
            player_name += f' ({name_mark + 1})'
            self.define_unique_name(player_name, players, name_mark)
        return player_name
