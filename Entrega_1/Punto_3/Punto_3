from collections import deque 

class Node:
    def __init__(self,state, parent=None,action=None,path_cost=0):
        self.state = state
        self.parent = parent
        self.action= action
    def __lt__(self,other):
        return self.path_cost < other.path_cost
        
    
    def expand(problem, node):
        s = node.state 
        for action in problem.actions(s):
            s_prime = problem.result(s, action) 
            yield Node(state=s_prime, parent=node, action=action) 
            
class Problem:
       def __init__(self, initial, goal, actions, result, is_goal):
        self.initial = initial #Estado inicial
        self.goal = goal #Estado objetivo
        self.actions = actions #acciones disponibles desde un estado.
        self.result = result  #estado resultante de aplicar una acción
        self.is_goal = is_goal #verificación de si el estado es el estado objetivo     
        
def problem_metro():
    initial = 'Estacion A'
    goal = 'Estacion J'
    actions= {
        'Estacion A' : ['Estacion B','Estacion C'],
        'Estacion B' : ['Estacion A','Estacion D','Estacion E'],
        'Estacion C' : ['Estacion A', 'Estacion F'],
        'Estacion D' : ['Estacion B','Estacion G'],
        'Estacion E' : ['Estacion B','Estacion H','Estacion I'],
        'Estacion F' : ['Estacion C','Estacion J'],
        'Estacion G' : ['Estacion D'],
        'Estacion H' : ['Estacion E'],
        'Estacion I' : ['Estacion E','Estacion J'],
        'Estacion J' : ['Estacion F','Estacion I']
        }
    def result(state,action):
        return action
    def is_goal(state):
        return state == goal
    
    def breadth_first_search(problem):
        node = Node(problem.initial)
        if problem.is_goal(node.state):
            return node
        frontier = deque([node])
        explored = set()
        while frontier:
            node = frontier.popleft()
            explored.add(node.state)
            for child in Node.expand(problem,node):
                if child.state not in explored and all(child.state != n.state for n in frontier):
                    if problem.is_goal(child.state):
                        return child
                    frontier.append(child)
        return None
    
    def depth_limited_search(problem, limit):
        def recursive_dls(node, problem, limit):
            if problem.is_goal(node.state):
                return node
            elif limit == 0:
                return None
            else:
                for child in Node.expand(problem, node):
                    result = recursive_dls(child, problem, limit-1)
                    if result:
                        return result
                return None
        return recursive_dls(Node(problem.initial), problem, limit)

    def iterative_deepening_search(problem):
        depth = 0
        while True:
            result = depth_limited_search(problem, depth)
            if result:
                return result
            depth += 1
  
    problem = Problem(initial, goal, lambda s: actions.get(s,[]), result, is_goal)
    solution = breadth_first_search(problem)
  

    if solution:
        path = []
        while solution:
            path.append(solution.state)
            solution = solution.parent
        path.reverse()
        print("Ruta encontrada:", path)
    else:
        print("Ruta no encontrada")
        
    solution_ids = iterative_deepening_search(problem)
    if solution_ids:
        path_ids = []
        while solution_ids:
            path_ids.append(solution_ids.state)
            solution_ids = solution_ids.parent
        path_ids.reverse()
        print("Ruta encontrada por IDS:", path_ids)
    else:
        print("Ruta no encontrada por IDS")
      
problem_metro()
