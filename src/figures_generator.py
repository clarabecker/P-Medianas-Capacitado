import matplotlib.pyplot as plt
import numpy as np

def gerar_figura(x_matriz, y_matriz, equipamentos, coberturas):
    coberturas_incrementadas = [num + 1 for num in coberturas]
    indices_equipamentos = [i + 1 for i, val in enumerate(equipamentos) if val == 1]
    coords_clientes = {str(i + 1): (i // y_matriz + 1, i % y_matriz + 1) for i in range(len(equipamentos))}
    coords_locais = {f'L{i}': coords_clientes[f'{i}'] for i in indices_equipamentos}
    alocacao = {f'{j + 1}': f'L{i}' for j in range(len(coberturas_incrementadas)) for i in indices_equipamentos if
                i == coberturas_incrementadas[j]}

    fig, ax = plt.subplots(figsize=(8, 4))

    # Plotar clientes
    for idx, (cliente, (x, y)) in enumerate(coords_clientes.items()):
        if idx == 0:
            ax.scatter(x, y, s=20, c='blue', label='Cliente')
        else:
            ax.scatter(x, y, s=20, c='blue')
        #ax.text(x, y, f' {cliente}', fontsize=12)

    # Plotar locais
    for idx, (local, (x, y)) in enumerate(coords_locais.items()):
        if idx == 0:
            ax.scatter(x, y, s=80, c='red', label='Local')
        else:
            ax.scatter(x, y, s=80, c='red')

    # Plotar conexões
    for cliente, local in alocacao.items():
        x_values = [coords_clientes[cliente][0], coords_locais[local][0]]
        y_values = [coords_clientes[cliente][1], coords_locais[local][1]]
        ax.plot(x_values, y_values, 'k--')

    x_min, x_max = 0, 230
    y_min, y_max = 0, 190

    x_ticks = np.linspace(x_min, x_max, x_matriz)
    y_ticks = np.linspace(y_min, y_max, y_matriz)

    indices_x = np.linspace(1, x_matriz, x_matriz)
    indices_y = np.linspace(1, y_matriz, y_matriz)

    ax.set_xticks(indices_x)
    ax.set_xticklabels([f'{x:.0f}' for x in x_ticks])
    ax.set_yticks(indices_y)
    ax.set_yticklabels([f'{y:.0f}' for y in y_ticks])

    ax.set_xlabel('X (m²)')
    ax.set_ylabel('Y (m²)')

    plt.show()

if __name__ == '__main__':
    # Solução ótima para a instância 25_5
    #x_matriz = 5
    #y_matriz = 5
    #equipamentos = [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0]
    #coberturas = [1, 1, 1, 1, 9, 10, 1, 9, 9, 9, 10, 10, 10, 18, 9, 10, 21, 18, 18, 18, 21, 21, 21, 18, 18]

    #Solução ótima para a instância 25_7
    #x_matriz = 5
    #y_matriz = 5
    #equipamentos = [0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0]
    #coberturas = [1, 1, 1, 3, 9, 10, 1, 12, 9, 9, 10, 10, 12, 12, 9, 10, 21, 18, 18, 18, 21, 21, 21, 18, 18]

    #Solução ótima para a instância 49_9
    #x_matriz = 7
    #y_matriz = 7
    #equipamentos = [0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
    #coberturas = [8, 8, 3, 3, 3, 6, 6, 8, 8, 8, 3, 19, 19, 6, 8, 8, 23, 23, 19, 19, 19, 23, 23, 23, 23, 32, 19, 19, 36, 36, 23, 32, 32, 32, 41, 36, 36, 36, 45, 32, 41, 41, 36, 36, 45, 45, 45, 45, 41]

    #Solução ótima para a instância 49_14
    #x_matriz = 7
    #y_matriz = 7
    #equipamentos = [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0]
    #coberturas =[0, 0, 3, 3, 3, 6, 6, 0, 15, 10, 10, 10, 13, 13, 15, 15, 15, 18, 18, 18, 13, 28, 15, 30, 25, 25, 25, 34, 28, 28, 30, 30, 25, 34, 34, 28, 43, 38, 38, 38, 47, 34, 43, 43, 43, 38, 47, 47, 47]

    #Melhor solução encontrada para a instância 80_16
    #x_matriz = 8
    #y_matriz = 10
    #equipamentos = [0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
    #coberturas = [11, 11, 3, 3, 3, 3, 6, 6, 9, 9, 11, 11, 11, 23, 14, 14, 16, 16, 28, 28, 30, 11, 23, 23, 23, 23, 36, 28, 28, 28, 30, 30, 30, 23, 36, 36, 36, 36, 28, 28, 30, 42, 42, 42, 45, 45, 45, 45, 58, 58, 61, 61, 42, 64, 64, 45, 58, 58, 58, 58, 61, 61, 61, 64, 64, 64, 64, 77, 58, 58, 61, 61, 61, 64, 64, 64, 77, 77, 77, 77]

    #Melhor solução encontrada para a instância 80_24
    #x_matriz = 8
    #y_matriz = 10
    #equipamentos = [0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0]
    #coberturas = [2, 2, 2, 2, 2, 5, 6, 7, 8, 9, 12, 12, 12, 12, 12, 15, 16, 17, 18, 29, 31, 31, 23, 23, 23, 26, 26, 26, 29, 29, 31, 31, 31, 23, 35, 35, 26, 35, 48, 29, 51, 51, 43, 43, 43, 35, 56, 48, 48, 48, 51, 51, 51, 51, 64, 56, 56, 56, 48, 48, 70, 51, 64, 64, 64, 64, 64, 68, 68, 68, 70, 70, 70, 64, 64, 77, 77, 77, 77, 77]

    #Melhor solução encontrada para a instância 90_18
    #x_matriz = 9
    #y_matriz = 10
    #equipamentos = [0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0]
    #coberturas = [1, 1, 1, 4, 4, 4, 7, 7, 9, 9, 1, 1, 22, 14, 14, 14, 17, 17, 28, 28, 22, 22, 22, 22, 24, 24, 28, 28, 28, 28, 41, 41, 22, 34, 34, 34, 34, 47, 28, 28, 41, 41, 41, 41, 34, 47, 47, 47, 47, 47, 41, 41, 62, 54, 54, 54, 54, 47, 68, 68, 62, 62, 62, 62, 62, 75, 68, 68, 68, 68, 81, 81, 62, 75, 75, 75, 75, 87, 68, 68, 81, 81, 81, 81, 75, 75, 87, 87, 87, 87]

    #Melhor solução encontrada para a instância 90_27
    #x_matriz = 9
    #y_matriz = 10
    #equipamentos = [0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
    #coberturas = [2, 2, 2, 2, 2, 5, 6, 7, 8, 9, 12, 12, 12, 12, 12, 15, 16, 17, 18, 29, 22, 22, 22, 22, 22, 26, 26, 26, 29, 29, 41, 41, 33, 33, 33, 36, 36, 36, 48, 29, 41, 41, 41, 33, 54, 55, 36, 48, 48, 48, 51, 51, 51, 54, 54, 55, 55, 67, 48, 48, 51, 51, 72, 65, 65, 65, 67, 67, 67, 67, 72, 72, 72, 72, 72, 65, 86, 78, 78, 78, 82, 82, 82, 82, 86, 86, 86, 86, 78, 78]

    #Melhor solução encontrada para a instância 100_20
    x_matriz = 10
    y_matriz = 10
    equipamentos = [0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
    coberturas = [11, 11, 3, 3, 3, 5, 16, 17, 9, 9, 11, 11, 11, 3, 3, 5, 16, 17, 28, 28, 30, 11, 33, 33, 33, 35, 16, 28, 28, 28, 30, 30, 33, 33, 33, 35, 35, 47, 28, 28, 30, 51, 43, 43, 43, 35, 47, 47, 47, 47, 51, 51, 51, 43, 43, 65, 47, 47, 68, 68, 51, 51, 72, 72, 65, 65, 65, 68, 68, 68, 72, 72, 72, 72, 72, 77, 77, 77, 68, 68, 91, 91, 72, 85, 85, 85, 85, 88, 88, 88, 91, 91, 91, 91, 85, 85, 85, 88, 88, 88]

    #Melhor solução encontrada para a instância 100_30
    x_matriz = 10
    y_matriz = 10
    equipamentos = [0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0]
    coberturas = [11, 11, 3, 3, 3, 5, 6, 7, 8, 9, 11, 11, 11, 23, 11, 15, 16, 17, 18, 29, 21, 21, 21, 23, 23, 26, 26, 26, 29, 29, 40, 21, 33, 33, 33, 37, 37, 37, 37, 29, 40, 40, 40, 53, 54, 46, 46, 46, 58, 58, 40, 61, 53, 53, 54, 54, 46, 58, 58, 58, 61, 61, 61, 63, 63, 63, 76, 58, 58, 79, 61, 61, 61, 63, 84, 76, 76, 76, 79, 79, 81, 81, 81, 84, 84, 84, 76, 97, 97, 79, 81, 81, 92, 92, 84, 97, 97, 97, 97, 97]
    
    gerar_figura(x_matriz, y_matriz, equipamentos, coberturas)

