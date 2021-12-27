# Victorgonl - Knight's Tour Puzzle - 20211218
# Knight's_Tour_Puzzle.py


class Position:
    x = -1
    y = -1
    
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Board:
    NULL_CELL = ''
    CHECK_CELL = '*'
    INITIAL_POSITION = '1'
    x = -1
    y = -1
    matrix = [[]]
    
    def __init__(self, position: Position) -> None:
        self.x = position.x
        self.y = position.y
        self.matrix = [[self.NULL_CELL for _ in range(self.y)] for _ in range(self.x)]
        
    def check(self, position: Position) -> None:
        self.matrix[position.x][position.y] = self.CHECK_CELL


MAX_MOVE = 8
MOVE_X = [2, 1, -1, -2, -2, -1, 1, 2]
MOVE_Y = [1, 2, 2, 1, -1, -2, -2, -1]


def distinct_moves(board, knight):
    total = 0
    for i in range(MAX_MOVE):
        new_x = knight.x + MOVE_X[i]
        new_y = knight.y + MOVE_Y[i]
        new_knight_position = Position(new_x, new_y)
        if valid_position(board, new_knight_position):
            total += 1
    return total


def is_in_bounds(board: Board, position: Position) -> bool:
    if position.x < 0 or position.y < 0:
        return False
    if position.x >= board.x or position.y >= board.y:
        return False
    return True


def is_null_cell(board: Board, position: Position) -> bool:
    return board.matrix[position.x][position.y] == board.NULL_CELL


def valid_position(board: Board, position: Position):
    return is_in_bounds(board, position) and is_null_cell(board, position)


def valid_move(board: Board, knight: Position, position: Position) -> bool:
    if valid_position(board, position):
        for i in range(MAX_MOVE):
            new_x = knight.x + MOVE_X[i]
            new_y = knight.y + MOVE_Y[i]
            new_position = Position(new_x, new_y)
            if new_position == position:
                return True
    return False


def warnsdorff_rule(board: Board, knight: Position, point=1) -> bool:
    if point == 1:
        board.matrix[knight.x][knight.y] = board.INITIAL_POSITION
        point += 1
    for i in range(MAX_MOVE):
        if point == board.x * board.y + 1:
            return True
        new_x = knight.x + MOVE_X[i]
        new_y = knight.y + MOVE_Y[i]
        new_knight_position = Position(new_x, new_y)
        if valid_position(board, new_knight_position):
            board.matrix[new_x][new_y] = str(point)
            if warnsdorff_rule(board, new_knight_position, point + 1):
                return True
            board.matrix[new_x][new_y] = board.NULL_CELL
    return False


def has_solution(board: Board, knight: Position) -> bool:
    position_temp = Position(board.x, board.y)
    board_temp = Board(position_temp)
    board_temp.check(knight)
    return warnsdorff_rule(board_temp, knight)


def is_full(board: Board) -> bool:
    for x in range(board.x):
        for y in range(board.y):
            if board.matrix[x][y] == board.NULL_CELL:
                return False
    return True


def can_continue(board: Board, knight: Position) -> bool:
    if is_full(board):
        return False
    else:
        for i in range(MAX_MOVE):
            new_x = knight.x + MOVE_X[i]
            new_y = knight.y + MOVE_Y[i]
            new_position = Position(new_x, new_y)
            if valid_move(board, knight, new_position):
                return True
    return False


def cell_visited(board) -> int:
    total = 0
    for x in range(board.x):
        for y in range(board.y):
            if board.matrix[x][y] == board.CHECK_CELL:
                total += 1
    return total


