import json
from pgmpy.models import BayesianNetwork

G = BayesianNetwork()

def construct_family_tree(family_tree, target_person):
    new_tree = {}
    for item in family_tree:
        new_tree[item["subject"]] = {"X": {"allele": "unknown", "probability": 0}, "Y": {"allele": "unknown", "probability": 0}}
        subject_X = new_tree[item["subject"]]["X"]
        subject_Y = new_tree[item["subject"]]["Y"]

        item["subject"] --> item["object"]
        item["subject"] --> subject_blood_type
        item["object"] --> object_blood_type


with open("problem-a-00.json", 'r') as fp:
    config = json.load(fp)

goal_person_name = config["queries"]["person"]
tested_person_name = config["test-results"]["person"]
tested_person_blood_type = config["test-results"]["result"]


