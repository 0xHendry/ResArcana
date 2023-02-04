class Actions:
    def __init__(self):
        self.mage_choice = None
        self.item_choice = None
        self.income_cards = ('artifacts', 'monuments', 'places of power', 'item', 'mage')

    def reset_player_choice(self):
        self.mage_choice = None

    def reset_item_choice(self):
        self.item_choice = None

    # todo: Add help for choices
    def player_mage_choice(self, sheet):
        while self.mage_choice is None:
            try:
                self.mage_choice = int(input(f'{sheet.get("name")}, you have to choose one of two mages,'
                                             f' enter 1 or 2 to choose a mage:\n'))
                if int(self.mage_choice) in (1, 2):
                    sheet['mage'] = [sheet['mages'][self.mage_choice - 1]]
                    sheet.pop('mages')
                else:
                    self.reset_player_choice()
            except ValueError:
                print('Please enter the correct number.')
        self.reset_player_choice()

    def player_item_choice(self, sheet, items):
        while self.item_choice is None:
            try:
                self.item_choice = int(input(f'{sheet.get("name")}, you have to choose an item'
                                             f' enter number of chosen item:\n'))
                if int(self.item_choice) in range(1, len(items)):
                    sheet['item'] = [items[self.item_choice - 1]]
                    del items[self.item_choice - 1]
                else:
                    self.reset_item_choice()
            except ValueError:
                print('Please enter the correct number.')
        self.reset_item_choice()

    def auto_income(self, sheet):
        for key, value in sheet.items():
            if key in self.income_cards and isinstance(value, list):
                self.income_from_cards(sheet, value)
                # if value.get('income').get('choice'):
                #     print(f'You need choose one essence from income ability for {key} {sheet[key].get("name")}')

        pass

    def income_from_cards(self, sheet, cards):
        return

    @staticmethod
    def any_income():
        pass

    @staticmethod
    def choice_income():
        pass

    @staticmethod
    def player_item_fold(sheet, items):
        items.extend(sheet['item'])
        del sheet['item']
