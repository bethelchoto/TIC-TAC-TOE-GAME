import sys
import copy
INF = sys.maxsize


class Game:
    def __init__(self, init_state):
        self.init_state = init_state

    def __str__(self):
        return "Init_state="+str(init_state)

    # placeholder, to be overridden in derived class
    def terminal_test(self, state):
        return True

    # placeholder, to be overriden in derived class
    def utility(self, state):
        return 0

    # placeholder, to be overriden in derived class
    def actions(self, state):
        moves = []
        return moves

    # placeholder, to be overriden in derived class
    def result(self, state, action):
        return state


BLANK = '_'
X = 'X'
O = 'O'
EMPTY_GRID = [[BLANK, BLANK, BLANK],
              [BLANK, BLANK, BLANK],
              [BLANK, BLANK, BLANK]]


class TicTacToe(Game):
    def __init__(self):
        super().__init__(copy.deepcopy(EMPTY_GRID))
        self.player = "X"

    def terminal_test(self, state):
        # if there is no empty space then it's a terminal state
        if not (BLANK in state[0] or
                BLANK in state[1] or
                BLANK in state[2]):
            return True

        # otherwise, if there's a winner, it's a terminal state
        winner = self.winner(state)
        return winner == X or winner == O

    def winner(self, state):
        # check each row for a winning configuration
        for row in [0, 1, 2]:
            if (state[row][0] != BLANK and
                state[row][0] == state[row][1] and
                    state[row][0] == state[row][2]):
                return state[row][0]

        # check each column for a winner configuration
        for col in [0, 1, 2]:
            if (state[0][col] != BLANK and
                state[0][col] == state[1][col] and
                    state[0][col] == state[2][col]):
                return state[0][col]

        # check the top left to bottom right diagonal
        if (state[0][0] != BLANK and
            state[0][0] == state[1][1] and
                state[0][0] == state[2][2]):
            return state[0][0]

        # check the bottom left to top right diagonal
        if (state[2][0] != BLANK and
            state[2][0] == state[1][1] and
                state[2][0] == state[0][2]):
            return state[2][0]

        return None

    def utility(self, state):
        winner = self.winner(state)
        if winner == X:
            return 1
        elif winner == O:
            return -1
        else:
            return 0

    def actions(self, state):
        moves = []
        for row in [0, 1, 2]:
            for col in [0, 1, 2]:
                if state[row][col] == BLANK:
                    moves.append((row, col))
        return moves

    def result(self, state, action, player):
        res_state = copy.deepcopy(state)
        res_state[action[0]][action[1]] = player
        return res_state


n_levels = 0
n_states = 0
n_terminal_states = 0
states = dict()
playing_position = None
terminal_states = set()
player = None


def minimax_decision(game, state):
    global n_levels, n_states,player, n_terminal_states, states, terminal_states, playing_position
    n_levels = n_states = n_terminal_states = 0
    states = dict()
    terminal_states = set()

    if (player == O):
        value = INF
    elif(player == X):
        value = -INF
    else:
        print("YOU HAVE ENTERED AN INVALID INPUT PLEASE RESTART THE GAME, BYE\n")
        quit()
        
    best_action = None
    actions = game.actions(state)
    for i in range(len(actions)):
        result_state = game.result(state, actions[i], player)
        statestr = grid_to_str(result_state)
        if statestr in states:
            next_state_value = states[statestr]
        else:
            n_states += 1
            if(player == O):
                next_state_value = max_value(game, result_state, 1)
                
            else:
                next_state_value = min_value(game, result_state, 1)
            states[statestr] = next_state_value
        if (player == O):
            if (next_state_value < value):
                value = next_state_value
                best_action = actions[i]
        else:
            if(next_state_value > value):
                value = next_state_value
                best_action = actions[i]
    return best_action


def max_value(game, state, level):
    global n_levels, n_states, n_terminal_states, states
    n_levels = max(n_levels, level)
    if game.terminal_test(state):
        util = game.utility(state)
        #print_grid("Reached terminal state with utility "+str(util)+":",state)
        n_terminal_states += 1
        terminal_states.add(grid_to_str(state))
        return util
    value = -INF 
    actions = game.actions(state)
    for action in actions:
        next_state = game.result(state, action, X) 
        statestr = grid_to_str(next_state)
        if statestr in states:
            next_state_value = states[statestr]
        else:
            n_states += 1
            next_state_value = min_value(game, next_state, level+1)
            states[grid_to_str(next_state)] = next_state_value
        value = max(value, next_state_value)
    return value


def min_value(game, state, level):
    global n_levels, n_states, n_terminal_states, states
    n_levels = max(n_levels, level)
    if game.terminal_test(state):
        util = game.utility(state)
        #print_grid("Reached terminal state with utility "+str(util)+":",state)
        n_terminal_states += 1
        terminal_states.add(grid_to_str(state))
        return util
    value = INF
    actions = game.actions(state)
    for action in actions:
        next_state = game.result(state, action, O)
        statestr = grid_to_str(next_state)
        if statestr in states:
            next_state_value = states[statestr]
        else:
            n_states += 1
            next_state_value = max_value(game, next_state, level+1)
            states[grid_to_str(next_state)] = next_state_value
        value = min(value, next_state_value)
    return value


