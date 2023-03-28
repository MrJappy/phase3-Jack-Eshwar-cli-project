import random
import re
class Board:
    BEGINNER_PARAMS = {
        'dim_size': 8,
        'num_bombs': 10
    }

    INTERMEDIATE_PARAMS = {
        'dim_size': 16,
        'num_bombs': 40
    }

    EXPERT_PARAMS = {
        'dim_size': 24,
        'num_bombs': 99
    }
    def __init__(self, dim_size, num_bombs):
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        self.board = self.make_new_board()
        self.assign_values_to_board()
        
        self.dug = set()

    def make_new_board(self):


        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]

        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc  = random.randint(0 ,self.dim_size**2 - 1)
            row  = loc  // self.dim_size
            col = loc % self.dim_size

            if board[row][col] == '*':
                continue

            board[row][col] = '*'
            bombs_planted += 1
        return board

    def assign_values_to_board(self):
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    continue
                self.board[r][c] = self.get_num_neighboring_bombs(r,c)
    
    def get_num_neighboring_bombs(self, row, col):


        num_neighboring_bombs = 0
        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):
                if r == row and c == col:
                    continue
                if self.board[r][c] == '*':
                    num_neighboring_bombs += 1
                
        return num_neighboring_bombs
    

    def dig(self, row, col):
        self.dug.add((row, col))

        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True
        
        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):
                if (r, c) in self.dug:   
                    continue
                self.dig(r,c)
        return True
        
    def __str__(self):
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row,col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '
        
        string_rep = ''
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )

        indices = [i for i in range(self.dim_size)]
        indices_row = '' * (widths[0]+1)  # add some spaces before the first column
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)  # add double spaces between columns
        indices_row += ' \n'  # add a space and a new line character at the end
        
        string_rep += indices_row

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i:2} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'
        
        string_rep += '-'*(sum(widths)+len(widths)+1) + '\n'
        str_len = int(len(string_rep) / self.dim_size)

        return string_rep
            

def play(dim_size=8, num_bombs=10):
    print('Welcome to MinseSweeper!!!!!!!')
    difficulty = input("Select a difficulty level (beginner, intermediate, expert): ")
    if difficulty == 'beginner':
        params = Board.BEGINNER_PARAMS
    elif difficulty == 'intermediate':
        params = Board.INTERMEDIATE_PARAMS
    elif difficulty == 'expert':
        params = Board.EXPERT_PARAMS
    else:
        print('Invalid difficulty')
        return
    
    
    board = Board(dim_size=params['dim_size'], num_bombs=params['num_bombs'])

    safe = True

    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        print(board)
        user_input = re.split(',(\\s)*', input("Where would you like to dig? Input as row,col: "))
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= board.dim_size or col < 0 or col >= board.dim_size:
            print('Invalid Location. Try again.')
            continue
        safe = board.dig(row, col)
        if not safe:
            break

    if safe:
        print('ARE YOU NOT ENTERTAINED')
    else:
        print('GAME OVER!!!!! XD')

        board.dug = [(r,c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)

if __name__ == '__main__':
    play()