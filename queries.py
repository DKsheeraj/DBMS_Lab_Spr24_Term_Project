# Queries

class Queries:
    def __init__(self, session):
        self.sesssion = session
        
    def createProjection(self):
        query_project = (
                        f"CALL gds.graph.project.cypher( "
                        f"'myGraph', "
                        f"'MATCH (n) RETURN id(n) AS id', "
                        f"'MATCH (n)-[:EDGE_TO]->(m) RETURN id(n) AS source, id(m) AS target' "
                        f") "
                        f"YIELD graphName, nodeCount, relationshipCount "
                        f"RETURN graphName, nodeCount, relationshipCount"
                    )

        self.session.run(query_project)
        
    def dropProjection(self):
        query_drop = "CALL gds.graph.drop('myGraph')"
        self.session.run(query_drop)

    def countNodes(self):
        # Query 1: Get the count of nodes in the graph
        print("\n\nNumber of nodes in the graph: ")
        query1 = "MATCH (n) RETURN count(n) AS node_count"

        result1 = self.session.run(query1)
        for record in result1:
            node_count = record["node_count"]
            print("Total nodes count:", node_count)
            
    def allNodes(self):
        # Query 2: Get all nodes in the graph
        print("\n\nNodes in the graph: ")
        query2 = "MATCH (n) RETURN n"

        result2 = self.session.run(query2)
        for record in result2:
            node_number = record['n']['id']
            print(node_number, end=" ")
                
    def connectedNodes(self, node_id):
        # Query 3: Get all nodes connected to a specific node
        print("\n\nNodes that have connection from ", node_id, " :")
        query3 = f"MATCH (n)-[:EDGE_TO]->(m) WHERE n.id = {node_id} RETURN m"
        
        count = 0

        result3 = self.session.run(query3)
        for record in result3:
            node_number = record['m']['id']
            print(node_number, end=" ")
            count += 1
            
        return count
                
    def commonNeighbors(self, node_id1, node_id2):
        # Query 4: Get the common neighbors of two nodes
        print("\n\nCommon connections from nodes ", node_id1, " and ", node_id2, " :")
        query4 = f"MATCH (n1)-[:EDGE_TO]->(m)<-[:EDGE_TO]-(n2) WHERE n1.id = {node_id1} AND n2.id = {node_id2} RETURN m"

        result4 = self.session.run(query4)
        for record in result4:
            node_number = record['m']['id']
            print(node_number, end=" ")
                
    def shortestPath(self, node_id1, node_id2):
        # Query 5: Get the shortest path between two nodes
        print("\n\nShortest path between nodes ", node_id1, " and ", node_id2, " :")
        query5 = f"MATCH path = shortestPath((n1)-[:EDGE_TO*]->(n2)) WHERE n1.id = {node_id1} AND n2.id = {node_id2} RETURN nodes(path)"

        result5 = self.session.run(query5)
        for record in result5:
            nodes_in_path = record['nodes(path)']
            for node in nodes_in_path:
                print(node['id'], end = " ")
            
    def allPaths(self, node_id1, node_id2):
        # Query 6: Get all paths between two nodes
        print("\n\nAll paths between nodes ", node_id1, " and ", node_id2, " :")
        query6 = f"MATCH path = allShortestPaths((n1)-[:EDGE_TO*]-(n2)) WHERE n1.id = {node_id1} AND n2.id = {node_id2} RETURN nodes(path)"

        result6 = self.session.run(query6)
        for record in result6:
            nodes_in_path = record['nodes(path)']
            for node in nodes_in_path:
                print(node['id'], end = " ")
                
            print()
            
    def kLengthPaths(self, node_id1, node_id2, k):
        # Query 7: Get all paths of length k between two nodes
        print("\n\nAll paths of length ", k, " between nodes ", node_id1, " and ", node_id2, " :")

        query7 = (
            f"MATCH path = (n1)-[:EDGE_TO*{k}]-(n2) "
            f"WHERE n1.id = {node_id1} AND n2.id = {node_id2} "
            f"RETURN nodes(path)"
        )
        

        result7 = self.session.run(query7)
        for record in result7:
            nodes_in_path = record['nodes(path)']
            for node in nodes_in_path:
                print(node['id'], end = " ")
                
            print()
                
    def traingleCount(self):
        # Query 8: Get the count of triangles in the graph
        print("\n\nNumber of triangles in the graph: ")
        query8 = "MATCH (a)-[:EDGE_TO]->(b)-[:EDGE_TO]->(c)-[:EDGE_TO]->(a) RETURN count(DISTINCT [a, b, c]) AS triangle_count"

        result8 = self.session.run(query8)
        for record in result8:
            triangle_count = record["triangle_count"]
            print("Total triangles count:", triangle_count)
                
    def trianglesContainingNode(self, node_id):
        # Query to find all triangles containing a specific node
        print("\n\nTriangles containing node ", node_id, ":")
        query9 = (
            f"MATCH (a)-[:EDGE_TO]->(b)-[:EDGE_TO]->(c)-[:EDGE_TO]->(a) "
            f"WHERE a.id = {node_id} OR b.id = {node_id} OR c.id = {node_id} "
            "RETURN DISTINCT a.id, b.id, c.id"
        )
        
        count = 0

        result = self.session.run(query9)
        for record in result:
            count += 1
            
            node_a = record["a.id"]
            node_b = record["b.id"]
            node_c = record["c.id"]
            print("Triangle ", count, ":", (node_a, node_b, node_c))
            
        return count
                
    def clusteringCoefficient(self, node_id):
        # Query to calculate the clustering coefficient of a node
        print("\n\nClustering coefficient of node ", node_id, " :", end = " ")
        
        query1 = (
            f"MATCH (a)-[:EDGE_TO]->(b)-[:EDGE_TO]->(c)-[:EDGE_TO]->(a) "
            f"WHERE a.id = {node_id} OR b.id = {node_id} OR c.id = {node_id} "
            "RETURN DISTINCT a.id, b.id, c.id"
        )
        
        query2 = f"MATCH (n)-[:EDGE_TO]->(m) WHERE n.id = {node_id} RETURN count(m) AS degree"
        

        result1 = self.session.run(query1)
        result2 = self.session.run(query2)
        
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
                
    def communityDetection(self):
        # Query 11: Community detection using the Louvain algorithm
        print("\n\nCommunity detection using the Louvain algorithm: ")
        
        query11 = (
            f"CALL gds.louvain.stream('myGraph') "
            f"YIELD nodeId, communityId "
            f"RETURN gds.util.asNode(nodeId).id AS id, communityId "
            f"ORDER BY [communityId, id] ASC"
        )
        
        result11 = self.session.run(query11)
        for record in result11:
            node_number = record['id']
            community_id = record['communityId']
            print("Node:", node_number, " Community ID:", community_id)
                
    def pageRank(self):
        # Query 12: PageRank algorithm
        print("\n\nPageRank algorithm: ")

        query12 = (
            f"CALL gds.pageRank.stream('myGraph', {{scaler: 'L1Norm'}}) "
            # f"CALL gds.pageRank.stream('myGraph') "
            f"YIELD nodeId, score "
            f"RETURN gds.util.asNode(nodeId).id AS node, score "
            f"ORDER BY score DESC"
        )

        result12 = self.session.run(query12)
        for record in result12:
            node_number = record['node']
            score = record['score']
            print("Node:", node_number, " Score:", score)
                
    def centrality(self):
        # Query 13: Centrality measures
        print("\n\nCentrality measures: ")

        query13 = (
            f"CALL gds.pageRank.stream('myGraph', {{maxIterations: 20, dampingFactor: 0.85}}) "
            f"YIELD nodeId, score "
            f"RETURN gds.util.asNode(nodeId).id AS node, score "
            f"ORDER BY score DESC"
        )
        
        result13 = self.session.run(query13)
        for record in result13:
            node_number = record['node']
            score = record['score']
            print("Node:", node_number, " Score:", score)
                
    def connectedComponents(self):
        # Query 14: Connected components
        print("\n\nConnected components: ")
        query14 = "CALL gds.wcc.stream('myGraph') YIELD nodeId, componentId RETURN gds.util.asNode(nodeId).id AS node, componentId ORDER BY [componentId, node] ASC"

        result14 = self.session.run(query14)
        for record in result14:
            node_number = record['node']
            component_id = record['componentId']
            print("Node:", node_number, " Component ID:", component_id)
                
    def graphSage(self):
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

        result15 = self.session.run(query15)
        for record in result15:
            node_number = record['node']
            embedding = record['embedding']
            print("Node:", node_number, " Embedding:", embedding)