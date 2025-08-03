# Proyecto: Resolución de Laberintos con Algoritmo de Búsqueda A*

Este proyecto implementa el algoritmo de búsqueda A* para encontrar la ruta más corta en un laberinto 2D. El objetivo es que un agente (robot) se mueva desde una posición inicial 'S' hasta una posición final 'E', evitando paredes '#'.

## 1. Estructura del Problema

El problema de resolución del laberinto se define formalmente como un problema de búsqueda, donde se establecen los siguientes componentes:

### 1.1. `Actions` (Acciones)

Las acciones disponibles para el agente son los movimientos ortogonales en el espacio 2D del laberinto. No se permiten movimientos diagonales. Las acciones se definen como un diccionario de desplazamientos:

* **'Up'**: `(-1, 0)` - Moverse una celda hacia arriba.
* **'Down'**: `(1, 0)` - Moverse una celda hacia abajo.
* **'Left'**: `(0, -1)` - Moverse una celda hacia la izquierda.
* **'Right'**: `(0, 1)` - Moverse una celda hacia la derecha.

### 1.2. `Result` (Resultado)

El resultado de una acción es el nuevo estado (posición) del agente. A partir de un estado actual `(x, y)` y una acción, el resultado es la nueva posición `(x + dx, y + dy)`. Sin embargo, esta acción solo es válida si:

1.  La nueva posición está dentro de los límites del laberinto.
2.  La nueva posición no es una pared (`#`).

Si una acción no es válida, el resultado es `None`, y el agente permanece en su posición actual.

### 1.3. `Action-Cost` (Costo de la Acción)

El costo de cada acción se define como una constante. En este problema, todas las acciones (arriba, abajo, izquierda, derecha) tienen el mismo costo:

* **Costo de la acción**: `1`

Este costo uniforme hace que el algoritmo busque el camino con el menor número de pasos, lo que se conoce como el camino más corto en términos de distancia discreta.

## 2. Análisis del Algoritmo A*

El algoritmo A* es una estrategia de búsqueda informada que utiliza una función de evaluación $f(n) = g(n) + h(n)$, donde:

* $g(n)$ es el costo del camino desde el nodo inicial hasta el nodo actual $n$.
* $h(n)$ es una heurística, una estimación del costo para llegar desde el nodo actual $n$ al nodo objetivo.

### 2.1. ¿Cómo cambia el comportamiento si cambiamos la función de costo?

El comportamiento del algoritmo A* depende directamente de la función de costo. El algoritmo busca minimizar la función de evaluación $f(n)$.

Si cambiamos la función de costo (`action-cost`):

* **Costo uniforme (actual):** Si todas las acciones tienen un costo de `1`, el algoritmo A* se comporta de manera muy similar a un algoritmo de Búsqueda del Camino Más Corto (Uniform-Cost Search), pero acelerado por la heurística. La solución encontrada será el camino con el menor número de pasos.
* **Costo variable:** Si las acciones tuvieran costos diferentes (por ejemplo, moverse a través de una celda de lodo costara `2`), el algoritmo buscaría el camino con el costo total más bajo, no necesariamente el camino con el menor número de pasos. Un camino más largo en términos de pasos podría ser preferible si está compuesto por acciones de bajo costo.

Un cambio en la heurística $h(n)$ también altera el comportamiento:
* **Heurística de Manhattan (actual):** Mide la distancia en líneas horizontales y verticales. Es **admisible** (nunca sobreestima el costo real) y **consistente** en este problema. Esto garantiza que A* encuentre la solución óptima.
* **Heurística de Euclides:** Mide la distancia en línea recta. Es admisible, pero no consistente en un grid con movimientos ortogonales, ya que un paso en el grid siempre tendrá una distancia real de `1`, pero la distancia euclidiana puede ser menor. Su uso puede ser menos eficiente si el camino óptimo no se acerca a una línea recta.

### 2.2. Múltiples Salidas en el Laberinto

Si hubiera múltiples salidas en el laberinto, el algoritmo A* encontraría la ruta más corta (o de menor costo) a **la primera salida que alcance**. El comportamiento del algoritmo no necesita una modificación sustancial si solo queremos encontrar la primera salida.

**Propuesta para encontrar la mejor salida:**

Para manejar esto, podemos modificar el algoritmo para que continúe la búsqueda incluso después de encontrar una salida.

1.  **Encontrar todas las salidas:** Se puede modificar el algoritmo para que, en lugar de terminar cuando se encuentra la primera salida, siga explorando hasta que la `frontier` (cola de prioridad) esté vacía.
2.  **Almacenar todas las soluciones:** Cada vez que el algoritmo encuentra una salida, almacena el camino y su costo total.
3.  **Seleccionar la mejor solución:** Una vez que la búsqueda termina, se puede seleccionar el camino almacenado con el costo total más bajo.

Esta estrategia asegura que, incluso si el algoritmo encuentra una salida "cercana" pero no óptima al principio, la búsqueda continuará para encontrar una solución de menor costo.

## 3. Modificación del Laberinto y Limitaciones

### 3.1. Laberinto con Múltiples Obstáculos

Se puede crear un laberinto más grande y con diferentes tipos de obstáculos. Por ejemplo, podríamos añadir `~` para representar agua o lodo, con un costo de movimiento más alto.

**Laberinto Ejemplo (con lodo `~`):**

maze_modified = [
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
    ["#", "S", "~", " ", "#", " ", " ", " ", " ", "#"],
    ["#", " ", "~", " ", "#", " ", "~", " ", "E", "#"],
    ["#", " ", " ", " ", "#", " ", "~", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#"]
]

Para manejar esto, la función action_cost debería ser modificada para devolver un valor diferente basado en el tipo de celda a la que se va a mover el agente.

### 3.2. Limitaciones del Algoritmo
A pesar de ser muy eficiente, el algoritmo A* tiene algunas limitaciones en este contexto:
1. **Espacio de Estados Abierto:** El algoritmo mantiene un conjunto de nodos reached y una cola de prioridad frontier. Para laberintos muy grandes y complejos, estos conjuntos pueden consumir una gran cantidad de memoria, llevando a un error de memoria (OutOfMemoryError).
2. **Heurística Subóptima:** Si la heurística no es admisible (es decir, sobreestima el costo real), el algoritmo A* no garantiza encontrar la solución óptima.
3. **No resuelve laberintos con ciclos infinitos:** Aunque improbable en un laberinto con un reached set, si la lógica fuera defectuosa, un laberinto con un ciclo sin salida podría teóricamente llevar a un bucle infinito. El uso de reached en A* mitiga esto.
4. **No es eficiente en todos los casos:** En laberintos muy densos o con caminos óptimos muy complejos, la búsqueda expande muchos nodos, y el rendimiento puede ser similar a un BFS (Breadth-First Search) con un costo de cómputo adicional por la heurística.