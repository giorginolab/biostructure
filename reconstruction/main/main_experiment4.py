import numpy as np

def solve(X, Y, solution=[]):
  if not X:
    yield list(solution)
  else:
    c = min(X, key=lambda c: len(X[c]))
    for r in list(X[c]):
      solution.append(r)
      cols = select(X, Y, r)
      for s in solve(X, Y, solution):
        yield s
      deselect(X, Y, r, cols)
      solution.pop()


def select(X, Y, r):
  cols = []
  for j in Y[r]:     #En cada una de las columnas que este presente
    for i in X[j]:     #Para cada uno de los valores de esa columna
      for k in Y[i]:     #Para cada una de las columnas en que esten esos valores
        if k != j:
          X[k].remove(i)
    cols.append(X.pop(j))
  return cols


def deselect(X, Y, r, cols):
  for j in reversed(Y[r]):
    X[j] = cols.pop()
    for i in X[j]:
      for k in Y[i]:
        if k != j:
          X[k].add(i)

if __name__ == '__main__':
  X = {1, 2, 3, 4, 5, 6, 7}
  Y = {
    'A': [1, 4, 7],
    'B': [1, 4],
    'C': [4, 5, 7],
    'D': [3, 5, 6],
    'E': [2, 3, 6, 7],
    'F': [2, 7]}

  X = {j: set() for j in X}
  for i in Y:
    for j in Y[i]:
      X[j].add(i)
  result = list(solve(X, Y))
  print(result)
