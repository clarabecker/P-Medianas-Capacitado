from instance import Instance
from solution import Solution
from constructive import random_solution, construction, random_destruction, guided_destruction
from ls import local_search
import random
import argparse

def setup():
    global MAX_ITERATIONS, ALPHA, BETA, D1, D2, I, RESTART, RESTART_PERCENT, DESTRUCTION, LS, ACCEPTANCE
    MAX_ITERATIONS = args.max_iterations
    ALPHA = args.alpha
    BETA = args.beta
    D1 = args.d1
    D2 = args.d2
    RESTART = args.restart
    RESTART_PERCENT = args.restart_percent
    DESTRUCTION = args.destruction
    LS = args.ls
    ACCEPTANCE = args.acceptance
    I = Instance(args.instance)


def accept(S_new, incumbent, S_new_value, incumbent_value):
    if   ACCEPTANCE == 'incumbent': return incumbent
    elif ACCEPTANCE ==   'current': return S_new


def iterated_greedy():
    S = random_solution(I)
    incumbent = Solution(I, S)
    incumbent_value = incumbent.complete_obj()
    print(incumbent_value)

    no_improving_iterations = 0

    for _ in range(MAX_ITERATIONS):
        S_new = Solution(I, S)

        if RESTART and no_improving_iterations >= (MAX_ITERATIONS * RESTART_PERCENT):
            S_new = random_solution(I)
            no_improving_iterations = 0

        if DESTRUCTION == 'random':
            S_new = random_destruction(I, S_new, D1, D2)
        elif DESTRUCTION == 'guided':
            S_new = guided_destruction(I, S_new, D1, D2)

        S_new = construction(I, S_new, ALPHA, BETA)

        if LS: S_new = local_search(S_new)

        S_value = S.complete_obj()
        S_new_value = S_new.complete_obj()
        no_improving_iterations += 1

        if S_new_value < incumbent_value:
            incumbent = Solution(I, S_new)
            incumbent_value = S_new_value
            no_improving_iterations = 0
            print(incumbent_value)

        S = accept(S_new, incumbent, S_value, incumbent_value)

    print(incumbent)


def main():
    setup()
    iterated_greedy()


if __name__ == "__main__":
    global args
    parser = argparse.ArgumentParser()
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')
    required.add_argument('--instance', help = 'problem instance', metavar = '<file>', type=str, required = True)
    optional.add_argument('--max_iterations', help = 'max. number of iterations of IG [100, 100000] (default: 1000)', metavar = '<m>', type = int, default = 1000)
    optional.add_argument('--alpha', help = 'construction greediness for equipments [0, 1] (default: 0.3)', metavar = '<a>', type = float, default = 0.3)
    optional.add_argument('--beta', help = 'construction greediness for coverage [0, 1] (default: 0.2)', metavar = '<b>', type = float, default = 0.2)
    optional.add_argument('--d1', help = 'destruction size for equipments [0, 1] (default: 0.4)', metavar = '<d1>', type = float, default = 0.4)
    optional.add_argument('--d2', help = 'destruction size for coverage [0, 1] (default: 0.3)', metavar = '<d2>', type = float, default = 0.3)
    optional.add_argument('--restart', help = 'enables restart uppon stagnation (disabled by default)', action='store_true')
    optional.add_argument('--restart_percent', help = 'percentage of total iterations without improvement indicating stagnation [0, 1] (default: 0.1)', metavar = '<r>', type = float, default = 0.1)
    optional.add_argument('--destruction', help = 'destruction procedure {random, guided} (default: random)', metavar = '<des>', type = str, default = 'guided')
    optional.add_argument('--ls', help = 'enables local search (disabled by default)', action='store_true')
    optional.add_argument('--acceptance', help = 'acceptance strategy {current, incumbent} (default: current)', metavar = '<acc>', type = str, default = 'current')

    args, other = parser.parse_known_args()
    main()