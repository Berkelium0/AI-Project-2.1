from pgmpy.models import BayesianNetwork
from pgmpy.inference import VariableElimination
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import CausalInference
import daft
import json

with open("problem-a-00.json", 'r') as fp:
    config = json.load(fp)

goal_person_name = config["queries"]["person"]
tested_person_name = config["test-results"]["person"]
tested_person_blood_type = config["test-results"]["result"]

model_inference = BayesianNetwork([("Country", "Parent"), ("Parent", "Child")])
model_inference.to_daft(node_pos={"Country": (0, 0), "Parent": (2, 0), "Child": (1, 1)}).render()

