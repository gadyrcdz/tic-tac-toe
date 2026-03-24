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
    countRow = -1
    countCol = -1
    for i in board:
        countRow+=1
        for player in i:
            if(countCol == 2):
                countCol = -1
            countCol += 1
            move =countRow, countCol
            print(move)
            if(is_free_to_mark(board,move)):
                movement += [move]
            
    return movement


def result(board, action):
    """
    Returns the state after taking action a in state s
    """
    player = players(board)

    x,y = action
    copyBoard = copy.deepcopy(board)

   
    copyBoard[y][x] = player

    print(copyBoard)
    return copyBoard



def terminal(board):
    """
    Checks whether state s is a terminal state
    """
    x = 0
    y = 0
    flagR = True
    flagC = False
    counter = 0
    while(counter < 9):
        if(y > 2):
            flagR = False
            flagC = True
            y = 0
        if(x > 2):
            x = 0
        pos = x,y
        if(y == 0 and x == 0):
            if(valRight(board,pos)):
                print("gana derecha")
                print(board[x][y])
                return True
            elif(valdiagonally(board,pos)):
                print("gana diagonal")
                return True
            elif(valDown(board,pos)):
                print("gana abajo")
                return True
        elif(x == 0):
            if(valDown(board,pos)):
                print("gana abajo")
                return True
        elif(y > 0):
            if(valDown(board,pos)):
                print("gana abajo")
                return True

        elif(x == 1):
            if(valRight(board,pos)):
                print("gana derecha")
                return True

        elif(x == 2):
            if(valdiagonallyDown(board,pos)):
                print("gana diagonalInversa")
                return True
        counter+=1
        if(flagR):
            y+=1
        if(flagC):
            x+=1

    if(len(actions(board))>0):
        return False
    return True    




    
def valRight(board, pos):
    x , y = pos
    player = board[x][y]
    if(player == None):
        return False
    count = 0
    countX = 0
    countO = 0
    while(count < 2):
        if(player == PLAYER_X):
            y+=1
            if(board[x][y] == PLAYER_X):
                countX+=1
            else:
                return False
        elif(player == PLAYER_O):
            y+=1
            if(board[x][y] == PLAYER_O):
                countO+=1
            else:
                return False
        count+=1
    return True

def valDown(board, pos):
    x , y = pos
    player = board[x][y]
    if(player == None):
        return False
    count = 0
    countX = 0
    countO = 0
    while(count < 2):
        if(player == PLAYER_X):
            x+=1
            if(board[x][y] == PLAYER_X):
                countX+=1
            else:
                return False
        elif(player == PLAYER_O):
            x+=1
            if(board[x][y] == PLAYER_O):
                countO+=1
            else:
                return False
        count+=1
    return True

def valdiagonally(board, pos):
    x , y = pos
    player = board[x][y]
    if(player == None):
        return False
    count = 0
    countX = 0
    countO = 0
    while(count < 2):
        if(player == PLAYER_X):
            x+=1
            y+=1
            if(board[x][y] == PLAYER_X):
                countX+=1
            else:
                return False
        elif(player == PLAYER_O):
            x+=1
            y+=1
            if(board[x][y] == PLAYER_O):
                countO+=1
            else:
                return False
        count+=1
    return True


def valdiagonallyDown(board, pos):
    x , y = pos
    player = board[x][y]
    if(player == None):
        return False
    count = 0
    countX = 0
    countO = 0
    while(count < 2):
        if(player == PLAYER_X):
            x-=1
            y+=1
            if(board[x][y] == PLAYER_X):
                countX+=1
            else:
                return False
        elif(player == PLAYER_O):
            x-=1
            y+=1
            if(board[x][y] == PLAYER_O):
                countO+=1
            else:
                return False
        count+=1

    return True


def utility(board):
    """
    Final numeric value for terminal state s
    """
    x = 0
    y = 0
    flagR = True
    flagC = False
    counter = 0
    while(counter < 9):
        if(y > 2):
            flagR = False
            flagC = True
            y = 0
        if(x > 2):
            x = 0
        pos = x,y
        if(y == 0 and x == 0):
            if(valRight(board,pos)):
                print("gana derecha")
                if(board[x][y] == PLAYER_X):
                    print("1")
                    return 1
                elif(board[x][y] == PLAYER_O):
                    print("-1")
                    return -1
            elif(valdiagonally(board,pos)):
                if(board[x][y] == PLAYER_X):
                    print("1")
                    return 1
                elif(board[x][y] == PLAYER_O):
                    print("-1")
                    return -1
            elif(valDown(board,pos)):
                print("gana abajo")
                if(board[x][y] == PLAYER_X):
                    print("1")
                    return 1
                elif(board[x][y] == PLAYER_O):
                    print("-1")
                    return -1
        elif(x == 0):
            if(valDown(board,pos)):
                print("gana abajo")
                if(board[x][y] == PLAYER_X):
                    print("1")
                    return 1
                elif(board[x][y] == PLAYER_O):
                    print("-1")
                    return -1
        elif(y > 0):
            if(valDown(board,pos)):
                print("gana abajo")
                if(board[x][y] == PLAYER_X):
                    print("1")
                    return 1
                elif(board[x][y] == PLAYER_O):
                    print("-1")
                    return -1

        elif(x == 1):
            if(valRight(board,pos)):
                print("gana derecha")
                if(board[x][y] == PLAYER_X):
                    print("1")
                    return 1
                elif(board[x][y] == PLAYER_O):
                    print("-1")
                    return -1

        elif(x == 2):
            if(valdiagonallyDown(board,pos)):
                print("gana diagonalInversa")
                if(board[x][y] == PLAYER_X):
                    print("1")
                    return 1
                elif(board[x][y] == PLAYER_O):
                    print("-1")
                    return -1
        counter+=1
        if(flagR):
            y+=1
        if(flagC):
            x+=1

    print("0")
    return 0 
    



    



# is_free_to_mark([["X", "O", "X"],[None,None,None],[None,None,None]],(0,1))
# valdiagonallyDown([["X", "O", "X"],["O", "X", "O"],["X", "X", "O"]],(2,0))
# result([["X", "O", "X"],[None,"O",None],[None,None,None]],(2,2))
# terminal([["X", "O", "X"],["X", "X", "X"],["O", "O", "O"]])

utility(board = [
        ["X", "O", "X"],
        ["X", "O", "O"],
        ["O", "X", "X"],
    ])

