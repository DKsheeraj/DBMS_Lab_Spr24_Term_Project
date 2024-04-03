import random

# Number of nodes and edges
num_nodes = 100
num_edges = 200

random.seed(random.randint(0, 1000))

# Generate random edges
edges = []
while len(edges) < num_edges:
    node1 = random.randint(1, num_nodes)
    node2 = random.randint(1, num_nodes)
    if node1 != node2 and (node1, node2) not in edges and (node2, node1) not in edges:
        edges.append((node1, node2))

# Sort the edges by the first node ID
edges.sort(key=lambda x: (x[0], x[1]))
    
# Write the edges to a file
with open('./sample_dataset.txt', 'w') as file:
    for edge in edges:
        print(edge)
        file.write(str(edge[0]) + '\t' + str(edge[1]) + '\n')