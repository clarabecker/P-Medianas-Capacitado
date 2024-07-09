from random import shuffle

class Solution:
    # Representation
    x = None  # lista armazena qual p cobre cada localização
    y = None  # indica quantos equipamentos estão em cada localização "i", binário

    # Auxiliary structures
    I                  = None  # Instance
    uncovered          = None  # localidades não cobertas
    equipments         = None  # localidades que possuem equipamentos
    remaining_capacity = None  # capacidade restante de cada localização que pode cobrir as outras


    def __init__(self, I, S = None):
        self.I = I
        #copia os valores recebidos
        if S is not None:
            self.x = S.x.copy()
            self.y = S.y.copy()
            self.uncovered = S.uncovered.copy()
            self.equipments = S.equipments.copy()
            self.remaining_capacity = S.remaining_capacity.copy()

        #se a solução for vazia
        else:
            self.x = [-1] * I.N #recebe -1 pq nenhuma localização cobre i
            self.y = [0] * I.N #recebe 0 porque nenhum equipamento está instalado
            self.uncovered = [_ for _ in range(self.I.N)] #todas as localidades não são cobertas inicialmente
            self.equipments = []
            self.remaining_capacity = [0 for _ in range(self.I.N)]  #todos tem capacidade restante 0

    #mudar implementação
    def add_equipment(self, location):
        #todos os bebedouros ja foram alocados, não é possível colocar mais
        if sum(self.y) == self.I.p:
            print('Error: trying to add more than p equipments!')
            exit(1)
        if self.y[location] == 0:
            self.y[location] = 1 #acréscimo ao número de equipamentos
            if location not in self.equipments: self.equipments.append(location) #verificação se o ponto não está presente nos pontos atendidos
            #Moficado para = ao invés de +=
            self.remaining_capacity[location] = self.I.cap #capacidade remanescente recebe capacidade
            if self.x[location] != location and self.check_cover(location, location): #verifica se localização está sendo coberta e se ela mesmo está se cobrindo
                self.cover(location, location)  #cobertura recebe o p que está cobrindo o outro ponto

    #remove p da solução
    def remove_equipment(self, location):
        if self.y[location] == 0:
            print('Error: trying to remove a nonexistent equipment!')
            exit(1)
        self.y[location] = 0
        self.remaining_capacity[location] -= self.I.cap
        if self.y[location] == 0: self.equipments.remove(location)
        [self.uncover(loc) for loc in range(self.I.N) if self.x[loc] == location]


    #verifica se a capacidade restante é maior ou igual a demanda da localidade
    def check_cover(self, location_covering, location_to_cover):
        return self.remaining_capacity[location_covering] >= self.I.dem[location_to_cover]

    #Função para cobrir uma dada localização
    def cover(self, location_covering, location_to_cover):
        if not self.check_cover(location_covering, location_to_cover):
            print('Error: trying to cover with no capacity available!')
            exit(1)
        current_covering = self.x[location_to_cover]
        if current_covering == -1:
            self.uncovered.remove(location_to_cover) #atualiza a lista de não cobertos
        else:
           self.remaining_capacity[current_covering] += self.I.dem[location_to_cover] #adiciona a demanda, porque local não está sendo mais atendido
        self.x[location_to_cover] = location_covering #sendo atendido por p
        self.remaining_capacity[location_covering] -= self.I.dem[location_to_cover] #diminui o valor da capacidade

    #Função para descobrir uma localização que estava corberta
    def uncover(self, location_covered):
        if self.x[location_covered] == -1:
            print('Error: trying to uncover an uncovered location!')
            exit(1)
        location_covering = self.x[location_covered]
        self.remaining_capacity[location_covering] += self.I.dem[location_covered] #o ponto não está mais na cobertura, capacidade adiciona o valor da demanda daquele ponto
        self.uncovered.append(location_covered)
        self.x[location_covered] = -1 #recebe -1 porque está sem equipamentos de novo

    # Full evaluation of objective function
    def complete_obj(self):
        total_dist = 0
        for i in range(self.I.N):
            if self.x[i] == -1:
                total_dist += self.I.penalty
            else:
                total_dist += self.I.distance[i][self.x[i]]
        return total_dist

    def __str__(self):
        result = f'Instance:\t[cap: {self.I.cap}, dem: {self.I.dem}]\n'
        result += f'Distância:\t[distance: {self.I.distance}]\n'
        result += f'Equipments:\t{self.y}\n'
        result += f'Coverage:\t{self.x}\n'
        result += f'Rem. cap.:\t{self.remaining_capacity}\n'
        result += f'Value:\t\t{self.complete_obj()}'
        return result