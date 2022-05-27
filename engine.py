class GameState:
    def __init__(self):
        self.board = [
            ["rb", "nb", "bb", "qb", "kb", "bb", "nb", "rb"],
            ["pb", "pb", "pb", "pb", "pb", "pb", "pb", "pb"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["pw", "pw", "pw", "pw", "pw", "pw", "pw", "pw"],
            ["rw", "nw", "bw", "qw", "kw", "bw", "nw", "rw"]
        ]
        self.checkmate_status = False
        self.stalemate_status = False
        self.move_log = []
        self.white_move = True
        self.black_loc = ()
        self.white_loc = ()
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == "kb":
                    self.black_loc = (i, j)
                if self.board[i][j] == "kw":
                    self.white_loc = (i, j)

    def move(self, move_obj):
        self.board[move_obj.end_row][move_obj.end_col] = move_obj.moved
        self.board[move_obj.start_row][move_obj.start_col] = "--"
        self.white_move = not self.white_move
        self.move_log.append(move_obj)

    def undo(self):
        if len(self.move_log) > 0:
            last_move = self.move_log.pop()
            self.board[last_move.start_row][last_move.start_col] = last_move.moved
            self.board[last_move.end_row][last_move.end_col] = last_move.captured
            self.white_move = not self.white_move

    def valid_moves(self):
        all_moves =  self.all_moves()
        for i in range(len(all_moves)-1, -1, -1):
            self.move(all_moves[i])
            self.white_move = not self.white_move
            if self.check():
                all_moves.remove(all_moves[i])
            self.white_move = not self.white_move
            self.undo()
        return all_moves
    def check(self):
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == "kb":
                    self.black_loc = (i, j)
                if self.board[i][j] == "kw":
                    self.white_loc = (i, j)
        if self.white_move:
            king = self.white_loc
        else:
            king = self.black_loc
        self.white_move = not self.white_move
        opp_moves = self.all_moves()
        self.white_move = not self.white_move
        for i in opp_moves:
            if (i.end_row, i.end_col) == king:
                return True

    def all_moves(self):
        possible_moves = []
        if self.white_move:
            color = "w"
        else:
            color = "b"
        for i in range(8):
            for j in range(8):
                if self.board[i][j][0] == "p" and self.board[i][j][1] == color:
                    possible_moves.extend(self.pawn_moves(i, j))
                elif self.board[i][j][0] == "b" and self.board[i][j][1] == color:
                    possible_moves.extend(self.bishop_moves(i, j))
                elif self.board[i][j][0] == "r" and self.board[i][j][1] == color:
                    possible_moves.extend(self.rook_moves(i, j))
                elif self.board[i][j][0] == "n" and self.board[i][j][1] == color:
                    possible_moves.extend(self.knight_moves(i, j))
                elif self.board[i][j][0] == "q" and self.board[i][j][1] == color:
                    possible_moves.extend(self.queen_moves(i, j))
                elif self.board[i][j][0] == "n" and self.board[i][j][1] == color:
                    possible_moves.extend(self.knight_moves(i, j))
                elif self.board[i][j][0] == "k" and self.board[i][j][1] == color:
                    possible_moves.extend(self.king_moves(i, j))
        return possible_moves

    def checkmate(self):
        if len(self.valid_moves()) == 0:
            self.checkmate_status = True
            return True
    def stalemate(self):
        if len(self.valid_moves()) == 0:
            self.white_move = not self.white_move
            if len(self.valid_moves()) == 0:
                self.stalemate_status = True
                self.white_move = not self.white_move
                return True
            self.white_move = not self.white_move

    def king_moves(self, row, col):
        dirs = [(-1, 0), (1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1), (0, -1), (0, 1)]
        moves = []
        color = self.board[row][col][1]
        for direction in dirs:
            current_row = row
            current_col = col
            current_row += direction[0]
            current_col += direction[1]
            if 0 <= current_col <= 7 and 0 <= current_row <= 7:
                if color == "w" and self.board[current_row][current_col][1] == "w":
                    pass
                elif color == "w" and self.board[current_row][current_col][1] == "b":
                    moves.append(Move(self.board, (row, col), (current_row, current_col)))
                elif color == "b" and self.board[current_row][current_col][1] == "b":
                    pass
                elif color == "b" and self.board[current_row][current_col][1] == "w":
                    moves.append(Move(self.board, (row, col), (current_row, current_col)))
                    pass
                else:
                    moves.append(Move(self.board, (row, col), (current_row, current_col)))
        return moves

    def queen_moves(self, row, col):
        moves = []
        moves.extend(self.rook_moves(row, col))
        moves.extend(self.bishop_moves(row, col))
        return moves

    def knight_moves(self, row, col):
        dirs = [(-1, 2), (-1, -2), (1, 2), (1, -2), (2, -1), (-2, -1), (2, 1), (-2, 1)]
        moves = []
        color = self.board[row][col][1]
        for direction in dirs:
            current_row = row
            current_col = col
            current_row += direction[0]
            current_col += direction[1]
            if 0 <= current_col <= 7 and 0 <= current_row <= 7:
                if color == "w" and self.board[current_row][current_col][1] == "w":
                            pass
                elif color == "w" and self.board[current_row][current_col][1] == "b":
                            moves.append(Move(self.board, (row, col), (current_row, current_col)))
                elif color == "b" and self.board[current_row][current_col][1] == "b":
                            pass
                elif color == "b" and self.board[current_row][current_col][1] == "w":
                            moves.append(Move(self.board, (row, col), (current_row, current_col)))
                            pass
                else:
                            moves.append(Move(self.board, (row, col), (current_row, current_col)))
        return moves

    def rook_moves(self, row, col):
        moves = []
        dirs = [(1, 0), (-1, 0), (0, -1), (0, 1)]
        color = self.board[row][col][1]
        for direction in dirs:
            current_row = row
            current_col = col
            while True:
                current_row += direction[0]
                current_col += direction[1]
                if 0 <= current_col <= 7 and 0 <= current_row <= 7:
                    if color == "w" and self.board[current_row][current_col][1] == "w":
                        break
                    elif color == "w" and self.board[current_row][current_col][1] == "b":
                        moves.append(Move(self.board, (row, col), (current_row, current_col)))
                        break
                    elif color == "b" and self.board[current_row][current_col][1] == "b":
                        break
                    elif color == "b" and self.board[current_row][current_col][1] == "w":
                        moves.append(Move(self.board, (row, col), (current_row, current_col)))
                        break
                    else:
                        moves.append(Move(self.board, (row, col), (current_row, current_col)))
                else:
                    break
        return moves

    def bishop_moves(self, row, col):
        moves = []
        dirs = [(1,1), (-1,-1), (1,-1), (-1,1)]
        color = self.board[row][col][1]
        for direction in dirs:
            current_row = row
            current_col = col
            while True:
                current_row += direction[0]
                current_col += direction[1]
                if 0 <= current_col <= 7 and 0 <= current_row <= 7:
                        if color == "w" and self.board[current_row][current_col][1] == "w":
                            break
                        elif color == "w" and self.board[current_row][current_col][1] == "b":
                            moves.append(Move(self.board, (row, col), (current_row, current_col)))
                            break
                        elif color == "b" and self.board[current_row][current_col][1] == "b":
                            break
                        elif color == "b" and self.board[current_row][current_col][1] == "w":
                            moves.append(Move(self.board, (row, col), (current_row, current_col)))
                            break
                        else:
                            moves.append(Move(self.board, (row, col), (current_row, current_col)))
                else:
                    break
        return moves

    def pawn_moves(self, row, col):
        moves = []
        color = self.board[row][col][1]
        if color == "w" and self.board[row-1][col] == "--":
            moves.append(Move(self.board, (row, col), (row-1, col)))
            if row == 6 and self.board[row-2][col] == "--":
                moves.append(Move(self.board, (row, col), (row - 2, col)))
        if color == "b" and self.board[row+1][col] == "--":
            moves.append(Move(self.board, (row, col), (row+1, col)))
            if row == 1 and self.board[row+2][col] == "--":
                moves.append(Move(self.board, (row, col), (row + 2, col)))
        if col < 7:
            if color == "w" and self.board[row-1][col+1][1] == "b":
                moves.append(Move(self.board, (row, col), (row - 1, col+1)))
        if col > 0:
            if color == "w" and self.board[row-1][col-1][1] == "b":
                moves.append(Move(self.board, (row, col), (row - 1, col-1)))

        if col < 7:
            if color == "b" and self.board[row+1][col+1][1] == "w":
                moves.append(Move(self.board, (row, col), (row + 1, col+1)))
        if col > 0:
            if color == "b" and self.board[row+1][col-1][1] == "w":
                moves.append(Move(self.board, (row, col), (row + 1, col-1)))

        return moves

class Move:
    def __init__(self, board, start, end):
        self.start_row = start[0]
        self.end_row = end[0]
        self.start_col = start[1]
        self.end_col = end[1]
        self.moved = board[self.start_row][self.start_col]
        self.captured = board[self.end_row][self.end_col]







