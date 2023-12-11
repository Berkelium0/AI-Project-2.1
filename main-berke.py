from pgmpy.models import BayesianModel
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
import numpy as np

bayesNet = BayesianModel()
bayesNet.add_node("OX")
bayesNet.add_node("OY")
#bayesNet.add_node("OBT")
bayesNet.add_node("KX")
bayesNet.add_node("KY")
#bayesNet.add_node("KBT")
bayesNet.add_node("IX")
bayesNet.add_node("IY")
#bayesNet.add_node("IBT")


bayesNet.add_edge("OX", "KX")
#bayesNet.add_edge("OX", "OBT")
bayesNet.add_edge("OY", "KX")
#bayesNet.add_edge("OY", "OBT")

bayesNet.add_edge("IX", "KY")
#bayesNet.add_edge("IX", "IBT")
bayesNet.add_edge("IY", "KY")
#bayesNet.add_edge("IY", "IBT")

#bayesNet.add_edge("KX", "KBT")
#bayesNet.add_edge("KY", "KBT")

north_wumponia = [[.40],
                  [.35],
                  [.25]]

subject_values = [[1, 0, 0],
                  [.5, .5, 0],
                  [.5, 0, .5],
                  [.5, 0, .5],
                  [0, 1, 0],
                  [0, .5, .5],
                  [.5, 0, .5],
                  [0, .5, .5],
                  [0, 0, 1]]

blood_type_chart = [[100,0,0,0],
                  [0,0,100,0],
                  [0,100,0,0],
                  [0,0,100,0],
                  [0,100,0,0],
                  [0,100,0,0],
                  [100,0,0,0],
                  [0,100,0,0],
                  [0,0,0,100]]

# blood_type_chart = [[100,0,100,0,0,0,100,0,0],
#                   [0,0,0,0,100,100,0,100,0],
 #                  [0,100,0,100,0,0,0,0,0],
  #                 [0,0,0,0,0,0,0,0,100]]



cpd_OX = TabularCPD("OX", 3, values=north_wumponia)
cpd_OY = TabularCPD("OY", 3, values=north_wumponia)
#cpd_OBT = TabularCPD("OBT", 9, values=blood_type_chart)
cpd_KX = TabularCPD("KX", 9, values=subject_values,evidence=['OX', 'OY'], evidence_card=[3, 1])
cpd_KX.normalize()
cpd_KY = TabularCPD("KY", 9, values=subject_values,evidence=['IX', 'IY'], evidence_card=[3, 1])
cpd_KY.normalize()
#cpd_KBT = TabularCPD("KBT", 9, values=blood_type_chart)
cpd_IX = TabularCPD("IX", 3, values=north_wumponia)
cpd_IY = TabularCPD("IY", 3, values=north_wumponia)
#cpd_IBT = TabularCPD("IBT", 9, values=blood_type_chart)

#bayesNet.add_cpds(cpd_OX, cpd_OY, cpd_OBT, cpd_KX, cpd_KY, cpd_KBT, cpd_IX, cpd_IY, cpd_IBT)

bayesNet.add_cpds(cpd_OX, cpd_OY, cpd_KX, cpd_KY, cpd_IX, cpd_IY)

bayesNet.check_model()