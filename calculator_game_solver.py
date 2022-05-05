from collections import namedtuple
from collections import deque

SCREEN_WIDTH = 6

State = namedtuple("State", ["value", "moved", "operators", "failed", "won", "lastOperator"])

class Board:
  def __init__(self, screenWidth, operators, start, target, nMoves):
    self.screenWidth = screenWidth

    self.operators = operators
    self.start = start
    self.target = target
    self.nMoves = nMoves

    self.value = start
    self.moved = 0
    self.failed = False
    self.won = self.value == self.target

    self.lastOperator = None
    self.states = [self.getCurrentState()]


  def copy(self):
    board = Board(self.screenWidth, self.operators[:], self.start, self.target, self.nMoves)
    board.applyState(self.states[-1])
    board.states = self.states[:]
    return board

  def getCurrentState(self):
    return State(self.value, self.moved, self.operators[:], self.failed, self.won, self.lastOperator)

  def rollbackState(self, i):
    self.applyState(self.states[-(i+1)])
    self.states = self.states[:-i]

  def applyState(self, state):
    self.value = state.value
    self.moved = state.moved
    self.operators = state.operators
    self.failed = state.failed
    self.won = state.won
    self.lastOperator = state.lastOperator

  def reset(self):
    self.rollbackState(len(self.states) - 1)

  def playManualTurn(self):
    if self.won:
      self.printState()
      print("Game over. You Won!")
      return
    print('\n'.join(["Choose Operator by number: "] + [str(i) + '\t' + str(o) for i, o in enumerate(self.operators)] + [str(len(self.operators)) + '\t' + "reset"]))
    i = int(input("\nChoice: "))
    if i == len(self.operators):
      self.reset()
      return
    operator = self.operators[i]
    # self.playTurn(operator)

  def playTurn(self, operator):
    self.moved += 1
    self.lastOperator = operator
    self.applyOperation(operator)
    try:
      self.validateState()
    finally:
      self.printState()
    self.states.append(self.getCurrentState())

  def printState(self):
    print('')
    print("Moves Remaining:", self.nMoves - self.moved)
    print("Target:", self.target)
    print("Current Value:", self.value)
    print("Victory:", self.won)

  def applyOperation(self, operator):
    if type(operator) == FunOperator:
      self.operators = list(map(operator.operate, self.operators))
    else:
      self.value = operator.operate(self.value)

  def undoLastTurn(self):
    self.rollbackState(1)


  def validateState(self):
    if self.value == self.target:
      self.won = True
      return

    if self.moved >= self.nMoves:
      self.failed = True
      print("Out of moves")
      # raise RuntimeError("Out of moves")

    if len(str(self.value)) > self.screenWidth:
      self.failed = True
      print("Overflow")
      # raise RuntimeError("Overflow")


class Operator:
  def __init__(self, operation, n):
    self.operation = operation
    self.n = n
    self.o = VAL_OPERATORS.get(operation, FUN_OPERATORS.get(operation))(n)
    self.uo = VAL_OPERATORS.get(operation, FUN_OPERATORS.get(operation))(-n)

  def operate(self, v):
    return self.o(v)

  def __str__(self):
    return self.operation + " " + str(self.n)

  def __repr__(self):
    return str(self)


class FunOperator(Operator):
  def __init__(self, operation, n):
    super().__init__(operation, n)

  def operate(self, o):
    if type(o) == FunOperator:
      return o
    return self.o(o)


def sign(x):
  return int(x/abs(x))


VAL_OPERATORS = {
  "addN": lambda n: lambda v: n + v,
  "multN": lambda n: lambda v: n * v,
  "deleteN": lambda n: lambda v: v // 10^n,
  "appendN": lambda n: lambda v: int(str(v) + str(n)),
  "reflect": lambda n: lambda v: int(str(v) + ''.join(reversed(str(v)))),
  "reverse": lambda n: lambda v: int(''.join(reversed(str(v)))),
  "noop": lambda n: lambda v: v,
}

FUN_OPERATORS = {
  "faddN": lambda n: lambda vo: Operator(vo.operation, vo.n + sign(vo.n) * n)
}


def printPath(states):
  return ' -> '.join([str(s.lastOperator) for s in states])


# board = Board(SCREEN_WIDTH, [Operator("appendN", 2), Operator("addN", 5), FunOperator("faddN", 2)], 0, 101, 5)
board = Board(SCREEN_WIDTH, [Operator("appendN", 1), Operator("addN", 2), FunOperator("faddN", 3)], 21, 28, 3)

def solve(board):
  print(dfs(board.copy()))  # Solve with DFS
  # print(bfs(board.copy()))  # solve with BFS


def dfs(board):
  if board.won:
    print("Found a path", printPath(board.states))
    return board.states

  if board.failed:
    return None

  for o in board.operators:
    board.playTurn(o)
    solution = dfs(board.copy())
    if solution is not None:
      return solution
    board.undoLastTurn()
  return None

def bfs(board):
  if board.won:
    print("Found a path", printPath(board.states))
    return board.states
  
  queue = deque([board.copy()])
  while len(queue) > 0:
    b = queue.popleft()
    for o in b.operators:
      b.playTurn(o)
      if b.won:
        print("Found a path", printPath(board.states))
        return b.states
      if not b.failed:
        queue.append(b.copy())
      b.undoLastTurn()
  return None

solve(board)


# TODO: add a way to input board
def generateOptions(s):
  options = {
    # 1: lambda v: s.start =v,
    2: lambda v: setTarget
  }

def setupBoard():
  operators = []
  start = 0
  target = 0
  nMoves = 0
  screenWidth = SCREEN_WIDTH
  
  choice = None
  options = generateOptions()
  while choice != 0:
    printOptions(options)
    choiceInput = input("Choice: ")
    choiceInput = choiceInput.split()
    choice = int(choiceInput[0])