import io
# from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
from neo4j import GraphDatabase
import re
from tabulate import tabulate

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

class GraphDatabaseGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Database GUI")
        
        # Neo4j connection details
        self.uri = "neo4j://localhost:7687"
        self.username = "neo4j"
        self.password = "8985847358"

        # Connect to Neo4j
        self.driver = None
        self.session = None

        # Create custom style
        self.style = ttk.Style()
        self.style.configure("Custom.TButton", foreground="black", background="#CDCDCD", padding=10, font=("Sans Serif", 10), bordercolor="#333333")  # Change font to sans serif and border color
        self.style.configure("Custom.TLabel", foreground="black", background="#F0F0F0", font=("Sans Serif", 10))  # Change font to sans serif
        self.style.configure("Custom.TEntry", foreground="black", background="white", font=("Sans Serif", 10))  # Change font to sans serif

        # Create left frame with scrollbar
        self.left_frame = ttk.Frame(root)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.left_canvas = tk.Canvas(self.left_frame)
        self.left_scrollbar = ttk.Scrollbar(self.left_frame, orient=tk.VERTICAL, command=self.left_canvas.yview)
        self.left_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.left_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.left_canvas.configure(yscrollcommand=self.left_scrollbar.set)

        self.left_frame_inner = ttk.Frame(self.left_canvas)
        self.left_canvas.create_window((0, 0), window=self.left_frame_inner, anchor=tk.NW)

        # Add elements to the inner frame
        self.label = ttk.Label(self.left_frame_inner, text="Graph Database GUI", style="Custom.TLabel")
        self.label.pack(pady=10)

        self.connect_button = ttk.Button(self.left_frame_inner, text="Connect to Neo4j", style="Custom.TButton", command=self.connect_to_neo4j)
        self.connect_button.pack(pady=5)

        self.open_button = ttk.Button(self.left_frame_inner, text="Open Dataset File", style="Custom.TButton", command=self.open_dataset_file, state=tk.DISABLED)
        self.open_button.pack(pady=5)

        self.query1_button = ttk.Button(self.left_frame_inner, text="Create Projection", style="Custom.TButton", command=self.createProjection, state=tk.DISABLED)
        self.query1_button.pack(pady=5)

        self.query2_button = ttk.Button(self.left_frame_inner, text="Drop Projection", style="Custom.TButton", command=self.dropProjection, state=tk.DISABLED)
        self.query2_button.pack(pady=5)

        self.query3_button = ttk.Button(self.left_frame_inner, text="Count Nodes", style="Custom.TButton", command=self.countNodes, state=tk.DISABLED)
        self.query3_button.pack(pady=5)

        self.query4_button = ttk.Button(self.left_frame_inner, text="All Nodes", style="Custom.TButton", command=self.allNodes, state=tk.DISABLED)
        self.query4_button.pack(pady=5)

        self.query5_button = ttk.Button(self.left_frame_inner, text="Connected Nodes", style="Custom.TButton", command=self.connectedNodes, state=tk.DISABLED)
        self.query5_button.pack(pady=5)

        self.query6_button = ttk.Button(self.left_frame_inner, text="Common Neighbours", style="Custom.TButton", command=self.commonNeighbors, state=tk.DISABLED)
        self.query6_button.pack(pady=5)

        self.query7_button = ttk.Button(self.left_frame_inner, text="Shortest Path", style="Custom.TButton", command=self.shortestPath, state=tk.DISABLED)
        self.query7_button.pack(pady=5)
        
        # self.left_frame_inner.bind("<Configure>", self.on_configure)
        
        self.query8_button = ttk.Button(self.left_frame_inner, text="All Paths", style="Custom.TButton", command=self.allPaths, state=tk.DISABLED)
        self.query8_button.pack(pady=5)

        self.query9_button = ttk.Button(self.left_frame_inner, text="K Length Paths", style="Custom.TButton", command=self.kLengthPaths, state=tk.DISABLED)
        self.query9_button.pack(pady=5)

        self.query10_button = ttk.Button(self.left_frame_inner, text="Triangle Count", style="Custom.TButton", command=self.triangleCount , state=tk.DISABLED)
        self.query10_button.pack(pady=5)

        self.query11_button = ttk.Button(self.left_frame_inner, text="Triangles containing Node", style="Custom.TButton", command=self.trianglesContainingNode, state=tk.DISABLED)
        self.query11_button.pack(pady=5)

        self.query12_button = ttk.Button(self.left_frame_inner, text="Clustering Coefficient", style="Custom.TButton", command=self.clusteringCoefficient , state=tk.DISABLED)
        self.query12_button.pack(pady=5)

        self.query13_button = ttk.Button(self.left_frame_inner, text="Community Detection", style="Custom.TButton", command=self.communityDetection , state=tk.DISABLED)
        self.query13_button.pack(pady=5)

        self.query14_button = ttk.Button(self.left_frame_inner, text="Page Rank", style="Custom.TButton", command=self.pageRank , state=tk.DISABLED)
        self.query14_button.pack(pady=5)

        self.query15_button = ttk.Button(self.left_frame_inner, text="Centrality", style="Custom.TButton", command=self.centrality , state=tk.DISABLED)
        self.query15_button.pack(pady=5)

        self.query16_button = ttk.Button(self.left_frame_inner, text="Connected Components", style="Custom.TButton", command=self.connectedComponents , state=tk.DISABLED)
        self.query16_button.pack(pady=5)

        self.query17_button = ttk.Button(self.left_frame_inner, text="Graph Sage", style="Custom.TButton", command=self.graphSage , state=tk.DISABLED)
        self.query17_button.pack(pady=5)
        
        # self.query17_button = ttk.Button(root, text="Graph Sage", style="Custom.TButton", command=self.graphSage, state=tk.DISABLED)
        # self.query17_button.pack(pady=5)

        # Configure the left canvas scrollregion
        self.left_frame_inner.update_idletasks()
        self.left_canvas.config(scrollregion=self.left_canvas.bbox("all"))

        
        self.result_label = ScrolledText(root, height=20, width=120, font=("Sans Serif", 10))
        self.result_label.pack(pady=10)

        self.image_label = tk.Label(root)
        self.image_label.pack(pady=10)

    def connect_to_neo4j(self):
        try:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.username, self.password))
            self.session = self.driver.session()
            self.result_label.insert(tk.END, "Successfully connected to Neo4j!\n")
            self.open_button.config(state=tk.NORMAL)
            self.query1_button.config(state=tk.NORMAL)
            self.query2_button.config(state=tk.NORMAL)
            self.query3_button.config(state=tk.NORMAL)
            self.query4_button.config(state=tk.NORMAL)
            self.query5_button.config(state=tk.NORMAL)
            self.query6_button.config(state=tk.NORMAL)
            self.query7_button.config(state=tk.NORMAL)
            self.query8_button.config(state=tk.NORMAL)
            self.query9_button.config(state=tk.NORMAL)
            self.query10_button.config(state=tk.NORMAL)
            self.query11_button.config(state=tk.NORMAL)
            self.query12_button.config(state=tk.NORMAL)
            self.query13_button.config(state=tk.NORMAL)
            self.query14_button.config(state=tk.NORMAL)
            self.query15_button.config(state=tk.NORMAL)
            self.query16_button.config(state=tk.NORMAL)
            self.query17_button.config(state=tk.NORMAL)

            # Display image from Neo4j
            # self.display_image_from_neo4j()
        except Exception as e:
            self.result_label.insert(tk.END, f"Failed to connect to Neo4j: {e}\n")

    def open_dataset_file(self):
        filename = filedialog.askopenfilename(title="Select Dataset File")
        if filename:
            try:
                with open(filename, "r") as file:
                    # Assuming sample_dataset.txt contains source and target nodes separated by tabs
                    for line in file:
                        
                        if line[0] == '#': continue # Skip lines that are comments.

                        source, target = line.strip().split("\t")
                        query = (
                            f"MERGE (source:Node {{id: {source}}})"
                            f"MERGE (target:Node {{id: {target}}})"
                            f"MERGE (source)-[:CONNECTED_TO]->(target)"
                        )
                        self.session.run(query)
                self.result_label.insert(tk.END, "Data loaded into Neo4j successfully!\n")
            except Exception as e:
                self.result_label.insert(tk.END, f"Error loading data into Neo4j: {e}\n")

    def createProjection(self):
        try:
            
            create_query = (
                f"CALL gds.graph.project.cypher( "
                f"'myGraph', "
                f"'MATCH (n) RETURN id(n) AS id', "
                f"'MATCH (n)-[:CONNECTED_TO]->(m) RETURN id(n) AS source, id(m) AS target' "
                f") "
                f"YIELD graphName, nodeCount, relationshipCount "
                f"RETURN graphName, nodeCount, relationshipCount"
            )
            self.session.run(create_query)
            
            self.result_label.insert(tk.END, "Projection created successfully!\n")
        except Exception as e:
            self.result_label.insert(tk.END, f"Error creating projection: {e}\n")



    def dropProjection(self):
        try:
            query_drop = "CALL gds.graph.drop('myGraph')"
            self.session.run(query_drop)
            self.result_label.insert(tk.END, "Projection dropped successfully!\n")
        except Exception as e:
            if "Graph with name 'myGraph' does not exist on database" in str(e):
                self.result_label.insert(tk.END, "The graph 'myGraph' does not exist in the current database.\n")
            else:
                self.result_label.insert(tk.END, f"Error dropping projection: {e}\n")

    
    def countNodes(self):
        try:
            # Query: Get the count of nodes in the graph
            query = "PROFILE MATCH (n) RETURN count(n) AS node_count"

            result = self.session.run(query)
            for record in result:
                node_count = record["node_count"]
                self.result_label.insert(tk.END, f"Total nodes count: {node_count}\n")
            
            summary = result.consume()

            self.result_label.insert(tk.END, f"\n\nProfiling Information:\n\n")
            # self.result_label.insert(tk.END, f"{summary.profile['args']['string-representation']}\n")
            profile_info = parse_profile(summary.profile['args']['string-representation'])

            for info in profile_info["operators"]:
                if info["Operator"] == "Operator": 
                    self.result_label.insert(tk.END, f'Operator\t\t|Page Cache Hits/Misses\t\t\t|Time (ms)\t|DB Hits\t|Memory (Bytes)\t|\n')
                    continue

                self.result_label.insert(tk.END, f'{info["Operator"]}\t\t|')
                self.result_label.insert(tk.END, f'{info["Page Cache Hits/Misses"]}\t\t\t|{info["Time (ms)"]}\t|{info["DB Hits"]}\t|{info["Memory (Bytes)"]}\t\t|\n')

            self.result_label.insert(tk.END, f'\nTotal Database Accesses: {profile_info["database_accesses"]}\nTotal Allocated Memory: {profile_info["allocated_memory"]}\n\n')

        except Exception as e:
            self.result_label.insert(tk.END, f"Error counting nodes: {e}\n")

    def allNodes(self):
        try:
            # Query: Get all nodes in the graph
            query = "PROFILE MATCH (n) RETURN n"

            result = self.session.run(query)
            nodes = [str(record['n']['id']) for record in result]  # Convert node IDs to strings
            self.result_label.insert(tk.END, f"Nodes in the graph: {' '.join(nodes)}\n")

            summary = result.consume()

            self.result_label.insert(tk.END, f"\n\nProfiling Information:\n\n")
            #self.result_label.insert(tk.END, f"{summary.profile['args']['string-representation']}\n")
            profile_info = parse_profile(summary.profile['args']['string-representation'])

            for info in profile_info["operators"]:
                if info["Operator"] == "Operator": 
                    self.result_label.insert(tk.END, f'Operator\t\t|Page Cache Hits/Misses\t\t\t|Time (ms)\t|DB Hits\t|Memory (Bytes)\t|\n')
                    continue

                self.result_label.insert(tk.END, f'{info["Operator"]}\t\t|')
                self.result_label.insert(tk.END, f'{info["Page Cache Hits/Misses"]}\t\t\t|{info["Time (ms)"]}\t|{info["DB Hits"]}\t|{info["Memory (Bytes)"]}\t\t|\n')

            self.result_label.insert(tk.END, f'\nTotal Database Accesses: {profile_info["database_accesses"]}\nTotal Allocated Memory: {profile_info["allocated_memory"]}\n\n')

        except Exception as e:
            self.result_label.insert(tk.END, f"Error fetching nodes: {e}\n")

    def connectedNodes(self):
        self.result_label.delete('1.0', tk.END)
        
        # Create a label and entry widget for node ID input
        node_id_label = ttk.Label(self.root, text="Enter Node ID:", style="Custom.TLabel")
        node_id_label.pack()
        
        node_id_entry = ttk.Entry(self.root, font=("Sans Serif", 10))
        node_id_entry.pack()
        
        # Define a function to execute the query when the button is clicked
        def execute_query():
            # Get the node ID from the entry widget
            node_id = node_id_entry.get()
            
            # Execute the query
            query = f"PROFILE MATCH (n)-[:CONNECTED_TO]->(m) WHERE n.id = {node_id} RETURN m"
            result = self.session.run(query)
            
            # Build the string to display in the output box
            self.result_label.insert(tk.END, f"Nodes connected to {node_id}:\n")
            output = " ".join([str(record['m']['id']) for record in result])
            
            # Display the output in the result_label
            self.result_label.insert(tk.END, output)

            summary = result.consume()

            self.result_label.insert(tk.END, f"\n\nProfiling Information:\n\n")
            #self.result_label.insert(tk.END, f"{summary.profile['args']['string-representation']}\n")
            profile_info = parse_profile(summary.profile['args']['string-representation'])

            for info in profile_info["operators"]:
                if info["Operator"] == "Operator": 
                    self.result_label.insert(tk.END, f'Operator\t\t|Page Cache Hits/Misses\t\t\t|Time (ms)\t|DB Hits\t|Memory (Bytes)\t|\n')
                    continue

                self.result_label.insert(tk.END, f'{info["Operator"]}\t\t|')
                self.result_label.insert(tk.END, f'{info["Page Cache Hits/Misses"]}\t\t\t|{info["Time (ms)"]}\t|{info["DB Hits"]}\t|{info["Memory (Bytes)"]}\t\t|\n')

            self.result_label.insert(tk.END, f'\nTotal Database Accesses: {profile_info["database_accesses"]}\nTotal Allocated Memory: {profile_info["allocated_memory"]}\n\n')
            
            # Destroy the entry box and execute button
            node_id_label.pack_forget()
            node_id_entry.pack_forget()
            execute_button.pack_forget()

            # Display image from Neo4j
            self.display_image_from_neo4j()
        
        # Create a button to execute the query
        execute_button = ttk.Button(self.root, text="Execute", style="Custom.TButton", command=execute_query)
        execute_button.pack()

    
    def commonNeighbors(self):
        self.result_label.delete('1.0', tk.END)
        
        # Create a label and entry widget for node ID input
        node_id1_label = ttk.Label(self.root, text="Enter Node ID 1:", style="Custom.TLabel")
        node_id1_label.pack()
        
        node_id1_entry = ttk.Entry(self.root, font=("Sans Serif", 10))
        node_id1_entry.pack()

        node_id2_label = ttk.Label(self.root, text="Enter Node ID 2:", style="Custom.TLabel")
        node_id2_label.pack()
        
        node_id2_entry = ttk.Entry(self.root, font=("Sans Serif", 10))
        node_id2_entry.pack()
        
        # Define a function to execute the query when the button is clicked
        def execute_query():
            # Get the node ID from the entry widget
            node_id1 = node_id1_entry.get()
            node_id2 = node_id2_entry.get()
            
            # Execute the query
            query = f"PROFILE MATCH (n1)-[:CONNECTED_TO]->(m)<-[:CONNECTED_TO]-(n2) WHERE n1.id = {node_id1} AND n2.id = {node_id2} RETURN m"
            result = self.session.run(query)

            if result.peek() is None:
                self.result_label.insert(tk.END, "No such nodes found.\n")
            else:
                # Build the string to display in the output box
                self.result_label.insert(tk.END, f"Common neighbours of {node_id1} and {node_id2}:\n")
                output = " ".join([str(record['m']['id']) for record in result])
                
                # Display the output in the result_label
                self.result_label.insert(tk.END, output)

            summary = result.consume()

            self.result_label.insert(tk.END, f"\n\nProfiling Information:\n\n")
            #self.result_label.insert(tk.END, f"{summary.profile['args']['string-representation']}\n")
            profile_info = parse_profile(summary.profile['args']['string-representation'])

            for info in profile_info["operators"]:
                if info["Operator"] == "Operator": 
                    self.result_label.insert(tk.END, f'Operator\t\t|Page Cache Hits/Misses\t\t\t|Time (ms)\t|DB Hits\t|Memory (Bytes)\t|\n')
                    continue

                self.result_label.insert(tk.END, f'{info["Operator"]}\t\t|')
                self.result_label.insert(tk.END, f'{info["Page Cache Hits/Misses"]}\t\t\t|{info["Time (ms)"]}\t|{info["DB Hits"]}\t|{info["Memory (Bytes)"]}\t\t|\n')

            self.result_label.insert(tk.END, f'\nTotal Database Accesses: {profile_info["database_accesses"]}\nTotal Allocated Memory: {profile_info["allocated_memory"]}\n\n')
            
            # Destroy the entry box and execute button
            node_id1_label.pack_forget()
            node_id1_entry.pack_forget()
            node_id2_label.pack_forget()
            node_id2_entry.pack_forget()
            execute_button.pack_forget()

            # Display image from Neo4j
            self.display_image_from_neo4j()
        
        # Create a button to execute the query
        execute_button = ttk.Button(self.root, text="Execute", style="Custom.TButton", command=execute_query)
        execute_button.pack()

    def shortestPath(self):
        self.result_label.delete('1.0', tk.END)
        
        # Create a label and entry widget for node ID input
        node_id1_label = ttk.Label(self.root, text="Enter Node ID 1:", style="Custom.TLabel")
        node_id1_label.pack()
        
        node_id1_entry = ttk.Entry(self.root, font=("Sans Serif", 10))
        node_id1_entry.pack()

        node_id2_label = ttk.Label(self.root, text="Enter Node ID 2:", style="Custom.TLabel")
        node_id2_label.pack()
        
        node_id2_entry = ttk.Entry(self.root, font=("Sans Serif", 10))
        node_id2_entry.pack()
        
        # Define a function to execute the query when the button is clicked
        def execute_query():
            node_id1 = node_id1_entry.get()
            node_id2 = node_id2_entry.get()
        # Query: Get the shortest path between two nodes
            print(node_id1)
            print(node_id2)
            query = f"PROFILE MATCH path = shortestPath((n1)-[:CONNECTED_TO*]->(n2)) WHERE n1.id = {node_id1} AND n2.id = {node_id2} RETURN nodes(path)"
            
            # Execute the query
            result = self.session.run(query)
            records = list(result)

            if not records:
                self.result_label.insert(tk.END, "No path found between the nodes.\n")
            else:
                # Build the string to display in the output box
                result_string = f"Shortest path between nodes {node_id1} and {node_id2}: "
                for record in records:  # Iterate over the records list
                    nodes_in_path = record['nodes(path)']
                    for node in nodes_in_path:
                        result_string += f"{node['id']} "
                            
                # Display the output in the result_label
                self.result_label.insert(tk.END, result_string)

            summary = result.consume()

            self.result_label.insert(tk.END, f"\n\nProfiling Information:\n\n")
            #self.result_label.insert(tk.END, f"{summary.profile['args']['string-representation']}\n")
            profile_info = parse_profile(summary.profile['args']['string-representation'])

            for info in profile_info["operators"]:
                if info["Operator"] == "Operator": 
                    self.result_label.insert(tk.END, f'Operator\t\t|Page Cache Hits/Misses\t\t\t|Time (ms)\t|DB Hits\t|Memory (Bytes)\t|\n')
                    continue

                self.result_label.insert(tk.END, f'{info["Operator"]}\t\t|')
                self.result_label.insert(tk.END, f'{info["Page Cache Hits/Misses"]}\t\t\t|{info["Time (ms)"]}\t|{info["DB Hits"]}\t|{info["Memory (Bytes)"]}\t\t|\n')

            self.result_label.insert(tk.END, f'\nTotal Database Accesses: {profile_info["database_accesses"]}\nTotal Allocated Memory: {profile_info["allocated_memory"]}\n\n')

            node_id1_label.pack_forget()
            node_id1_entry.pack_forget()
            node_id2_label.pack_forget()
            node_id2_entry.pack_forget()
            execute_button.pack_forget()
        
        # Create a button to execute the query
        execute_button = ttk.Button(self.root, text="Execute", style="Custom.TButton", command=execute_query)
        execute_button.pack()


    def allPaths(self):
        self.result_label.delete('1.0', tk.END)
        
        # Create a label and entry widget for node ID input
        node_id1_label = ttk.Label(self.root, text="Enter Node ID 1:", style="Custom.TLabel")
        node_id1_label.pack()
        
        node_id1_entry = ttk.Entry(self.root, font=("Sans Serif", 10))
        node_id1_entry.pack()

        node_id2_label = ttk.Label(self.root, text="Enter Node ID 2:", style="Custom.TLabel")
        node_id2_label.pack()
        
        node_id2_entry = ttk.Entry(self.root, font=("Sans Serif", 10))
        node_id2_entry.pack()
        
        # Define a function to execute the query when the button is clicked
        def execute_query():
            # Get the node ID from the entry widget
            node_id1 = node_id1_entry.get()
            node_id2 = node_id2_entry.get()
            
            # Execute the query
            query = f"PROFILE MATCH path = allShortestPaths((n1)-[:CONNECTED_TO*]-(n2)) WHERE n1.id = {node_id1} AND n2.id = {node_id2} RETURN nodes(path)"

            result = self.session.run(query)
            records = list(result)


            if not records:
                self.result_label.insert(tk.END, "No path found between the nodes.\n")
            else:
                # Build the string to display in the output box
                result_string = f"All paths between nodes {node_id1} and {node_id2}: "
                for record in records:  # Iterate over the records list
                    nodes_in_path = record['nodes(path)']
                    for node in nodes_in_path:
                        result_string += f"{node['id']} "

                self.result_label.insert(tk.END, result_string)
                            
                # Display the output in the result_label

            summary = result.consume()

            self.result_label.insert(tk.END, f"\n\nProfiling Information:\n\n")
            #self.result_label.insert(tk.END, f"{summary.profile['args']['string-representation']}\n")
            profile_info = parse_profile(summary.profile['args']['string-representation'])

            for info in profile_info["operators"]:
                if info["Operator"] == "Operator": 
                    self.result_label.insert(tk.END, f'Operator\t\t|Page Cache Hits/Misses\t\t\t|Time (ms)\t|DB Hits\t|Memory (Bytes)\t|\n')
                    continue

                self.result_label.insert(tk.END, f'{info["Operator"]}\t\t|')
                self.result_label.insert(tk.END, f'{info["Page Cache Hits/Misses"]}\t\t\t|{info["Time (ms)"]}\t|{info["DB Hits"]}\t|{info["Memory (Bytes)"]}\t\t|\n')

            self.result_label.insert(tk.END, f'\nTotal Database Accesses: {profile_info["database_accesses"]}\nTotal Allocated Memory: {profile_info["allocated_memory"]}\n\n')
            
            # Destroy the entry box and execute button
            node_id1_label.pack_forget()
            node_id1_entry.pack_forget()
            node_id2_label.pack_forget()
            node_id2_entry.pack_forget()
            execute_button.pack_forget()

            # Display image from Neo4j
            # self.display_image_from_neo4j()
        
        # Create a button to execute the query
        execute_button = ttk.Button(self.root, text="Execute", style="Custom.TButton", command=execute_query)
        execute_button.pack()


    def kLengthPaths(self):
        self.result_label.delete('1.0', tk.END)
        
        # Create a label and entry widget for node ID input
        node_id1_label = ttk.Label(self.root, text="Enter Node ID 1:", style="Custom.TLabel")
        node_id1_label.pack()
        
        node_id1_entry = ttk.Entry(self.root, font=("Sans Serif", 10))
        node_id1_entry.pack()

        node_id2_label = ttk.Label(self.root, text="Enter Node ID 2:", style="Custom.TLabel")
        node_id2_label.pack()
        
        node_id2_entry = ttk.Entry(self.root, font=("Sans Serif", 10))
        node_id2_entry.pack()

        k_label = ttk.Label(self.root, text="Enter Node ID 2:", style="Custom.TLabel")
        k_label.pack()
        
        k_entry = ttk.Entry(self.root, font=("Sans Serif", 10))
        k_entry.pack()
        
        # Define a function to execute the query when the button is clicked
        def execute_query():
            # Get the node ID from the entry widget
            node_id1 = node_id1_entry.get()
            node_id2 = node_id2_entry.get()
            k = k_entry.get()
            
            # Execute the query
            query =  (
                f"PROFILE MATCH path = (n1)-[:CONNECTED_TO*{k}]-(n2) "
                f"WHERE n1.id = {node_id1} AND n2.id = {node_id2} "
                f"RETURN nodes(path)"
            )

            result = self.session.run(query)
            records = list(result)


            if not records:
                self.result_label.insert(tk.END, "No such path found between the nodes.\n")
            else:
                # Build the string to display in the output box
                result_string = f"{k} length path {node_id1} and {node_id2}: "
                for record in records:  # Iterate over the records list
                    nodes_in_path = record['nodes(path)']
                    for node in nodes_in_path:
                        result_string += f"{node['id']} "

                self.result_label.insert(tk.END, result_string)
                            
                # Display the output in the result_label

            summary = result.consume()

            self.result_label.insert(tk.END, f"\n\nProfiling Information:\n\n")
            #self.result_label.insert(tk.END, f"{summary.profile['args']['string-representation']}\n")
            profile_info = parse_profile(summary.profile['args']['string-representation'])

            for info in profile_info["operators"]:
                if info["Operator"] == "Operator": 
                    self.result_label.insert(tk.END, f'Operator\t\t|Page Cache Hits/Misses\t\t\t|Time (ms)\t|DB Hits\t|Memory (Bytes)\t|\n')
                    continue

                self.result_label.insert(tk.END, f'{info["Operator"]}\t\t|')
                self.result_label.insert(tk.END, f'{info["Page Cache Hits/Misses"]}\t\t\t|{info["Time (ms)"]}\t|{info["DB Hits"]}\t|{info["Memory (Bytes)"]}\t\t|\n')

            self.result_label.insert(tk.END, f'\nTotal Database Accesses: {profile_info["database_accesses"]}\nTotal Allocated Memory: {profile_info["allocated_memory"]}\n\n')
            
            # Destroy the entry box and execute button
            node_id1_label.pack_forget()
            node_id1_entry.pack_forget()
            node_id2_label.pack_forget()
            node_id2_entry.pack_forget()
            k_label.pack_forget()
            k_entry.pack_forget()
            execute_button.pack_forget()

            # Display image from Neo4j
            # self.display_image_from_neo4j()
        
        # Create a button to execute the query
        execute_button = ttk.Button(self.root, text="Execute", style="Custom.TButton", command=execute_query)
        execute_button.pack()

    def triangleCount(self):
        # Query 8: Get the count of triangles in the graph
        query = "PROFILE MATCH (a)-[:CONNECTED_TO]->(b)-[:CONNECTED_TO]->(c)-[:CONNECTED_TO]->(a) RETURN count(DISTINCT [a, b, c]) AS triangle_count"

        result = self.session.run(query)
        
        print("Result:", result)
        
        # Check if the result is not empty
        if not result:
            print("No triangles found.")
            self.result_label.insert(tk.END, "No triangles found in the graph.\n")
        else:
            for record in result:
                triangle_count = record["triangle_count"]
                print("Total triangles count:", triangle_count)
                self.result_label.insert(tk.END, f"Total triangles count: {triangle_count}\n")

        summary = result.consume()

        self.result_label.insert(tk.END, f"\n\nProfiling Information:\n\n")
        #self.result_label.insert(tk.END, f"{summary.profile['args']['string-representation']}\n")
        profile_info = parse_profile(summary.profile['args']['string-representation'])

        for info in profile_info["operators"]:
            if info["Operator"] == "Operator": 
                self.result_label.insert(tk.END, f'Operator\t\t|Page Cache Hits/Misses\t\t\t|Time (ms)\t|DB Hits\t|Memory (Bytes)\t|\n')
                continue

            self.result_label.insert(tk.END, f'{info["Operator"]}\t\t|')
            self.result_label.insert(tk.END, f'{info["Page Cache Hits/Misses"]}\t\t\t|{info["Time (ms)"]}\t|{info["DB Hits"]}\t|{info["Memory (Bytes)"]}\t\t|\n')

        self.result_label.insert(tk.END, f'\nTotal Database Accesses: {profile_info["database_accesses"]}\nTotal Allocated Memory: {profile_info["allocated_memory"]}\n\n')


    def trianglesContainingNode(self):
        self.result_label.delete('1.0', tk.END)
        
        # Create a label and entry widget for node ID input
        node_id_label = ttk.Label(self.root, text="Enter Node ID:", style="Custom.TLabel")
        node_id_label.pack()
        
        node_id_entry = ttk.Entry(self.root, font=("Sans Serif", 10))
        node_id_entry.pack()
        
        # Define a function to execute the query when the button is clicked
        def execute_query():
            # Get the node ID from the entry widget
            node_id = node_id_entry.get()
            
            # Execute the query
            query = (
                f"PROFILE MATCH (a)-[:CONNECTED_TO]->(b)-[:CONNECTED_TO]->(c)-[:CONNECTED_TO]->(a) "
                f"WHERE a.id = {node_id} OR b.id = {node_id} OR c.id = {node_id} "
                "RETURN DISTINCT a.id, b.id, c.id"
            )
            result = self.session.run(query)
            # print(result)
            
            # Check if the result is not empty
            if not result:
                print("No triangles found.")
                self.result_label.insert(tk.END, f"No triangles found containing node {node_id}.\n")
            else:
                # Display the output in the result_label
                
                count = 0
                for record in result:
                    if(count == 0):
                        self.result_label.insert(tk.END, f"Triangles containing node {node_id}:\n")
                    count += 1
                    node_a = record["a.id"]
                    node_b = record["b.id"]
                    node_c = record["c.id"]
                    self.result_label.insert(tk.END, f"Triangle {count}: ({node_a}, {node_b}, {node_c})\n")

                if(count == 0):
                    self.result_label.insert(tk.END, f"No triangles found containing node {node_id}.\n")

            summary = result.consume()

            self.result_label.insert(tk.END, f"\n\nProfiling Information:\n\n")
            #self.result_label.insert(tk.END, f"{summary.profile['args']['string-representation']}\n")
            profile_info = parse_profile(summary.profile['args']['string-representation'])

            for info in profile_info["operators"]:
                if info["Operator"] == "Operator": 
                    self.result_label.insert(tk.END, f'Operator\t\t|Page Cache Hits/Misses\t\t\t|Time (ms)\t|DB Hits\t|Memory (Bytes)\t|\n')
                    continue

                self.result_label.insert(tk.END, f'{info["Operator"]}\t\t|')
                self.result_label.insert(tk.END, f'{info["Page Cache Hits/Misses"]}\t\t\t|{info["Time (ms)"]}\t|{info["DB Hits"]}\t|{info["Memory (Bytes)"]}\t\t|\n')

            self.result_label.insert(tk.END, f'\nTotal Database Accesses: {profile_info["database_accesses"]}\nTotal Allocated Memory: {profile_info["allocated_memory"]}\n\n')

            # Destroy the entry box and execute button
            node_id_label.pack_forget()
            node_id_entry.pack_forget()
            execute_button.pack_forget()

            # Display image from Neo4j
            # self.display_image_from_neo4j()
        
        # Create a button to execute the query
        execute_button = ttk.Button(self.root, text="Execute", style="Custom.TButton", command=execute_query)
        execute_button.pack()


    def clusteringCoefficient(self):
        # Clear previous results from the result label
        self.result_label.delete('1.0', tk.END)
        
        # Create a label and entry widget for node ID input
        node_id_label = ttk.Label(self.root, text="Enter Node ID:", style="Custom.TLabel")
        node_id_label.pack()
        
        node_id_entry = ttk.Entry(self.root, font=("Sans Serif", 10))
        node_id_entry.pack()
        
        # Define a function to execute the query when the button is clicked
        def execute_query():
            # Get the node ID from the entry widget
            node_id = node_id_entry.get()
            
            # Query to calculate the clustering coefficient of a node
           
            query1 = (
                f"PROFILE MATCH (a)-[:CONNECTED_TO]->(b)-[:CONNECTED_TO]->(c)-[:CONNECTED_TO]->(a) "
                f"WHERE a.id = {node_id} OR b.id = {node_id} OR c.id = {node_id} "
                "RETURN DISTINCT a.id, b.id, c.id"
            )
            
            query2 = f"PROFILE MATCH (n)-[:EDGE_TO]->(m) WHERE n.id = {node_id} RETURN count(m) AS degree"

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
            
            # Display the result in the result_label
            self.result_label.insert(tk.END, f"Clustering coefficient of node {node_id}: {clust_coeff}\n")

            summary = result1.consume()

            self.result_label.insert(tk.END, f"\n\nProfiling Information:\n\n")
            #self.result_label.insert(tk.END, f"{summary.profile['args']['string-representation']}\n")
            profile_info = parse_profile(summary.profile['args']['string-representation'])

            for info in profile_info["operators"]:
                if info["Operator"] == "Operator": 
                    self.result_label.insert(tk.END, f'Operator\t\t|Page Cache Hits/Misses\t\t\t|Time (ms)\t|DB Hits\t|Memory (Bytes)\t|\n')
                    continue

                self.result_label.insert(tk.END, f'{info["Operator"]}\t\t|')
                self.result_label.insert(tk.END, f'{info["Page Cache Hits/Misses"]}\t\t\t|{info["Time (ms)"]}\t|{info["DB Hits"]}\t|{info["Memory (Bytes)"]}\t\t|\n')

            self.result_label.insert(tk.END, f'\nTotal Database Accesses: {profile_info["database_accesses"]}\nTotal Allocated Memory: {profile_info["allocated_memory"]}\n\n')

            summary = result2.consume()
            #self.result_label.insert(tk.END, f"{summary.profile['args']['string-representation']}\n")
            profile_info = parse_profile(summary.profile['args']['string-representation'])

            for info in profile_info["operators"]:
                if info["Operator"] == "Operator": 
                    self.result_label.insert(tk.END, f'Operator\t\t|Page Cache Hits/Misses\t\t\t|Time (ms)\t|DB Hits\t|Memory (Bytes)\t|\n')
                    continue

                self.result_label.insert(tk.END, f'{info["Operator"]}\t\t|')
                self.result_label.insert(tk.END, f'{info["Page Cache Hits/Misses"]}\t\t\t|{info["Time (ms)"]}\t|{info["DB Hits"]}\t|{info["Memory (Bytes)"]}\t\t|\n')

            self.result_label.insert(tk.END, f'\nTotal Database Accesses: {profile_info["database_accesses"]}\nTotal Allocated Memory: {profile_info["allocated_memory"]}\n\n')
            
            # Destroy the entry box, label, and execute button
            node_id_label.pack_forget()
            node_id_entry.pack_forget()
            execute_button.pack_forget()

        # Create a button to execute the query
        execute_button = ttk.Button(self.root, text="Execute", style="Custom.TButton", command=execute_query)
        execute_button.pack()

    
    def communityDetection(self):
        # Clear previous results from the result label
        self.result_label.delete('1.0', tk.END)
        
        # Query to perform community detection using the Louvain algorithm
        query = (
            f"PROFILE CALL gds.louvain.stream('myGraph') "
            f"YIELD nodeId, communityId "
            f"RETURN gds.util.asNode(nodeId).id AS id, communityId "
            f"ORDER BY [communityId, id] ASC"
        )
        
        # Execute the query
        result = self.session.run(query)
        
        # Display the results in the result_label
        self.result_label.insert(tk.END, "Community detection using the Louvain algorithm:\n")
        for record in result:
            node_number = record['id']
            community_id = record['communityId']
            self.result_label.insert(tk.END, f"Node: {node_number} Community ID: {community_id}\n")

        summary = result.consume()

        self.result_label.insert(tk.END, f"\n\nProfiling Information:\n\n")
        #self.result_label.insert(tk.END, f"{summary.profile['args']['string-representation']}\n")
        profile_info = parse_profile(summary.profile['args']['string-representation'])

        for info in profile_info["operators"]:
            if info["Operator"] == "Operator": 
                self.result_label.insert(tk.END, f'Operator\t\t|Page Cache Hits/Misses\t\t\t|Time (ms)\t|DB Hits\t|Memory (Bytes)\t|\n')
                continue

            self.result_label.insert(tk.END, f'{info["Operator"]}\t\t|')
            self.result_label.insert(tk.END, f'{info["Page Cache Hits/Misses"]}\t\t\t|{info["Time (ms)"]}\t|{info["DB Hits"]}\t|{info["Memory (Bytes)"]}\t\t|\n')

        self.result_label.insert(tk.END, f'\nTotal Database Accesses: {profile_info["database_accesses"]}\nTotal Allocated Memory: {profile_info["allocated_memory"]}\n\n')

    def pageRank(self):
        # Clear previous results from the result label
        self.result_label.delete('1.0', tk.END)
        
        # Query 12: PageRank algorithm
        self.result_label.insert(tk.END, "PageRank algorithm:\n")
        
        query12 = (
            f"PROFILE CALL gds.pageRank.stream('myGraph', {{scaler: 'L1Norm'}}) "
            f"YIELD nodeId, score "
            f"RETURN gds.util.asNode(nodeId).id AS node, score "
            f"ORDER BY score DESC"
        )

        result12 = self.session.run(query12)
        for record in result12:
            node_number = record['node']
            score = record['score']
            result_string = f"Node: {node_number}, Score: {score}\n"
            self.result_label.insert(tk.END, result_string)

        summary = result12.consume()

        self.result_label.insert(tk.END, f"\n\nProfiling Information:\n\n")
        #self.result_label.insert(tk.END, f"{summary.profile['args']['string-representation']}\n")
        profile_info = parse_profile(summary.profile['args']['string-representation'])

        for info in profile_info["operators"]:
            if info["Operator"] == "Operator": 
                self.result_label.insert(tk.END, f'Operator\t\t|Page Cache Hits/Misses\t\t\t|Time (ms)\t|DB Hits\t|Memory (Bytes)\t|\n')
                continue

            self.result_label.insert(tk.END, f'{info["Operator"]}\t\t|')
            self.result_label.insert(tk.END, f'{info["Page Cache Hits/Misses"]}\t\t\t|{info["Time (ms)"]}\t|{info["DB Hits"]}\t|{info["Memory (Bytes)"]}\t\t|\n')

        self.result_label.insert(tk.END, f'\nTotal Database Accesses: {profile_info["database_accesses"]}\nTotal Allocated Memory: {profile_info["allocated_memory"]}\n\n')


    def centrality(self):
        # Clear previous results from the result label
        self.result_label.delete('1.0', tk.END)
        
        # Query 13: Centrality measures
        self.result_label.insert(tk.END, "Centrality measures:\n")
        
        query13 = (
            f"PROFILE CALL gds.pageRank.stream('myGraph', {{maxIterations: 20, dampingFactor: 0.85}}) "
            f"YIELD nodeId, score "
            f"RETURN gds.util.asNode(nodeId).id AS node, score "
            f"ORDER BY score DESC"
        )
        
        result13 = self.session.run(query13)
        for record in result13:
            node_number = record['node']
            score = record['score']
            result_string = f"Node: {node_number}, Score: {score}\n"
            self.result_label.insert(tk.END, result_string)

        summary = result13.consume()

        self.result_label.insert(tk.END, f"\n\nProfiling Information:\n\n")
        #self.result_label.insert(tk.END, f"{summary.profile['args']['string-representation']}\n")
        profile_info = parse_profile(summary.profile['args']['string-representation'])

        for info in profile_info["operators"]:
            if info["Operator"] == "Operator": 
                self.result_label.insert(tk.END, f'Operator\t\t|Page Cache Hits/Misses\t\t\t|Time (ms)\t|DB Hits\t|Memory (Bytes)\t|\n')
                continue

            self.result_label.insert(tk.END, f'{info["Operator"]}\t\t|')
            self.result_label.insert(tk.END, f'{info["Page Cache Hits/Misses"]}\t\t\t|{info["Time (ms)"]}\t|{info["DB Hits"]}\t|{info["Memory (Bytes)"]}\t\t|\n')

        self.result_label.insert(tk.END, f'\nTotal Database Accesses: {profile_info["database_accesses"]}\nTotal Allocated Memory: {profile_info["allocated_memory"]}\n\n')

    def connectedComponents(self):
        # Clear previous results from the result label
        self.result_label.delete('1.0', tk.END)
        
        # Query 14: Connected components
        self.result_label.insert(tk.END, "Connected components:\n")
        
        query14 = "PROFILE CALL gds.wcc.stream('myGraph') YIELD nodeId, componentId RETURN gds.util.asNode(nodeId).id AS node, componentId ORDER BY [componentId, node] ASC"

        result14 = self.session.run(query14)
        for record in result14:
            node_number = record['node']
            component_id = record['componentId']
            result_string = f"Node: {node_number}, Component ID: {component_id}\n"
            self.result_label.insert(tk.END, result_string)

        summary = result14.consume()

        self.result_label.insert(tk.END, f"\n\nProfiling Information:\n\n")
        #self.result_label.insert(tk.END, f"{summary.profile['args']['string-representation']}\n")
        profile_info = parse_profile(summary.profile['args']['string-representation'])

        for info in profile_info["operators"]:
            if info["Operator"] == "Operator": 
                self.result_label.insert(tk.END, f'Operator\t\t|Page Cache Hits/Misses\t\t\t|Time (ms)\t|DB Hits\t|Memory (Bytes)\t|\n')
                continue

            self.result_label.insert(tk.END, f'{info["Operator"]}\t\t|')
            self.result_label.insert(tk.END, f'{info["Page Cache Hits/Misses"]}\t\t\t|{info["Time (ms)"]}\t|{info["DB Hits"]}\t|{info["Memory (Bytes)"]}\t\t|\n')

        self.result_label.insert(tk.END, f'\nTotal Database Accesses: {profile_info["database_accesses"]}\nTotal Allocated Memory: {profile_info["allocated_memory"]}\n\n')

    def graphSage(self):
        # Clear previous results from the result label
        self.result_label.delete('1.0', tk.END)
        
        # Query 15: GraphSAGE algorithm
        self.result_label.insert(tk.END, "GraphSAGE algorithm:\n")
        
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
        
        # self.session.run(query_train).consume()

        query15 = """
            PROFILE CALL gds.beta.graphSage.stream('myGraph', {modelName: 'graphsage-mean'})
            YIELD nodeId, embedding
            RETURN gds.util.asNode(nodeId).id AS node, embedding
            ORDER BY node
            """

        result15 = self.session.run(query15)
        for record in result15:
            node_number = record['node']
            embedding = record['embedding']
            result_string = f"Node: {node_number}, Embedding: {embedding}\n"
            self.result_label.insert(tk.END, result_string)

        summary = result15.consume()

        self.result_label.insert(tk.END, f"\n\nProfiling Information:\n\n")
        #self.result_label.insert(tk.END, f"{summary.profile['args']['string-representation']}\n")
        profile_info = parse_profile(summary.profile['args']['string-representation'])

        for info in profile_info["operators"]:
            if info["Operator"] == "Operator": 
                self.result_label.insert(tk.END, f'Operator\t\t|Page Cache Hits/Misses\t\t\t|Time (ms)\t|DB Hits\t|Memory (Bytes)\t|\n')
                continue

            self.result_label.insert(tk.END, f'{info["Operator"]}\t\t|')
            self.result_label.insert(tk.END, f'{info["Page Cache Hits/Misses"]}\t\t\t|{info["Time (ms)"]}\t|{info["DB Hits"]}\t|{info["Memory (Bytes)"]}\t\t|\n')

        self.result_label.insert(tk.END, f'\nTotal Database Accesses: {profile_info["database_accesses"]}\nTotal Allocated Memory: {profile_info["allocated_memory"]}\n\n')



    

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphDatabaseGUI(root)
    root.mainloop()