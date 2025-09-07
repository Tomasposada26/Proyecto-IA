COMPARACIÓN DE BFS E IDS

4. Comparación: Tiempo y Memoria

 Algoritmo →  Ruta encontrada     →    Tiempo →  Memoria
 
 
 BFS        A → C → F → J       →       0.001686(s)   →     4.84kb   
 
 
 
 IDS        A → C → F → J     →         0.000142(s)   →     2.51kb       

5. Explicación de diferencias
1. Tiempo de ejecución:
   - IDS fue más rápido que BFS en este caso, porque la profundidad de la solución es baja.
   - BFS recorrió más nodos al explorar por niveles.

2. Consumo de memoria:
   - BFS consume más memoria al almacenar todos los nodos en la frontera.
   - IDS mantiene solo una rama en memoria, lo que reduce el consumo.

3. Estrategia de búsqueda:
   - BFS: Explora por niveles y garantiza la ruta más corta.
   - IDS: Combina búsqueda en profundidad limitada con iteraciones incrementales, también encuentra la ruta más corta pero repite nodos.

4. Conclusión:
   - En problemas pequeños, IDS puede ser más rápido y usar menos memoria.
   - En problemas grandes, BFS puede volverse muy costoso en memoria, mientras que IDS mantiene bajo uso de memoria pero puede tardar más.
