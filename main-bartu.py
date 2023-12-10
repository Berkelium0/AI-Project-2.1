from pgmpy.models import BayesianNetwork
from pgmpy.inference import VariableElimination
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import CausalInference
import daft

model_inference = BayesianNetwork([("Country", "Parent"), ("Parent", "Child")])
model_inference.to_daft(node_pos={"Country": (0, 0), "Parent": (2, 0), "Child": (1, 1)}).render()

