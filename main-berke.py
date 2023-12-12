from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.sampling import BayesianModelSampling
from pgmpy.inference import VariableElimination
import networkx as nx
import matplotlib.pyplot as plt

family_tree = BayesianNetwork()

# Create Nodes
family_tree.add_node("OX")
family_tree.add_node("OY")
family_tree.add_node("OBT")
family_tree.add_node("KX")
family_tree.add_node("KY")
family_tree.add_node("KBT")
family_tree.add_node("IX")
family_tree.add_node("IY")
family_tree.add_node("IBT")

# Set the Relations
family_tree.add_edge("OX", "KX")
family_tree.add_edge("OX", "OBT")
family_tree.add_edge("OY", "KX")
family_tree.add_edge("OY", "OBT")

family_tree.add_edge("IX", "KY")
family_tree.add_edge("IX", "IBT")
family_tree.add_edge("IY", "KY")
family_tree.add_edge("IY", "IBT")

family_tree.add_edge("KX", "KBT")
family_tree.add_edge("KY", "KBT")

north_wumponia = [[.40],
                  [.35],
                  [.25]]

subject_values = [[1, 0.5, 0.5, 0.5, 0, 0, 0.5, 0, 0],
                  [0, 0.5, 0, 0, 1, 0.5, 0, 0.5, 0],
                  [0, 0, 0.5, 0.5, 0, 0.5, 0.5, 0.5, 1]]

blood_type_chart = [[1, 0, 1, 0, 0, 0, 1, 0, 0],
                    [0, 0, 0, 0, 1, 1, 0, 1, 0],
                    [0, 1, 0, 1, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 1]]

cpd_OX = TabularCPD("OX", 3, values=north_wumponia)
cpd_OY = TabularCPD("OY", 3, values=north_wumponia)
cpd_OBT = TabularCPD("OBT", 4, values=blood_type_chart, evidence=['OX', 'OY'], evidence_card=[3, 3])

cpd_KX = TabularCPD("KX", 3, values=subject_values, evidence=['OX', 'OY'], evidence_card=[3, 3])
cpd_KY = TabularCPD("KY", 3, values=subject_values, evidence=['IX', 'IY'], evidence_card=[3, 3])
cpd_KBT = TabularCPD("KBT", 4, values=blood_type_chart, evidence=['KX', 'KY'], evidence_card=[3, 3])
cpd_IX = TabularCPD("IX", 3, values=north_wumponia)
cpd_IY = TabularCPD("IY", 3, values=north_wumponia)
cpd_IBT = TabularCPD("IBT", 4, values=blood_type_chart, evidence=['IX', 'IY'], evidence_card=[3, 3])

family_tree.add_cpds(cpd_OX, cpd_OY, cpd_OBT, cpd_KX, cpd_KY, cpd_KBT, cpd_IX, cpd_IY, cpd_IBT)

family_tree.check_model()

# Extract the edges from the Bayesian Network
edges = family_tree.edges()

# Create a directed graph using networkx
G = nx.DiGraph()
G.add_edges_from(edges)

# Plot the Bayesian network structure
plt.figure(figsize=(6, 6))
pos = nx.spring_layout(G)  # Choose a layout for visualization
nx.draw(G, pos, with_labels=True, node_size=1000, node_color='skyblue', font_weight='bold', arrows=True)
plt.title("Bayesian Network Structure")
plt.show()