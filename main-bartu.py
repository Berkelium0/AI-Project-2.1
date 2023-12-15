from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.sampling import BayesianModelSampling
from pgmpy.inference import VariableElimination
import networkx as nx
import matplotlib.pyplot as plt
import json

family_tree = BayesianNetwork()

with open('example-problems/problem-d-04.json') as f:
    d = json.load(f)

# Conditional Probability Tables
north_wumponia = [[.40],
                  [.35],
                  [.25]]

south_wumponia = [[.25],
                  [.45],
                  [.30]]

if d["country"] == 'North Wumponia':
    country = north_wumponia
elif d["country"] == 'South Wumponia':
    country = south_wumponia

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
    if family_tree.get_cpds(f"{subX}") == None:
        globals()[f"cpd_{subX}"] = TabularCPD(f"{subX}", 3, values=country, state_names=state_names)
    if family_tree.get_cpds(f"{subY}") == None:
        globals()[f"cpd_{subY}"] = TabularCPD(f"{subY}", 3, values=country, state_names=state_names)

    globals()[f"cpd_{subBT}"] = TabularCPD(f"{subBT}", 4, values=blood_type_chart, evidence=[f"{subX}", f"{subY}"],
                                           evidence_card=[3, 3], state_names=state_names)
    globals()[f"cpd_{objBT}"] = TabularCPD(f"{objBT}", 4, values=blood_type_chart, evidence=[f"{objX}", f"{objY}"],
                                           evidence_card=[3, 3], state_names=state_names)

    if x["relation"] == "mother-of":
        globals()[f"cpd_{objX}"] = TabularCPD(f"{objX}", 3, values=subject_values, evidence=[f'{subX}', f'{subY}'],
                                              evidence_card=[3, 3], state_names=state_names)
        if family_tree.get_cpds(f"{objY}") == None:
            print("emptyY")
            globals()[f"cpd_{objY}"] = TabularCPD(f"{objY}", 3, values=country, state_names=state_names)
            family_tree.add_cpds(globals()[f"cpd_{subX}"], globals()[f"cpd_{subY}"], globals()[f"cpd_{subBT}"],
                                 globals()[f"cpd_{objX}"], globals()[f"cpd_{objY}"], globals()[f"cpd_{objBT}"])
        else:
            family_tree.add_cpds(globals()[f"cpd_{subX}"], globals()[f"cpd_{subY}"], globals()[f"cpd_{subBT}"],
                                 globals()[f"cpd_{objX}"], globals()[f"cpd_{objBT}"])


    elif x["relation"] == "father-of":
        globals()[f"cpd_{objY}"] = TabularCPD(f"{objY}", 3, values=subject_values, evidence=[f'{subX}', f'{subY}'],
                                              evidence_card=[3, 3], state_names=state_names)
        if family_tree.get_cpds(f"{objX}") == None:
            print("emptyX")
            globals()[f"cpd_{objX}"] = TabularCPD(f"{objX}", 3, values=country, state_names=state_names)
            family_tree.add_cpds(globals()[f"cpd_{subX}"], globals()[f"cpd_{subY}"], globals()[f"cpd_{subBT}"],
                                 globals()[f"cpd_{objX}"], globals()[f"cpd_{objY}"], globals()[f"cpd_{objBT}"])
        else:
            family_tree.add_cpds(globals()[f"cpd_{subX}"], globals()[f"cpd_{subY}"], globals()[f"cpd_{subBT}"],
                                 globals()[f"cpd_{objY}"], globals()[f"cpd_{objBT}"])

    # family_tree.add_cpds(globals()[f"cpd_{subX}"], globals()[f"cpd_{subY}"], globals()[f"cpd_{subBT}"],
    #                      globals()[f"cpd_{objX}"], globals()[f"cpd_{objY}"], globals()[f"cpd_{objBT}"])

family_tree.check_model()

# Extract the edges from the Bayesian Network
edges = family_tree.edges()

# Create a directed graph using networkx
G = nx.DiGraph()
G.add_edges_from(edges)

# Visualize Bayesian network structure
plt.figure(figsize=(8, 6))
pos = nx.spring_layout(G)  # Choose a layout for visualization
nx.draw(G, pos, with_labels=True, node_size=1000, node_color='skyblue', font_weight='bold', arrows=True)
plt.title("Bayesian Network Structure")
plt.show()

# Inference
infer = VariableElimination(family_tree)

# Set evidence

pair_blood_type_chart = [[0.8],
                         [0.2]]

mixed_blood_test = [
    [.5, 0, .25, 0],
    [0, .5, .25, 0],
    [0, 0, .25, 0],
    [.5, .5, .25, 1]
]
# mbt_virtual_evidence = TabularCPD(variable="MBT", variable_card=4, values=mixed_blood_test,
#                                   state_names={'A', 'B', 'AB', 'O'})
evidence = {}
virtual_evidence = []
for item in range(len(d["test-results"])):
    if f'{d["test-results"][item]["type"]}' == 'bloodtype-test':
        evidence.update({f'{d["test-results"][item]["person"]}BT': f'{d["test-results"][item]["result"]}'})
    # if f'{d["test-results"][item]["type"]}' == 'mixed-bloodtype-test':
    #     virtual_evidence.append(
    #         TabularCPD(variable=f'{d["test-results"][item]["person-1"]}', variable_card=4, values=mixed_blood_test,
    #                    state_names={'A', 'B', 'AB', 'O'}))
    if f'{d["test-results"][item]["type"]}' == 'pair-bloodtype-test':
        virtual_evidence.append(
            TabularCPD(variable=f'{d["test-results"][item]["person-1"]}BT', variable_card=2, values=pair_blood_type_chart,
                       state_names={f'{d["test-results"][item]["person-1"]}BT': [f'{d["test-results"][item]["result-1"]}', f'{d["test-results"][item]["result-2"]}']}))
        virtual_evidence.append(
            TabularCPD(variable=f'{d["test-results"][item]["person-2"]}BT', variable_card=2, values=pair_blood_type_chart,
                   state_names={f'{d["test-results"][item]["person-2"]}BT': [f'{d["test-results"][item]["result-1"]}', f'{d["test-results"][item]["result-2"]}']}))


# Perform Inference for the results
for item in range(len(d["queries"])):
    result = infer.query(variables=[f'{d["queries"][item]["person"]}BT'], evidence=evidence,
                         virtual_evidence=virtual_evidence)

    print(result)
