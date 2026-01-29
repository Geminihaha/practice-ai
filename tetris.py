
import os
import time
import random

# 게임 보드 크기
BOARD_WIDTH = 10
BOARD_HEIGHT = 20

# 테트로미노 모양
TETROMINOES = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1], [1, 1]],
    'T': [[0, 1, 0], [1, 1, 1]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'Z': [[1, 1, 0], [0, 1, 1]],
    'J': [[1, 0, 0], [1, 1, 1]],
    'L': [[0, 0, 1], [1, 1, 1]]
}

# 테트로미노 색상
COLORS = {
    'I': '\033[96m',  # Cyan
    'O': '\033[93m',  # Yellow
    'T': '\033[95m',  # Magenta
    'S': '\033[92m',  # Green
    'Z': '\033[91m',  # Red
    'J': '\033[94m',  # Blue
    'L': '\033[38;5;208m', # Orange
    'EMPTY': '\033[0m',   # Reset color for empty cells
    'BLACK': '\033[0m'    # Black - This one seems redundant now, but keep for other uses or clear.
}

def clear_screen():
    """화면을 지웁니다."""
    os.system('cls' if os.name == 'nt' else 'clear')

def create_board():
    """게임 보드를 생성합니다."""
    return [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

def new_tetromino():
    """새로운 테트로미노를 생성합니다."""
    shape_key = random.choice(list(TETROMINOES.keys()))
    return {
        'shape': TETROMINOES[shape_key],
        'color': COLORS[shape_key],
        'x': BOARD_WIDTH // 2 - len(TETROMINOES[shape_key][0]) // 2,
        'y': 0,
        'shape_key': shape_key
    }

def is_valid_position(board, piece):
    """테트로미노가 유효한 위치에 있는지 확인합니다."""
    for y, row in enumerate(piece['shape']):
        for x, cell in enumerate(row):
            if cell:
                board_y = piece['y'] + y
                board_x = piece['x'] + x
                if not (0 <= board_y < BOARD_HEIGHT and 0 <= board_x < BOARD_WIDTH and board[board_y][board_x] == 0):
                    return False
    return True

def lock_piece(board, piece):
    """테트로미노를 보드에 고정합니다."""
    for y, row in enumerate(piece['shape']):
        for x, cell in enumerate(row):
            if cell:
                board[piece['y'] + y][piece['x'] + x] = piece['shape_key']

def draw_board(board, piece, score):
    """게임 보드를 그립니다."""
    clear_screen()
    print("점수:", score)
    temp_board = [row[:] for row in board]
    for y, row in enumerate(piece['shape']):
        for x, cell in enumerate(row):
            if cell:
                temp_board[piece['y'] + y][piece['x'] + x] = piece['shape_key']

    # Print top border
    print("+" + "—" * (BOARD_WIDTH * 2) + "+")

    for row in temp_board:
        line = "|"
        for cell in row:
            if cell == 0:
                line += f"{COLORS['EMPTY']}  "
            else:
                line += f"{COLORS[cell]}██{COLORS['EMPTY']}"
        line += "|"
        print(line)

    # Print bottom border
    print("+" + "—" * (BOARD_WIDTH * 2) + "+")


def clear_lines(board):
    """완성된 라인을 지우고 점수를 반환합니다."""
    lines_cleared = 0
    new_board = [row for row in board if any(cell == 0 for cell in row)]
    lines_cleared = BOARD_HEIGHT - len(new_board)
    for _ in range(lines_cleared):
        new_board.insert(0, [0 for _ in range(BOARD_WIDTH)])
    return new_board, lines_cleared * 10


import os
import time
import random
import sys
import tty
import termios

def get_key():
    """사용자 입력을 즉시 반환합니다."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def rotate_piece(piece):
    """테트로미노를 회전합니다."""
    shape = piece['shape']
    new_shape = [list(row) for row in zip(*shape[::-1])]
    piece['shape'] = new_shape

def main():
    """게임의 메인 루프입니다."""
    board = create_board()
    score = 0
    game_over = False
    current_piece = new_tetromino()
    
    fall_time = 0
    fall_speed = 0.5

    while not game_over:
        draw_board(board, current_piece, score)
        
        key = get_key()
        if key == 'q':
            game_over = True
        elif key == 'a':
            current_piece['x'] -= 1
            if not is_valid_position(board, current_piece):
                current_piece['x'] += 1
        elif key == 'd':
            current_piece['x'] += 1
            if not is_valid_position(board, current_piece):
                current_piece['x'] -= 1
        elif key == 's':
            current_piece['y'] += 1
            if not is_valid_position(board, current_piece):
                current_piece['y'] -= 1
        elif key == 'w':
            rotate_piece(current_piece)
            if not is_valid_position(board, current_piece):
                rotate_piece(current_piece)
                rotate_piece(current_piece)
                rotate_piece(current_piece)


        fall_time += 0.1
        if fall_time >= fall_speed:
            fall_time = 0
            current_piece['y'] += 1
            if not is_valid_position(board, current_piece):
                current_piece['y'] -= 1
                lock_piece(board, current_piece)
                board, points = clear_lines(board)
                score += points
                current_piece = new_tetromino()
                if not is_valid_position(board, current_piece):
                    game_over = True
        
        time.sleep(0.1)


    print("게임 오버! 최종 점수:", score)

if __name__ == "__main__":
    main()
