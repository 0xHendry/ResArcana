class Actions:
    def __init__(self):
        self.mage_choice = None

    def reset_player_choice(self):
        self.mage_choice = None

    def set_player_choice(self, sheet):
        while self.mage_choice is None:
            try:
                self.mage_choice = int(input(f'{sheet.get("name")}, you have to choose one of two mages,'
                                             f' enter 1 or 2 for choose mage:\n'))
                if int(self.mage_choice) in (1, 2):
                    sheet['mage'] = sheet['mages'][self.mage_choice - 1]
                    sheet.pop('mages')
                else:
                    self.reset_player_choice()
            except ValueError:
                print('Please enter the correct number.')
        self.reset_player_choice()
