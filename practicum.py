__author__ = 'r0583570'
# Skeleton file for BVP Practicum
#
# You need to implement all functions in this file.
#
# If you implement them correctly, you can run this file to
# play the 2048 game.  For that to work, this file has to be
# in the same directory as the `game.py` file we provided.


# This imports our GUI code and allows you to play the game based on the
# functions you define in this file.
import game
import math
from random import randint
def initialize( dimension = 4, nb_of_pieces = 2, difficulty = 2 ):
    """
    Initialization function.  Should produce a valid board state of size `dimension` x `dimension`.
    This function should initialize the datastructure needed to represent the board state.  Initially,
    the board should be empty with only `nb_of_pieces` elements on there.  The initial elements shouldn't
    be larger than `math.pow( 2, difficulty )`.
    :param dimension: width and height of the board
    :type dimension: int
    :param nb_of_pieces: number of initial elements on the board
    :type nb_of_pieces: int
    :param difficulty: max log2 of initial elements.
    :type difficulty: int
    :return: valid board state with initial elements
    :rtype list[ list[ int | None ] ]
    """
    matrix=[]
    for i in range(0, dimension):
        row = [None] * dimension
        matrix.append(row)
    used=[]
    for i in range (nb_of_pieces):
        pos1=randint(0,dimension-1)
        pos2=randint(0,dimension-1)
        position=[pos1,pos2]
        while position in used:
            pos1=randint(0,dimension-1)
            pos2=randint(0,dimension-1)
            position=[pos1,pos2]
        matrix[pos1][pos2]=int(math.pow(2,randint(1,difficulty)))
        used.append(position)
    print(matrix)

    return matrix


def match(row):
    """
    Matches all identical elements in the row.
    This function searches for possible matches in a row ( a match is when
    two identical elements are next to each other or only separated from
    each other by `None`'s.).  When a match is found, the match is made and
    the result is placed on the position of the *left* most element in the match.
    The function also calculates the score for matching in this row.  The score for
    matching the elements in the row is the sum of all matched elements.  If,
    for example, the row has two 4 elements next to each other, the score will be
    8.  If the row has two 2 elements and two 4 elements next to each other
    (`[ 2, 2, 4, 4 ]`), the score will be 12.
    Examples:
        >>> match( [ 2, 2, None ] )
        ( [ 4, None, None ], 4 )
        >>> match( [ 2, 2, 2, ] )
        ( [ 4, None, 2 ], 4 )
        >>> match( [ 2, 2, 2, 2 ] )
        ( [ 4, None, 4, None ], 8 )
        >>> match( [ 2, None, 2 ] )
        ( [ 4, None, None ], 4 )
        >>> match( [ 2, 4, None, 4 ] )
        ( [ 2, 8, None, None ], 8 )
        >>> match( [ 2, 2, 4 ] )
        ( [ 4, None, 4  ], 4 )
        >>> match( [ 4, 2, 2 ] )
        ( [ 4, 4, None ], 4 )
        >>> match( [ 2, 2, 4, 4 ] )
        ( [ 4, None, 8, None ], 12 )
        >>> match( [ 2, 2, None, 2, 2 ] )
        ( [ 4, None, None, 4, None ], 8 )
        >>> match( [ 4, 2, 4, None ] )
        ( [ 4, 2, 4, None ], 0 )
    :type row: list[ int | None ]
    :param row: row to match
    :return: tuple with matched row and score
    :rtype: ( list[ int | None ], int )
    """
    score = 0

    for i in range (0,len(row)-1):
        j=i
        if row[i]!=None:
            while row[j+1]== None:
                if j+1<len(row)-1:
                    j+=1
                break
            if j+1<len(row):
                j+=1
            if row [i] == row [j]:
                row[i]= 2*row[i]
                row [j] = None
                score += row[i]

    return ( row, score )


def reduce(row):
    """
    Removes the empty spaces in a row.
    This function moves all elements in the row to the front of
    the row.  Elements are not changed, the are not summed.  The
    dimension of the row should not change.
    Examples:
        >>> reduce( [ 2, None, 2, None ] )
        [ 2, 2, None, None ]
        >>> reduce( [ 4, 2, None, None ] )
        [ 4, 2, None, None ]
        >>> reduce( [ None, None, 2 ] )
        [ 2, None, None ]
    :rtype: list[int | None]
    :param row: the row to remove empty spaces from
    :return: row with all not None elements in the front
    """
    for j in range(len(row)):
        for i in range (0,len(row)-1):
            if row [i] == None:
                row [i] = row [i+1]
                row [i+1] = None
    return row


