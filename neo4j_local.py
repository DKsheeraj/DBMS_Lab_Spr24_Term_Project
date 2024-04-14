from neo4j import GraphDatabase
import random
import sys
import heapq

if len(sys.argv) < 2:
    print("Usage: python3 dataset.py <load>")
    exit()

load = sys.argv[1]

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

if load=='2':
    query = "MATCH (n) DETACH DELETE n"
    session.run(query)
    
    print("Data deleted from Neo4j successfully!")
    
    driver.close()
    session.close()
    exit()

if load=='1':
    with open("dataset.txt", "r") as file:
    # with open("sample_dataset.txt", "r") as file:
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

# Helper functions

import re

def parse_profile(profile_string):
    profile_info = {}

    # Extracting operator details using regex
    operator_regex = r'\| (.+?) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \|'
    operator_matches = re.findall(operator_regex, profile_string, re.MULTILINE)

    # If matches found
    if operator_matches:
        operators = []
        for match in operator_matches:
            operator = {
                "Operator": match[0].strip(),
                "Id": match[1].strip(),
                "Details": match[2].strip(),
                "Estimated Rows": match[3].strip(),
                "Rows": match[4].strip(),
                "DB Hits": match[5].strip(),
                "Memory (Bytes)": match[6].strip(),
                "Page Cache Hits/Misses": match[7].strip(),
                "Time (ms)": match[8].strip(),
                "Pipeline": match[9].strip()
            }
            operators.append(operator)
        profile_info["operators"] = operators

    # Extracting database accesses and allocated memory using regex
    database_regex = r'Total database accesses: (\d+), total allocated memory: (\d+)'
    database_matches = re.search(database_regex, profile_string)
    if database_matches:
        profile_info["database_accesses"] = int(database_matches.group(1))
        profile_info["allocated_memory"] = int(database_matches.group(2))

    return profile_info

def profile(summary):
    print("\nProfiling Information:")
    
    profile_string = summary.profile['args']['string-representation']
    print(profile_string)

    profile_info = parse_profile(profile_string)
    print(profile_info)

# Queries

def countNodes():
    # Query 1: Get the count of nodes in the graph
    print("\n\nNumber of nodes in the graph: ")
    query1 = "PROFILE MATCH (n) RETURN count(n) AS node_count"

    result1 = session.run(query1)
    for record in result1:
        node_count = record["node_count"]
        print("Total nodes count:", node_count)
        
    profile(result1.consume())
        
def allNodes():
    # Query 2: Get all nodes in the graph
    print("\n\nNodes in the graph: ")
    query2 = "PROFILE MATCH (n) RETURN n"

    result2 = session.run(query2)
    for record in result2:
        node_number = record['n']['id']
        print(node_number, end=" ")
        
    profile(result2.consume())
            
def connectedNodes(node_id):
    # Query 3: Get all nodes connected to a specific node
    print("\n\nNodes that have connection from ", node_id, " :")
    query3 = f"PROFILE MATCH (n)-[:EDGE_TO]->(m) WHERE n.id = {node_id} RETURN m"
    
    count = 0

    result3 = session.run(query3)
    for record in result3:
        node_number = record['m']['id']
        print(node_number, end=" ")
        count += 1
        
    profile(result3.consume())
        
    return count
            
def commonNeighbors(node_id1, node_id2):
    # Query 4: Get the common neighbors of two nodes
    # print("\n\nCommon connections from nodes ", node_id1, " and ", node_id2, " :")
    query4 = f"PROFILE MATCH (n1)-[:EDGE_TO]->(m)<-[:EDGE_TO]->(n2) WHERE n1.id = {node_id1} AND n2.id = {node_id2} RETURN m"

    count = 0
    
    result4 = session.run(query4)
    for record in result4:
        node_number = record['m']['id']
        print(node_number, end=" ")
        
        count += 1
        
    # profile(result4.consume())
    
    return count
            
def shortestPath(node_id1, node_id2):
    # Query 5: Get the shortest path between two nodes
    print("\n\nShortest path between nodes ", node_id1, " and ", node_id2, " :")
    query5 = f"PROFILE MATCH path = shortestPath((n1)-[:EDGE_TO*]->(n2)) WHERE n1.id = {node_id1} AND n2.id = {node_id2} RETURN nodes(path)"

    result5 = session.run(query5)
    for record in result5:
        nodes_in_path = record['nodes(path)']
        for node in nodes_in_path:
            print(node['id'], end = " ")
            
    profile(result5.consume())
        
def allPaths(node_id1, node_id2):
    # Query 6: Get all paths between two nodes
    print("\n\nAll paths between nodes ", node_id1, " and ", node_id2, " :")
    query6 = f"PROFILE MATCH path = allShortestPaths((n1)-[:EDGE_TO*]->(n2)) WHERE n1.id = {node_id1} AND n2.id = {node_id2} RETURN nodes(path)"

    result6 = session.run(query6)
    for record in result6:
        nodes_in_path = record['nodes(path)']
        for node in nodes_in_path:
            print(node['id'], end = " ")
            
        print()
        
    profile(result6.consume())
        
