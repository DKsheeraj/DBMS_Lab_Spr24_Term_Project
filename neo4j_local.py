from neo4j import GraphDatabase
import random
import sys

if len(sys.argv) < 2:
    print("Usage: python3 dataset.py <load>")
    exit()

load = sys.argv[1]=="1"

# Set up the connection parameters
uri = "bolt://localhost:7687"  # URI of your local Neo4j instance
username = "neo4j"  # Default username
password = "8985847358"  # Default password

# Function to establish a connection to the Neo4j database
def connect_to_neo4j(uri, username, password):
    try:
        driver = GraphDatabase.driver(uri, auth=(username, password))
        print("Successfully connected to Neo4j!")
        return driver
    except Exception as e:
        print(f"Failed to connect to Neo4j: {e}")
        return None

# Connect to Neo4j Aura
driver = connect_to_neo4j(uri, username, password)
session = driver.session()

# Example query (replace with your own queries)
if driver is None:
    print("Connection to Neo4j Aura failed.")

##########################################################################

# Load the dataset into Neo4j Aura

if load:
    with open("sample_dataset.txt", "r") as file:
        for line in file:
            source, target = line.strip().split("\t")
            
            query = (
                f"MERGE (source:Node {{id: {source}}})"
                f"MERGE (target:Node {{id: {target}}})"
                f"MERGE (source)-[:EDGE_TO]->(target)"
            )
            
            session.run(query)
                
    print("Data loaded into Neo4j successfully!")
else:
    print("Using Data already loaded into Neo4j.")


# Queries

def countNodes():
    # Query 1: Get the count of nodes in the graph
    print("\n\nNumber of nodes in the graph: ")
    query1 = "MATCH (n) RETURN count(n) AS node_count"

    result1 = session.run(query1)
    for record in result1:
        node_count = record["node_count"]
        print("Total nodes count:", node_count)
        
def allNodes():
    # Query 2: Get all nodes in the graph
    print("\n\nNodes in the graph: ")
    query2 = "MATCH (n) RETURN n"

    result2 = session.run(query2)
    for record in result2:
        node_number = record['n']['id']
        print(node_number, end=" ")
            
def connectedNodes(node_id):
    # Query 3: Get all nodes connected to a specific node
    print("\n\nNodes that have connection from ", node_id, " :")
    query3 = f"MATCH (n)-[:EDGE_TO]->(m) WHERE n.id = {node_id} RETURN m"
    
    count = 0

    result3 = session.run(query3)
    for record in result3:
        node_number = record['m']['id']
        print(node_number, end=" ")
        count += 1
        
    return count
            
def commonNeighbors(node_id1, node_id2):
    # Query 4: Get the common neighbors of two nodes
    print("\n\nCommon connections from nodes ", node_id1, " and ", node_id2, " :")
    query4 = f"MATCH (n1)-[:EDGE_TO]->(m)<-[:EDGE_TO]-(n2) WHERE n1.id = {node_id1} AND n2.id = {node_id2} RETURN m"

    result4 = session.run(query4)
    for record in result4:
        node_number = record['m']['id']
        print(node_number, end=" ")
            
def shortestPath(node_id1, node_id2):
    # Query 5: Get the shortest path between two nodes
    print("\n\nShortest path between nodes ", node_id1, " and ", node_id2, " :")
    query5 = f"MATCH path = shortestPath((n1)-[:EDGE_TO*]-(n2)) WHERE n1.id = {node_id1} AND n2.id = {node_id2} RETURN nodes(path)"

    result5 = session.run(query5)
    for record in result5:
        nodes_in_path = record['nodes(path)']
        for node in nodes_in_path:
            print(node['id'], end = " ")
        
def allPaths(node_id1, node_id2):
    # Query 6: Get all paths between two nodes
    print("\n\nAll paths between nodes ", node_id1, " and ", node_id2, " :")
    query6 = f"MATCH path = allShortestPaths((n1)-[:EDGE_TO*]-(n2)) WHERE n1.id = {node_id1} AND n2.id = {node_id2} RETURN nodes(path)"

    result6 = session.run(query6)
    for record in result6:
        nodes_in_path = record['nodes(path)']
        for node in nodes_in_path:
            print(node['id'], end = " ")
            
        print()
        
