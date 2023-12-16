from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
import networkx as nx
import matplotlib.pyplot as plt
import json
import os

family_tree = BayesianNetwork()

# Conditional Probability Tables
north_wumponia = [[.40],
                  [.35],
                  [.25]]

south_wumponia = [[.25],
                  [.45],
                  [.30]]

subject_values = [[1, 0.5, 0.5, 0.5, 0, 0, 0.5, 0, 0],
                  [0, 0.5, 0, 0.5, 1, 0.5, 0, 0.5, 0],
                  [0, 0, 0.5, 0, 0, 0.5, 0.5, 0.5, 1]]

blood_type_chart = [[1, 0, 1, 0, 0, 0, 1, 0, 0],
                    [0, 0, 0, 0, 1, 1, 0, 1, 0],
                    [0, 1, 0, 1, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 1]]

mixed_blood_test = [
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
]

pair_blood_test_1 = [
    [1, 0.8, 0.8, 0.8, 0.2, 0, 0, 0, 0.2, 0, 0, 0, 0.2, 0, 0, 0],
    [0, 0.2, 0, 0, 0.8, 1, 0.8, 0.8, 0, 0.2, 0, 0, 0, 0.2, 0, 0],
    [0, 0, 0.2, 0, 0, 0, 0.2, 0, 0.8, 0.8, 1, 0.8, 0, 0, 0.2, 0],
    [0, 0, 0, 0.2, 0, 0, 0, 0.2, 0, 0, 0, 0.2, 0.8, 0.8, 0.8, 1]
]

pair_blood_test_2 = [
    [1, 0.2, 0.2, 0.2, 0.8, 0, 0, 0, 0.8, 0, 0, 0, 0.8, 0, 0, 0],
    [0, 0.8, 0, 0, 0.2, 1, 0.2, 0.2, 0, 0.8, 0, 0, 0, 0.8, 0, 0],
    [0, 0, 0.8, 0, 0, 0, 0.8, 0, 0.2, 0.2, 1, 0.2, 0, 0, 0.8, 0],
    [0, 0, 0, 0.8, 0, 0, 0, 0.8, 0, 0, 0, 0.8, 0.2, 0.2, 0.2, 1]
]

pair_blood_test_3 = [
    [1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1]
]

pair_blood_test_4 = [
    [1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1]
]


pair_blood_test_check = [[.8], [.2]]

state_names = {}
family_list = {}


def guess_blood(d, json_name):
    for x in d["family-tree"]:

        if d["country"] == 'North Wumponia':
            country = north_wumponia
        elif d["country"] == 'South Wumponia':
            country = south_wumponia

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
                globals()[f"cpd_{objX}"] = TabularCPD(f"{objX}", 3, values=country, state_names=state_names)
                family_tree.add_cpds(globals()[f"cpd_{subX}"], globals()[f"cpd_{subY}"], globals()[f"cpd_{subBT}"],
                                     globals()[f"cpd_{objX}"], globals()[f"cpd_{objY}"], globals()[f"cpd_{objBT}"])
            else:
                family_tree.add_cpds(globals()[f"cpd_{subX}"], globals()[f"cpd_{subY}"], globals()[f"cpd_{subBT}"],
                                     globals()[f"cpd_{objY}"], globals()[f"cpd_{objBT}"])

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
                                                         f'{d["test-results"][item]["person-1"]}BT': ['A', 'B', 'AB',
                                                                                                      'O'],
                                                         f'{d["test-results"][item]["person-2"]}BT': ['A', 'B', 'AB',
                                                                                                      'O'],
                                                         },
                                            evidence=[f'{d["test-results"][item]["person-1"]}BT',
                                                      f'{d["test-results"][item]["person-2"]}BT'],
                                            evidence_card=[4, 4])
                                 )
            evidence.update({f"MBT{item}": f'{d["test-results"][item]["result"]}'})

        elif f'{d["test-results"][item]["type"]}' == 'pair-bloodtype-test':

            person_1 = d["test-results"][item]["person-1"]
            result_1 = d["test-results"][item]["result-1"]

            person_2 = d["test-results"][item]["person-2"]
            result_2 = d["test-results"][item]["result-2"]

            family_tree.add_edge(f'{person_1}BT', f'{item}_Result1')
            family_tree.add_edge(f'{person_1}BT', f'{item}_Result2')
            family_tree.add_edge(f'{person_2}BT', f'{item}_Result1')
            family_tree.add_edge(f'{person_2}BT', f'{item}_Result2')
            family_tree.add_edge(f'{item}PBT', f'{item}_Result1')
            family_tree.add_edge(f'{item}PBT', f'{item}_Result2')

            family_tree.add_cpds(TabularCPD(variable=f'{item}PBT', variable_card=2, values=pair_blood_test_check,
                                            state_names={f'{item}PBT': ['work', 'fail']}
                                            ),
                                 TabularCPD(variable=f'{item}_Result1', variable_card=4, values=pair_blood_test_3,
                                            state_names={f'{item}_Result1': ['A', 'B', 'AB', 'O'],
                                                         f'{d["test-results"][item]["person-1"]}BT': ['A', 'B', 'AB',
                                                                                                      'O'],
                                                         f'{d["test-results"][item]["person-2"]}BT': ['A', 'B', 'AB',
                                                                                                      'O'],
                                                         f'{item}PBT': ['work', 'fail']
                                                         },
                                            evidence=[f'{d["test-results"][item]["person-1"]}BT',
                                                      f'{d["test-results"][item]["person-2"]}BT',
                                                      f'{item}PBT'],
                                            evidence_card=[4, 4, 2]
                                            ),
                                 TabularCPD(variable=f'{item}_Result2', variable_card=4, values=pair_blood_test_4,
                                            state_names={f'{item}_Result2': ['A', 'B', 'AB', 'O'],
                                                         f'{d["test-results"][item]["person-1"]}BT': ['A', 'B', 'AB',
                                                                                                      'O'],
                                                         f'{d["test-results"][item]["person-2"]}BT': ['A', 'B', 'AB',
                                                                                                      'O'],
                                                         f'{item}PBT': ['work', 'fail']
                                                         },
                                            evidence=[f'{d["test-results"][item]["person-1"]}BT',
                                                      f'{d["test-results"][item]["person-2"]}BT',
                                                      f'{item}PBT'],
                                            evidence_card=[4, 4, 2]
                                            ),
                                 )
            evidence.update({f'{item}_Result1': f'{d["test-results"][item]["result-1"]}'})
            evidence.update({f'{item}_Result2': f'{d["test-results"][item]["result-2"]}'})

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

    data = []
    for item in range(len(d["queries"])):
        result = infer.query(variables=[f'{d["queries"][item]["person"]}BT'], evidence=evidence)
        print(result)
        result_arr = result.values.tolist()
        data.append({
            "type": "bloodtype",
            "person": f'{d["queries"][item]["person"]}',
            "distribution": {
                "O": result_arr[3],
                "A": result_arr[0],
                "B": result_arr[1],
                "AB": result_arr[2]
            }
        })

    with open(f'solutions/{json_name.replace("problem", "solution")}', 'w') as f:
        json.dump(data, f)

    node_list = list(family_tree.nodes())

    for node in node_list:
        family_tree.remove_node(node)


path_to_json = 'problems'
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]

for jsons in json_files:
    with open(f'problems/{jsons}') as f:
        print(jsons)
        d = json.load(f)
        guess_blood(d, jsons)
