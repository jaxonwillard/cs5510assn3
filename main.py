from string import ascii_lowercase
class Orientation():

  def __init__(self):
    self.u= (-1,0)
    self.d=  (1,0)
    self.l=  (0,-1)
    self.r=  (0,1)
    self.ur= (-1,1)
    self.ul= (-1,-1)
    self.dl= (1,-1)
    self.dr= (1,1)
    
    sides      = [self.u,self.d,self.ur,self.ul,self.dr, self.dl]
    up_down    = [self.r,self.l,self.ur,self.ul,self.dr,self.dl] 
    diag_right = [self.r,self.l,self.u,self.d,self.ul,self.dr]
    diag_left  = [self.r,self.l,self.u,self.d,self.ur,self.dl]
    self.options = {
      "u": sides,
      "d": sides,
      "l": up_down,
      "r": up_down,
      "ur": diag_left,
      "ul": diag_right,
      "dl": diag_left,
      "dr": diag_right,
    }
    self.orientation = "u" 

  def get_options(self):
    return self.options[self.orientation]

  def update_orientation(self, current_position, child_position):
    diff = (current_position[0]-child_position[0], current_position[1]-child_position[1])
    if diff == self.u:
      self.orientation = "u"
    elif diff == self.d:
      self.orientation = "d"
    elif diff == self.l:
      self.orientation = "l"
    elif diff == self.r:
      self.orientation = "r"
    elif diff == self.ur:
      self.orientation = "ur"
    elif diff == self.ul:
      self.orientation = "ul"
    elif diff == self.dl:
      self.orientation = "dl"
    elif diff == self.dr:
      self.orientation = "dr"
    else:
      print("---err---", diff)
class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0
        self.o = Orientation()

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""
    o = Orientation()
    print(o.get_options())

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        # for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares
        for new_position in current_node.o.get_options():

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h
            child.o = child.o.update_orientation(current_node.position, child.position)

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)

def show_path(path, maze):

  mcopy = [i for i in maze]
  for i, step in enumerate(path):
    mcopy[step[0]][step[1]] = "%s" % ascii_lowercase[i]

  for i in range(len(mcopy)):
    for j in range(len(mcopy[i])):
      print(mcopy[i][j], end="  ")
    print("")

def main():

    maze = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    # maze = [
    #   [0,0,0],
    #   [1,0,0]
    # ]

    start = (0, 0)
    end = (6,6)

    path = astar(maze, start, end)
    print(path)

    show_path(path, maze)


if __name__ == '__main__':
    main()
