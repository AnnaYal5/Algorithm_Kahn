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

    

