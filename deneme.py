from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.sampling import BayesianModelSampling
from pgmpy.inference import VariableElimination
import networkx as nx
import matplotlib.pyplot as plt
import json

with open('example-problems/problem-b-00.json') as f:
    d = json.load(f)

# Conditional Probability Tables
country = []
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

network = BayesianNetwork()

for item in d["family-tree"]:
    print(item)
    subX = f"{item['subject']}X"
    subY = f"{item['subject']}Y"
    subBT = f"{item['subject']}BT"
    objX = f"{item['object']}X"
    objY = f"{item['object']}Y"
    objBT = f"{item['object']}BT"

    if item["relation"] == "mother-of":
        network.add_edge(subX, objX)
        network.add_edge(subY, objX)
    elif item["relation"] == "father-of":
        network.add_edge(subX, objY)
        network.add_edge(subY, objY)

    network.add_edge(subX, subBT)
    network.add_edge(subY, subBT)
    network.add_edge(objX, objBT)
    network.add_edge(objY, objBT)

    state_names = {
        f'{subX}': ['A', 'B', 'O'],
        f'{subY}': ['A', 'B', 'O'],
        f'{subBT}': ['A', 'B', 'AB', 'O'],
        f'{objX}': ['A', 'B', 'O'],
        f'{objY}': ['A', 'B', 'O'],
        f'{objBT}': ['A', 'B', 'AB', 'O']
    }

    globals()[f"cpd_{subX}"] = TabularCPD(
        variable=f"{subX}",
        variable_card=3,
        values=country,
        state_names=state_names
    )

    globals()[f"cpd_{subY}"] = TabularCPD(
        variable=f"{subY}",
        variable_card=3,
        values=country,
        state_names=state_names
    )

    globals()[f"cpd_{subBT}"] = TabularCPD(
        variable=f"{subBT}",
        variable_card=4,
        values=blood_type_chart,
        evidence=[f"{subX}", f"{subY}"],
        evidence_card=[3, 3],
        state_names=state_names
    )

    globals()[f"cpd_{objBT}"] = TabularCPD(
        variable=f"{objBT}",
        variable_card=4,
        values=blood_type_chart,
        evidence=[f"{objX}", f"{objY}"],
        evidence_card=[3, 3],
        state_names=state_names
    )

    if item["relation"] == "mother-of":
        globals()[f"cpd_{objX}"] = TabularCPD(f"{objX}", 3, values=subject_values, evidence=[f'{subX}', f'{subY}'],
                                              evidence_card=[3, 3], state_names=state_names)
        if network.get_cpds(f"{objY}") == None:
            print("emptyY")
            globals()[f"cpd_{objY}"] = TabularCPD(f"{objY}", 3, values=country, state_names=state_names)
            network.add_cpds(globals()[f"cpd_{subX}"], globals()[f"cpd_{subY}"], globals()[f"cpd_{subBT}"],
                             globals()[f"cpd_{objX}"], globals()[f"cpd_{objY}"], globals()[f"cpd_{objBT}"])
        else:
            network.add_cpds(globals()[f"cpd_{subX}"], globals()[f"cpd_{subY}"], globals()[f"cpd_{subBT}"],
                             globals()[f"cpd_{objX}"], globals()[f"cpd_{objBT}"])


    elif item["relation"] == "father-of":
        print("it was here")
        globals()[f"cpd_{objY}"] = TabularCPD(f"{objY}", 3, values=subject_values, evidence=[f'{subX}', f'{subY}'],
                                              evidence_card=[3, 3], state_names=state_names)
        if network.get_cpds(f"{objX}") == None:
            print("emptyX")
            globals()[f"cpd_{objX}"] = TabularCPD(f"{objX}", 3, values=country, state_names=state_names)
            network.add_cpds(globals()[f"cpd_{subX}"], globals()[f"cpd_{subY}"], globals()[f"cpd_{subBT}"],
                             globals()[f"cpd_{objX}"], globals()[f"cpd_{objY}"], globals()[f"cpd_{objBT}"])
        else:
            network.add_cpds(globals()[f"cpd_{subX}"], globals()[f"cpd_{subY}"], globals()[f"cpd_{subBT}"],
                             globals()[f"cpd_{objY}"], globals()[f"cpd_{objBT}"])

    print("was here")
    # network.add_cpds(globals()[f"cpd_{subX}"], globals()[f"cpd_{subY}"], globals()[f"cpd_{subBT}"],
    #                  globals()[f"cpd_{objX}"], globals()[f"cpd_{objY}"], globals()[f"cpd_{objBT}"])
    
edges = network.edges
G = nx.DiGraph()
G.add_edges_from(edges)

# Plot the Bayesian network structure
plt.figure(figsize=(6, 6))
pos = nx.spring_layout(G)  # Choose a layout for visualization
nx.draw(G, pos, with_labels=True, node_size=1000, node_color='skyblue', font_weight='bold', arrows=True)
plt.title("Bayesian Network Structure")
plt.show()

network.check_model()

# Inference - Guessing KBT when OBT = A
infer = VariableElimination(network)

for item in range(len(d["test-results"])):
    evidence = {f'{d["test-results"][item]["person"]}BT': f'{d["test-results"][item]["result"]}'}

# Perform Inference for KBT
result = infer.query(variables=[f'{d["queries"][0]["person"]}BT'], evidence=evidence)
print(result)
