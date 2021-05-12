import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


# New Antecedent/Consequent objects hold universe variables and membership
# functions
distance = ctrl.Antecedent(np.arange(0, 1, 0.01), 'distance')
motor_1 = ctrl.Consequent(np.arange(0, 1, 0.01), 'motor_1')
motor_2 = ctrl.Consequent(np.arange(0, 1, 0.01), 'motor_2')

motor_1.defuzzify_method = 'mom'
motor_2.defuzzify_method = 'mom'

# Custom membership functions can be built interactively with a familiar,
# Pythonic API
distance['very close'] = fuzz.trapmf(distance.universe, [0, 0, 0.100, 0.150])
distance['close'] = fuzz.trapmf(
    distance.universe, [0.100, 0.150, 0.350, 0.400])
distance['normal'] = fuzz.trapmf(
    distance.universe, [0.350, 0.400, 0.600, 0.650])
distance['far'] = fuzz.trapmf(distance.universe, [0.600, 0.650, 0.850, 0.900])
distance['very far'] = fuzz.trapmf(distance.universe, [0.850, 0.900, 1, 1])

# Output membership functions
motor_1['medium'] = fuzz.gbellmf(motor_1.universe, 0.2, 2, 0)
motor_1['high'] = fuzz.gbellmf(motor_1.universe, 0.2, 2, 0.5)
motor_1['very high'] = fuzz.gbellmf(motor_1.universe, 0.2, 2, 1)

motor_2['medium'] = fuzz.gbellmf(motor_2.universe, 0.2, 2, 0)
motor_2['high'] = fuzz.gbellmf(motor_2.universe, 0.2, 2, 0.5)
motor_2['very high'] = fuzz.gbellmf(motor_2.universe, 0.2, 2, 1)


# Establish the rules for the system
rule1 = ctrl.Rule(distance['very close'],
                  (motor_1['very high'], motor_2['medium']))
rule2 = ctrl.Rule(distance['close'], (motor_1['high'], motor_2['medium']))
rule3 = ctrl.Rule(distance['normal'], (motor_1['medium'], motor_2['medium']))
rule4 = ctrl.Rule(distance['far'], (motor_1['medium'], motor_2['high']))
rule5 = ctrl.Rule(distance['very far'],
                  (motor_1['medium'], motor_2['very high']))


motion_control = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
motion = ctrl.ControlSystemSimulation(motion_control)


def get_fuzzy_value(distance, motor):

    motion.input['distance'] = distance
    motion.compute()

    if motor == 1:
        return float(motion.output['motor_1'])
    if motor == 2:
        return float(motion.output['motor_2'])
