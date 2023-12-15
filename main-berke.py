from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.sampling import BayesianModelSampling
from pgmpy.inference import VariableElimination
import networkx as nx
import matplotlib.pyplot as plt
import json
import json_numpy

family_tree = BayesianNetwork()

with open('example-problems/problem-c-02.json') as f:
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


mixed_blood_test = [
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
]
evidence = {}
mbt_virtual_evidence = []
for item in range(len(d["test-results"])):
    if f'{d["test-results"][item]["type"]}' == 'bloodtype-test':
        evidence.update({f'{d["test-results"][item]["person"]}BT': f'{d["test-results"][item]["result"]}'})
    elif f'{d["test-results"][item]["type"]}' == 'mixed-bloodtype-test':
        family_tree.add_edge(f'{d["test-results"][item]["person-1"]}BT', f"MBT{item}")
        family_tree.add_edge(f'{d["test-results"][item]["person-2"]}BT', f"MBT{item}")
        family_tree.add_cpds(TabularCPD(variable=f"MBT{item}", variable_card=4, values=mixed_blood_test,
                                        state_names={f"MBT{item}": ['A', 'B', 'AB', 'O'],
                                                     f'{d["test-results"][item]["person-1"]}BT': ['A', 'B', 'AB', 'O'],
                                                     f'{d["test-results"][item]["person-2"]}BT': ['A', 'B', 'AB', 'O'],
                                                     },
                                        evidence=[f'{d["test-results"][item]["person-1"]}BT',
                                                  f'{d["test-results"][item]["person-2"]}BT'],
                                        evidence_card=[4, 4])
                             )
        evidence.update({f"MBT{item}": f'{d["test-results"][item]["result"]}'})

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
    # Perform Inference for the results
for item in range(len(d["queries"])):
    result = infer.query(variables=[f'{d["queries"][item]["person"]}BT'], evidence=evidence)
    print(result)

result_dict = result.values
print(type(result_dict))
# Import the json module
# import json
#
# # Convert the dictionary to JSON format
# result_json = json.dumps(result_dict)
#
# # Write the JSON result to a file
# with open('pgmpy_result.json', 'w') as file:
#     file.write(result_json)
