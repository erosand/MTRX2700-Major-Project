from math import floor, sin, cos, radians, degrees
from multiprocessing import connection
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np
import random

# 1. Generate test data (store data in a boolean array to decrease memory usage)
# 2. Thresdhold each depth then filter noise
# 3. Detect boxes for each threshdold image (Calculate perceived area of each box for a given depth. If the area is an integer mutliple of the perceived area of a box at a given depth)
# 4. Calculate number of boxes
# 5. Display information on a screen or something


def dfs(visited, graph, node): 
    if node not in visited:
        # print (node)
        visited.add(node)
        for neighbour in graph[node]:
            dfs(visited, graph, neighbour)

def GenerateData(floor_depth, box_side):
    # FOV boundary values
    x_length = 45
    y_length = 45
    error = int(box_side*0.1)

    arr_depths = np.zeros((x_length, y_length), dtype=int)

    floor_error = 2
    for i in range(0, len(arr_depths)):
        for j in range(0, len(arr_depths[i])):
            arr_depths[i][j] = random.randint(int(floor_depth - floor_error), int(floor_depth + floor_error))

    
    # 1st quadrant
    for i in range(y_length//4, y_length//2):
        for j in range(x_length//2, x_length//2 + x_length//4):
            arr_depths[i][j] = random.randint(floor_depth - 1*box_side - error, floor_depth - 1*box_side + error)

    # 2st quadrant
    for i in range(y_length//4 - 1, y_length//2):
        for j in range(x_length//4 - 1, x_length//4 + x_length//4):
            arr_depths[i][j] = random.randint(floor_depth - 2*box_side - error, floor_depth - 2*box_side + error)

    # 3rd quadrant
    for i in range(y_length//2, y_length//2 + y_length//4 + 2):
        for j in range(x_length//4 - 2, x_length//4 + x_length//4):
            arr_depths[i][j] = random.randint(floor_depth - 3*box_side - error, floor_depth - 3*box_side + error)

    # 4th quadrant
    for i in range(y_length//2, y_length//2 + y_length//4 + 3):
        for j in range(x_length//2, x_length//2 + x_length//4 + 3):
            arr_depths[i][j] = random.randint(floor_depth - 4*box_side - error, floor_depth - 4*box_side + error)

    return arr_depths

def PlotData(arr_data):
    rowdata = []
    coldata = []
    zdata = []
    countrow = 0
    for row in arr_data:
        countcol = 0
        for col in row:
            rowdata.append(countrow)
            coldata.append(countcol)
            # if col == 0:
            #     zdata.append(float("nan"))
            # else:
            zdata.append(col)
            countcol += 1
        countrow += 1


    # Plotting 
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.scatter3D(rowdata, coldata, zdata, c=zdata, cmap="bone")

    ax.set_zlim3d(zmin=0)

    ax.set_xlabel('X - axis')
    ax.set_ylabel('Y - axis')
    ax.set_zlabel('Height')

    plt.show()

def NormaliseData(arr_depths, floor_depth):
    for row in range(0, len(arr_depths)):
        for col in range(0, len(arr_depths[row])):
            arr_depths[row][col] = -1*(arr_depths[row][col] - floor_depth)
    
    return arr_depths

def GenerateNodes(arr_depths, box_side):

    # Determine how many boxes is in the highest stack
    highest_stack = 0
    for row in range(0, len(arr_depths)):
        for col in range(0, len(arr_depths[row])):
            if arr_depths[row][col] > highest_stack:
                highest_stack = arr_depths[row][col]
                
    
    max_stack = highest_stack // box_side # Determine how many boxes high fit into the maximum height
    highest_stack = max_stack * box_side  # Change max height to integer multiple of boxes
    print("Highest height:", highest_stack)
    print("Highest stack:", max_stack)

    # Create array with length of the max boxes that fit within the height
    arr_thresholds = []

    # For each index of the array, multiply the box height by stack height multiple and create a threshold array from the specific depth
    error = box_side*0.1 # Accepted error threshold
    for stack in range(1, max_stack+1):
        target_depth = stack*box_side
        upper_error = target_depth + error # Can change to percentage error as well
        lower_error = target_depth - error # Can change to percentage error as well

        nodes = {}
        # Add nodes to a graph
        for i in range(0, len(arr_depths)):
            for j in range(0, len(arr_depths[i])):
                if (arr_depths[i][j] >= lower_error) and (arr_depths[i][j] <= upper_error):
                    #Create a node and add the node
                    nodes[(i, j)] = []
                else: 
                    pass

        # Connnect nodes
        for row, col in nodes:
            # Check above
            if (row-1, col) in nodes:
                nodes[(row, col)].append((row-1, col))
            # Check below
            if (row+1, col) in nodes:
                nodes[(row, col)].append((row+1, col))
            # Check left
            if (row, col-1) in nodes:
                nodes[(row, col)].append((row, col-1))
            # Check right
            if (row, col+1) in nodes:
                nodes[(row, col)].append((row, col+1))

        # Add the graph of nodes to an array
        arr_thresholds.append(nodes)
    

    return arr_thresholds

def PredictedNodeCount(angle_step, floor_depth, box_side, stack_integer):
    x = box_side/(floor_depth - (stack_integer*box_side))
    return floor(degrees(np.arctan(x) / angle_step))**2 

def CalculateBoxCount(arr_raw_nodes, angle_step, floor_depth, box_side):
    box_count = 0
    accuracy = 0.95

    curr_stack_count = 0
    for depth in arr_raw_nodes:
        curr_stack_count += 1

        target_node_count = PredictedNodeCount(angle_step, floor_depth, box_side, curr_stack_count)
        # print("Target Node cnt: " + str(target_node_count))

        while len(depth) > 0: #While there are still more nodes in the arr_raw_nodes
            visited = set()
            dfs(visited, depth, next(iter(depth))) # Try the list typcast then access first element from there
            # print("Current stack height:", str(curr_stack_count), "-- Number of Nodes: ", str(len(visited)))
            remainder = len(visited)
            while remainder >= accuracy*target_node_count:
                box_count += curr_stack_count
                remainder -= accuracy*target_node_count

            # Deleted the visited nodes from the graph
            for node in visited:
                if node in depth:
                    del depth[node]
            visited.clear()

    print("There are currently:", str(box_count), "boxes!")


if __name__ == "__main__":
    # Initialisation values
    box_side = 10
    floor_depth = 80
    angle_step = 1
    raw_data = GenerateData(floor_depth, box_side)
    normalised_data = NormaliseData(raw_data, floor_depth)
    PlotData(normalised_data)
    raw_nodes = GenerateNodes(normalised_data, box_side)
    CalculateBoxCount(raw_nodes, angle_step, floor_depth, box_side)
