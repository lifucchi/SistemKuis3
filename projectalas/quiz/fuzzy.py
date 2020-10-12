
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def fuzzy(a , b ,p , r):
    x_discriminant, x_difficulty2 , x_prob , x_response, ability = membership()

    #infrence rule
    ability_ctrl = rule(x_discriminant, x_difficulty2 , x_prob , x_response, ability)

    theability = ctrl.ControlSystemSimulation(ability_ctrl)

    #fuzzification
    theability.input['discriminant'] = float(a)
    theability.input['difficulty2'] = float(b)
    theability.input['probabilitas'] = float(p)
    theability.input['response'] = r

    #inference
    theability.compute()

    #defuzzifikasi
    ability = (theability.output['ability'])

    return ability


def membership():
    x_discriminant = ctrl.Antecedent(np.arange(0, 1, 0.1), 'discriminant')

    # x_difficulty = ctrl.Antecedent(np.arange(0, 1, 0.1), 'difficulty')
    x_difficulty2 = ctrl.Antecedent(np.arange(-3, 3, 0.1), 'difficulty2')

    x_prob = ctrl.Antecedent(np.arange(0, 1, 0.1), 'probabilitas')
    x_response = ctrl.Antecedent(np.arange(0, 1, 0.1), 'response')
    ability = ctrl.Consequent(np.arange(-3, 3, 0.1), 'ability')

    x_discriminant['satisfactory'] = fuzz.trapmf(x_discriminant.universe, [0, 0, 0.4, 0.6])
    x_discriminant['good'] = fuzz.trapmf(x_discriminant.universe, [0.4, 0.6, 1, 1])
    # b
    # jika rentang  0 - 1
    # x_difficulty['lo'] = fuzz.trapmf(x_difficulty.universe, [0, 0, 0.4, 0.6])
    # x_difficulty['hi'] = fuzz.trapmf(x_difficulty.universe, [0.4, 0.6, 1, 1])

    # jika rentang -2 - 2
    x_difficulty2['easy'] = fuzz.trapmf(x_difficulty2.universe, [-3, -3, -1, 0])
    x_difficulty2['medium'] = fuzz.trapmf(x_difficulty2.universe, [-1, 0, 1, 2])
    x_difficulty2['high'] = fuzz.trapmf(x_difficulty2.universe, [1, 2, 3, 3])

    # p
    x_prob['min'] = fuzz.trapmf(x_prob.universe, [0, 0, 0.47, 0.50])
    x_prob['max'] = fuzz.trapmf(x_prob.universe, [0.47, 0.50, 1, 1])

    # r
    x_response['wrong'] = fuzz.trapmf(x_response.universe, [0, 0, 0.47, 0.50])
    x_response['right'] = fuzz.trapmf(x_response.universe, [0.47, 0.50, 1, 1])

    ability['verylow'] = fuzz.trapmf(ability.universe, [-3, -3, -1, -0.50])
    ability['low'] = fuzz.trimf(ability.universe, [-1, 0, 0.5])
    ability['averange'] = fuzz.trimf(ability.universe, [0, 0.5, 1.5])
    ability['good'] = fuzz.trimf(ability.universe, [0.5, 1.5, 2])
    ability['excellent'] = fuzz.trapmf(ability.universe, [1.5, 2.50, 3, 3])

    return x_discriminant, x_difficulty2 , x_prob , x_response, ability


