import sys
from neo4j import GraphDatabase
import random

if len(sys.argv) < 2:
    print("Usage: python3 dataset.py <load>")
    exit()

load = sys.argv[1]=="1"

# Neo4j Aura credentials
uri = "neo4j+s://c88bce7d.databases.neo4j.io"
username = "neo4j"
password = "7Ox4GnmURxzfnFJ4vjYXx0MjRqSIQeUgn3a7l9CaLu0"

# Function to establish a connection to the Neo4j database
def connect_to_neo4j(uri, username, password):
    try:
        driver = GraphDatabase.driver(uri, auth=(username, password))
        print("Successfully connected to Neo4j Aura!")
        return driver
    except Exception as e:
        print(f"Failed to connect to Neo4j Aura: {e}")
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
                f"MERGE (source)-[:CONNECTED_TO]->(target)"
            )
            
            session.run(query)
                
    print("Data loaded into Neo4j successfully!")
else:
    print("Using Data already loaded into Neo4j.")

# # Close the session & driver connection
# session.close()
# driver.close()

# exit()

# Run simple queries to verify the data was loaded correctly

# # Query 1: Get all nodes in the graph
# print("\nNodes in the graph: ")
# query1 = "MATCH (n) RETURN n"
# with driver.session() as session:
#     result1 = session.run(query1)
#     for record in result1:
#         node_number = record['n']['id']
#         print(node_number, end=" ")

# # Query 2: Get all nodes connected to a specific node
# node_id = 1  # Replace with the desired node ID
# print("\n\nNodes connected to a node ", node_id, " :")
# query2 = f"MATCH (n)-[:CONNECTED_TO]->(m) WHERE n.id = {node_id} RETURN m"
# with driver.session() as session:
#     result2 = session.run(query2)
#     for record in result2:
#         node_number = record['m']['id']
#         print(node_number, end=" ")

# # Query 3: Get the count of nodes in the graph
# print("\n\nNumber of nodes in the graph: ")
# query3 = "MATCH (n) RETURN count(n) AS node_count"
# with driver.session() as session:
#     result3 = session.run(query3)
#     for record in result3:
#         node_count = record["node_count"]
#         print("Total nodes count:", node_count)


def countNodes(driver):
    # Query 1: Get the count of nodes in the graph
    print("\n\nNumber of nodes in the graph: ")
    query1 = "MATCH (n) RETURN count(n) AS node_count"
    with driver.session() as session:
        result1 = session.run(query1)
        for record in result1:
            node_count = record["node_count"]
            print("Total nodes count:", node_count)
        
def allNodes(driver):
    # Query 2: Get all nodes in the graph
    print("\n\nNodes in the graph: ")
    query2 = "MATCH (n) RETURN n"
    with driver.session() as session:
        result2 = session.run(query2)
        for record in result2:
            node_number = record['n']['id']
            print(node_number, end=" ")
            
def connectedNodes(driver, node_id):
    # Query 3: Get all nodes connected to a specific node
    print("\n\nNodes that have connection from ", node_id, " :")
    query3 = f"MATCH (n)-[:CONNECTED_TO]->(m) WHERE n.id = {node_id} RETURN m"
    
    count = 0
    with driver.session() as session:
        result3 = session.run(query3)
        for record in result3:
            node_number = record['m']['id']
            print(node_number, end=" ")
            count += 1
            
        return count
            
def commonNeighbors(driver, node_id1, node_id2):
    # Query 4: Get the common neighbors of two nodes
    print("\n\nCommon connections from nodes ", node_id1, " and ", node_id2, " :")
    query4 = f"MATCH (n1)-[:CONNECTED_TO]->(m)<-[:CONNECTED_TO]-(n2) WHERE n1.id = {node_id1} AND n2.id = {node_id2} RETURN m"
    with driver.session() as session:
        result4 = session.run(query4)
        for record in result4:
            node_number = record['m']['id']
            print(node_number, end=" ")
            
def shortestPath(driver, node_id1, node_id2):
    # Query 5: Get the shortest path between two nodes
    print("\n\nShortest path between nodes ", node_id1, " and ", node_id2, " :")
    query5 = f"MATCH path = shortestPath((n1)-[:CONNECTED_TO*]-(n2)) WHERE n1.id = {node_id1} AND n2.id = {node_id2} RETURN nodes(path)"
    with driver.session() as session:
        result5 = session.run(query5)
        for record in result5:
            nodes_in_path = record['nodes(path)']
            for node in nodes_in_path:
                print(node['id'], end = " ")
            