def kLengthPaths(node_id1, node_id2, k):
    # Query 7: Get all paths of length k between two nodes
    print("\n\nAll paths of length ", k, " between nodes ", node_id1, " and ", node_id2, " :")

    query7 = (
        f"MATCH path = (n1)-[:EDGE_TO*{k}]-(n2) "
        f"WHERE n1.id = {node_id1} AND n2.id = {node_id2} "
        f"RETURN nodes(path)"
    )
    

    result7 = session.run(query7)
    for record in result7:
        nodes_in_path = record['nodes(path)']
        for node in nodes_in_path:
            print(node['id'], end = " ")
            
        print()
            
def traingleCount():
    # Query 8: Get the count of triangles in the graph
    print("\n\nNumber of triangles in the graph: ")
    query8 = "MATCH (a)-[:EDGE_TO]->(b)-[:EDGE_TO]->(c)-[:EDGE_TO]->(a) RETURN count(DISTINCT [a, b, c]) AS triangle_count"

    result8 = session.run(query8)
    for record in result8:
        triangle_count = record["triangle_count"]
        print("Total triangles count:", triangle_count)
            
def trianglesContainingNode(node_id):
    # Query to find all triangles containing a specific node
    print("\n\nTriangles containing node ", node_id, ":")
    query9 = (
        f"MATCH (a)-[:EDGE_TO]->(b)-[:EDGE_TO]->(c)-[:EDGE_TO]->(a) "
        f"WHERE a.id = {node_id} OR b.id = {node_id} OR c.id = {node_id} "
        "RETURN DISTINCT a.id, b.id, c.id"
    )
    
    count = 0

    result = session.run(query9)
    for record in result:
        count += 1
        
        node_a = record["a.id"]
        node_b = record["b.id"]
        node_c = record["c.id"]
        print("Triangle ", count, ":", (node_a, node_b, node_c))
        
    return count
            
def clusteringCoefficient(node_id):
    # Query to calculate the clustering coefficient of a node
    print("\n\nClustering coefficient of node ", node_id, " :", end = " ")
    
    query1 = (
        f"MATCH (a)-[:EDGE_TO]->(b)-[:EDGE_TO]->(c)-[:EDGE_TO]->(a) "
        f"WHERE a.id = {node_id} OR b.id = {node_id} OR c.id = {node_id} "
        "RETURN DISTINCT a.id, b.id, c.id"
    )
    
    query2 = f"MATCH (n)-[:EDGE_TO]->(m) WHERE n.id = {node_id} RETURN count(m) AS degree"
    

    result1 = session.run(query1)
    result2 = session.run(query2)
    
    for record in result2:
        degree = record["degree"]
    
    triangles = 0
    for record in result1:
        triangles += 2
    
    neighbors = degree * (degree - 1)
    
    if neighbors == triangles:
        clust_coeff = -1
    else:
        clust_coeff = triangles / (neighbors - triangles)
        
    print(clust_coeff)
    
    return clust_coeff
            
def communityDetection():
    # Query 11: Community detection using the Louvain algorithm
    print("\n\nCommunity detection using the Louvain algorithm: ")

    # query = (
    #     f"CALL gds.graph.project('myGraph', 'neo4j', "
    #     "{nodeProjection: 'Node', relationshipProjection: {EDGE_TO: {type: 'EDGE_TO', orientation: 'DIRECTED'}}, includeIntermediateCommunities: true})"
    # )

    query = "CALL gds.graph.project('myGraph', 'neo4j', {nodeProjection: 'Node', relationshipProjection: {EDGE_TO: {type: 'EDGE_TO', orientation: 'UNDIRECTED'}}})"

    query11 = "CALL gds.louvain.stream('myGraph') YIELD nodeId, communityId, intermediateCommunityIds RETURN gds.util.asNode(nodeId).id AS id, communityId ORDER BY id"

    with driver.session() as session:
        result = session.run(query)
        result11 = session.run(query11)
        for record in result11:
            node_number = record['id']
            community_id = record['communityId']
            print("Node:", node_number, " Community ID:", community_id)

            
def pageRank():
    # Query 12: PageRank algorithm
    print("\n\nPageRank algorithm: ")
    query12 = "CALL gds.pageRank.stream({nodeProjection: 'Node', relationshipProjection: {EDGE_TO: {type: 'EDGE_TO', orientation: 'DIRECTED'}}, maxIterations: 20, dampingFactor: 0.85}) YIELD nodeId, score RETURN gds.util.asNode(nodeId).id AS node, score ORDER BY score DESC"

    result12 = session.run(query12)
    for record in result12:
        node_number = record['node']
        score = record['score']
        print("Node:", node_number, " Score:", score)
            
