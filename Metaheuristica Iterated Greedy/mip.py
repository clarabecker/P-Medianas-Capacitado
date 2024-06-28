from pyomo.environ import *
from instance import Instance
import sys

def solution(I, model):
    print('Equipments: ', end='')
    for i in range(I.N):
        if model.y[i]() > 0: print(f'{i}({model.y[i]()}) ', end='')
    print()
    print('Uncovered cities: ', end='')
    for j in range(I.N):
        covered = False
        for i in range(I.N):
            if model.x[i,j]() == 1:
                covered = True
                break
        if not covered:
            print(f'{j} ')
    print()
    print('Coverage:')
    for i in range(I.N):
        for j in range(I.N):
            if model.x[i,j]() == 1:
                print(f'{i} attending {j}')


def number_uncovered(I, model):
    result = 0
    for j in range(I.N):
        covered = False
        for i in range(I.N):
            if model.x[i,j]() == 1:
                covered = True
                break
        if not covered:
            result +=1
    return result


def formulation(I):
    model = ConcreteModel()

    model.x = Var([_ for _ in range(I.N)], [_ for _ in range(I.N)], domain = Binary)
    model.y = Var([_ for _ in range(I.N)], domain = NonNegativeIntegers)
    model.M = Var(domain = NonNegativeIntegers)

    model.obj = Objective(
        expr = sum(I.distance[i][j] * model.x[i,j] for i in range(I.N) for j in range(I.N)) + model.M * I.penalty, sense = minimize
    )

    model.cons = ConstraintList()

    for j in range(I.N):
        model.cons.add(expr = sum(model.x[i,j] for i in range(I.N)) <= 1)

    for i in range(I.N):
        for j in range(I.N):
            model.cons.add(expr = model.y[i] >= model.x[i,j])

    model.cons.add(expr = sum(model.y[i] for i in range(I.N)) == I.p)

    for i in range(I.N):
        model.cons.add(expr = sum(I.dem[j] * model.x[i,j] for j in range(I.N)) <= I.cap * model.y[i])

    model.cons.add(expr = sum(model.x[i,j] for i in range(I.N) for j in range(I.N)) == I.N - model.M)

    solver = SolverFactory('glpk')
    solver.options['tmlim'] = 3600
    results = solver.solve(model)
    return model.obj.expr(), results, model


def check_coverage():
    regions = ['grande_florianopolis', 'norte', 'serrana', 'alto_vale', 'sul', 'oeste', 'all']
    for region in regions:
        print('='*10, region, '='*10)
        I = Instance(f'../instances/sc_{region}.txt')
        value, results, model = formulation(I)
        print(region, number_uncovered(I, model), f'({results.solver.termination_condition})', value)

#check_coverage()
#exit()

I = Instance(sys.argv[1])
value, results, model = formulation(I)
print(value)
solution(I, model)
if results.solver.termination_condition != TerminationCondition.optimal: print(results.solver.termination_condition)
#print(results.solver.status)