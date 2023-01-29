import random


def generate_deck(artifacts: list):
    return generate_cards(artifacts, 8)


def generate_hand(deck: list):
    return generate_cards(deck, 3)


def generate_mages(mages: list):
    return generate_cards(mages, 2)


def generate_monuments(monuments: list):
    return generate_cards(monuments, 2)


def generate_monuments_deck(monuments: list, number: int):
    return generate_cards(monuments, number)


def generate_places_of_power(places_of_power: list, number: int):
    return generate_cards(places_of_power, number)


def generate_cards(components: list, number: int):
    return random.sample(components, number)


def shuffle_deck(deck):
    random.shuffle(deck)
