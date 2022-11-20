from testing_suite_full import GliderSimulator, GLOBAL_PARAMETERS
from marsglider import estimate_next_pos, next_angle
import sys
import pdb

try:
    test_case = int(sys.argv[1])
    test_type = sys.argv[2]
except:
    print("Usage: python test_single.py test_number estimate|navigate")
    exit(1)
    
params = GLOBAL_PARAMETERS[test_case]
params['tolerance_ratio'] = 0.02
params['part'] = 'A'
params['noise_ratio'] = 0.00

class FakeQ():
    def __init__(self):
        self.L = []
    def empty(self):
        return len(self.L) == 0
    def put(self, item):
        self.L.append(item)
    def get(self):
        self.L.pop() # pop(0) for first item?
            
class GliderSimulatorStandAlone(GliderSimulator):
    def __init__(self):
        self.glider_steps = FakeQ()
        self.glider_found = FakeQ()
        self.glider_error = FakeQ()
                                    
G = GliderSimulatorStandAlone()

if test_type == "estimate":
    G.simulate_without_steering(estimate_next_pos, params)
else:
    G.simulate_with_steering(next_angle, params)
    

print("---------- glider_steps ----------")
print((G.glider_steps.L))
print("---------- glider_found ----------")
print((G.glider_found.L))
print("---------- glider_error ----------")
for error in  G.glider_error.L:
    print(error)
