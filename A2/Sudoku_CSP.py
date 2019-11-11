import queue
import sys
import math

fullDomain = [1, 2, 3, 4, 5, 6, 7, 8, 9]

class cell:
    def __init__(self, row, col, value):
        self.row = row
        self.col = col
        self.value = value

class CSP:
    def __init__(self, inp):
        self.variables = [r + c for r in 'ABCDEFGHI' for c in '123456789']
        self.domain = dict((self.variables[i], fullDomain if inp[i] == '0' else [int(inp[i])]) for i in range(len(inp)))
        a = [self.colNeighbors(self.variables, i) for i in range(9)]
        b = [self.rowNeighbors(self.variables, i) for i in range(9)]
        c = [self.blockNeighbors(self.variables, i, j) for i in range(9) for j in range(9)]
        self.cells = (a + b + c)
        
        self.cellNeighbors = dict((s, [u for u in self.cells if s in u]) for s in self.variables)
        self.neighbors = dict((s, set(sum(self.cellNeighbors[s], [])) - set([s])) for s in self.variables)
        self.constraints = [(variable, neighbor) for variable in self.variables for neighbor in self.neighbors[variable]]
        
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
            if len(self.domain[v]) == 1:
                return False

        return True


def AC3(csp):
    q = queue.Queue()

    for arc in csp.constraints:
        q.put(arc)

    while not q.empty():
        Xi, Xj = q.get()

        if Revise(csp, Xi, Xj):
            if len(csp.domain[Xi]) == 0:
                return False
            
            for Xk in (csp.neighbors[Xi] - set(Xj)):
                q.put((Xk, Xi))

    return True

def Revise(csp, Xi, Xj):
    revised = False
    i = 0

    for x in csp.domain[Xi]:
        invalid = True

        for y in csp.domain[Xj]:
            if x != y:
                invalid = False
        
        if invalid:
            csp.domain[Xi].pop(i)
            revised = True
        
        else:
            i += 1

    return revised

csp = CSP('003020600900305001001806400008102900700000008006708200002609500800203009005010300')
print(AC3(csp))
print(csp.solved())
