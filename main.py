from datetime import datetime, timedelta

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

# Variáveis de capacidade e autonomia do veículo
capacidade_passageiros = 5
autonomia_km = 80
velocidade_media = 60  # km/h

# Controle global do horário do carro
horario_atual = datetime.strptime("18:00", "%H:%M")

# Função para calcular sub-rotas com retornos à sede
def calcular_subrotas(cidades, distancias, autonomia_km, capacidade_passageiros):
    subrotas = []
    rota_atual = [0]  # Começa em Brasília (0)
    distancia_atual = 0
    passageiros_atual = 0

    for cidade in cidades:
        proxima_distancia = distancias[rota_atual[-1]][cidade]
        if (
            distancia_atual + proxima_distancia > autonomia_km or
            passageiros_atual >= capacidade_passageiros
        ):
            # Fechar sub-rota e voltar à sede
            rota_atual.append(0)  # Retorno à sede
            subrotas.append(rota_atual)
            rota_atual = [0, cidade]  # Nova sub-rota começando na sede
            distancia_atual = distancias[0][cidade]
            passageiros_atual = 1  # Primeiro passageiro da nova sub-rota
        else:
            # Continuar na rota atual
            rota_atual.append(cidade)
            distancia_atual += proxima_distancia
            passageiros_atual += 1

    # Adicionar última sub-rota
    if len(rota_atual) > 1:
        rota_atual.append(0)  # Garantir retorno à sede
        subrotas.append(rota_atual)

    return subrotas

# Função para calcular rotas e horários
def resolver_rotas(equipe, distancias, autonomia_km, capacidade_passageiros, velocidade_media):
    global horario_atual  # Usa o horário global do carro
    subrotas = calcular_subrotas(equipe, distancias, autonomia_km, capacidade_passageiros)
    resultado = []

    for idx, subrota in enumerate(subrotas):
        distancia_total = sum(distancias[subrota[i]][subrota[i + 1]] for i in range(len(subrota) - 1))
        print(f"\nInício da sub-rota às {horario_atual.strftime('%H:%M')}")

        for i in range(len(subrota) - 1):
            origem = subrota[i]
            destino = subrota[i + 1]
            tempo_viagem = distancias[origem][destino] / velocidade_media
            horario_chegada = horario_atual + timedelta(hours=tempo_viagem)
            print(f"Saindo de {funcionarios.get(origem, 'Brasília')} às {horario_atual.strftime('%H:%M')} e chegando em {funcionarios.get(destino, 'Brasília')} às {horario_chegada.strftime('%H:%M')}")
            horario_atual = horario_chegada

        print(f"Distância percorrida: {distancia_total} km")

        if idx < len(subrotas) - 1:  # Exibir mensagem entre sub-rotas
            print("\nVoltando para a empresa, para carregar o carro")

        resultado.append({
            "rota": subrota,
            "distancia": distancia_total,
            "horario_termino": horario_atual
        })

    return resultado

# Resolvendo as rotas para cada equipe
for equipe, trabalhadores in equipes.items():
    print(f"\n{equipe}:")
    rotas = resolver_rotas(trabalhadores, distancias, autonomia_km, capacidade_passageiros, velocidade_media)
    for i, rota in enumerate(rotas):
        nomes = [funcionarios.get(cidade, "Brasília") for cidade in rota["rota"]]
        print(f"Sub-rota {i + 1}: {' -> '.join(nomes)}")
        print(f"Distância percorrida: {rota['distancia']} km")
