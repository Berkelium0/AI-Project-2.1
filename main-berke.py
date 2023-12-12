from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.sampling import BayesianModelSampling
from pgmpy.inference import VariableElimination
import networkx as nx
import matplotlib.pyplot as plt
import json

family_tree = BayesianNetwork()

with open('example-problems/problem-b-00.json') as f:
    d = json.load(f)

# Conditional Probability Tables
north_wumponia = [[.40],
                  [.35],
                  [.25]]

east_wumponia = [[.25],
                 [.45],
                 [.30]]

subject_values = [[1, 0.5, 0.5, 0.5, 0, 0, 0.5, 0, 0],
                  [0, 0.5, 0, 0.5, 1, 0.5, 0, 0.5, 0],
                  [0, 0, 0.5, 0, 0, 0.5, 0.5, 0.5, 1]]

blood_type_chart = [[1, 0, 1, 0, 0, 0, 1, 0, 0],
                    [0, 0, 0, 0, 1, 1, 0, 1, 0],
                    [0, 1, 0, 1, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 1]]

state_names = {}
family_list = {}

for x in d["family-tree"]:
    subX = f"{x['subject']}X"
    subY = f"{x['subject']}Y"
    subBT = f"{x['subject']}BT"
    objX = f"{x['object']}X"
    objY = f"{x['object']}Y"
    objBT = f"{x['object']}BT"

    # Create Nodes
    family_tree.add_node(subX)
    family_tree.add_node(subY)
    family_tree.add_node(subBT)
    family_tree.add_node(objX)
    family_tree.add_node(objY)
    family_tree.add_node(objBT)

    # Add the Edges
    family_tree.add_edge(subX, subBT)
    family_tree.add_edge(subY, subBT)
    family_tree.add_edge(objX, objBT)
    family_tree.add_edge(objY, objBT)

    if x["relation"] == "mother-of":
        family_tree.add_edge(subX, objX)
        family_tree.add_edge(subY, objX)
    elif x["relation"] == "father-of":
        family_tree.add_edge(subX, objY)
        family_tree.add_edge(subY, objY)

    # Create State Names
    state_names.update({
        f'{subX}': ['A', 'B', 'O'],
        f'{subY}': ['A', 'B', 'O'],
        f'{subBT}': ['A', 'B', 'AB', 'O'],
        f'{objX}': ['A', 'B', 'O'],
        f'{objY}': ['A', 'B', 'O'],
        f'{objBT}': ['A', 'B', 'AB', 'O']
    })

    globals()[f"cpd_{subX}"] = TabularCPD(f"{subX}", 3, values=north_wumponia, state_names=state_names)
    globals()[f"cpd_{subY}"] = TabularCPD(f"{subY}", 3, values=north_wumponia, state_names=state_names)
    globals()[f"cpd_{subBT}"] = TabularCPD(f"{subBT}", 4, values=blood_type_chart, evidence=[f"{subX}", f"{subY}"],
                                           evidence_card=[3, 3], state_names=state_names)
    globals()[f"cpd_{objBT}"] = TabularCPD(f"{objBT}", 4, values=blood_type_chart, evidence=[f"{objX}", f"{objY}"],
                                           evidence_card=[3, 3], state_names=state_names)

    if x["relation"] == "mother-of":
        globals()[f"cpd_{objX}"] = TabularCPD(f"{objX}", 3, values=subject_values, evidence=[f'{subX}', f'{subY}'],
                                              evidence_card=[3, 3], state_names=state_names)
        if family_tree.get_cpds(f"{objY}") == None:
            print("empty")
            globals()[f"cpd_{objY}"] = TabularCPD(f"{objY}", 3, values=north_wumponia, state_names=state_names)
        else:
            family_tree.add_cpds(globals()[f"cpd_{subX}"], globals()[f"cpd_{subY}"], globals()[f"cpd_{subBT}"],
                                 globals()[f"cpd_{objX}"], globals()[f"cpd_{objBT}"])
            break

    elif x["relation"] == "father-of":
        globals()[f"cpd_{objY}"] = TabularCPD(f"{objY}", 3, values=subject_values, evidence=[f'{subX}', f'{subY}'],
                                              evidence_card=[3, 3], state_names=state_names)
        if family_tree.get_cpds(f"{objX}") == None:
            print("emptyX")
            globals()[f"cpd_{objX}"] = TabularCPD(f"{objX}", 3, values=north_wumponia, state_names=state_names)
        else:
            family_tree.add_cpds(globals()[f"cpd_{subX}"], globals()[f"cpd_{subY}"], globals()[f"cpd_{subBT}"],
                                 globals()[f"cpd_{objY}"], globals()[f"cpd_{objBT}"])
            break

    # cpd_KY = TabularCPD("KY", 3, values=subject_values, evidence=['IX', 'IY'], evidence_card=[3, 3],
    #                     state_names=state_names)

    family_tree.add_cpds(globals()[f"cpd_{subX}"], globals()[f"cpd_{subY}"], globals()[f"cpd_{subBT}"],
                         globals()[f"cpd_{objX}"], globals()[f"cpd_{objY}"], globals()[f"cpd_{objBT}"])

