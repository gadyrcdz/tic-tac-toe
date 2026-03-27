import copy


PLAYER_X = "X"
PLAYER_O = "O"




def is_free_to_mark(board, movement):
    x,y = movement
    # res =board[x][y]

    return not board[x][y]
    # if(res != None):
    #     return board[x][y]
    # return False


def players(board):
    """
    Returns the player who must move in state s
    """
    x = 0
    o = 0
    for i in board:
        for player in i:
            if(player == PLAYER_X):
                x+=1
            elif(player == PLAYER_O):
                o += 1
    
    if(x == o):
        return PLAYER_X
    elif(x > o):
        return PLAYER_O





def actions(board):
    """
    Returns the legal moves in state s
    """
    movement = []
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                movement.append((i, j))
    return movement


def result(board, action):
    """
    Returns the state after taking action a in state s
    """
    player = players(board)

    x,y = action
    copyBoard = copy.deepcopy(board)

    copyBoard[x][y] = player

    return copyBoard



def terminal(board):
    """
    Checks whether state s is a terminal state
    """
    for i in range(3):
        if board[i][0] and board[i][0] == board[i][1] == board[i][2]:
            return True
        if board[0][i] and board[0][i] == board[1][i] == board[2][i]:
            return True
    if board[0][0] and board[0][0] == board[1][1] == board[2][2]:
        return True
    if board[0][2] and board[0][2] == board[1][1] == board[2][0]:
        return True
    return len(actions(board)) == 0





def utility(board):
    """
    Final numeric value for terminal state s
    """
    for i in range(3):
        if board[i][0] and board[i][0] == board[i][1] == board[i][2]:
            return 1 if board[i][0] == PLAYER_X else -1
        if board[0][i] and board[0][i] == board[1][i] == board[2][i]:
            return 1 if board[0][i] == PLAYER_X else -1
    if board[0][0] and board[0][0] == board[1][1] == board[2][2]:
        return 1 if board[0][0] == PLAYER_X else -1
    if board[0][2] and board[0][2] == board[1][1] == board[2][0]:
        return 1 if board[0][2] == PLAYER_X else -1
    return 0



    



# is_free_to_mark([["X", "O", "X"],[None,None,None],[None,None,None]],(0,1))
# result([["X", "O", "X"],[None,"O",None],[None,None,None]],(2,2))
# terminal([["X", "O", "X"],["X", "X", "X"],["O", "O", "O"]])

utility(board = [
        ["X", "O", "X"],
        ["X", "O", "O"],
        ["O", "X", "X"],
    ])