def read_grid(prompt, grid):
    print(prompt)
    for row in range(3):
        vals = input()
        grid[row] = vals.split()


def print_grid(title, grid):
    print(title)
    for row in [0, 1, 2]:
        for col in [0, 1, 2]:
            print(grid[row][col], end=" ")
        print()


def grid_to_str(grid):
    return "".join(grid[0])+"".join(grid[1])+"".join(grid[2])


def welcome_msg():
    
    print('__        _______ _     ____ ___  __  __ _____ _  ')
    print('\ \      / / ____| |   / ___/ _ \|  \/  | ____| | ')
    print(' \ \ /\ / /|  _| | |  | |  | | | | |\/| |  _| | | ')
    print('  \ V  V / | |___| |__| |__| |_| | |  | | |___|_| ')
    print('   \_/\_/  |_____|_____\____\___/|_|  |_|_____(_) ')
    
    print(                    ' _         ')
    print(                    '| |_ ___   ')
    print(                    '| __/ _ \  ')
    print(                    '| || (_) | ')
    print(                     ' \__\___/ ')                                                
                                         
    print(' _____ _        _____            _____           ')                   
    print('|_   _(_) ___  |_   _|_ _  ___  |_   _|__   ___  ')
    print("  | | | |/ __|   | |/ _  |/ __|   | |/ _ \ / _ \ ")
    print('  | | | | (__    | | (_| | (__    | | (_) |  __/ ')
    print('  |_| |_|\___|   |_|\__,_|\___|   |_|\___/ \___| ')
    print('------------------------------------------------------\n')
    print('------------------------------------------------------\n')

    
"""def playing():
    global playing_position, player
    playing_position = input("do you want to play First or Second (1/2)?: ")
    if (playing_position == 1):
        player = "X"
        value = -INF
    else:
        player = "O"
        value = INF"""

def test_move():
    global playing_position, player
    welcome_msg() 
    player_name = input("PLEASE ENTER YOUR NAME: ")
    comp_name = "DEEPMIND AI"
    print(player_name.upper(), "YOU ARE PLAYING AGAINST", comp_name)
    playing_position = int(input("DO YOU WANT TO PLAY First or Second (1/2)?: "))
    print("RELAX AND ENJOY THE GAME!!!")
    game = TicTacToe()
    test_again = "Y"
    grid = copy.deepcopy(EMPTY_GRID)
    if (playing_position == 1):
        player = "O"
        user = "X"
        print("PLAYER: ", player)

    else:
        player = "X"
        user = "O"
        print("PLAYER: ", player)

    curr_player = "X"   
    print("PLAYING POSITION: ", playing_position)
    print("PLAYER: ", player)
    
    print_grid("Current grid:", grid)
    while (not game.terminal_test(grid)):
        if (curr_player == player):
            print("Current player is", comp_name)
            values = minimax_decision(game, grid)
            print(comp_name, "Played", values)
            comp_row = values[0]
            comp_col = values[-1]
            if (grid[comp_row][comp_col] == BLANK):
                grid[comp_row][comp_col] = player
            curr_player = user

        elif (curr_player == user):
       # else:
            print("Current player is", player_name)
            ans = input("Enter the row and col to play: ")
            rowStr, colStr = ans.split()
            row, col = int(rowStr), int(colStr)
            print("You entered ", row, col)
            
            if (grid[row][col] == BLANK):
                grid[row][col] = user
                curr_player = player
            else:
                print("Position already exist!\n Re-Try")
                continue
            
        print_grid("Current grid:", grid)

    winner = game.winner(grid)
    if (winner != None):
        if (winner == user):
            print("Congratulations", player_name.upper(),
                  "WINS", "!")
            game_over()
        else:
            print("Congratulations", comp_name.upper(),
                  "WINS", "!")
            game_over()
    else:
        print("It was a draw.")
        game_over()
    
def game_over():
        print('  ____                         ___                 _  ')
        print(' / ___| __ _ _ __ ___   ___   / _ \__   _____ _ __| | ')
        print('| |  _ / _` |  _ ` _ \ / _ \ | | | \ \ / / _ \  __| | ')
        print('| |_| | (_| | | | | | |  __/ | |_| |\ V /  __/ |  |_| ')
        print(' \____|\__,_|_| |_| |_|\___|  \___/  \_/ \___|_|  (_) ') 
        print('------------------------------------------------------\n')
        print('------------------------------------------------------\n')
        play_again()
        
def play_again():
    play = input("Do you want to play again?(Y/N)")
    if(play.upper() == "Y"):
        test_move()
    else:
        quit()

if __name__ == "__main__":
    test_move()
    
