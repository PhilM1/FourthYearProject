"""
This script is used for testing Continuous Sampling
"""

from ContinuousSampling import ContinuousSampling

minimums = [1, 20]
maximums = [10, 30]
test = ContinuousSampling(minimums, maximums, 1)
for n in range(100):
    print(test.get_current_values())
    test.increment_values()