def rule(x_discriminant, x_difficulty2, x_prob, x_response, ability):
    rule1 = ctrl.Rule(x_discriminant['satisfactory'] & x_difficulty2['easy'] & x_prob['min'] & x_response['wrong'],
                      ability['verylow'])
    rule2 = ctrl.Rule(x_discriminant['satisfactory'] & x_difficulty2['easy'] & x_prob['min'] & x_response['right'],
                      ability['low'])
    rule3 = ctrl.Rule(x_discriminant['satisfactory'] & x_difficulty2['easy'] & x_prob['max'] & x_response['wrong'],
                      ability['verylow'])
    rule4 = ctrl.Rule(x_discriminant['satisfactory'] & x_difficulty2['easy'] & x_prob['max'] & x_response['right'],
                      ability['averange'])
    rule5 = ctrl.Rule(x_discriminant['satisfactory'] & x_difficulty2['medium'] & x_prob['min'] & x_response['wrong'],
                      ability['low'])
    rule6 = ctrl.Rule(x_discriminant['satisfactory'] & x_difficulty2['medium'] & x_prob['min'] & x_response['right'],
                      ability['averange'])
    rule7 = ctrl.Rule(x_discriminant['satisfactory'] & x_difficulty2['medium'] & x_prob['max'] & x_response['wrong'],
                      ability['low'])
    rule8 = ctrl.Rule(x_discriminant['satisfactory'] & x_difficulty2['medium'] & x_prob['max'] & x_response['right'],
                      ability['good'])
    rule9 = ctrl.Rule(x_discriminant['satisfactory'] & x_difficulty2['high'] & x_prob['min'] & x_response['wrong'],
                      ability['averange'])
    rule10 = ctrl.Rule(x_discriminant['satisfactory'] & x_difficulty2['high'] & x_prob['min'] & x_response['right'],
                       ability['good'])
    rule11 = ctrl.Rule(x_discriminant['satisfactory'] & x_difficulty2['high'] & x_prob['max'] & x_response['wrong'],
                       ability['averange'])
    rule12 = ctrl.Rule(x_discriminant['satisfactory'] & x_difficulty2['high'] & x_prob['max'] & x_response['right'],
                       ability['excellent'])
    rule13 = ctrl.Rule(x_discriminant['good'] & x_difficulty2['easy'] & x_prob['min'] & x_response['wrong'],
                       ability['low'])
    rule14 = ctrl.Rule(x_discriminant['good'] & x_difficulty2['easy'] & x_prob['min'] & x_response['right'],
                       ability['averange'])
    rule15 = ctrl.Rule(x_discriminant['good'] & x_difficulty2['easy'] & x_prob['max'] & x_response['wrong'],
                       ability['verylow'])
    rule16 = ctrl.Rule(x_discriminant['good'] & x_difficulty2['easy'] & x_prob['max'] & x_response['right'],
                       ability['averange'])
    rule17 = ctrl.Rule(x_discriminant['good'] & x_difficulty2['medium'] & x_prob['min'] & x_response['wrong'],
                       ability['averange'])
    rule18 = ctrl.Rule(x_discriminant['good'] & x_difficulty2['medium'] & x_prob['min'] & x_response['right'],
                       ability['good'])
    rule19 = ctrl.Rule(x_discriminant['good'] & x_difficulty2['medium'] & x_prob['max'] & x_response['wrong'],
                       ability['low'])
    rule20 = ctrl.Rule(x_discriminant['good'] & x_difficulty2['medium'] & x_prob['max'] & x_response['right'],
                       ability['excellent'])
    rule21 = ctrl.Rule(x_discriminant['good'] & x_difficulty2['high'] & x_prob['min'] & x_response['wrong'],
                       ability['averange'])
    rule22 = ctrl.Rule(x_discriminant['good'] & x_difficulty2['high'] & x_prob['min'] & x_response['right'],
                       ability['excellent'])
    rule23 = ctrl.Rule(x_discriminant['good'] & x_difficulty2['high'] & x_prob['max'] & x_response['wrong'],
                       ability['averange'])
    rule24 = ctrl.Rule(x_discriminant['good'] & x_difficulty2['high'] & x_prob['max'] & x_response['right'],
                       ability['excellent'])

    ability_ctrl = ctrl.ControlSystem(
        [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule15,
         rule16, rule17, rule18, rule19, rule20, rule21, rule22, rule23, rule24])

    return ability_ctrl



# print (fuzzy(-0.053 , 0.61 ,0.5 , 0))
# print (fuzzy(0.8 , -0.4055 ,0.5 , 1))