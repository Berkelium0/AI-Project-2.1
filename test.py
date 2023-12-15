from pgmpy.models import BayesianModel

# Creating a Bayesian Network
model = BayesianModel([('A', 'C'), ('A', 'D'), ('B', 'C'), ('A', 'F')])

# In this example, 'A' has two child nodes 'C' and 'D'.
# This creates a structure where 'A' influences both 'C' and 'D'.

# Visualizing the Bayesian Network
import networkx as nx
import matplotlib.pyplot as plt

edges = model.edges
G = nx.DiGraph()
G.add_edges_from(edges)

# Plot the Bayesian network structure
plt.figure(figsize=(6, 6))
pos = nx.spring_layout(G)  # Choose a layout for visualization
nx.draw(G, pos, with_labels=True, node_size=1000, node_color='skyblue', font_weight='bold', arrows=True)
plt.title("Bayesian Network Structure")
plt.show()
