# Búsqueda A* para Ruta Óptima en Rumania

Este proyecto implementa el algoritmo de búsqueda **A*** para encontrar la ruta óptima entre dos ciudades en Rumania. Utiliza un grafo de conexiones reales entre ciudades, incluyendo distancias de carretera y una heurística basada en distancias en línea recta (aéreas) hacia el destino.

## Análisis del Problema

El objetivo principal es encontrar el **camino de menor costo** (en kilómetros) desde una ciudad inicial hasta una ciudad destino. En este caso:

- **Estado inicial:** `'Arad'`
- **Estado objetivo:** `'Bucharest'`

La representación del problema incluye:
- Un conjunto de **acciones posibles** desde cada ciudad (movimientos entre nodos).
- Un **costo de acción** asociado a cada movimiento (distancia en km).
- Un **estado objetivo** que representa el destino deseado.
- Un **grafo dirigido** modelado como diccionario de adyacencias.

## Algoritmo A* Search

La búsqueda A* funciona como una mejora de la búsqueda de costo uniforme, al incluir una **heurística h(n)** que estima el costo desde el nodo actual hasta el objetivo. La función de evaluación es:
**f(n) = g(n) + h(n)**
Donde:
- `g(n)` es el costo del camino desde el nodo inicial hasta el nodo actual.
- `h(n)` es la estimación del costo restante (heurística).

Para este proyecto:
- `g(n)` se calcula acumulando los costos reales de los movimientos.
- `h(n)` es la **distancia aérea a Bucharest**, precalculada para cada ciudad.

El algoritmo explora los nodos en orden creciente de `f(n)`, priorizando los que parecen más prometedores tanto por el costo acumulado como por la estimación futura.

## ¿Por qué la ruta encontrada es óptima?

La ruta calculada por A* se considera **óptima** siempre que:

- La heurística utilizada sea **admisible** (nunca sobreestima el costo real restante).
- El grafo no tenga ciclos negativos o costos variables.

Dado que las distancias aéreas entre ciudades **son menores o iguales** a las reales, la heurística cumple la condición de admisibilidad.

En este caso, A* encuentra la ruta:
`['Arad', 'Sibiu', 'Fagaras', 'Bucharest']`

Con un costo total de 140 + 99 + 211 = **450 km**, que es el camino más corto posible entre las dos ciudades, según el grafo definido.

