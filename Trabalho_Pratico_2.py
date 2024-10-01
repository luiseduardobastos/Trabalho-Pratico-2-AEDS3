import csv
import networkx as nx

# Função para ler o arquivo CSV e construir o grafo direcionado com nomes e dependências
def construir_grafo(arquivo_csv):
    G = nx.DiGraph()

    # Abrir o arquivo CSV
    with open(arquivo_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)  # Lê o arquivo como dicionário

        # Percorrer as linhas do CSV
        for row in reader:
            tarefa = row['Nome']  # Nome da tarefa (ou disciplina)
            codigo = row['Código']  # Código da tarefa (usado como identificador)
            dependencias = row['Dependências'].split(';') if row['Dependências'] else []  # Dependências da tarefa

            G.add_node(codigo, nome=tarefa)  # Adiciona o nó (disciplina) ao grafo

            # Para cada dependência, adiciona uma aresta de peso 1
            for dep in dependencias:
                G.add_edge(dep, codigo, peso=1)

    return G  # Retorna o grafo construído

# Função que implementa o algoritmo de Bellman-Ford
def bellman_ford(grafo, inicio):
    # Inicializa as distâncias de todos os nós como -infinito, exceto o nó de início
    dist = {nodo: float('-inf') for nodo in grafo}
    dist[inicio] = 0
    predecessor = {nodo: None for nodo in grafo}

    # Verifica as arestas repetidamente (|V| - 1 vezes)
    for _ in range(len(grafo) - 1):
        for u, v, dados in grafo.edges(data=True):
            peso = dados.get('peso', 1)
            if dist[u] + peso > dist[v]:
                dist[v] = dist[u] + peso
                predecessor[v] = u

    return dist, predecessor  # Retorna distâncias e predecessores

# Função para reconstruir o caminho crítico a partir dos predecessores
def reconstruir_caminho(predecessor, nodo_fim):
    caminho = []
    while nodo_fim:
        caminho.insert(0, nodo_fim)
        nodo_fim = predecessor[nodo_fim]
    return caminho  # Retorna o caminho na ordem correta

# Função principal para calcular o caminho crítico
def calcular_caminho_critico(grafo):
    # Encontrar o(s) nó(s) de início (sem predecessores)
    inicio = [n for n, d in grafo.in_degree() if d == 0]

    if not inicio:  # Se não houver nós de início, lança erro
        raise Exception("Nenhum nodo de início encontrado.")

    # Variáveis para armazenar o caminho crítico e sua duração máxima
    caminho_critico = []
    duracao_maxima = 0

    # Aplica o algoritmo de Bellman-Ford para cada nodo inicial
    for nodo_inicial in inicio:
        dist, predecessor = bellman_ford(grafo, nodo_inicial)

        # Encontrar o nodo com a maior distância (fim do caminho crítico)
        nodo_fim = max(dist, key=dist.get)
        if dist[nodo_fim] > duracao_maxima:
            duracao_maxima = dist[nodo_fim]  # Atualiza a duração máxima
            caminho_critico = reconstruir_caminho(predecessor, nodo_fim)  # Reconstrói o caminho crítico

    # Mapeia os códigos dos nós para seus nomes
    caminho_com_nomes = [grafo.nodes[n]['nome'] for n in caminho_critico]

    return caminho_com_nomes, duracao_maxima + 1

# Função principal que interage com o usuário
def main():
    while True:
        # Pede o caminho do arquivo CSV
        arquivo = input("Informe o caminho do arquivo CSV (0 para sair): ").strip()
        if arquivo == '0':
            print("Encerrando o programa.")
            break

        try:
            print("Processando...")
            grafo = construir_grafo(arquivo)  # Constrói o grafo a partir do arquivo CSV
            caminho, duracao = calcular_caminho_critico(grafo)  # Calcula o caminho crítico

            if caminho:
                print("\nCaminho Crítico:")
                for tarefa in caminho:
                    print(f"- {tarefa}")
                print(f"\nTempo Mínimo: {duracao}\n")
            else:
                print("Não foi possível calcular o caminho crítico.")

        except FileNotFoundError:
            print(f"\nErro: Arquivo '{arquivo}' não encontrado.\n")
        except Exception as e:
            print(f"Ocorreu um erro: {str(e)}")

if __name__ == "__main__":
    main()