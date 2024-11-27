# Otimização de Rotas para Transporte de Equipes (TSP)

Este projeto resolve o problema de otimização de rotas no contexto de transporte de equipes de uma empresa. Baseia-se no **Problema do Caixeiro Viajante (TSP)** e utiliza técnicas de programação linear e heurísticas para minimizar a distância total percorrida, respeitando restrições como autonomia de veículo e capacidade.

---

## **Problema**

A empresa disponibiliza transporte para seus funcionários, com equipes divididas em grupos que precisam ser transportados diariamente. Cada grupo parte da sede da empresa em Brasília e passa por várias localidades, retornando à sede ao final da rota.

### **Requisitos**
1. Minimizar a distância total percorrida.
2. Respeitar a autonomia do veículo (100 km por carga).
3. Considerar a capacidade máxima de 5 passageiros por rota.
4. Exibir horários de saída e chegada para cada etapa da rota.

---

## **Tecnologias Utilizadas**
- **Python 3.9+**
- **Bibliotecas**:
  - `PuLP`: Para resolver o problema de programação linear.
  - `datetime`: Para manipulação de horários.
  - `random`: Para geração de horários de saída aleatórios.

---

## **Implementação**

O programa utiliza programação linear para resolver o TSP, criando uma rota otimizada que minimiza a soma das distâncias percorridas. Inclui funcionalidades como:

1. **Otimização da Rota**:
   Utiliza o solver do PuLP para determinar a rota com a menor distância.

2. **Cálculo de Horários**:
   Para cada etapa, calcula e exibe os horários de saída e chegada com base na distância e na velocidade média (40 km/h).

3. **Mensagens Descritivas**:
   Inclui mensagens detalhadas como:
   - "Saindo da empresa às X horas".
   - "Saindo de Y às X horas e chegando em Z às X horas".
   - "Chegando de volta à empresa às X horas".

---

## **Como Executar**

1. Instale as dependências:
   ```bash
   pip install pulp
2. py main.py