# cpd_OX = TabularCPD("OX", 3, values=north_wumponia, state_names=state_names)
# cpd_OY = TabularCPD("OY", 3, values=north_wumponia, state_names=state_names)
# cpd_OBT = TabularCPD("OBT", 4, values=blood_type_chart, evidence=['OX', 'OY'], evidence_card=[3, 3],
#                      state_names=state_names)
# cpd_KX = TabularCPD("KX", 3, values=subject_values, evidence=['OX', 'OY'], evidence_card=[3, 3],
#                     state_names=state_names)
# cpd_KY = TabularCPD("KY", 3, values=subject_values, evidence=['IX', 'IY'], evidence_card=[3, 3],
#                     state_names=state_names)
# cpd_KBT = TabularCPD("KBT", 4, values=blood_type_chart, evidence=['KX', 'KY'], evidence_card=[3, 3],
#                      state_names=state_names)
# cpd_IX = TabularCPD("IX", 3, values=north_wumponia, state_names=state_names)
# cpd_IY = TabularCPD("IY", 3, values=north_wumponia, state_names=state_names)
# cpd_IBT = TabularCPD("IBT", 4, values=blood_type_chart, evidence=['IX', 'IY'], evidence_card=[3, 3],
#                      state_names=state_names)

# family_tree.add_cpds(cpd_OX, cpd_OY, cpd_OBT, cpd_KX, cpd_KY, cpd_KBT, cpd_IX, cpd_IY, cpd_IBT)

# # Create Nodes
# family_tree.add_node("OX")
# family_tree.add_node("OY")
# family_tree.add_node("OBT")
# family_tree.add_node("KX")
# family_tree.add_node("KY")
# family_tree.add_node("KBT")
# family_tree.add_node("IX")
# family_tree.add_node("IY")
# family_tree.add_node("IBT")

# # Add the Edges
# family_tree.add_edge("OX", "KX")
# family_tree.add_edge("OX", "OBT")
# family_tree.add_edge("OY", "KX")
# family_tree.add_edge("OY", "OBT")
#
# family_tree.add_edge("IX", "KY")
# family_tree.add_edge("IX", "IBT")
# family_tree.add_edge("IY", "KY")
# family_tree.add_edge("IY", "IBT")
#
# family_tree.add_edge("KX", "KBT")
# family_tree.add_edge("KY", "KBT")


# state_names = {
#     'OX': ['A', 'B', 'O'],
#     'OY': ['A', 'B', 'O'],
#     'OBT': ['A', 'B', 'AB', 'O'],
#     'KX': ['A', 'B', 'O'],
#     'KY': ['A', 'B', 'O'],
#     'KBT': ['A', 'B', 'AB', 'O'],
#     'IX': ['A', 'B', 'O'],
#     'IY': ['A', 'B', 'O'],
#     'IBT': ['A', 'B', 'AB', 'O']
# }


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

# # Display CPDs
# cpds = family_tree.get_cpds()
# for cpd in cpds:
#     print("CPD for variable:", cpd.variable)
#     print(cpd)
#     print("\n")

# Visualize Bayesian network structure
plt.figure(figsize=(8, 6))
pos = nx.spring_layout(G)  # Choose a layout for visualization
nx.draw(G, pos, with_labels=True, node_size=1000, node_color='skyblue', font_weight='bold', arrows=True)
plt.title("Bayesian Network Structure")
plt.show()

# Inference - Guessing KBT when OBT = A
infer = VariableElimination(family_tree)

# Set evidence OBT = A
print(d)
evidence = {f'{d["test-results"][0]["person"]}BT': f'{d["test-results"][0]["result"]}',
            f'{d["test-results"][1]["person"]}BT': f'{d["test-results"][0]["result"]}',
            f'{d["test-results"][2]["person"]}BT': f'{d["test-results"][0]["result"]}'
            }

# Perform Inference for KBT
result = infer.query(variables=[f'{d["queries"][0]["person"]}BT'], evidence=evidence)

print(result)