def allPaths(driver, node_id1, node_id2):
    # Query 6: Get all paths between two nodes
    print("\n\nAll paths between nodes ", node_id1, " and ", node_id2, " :")
    query6 = f"MATCH path = allShortestPaths((n1)-[:CONNECTED_TO*]-(n2)) WHERE n1.id = {node_id1} AND n2.id = {node_id2} RETURN nodes(path)"
    with driver.session() as session:
        result6 = session.run(query6)
        for record in result6:
            nodes_in_path = record['nodes(path)']
            for node in nodes_in_path:
                print(node['id'], end = " ")
                
            print()
            
def kLengthPaths(driver, node_id1, node_id2, k):
    # Query 7: Get all paths of length k between two nodes
    print("\n\nAll paths of length ", k, " between nodes ", node_id1, " and ", node_id2, " :")

    query7 = (
        f"MATCH path = (n1)-[:CONNECTED_TO*{k}]-(n2) "
        f"WHERE n1.id = {node_id1} AND n2.id = {node_id2} "
        f"RETURN nodes(path)"
    )
    
    with driver.session() as session:
        result7 = session.run(query7)
        for record in result7:
            nodes_in_path = record['nodes(path)']
            for node in nodes_in_path:
                print(node['id'], end = " ")
                
            print()
            
def traingleCount(driver):
    # Query 8: Get the count of triangles in the graph
    print("\n\nNumber of triangles in the graph: ")
    query8 = "MATCH (a)-[:CONNECTED_TO]->(b)-[:CONNECTED_TO]->(c)-[:CONNECTED_TO]->(a) RETURN count(DISTINCT [a, b, c]) AS triangle_count"
    with driver.session() as session:
        result8 = session.run(query8)
        for record in result8:
            triangle_count = record["triangle_count"]
            print("Total triangles count:", triangle_count)
            
def trianglesContainingNode(driver, node_id):
    # Query to find all triangles containing a specific node
    print("\n\nTriangles containing node ", node_id, ":")
    query9 = (
        f"MATCH (a)-[:CONNECTED_TO]->(b)-[:CONNECTED_TO]->(c)-[:CONNECTED_TO]->(a) "
        f"WHERE a.id = {node_id} OR b.id = {node_id} OR c.id = {node_id} "
        "RETURN DISTINCT a.id, b.id, c.id"
    )
    
    count = 0
    with driver.session() as session:
        result = session.run(query9)
        for record in result:
            count += 1
            
            node_a = record["a.id"]
            node_b = record["b.id"]
            node_c = record["c.id"]
            print("Triangle ", count, ":", (node_a, node_b, node_c))
            
        return count
            
def clusteringCoefficient(driver, node_id):
    # Query to calculate the clustering coefficient of a node
    print("\n\nClustering coefficient of node ", node_id, " :", end = " ")
    
    query1 = (
        f"MATCH (a)-[:CONNECTED_TO]->(b)-[:CONNECTED_TO]->(c)-[:CONNECTED_TO]->(a) "
        f"WHERE a.id = {node_id} OR b.id = {node_id} OR c.id = {node_id} "
        "RETURN DISTINCT a.id, b.id, c.id"
    )
    
    query2 = f"MATCH (n)-[:CONNECTED_TO]->(m) WHERE n.id = {node_id} RETURN count(m) AS degree"
    
    with driver.session() as session:
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
            
def communityDetection(driver):
    # Query 11: Community detection using the Louvain algorithm
    print("\n\nCommunity detection using the Louvain algorithm: ")
    query11 = "CALL gds.louvain.stream({nodeProjection: 'Node', relationshipProjection: {CONNECTED_TO: {type: 'CONNECTED_TO', orientation: 'UNDIRECTED'}}, includeIntermediateCommunities: true}) YIELD nodeId, communityId, intermediateCommunityIds RETURN gds.util.asNode(nodeId).id AS node, communityId, intermediateCommunityIds ORDER BY node"
    with driver.session() as session:
        result11 = session.run(query11)
        for record in result11:
            node_number = record['node']
            community_id = record['communityId']
            print("Node:", node_number, " Community ID:", community_id)
            
def pageRank(driver):
    # Query 12: PageRank algorithm
    print("\n\nPageRank algorithm: ")
    query12 = "CALL gds.pageRank.stream({nodeProjection: 'Node', relationshipProjection: {CONNECTED_TO: {type: 'CONNECTED_TO', orientation: 'UNDIRECTED'}}, maxIterations: 20, dampingFactor: 0.85}) YIELD nodeId, score RETURN gds.util.asNode(nodeId).id AS node, score ORDER BY score DESC"
    with driver.session() as session:
        result12 = session.run(query12)
        for record in result12:
            node_number = record['node']
            score = record['score']
            print("Node:", node_number, " Score:", score)
            
