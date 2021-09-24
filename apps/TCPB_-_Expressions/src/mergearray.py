# -*- coding: utf-8 -*-
"""Formatter class to facilitate TC Entity creation via batch.
"""

from typing import List, Union


def mergearray(array1: Union[str, List[str]], array2: Union[str, List[str]]) -> List[str]:
    """Merge the different parts of s1 and s2.  The output will
    have identical rows lineing up, but differences will be included
    at the respective match points.  This function is similar
    to an apply of a diff.  If the inputs are strings they are split
    on newline."""

    if isinstance(array1, str):
        a1 = array1.split('\n')
    else:
        a1 = array1

    if isinstance(array2, str):
        a2 = array2.split('\n')
    else:
        a2 = array2

    r1 = []
    pending = []

    while a1 or a2:
        if a1:
            v1 = a1.pop(0)
        else:
            v1 = ''

        if a2:
            v2 = a2.pop(0)
        else:
            v2 = ''

        # if the two lines match, consume both
        if v1 == v2:
            if pending:
                r1.extend(pending)
                pending = []
            if a1 or a2 or v1 or v2:  # eat trailing ''
                r1.append(v1)
            continue

        # If value 2 is in array 1, catch up array 1
        if v2 and v2 in a1:
            while v1 != v2:
                r1.append(v1)
                v1 = a1.pop(0)
            if pending:
                r1.extend(pending)
                pending = []
            if v1 or a1:
                r1.append(v1)
            continue

        # If value 1 is in array 2, catch up array 2
        if v1 and v1 in a2:
            while v1 != v2:
                if v2 or a2:
                    pending.append(v2)
                v2 = a2.pop(0)
            if pending:
                r1.extend(pending)
                pending = []
            if v1 or a1:
                r1.append(v1)
            continue

        # Otherwise, v1 gets emitted, and v2 gets accumulated
        # until there is a match

        if v1 or a1:
            r1.append(v1)
        if v2 or a2:
            pending.append(v2)

    if pending:
        r1.extend(pending)

    return r1
