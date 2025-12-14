import random
import time
import matplotlib.pyplot as plt
import csv
import os
import sys
import itertools

def generate_graph(n, density):
    adj_list = {k: [] for k in range(1, n + 1)}
    max_edges = n * (n - 1) // 2
    target_edges = int(density * max_edges / 100)
    possible_edges = list(itertools.combinations(range(1, n + 1), 2))
    chosen_edges = random.sample(possible_edges, target_edges)
    
    for u, v in chosen_edges:
        adj_list[u].append(v)
        
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

        i_index = n - 1
        for v_index in range(i):
            if matrix[i_index][v_index] == 1:
                in_degree[v_index] -= 1
                if in_degree[v_index] == 0:
                    queue.append(v_index + 1)
    
    return sorted_list

def experiments():
    Sizes = [20, 40, 60, 80, 100, 120, 140, 160, 180, 200]
    Densities = [10, 30, 50, 70, 90]
    Repetitions = 25

    result = []

    algorithms = [("Список суміжності", algorithm_Kahn_list),
                   ("Матриця суміжності", algorithm_Kahn_matrix)]
    
    for represent, algorithm_func in algorithms:
        print(f"\n Експерименти: {represent}")

        for i in Sizes:
            for density in Densities:

                total_time = 0.0
                for _ in range(Repetitions):
                    adj_list = generate_graph(i, density)
                    start_time = time.time()
                    algorithm_func(i, adj_list)
                    end_time = time.time()
                    total_time += (end_time - start_time) * 1000
                avg_time = total_time / Repetitions

                result.append({
                    "Представлення": represent,
                    "Вершини": i,
                    "Щільність": density,
                    "Середній час": avg_time
                })

                print(f" n={i:<3}, d={density}%: {avg_time:.6f} ms")
    
    return result

def save_to_csv(results):
    if not results:
        print("Немає даних для запису!")
        return
    
    script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    csv_file_name = "results.csv"
    full_path = os.path.join(csv_file_name)
    print(full_path)

    with open(full_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["Представлення", "Вершини", "Щільність", "Середній час"]
        )
        writer.writeheader()
        for row in results:
            writer.writerow(row)

def plot_graphs(results):
    densities = [10, 30, 50, 70, 90]

    script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

    for density in densities:
        plt.figure()
        for represent in ["Список суміжності", "Матриця суміжності"]:
            x = []
            y = []
            for r in results:
                if r["Щільність"] == density and r["Представлення"] == represent:
                    x.append(r["Вершини"])
                    y.append(r["Середній час"])
            plt.plot(x, y, label=represent)
        plt.xlabel("Кількість вершин")
        plt.ylabel("Час виконання (мс)")
        plt.title(f"Щільність графу {density}%")
        plt.legend()
        plt.grid(True)
        file_name = f"graph_density_{density}%.png"
        full_path = os.path.join(script_dir, file_name)
        plt.savefig(full_path) 
        plt.close()
        print(f":white_check_mark: Збережено графік: {full_path}")
    print(":white_check_mark: Усі графіки та файл CSV збережено!")

if __name__ == "__main__":
    results = experiments()
    save_to_csv(results)
    plot_graphs(results)
    print("\n--- Зібрані результати (повний список) ---")
    for r in results:
        print(f"[{r['Представлення']:<20}] N={r['Вершини']:<4} D={r['Щільність']:<3}%: {r['Середній час']:.6f} ms")