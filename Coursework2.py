#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MATH20621 - Coursework 2
Student name: Yaocong Deng
Student id:   REDACTED
Student mail: REDACTED
"""
import random

# Problem 1
def turing_step(s, p):
    n = len(s)
    s.append(s[0]) # Add the leftmost value at the end
    s.pop(0)       # Delete the leftmost value
    
    if random.uniform(0, 1) < p:
        s[-1] = 1 - s[-1]     # Filp randomly
    
    value = sum(2**(-i-1)*s[i] for i in range(n)) # 
    return value

# Problem 2
def turing_period(s, p):
    initial_s = s[:]
    current_s = s[:] # Start from the initial state
    steps = 0
    
    while True:
        steps += 1
        turing_step(current_s, p)

        if current_s == initial_s:  # Check if state returns to the initial state
            break
    
    return steps


# Problem 3
def diff_distn(v_list):
    n = len(v_list)
    # The differences between adjacent values
    v_diff = [v_list[i] - v_list[i-1] for i in range(1,n)]
    # Create a dictionary
    diff_counts = {}
    # Counting number
    for diff in v_diff:
        if diff not in diff_counts:
            diff_counts[diff] = 1
        else:
            diff_counts[diff] += 1

    return diff_counts



# main() function for all the testing
def main():
    # TODO (optional): do any testing you wish here
    # This main function will not be assessed
    state1 = [1,0,1,1,0,0,0,1]
    print("V = ", turing_step(state1, 0.3)) # should display 0.3828125 or 0.38671875
    print("State is ", state1) # 01100010 if V = 0.3828125 or 01100011 if V = 0.38671875
    print(turing_period(state1, 0.5)) # should display a random integer
    print("State is ", state1) # the same as before
    state2 = [0,0,0,0,0,0,0,0]
    print(turing_period(state2, 0)) # should display 1
    print(diff_distn([0, 0.5, 0.25, 0])) # Should display {0.5: 1, -0.25: 2}
    print(diff_distn([0.125,0,0.5,0.25,0.5,0.125,0,0.5])) # SHould display {-0.125: 2, 0.5: 2, -0.25: 1, 0.25: 1, -0.375: 1}
    print(turing_period([0, 1, 0, 0, 1, 0], 1))
    print(turing_period([0, 0], 1))
    print(turing_period([0, 0, 0, 0], 0.25))
    return


main() # call main() function to run all tests