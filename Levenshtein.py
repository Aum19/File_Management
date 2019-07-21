import numpy as np
from functools import lru_cache

@lru_cache(maxsize=5000)
def levenshtein_lru(s, t):
	if not s: return len(t)
	if not t: return len(s)
	if s[0] == t[0]: return levenshtein_lru(s[1:], t[1:])
	l1 = levenshtein_lru(s, t[1:])
	l2 = levenshtein_lru(s[1:], t)
	l3 = levenshtein_lru(s[1:], t[1:])
	return 1 + min(l1, l2, l3)

def levenshtein_no_lru(seq1, seq2):  
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in range(size_x):
        matrix [x, 0] = x
    for y in range(size_y):
        matrix [0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + 1,
                    matrix[x-1,y-1] + 1,
                    matrix[x,y-1] + 1
                )
    return (matrix[size_x - 1, size_y - 1])