def centrality():
    # Query 13: Centrality measures
    print("\n\nCentrality measures: ")
    query13 = "CALL gds.pageRank.stream({nodeProjection: 'Node', relationshipProjection: {EDGE_TO: {type: 'EDGE_TO', orientation: 'DIRECTED'}}, maxIterations: 20, dampingFactor: 0.85}) YIELD nodeId, score RETURN gds.util.asNode(nodeId).id AS node, score ORDER BY score DESC"

    result13 = session.run(query13)
    for record in result13:
        node_number = record['node']
        score = record['score']
        print("Node:", node_number, " Score:", score)
            
def connectedComponents():
    # Query 14: Connected components
    print("\n\nConnected components: ")
    query14 = "CALL gds.wcc.stream({nodeProjection: 'Node', relationshipProjection: {EDGE_TO: {type: 'EDGE_TO', orientation: 'DIRECTED'}}}) YIELD nodeId, componentId RETURN gds.util.asNode(nodeId).id AS node, componentId ORDER BY node"

    result14 = session.run(query14)
    for record in result14:
        node_number = record['node']
        component_id = record['componentId']
        print("Node:", node_number, " Component ID:", component_id)
            
def graphSage():
    # Query 15: GraphSAGE algorithm
    print("\n\nGraphSAGE algorithm: ")
    query15 = "CALL gds.beta.graphSage.stream({nodeProjection: 'Node', relationshipProjection: {EDGE_TO: {type: 'EDGE_TO', orientation: 'DIRECTED'}}, model: 'graphsage-mean', featureProperties: ['id'], aggregator: 'mean', activationFunction: 'sigmoid', sampleSizes: [25, 10], degreeAsProperty: true, epochs: 5, searchDepth: 5, batchSize: 1000, learningRate: 0.01, embeddingSize: 16, 'negativeSampleWeight': 5.0, 'includeProperties': true}) YIELD nodeId, embedding RETURN gds.util.asNode(nodeId).id AS node, embedding ORDER BY node"

    result15 = session.run(query15)
    for record in result15:
        node_number = record['node']
        embedding = record['embedding']
        print("Node:", node_number, " Embedding:", embedding)
            
            
node1 = 37
node2 = random.randint(1, 100)

# try:
#     communityDetection()
# except Exception as e:
#     print("Error :", e)

# session.close()
# driver.close()
# exit()

try:
    countNodes()
except Exception as e:
    print("Error in countNodes: ", e)

try:
    countNodes()
except Exception as e:
    print("Error in countNodes: ", e)

try:
    allNodes()
except Exception as e:
    print("Error in allNodes: ", e)

try:
    connectedNodes(node1)
except Exception as e:
    print("Error in connectedNodes: ", e)

try:
    commonNeighbors(node1, node2)
except Exception as e:
    print("Error in commonNeighbors: ", e)

try:
    shortestPath(node1, node2)
except Exception as e:
    print("Error in shortestPath: ", e)

try:
    allPaths(node1, node2)
except Exception as e:
    print("Error in allPaths: ", e)

try:
    kLengthPaths(node1, node2, random.randint(1, 10))
except Exception as e:
    print("Error in kLengthPaths: ", e)

try:
    traingleCount()
except Exception as e:
    print("Error in traingleCount: ", e)
    
try:
    trianglesContainingNode(node1)
except Exception as e:
    print("Error in trianglesContainingNode: ", e)

try:
    clusteringCoefficient(node1)
except Exception as e:
    print("Error in clusteringCoefficient: ", e)

# try:
#     communityDetection()
# except Exception as e:
#     print("Error in communityDetection: ", e)

# try:
#     pageRank()
# except Exception as e:
#     print("Error in pageRank: ", e)

# try:
#     centrality()
# except Exception as e:
#     print("Error in centrality: ", e)

# try:
#     connectedComponents()
# except Exception as e:
#     print("Error in connectedComponents: ", e)

# try:
#     graphSage()
# except Exception as e:
#     print("Error in graphSage: ", e)
        
# # Close the session & driver connection
session.close()
driver.close()

exit()