def draw_board(board: Board, knight: Position):
    draw = ""

    def cell_size():
        return len(str(board.x * board.y))

    def border_size():
        return board.y * (cell_size() + 1) + 3

    def border():
        nonlocal draw
        for _ in range(len(str(board.x))):
            draw += ' '
        for _ in range(border_size()):
            draw += '-'
        draw += '\n'

    def columns_number():
        nonlocal draw
        for _ in range(len(str(board.x)) + 2):
            draw += ' '
        for i in range(board.y):
            for _ in range(cell_size() - len(str(i))):
                draw += ' '
            draw += str(i + 1) + ' '

    border()

    for x in range(board.x - 1, -1, -1):
        if len(str(x + 1)) != len(str(board.x)):
            for _ in range(len(str(board.x)) - 1):
                draw += ' '
        draw += str(x + 1) + '|' + ' '
        for y in range(board.y):
            temp = ''
            position = Position(x, y)
            if board.matrix[x][y] != board.NULL_CELL:
                temp = board.matrix[x][y]
                if temp != board.INITIAL_POSITION and position == knight:
                    temp = 'X'
            elif valid_move(board, knight, position):
                temp = str(distinct_moves(board, position))
            else:
                for _ in range(cell_size()):
                    temp += '_'
            if len(str(temp)) != cell_size():
                for _ in range(cell_size() - len(str(temp))):
                    draw += ' '
            draw += str(temp) + ' '
        draw += '|' + '\n'

    border()
    columns_number()

    print(draw)


def read_position(board: Board) -> Position:
    try:
        position = [x for x in input("Enter the knight's starting position: ").split(maxsplit=1)]
        if (not position[0].isnumeric()) or (not position[1].isnumeric()):
            raise
        position = [int(x) for x in position]
        position[0], position[1] = position[1] - 1, position[0] - 1
        position = Position(position[0], position[1])
        if not is_in_bounds(board, position):
            raise
        return position
    except Exception as _:
        raise Exception("Invalid dimensions!")


def read_board() -> Board:
    try:
        size = [x for x in input("Enter your board dimensions: ").split(maxsplit=1)]
        if (not size[0].isnumeric()) or (not size[1].isnumeric()):
            raise
        size = [int(x) for x in size]
        if size[0] <= 0 or size[1] <= 0:
            raise
        size[0], size[1] = size[1], size[0]
        size = Position(size[0], size[1])
        board = Board(size)
        return board
    except Exception as _:
        raise Exception("Invalid dimensions!")


def read_move(board: Board, knight: Position) -> Position:
    try:
        position = [x for x in input("Enter your next move: ").split(maxsplit=1)]
        if (not position[0].isnumeric()) or (not position[1].isnumeric()):
            raise
        position = [int(x) for x in position]
        position[0], position[1] = position[1] - 1, position[0] - 1
        position = Position(position[0], position[1])
        if not valid_move(board, knight, position):
            raise
        return position
    except Exception as _:
        raise Exception("Invalid move!")


def main() -> None:
    while True:
        try:
            board = read_board()
            break
        except Exception as error:
            print(error)
    while True:
        try:
            knight = read_position(board)
            board.check(knight)
            break
        except Exception as error:
            print(error)
    while True:
        try:
            choice = ''
            while choice != 'n' and choice != 'y':
                choice = input("Do you want to try the puzzle? (y/n): ")
                if choice != 'n' and choice != 'y':
                    print("Invalid input!")
            if (choice == 'n' or choice == 'y') and has_solution(board, knight):
                if choice == 'n':
                    warnsdorff_rule(board, knight)
                    print()
                    print("Here's the solution!")
                    draw_board(board, knight)
                elif choice == 'y':
                    draw_board(board, knight)
                    print()
                    while can_continue(board, knight):
                        try:
                            knight = read_move(board, knight)
                            board.check(knight)
                            draw_board(board, knight)
                            print()
                        except Exception as error:
                            print(error, end=' ')
                    if is_full(board):
                        print("What a great tour! Congratulations!")
                    else:
                        print("No more possible moves!")
                        print("Your knight visited", cell_visited(board), "squares!")
            else:
                print("No solution exists!")
            return
        except Exception as error:
            print(error)


main()
