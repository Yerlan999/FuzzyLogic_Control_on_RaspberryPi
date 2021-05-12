import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


z_current = ctrl.Antecedent(np.arange(-1, 1, 0.01), 'z_current')
disk_voltage = ctrl.Consequent(np.arange(0, 1, 0.01), 'disk_voltage')

disk_voltage.defuzzify_method = 'mom'

# Custom membership functions can be built interactively with a familiar,
z_current['-overload'] = fuzz.trapmf(z_current.universe,
                                     [-1, -1, -0.90, -0.80])
z_current['-nominal'] = fuzz.trapmf(z_current.universe,
                                    [-0.90, -0.70, -0.20, -0.10])
z_current['turned_off'] = fuzz.trapmf(
    z_current.universe, [-0.20, -0.10, 0.10, 0.20])
z_current['+nominal'] = fuzz.trapmf(z_current.universe,
                                    [0.10, 0.20, 0.70, 0.90])
z_current['+overload'] = fuzz.trapmf(z_current.universe, [0.80, 0.90, 1, 1])

# Output membership functions
disk_voltage['OFF'] = fuzz.trimf(disk_voltage.universe, [0, 0, 0.5])
disk_voltage['ON'] = fuzz.trimf(disk_voltage.universe, [0.5, 1, 1])


rule1 = ctrl.Rule(z_current['-overload'], disk_voltage['OFF'])
rule2 = ctrl.Rule(z_current['-nominal'], disk_voltage['OFF'])
rule3 = ctrl.Rule(z_current['turned_off'], disk_voltage['OFF'])
rule4 = ctrl.Rule(z_current['+nominal'], disk_voltage['ON'])
rule5 = ctrl.Rule(z_current['+overload'], disk_voltage['OFF'])


disk_control = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
disk = ctrl.ControlSystemSimulation(disk_control)


def get_fuzzy_value(distance):

    disk.input['z_current'] = distance
    disk.compute()

    return float(disk.output['disk_voltage'])
