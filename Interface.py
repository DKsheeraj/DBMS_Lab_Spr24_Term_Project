# import tkinter as tk
# from tkinter import filedialog
# from tkinter.scrolledtext import ScrolledText
# from neo4j import GraphDatabase

# class GraphDatabaseGUI:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Graph Database GUI")

#         # Neo4j connection details
#         self.uri = "neo4j://localhost:7687"
#         self.username = "neo4j"
#         self.password = "Datta@2003"

#         # Connect to Neo4j
#         self.driver = None
#         self.session = None

#         # Create UI elements
#         self.label = tk.Label(root, text="Graph Database GUI")
#         self.label.pack()

#         self.connect_button = tk.Button(root, text="Connect to Neo4j", command=self.connect_to_neo4j)
#         self.connect_button.pack()

#         self.open_button = tk.Button(root, text="Open Dataset File", command=self.open_dataset_file, state=tk.DISABLED)
#         self.open_button.pack()

#         self.query1_button = tk.Button(root, text="Get all nodes in the graph", command=self.execute_query1, state=tk.DISABLED)
#         self.query1_button.pack()

#         self.query2_button = tk.Button(root, text="Get nodes connected to a specific node", command=self.execute_query2, state=tk.DISABLED)
#         self.query2_button.pack()

#         self.query3_button = tk.Button(root, text="Get count of nodes in the graph", command=self.execute_query3, state=tk.DISABLED)
#         self.query3_button.pack()

#         self.query4_button = tk.Button(root, text="Compute PageRank for the graph", command=self.compute_pagerank, state=tk.DISABLED)
#         self.query4_button.pack()

#         self.result_label = ScrolledText(root, height=10, width=60)
#         self.result_label.pack()

#     def connect_to_neo4j(self):
#         try:
#             self.driver = GraphDatabase.driver(self.uri, auth=(self.username, self.password))
#             self.session = self.driver.session()
#             self.result_label.insert(tk.END, "Successfully connected to Neo4j!\n")
#             self.open_button.config(state=tk.NORMAL)
#             self.query1_button.config(state=tk.NORMAL)
#             self.query2_button.config(state=tk.NORMAL)
#             self.query3_button.config(state=tk.NORMAL)
#             self.query4_button.config(state=tk.NORMAL)
#         except Exception as e:
#             self.result_label.insert(tk.END, f"Failed to connect to Neo4j: {e}\n")

#     def open_dataset_file(self):
#         filename = filedialog.askopenfilename(title="Select Dataset File")
#         if filename:
#             try:
#                 with open(filename, "r") as file:
#                     # Assuming sample_dataset.txt contains source and target nodes separated by tabs
#                     for line in file:
#                         source, target = line.strip().split("\t")
#                         query = (
#                             f"MERGE (source:Node {{id: {source}}})"
#                             f"MERGE (target:Node {{id: {target}}})"
#                             f"MERGE (source)-[:CONNECTED_TO]->(target)"
#                         )
#                         self.session.run(query)
#                 self.result_label.insert(tk.END, "Data loaded into Neo4j successfully!\n")
#             except Exception as e:
#                 self.result_label.insert(tk.END, f"Error loading data into Neo4j: {e}\n")

#     def execute_query1(self):
#         self.result_label.delete('1.0', tk.END)

#         query = "MATCH (n) RETURN n"
#         result = self.session.run(query)
        
#         # Extract node IDs from the result and join them into a single string
#         nodes = [str(record['n']['id']) for record in result]
#         output = " ".join(nodes)
        
#         # Display the output in the result_label
#         self.result_label.insert(tk.END, output + "\n")


#     def execute_query2(self):
#         self.result_label.delete('1.0', tk.END)
        
#         # Create a label and entry widget for node ID input
#         node_id_label = tk.Label(self.root, text="Enter Node ID:")
#         node_id_label.pack()
        
#         node_id_entry = tk.Entry(self.root)
#         node_id_entry.pack()
        
#         # Define a function to execute the query when the button is clicked
#         def execute_query():
#             # Get the node ID from the entry widget
#             node_id = node_id_entry.get()
            
