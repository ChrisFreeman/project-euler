#
'''
Project Euler - Problem 1 - Multiples of 3 and 5
https://projecteuler.net/problem=1

If we list all the natural numbers below 10 that are multiples of 3 or 5, we
get 3, 5, 6 and 9. The sum of these multiples is 23.

Find the sum of all the multiples of 3 or 5 below 1000.
'''

import sys


def main():
    '''Sum the numbers from 1 through 999 that are multiples of either 3 or 5.
    '''
    # get list of numbers using list comprehension
    numbers = [x for x in range(1, 1000) if x % 3 == 0 or x % 5 == 0]
    count = len(numbers)
    total = sum(numbers)
    # display length of list and the sum of its elements
    print("There are {0} numbers from 1 through 999 that are multiples of either"
          "3 or 5. Their sum is: {1}".format(count, total))

    # One line alternative solution
    # sum the output of a generator whose elements are from 1 to 999 and provided
    # they are a multiple of 3 or 5 using modulo arithmetic. No intermediate list
    # is constructed.
    total = sum(x for x in range(1, 1000) if x % 3 == 0 or x % 5 == 0)
    print("Alternative: Sum of numbers 1 through 999 that are multiples of either"
          " 3 or 5: {0}".format(total))

if __name__ == '__main__':
    # interactive run main, capture keyboard interrupts
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass
