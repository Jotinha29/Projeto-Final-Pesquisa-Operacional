import numpy as np

def tsp_nearest_neighbor(distance_matrix):
    n = len(distance_matrix)
    visited = [False] * n
    path = [0]
    visited[0] = True
    total_distance = 0

    print(f"Iniciando na cidade A (índice 0).")

    for _ in range(n - 1):
        current_city = path[-1]
        print(f"\nCidade atual: {current_city} (Índice: {current_city})")
        print(f"Visitados: {visited}")
        
        nearest_city = None
        min_distance = float('inf')

        for city in range(n):
            if not visited[city]:
                print(f" - Avaliando cidade {city} (Distância: {distance_matrix[current_city][city]})")
                if distance_matrix[current_city][city] < min_distance:
                    nearest_city = city
                    min_distance = distance_matrix[current_city][city]
                    print(f"   -> Atualizando cidade mais próxima: {nearest_city} com distância {min_distance}")

        path.append(nearest_city)
        visited[nearest_city] = True
        total_distance += min_distance
        print(f"Selecionada cidade {nearest_city} com distância {min_distance}. Caminho atual: {path}")
        print(f"Distância total até agora: {total_distance} km")

    total_distance += distance_matrix[path[-1]][path[0]]
    print(f"\nRetornando à cidade inicial (A). Distância de {path[-1]} para 0: {distance_matrix[path[-1]][path[0]]} km")
    path.append(0)

    print(f"\nCaminho completo: {path}")
    print(f"Distância total final: {total_distance} km\n")

    return path, total_distance


distance_matrix = [
    [0, 10, 15, 30, 15],
    [10, 0, 20, 25, 15],
    [15, 20, 0, 10, 30],
    [30, 25, 10, 0, 15],
    [15, 15, 30, 15, 0]
]

path, total_distance = tsp_nearest_neighbor(distance_matrix)
print("Resultado Final:")
print("Caminho percorrido:", " -> ".join(["A", "B", "C", "D", "E"][i] for i in path))
print("Distância total:", total_distance, "km")
