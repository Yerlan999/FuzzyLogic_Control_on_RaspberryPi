import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# New Antecedent/Consequent objects hold universe variables and membership
# functions
distance_x = ctrl.Antecedent(np.arange(-1, 1, 0.01), 'distance_x')
motor_x = ctrl.Consequent(np.arange(-1, 1, 0.01), 'motor_x')

motor_x.defuzzify_method = 'mom'

# Custom membership functions can be built interactively with a familiar,
distance_x['-far'] = fuzz.gbellmf(distance_x.universe, 0.2, 3, -1)
distance_x['-average'] = fuzz.gbellmf(distance_x.universe, 0.2, 3, -0.7)
distance_x['-close'] = fuzz.gbellmf(distance_x.universe, 0.2, 3, -0.3)
distance_x['zero'] = fuzz.trimf(distance_x.universe, [-0.3, 0, 0.3])
distance_x['+close'] = fuzz.gbellmf(distance_x.universe, 0.2, 3, 0.3)
distance_x['+average'] = fuzz.gbellmf(distance_x.universe, 0.2, 3, 0.7)
distance_x['+far'] = fuzz.gbellmf(distance_x.universe, 0.2, 3, 1)

# Output membership functions
motor_x['-high'] = fuzz.gbellmf(motor_x.universe, 0.2, 3, -1)
motor_x['-average'] = fuzz.gbellmf(motor_x.universe, 0.2, 3, -0.7)
motor_x['-low'] = fuzz.gbellmf(motor_x.universe, 0.2, 3, -0.3)
motor_x['zero'] = fuzz.trimf(motor_x.universe, [-0.3, 0, 0.3])
motor_x['+low'] = fuzz.gbellmf(motor_x.universe, 0.2, 3, 0.3)
motor_x['+average'] = fuzz.gbellmf(motor_x.universe, 0.2, 3, 0.7)
motor_x['+high'] = fuzz.gbellmf(motor_x.universe, 0.2, 3, 1)


rule1 = ctrl.Rule(distance_x['+far'], motor_x['+high'])
rule2 = ctrl.Rule(distance_x['+average'], motor_x['+average'])
rule3 = ctrl.Rule(distance_x['+close'], motor_x['+low'])
rule4 = ctrl.Rule(distance_x['zero'], motor_x['zero'])
rule5 = ctrl.Rule(distance_x['-close'], motor_x['-low'])
rule6 = ctrl.Rule(distance_x['-average'], motor_x['-average'])
rule7 = ctrl.Rule(distance_x['-far'], motor_x['-high'])


x_motion_control = ctrl.ControlSystem(
    [rule1, rule2, rule3, rule4, rule5, rule6, rule7])
x_motion = ctrl.ControlSystemSimulation(x_motion_control)


def get_fuzzy_value(distance):

    x_motion.input['distance_x'] = distance
    x_motion.compute()

    return float(x_motion.output['motor_x'])
