import time

class State():
    def __init__(self, cLeft, mLeft, boat, cRight, mRight, parent):
        self.cLeft = cLeft
        self.mLeft = mLeft
        self.boat = boat
        self.cRight = cRight
        self.mRight = mRight
        self.parent = parent
        self.children = []

    def isGoal(self):
        if self.cLeft == 0 and self.mLeft == 0:
            return True

        else:
            return False
    
    def isValid(self):
        if self.cLeft >= 0 and self.cRight >= 0 \
            and self.mLeft >=0 and self.mRight >= 0 \
            and (self.mLeft == 0 or self.mLeft >= self.cLeft) \
            and (self.mRight == 0 or self.mRight >= self.cRight):
                return True

        else:
            return False
    
    def hasChildren(self):
        return len(self.children) > 0

def setStateChildren(cur_state):
    if cur_state.boat == 'left':
        # 1 3 left 2 0
        new_state = State(cur_state.cLeft, cur_state.mLeft - 2, 'right', cur_state.cRight, cur_state.mRight + 2, cur_state)
        # two missionaries cross
        if new_state.isValid():
            cur_state.children.append(new_state)
        
        new_state = State(cur_state.cLeft - 2, cur_state.mLeft, 'right', cur_state.cRight + 2, cur_state.mRight, cur_state)
        # two cannibals cross
        if new_state.isValid():
            cur_state.children.append(new_state)

        new_state = State(cur_state.cLeft - 1, cur_state.mLeft - 1, 'right', cur_state.cRight + 1, cur_state.mRight + 1, cur_state)
        # one missionary and one cannibal cross
        if new_state.isValid():
            cur_state.children.append(new_state)

        new_state = State(cur_state.cLeft, cur_state.mLeft - 1, 'right', cur_state.cRight, cur_state.mRight + 1, cur_state)
        # one missionary crosses
        if new_state.isValid():
            cur_state.children.append(new_state)

        new_state = State(cur_state.cLeft - 1, cur_state.mLeft, 'right', cur_state.cRight + 1, cur_state.mRight, cur_state)
        # one cannibal crosses
        if new_state.isValid():
            cur_state.children.append(new_state)

    if cur_state.boat == 'right':
        new_state = State(cur_state.cLeft, cur_state.mLeft + 2, 'left', cur_state.cRight, cur_state.mRight - 2, cur_state)
        # two missionaries cross
        if new_state.isValid():
            cur_state.children.append(new_state)
        
        new_state = State(cur_state.cLeft + 2, cur_state.mLeft, 'left', cur_state.cRight - 2, cur_state.mRight, cur_state)
        # two cannibals cross
        if new_state.isValid():
            cur_state.children.append(new_state)

        new_state = State(cur_state.cLeft + 1, cur_state.mLeft + 1, 'left', cur_state.cRight - 1, cur_state.mRight - 1, cur_state)
        # one missionary and one cannibal cross
        if new_state.isValid():
            cur_state.children.append(new_state)

        new_state = State(cur_state.cLeft, cur_state.mLeft + 1, 'left', cur_state.cRight, cur_state.mRight - 1, cur_state)
        # one missionary crosses
        if new_state.isValid():
            cur_state.children.append(new_state)

        new_state = State(cur_state.cLeft + 1, cur_state.mLeft, 'left', cur_state.cRight - 1, cur_state.mRight, cur_state)
        # one cannibal crosses
        if new_state.isValid():
            cur_state.children.append(new_state)

    return

def compare(parent, child):
    # print("parent:")
    # printState(parent)
    # print("child")
    # printState(child)
    # print("-----------------")
    if parent.cLeft == child.cLeft and parent.mLeft == child.mLeft \
        and parent.boat == child.boat:
            return True

    return False

def BFS(cur_state):
    queue = list()
    visited = set()
    queue.append(cur_state)

    while queue:
        state = queue.pop(0)
        if state.isGoal():
            return state

        visited.add(state)
        setStateChildren(state)
        for child in state.children:
            if child not in visited or child not in queue:
                queue.append(child)

def DFSlimited(cur_state, limit):
    if cur_state.isGoal():
        return cur_state
    
    elif limit == 0:
        return "cutoff"

    else:
        cutoff = False
        setStateChildren(cur_state)
        for child in cur_state.children:
            result = DFSlimited(child, limit - 1)
           
            if result == "cutoff":
                cutoff = True

            elif result is not None:
                return result
            
        return "cutoff" if cutoff else None

def printState(cur_state):
    print("<{},{},{},{},{}>".format(cur_state.cLeft, cur_state.mLeft, cur_state.boat, cur_state.cRight, cur_state.mRight))


def main():
    starttime = time.time()
    initial_state = State(3, 3, 'left', 0, 0, None)
    
    # finish_state = DFSlimited(initial_state, 20)
    # if finish_state == 'cutoff' or finish_state == None:
    #     print("not found")
    
    # else:
    #     printState(finish_state)
    
    finish_state = BFS(initial_state)
    path = []
    while finish_state != None:
        path.append(finish_state)
        finish_state = finish_state.parent

    for i in range(len(path) - 1, -1, -1):
        printState(path[i])

    endtime = time.time() - starttime
    print(endtime)

if __name__ == "__main__":
    main()