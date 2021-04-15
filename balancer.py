import json


def items_from_json(filename):
    with open(filename, "r") as file:
        return json.load(file)


def write_items_to_file(filename, json_data):
    with open(filename, "w") as file:
        json.dump(json_data, file, indent=2)


def get_chances(items, key='chance'):
    chances = []
    for item in items:
        chances.append(item[key])
    return chances


def get_total_chance(items, key='chance'):
    chance_placeholder = 0
    for item in items:
        if 'identifier' in item:
            print("adding up", item)
            chance_placeholder += get_total_chance(item['content'])
        else:
            chance_placeholder += item[key]
    return chance_placeholder


def balance(items, key='chance', total=100, inflation_factor=1000):
    chances = get_corrected_chances(inflation_factor=inflation_factor, items=items, key=key, total=total)
    for item, chance in zip(items, chances):
        item[key] = chance
    return items


def get_corrected_chances(items, key, total, inflation_factor):
    new_total = total / inflation_factor
    chances = get_chances(items, key)
    chance_divisor = sum(chances) / new_total
    corrected_chances = []
    for chance in chances:
        corrected_chances.append(int((chance / chance_divisor) * inflation_factor))
    return corrected_chances


def balance_with_output(items, key='chance', total=100, inflation_factor=1000):
    old_chances = get_chances(items, key)
    print("old chances: ", old_chances, "Total:", get_total_chance(items, key))
    balanced_items = balance(items=items, key=key, inflation_factor=inflation_factor, total=total)
    balanced_chances = get_chances(balanced_items, key)
    print("rebalanced chances: ", balanced_chances, "Total:", get_total_chance(items, key))
    return balanced_items


def balance_file(filename, key='chance', total=100, inflation_factor=1000):
    items = items_from_json(filename)
    balanced_items = balance_with_output(items=items, key=key, inflation_factor=inflation_factor, total=total)
    write_items_to_file(filename, balanced_items)


def test_for_group(items):
    there_are_groups = False
    for item in items:
        if 'identifier' in item:
            there_are_groups = True
    return there_are_groups


def balance_with_groups(items, total=1000000, key='chance'):
    has_groups = test_for_group(items)
    print("working on items:", items)
    for item in items:
        print("working on item:", item)
        if 'identifier' in item:
            print("getting chance for group:", item)
            item['chance'] = item['identifier']['total_chance']
    # print(json.dumps(items, indent=2))
    print("balanced total")
    balance(items, total=total)
    # print(json.dumps(items, indent=2))
    for item in items:
        if 'identifier' in item:
            print("overwriting group:", item)
            item['identifier']['total_chance'] = item['chance']
    # print(json.dumps(items, indent=2))
    if has_groups:
        print("working on deeper groups")
        for item in items:
            if 'identifier' in item:
                balance_with_groups(item['content'], item['identifier']['total_chance'])
    else:
        return items
    write_items_to_file("grouped_encounters_test.json", items)
    return items


if __name__ == "__main__":
    # balance_file("Weather.json")
    # balance_file("Wind.json", key='apocalypseChance')
    # balance_file("Wind.json", key='nonApocalypseChance')
    # balance_file("SailingEncounter.json")
    balance_with_output(items_from_json("SailingEncounter.json"), total=1000000)
