import numpy as np
import matplotlib.pyplot as plt
from retangulo_demanda import RetanguloDemanda

def criarFigura (largura, altura, num_pontos_x, num_pontos_y, path_image):
    fig, ax = plt.subplots()
    retangulo = plt.Rectangle((0, 0), largura, altura, edgecolor='black', facecolor='none')
    ax.add_patch(retangulo)

    img = plt.imread(path_image)
    ax.imshow(img, extent=[0, largura, 0, altura], aspect='auto')

    # distância de Manhattan
    x_coords = np.linspace(largura*0.05, largura*0.95, num_pontos_x)
    y_coords = np.linspace(altura*0.05, altura*0.95, num_pontos_y)

    pontos_grid = np.array(np.meshgrid(x_coords, y_coords)).T.reshape(-1, 2)

    pontos_grid = np.round(pontos_grid).astype(int)

    distancias_manhattan = np.zeros((len(pontos_grid), len(pontos_grid)))

    for i, ponto_a in enumerate(pontos_grid):
        for j, ponto_b in enumerate(pontos_grid):
            distancias_manhattan[i, j] = abs(ponto_a[0] - ponto_b[0]) + abs(ponto_a[1] - ponto_b[1])

    ax.plot(pontos_grid[:, 0], pontos_grid[:, 1], 'bo', markersize=5)

    ax.set_xlabel('X (metros)')
    ax.set_ylabel('Y (metros)')

    def criarFiguraRetanguloDemanda(RetanguloDemanda_obj, cor):
        figura = plt.Rectangle(
            (RetanguloDemanda_obj.x, RetanguloDemanda_obj.y),
            RetanguloDemanda_obj.largura,
            RetanguloDemanda_obj.altura,
            edgecolor=cor,
            facecolor='none'
        )
        return figura

    alta_demanda1 = RetanguloDemanda(8, 115, 70, 40)
    figura1 = criarFiguraRetanguloDemanda(alta_demanda1, "red")
    ax.add_patch(figura1)

    alta_demanda2 = RetanguloDemanda(1,80,30,90)
    figura2 = criarFiguraRetanguloDemanda(alta_demanda2, "red")
    ax.add_patch(figura2)

    media_demanda = RetanguloDemanda(100,43,85,90)
    figura3 = criarFiguraRetanguloDemanda(media_demanda, "yellow")
    ax.add_patch(figura3)

    plt.savefig('instance_image.png')

    plt.show()

    return pontos_grid, alta_demanda1, alta_demanda2, media_demanda, distancias_manhattan

def calcular_demanda(pontos_grid, alta_demanda1, alta_demanda2, media_demanda, num_totaldemanda):
    aux_demanda = []
    for ponto in pontos_grid:
        if (alta_demanda1.x <= ponto[0] <= (alta_demanda1.x + alta_demanda1.largura)) and (alta_demanda1.y <= ponto[1] <= (alta_demanda1.y + alta_demanda1.altura)):
            aux_demanda.append(1)
        elif (alta_demanda2.x <= ponto[0] <= (alta_demanda2.x + alta_demanda2.largura)) and (alta_demanda1.y <= ponto[1] <= (alta_demanda1.y + alta_demanda1.altura)):
            aux_demanda.append(1)
        elif (media_demanda.x <= ponto[0] <= (media_demanda.x + media_demanda.largura)) and (media_demanda.y <= ponto[1] <= (media_demanda.y + media_demanda.altura)):
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

    demanda = []
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

    return demanda
def salvar_dados(num_pontos_x, num_pontos_y, p, cap, demanda, distancias_manhattan):
    with open(f'AAD_PMEDcap_{num_pontos_x * num_pontos_y}_{p}.txt', 'w') as f:
        f.write(f"{num_pontos_x * num_pontos_y}\n{p}\n{cap}\n")
        f.write(" ".join(map(str, demanda)) + "\n")
        for linha, colunas in enumerate(distancias_manhattan):
            for coluna, distancia in enumerate(colunas):
                f.write(f"{linha} {coluna} {int(distancia)}\n")


if __name__ == '__main__':
    perc_p = 0.3
    num_totaldemanda = 500
    num_pontos_x = 5
    num_pontos_y = 5

    p = int((num_pontos_x * num_pontos_y) * perc_p)
    cap = int((num_totaldemanda/p) * 1.7)

    pontos_grid, alta_demanda1, alta_demanda2, media_demanda, distancias_manhattan = criarFigura(230, 190, num_pontos_x, num_pontos_y, 'C:\\P-Medianas-Capacitado\\image_map.jpeg')
    demanda = calcular_demanda(pontos_grid, alta_demanda1, alta_demanda2, media_demanda, num_totaldemanda)
    salvar_dados(num_pontos_x, num_pontos_y, p, cap, demanda, distancias_manhattan)

