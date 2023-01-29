def format_deck_info(artifacts_deck, num_card=0):
    component_type = artifacts_deck[0].get('type')
    result = f"{component_type}s:\n" \
             f"------------------------------------\n"
    match component_type:
        case "Artifact":
            format_case = artifacts_format_msg
        case "Item":
            format_case = items_format_msg
        case "Mage":
            format_case = mages_format_msg
        case "Monument":
            format_case = monuments_format_msg
        case "Place of power":
            format_case = places_of_power_format_msg
        case "Scroll":
            format_case = scroll_format_msg
        case _:
            return
    for card in artifacts_deck:
        num_card += 1
        result += format_case(card, component_type)
    return result


def player_choice_info(sheet):
    return (f"Player {sheet.get('number')} turn.\n"
            f"Essences {sheet.get('essences')}.\n"
            f"Your cards:\n"
            f"{format_deck_info(sheet.get('deck'))}.\n"
            f"You have to choose one of two mages:\n"
            f"{format_deck_info(sheet.get('mages'))}")


def artifacts_format_msg(component_card, num_card):
    return (f"{num_card}. Artifact name - {component_card.get('name')}\n"
            f"Archetype - {component_card.get('archetype')}\n"
            f"Cost - {component_card.get('cost')}\n"
            f"Income - {component_card.get('income')}\n"
            f"Points - {component_card.get('points')}\n"
            f"Option - {component_card.get('option')}\n"
            f"Option2 - {component_card.get('option2')}\n"
            f"------------------------------------\n")


def items_format_msg(component_card, num_card):
    return (f"{num_card}. Item name - {component_card.get('name')}\n"
            f"Income - {component_card.get('income')}\n"
            f"Option - {component_card.get('option')}\n"
            f"------------------------------------\n")


def mages_format_msg(component_card, num_card):
    return (f"{num_card}. Mage name - {component_card.get('name')}\n"
            f"Income - {component_card.get('income')}\n"
            f"Option - {component_card.get('option')}\n"
            f"Option2 - {component_card.get('option2')}\n"
            f"------------------------------------\n")


def monuments_format_msg(component_card, num_card):
    return (f"{num_card}. Monument name - {component_card.get('name')}\n"
            f"Cost - {'gold': 4}\n"
            f"Income - {component_card.get('income')}\n"
            f"Points - {component_card.get('points')}\n"
            f"Points generating - {component_card.get('points_generating')}\n"
            f"Option - {component_card.get('option')}\n"
            f"------------------------------------\n")


def places_of_power_format_msg(component_card, num_card):
    return (f"{num_card}. Place of power name - {component_card.get('name')}\n"
            f"Cost - {component_card.get('cost')}\n"
            f"Income - {component_card.get('income')}\n"
            f"Points - {component_card.get('points')}\n"
            f"Points generating - {component_card.get('points_generating')}\n"
            f"Option - {component_card.get('option')}\n"
            f"Option2 - {component_card.get('option2')}\n"
            f"Option3 - {component_card.get('option3')}\n"
            f"------------------------------------\n")


def scroll_format_msg(component_card, num_card):
    return (f"{num_card}. Scroll name - {component_card.get('name')}\n"
            f"Option - {component_card.get('option')}\n"
            f"------------------------------------\n")