def transpose( matrix ):
    """
    Calculates the transpose of a matrix.
    Examples:
        >>> transpose( [ [ 2, None ], [ 2, None ] ] )
        [ [ 2, 2 ], [ None, None ] ]
    :param matrix: matrix to calculate transpose of
    :return: the transpose of matrix
    :rtype: list[list[int | None]]
    """
    transpose =[]
    for kolom in range(len(matrix)):
        transpose_row = []
        for rij in range(len(matrix)):
            transpose_row.append(matrix[rij][kolom])
        transpose.append(transpose_row)

    return transpose


def mirror( matrix ):
    """
    Mirrors all rows in the matrix.
    Examples:
        >>> mirror( [ [ 1, 2, 3 ], [ 1, 2, 3 ], [ 1, 2, 3 ] ] )
        [ [ 3, 2, 1 ], [ 3, 2, 1 ], [ 3, 2, 1 ] ]
        >>> mirror( [ [ 1, 2 ], [ 3, 4 ] ] )
        [ [ 2, 1 ], [ 4, 3 ] ]
    :param matrix: matrix to mirror
    :return: matrix with all rows reversed
    :rtype: list[ list[ int | None ] ]
    """
    mirror =[]
    for kolom in range(len(matrix)):
        mirror_row= []
        for rij in range(len(matrix)):
            mirror_row.append(matrix[kolom][(len(matrix)-rij)-1])
        mirror.append(mirror_row)
    return mirror


def has_empty_slot( matrix ):
    """
    Checks for empty slots (`None`) elements in the matrix.
    Examples:
        >>> has_empty_slot( [ [ 1 ] ] )
        False
        >>> has_empty_slot( [ [ None ] ] )
        True
        >>> has_empty_slot( [ [ 2, 2 ], [ 4, 4 ] ] )
        False
        >>> has_empty_slot( [ [ 2, None ], [ 4, 4 ] ] )
        True
        >>> has_empty_slot( [ [ 2, None ], [ 4, None ] ] )
        True
    :param matrix: matrix to check
    :rtype matrix: list[ list[ int | None ] ]
    :return: whether there is an empty slot
    :rtype boolean
    """
    for rij in range(len(matrix)):
        for kolom in range(len(matrix)):
            if matrix[rij][kolom] == None:
                return True
    return False


def has_matches( matrix ):
    """
    Checks if there are potential matches in the matrix.
    There is a potential match in the matrix if in any of the rows
    or columns contain two identical elements next to each other or
    only separated by `None`'s.
    Examples:
        >>> has_matches( [ [ 2, None ], [ None, 2 ] ] )
        False
        >>> has_matches( [ [ 2, 2 ], [ None, None ] ] )
        True
        >>> has_matches( [ [ 2, None ], [ 2, None ] ] )
        True
        >>> has_matches( [ [ 2, 4 ], [ 4, 2 ] ] )
        False
        >>> has_matches( [ [ 2, None, 2 ], [ None, None, None ], [ None, None, None ] ] )
        True
        >>> has_matches( [ [ 2, 4, 2 ], [ None, None, None ], [ None, None, None ] ] )
        False
        >>> has_matches( [ [ 2, None, None ], [ None, None, None ], [ 2, None, None ] ] )
        True
        >>> has_matches( [ [ None, None, 2 ], [ None, None, 2 ], [ None, None, None ] ] )
        True
        >>> has_matches( [ [ 2, None, None ], [ None, None, None ], [ None, None, 2 ] ] )
        False
        >>> has_matches( [ [ 2, None, None ], [ None, 2, None ], [ None, None, 2 ] ] )
        False
    :param matrix: matrix to check for matches
    :rtype matrix: list[ list[ int | None ] ]
    :return: whether there are any matches
    :rtype: boolean
    """
    if check_for_possibilities(matrix)==True:
        return True
    if check_for_possibilities(transpose(matrix))==True:
        return True
    if check_for_possibilities(transpose(mirror(matrix)))== True:
        return True
    return False

def check_for_possibilities(matrix):
    for rij in range (len(matrix)-1):
        for kolom in range(len(matrix)-1):
            if matrix [rij][kolom] != None:
                hulpwaarde = kolom
                while matrix [rij][hulpwaarde+1]==None:
                    if hulpwaarde+1<(len(matrix)-1):
                        hulpwaarde+=1
                    break
                if hulpwaarde+1<(len(matrix)):
                    hulpwaarde+=1
                if matrix[rij][kolom]==matrix[rij][hulpwaarde]:
                    return True
    return False
