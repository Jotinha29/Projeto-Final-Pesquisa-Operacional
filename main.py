from pulp import LpProblem, LpVariable, lpSum, LpMinimize, PULP_CBC_CMD
from datetime import datetime, timedelta
import random

# Dados dos funcionários e localidades
funcionarios = {
    1: "João (Samambaia)",
    2: "Gabriel (Valparaíso)",
    3: "Ryann (Taguatinga)",
    4: "Victor (Ceilândia)",
    5: "Guilherme (São Sebastião)",
    6: "Gustavo (Gama)",
    7: "Zé (Paranoá)",
    8: "Duda (Sobradinho)",
    9: "Matheus (Ceilândia)",
    10: "Enzo (Águas Claras)",
    11: "Braz (Brazlândia)"
}

# Equipes de trabalho divididas em grupos
equipes = {
    "Equipe 1 - Grupo 1": [1, 2, 3, 7, 8],
    "Equipe 1 - Grupo 2": [9],
    "Equipe 2 - Grupo 1": [4, 5, 6, 10],
    "Equipe 2 - Grupo 2": [11]
}

# Matriz de distâncias atualizada com Brazlândia
distancias = [
    [0, 30, 24, 26, 28, 36, 32, 25, 22, 20, 45, 50],  # Brasília
    [30, 0, 8, 10, 34, 20, 12, 40, 42, 6, 50, 55],    # Samambaia
    [24, 8, 0, 6, 32, 22, 14, 35, 38, 4, 46, 52],     # Taguatinga
    [26, 10, 6, 0, 35, 25, 16, 38, 40, 10, 44, 50],   # Ceilândia
    [28, 34, 32, 35, 0, 18, 20, 30, 25, 32, 60, 65],  # São Sebastião
    [36, 20, 22, 25, 18, 0, 12, 42, 44, 26, 48, 55],  # Valparaíso
    [32, 12, 14, 16, 20, 12, 0, 45, 46, 18, 42, 50],  # Gama
    [25, 40, 35, 38, 30, 42, 45, 0, 12, 36, 55, 60],  # Paranoá
    [22, 42, 38, 40, 25, 44, 46, 12, 0, 40, 57, 62],  # Sobradinho
    [20, 6, 4, 10, 32, 26, 18, 36, 40, 0, 44, 50],    # Águas Claras
    [45, 50, 46, 44, 60, 48, 42, 55, 57, 44, 0, 10],  # Brazlândia
    [50, 55, 52, 50, 65, 55, 50, 60, 62, 50, 10, 0]   # Brazlândia
]

# Função para resolver a rota com minimização da distância
def resolver_otimizacao(equipe, distancias, velocidade_media=40):
    n = len(distancias)
    cidades = [0] + equipe  # Inclui Brasília (0) e as cidades da equipe

    # Problema de Minimização
    problema = LpProblem("Minimizar_Distancia", LpMinimize)

    # Variáveis de decisão
    rota = LpVariable.dicts("Rota", [(i, j) for i in cidades for j in cidades if i != j], 0, 1, cat='Binary')

    # Função objetivo: minimizar a soma das distâncias
    problema += lpSum(rota[i, j] * distancias[i][j] for i in cidades for j in cidades if i != j)

    # Restrição 1: Cada cidade deve ser visitada exatamente uma vez
    for i in cidades:
        problema += lpSum(rota[i, j] for j in cidades if j != i) == 1
        problema += lpSum(rota[j, i] for j in cidades if j != i) == 1

    # Restrição 2: Subtours não são permitidos (eliminação de ciclos)
    u = LpVariable.dicts("u", cidades, 0, len(cidades) - 1, cat='Integer')
    for i in cidades[1:]:
        for j in cidades[1:]:
            if i != j:
                problema += u[i] - u[j] + len(cidades) * rota[i, j] <= len(cidades) - 1

    # Resolvendo o problema
    problema.solve(PULP_CBC_CMD(msg=0))

    # Extraindo a solução
    rota_final = []
    for i in cidades:
        for j in cidades:
            if i != j and rota[i, j].value() == 1:
                rota_final.append((i, j))

    # Ordenar a rota para exibição
    rota_ordenada = [0]
    while len(rota_ordenada) < len(cidades):
        for (i, j) in rota_final:
            if i == rota_ordenada[-1]:
                rota_ordenada.append(j)

    # Calcular a distância total
    distancia_total = sum(distancias[i][j] for i, j in zip(rota_ordenada[:-1], rota_ordenada[1:]))

    # Cálculo dos horários
    horario_atual = datetime.strptime(f"18:{random.randint(0, 59)}", "%H:%M")
    print(f"\nSaindo da empresa às {horario_atual.strftime('%H:%M')}")

    for i, j in zip(rota_ordenada[:-1], rota_ordenada[1:]):
        tempo_viagem = distancias[i][j] / velocidade_media
        horario_chegada = horario_atual + timedelta(hours=tempo_viagem)
        print(f"Saindo de {funcionarios.get(i, 'a empresa')} às {horario_atual.strftime('%H:%M')} e chegando em {funcionarios.get(j, 'a empresa')} às {horario_chegada.strftime('%H:%M')}")
        horario_atual = horario_chegada

    print(f"Chegando de volta à empresa às {horario_atual.strftime('%H:%M')}")

    return rota_ordenada, distancia_total

# Calculando rotas otimizadas para cada equipe
for equipe, trabalhadores in equipes.items():
    print(f"\n{equipe}:")
    rota, distancia = resolver_otimizacao(trabalhadores, distancias)
    rota_nomes = [funcionarios.get(cidade, "Brasília") for cidade in rota]
    print("Rota:", " -> ".join(rota_nomes))
    print(f"Distância total percorrida: {distancia} km")
