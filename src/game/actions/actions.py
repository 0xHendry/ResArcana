class Actions:
    def __init__(self):
        self.mage_choice = None
        self.item_choice = None
        self.essences = ('calm', 'death', 'elan', 'life', 'gold', 'pearl')
        self.income_cards = ('artifacts', 'monuments', 'places of power', 'item', 'mage')
        self.any_essence = 'any'

    def reset_player_choice(self):
        self.mage_choice = None

    def reset_item_choice(self):
        self.item_choice = None

    # todo: Add "show deck" help for choices
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
        self.reset_player_choice()  # ?

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

    def get_player_essences_after_income(self, sheet):
        print('-----------------------------------------')
        print(f'Player {sheet.get("name")} income stage')
        print(f'Your current essences - {sheet.get("essences")}')
        player_essences = sheet.get('essences').copy()
        for key, value in sheet.items():
            if key in self.income_cards and value and isinstance(value, list):
                self.income_from_cards(player_essences, value)
        return player_essences

    def income_from_cards(self, essences, cards_pack):
        essence_choices = []
        any_choices = []
        hold_choices = []
        for card in cards_pack:
            if isinstance(card.get('income'), dict):
                income = card.get('income')
                if income.get('hold'):
                    hold_choices.append(card)
                elif income.get('choice'):
                    income.pop('choice')
                    essence_choices.append(card)
                elif income.get('any'):
                    any_choices.append(card)
                else:
                    for essence, value in income.items():
                        print(f"Added {value} '{essence}' from {card.get('type')} - {card.get('name')}")
                        essences[essence] = essences.get(essence, 0) + value
        [self.hold_income(essences, card) for card in hold_choices]
        [self.choice_income(essences, card) for card in essence_choices]
        [self.any_income(essences, card) for card in any_choices]
        return essences

    # add get income from on_card
    def hold_income(self, essences, card):
        income = card.get('income')
        if card.get('on_card', {}).get(income.get('hold')):
            if income.get('summation'):
                self.summation_income(card)
            elif income.get('choice'):
                self.choice_income(essences, card)
            elif income.get('any'):
                self.any_income(essences, card)

    @staticmethod
    def summation_income(card):  # windup man mechanics
        for essence, value in card.get('on_card'):
            value += 2

    def any_income(self, essences, card):
        income = card.get('income')
        essence_types = tuple(set(self.essences) - set(income.get('except')) if income.get('except') else self.essences)
        essence_count = income.get(self.any_essence)
        print(f'You need to choose {essence_count} any essence(s) from {card.get("type")} - {card.get("name")}')
        any_msg = ''
        for number, essence in enumerate(essence_types):
            any_msg += f'{number + 1}. {essence}\n'
        for essence_num in range(essence_count):
            choice = None
            while choice is None:
                try:
                    choice = int(input(any_msg))
                    if choice in range(1, len(essence_types)):
                        chosen_key, value = essence_types[choice - 1], 1
                        essences[chosen_key] = essences.get(chosen_key, 0) + value
                        remaining_essences = int(essence_count) - (essence_num + 1)
                        if remaining_essences > 0:
                            print(f"Remaining essences {remaining_essences} to choose from any income.\n")
                        print(f"Your choice is {essence_types[choice - 1]}.\n"
                              f"Your current essences - {essences}")
                    else:
                        choice = None
                except ValueError:
                    print('Please enter the correct number for choose')

    def choice_income(self, essences, card):
        choice_msg = f'You need to choose income from {card.get("type")} - {card.get("name")}\n'
        income = card.get('income')
        essence_types = self.essences + (self.any_essence,)
        for number, income_info in enumerate(income.items()):
            if income_info[0] in essence_types:
                choice_msg += f'{number + 1}. {income_info[0]} +{income_info[1]}\n'
        choice = None
        while choice is None:
            try:
                choice = int(input(choice_msg))
                if choice in (1, 2):
                    chosen_key, value = list(card.get('income').items())[choice - 1]
                    if chosen_key == self.any_essence:
                        self.any_income(essences, card)
                    else:
                        essences[chosen_key] = essences.get(chosen_key, 0) + value
                        print(f"Added {value} '{chosen_key}' from {card.get('type')} - {card.get('name')}.\n"
                              f"Your essences {essences}")
                else:
                    choice = None
            except ValueError:
                print('Please enter the correct number for choose')

    def get_player_essences_from_card_hold(self, sheet):
        pass

    @staticmethod
    def player_item_fold(sheet, items):
        items.extend(sheet['item'])
        sheet['item'].clear()
