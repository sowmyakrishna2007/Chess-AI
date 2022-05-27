import pygame as p
from engine import*
from chess_ai import*
import time

images = {}
sq_size = 70

def setup():
    global screen, clock
    p.init()
    screen = p.display.set_mode((560, 560))
    clock = p.time.Clock()

def load():
    images["--"] = None
    pieces = ["bb","bw","kb","kw","nb","nw","pb","pw","qb","qw","rb","rw"]
    for i in pieces:
        images[i] = p.image.load(i + ".png")

def draw_pieces(game_state):
    for i in range(8):
        for j in range(8):
            piece = game_state.board[i][j]
            if images[piece] != None:
                img = images[piece]
                center = img.get_rect(center=p.Rect(j * sq_size, i * sq_size, sq_size, sq_size).center)
                screen.blit(images[piece], center)

def draw_board():
    white = True
    for i in range(8):
        for j in range(8):
            if white:
                p.draw.rect(screen, "wheat1", p.Rect(j * sq_size, i * sq_size, sq_size, sq_size))
            else:
                p.draw.rect(screen, "burlywood3", p.Rect(j*sq_size, i*sq_size, sq_size, sq_size))
            white = not white
        white = not white

def draw_state(game_state):
    draw_board()
    draw_pieces(game_state)

def main():
    load()
    setup()
    game_state = GameState()
    done = False
    selected = ()
    clicks = []
    while not done:
        draw_board()
        if not game_state.white_move:
            move = minmax(game_state.valid_moves(), game_state)
            time.sleep(0.5)
            game_state.move(move)
            if game_state.checkmate() or game_state.stalemate():
                done = True

        for event in p.event.get():
            if event.type == p.QUIT:
                done = True
            if event.type == p.KEYDOWN:
                if event.key == p.K_z:
                    game_state.undo()
                    selected = ()
                    clicks = []
            if event.type == p.MOUSEBUTTONDOWN:
                pos = p.mouse.get_pos()
                if game_state.white_move:
                    turn = "w"
                else:
                    turn = "b"
                row = pos[1]//sq_size
                col = pos[0]//sq_size

                if selected == (row,col):
                    clicks = []
                    selected = ()
                else:
                    selected = (row, col)
                    clicks.append(selected)
                    if len(clicks) == 1:
                        if game_state.board[row][col][1] == turn:
                            valid_moves = game_state.valid_moves()

                        else:
                            selected = ()
                            clicks = []
                    if len(clicks) == 2:
                        board = game_state.board
                        first = clicks[0]
                        second = clicks[1]
                        move_obj = Move(board, first, second)
                        for move in valid_moves:
                            if move.end_row == move_obj.end_row and move.end_col == move_obj.end_col and move.start_row == move_obj.start_row and move.start_col == move_obj.start_col:
                                game_state.move(move_obj)
                                if game_state.checkmate() or game_state.stalemate():
                                    done = True
                        clicks = []
                        selected = ()
        if len(clicks) == 1:
            highlight_square(valid_moves, selected, game_state)

        draw_pieces(game_state)
        p.display.flip()
        clock.tick(20)
    p.quit()

def highlight_square(valid, selected, game_state):
    try:
        row, col = selected
        s = p.Surface((sq_size, sq_size))
        s.set_alpha(100)
        s.fill("blue")
        screen.blit(s, (col*sq_size, row*sq_size))
        s.fill("yellow")
        for v in valid:
            if v.start_row == row and v.start_col == col:
                if game_state.board[v.end_row][v.end_col] != "--":
                    s.fill("red")
                screen.blit(s, (v.end_col*sq_size, v.end_row*sq_size))
                s.fill("yellow")
    except:
        pass

if __name__ == "__main__":
    main()