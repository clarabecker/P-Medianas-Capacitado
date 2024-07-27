from solution import Solution
from random import randint, shuffle, choice, choices
from math import ceil

def random_solution(I, S = None):
    if S is None:
        S = Solution(I)
    count = 0
    while (count < I.p):
        index = randint(0, I.N - 1)
        if S.add_equipment(index):
            count = count + 1
    uncovered = S.uncovered.copy()
    shuffle(uncovered)
    for loc in uncovered:
        shuffle(S.equipments)
        for equip in S.equipments:
            if S.check_cover(equip, loc):
                S.cover(equip, loc)
                break
    return S

#Calcula a distância de cada localidade para todos os outros e escolhe uma localidade através de estratégia semi-gulosa (aleatória baseada em ponderação por alpha).
def select_location(I, S, alpha):
    total_dist = {}
    # Semi-greedy selection
    locations_distances = []
    for location in range(I.N):
        total_dist = 0
        for loc in S.uncovered:
            total_dist += I.distance[location][loc]
        locations_distances.append((location, total_dist))
    locations_distances.sort(key = lambda x: x[1])

    amount = max(ceil(len(locations_distances) * alpha), 1)

    to_stop = False
    while not to_stop:
        index = randint(0, amount - 1)
        if S.y[locations_distances[index][0]] != 0:
            locations_distances.remove(locations_distances[index])
        else:
            to_stop = True

    return locations_distances[index][0]

#Seleciona possíveis locais a serem cobertos pelo p, utilizando uma estratégia semi-gulosa controlada pelo parâmetro "beta"
def select_locations_to_cover(I, S, location_covering, beta):
    remaining_capacity = S.remaining_capacity[location_covering]
    locations_to_cover = [(loc, I.dem[loc], I.distance[location_covering][loc]) for loc in S.uncovered if I.dem[loc] <= remaining_capacity]
    locations_to_cover.sort(key = lambda x: x[2])
    # Semi-greedy selection
    result = []
    while len(locations_to_cover) > 0:
        amount = max(ceil(len(locations_to_cover) * beta), 1)
        index = randint(0, amount - 1)
        location, demand, distance = locations_to_cover[index]
        if demand <= remaining_capacity:
            result.append(location)
            remaining_capacity -= demand
        del locations_to_cover[index]
    return result

#estratégia construtiva que enquanto tiver equipamentos disponíveis, aloca em alguma localidade e depois cobre localidades se tiver capacidade restante
def construction(I, S = None, alpha = 0.5, beta = 0.5):
    if S is None:
        S = Solution(I)

    n_equip = I.p - sum(S.y)

    while n_equip > 0:
        location = select_location(I, S, alpha)
        #print(location)
        if S.add_equipment(location):
            n_equip -= 1

        locations_to_cover = select_locations_to_cover(I, S, location, beta)
        for location_to_cover in locations_to_cover:
            S.cover(location, location_to_cover)
    
    for location_covering in S.equipments:
        locations_cover = select_locations_to_cover(I, S, location_covering, beta)
        for location_to_cover in locations_cover:
            S.cover(location_covering, location_to_cover)

    return S

#destruição aleatória sendo d1 o número de equipamentos a serem destruidos e d2 as localidades a serem destruidas
def random_destruction(I, S, d1 = 0.5, d2 = 0.5):
    amount_equip = min(ceil(d1 * sum(S.y)), sum(S.y))
    for _ in range(amount_equip):
        location = choice(S.equipments)
        S.remove_equipment(location)

    covered = []
    for location in range(I.N):
        if S.x[location] != -1: covered.append(location)
    amount_uncover = min(ceil(d2 * len(covered)), len(covered))
    for _ in range(amount_uncover):
        location = choice(covered)
        S.uncover(location)
        covered.remove(location)

    return S

#a função destrói com base no peso de capacidade restante do equipamento (capacidade ociosa) e maior demanda
def guided_destruction(I, S, d1 = 0.5, d2 = 0.5):    
    equipments = [location for location in S.equipments for _ in range(S.y[location])]
    remaining_capacities = [S.remaining_capacity[loc] for loc in equipments]
    amount_equip = min(ceil(d1 * sum(S.y)), sum(S.y))

    for i in range(amount_equip):
        if (sum(remaining_capacities) != 0):
            selected_equipment = choices(equipments, weights=remaining_capacities, k=1)[0]
            index = equipments.index(selected_equipment)
            del equipments[index]
            del remaining_capacities[index]
            S.remove_equipment(selected_equipment)
    
    locations = [location for location in range(I.N) if S.x[location] != -1]
    demands = [I.dem[loc] for loc in locations]
    amount_loc = min(ceil(d2 * len(locations)), len(locations))
    
    for i in range(amount_loc):
        selected_location = choices(locations, weights=demands, k=1)[0]
        index = locations.index(selected_location)
        del locations[index]
        del demands[index]
        S.uncover(selected_location)

    return S
