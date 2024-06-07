import numpy as np
import matplotlib.pyplot as plt

largura = 230
altura = 190

fig, ax = plt.subplots()
retangulo = plt.Rectangle((0, 0), largura, altura, edgecolor='black', facecolor='none')
ax.add_patch(retangulo)

num_pontos_x = 10
num_pontos_y = 10

# Adicionar uma imagem de fundo ao retângulo
img = plt.imread('C://Users//11835692974//Downloads//WhatsApp Image 2024-06-05 at 17.08.31.jpeg')
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

# Salvar a matriz de distâncias em um arquivo de texto
print(len(distancias_manhattan))
with open('distancias_manhattan2.txt', 'w') as f:
    for linha in range(len(distancias_manhattan)):
        for coluna in range(len(distancias_manhattan[linha])):
            f.write(str(linha) + " " + str(coluna) + " " + str(distancias_manhattan[linha, coluna]) + "\n")

# Plotar os pontos do grid na figura
ax.plot(pontos_grid[:, 0], pontos_grid[:, 1], 'bo', markersize=5)

# Adicionar rótulos aos eixos
ax.set_xlabel('X (metros)')
ax.set_ylabel('Y (metros)')

# Salvar a figura com os pontos
plt.savefig('retangulo_com_grid_manhattan.png')

# Imprimir a coordenada de cada ponto no console
for ponto in pontos_grid:
    print(f'Coordenada: {ponto}')

# Mostrar a figura
plt.show()
