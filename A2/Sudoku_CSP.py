import queue
import sys
import copy

fullDomain = "123456789"

class cell:
    def __init__(self, row, col, value):
        self.row = row
        self.col = col
        self.value = value

class CSP:
    def __init__(self, inp):
        self.variables = [r + c for r in 'ABCDEFGHI' for c in '123456789']
        self.domain = dict((self.variables[i], fullDomain if inp[i] == '0' else inp[i]) for i in range(len(inp)))
        a = [self.colNeighbors(self.variables, i) for i in range(9)]
        b = [self.rowNeighbors(self.variables, i) for i in range(9)]
        c = [self.blockNeighbors(self.variables, i, j) for i in range(9) for j in range(9)]
        self.cells = (a + b + c)
        self.cellNeighbors = dict((s, [u for u in self.cells if s in u]) for s in self.variables)
        self.neighbors = dict((s, set(sum(self.cellNeighbors[s], [])) - set([s])) for s in self.variables)
        self.constraints = {(variable, neighbor) for variable in self.variables for neighbor in self.neighbors[variable]}

    def colNeighbors(self, b, col):
        neighbors = []
        for i in range(col, len(b), 9):
            neighbors.append(b[i])

        return neighbors

    def rowNeighbors(self, b, row):
        neighbors = []
        end = (row + 1) * 9
        start = end - 9
        for i in range(start, end, 1):
            neighbors.append(b[i])
        
        return neighbors

    def blockNeighbors(self, b, row, col):
        neighbors = []
        domRow = row - row % 3
        domCol = col - col % 3
        for j in range(3):
            for i in range(3):
                v = b[(j + domCol) + (i + domRow) * 9]
                neighbors.append(v)
            
        return neighbors

    def solved(self):
        for v in self.variables:
            if len(self.domain[v]) > 1:
                return False

        return True
    
    def printSudoku(self, values):
        print("SUDOKU:")
        dash = "------------"
        line = ""
        counter = 0
        domain = ''

        for var in self.variables:
            if len(values[var]) > 1:
                domain += '0'
            
            else:
                domain += str(values[var]) 

        for i in range(9):
            if (i % 3 == 0):
                print(dash)
            
            for j in range(9):
                if (j % 3) == 0:
                    line += '|'
                
                line += domain[counter]
                counter += 1
            
            print(line + '|')
            line = ''
        print(dash)
    
    def consistent(self, assignment, var, val):
        for neighbor in self.neighbors[var]:
            if neighbor in assignment.keys() and assignment[neighbor] == val:
                return False
        
        return True

def AC3(csp):
    q = queue.Queue()

    for arc in csp.constraints:
        q.put(arc)

    while not q.empty():
        (Xi, Xj) = q.get()

        if Revise(csp, Xi, Xj):
            if len(csp.domain[Xi]) == 0:
                return False
            
            for Xk in (csp.neighbors[Xi] - set(Xj)):
                q.put((Xk, Xi))

    return True

def Revise(csp, Xi, Xj):
    revised = False
    values = set(csp.domain[Xi])
    
    for x in values:
        if not isConsistent(csp, x, Xi, Xj):
            csp.domain[Xi] = csp.domain[Xi].replace(x, '')
            revised = True

    return revised

def isConsistent(csp, x, Xi, Xj):
    for y in csp.domain[Xj]:
        if Xj in csp.neighbors[Xi] and y != x:
            return True
    
    return False

def backtrack(assignment, csp):
    if set(assignment.keys()) == set(csp.variables):
        return assignment
    
    var = select_unassigned_variable(assignment, csp)
    domain = copy.deepcopy(csp.domain)
    
    for val in csp.domain[var]:
        if csp.consistent(assignment, var, val):
            assignment[var] = val
            inferences = {}
            inferences = Inference(assignment, inferences, csp, var, val)

            if inferences != "Fail":
                result = backtrack(assignment, csp)

                if result != "Fail":
                    return result
            
            del assignment[var]
            csp.domain.update(domain)

    return "Fail"

def select_unassigned_variable(assignment, csp):
    unassigned_vars = dict((cell, len(csp.domain[cell])) for cell in csp.domain if cell not in assignment.keys())
    return min(unassigned_vars, key=unassigned_vars.get)

def Inference(assignment, inferences, csp, var, val):
    inferences[var] = val
    
    for neighbor in csp.neighbors[var]:
        if neighbor not in assignment and val in csp.domain[neighbor]:
            if len(csp.domain[neighbor]) == 1:
                return "Fail"
            
            remaining = csp.domain[neighbor] = csp.domain[neighbor].replace(val, "")

            if len(remaining) == 1:
                flag = Inference(assignment, inferences, csp, neighbor, remaining)

                if flag == "Fail":
                    return "Fail"
    
    return inferences 

csp = CSP('003020600900305001001806400008102900700000008006708200002609500800203009005010300')

if AC3(csp):
    if csp.solved():
        print("----USING AC3----")
        csp.printSudoku(csp.domain)

    else:
        print("----USING BACKTRACKING----")
        sudoku = backtrack({}, csp)
        if sudoku == "Fail":
            print("Unsolvable")
        
        else:
            csp.printSudoku(sudoku)
