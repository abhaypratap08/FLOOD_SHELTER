#Defines membership functions and rules

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def get_fuzzy_simulator(capacity_val, distance_val, accessibility_val, elevation_val, proximity_val, medical_val):

  distance=ctrl.Antecedent(np.arange(0,21,1),'distance')
  distance['near']=fuzz.trimf(distance.universe,[0,0,7])
  distance['medium']=fuzz.trimf(distance.universe,[5,10,15])
  distance['far']=fuzz.trimf(distance.universe,[12,20,20])

  capacity=ctrl.Antecedent(np.arange(0,101,1),'capacity')
  capacity['low']=fuzz.trimf(capacity.universe,[0,0,40])
  capacity['medium']=fuzz.trimf(capacity.universe,[30,50,70])
  capacity['high']=fuzz.trimf(capacity.universe,[60,100,100])

  accessibility=ctrl.Antecedent(np.arange(0,11,1),'accessibility')
  accessibility['low']=fuzz.trimf(accessibility.universe,[0,0,4])
  accessibility['medium']=fuzz.trimf(accessibility.universe,[3,5,7])
  accessibility['high']=fuzz.trimf(accessibility.universe,[6,10,10])

  suitability = ctrl.Consequent(np.arange(0, 101, 1), 'suitability')
  suitability['low'] = fuzz.trimf(suitability.universe, [0, 0, 40])
  suitability['medium'] = fuzz.trimf(suitability.universe, [30, 50, 70])
  suitability['high'] = fuzz.trimf(suitability.universe, [60, 100, 100])
  
  elevation = ctrl.Antecedent(np.arange(0, 11, 1), 'elevation')
  elevation['low'] = fuzz.trimf(elevation.universe, [0, 0, 4])
  elevation['medium'] = fuzz.trimf(elevation.universe, [3, 5, 7])
  elevation['high'] = fuzz.trimf(elevation.universe, [6, 10, 10])

  proximity = ctrl.Antecedent(np.arange(0, 11, 1), 'proximity')
  proximity['very close'] = fuzz.trimf(proximity.universe, [0, 0, 3])
  proximity['moderate'] = fuzz.trimf(proximity.universe, [2, 5, 8])
  proximity['far'] = fuzz.trimf(proximity.universe, [7, 10, 10])

  medical = ctrl.Antecedent(np.arange(0, 11, 1), 'medical')
  medical['none'] = fuzz.trimf(medical.universe, [0, 0, 3])
  medical['basic'] = fuzz.trimf(medical.universe, [2, 5, 7])
  medical['advanced'] = fuzz.trimf(medical.universe, [6, 10, 10])


  rule1  = ctrl.Rule(distance['near'] & capacity['high'] & accessibility['high'] & elevation['high'] & proximity['moderate'] & medical['advanced'], suitability['high'])
  rule2  = ctrl.Rule(distance['near'] & capacity['medium'] & accessibility['high'] & elevation['high'] & proximity['far'] & medical['advanced'], suitability['high'])
  rule3  = ctrl.Rule(distance['medium'] & capacity['high'] & accessibility['high'] & elevation['high'] & proximity['far'] & medical['advanced'], suitability['high'])
  rule4  = ctrl.Rule(distance['near'] & capacity['high'] & accessibility['medium'] & elevation['high'] & proximity['moderate'] & medical['advanced'], suitability['high'])
  rule5  = ctrl.Rule(distance['near'] & capacity['high'] & accessibility['high'] & elevation['medium'] & proximity['moderate'] & medical['advanced'], suitability['high'])
  rule6  = ctrl.Rule(distance['medium'] & capacity['high'] & accessibility['high'] & elevation['medium'] & proximity['far'] & medical['advanced'], suitability['high'])
  rule7  = ctrl.Rule(distance['near'] & capacity['medium'] & accessibility['high'] & elevation['high'] & proximity['moderate'] & medical['basic'], suitability['high'])
  rule8  = ctrl.Rule(distance['near'] & capacity['high'] & accessibility['medium'] & elevation['high'] & proximity['far'] & medical['basic'], suitability['high'])
  rule9  = ctrl.Rule(distance['medium'] & capacity['high'] & accessibility['medium'] & elevation['high'] & proximity['moderate'] & medical['advanced'], suitability['high'])
  rule10 = ctrl.Rule(distance['near'] & capacity['medium'] & accessibility['medium'] & elevation['high'] & proximity['moderate'] & medical['advanced'], suitability['high'])
  rule11 = ctrl.Rule(distance['medium'] & capacity['medium'] & accessibility['high'] & elevation['high'] & proximity['moderate'] & medical['advanced'], suitability['high'])
  rule12 = ctrl.Rule(distance['near'] & capacity['high'] & accessibility['high'] & elevation['high'] & proximity['far'] & medical['basic'], suitability['high'])
  rule13 = ctrl.Rule(distance['medium'] & capacity['medium'] & accessibility['medium'] & elevation['medium'] & proximity['moderate'] & medical['basic'], suitability['medium'])
  rule14 = ctrl.Rule(distance['far'] & capacity['high'] & accessibility['medium'] & elevation['high'] & proximity['moderate'] & medical['basic'], suitability['medium'])
  rule15 = ctrl.Rule(distance['medium'] & capacity['high'] & accessibility['low'] & elevation['medium'] & proximity['far'] & medical['advanced'], suitability['medium'])
  rule16 = ctrl.Rule(distance['near'] & capacity['low'] & accessibility['medium'] & elevation['medium'] & proximity['moderate'] & medical['advanced'], suitability['medium'])
  rule17 = ctrl.Rule(distance['near'] & capacity['medium'] & accessibility['medium'] & elevation['low'] & proximity['moderate'] & medical['basic'], suitability['medium'])
  rule18 = ctrl.Rule(distance['medium'] & capacity['medium'] & accessibility['high'] & elevation['medium'] & proximity['far'] & medical['basic'], suitability['medium'])
  rule19 = ctrl.Rule(distance['medium'] & capacity['medium'] & accessibility['medium'] & elevation['high'] & proximity['very close'] & medical['advanced'], suitability['medium'])
  rule20 = ctrl.Rule(distance['medium'] & capacity['medium'] & accessibility['medium'] & elevation['low'] & proximity['far'] & medical['advanced'], suitability['medium'])
  rule21 = ctrl.Rule(distance['near'] & capacity['medium'] & accessibility['low'] & elevation['high'] & proximity['moderate'] & medical['advanced'], suitability['medium'])
  rule22 = ctrl.Rule(distance['far'] & capacity['high'] & accessibility['high'] & elevation['low'] & proximity['moderate'] & medical['basic'], suitability['medium'])
  rule23 = ctrl.Rule(distance['near'] & capacity['medium'] & accessibility['medium'] & elevation['medium'] & proximity['moderate'] & medical['basic'], suitability['medium'])
  rule24 = ctrl.Rule(distance['medium'] & capacity['medium'] & accessibility['medium'] & elevation['medium'] & proximity['moderate'] & medical['basic'], suitability['medium'])
  rule25 = ctrl.Rule(distance['near'] & capacity['low'] & accessibility['high'] & elevation['medium'] & proximity['moderate'] & medical['basic'], suitability['medium'])
  rule26 = ctrl.Rule(distance['far'] & capacity['medium'] & accessibility['medium'] & elevation['medium'] & proximity['moderate'] & medical['advanced'], suitability['medium'])
  rule27 = ctrl.Rule(distance['medium'] & capacity['low'] & accessibility['high'] & elevation['high'] & proximity['far'] & medical['basic'], suitability['medium'])
  rule28 = ctrl.Rule(distance['near'] & capacity['medium'] & accessibility['high'] & elevation['medium'] & proximity['very close'] & medical['basic'], suitability['medium'])
  rule29 = ctrl.Rule(distance['medium'] & capacity['medium'] & accessibility['high'] & elevation['low'] & proximity['moderate'] & medical['advanced'], suitability['medium'])
  rule30 = ctrl.Rule(distance['medium'] & capacity['high'] & accessibility['high'] & elevation['low'] & proximity['moderate'] & medical['basic'], suitability['medium'])
  rule31 = ctrl.Rule(distance['far'] & capacity['medium'] & accessibility['high'] & elevation['high'] & proximity['moderate'] & medical['advanced'], suitability['medium'])
  rule32 = ctrl.Rule(distance['near'] & capacity['medium'] & accessibility['medium'] & elevation['high'] & proximity['very close'] & medical['advanced'], suitability['medium'])
  rule33 = ctrl.Rule(distance['far'] & capacity['low'] & accessibility['high'] & elevation['high'] & proximity['far'] & medical['advanced'], suitability['medium'])
  rule34 = ctrl.Rule(distance['medium'] & capacity['high'] & accessibility['low'] & elevation['high'] & proximity['moderate'] & medical['advanced'], suitability['medium'])
  rule35 = ctrl.Rule(distance['far'] & capacity['medium'] & accessibility['medium'] & elevation['high'] & proximity['moderate'] & medical['basic'], suitability['medium'])
  rule36 = ctrl.Rule(distance['near'] & capacity['medium'] & accessibility['medium'] & elevation['medium'] & proximity['moderate'] & medical['basic'], suitability['medium'])
  rule37 = ctrl.Rule(distance['far'] & capacity['low'] & accessibility['low'] & elevation['low'] & proximity['very close'] & medical['none'], suitability['low'])
  rule38 = ctrl.Rule(distance['far'] & capacity['low'] & accessibility['medium'] & elevation['low'] & proximity['very close'] & medical['none'], suitability['low'])
  rule39 = ctrl.Rule(distance['medium'] & capacity['low'] & accessibility['low'] & elevation['low'] & proximity['very close'] & medical['none'], suitability['low'])
  rule40 = ctrl.Rule(distance['medium'] & capacity['low'] & accessibility['medium'] & elevation['low'] & proximity['very close'] & medical['none'], suitability['low'])
  rule41 = ctrl.Rule(distance['far'] & capacity['medium'] & accessibility['low'] & elevation['low'] & proximity['very close'] & medical['none'], suitability['low'])
  rule42 = ctrl.Rule(distance['medium'] & capacity['low'] & accessibility['medium'] & elevation['low'] & proximity['moderate'] & medical['none'], suitability['low'])
  rule43 = ctrl.Rule(distance['far'] & capacity['low'] & accessibility['low'] & elevation['medium'] & proximity['very close'] & medical['none'], suitability['low'])
  rule44 = ctrl.Rule(distance['far'] & capacity['low'] & accessibility['low'] & elevation['low'] & proximity['moderate'] & medical['none'], suitability['low'])
  rule45 = ctrl.Rule(distance['near'] & capacity['low'] & accessibility['low'] & elevation['low'] & proximity['very close'] & medical['none'], suitability['low'])
  rule46 = ctrl.Rule(distance['medium'] & capacity['low'] & accessibility['low'] & elevation['low'] & proximity['moderate'] & medical['none'], suitability['low'])
  rule47 = ctrl.Rule(distance['medium'] & capacity['low'] & accessibility['low'] & elevation['low'] & proximity['far'] & medical['none'], suitability['low'])
  rule48 = ctrl.Rule(distance['far'] & capacity['low'] & accessibility['low'] & elevation['low'] & proximity['far'] & medical['none'], suitability['low'])
  rule49 = ctrl.Rule(distance['far'] & capacity['low'] & accessibility['low'] & elevation['low'] & proximity['very close'] & medical['basic'], suitability['low'])

  rule50 = ctrl.Rule(antecedent=((distance['near'] | distance['medium'] | distance['far']) & 
                               (capacity['low'] | capacity['medium'] | capacity['high'])), 
                   consequent=suitability['medium'])

  suitability_ctrl = ctrl.ControlSystem([
    rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10,
    rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18, rule19, rule20,
    rule21, rule22, rule23, rule24, rule25, rule26, rule27, rule28, rule29, rule30,
    rule31, rule32, rule33, rule34, rule35, rule36, rule37, rule38, rule39, rule40,
    rule41, rule42, rule43, rule44, rule45, rule46, rule47, rule48, rule49, rule50
  ])
  
  sim=ctrl.ControlSystemSimulation(suitability_ctrl)
  
  sim.input['capacity'] = capacity_val
  sim.input['distance'] = distance_val
  sim.input['accessibility'] = accessibility_val
  sim.input['elevation'] = elevation_val
  sim.input['proximity'] = proximity_val
  sim.input['medical'] = medical_val

  sim.compute()
  return sim.output['suitability']
