import os
import copy
import mat

H = 20
W = 10

board = list()
pieces = list()

path = input()


def line2row(line):
    row = list()
    for letter in line:
        if letter != '\n':
            row.append(1 if letter == "#" else 0)
    return row


def load():
    with open(path, 'r') as f:
        for _ in range(H):
            row = line2row(f.readline())
            if row:
                board.append(row)
        for line in f:
            piece = list()
            while line not in os.linesep:
                row = line2row(line)
                if row:
                    piece.append(row)
                line = f.readline()
            if piece:
                pieces.append(piece)


def full(row):
    return sum(row) == W


def score(brd):
    return sum([1 if full(row) else 0 for row in brd])


def clockwise(piece):
    return list(zip(*piece[::-1]))


def rotate(piece, rotation):
    for _ in range(rotation):
        piece = clockwise(piece)
    return piece


def update_board(piece, pos, rot):
    piece = rotate(piece, rot)
    brd = copy.deepcopy(board)
    height, width = pos
    for i in range(len(piece)):
        for j in range(len(piece[0])):
            x = i + height
            y = j + width
            brd[x][y] += piece[i][j]
            # print(x, y, brd[x][y], i,j, piece[i][j])
            if brd[x][y] == 2:
                return None
    return brd


def fall_down(piece, c):
    p_length = len(piece[0])
    p_height = len(piece)
    last_h = -1
    for h in range(H-p_height-1):
        for ph in range(p_height):
            for pl in range(p_length):
                if board[h+ph][c+pl] + piece[ph][pl] > 1:
                    return last_h
        last_h = h
    return last_h


def solve():
    maximum = 0
    res = (0, 0, 0)
    for i, piece in enumerate(pieces):
        for c in range(len(board[0]) - len(piece[0])):
            for rot in range(4):
                h = fall_down(piece, c)
                pr(update_board(piece, (h, c), rot))
                scr = score(update_board(piece, (h, c), rot))
                if scr > maximum:
                    maximum = scr
                    res = (i, rot*90, c)
    return res


def test():
    print(solve())


def pr(brd):
    for row in brd:
        print(row)
    print("\n\n")


def main():
    load()
    test()


if __name__ == '__main__':
    main()
