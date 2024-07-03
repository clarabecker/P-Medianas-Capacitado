import numpy as np
import matplotlib.pyplot as plt

def criarFigura (largura, altura, num_pontos_x, num_pontos_y, path_image, num_totaldemanda, perc_p):
    fig, ax = plt.subplots()
    retangulo = plt.Rectangle((0, 0), largura, altura, edgecolor='black', facecolor='none')
    ax.add_patch(retangulo)
    aux_demanda = []
    demanda = []
    p = int((num_pontos_x * num_pontos_y) * perc_p)

    cap = int((num_totaldemanda/p) * 1.5)

    # Adicionar uma imagem de fundo ao retângulo
    img = plt.imread(path_image)
    ax.imshow(img, extent=[0, largura, 0, altura], aspect='auto')

    # Calcular as coordenadas dos pontos no grid usando distância de Manhattan
    x_coords = np.linspace(largura*0.05, largura*0.95, num_pontos_x)  # Ajuste para não ficar nas bordas
    y_coords = np.linspace(altura*0.05, altura*0.95, num_pontos_y)    # Ajuste para não ficar nas bordas

    # Gerar todas as combinações de coordenadas
    pontos_grid = np.array(np.meshgrid(x_coords, y_coords)).T.reshape(-1, 2)

    pontos_grid = np.round(pontos_grid).astype(int)

    # Gerar todas as combinações de coordenadas
    distancias_manhattan = np.zeros((len(pontos_grid), len(pontos_grid)))

    for i, ponto_a in enumerate(pontos_grid):
        for j, ponto_b in enumerate(pontos_grid):
            distancias_manhattan[i, j] = abs(ponto_a[0] - ponto_b[0]) + abs(ponto_a[1] - ponto_b[1])

    # Plotar os pontos do grid na figura
    ax.plot(pontos_grid[:, 0], pontos_grid[:, 1], 'bo', markersize=5)

    # Adicionar rótulos aos eixos
    ax.set_xlabel('X (metros)')
    ax.set_ylabel('Y (metros)')

    # Tamanho do retângulo menor
    largura_altademanda1 = 40
    altura_altademanda1 = 70

    # Calcular as coordenadas do retângulo menor
    x_altademanda1 = 8
    y_altademanda1 = 115

    # Desenhar o retângulo menor
    retangulo_altademanda1 = plt.Rectangle((x_altademanda1, y_altademanda1), largura_altademanda1, altura_altademanda1, edgecolor='red', facecolor='none')
    ax.add_patch(retangulo_altademanda1)

    largura_altademanda2 = 90
    altura_altademanda2 = 30

    x_altademanda2 = 1
    y_altademanda2 = 80

    # Desenhar o retângulo menor
    retangulo_altademanda2 = plt.Rectangle((x_altademanda2, y_altademanda2), largura_altademanda2, altura_altademanda2, edgecolor='red', facecolor='none')
    ax.add_patch(retangulo_altademanda2)

    largura_mediademanda = 85
    altura_mediademanda = 90

    x_mediademanda = 100
    y_mediademanda = 43

    retangulo_mediademanda = plt.Rectangle((x_mediademanda, y_mediademanda), largura_mediademanda, altura_mediademanda, edgecolor='yellow', facecolor='none')
    ax.add_patch(retangulo_mediademanda)

    # Salvar a figura com o retângulo menor
    plt.savefig('instance_image.png')

    # Mostrar a figura
    plt.show()

    for ponto in pontos_grid:
        if (ponto[0] >= x_altademanda1 and ponto[0] <= (x_altademanda1 + largura_altademanda1)) and (ponto[1] >= y_altademanda1 and ponto[1] <= (y_altademanda1 + altura_altademanda1)):
            aux_demanda.append(1)
        elif (ponto[0] >= x_altademanda2 and ponto[0] <= (x_altademanda2 + largura_altademanda2)) and (ponto[1] >= y_altademanda2  and ponto[1] <= (y_altademanda2 + altura_altademanda2)):
            aux_demanda.append(1)
        elif (ponto[0] >= x_mediademanda and ponto[0] <= (x_mediademanda + largura_mediademanda)) and (ponto[1] >= y_mediademanda and ponto[1] <= (y_mediademanda + altura_mediademanda)):
            aux_demanda.append(2)
        else:
            aux_demanda.append(3)

    contaltademanda = 0
    contmediademanda = 0
    contbaixademanda = 0

    for i in aux_demanda:
        if i == 1:
            contaltademanda += 1
        if i == 2:
            contmediademanda += 1
        if i == 3:
            contbaixademanda += 1

    val_altademanda = int((num_totaldemanda * 0.5)/contaltademanda)
    val_mediademanda = int((num_totaldemanda * 0.3)/contmediademanda)
    val_baixademanda = int((num_totaldemanda * 0.2)/contbaixademanda)

    sobra_valores = (num_totaldemanda - ((val_altademanda * contaltademanda) + (val_mediademanda * contmediademanda) + (val_baixademanda * contbaixademanda)))

    for i in aux_demanda:
        if (sobra_valores > 0):
            if i == 1:
                demanda.append(val_altademanda + 1)
                sobra_valores -= 1
            elif i == 2:
                demanda.append(val_mediademanda + 1)
                sobra_valores -= 1
            else:
                demanda.append(val_baixademanda + 1)
                sobra_valores -= 1
        else:
            if i == 1:
                demanda.append(val_altademanda)
            elif i == 2:
                demanda.append(val_mediademanda)
            else:
                demanda.append(val_baixademanda)

    with open('AAD_PMEDcap_'+ str(num_pontos_x * num_pontos_y) + '_' + str(p) +'.txt', 'w') as f:
        f.write(str(num_pontos_x * num_pontos_y) + "\n")
        f.write(str(p) + "\n")
        f.write(str(cap) + "\n")
        for i in demanda:
            f.write(str(i) + " ")
        f.write("\n")
        for linha in range(len(distancias_manhattan)):
            for coluna in range(len(distancias_manhattan[linha])):
                f.write(str(linha) + " " + str(coluna) + " " + str(int(distancias_manhattan[linha, coluna])) + "\n")


if __name__ == '__main__':
    criarFigura(230, 190, 5, 5, 'C://Users//02178611052//PMED_cap//image_map.jpeg', 500, 0.3)
