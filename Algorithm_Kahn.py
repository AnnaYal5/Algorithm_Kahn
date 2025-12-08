import random
import time

def generate_graph(i, density):
    adj_list = {k: [] for k in range(i + 1)} # Словник для Списку Суміжності. Кожна вершина (від 1 до n) має порожній список сусідів.
    max_edges = i * (i - 1) # Максимально можлива кількість ребер.
    target_edges = int(density * max_edges / 100) # Цільова кількість ребер, необхідна для досягнення заданої щільності (density).
    current_edges = 0

    while current_edges < target_edges:
        k = random.randint(1, i - 1)
        l = random.randint(k + 1, i)

    if l not in adj_list[k]:
        adj_list[k].append(l)
        current_edges += 1
        
    return adj_list


def algorithm_Kahn_list(i, adj_list):
    in_degree = {k: 0 for k in range(1, i + 1)} # Словник для зберігання вхідного степеня (кількість ребер, які входять в конкретну вершину) кожної вершини.
    for n in adj_list:
        for v in adj_list[n]:
            in_degree[v] += 1
    
    queue = [k for k in range(1, i + 1) if in_degree[k] == 0] # Вершини в які не входять ребра, тобто початкові
    sorted_list = []

    while len(queue) > 0: # Цикл продовжується, поки у нас є вершини, готові до обробки (тобто ті, що не мають необроблених вхідних ребер).
        n = queue.pop(0)
        sorted_list.append(n)

        for v in adj_list.get(n, []): # Проходимося по всіх сусідах v вершини n. Це імітує видалення всіх вихідних ребер вершини n.
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
        
    return sorted_list


def algorithm_Kahn_matrix(i, adj_list):
    matrix = [[0] * i for _ in range(i)] # Створюємо порожню матрицю n x n, заповнену нулями.
    for n, neighbors in adj_list.items():
        for v in neighbors:
            matrix[n - 1][v - 1] = 1

    in_degree = [0] * i # Ініціалізуємо список вхідних степенів (індекси від 0 до n-1).
    for l in range(i):
        for k in range(i):
            in_degree[l] += matrix[k][l]
    
    queue = [k + 1 for k in range(i) if in_degree[k] == 0]
    sorted_list = []

    while len(queue) > 0:
        n = queue.pop(0)
        sorted_list.append(n)

        n_index = n - 1
        for v_index in range(n):
            if matrix[n_index][v_index] == 1:
                in_degree[v_index] -= 1
                if in_degree[v_index] == 0:
                    queue.append(v_index + 1)
    
    return sorted_list


    