def kLengthPaths(node_id1, node_id2, k):
    # Query 7: Get all paths of length k between two nodes
    print("\n\nAll paths of length ", k, " between nodes ", node_id1, " and ", node_id2, " :")

    query7 = (
        f"PROFILE MATCH path = (n1)-[:EDGE_TO*{k}]-(n2) "
        f"WHERE n1.id = {node_id1} AND n2.id = {node_id2} "
        f"RETURN nodes(path)"
    )

    result7 = session.run(query7)
    for record in result7:
        nodes_in_path = record['nodes(path)']
        for node in nodes_in_path:
            print(node['id'], end = " ")
            
        print()
        
    profile(result7.consume())
            
def traingleCount():
    # Query 8: Get the count of triangles in the graph
    print("\n\nNumber of triangles in the graph: ")
    query8 = "PROFILE MATCH (a)-[:EDGE_TO]->(b)-[:EDGE_TO]->(c)-[:EDGE_TO]->(a) RETURN count(DISTINCT [a, b, c]) AS triangle_count"

    result8 = session.run(query8)
    for record in result8:
        triangle_count = record["triangle_count"]
        print("Total triangles count:", triangle_count)
        
    profile(result8.consume())
            
def trianglesContainingNode(node_id):
    # Query to find all triangles containing a specific node
    print("\n\nTriangles containing node ", node_id, ":")
    query9 = (
        f"PROFILE MATCH (a)-[:EDGE_TO]->(b)-[:EDGE_TO]->(c)-[:EDGE_TO]->(a) "
        f"WHERE a.id = {node_id} OR b.id = {node_id} OR c.id = {node_id} "
        "RETURN DISTINCT a.id, b.id, c.id"
    )
    
    count = 0

    result9 = session.run(query9)
    for record in result9:
        count += 1
        
        node_a = record["a.id"]
        node_b = record["b.id"]
        node_c = record["c.id"]
        print("Triangle ", count, ":", (node_a, node_b, node_c))
        
    profile(result9.consume())
    return count
            
