"""
AUTHOR: Daudi Wampamba
"""

from functools import cache
from time import time

SPACING = 3

class BoardState():
    state = [[0 for _ in range(3)] for _ in range(3)]

    def __init__(self, state = None, player = 0):
        if(state is not None):
            self.state = state
        self.player = player # -1 for player, 1 for computer

    @cache
    def get_valid(self):
        valid = []
        for (y, ys) in enumerate(self.state):
            for (x, xv) in enumerate(ys):
                if(xv == 0):
                    valid.append((x,y))
        return valid

    @cache
    def get_child(self, move):
        if(move not in self.get_valid()):
            raise KeyError("Invalid Move")
        childState = [[self.player if (x, y) == move else xv for x, xv in enumerate(ys)] for y, ys in enumerate(self.state)]
        return BoardState(state=childState, player= -1 if self.player == 1 else 1)

    @cache
    def get_children(self):
        return [self.get_child(move) for move in self.get_valid()]
    
    @cache
    def get_alphabeta_value(self, alpha=float('-inf'), beta=float('inf')):
        if(value := self.goal_test()):
            return value
        value = float('inf')
        if self.player == 1:
            value = float('-inf')
            for child in self.get_children():
                value = max(value, child.get_alphabeta_value(alpha, beta))
                alpha = max(alpha, value)
                if alpha > beta:
                    break
        else:
            value = float('inf')
            for child in self.get_children():
                value = min(value, child.get_alphabeta_value(alpha, beta))
                beta = min(beta, value)
                if alpha > beta:
                    break
        return value

    @cache
    def goal_test(self):
        for k in [-1, 1]:
            if(
                any(all(s == k for s in self.state[i]) for i in range(len(self.state))) or # row win
                any(all(s[i] == k for s in self.state) for i in range(len(self.state))) or # column win
                all([self.state[0][0] == k, self.state[1][1] == k, self.state[2][2] == k]) or # diagonal one
                all([self.state[0][2] == k, self.state[1][1] == k, self.state[2][0] == k]) # diagonal two
            ):
                v = (1 + sum(s.count(0) for s in self.state)) * k
                break
        else:
            v = 0
        return v

    @cache
    def get_utility_value(self):
        # print(self)
        value = self.goal_test()
        if(value == 0):
            f = max if self.player == 1 else min
            l = [child.get_utility_value() for child in self.get_children()]
            if(len(l) <= 0):
                return 0
            value = f(l)
        return value

    def play_turn(self):
        print(self)
        tbr = None
        if(self.player == -1):
            try:
                io = reversed([(int(x) - 1) for x in input("Enter a move (y, x): ").split(',')])
                tbr = self.get_child(tuple(io))
            except (ValueError, KeyError):
                print("BAD MOVE")
                tbr = self
        else:
            st = time()
            max_child = None
            for child in self.get_children():
                if(max_child is None):
                    max_child = child
                    continue
                # if(child.get_alphabeta_value() > max_child.get_alphabeta_value()):
                if(child.get_utility_value() > max_child.get_utility_value()):
                    max_child = child
            tbr = max_child
            print("Computer took: " + str(time() - st) + "s")
        if(tbr == None):
            return None
        if((test := tbr.goal_test()) != 0 or len(tbr.get_children()) <= 0):
            print(tbr)
            if(test < 0):
                print("You won!")
            elif(test == 0):
                print("You drew")
            else:
                print("You lost...")
            print("Your Score: " + str(test * -1))
            return None
        return tbr

    def __str__(self):
        spacing = SPACING
        def get_symbol(p):
            if(p == -1):
                return "X"
            elif(p == 1):
                return "O"
            else:
                return " "

        return \
            "=" * (spacing * 2 * 3 + 2 + 3) + "\n" + \
            " " * (spacing * 2 + 1) + "|" + " " * (spacing * 2 + 1) + "|" + " " * (spacing * 2 + 1) + "\n" + \
            " " * spacing + get_symbol(self.state[0][0]) + " " * spacing + "|" + " " * spacing + get_symbol(self.state[0][1]) + " " * spacing + "|" + " " * spacing + get_symbol(self.state[0][2]) + " " * spacing + "\n" + \
            " " * (spacing * 2 + 1) + "|" + " " * (spacing * 2 + 1) + "|" + " " * (spacing * 2 + 1) + "\n" + \
            "-" * (spacing * 2 + 1) + "+" + "-" * (spacing * 2 + 1) + "+" + "-" * (spacing * 2 + 1) + "\n" + \
            " " * (spacing * 2 + 1) + "|" + " " * (spacing * 2 + 1) + "|" + " " * (spacing * 2 + 1) + "\n" + \
            " " * spacing + get_symbol(self.state[1][0]) + " " * spacing + "|" + " " * spacing + get_symbol(self.state[1][1]) + " " * spacing + "|" + " " * spacing + get_symbol(self.state[1][2]) + " " * spacing + "\n" + \
            " " * (spacing * 2 + 1) + "|" + " " * (spacing * 2 + 1) + "|" + " " * (spacing * 2 + 1) + "\n" + \
            "-" * (spacing * 2 + 1) + "+" + "-" * (spacing * 2 + 1) + "+" + "-" * (spacing * 2 + 1) + "\n" + \
            " " * (spacing * 2 + 1) + "|" + " " * (spacing * 2 + 1) + "|" + " " * (spacing * 2 + 1) + "\n" + \
            " " * spacing + get_symbol(self.state[2][0]) + " " * spacing + "|" + " " * spacing + get_symbol(self.state[2][1]) + " " * spacing + "|" + " " * spacing + get_symbol(self.state[2][2]) + " " * spacing + "\n" + \
            " " * (spacing * 2 + 1) + "|" + " " * (spacing * 2 + 1) + "|" + " " * (spacing * 2 + 1)

if(__name__=='__main__'):
    current_board = BoardState(player=-1)
    while current_board:
        try:
            current_board = current_board.play_turn()
        except RecursionError:
            print("Recursion limit")
            break