def centrality(driver):
    # Query 13: Centrality measures
    print("\n\nCentrality measures: ")
    query13 = "CALL gds.pageRank.stream({nodeProjection: 'Node', relationshipProjection: {CONNECTED_TO: {type: 'CONNECTED_TO', orientation: 'UNDIRECTED'}}, maxIterations: 20, dampingFactor: 0.85}) YIELD nodeId, score RETURN gds.util.asNode(nodeId).id AS node, score ORDER BY score DESC"
    with driver.session() as session:
        result13 = session.run(query13)
        for record in result13:
            node_number = record['node']
            score = record['score']
            print("Node:", node_number, " Score:", score)
            
def connectedComponents(driver):
    # Query 14: Connected components
    print("\n\nConnected components: ")
    query14 = "CALL gds.wcc.stream({nodeProjection: 'Node', relationshipProjection: {CONNECTED_TO: {type: 'CONNECTED_TO', orientation: 'UNDIRECTED'}}}) YIELD nodeId, componentId RETURN gds.util.asNode(nodeId).id AS node, componentId ORDER BY node"
    with driver.session() as session:
        result14 = session.run(query14)
        for record in result14:
            node_number = record['node']
            component_id = record['componentId']
            print("Node:", node_number, " Component ID:", component_id)
            
def graphSage(driver):
    # Query 15: GraphSAGE algorithm
    print("\n\nGraphSAGE algorithm: ")
    query15 = "CALL gds.beta.graphSage.stream({nodeProjection: 'Node', relationshipProjection: {CONNECTED_TO: {type: 'CONNECTED_TO', orientation: 'UNDIRECTED'}}, model: 'graphsage-mean', featureProperties: ['id'], aggregator: 'mean', activationFunction: 'sigmoid', sampleSizes: [25, 10], degreeAsProperty: true, epochs: 5, searchDepth: 5, batchSize: 1000, learningRate: 0.01, embeddingSize: 16, 'negativeSampleWeight': 5.0, 'includeProperties': true}) YIELD nodeId, embedding RETURN gds.util.asNode(nodeId).id AS node, embedding ORDER BY node"
    with driver.session() as session:
        result15 = session.run(query15)
        for record in result15:
            node_number = record['node']
            embedding = record['embedding']
            print("Node:", node_number, " Embedding:", embedding)
            
            
node1 = random.randint(1, 100)
node2 = random.randint(1, 100)

try:
    communityDetection(driver)
except Exception as e:
    print("Error :", e)

session.close()
driver.close()
exit()

try:
    countNodes(driver)
except Exception as e:
    print("Error in countNodes: ", e)

try:
    countNodes(driver)
except Exception as e:
    print("Error in countNodes: ", e)

try:
    allNodes(driver)
except Exception as e:
    print("Error in allNodes: ", e)

try:
    connectedNodes(driver, node1)
except Exception as e:
    print("Error in connectedNodes: ", e)

try:
    commonNeighbors(driver, node1, node2)
except Exception as e:
    print("Error in commonNeighbors: ", e)

try:
    shortestPath(driver, node1, node2)
except Exception as e:
    print("Error in shortestPath: ", e)

try:
    allPaths(driver, node1, node2)
except Exception as e:
    print("Error in allPaths: ", e)

try:
    kLengthPaths(driver, node1, node2, 4)
except Exception as e:
    print("Error in kLengthPaths: ", e)

try:
    traingleCount(driver)
except Exception as e:
    print("Error in traingleCount: ", e)
    
try:
    trianglesContainingNode(driver, node1)
except Exception as e:
    print("Error in trianglesContainingNode: ", e)

try:
    clusteringCoefficient(driver, node1)
except Exception as e:
    print("Error in clusteringCoefficient: ", e)

try:
    degreeDistribution(driver)
except Exception as e:
    print("Error in degreeDistribution: ", e)

try:
    communityDetection(driver)
except Exception as e:
    print("Error in communityDetection: ", e)

try:
    pageRank(driver)
except Exception as e:
    print("Error in pageRank: ", e)

try:
    centrality(driver)
except Exception as e:
    print("Error in centrality: ", e)

try:
    connectedComponents(driver)
except Exception as e:
    print("Error in connectedComponents: ", e)

try:
    graphSage(driver)
except Exception as e:
    print("Error in graphSage: ", e)
        
# # Close the session & driver connection
session.close()
driver.close()

exit()