#             # Execute the query
#             query = f"MATCH (n)-[:CONNECTED_TO]->(m) WHERE n.id = {node_id} RETURN m"
#             result = self.session.run(query)
            
#             # Build the string to display in the output box
#             output = " ".join([str(record['m']['id']) for record in result])
            
#             # Display the output in the result_label
#             self.result_label.insert(tk.END, output)
            
#             # Destroy the entry box and execute button
#             node_id_label.pack_forget()
#             node_id_entry.pack_forget()
#             execute_button.pack_forget()
        
#         # Create a button to execute the query
#         execute_button = tk.Button(self.root, text="Execute", command=execute_query)
#         execute_button.pack()


#     def execute_query3(self):
#         self.result_label.delete('1.0', tk.END)
#         query = "MATCH (n) RETURN count(n) AS node_count"
#         result = self.session.run(query)
#         output = "\n".join([f"Number of nodes in the graph: {record['node_count']}" for record in result])
#         self.result_label.insert(tk.END, output + "\n")

#     def compute_pagerank(self):
#         self.result_label.delete('1.0', tk.END)
        
#         # Compute PageRank for the graph
#         projected_graph_query = """
#         CALL gds.graph.project.cypher(
#         'myProjectedGraph',  // Name for the projected graph
#         'MATCH (n) RETURN id(n) AS id',
#         'MATCH (n)-[:CONNECTED_TO]->(m) RETURN id(n) AS source, id(m) AS target'
#         )
#         YIELD graphName, nodeCount, relationshipCount
#         RETURN graphName, nodeCount, relationshipCount
#         """

#         # Define the PageRank query
#         pagerank_query = """
#         CALL gds.pageRank.stream('myProjectedGraph', {scaler: 'L1Norm'})
#         YIELD nodeId, score
#         RETURN nodeId AS name, score
#         ORDER BY name
#         """

#         # self.session.run(projected_graph_query)
#         result = self.session.run(pagerank_query)
#         output = "\n".join([f"Node: {record['name']}, PageRank: {record['score']}" for record in result])
#         self.result_label.insert(tk.END, output + "\n")

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = GraphDatabaseGUI(root)
#     root.mainloop()

import io
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
from neo4j import GraphDatabase

class GraphDatabaseGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Database GUI")
        self.root.attributes('-fullscreen', True)  # Open in fullscreen mode

        # Neo4j connection details
        self.uri = "neo4j://localhost:7687"
        self.username = "neo4j"
        self.password = "Datta@2003"

        # Connect to Neo4j
        self.driver = None
        self.session = None

        # Create custom style
        self.style = ttk.Style()
        self.style.configure("Custom.TButton", foreground="black", background="#CDCDCD", padding=10, font=("Sans Serif", 10), bordercolor="#333333")  # Change font to sans serif and border color
        self.style.configure("Custom.TLabel", foreground="black", background="#F0F0F0", font=("Sans Serif", 10))  # Change font to sans serif
        self.style.configure("Custom.TEntry", foreground="black", background="white", font=("Sans Serif", 10))  # Change font to sans serif

        # Create UI elements
        self.label = ttk.Label(root, text="Graph Database GUI", style="Custom.TLabel")
        self.label.pack(pady=10)

        self.connect_button = ttk.Button(root, text="Connect to Neo4j", style="Custom.TButton", command=self.connect_to_neo4j)
        self.connect_button.pack(pady=5)

        self.open_button = ttk.Button(root, text="Open Dataset File", style="Custom.TButton", command=self.open_dataset_file, state=tk.DISABLED)
        self.open_button.pack(pady=5)

        self.query1_button = ttk.Button(root, text="Get all nodes in the graph", style="Custom.TButton", command=self.execute_query1, state=tk.DISABLED)
        self.query1_button.pack(pady=5)

        self.query2_button = ttk.Button(root, text="Get nodes connected to a specific node", style="Custom.TButton", command=self.execute_query2, state=tk.DISABLED)
        self.query2_button.pack(pady=5)

        self.query3_button = ttk.Button(root, text="Get count of nodes in the graph", style="Custom.TButton", command=self.execute_query3, state=tk.DISABLED)
        self.query3_button.pack(pady=5)

        self.query4_button = ttk.Button(root, text="Compute PageRank for the graph", style="Custom.TButton", command=self.compute_pagerank, state=tk.DISABLED)
        self.query4_button.pack(pady=5)

        self.result_label = ScrolledText(root, height=10, width=60, font=("Sans Serif", 10))
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

            # Display image from Neo4j
            self.display_image_from_neo4j()
        except Exception as e:
            self.result_label.insert(tk.END, f"Failed to connect to Neo4j: {e}\n")

    def open_dataset_file(self):
        filename = filedialog.askopenfilename(title="Select Dataset File")
        if filename:
            try:
                with open(filename, "r") as file:
                    # Assuming sample_dataset.txt contains source and target nodes separated by tabs
                    for line in file:
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

    def execute_query1(self):
        self.result_label.delete('1.0', tk.END)

        query = "MATCH (n) RETURN n"
        result = self.session.run(query)
        
        # Extract node IDs from the result and join them into a single string
        nodes = [str(record['n']['id']) for record in result]
        output = " ".join(nodes)
        
        # Display the output in the result_label
        self.result_label.insert(tk.END, output + "\n")

        # Display image from Neo4j
        self.display_image_from_neo4j()

    def execute_query2(self):
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
            query = f"MATCH (n)-[:CONNECTED_TO]->(m) WHERE n.id = {node_id} RETURN m"
            result = self.session.run(query)
            
            # Build the string to display in the output box
            output = " ".join([str(record['m']['id']) for record in result])
            
            # Display the output in the result_label
            self.result_label.insert(tk.END, output)
            
            # Destroy the entry box and execute button
            node_id_label.pack_forget()
            node_id_entry.pack_forget()
            execute_button.pack_forget()

            # Display image from Neo4j
            self.display_image_from_neo4j()
        
        # Create a button to execute the query
        execute_button = ttk.Button(self.root, text="Execute", style="Custom.TButton", command=execute_query)
        execute_button.pack()


    def execute_query3(self):
        self.result_label.delete('1.0', tk.END)
        query = "MATCH (n) RETURN count(n) AS node_count"
        result = self.session.run(query)
        output = "\n".join([f"Number of nodes in the graph: {record['node_count']}" for record in result])
        self.result_label.insert(tk.END, output + "\n")

        # Display image from Neo4j
        self.display_image_from_neo4j()

    def compute_pagerank(self):
        self.result_label.delete('1.0', tk.END)
        
        # Compute PageRank for the graph
        projected_graph_query = """
        CALL gds.graph.project.cypher(
        'myProjectedGraph',  // Name for the projected graph
        'MATCH (n) RETURN id(n) AS id',
        'MATCH (n)-[:CONNECTED_TO]->(m) RETURN id(n) AS source, id(m) AS target'
        )
        YIELD graphName, nodeCount, relationshipCount
        RETURN graphName, nodeCount, relationshipCount
        """

        # Define the PageRank query
        pagerank_query = """
        CALL gds.pageRank.stream('myProjectedGraph', {scaler: 'L1Norm'})
        YIELD nodeId, score
        RETURN nodeId AS name, score
        ORDER BY name
        """

        # self.session.run(projected_graph_query)
        result = self.session.run(pagerank_query)
        output = "\n".join([f"Node: {record['name']}, PageRank: {record['score']}" for record in result])
        self.result_label.insert(tk.END, output + "\n")

        # Display image from Neo4j
        self.display_image_from_neo4j()

    def display_image_from_neo4j(self):
        # Retrieve image data from Neo4j (replace 'Image' with the appropriate label)
        result = self.session.run("MATCH (n:Image) RETURN n.image AS imageData LIMIT 1").single()

        if result:
            image_data = result["imageData"]

            # Process image data
            image = Image.open(io.BytesIO(image_data))

            # Resize the image if needed
            # image = image.resize((width, height), Image.ANTIALIAS)

            # Display the image in Tkinter
            photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo)
            self.image_label.image = photo
        else:
            print("No image found in Neo4j")

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphDatabaseGUI(root)
    root.mainloop()
