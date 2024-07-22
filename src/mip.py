from pyomo.environ import *

def readInstance(path):
    instance = {}
    with open(path, "r") as f:
        n = int(f.readline().strip())
        p = int(f.readline().strip())
        q = int(f.readline().strip())

        instance['n'] = n
        instance['m'] = n
        instance['p'] = p
        instance['q'] = q
        instance['dem'] = []
        instance['d'] = [[0] * n for _ in range(n)]

        instance['dem'].extend(map(float, f.readline().split()))

        for _ in range(n*n):
            linha = f.readline().strip().split()
            instance['d'][int(linha[0])][int(linha[1])] = float(linha[2])

    return instance

def instancePrint(instance):
    print(instance['n'])
    print(instance['m'])
    print(instance['p'])
    print(instance['q'])
    print(instance['dem'])
    print(instance['d'])

def modelConstruction(instance):
    model = ConcreteModel()

    #Variáveis de decisão
    model.x = Var(range(instance['n']), domain=Binary)
    model.y = Var(range(instance['m']), range(instance['n']), domain=Binary)

    # Função objetivo
    model.obj = Objective(expr=sum(instance['d'][i][j] * model.y[i, j] for i in range(instance['m']) for j in range(instance['n'])), sense=minimize)

    # Restrições
    model.con1 = Constraint(expr=sum(model.x[j] for j in range(instance['n'])) == instance['p'])

    model.con2 = ConstraintList()
    for i in range(instance['m']):
        model.con2.add(sum(model.y[i, j] for j in range(instance['n'])) == 1)

    model.con3 = ConstraintList()
    for i in range(instance['m']):
        for j in range(instance['n']):
            model.con3.add(model.y[i, j] - model.x[j] <= 0)

    model.con4 = ConstraintList()
    for j in range(instance['n']):
        model.con4.add(sum((instance['dem'][i] * model.y[i, j]) for i in range(instance['m'])) <= instance['q'] * model.x[j])
    return model

if __name__ == '__main__':
    instance = readInstance('C://Users//User//OneDrive//Área de Trabalho//respositorio//P-Medianas-Capacitado//instances//AAD_PMEDcap_100_20.txt')
    #instancePrint(instance)
    model = modelConstruction(instance)
    solver = SolverFactory('glpk')
    solver.options['tmlim'] = 3600  # Tempo limite de 1 hora
    result = solver.solve(model)

    print(result)
    print("Valor da Função Objetivo: ", model.obj())
    print("Medianas escolhidas: ", [j for j in range(instance['n']) if model.x[j].value == 1])
    print("Mediana para cada vértice: ",
          [[j for j in range(instance['n']) if model.y[i, j].value == 1] for i in range(instance['m'])])
