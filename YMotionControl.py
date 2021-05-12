import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


# New Antecedent/Consequent objects hold universe variables and membership
# functions
distance_y = ctrl.Antecedent(np.arange(-1, 1, 0.01), 'distance_y')
motor_y = ctrl.Consequent(np.arange(-1, 1, 0.01), 'motor_y')

motor_y.defuzzify_method = 'mom'

# Custom membership functions can be built interactively with a familiar,
distance_y['-far'] = fuzz.gbellmf(distance_y.universe, 0.2, 3, -1)
distance_y['-average'] = fuzz.gbellmf(distance_y.universe, 0.2, 3, -0.7)
distance_y['-close'] = fuzz.gbellmf(distance_y.universe, 0.2, 3, -0.3)
distance_y['zero'] = fuzz.trimf(distance_y.universe, [-0.3, 0, 0.3])
distance_y['+close'] = fuzz.gbellmf(distance_y.universe, 0.2, 3, 0.3)
distance_y['+average'] = fuzz.gbellmf(distance_y.universe, 0.2, 3, 0.7)
distance_y['+far'] = fuzz.gbellmf(distance_y.universe, 0.2, 3, 1)

# Output membership functions
motor_y['-high'] = fuzz.gbellmf(motor_y.universe, 0.2, 3, -1)
motor_y['-average'] = fuzz.gbellmf(motor_y.universe, 0.2, 3, -0.7)
motor_y['-low'] = fuzz.gbellmf(motor_y.universe, 0.2, 3, -0.3)
motor_y['zero'] = fuzz.trimf(motor_y.universe, [-0.3, 0, 0.3])
motor_y['+low'] = fuzz.gbellmf(motor_y.universe, 0.2, 3, 0.3)
motor_y['+average'] = fuzz.gbellmf(motor_y.universe, 0.2, 3, 0.7)
motor_y['+high'] = fuzz.gbellmf(motor_y.universe, 0.2, 3, 1)


rule1 = ctrl.Rule(distance_y['+far'], motor_y['+high'])
rule2 = ctrl.Rule(distance_y['+average'], motor_y['+average'])
rule3 = ctrl.Rule(distance_y['+close'], motor_y['+low'])
rule4 = ctrl.Rule(distance_y['zero'], motor_y['zero'])
rule5 = ctrl.Rule(distance_y['-close'], motor_y['-low'])
rule6 = ctrl.Rule(distance_y['-average'], motor_y['-average'])
rule7 = ctrl.Rule(distance_y['-far'], motor_y['-high'])


y_motion_control = ctrl.ControlSystem(
    [rule1, rule2, rule3, rule4, rule5, rule6, rule7])
y_motion = ctrl.ControlSystemSimulation(y_motion_control)


def get_fuzzy_value(distance):

    y_motion.input['distance_y'] = distance
    y_motion.compute()

    return float(y_motion.output['motor_y'])
