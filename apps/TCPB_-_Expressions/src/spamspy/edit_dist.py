# -*- coding: utf-8 -*-
from sys import argv


class Costs:
    insert = 1
    delete = 1
    change = 2  # like insertion + deletion
    swap = 2  # same


def costs_matrix(a, b, costs):
    """
    a = 'xyz'
    b = 'ayzb'

    m = /   a y z b
          0 1 2 3 4
        x 1 2 3 4 5
        y 2 3 2 3 4
        z 3 4 3 2 3

    m[row][col] -> m[2][4] == 6
    """
    height = len(a) + 1
    width = len(b) + 1

    m = [[0] * width for _ in range(height)]

    for row in range(height):
        m[row][0] = row * costs.delete

    for col in range(width):
        m[0][col] = col * costs.insert

    for row in range(1, height):
        for col in range(1, width):
            north = m[row - 1][col]
            west = m[row][col - 1]
            north_west = m[row - 1][col - 1]

            if a[row - 1] == b[col - 1]:
                m[row][col] = north_west
            else:
                m[row][col] = min(
                    north + costs.delete, west + costs.insert, north_west + costs.change
                )

            if row > 1 and col > 1 and a[row - 2] == b[col - 1] and a[row - 1] == b[col - 2]:

                before_two = m[row - 2][col - 2]

                m[row][col] = min(m[row][col], before_two + costs.swap)

    return m


def edit_dist(a, b, costs=None):
    costs = costs or Costs()
    m = costs_matrix(a, b, costs)
    return m[-1][-1]


def _print_costs_matrix(a, b):
    # XXX mainly for debug purposes; consider removing
    m = costs_matrix(a, b, Costs())

    print(' '.join('/ ' + b))

    for line, c in zip(m, ' ' + a):
        print(c, end=' ')

        for item in line:
            print(item, end=' ')

        print()


def print_costs_matrix():
    a, b = 'xyz', 'ayzb'
    print_costs_matrix(a, b)


def main():
    a, b = argv[1:]
    print(edit_dist(a, b))


if __name__ == '__main__':
    main()
