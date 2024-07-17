from solution import Solution
from random import choice, shuffle


def local_search(S):
    current = Solution(S.I, S)
    while True:
        neighbor = first_improvement(Solution(current.I, current))
        if neighbor is None: return current
        else: current = neighbor


def first_improvement(S):
    neighbor = Solution(S.I, S)
    value = neighbor.complete_obj()

    equipments = neighbor.equipments.copy()
    while len(equipments) > 0:
        location = choice(equipments)
        equipments.remove(location)
        neighbor.remove_equipment(location)

        for loc in range(neighbor.I.N):
            if neighbor.check_loc(loc):
                neighbor.add_equipment(loc)
                neighbor = cover_locations(neighbor)
                if neighbor.complete_obj() < value and len(neighbor.equipments) == neighbor.I.p:
                    return neighbor
                else:
                    neighbor = Solution(S.I, S)
                    neighbor.remove_equipment(location)
    return None


def cover_locations(S):
    uncovered = S.uncovered.copy()
    equipments = S.equipments.copy()
    shuffle(uncovered)
    shuffle(equipments)
    for loc in uncovered:
        for equip in equipments:
            if S.check_cover(equip, loc):
                S.cover(equip, loc)
                break
    return S