def insert_new( matrix, number, difficulty = 2):
    """
    Inserts `number` new elements in the matrix.  The maximum log2 of the newly
    introduced elements should be difficulty.
    This method should introduce new elements in the matrix.  The number of
    elements to introduce is given by `number`.  The location of the new elements
    should be chosen at random.
    To make the game more difficult, the elements introduced could also be greater
    than 2.  This is achieved through the `difficulty` argument.  Given a `difficulty` of
    `n`, this function should only introduce elements smaller or equal to math.pow( 2, n ).
    The power of 2 for the new elements can be chosen randomly from the range 1 to n,
    including both 1 and n.
    If `number` is greater than the number of empty slots in the board.  The function
    should simply fill the board, not overriding any of the existing elements.
    Examples:
        >>> insert_new( [ [ 8, 8 ], [ 8, 8 ] ], 1, 1 )
        [ [ 8, 8 ], [ 8, 8 ] ]
        >>> insert_new( [ [ 8, 8 ], [ 8, None ] ], 1, 1 )
        [ [ 8, 8 ], [ 8, 2 ] ]
        >>> insert_new( [ [ None, None ], [ None, None ] ], 4, 3 )
        [ [ 2, 4 ], [ 2, 8 ] ]
        >>> insert_new( [ [ None, None ], [ None, None ] ], 2, 2 )
        [ [ 2, None ], [ 4, None ] ]
        >>> insert_new( [ [ None, None ], [ None, None ] ], 2, 1 )
        [ [ None, 2 ], [ None, None ] ]
    :param matrix: matrix to insert new elements into
    :type matrix: list[ list[ int | None ] ]
    :param number: number of elements to introduce
    :type number: int
    :param difficulty: maximum log2 of the new elements
    :type difficulty: int
    :return: matrix with new elements
    :rtype: list[list[int | None]]
    """
    for i in range(number):
        if has_empty_slot(matrix)==False:
            return matrix
        rij = randint(0,len(matrix)-1)
        kolom = randint(0,len(matrix)-1)
        while matrix [rij] [kolom] != None:
                rij = randint(0,len(matrix)-1)
                kolom = randint(0,len(matrix)-1)
        matrix[rij][kolom]=pow(2,randint(1,difficulty))
    return matrix


def should_continue( matrix ):
    """
    Calculates whether the game should continue
    The game should continue as long as there are empty slots
    in the game or there are matches possible.
    :param matrix: current board state
    :return: whether there are empty slots or matches left in the board
    """
    if has_empty_slot(matrix)==True:
        return True
    if has_matches(matrix)==True:
        return True
    return False


def handle_key_press(board, score, direction):
    """
    Function called whenever there was a keypress.
    Should return a tuple with the new state of the
    board, the score and whether the game should continue.
    This function should calculate the new state of the board after
    all elements have been moved in the direction indicated by `direction`.
    All elements should be matched and then moved in the direction of the
    keypress.  If the state of the board has changed, new elements can
    be introduced in the board.
    We consider board to be a matrix where board[i][j] is the element in the i-th column
    of the board and j-th row of the board.
    Given the current score that is passed as an argument, the function should also
    update that value and return it as the second item in the tuple.
    Examples:
        >>> handle_key_press( [ [ 2, 2 ], [ None, 4 ] ], 0, "Up" )
        ( [ [ 4, None ], [ 4, None ] ], 4 )
        >>> handle_key_press( [ [ 4, None ], [ 4, None ] ], 4, "Left" )
        ( [ [ 8, None ], [ None, 2 ] ], 12 )
        >>> handle_key_press( [ [ 8, None ], [ None, 2 ] ], 12, "Right" )
        ( [ [ None, None ], [ 8, 2 ] ], 12 )
        >>> handle_key_press( [ [ None, None ], [ 8, 2 ] ], 12, "Down" )
        ( [ [ 2, None ], [ 8, 2 ] ], 12 )
    :param board: board state as returned by handle_key_press or initialize function
    :param score: players current score
    :param direction: symbol that was pressed ( one of "Up", "Down", "Left", "Right" )
    :return: new valid board state and the players new score
    """
    matrix=[]
    if direction =="Left":
        for rij in range(len(board)):
            result=match((transpose(board))[rij])
            score+=result[1]
            matrix.append(reduce(result[0]))
        matrix=transpose(matrix)
        print(matrix)
    if direction =="Right":
        for rij in range(len(board)):
            result=match((mirror(transpose(board)))[rij])
            score+=result[1]
            matrix.append(reduce(result[0]))
        matrix=transpose(mirror(matrix))
        print(matrix)
    if direction =="Up":
        for rij in range(len(board)):
            result = match(board[rij])
            score+=result[1]
            matrix.append(reduce(result[0]))
        print(matrix)
    if direction =="Down":
        for rij in range(len(board)):
            result = match((mirror(board))[rij])
            score+=result[1]
            matrix.append(reduce(result[0]))
        matrix=mirror(matrix)
        print(matrix)
    return ( matrix, score ) # Complete me


# This next bit of code initializes our GUI code with your functions
# `initialize`, `handle_key_press` and `should_continue` and starts
# the game.  The if test checks whether this file is being executed
# or just imported (e.g. for testing)
if __name__ == "__main__":
    game = game.Game(initialize, handle_key_press, should_continue)
    game.play()