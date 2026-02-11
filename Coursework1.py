#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MATH20621 - Coursework 1
Student name: Yaocong Deng
Student id:   REDACTED
Student mail: REDACTED
"""

# Problem 1
def leap_year(year):
    
    if year % 400 == 0:
        return True
    elif year % 100 == 0:
        return False
    elif year % 4 == 0:
        return True
    else:
        return False

# Problem 2
def divisors(n):
    u = 0
    for i in range(1, n):
        if n % i == 0:
            u += 1
    return u


# Problem 3
def highly_composite(m):
    max_divisors = 0
    num = 1
    found = 0  

    while found < m:
        # We need to add n itself
        current_divisors = divisors(num) + 1
        if current_divisors > max_divisors:
            max_divisors = current_divisors
            found += 1
            if found == m:
                return num  
        num += 1



# main() function for all the testing
def main():
    # TODO (optional): do any testing you wish here
    # This main function will not be assessed

    print("should return True:   ", leap_year(2024))
    print("should return False:  ", leap_year(1900))
    print("should return 3:   ", divisors(6))
    print("should return 5:   ", divisors(12))
    print("should return 2:   ", highly_composite(2))
    print("should return 12:  ", highly_composite(5))

main() # call main() function to run all tests