def clusteringCoefficient(node_id):
    # Query to calculate the clustering coefficient of a node
    print("\n\nClustering coefficient of node ", node_id, " :", end = " ")
    
    query1 = (
        f"PROFILE MATCH (a)-[:EDGE_TO]->(b)-[:EDGE_TO]->(c)-[:EDGE_TO]->(a) "
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
        
    # profile(result1.consume())
    # profile(result2.consume())
    
    return clust_coeff
            
def communityDetection():
    # Query 11: Community detection using the Louvain algorithm
    print("\n\nCommunity detection using the Louvain algorithm: ")
    
    query11 = (
        f"CALL gds.louvain.stream('myGraph') "
        f"YIELD nodeId, communityId "
        f"RETURN gds.util.asNode(nodeId).id AS id, communityId "
        f"ORDER BY [communityId, id] ASC"
    )
    
    communities = {}
    
    result11 = session.run(query11)
    for record in result11:
        node_number = record['id']
        community_id = record['communityId']
        # print("Node:", node_number, " Community ID:", community_id)
        
        # communities[community_id].append(node_number) if community_id in communities else communities.update({community_id: [node_number]})
        # Increment the count of nodes for the community_id
        communities[community_id] = communities.get(community_id, 0) + 1 
    
    # Use heapq to get the top 10 communities
    top_10_communities = heapq.nlargest(10, communities.items(), key=lambda x: x[1])    
                  
    for community_id, nodes in top_10_communities:
        # print("Component ID:", community_id, " Number of Nodes:", len(nodes))
        print("Component ID:", community_id, " Number of Nodes:", nodes)
        
    print()
            
def pageRank():
    # Query 12: PageRank algorithm
    print("\n\nPageRank algorithm: ")

    query12 = (
        f"CALL gds.pageRank.stream('myGraph', {{scaler: 'L1Norm'}}) "
        # f"CALL gds.pageRank.stream('myGraph') "
        f"YIELD nodeId, score "
        f"RETURN gds.util.asNode(nodeId).id AS node, score "
        f"ORDER BY score DESC"
    )
    
    top10 = []

    result12 = session.run(query12)
    for record in result12:
        node_number = record['node']
        score = record['score']
        # print("Node:", node_number, " Score:", score)
        
        # Maintain a heap of size 10 to keep track of top nodes
        if len(top10) < 10:
            heapq.heappush(top10, (score, node_number))
        else:
            heapq.heappushpop(top10, (score, node_number))
    
    # Print the top 10 nodes and their scores
    print("Top 10 nodes by centrality: ")
    for score, node_number in sorted(top10, reverse=True):
        print("Node:", node_number, " Score:", score)
        
    print()
            
def centrality():
    # Query 13: Centrality measures
    print("\n\nCentrality measures: ")

    query13 = (
        f"CALL gds.pageRank.stream('myGraph', {{maxIterations: 20, dampingFactor: 0.85}}) "
        f"YIELD nodeId, score "
        f"RETURN gds.util.asNode(nodeId).id AS node, score "
        f"ORDER BY score DESC"
    )
    
    result13 = session.run(query13)
    
    top10 = []
    
    for record in result13:
        node_number = record['node']
        score = record['score']
        # print("Node:", node_number, " Score:", score)
        
        # Maintain a heap of size 10 to keep track of top nodes
        if len(top10) < 10:
            heapq.heappush(top10, (score, node_number))
        else:
            heapq.heappushpop(top10, (score, node_number))
    
    # Print the top 10 nodes and their scores
    print("Top 10 nodes by centrality: ")
    for score, node_number in sorted(top10, reverse=True):
        print("Node:", node_number, " Score:", score)
        
    print()
            
def connectedComponents():
    # Query 14: Connected components
    print("\n\nConnected components: ")
    query14 = "CALL gds.wcc.stream('myGraph') YIELD nodeId, componentId RETURN gds.util.asNode(nodeId).id AS node, componentId ORDER BY [componentId, node] ASC"

    components = {}
    result14 = session.run(query14)
    for record in result14:
        node_number = record['node']
        component_id = record['componentId']
        # print("Node:", node_number, " Component ID:", component_id)
        
        # components[component_id].append(node_number) if component_id in components else components.update({component_id: [node_number]})
        # Increment the count of nodes for the component_id
        components[component_id] = components.get(component_id, 0) + 1    
                
    for component_id, nodes in components.items():
        # print("Component ID:", component_id, " Number of Nodes:", len(nodes))
        print("Component ID:", component_id, " Number of Nodes:", nodes)
        
    print()
            
def graphSage():
    # Query 15: GraphSAGE algorithm
    print("\n\nGraphSAGE algorithm: ")
    
    query_train = """
        CALL gds.beta.graphSage.train(
            'myGraph',
            {
                modelName: 'graphsage-mean',
                nodeLabels: ['Node'],
                featureProperties: ['id'],
                aggregator: 'mean',
                activationFunction: 'sigmoid',
                sampleSizes: [25, 10],
                degreeAsProperty: true,
                epochs: 5,
                searchDepth: 5,
                batchSize: 1000,
                learningRate: 0.01,
                embeddingSize: 16,
                negativeSampleWeight: 5.0,
                includeProperties: true
            }
        )
        """

    query15 = """
        CALL gds.beta.graphSage.stream('myGraph', {modelName: 'graphsage-mean'})
        YIELD nodeId, embedding
        RETURN gds.util.asNode(nodeId).id AS node, embedding
        ORDER BY node
        """

    result15 = session.run(query15)
    for record in result15:
        node_number = record['node']
        embedding = record['embedding']
        print("Node:", node_number, " Embedding:", embedding)
            

# node1 = 37
node1 = random.randint(1, 100)
node2 = random.randint(1, 100)

query_project = (
                f"CALL gds.graph.project.cypher( "
                f"'myGraph', "
                f"'MATCH (n) RETURN id(n) AS id', "
                f"'MATCH (n)-[:EDGE_TO]->(m) RETURN id(n) AS source, id(m) AS target' "
                f") "
                f"YIELD graphName, nodeCount, relationshipCount "
                f"RETURN graphName, nodeCount, relationshipCount"
            )

session.run(query_project)

query_drop = "CALL gds.graph.drop('myGraph')"

for node1 in range(100, 1000):
    for node2 in range(100, 1000):
        try:
            if(commonNeighbors(node1, node2) > 0):
                print("\n\nCommon connections from nodes ", node1, " and ", node2, " :")
                break
        except Exception as e:
            print("Error in commonNeighbors: ", e)
        
session.run(query_drop)
        
# # Close the session & driver connection
session.close()
driver.close()

exit()

try:
    countNodes()
except Exception as e:
    print("Error in countNodes: ", e)

try:
    # allNodes()
    pass
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

try:
    communityDetection()
except Exception as e:
    print("Error in communityDetection: ", e)

try:
    pageRank()
except Exception as e:
    print("Error in pageRank: ", e)

try:
    centrality()
except Exception as e:
    print("Error in centrality: ", e)

try:
    connectedComponents()
except Exception as e:
    print("Error in connectedComponents: ", e)

# try:
#     graphSage()
# except Exception as e:
#     print("Error in graphSage: ", e)

session.run(query_drop)
        
# # Close the session & driver connection
session.close()
driver.close()

exit()