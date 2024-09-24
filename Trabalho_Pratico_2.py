import csv
import networkx as nx

# Função para ler o arquivo CSV e construir o grafo direcionado com nomes e dependências corretas
def construir_grafo(arquivo_csv):
    G = nx.DiGraph()

    with open(arquivo_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            tarefa = row['Nome']  # Nome da tarefa (disciplina)
            codigo = row['Código']  # Código da disciplina
            dependencias = row['Dependências'].split(';') if row['Dependências'] else []
            G.add_node(codigo, nome=tarefa)  # Adiciona o nó com o código da tarefa

            # Adicionar arestas com dependências
            for dep in dependencias:
                G.add_edge(dep, codigo)  # As arestas vão das dependências para a tarefa atual

    return G

# Função para calcular o caminho crítico e o tempo mínimo de conclusão
def caminho_critico(grafo):
    try:
        # Usar a função de caminho mais longo
        caminho_critico = nx.dag_longest_path(grafo)
        duracao_caminho_critico = len(caminho_critico)  # Considerar que cada tarefa demora 1 unidade de tempo

        # Obter os nomes das tarefas no caminho crítico
        caminho_com_nomes = [grafo.nodes[n]['nome'] for n in caminho_critico]

        return caminho_com_nomes, duracao_caminho_critico
    except nx.NetworkXUnfeasible:
        return None, 0  # Grafo tem ciclos, não é possível calcular o caminho crítico

# Função principal para interação com o usuário
def main():
    while True:
        arquivo = input("Informe o caminho do arquivo CSV (0 para sair): ").strip()
        if arquivo == '0':
            print("Encerrando o programa.")
            break

        try:
            print("Processando...")
            grafo = construir_grafo(arquivo)
            caminho, duracao = caminho_critico(grafo)

            if caminho:
                print("\nCaminho Crítico:")
                for tarefa in caminho:
                    print(f"- {tarefa}")
                print(f"\nTempo Mínimo: {duracao}\n")
            else:
                print("Não foi possível calcular o caminho crítico (grafo inválido).")

        except FileNotFoundError:
            print(f"\nErro: Arquivo '{arquivo}' não encontrado.\n")
        except Exception as e:
            print(f"Ocorreu um erro: {str(e)}")

# Para rodar o programa
main()