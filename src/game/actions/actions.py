class Actions:
    def __init__(self):
        self.mage_choice = None
        self.item_choice = None
        self.essences = ('calm', 'death', 'elan', 'life', 'gold', 'pearl')
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

    def get_income(self, sheet):
        print(f'Turn {sheet.get("name")} income stage')
        for key, value in sheet.items():
            if key in self.income_cards and value and isinstance(value, list):
                self.income_from_cards(sheet.get('essences'), value)
                # if value.get('income').get('choice'):
                #     print(f'You need choose one essence from income ability for {key} {sheet[key].get("name")}')

        pass

    def income_from_cards(self, essences, cards_pack):
        essence_choices = []
        any_choices = []
        for card in cards_pack:
            if isinstance(card.get('income'), dict):
                income = card.get('income')
                if income.get('choice'):
                    income.pop('choice')
                    essence_choices.append(card)  # another check any check
                elif income.get('any'):
                    any_choices.append(card)
                else:
                    for essence, value in income.items():
                        print(f"Added {value} '{essence}' from {card.get('type')} - {card.get('name')}")
                        essences[essence] = essences.get(essence, 0) + value
        [self.choice_income(essences, card) for card in essence_choices]
        [self.any_income(essences, card) for card in any_choices]

    def any_income(self, essences, card):
        print(f'You need to choose any essence from {card.get("type")} - {card.get("name")}\n')
        income = card.get('income')
        essence_types = (set(self.essences) - set(income.get('except')) if income.get('except') else self.essences)
        any_msg = ''
        for number, essence in enumerate(essence_types):
            any_msg += f'{number+1}. {essence}\n'
        pass

    def choice_income(self, essences, card):  # any?
        choice_msg = f'You need to choose income from {card.get("type")} - {card.get("name")}\n'
        income = card.get('income')
        for number, income_info in enumerate(income.items()):
            choice_msg += f'{number+1}. {income_info[0]} +{income_info[1]}\n'
        choice = None
        while choice is None:
            try:
                choice = int(input(choice_msg))
                if choice in (1, 2):
                    chosen_key, value = list(card.get('income').items())[choice-1]
                    essences[chosen_key] = essences.get(chosen_key, 0) + value
                    print(f"Added {value} '{chosen_key}' from {card.get('type')} - {card.get('name')}")
                else:
                    choice = None
            except ValueError:
                print('Please enter the correct number for choose')

    @staticmethod
    def player_item_fold(sheet, items):
        items.extend(sheet['item'])
        sheet['item'].clear()
