import sys
from neo4j import GraphDatabase

if len(sys.argv) < 2:
    print("Usage: python dataset.py <load>")
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

# Query 1: Get all nodes in the graph
print("\nNodes in the graph: ")
query1 = "MATCH (n) RETURN n"
with driver.session() as session:
    result1 = session.run(query1)
    for record in result1:
        node_number = record['n']['id']
        print(node_number, end=" ")

# Query 2: Get all nodes connected to a specific node
node_id = 1  # Replace with the desired node ID
print("\n\nNodes connected to a node ", node_id, " :")
query2 = f"MATCH (n)-[:CONNECTED_TO]->(m) WHERE n.id = {node_id} RETURN m"
with driver.session() as session:
    result2 = session.run(query2)
    for record in result2:
        node_number = record['m']['id']
        print(node_number, end=" ")

# Query 3: Get the count of nodes in the graph
print("\n\nNumber of nodes in the graph: ")
query3 = "MATCH (n) RETURN count(n) AS node_count"
with driver.session() as session:
    result3 = session.run(query3)
    for record in result3:
        node_count = record["node_count"]
        print("Total nodes count:", node_count)
        
# # Close the session & driver connection
session.close()
driver.close()

exit()