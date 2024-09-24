# Trabalho Pratico 2 - AEDS3

A gestão de um curso de graduação envolve diversas disciplinas com dependências entre si. Uma técnica amplamente utilizada para garantir que o prazo seja cumprido é o Método do Caminho Crítico. Este método identifica a sequência de matérias que, caso sofram atraso, afetariam o tempo total do curso. Este projeto visa automatizar a identificação do caminho crítico, dado um conjunto de disciplinas e suas dependências, utilizando algoritmos em grafos.

O problema pode ser modelado como um grafo direcionado, onde cada nó representa uma disciplina e as arestas indicam as dependências entre elas. O objetivo é calcular o caminho mais longo no grafo, que corresponde ao caminho crítico para conclusão do curso, e o tempo mínimo necessário para completar todas as disciplinas.

O projeto utiliza a biblioteca networkx para manipulação de grafos. O grafo é representado como um grafo direcionado, onde cada nó corresponde a uma disciplina e cada aresta a uma dependência entre disciplinas.
