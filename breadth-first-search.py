import sys
from time import sleep

class NoSolution(BaseException):
    """A custom error that bypasses Exception handling
    by subclassing BaseException"""
    pass

class Node:
    def __init__(self, coords):
        self.parent = None
        self.coords = coords
        self.availableNodes = []
        self.type = None
        self.age = None
    def SetType(self, NodeType):
        self.type = NodeType
        return self
    


class Frontier:
    def __init__(self,start):
        self.queue = [start]
        self.statesChecked = set()
        self.order = 1
        self.age = 0
    def append(self, node):
        if node not in self.queue and node not in self.statesChecked:
            self.queue.append(node)
        return self
    def extend(self, nodes):
        if type(nodes) == list and all(type(node) == Node for node in nodes):
            for node in nodes:
                self.append(node)
        else:
            raise ValueError("Frontier.extend() takes 1 positional argument of type list of Nodes.")
        return self
    def expand(self,reverse=False):
        SelectedNode = self.queue[0]
        for node in SelectedNode.availableNodes:
            if node not in self.statesChecked:
                if node.type not in ("A","B"):
                    node.type = "░"
                node.parent = SelectedNode
                node.age = self.age
                self.age += 1
        self.statesChecked.add(SelectedNode)
        self.extend(SelectedNode.availableNodes)
        self.queue.remove(SelectedNode)
        self.Reorder(reverse)
        return SelectedNode
    def CheckGoal(self):
        if len(self.queue) == 0:
            raise NoSolution()
        goal = [node for node in self.queue if node.type == "B"]
        if len(goal) == 0:
            return None
        else:
            return goal[0]
    def Reorder(self,reverse):
        self.queue.sort(reverse=reverse,key=lambda node:node.age)
    def AssignAge(self,node):
        node.age = self.age
        self.age += 1
        return node


        
    #display the maze
def display(grid):
    length = len(grid)
    height = len(grid[-1])
    for y in range(height):
        for x in range(length):
            print(grid[x][y].type,end="")
        print(end="\n")
    print(end="\x1b[1A"*height)
    sleep(0.016)

def main():
    try:
        ## BUILDING THE MAZE
        if len(sys.argv) == 2: 
            with open(sys.argv[1], "r") as e:
                maze = e.readlines()
                height = len(maze)
                length = len(maze[-1])
                grid = [[None for _ in range(height)] for _ in range(length)]

                #assign each node its position
                for y, row in enumerate(maze):
                    for x in range(length): # using a for loop to avoid the \n character on most lines
                        grid[x][y] = Node((x,y)).SetType(row[x])
        display(grid)
        
        # find path
        path = search(grid)
            
        for node in path:
            if node.type not in ("A","B"):
                node.type = "█"
        display(grid)
        #cleanup
        print("\x1b[1B"*height)
    except KeyboardInterrupt:
        display([[Node((0,0)).SetType(" ") for _ in range(height)] for _ in range(length)])
    except NoSolution:
        display([[Node((0,0)).SetType(" ") for _ in range(height)] for _ in range(length)])
        print("No solution")
        

    



def search(grid):
    height = len(grid)
    length = len(grid[-1])
    
    def CheckAdjacents(node):
        x, y = node.coords
        if x != 0 and grid[x-1][y].type != "#":
            node.availableNodes.append(grid[x-1][y])
        if x != height- 1 and grid[x+1][y].type != "#":
            node.availableNodes.append(grid[x+1][y])
        if y != 0 and grid[x][y-1].type != "#":
            node.availableNodes.append(grid[x][y-1])
        if y != length - 1 and grid[x][y+1].type != "#":
            node.availableNodes.append(grid[x][y+1])
        return node
    
    start, goal = None, None
    # find start and goal
    for row in grid:
        for node in row:
            if node.type == "A":
                start = node
            elif node.type == "B":
                goal = node
            if start != None and goal != None:
                break

    # Start search
    frontier = Frontier(start)
    while frontier.CheckGoal() == None:
        frontier.queue[0] = CheckAdjacents(frontier.queue[0])
        frontier.expand(False)
        display(grid)
    node = frontier.CheckGoal()
    path = []
    while node.type != "A":
        path.append(node)
        node = node.parent
    path.reverse() 
    for row in grid:
        for node in row:
            if node in frontier.statesChecked and node.type not in ("A","B"):
                node.type = "░"
    for node in path:
        if node.type not in ("A","B"):
            node.type = "█"

    return path





if __name__ == "__main__":
    main()