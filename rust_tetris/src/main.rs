use crossterm::{
    cursor::{Hide, MoveTo, Show},
    event::{poll, read, Event, KeyCode},
    execute,
    style::{Color, Print, ResetColor, SetBackgroundColor},
    terminal::{
        disable_raw_mode, enable_raw_mode, EnterAlternateScreen, LeaveAlternateScreen,
        SetTitle,
    },
};
use rand::Rng;
use std::io::{stdout, Result, Write};
use std::time::Duration;

const WIDTH: u16 = 10;
const HEIGHT: u16 = 20;

#[derive(Clone, Debug)]
struct Piece {
    shape: Vec<Vec<u8>>,
    x: isize,
    y: isize,
    color: Color,
}

impl Piece {
    fn new(shape: Vec<Vec<u8>>, color: Color) -> Self {
        Piece {
            shape,
            x: WIDTH as isize / 2 - 2,
            y: 0,
            color,
        }
    }

    fn rotate(&mut self) {
        let mut new_shape = vec![vec![0; self.shape[0].len()]; self.shape.len()];
        for (r, row) in self.shape.iter().enumerate() {
            for (c, &val) in row.iter().enumerate() {
                new_shape[c][self.shape.len() - 1 - r] = val;
            }
        }
        self.shape = new_shape;
    }
}

fn get_random_piece() -> Piece {
    let mut rng = rand::thread_rng();
    let piece_type = rng.gen_range(0..7);
    match piece_type {
        0 => Piece::new(
            vec![
                vec![0, 0, 0, 0],
                vec![1, 1, 1, 1],
                vec![0, 0, 0, 0],
                vec![0, 0, 0, 0],
            ],
            Color::Cyan,
        ),
        1 => Piece::new(vec![vec![1, 1], vec![1, 1]], Color::Yellow),
        2 => Piece::new(vec![vec![0, 1, 0], vec![1, 1, 1], vec![0, 0, 0]], Color::Magenta),
        3 => Piece::new(
            vec![vec![0, 1, 1], vec![1, 1, 0], vec![0, 0, 0]],
            Color::Red,
        ),
        4 => Piece::new(
            vec![vec![1, 1, 0], vec![0, 1, 1], vec![0, 0, 0]],
            Color::Green,
        ),
        5 => Piece::new(
            vec![vec![1, 0, 0], vec![1, 1, 1], vec![0, 0, 0]],
            Color::Blue,
        ),
        _ => Piece::new(
            vec![vec![0, 0, 1], vec![1, 1, 1], vec![0, 0, 0]],
            Color::DarkYellow,
        ),
    }
}

fn check_collision(board: &Vec<Vec<(u8, Color)>>, piece: &Piece) -> bool {
    for (r, row) in piece.shape.iter().enumerate() {
        for (c, &val) in row.iter().enumerate() {
            if val != 0 {
                let board_x = piece.x + c as isize;
                let board_y = piece.y + r as isize;
                if board_x < 0
                    || board_x >= WIDTH as isize
                    || board_y < 0
                    || board_y >= HEIGHT as isize
                    || board[board_y as usize][board_x as usize].0 != 0
                {
                    return true;
                }
            }
        }
    }
    false
}

fn merge_piece(board: &mut Vec<Vec<(u8, Color)>>, piece: &Piece) {
    for (r, row) in piece.shape.iter().enumerate() {
        for (c, &val) in row.iter().enumerate() {
            if val != 0 {
                let board_x = piece.x + c as isize;
                let board_y = piece.y + r as isize;
                if board_y >= 0 {
                    board[board_y as usize][board_x as usize] = (1, piece.color);
                }
            }
        }
    }
}

fn clear_lines(board: &mut Vec<Vec<(u8, Color)>>) -> u32 {
    let mut lines_cleared = 0;
    let mut r = HEIGHT as usize - 1;
    while r > 0 {
        if board[r].iter().all(|&cell| cell.0 != 0) {
            lines_cleared += 1;
            for y in (1..=r).rev() {
                board[y] = board[y - 1].clone();
            }
            board[0] = vec![(0, Color::Reset); WIDTH as usize];
        } else {
            r -= 1;
        }
    }
    lines_cleared
}

fn draw_board(
    stdout: &mut std::io::Stdout,
    board: &Vec<Vec<(u8, Color)>>,
    piece: &Piece,
    score: u32,
) -> Result<()> {
    execute!(stdout, MoveTo(0, 0))?;
    for y in 0..HEIGHT {
        for x in 0..WIDTH {
            let mut is_piece = false;
            for r in 0..piece.shape.len() {
                for c in 0..piece.shape[0].len() {
                    if piece.shape[r][c] != 0 {
                        let piece_x = piece.x + c as isize;
                        let piece_y = piece.y + r as isize;
                        if piece_x == x as isize && piece_y == y as isize {
                            is_piece = true;
                            break;
                        }
                    }
                }
                if is_piece {
                    break;
                }
            }

            if is_piece {
                execute!(
                    stdout,
                    SetBackgroundColor(piece.color),
                    Print("  "),
                    ResetColor
                )?;
            } else if board[y as usize][x as usize].0 != 0 {
                execute!(
                    stdout,
                    SetBackgroundColor(board[y as usize][x as usize].1),
                    Print("  "),
                    ResetColor
                )?;
            } else {
                execute!(stdout, Print(" ."))?;
            }
        }
        execute!(stdout, Print("\n"))?;
    }
    execute!(
        stdout,
        MoveTo(WIDTH * 2 + 5, 5),
        Print(format!("Score: {}", score))
    )?;
    stdout.flush()?;
    Ok(())
}

fn main() -> Result<()> {
    let mut stdout = stdout();
    execute!(
        stdout,
        EnterAlternateScreen,
        Hide,
        SetTitle("Rust Tetris")
    )?;
    enable_raw_mode()?;

    let mut board = vec![vec![(0, Color::Reset); WIDTH as usize]; HEIGHT as usize];
    let mut piece = get_random_piece();
    let mut score = 0;
    let mut game_over = false;

    loop {
        if poll(Duration::from_millis(50))? {
            if let Event::Key(key_event) = read()? {
                match key_event.code {
                    KeyCode::Char('q') => break,
                    KeyCode::Left => {
                        piece.x -= 1;
                        if check_collision(&board, &piece) {
                            piece.x += 1;
                        }
                    }
                    KeyCode::Right => {
                        piece.x += 1;
                        if check_collision(&board, &piece) {
                            piece.x -= 1;
                        }
                    }
                    KeyCode::Down => {
                        piece.y += 1;
                        if check_collision(&board, &piece) {
                            piece.y -= 1;
                            merge_piece(&mut board, &piece);
                            score += clear_lines(&mut board) * 10;
                            piece = get_random_piece();
                            if check_collision(&board, &piece) {
                                game_over = true;
                            }
                        }
                    }
                    KeyCode::Up => {
                        let mut temp_piece = piece.clone();
                        temp_piece.rotate();
                        if !check_collision(&board, &temp_piece) {
                            piece = temp_piece;
                        }
                    }
                    _ => {}
                }
            }
        } else {
            // Gravity
            piece.y += 1;
            if check_collision(&board, &piece) {
                piece.y -= 1;
                merge_piece(&mut board, &piece);
                score += clear_lines(&mut board) * 10;
                piece = get_random_piece();
                if check_collision(&board, &piece) {
                    game_over = true;
                }
            }
        }

        if game_over {
            break;
        }

        draw_board(&mut stdout, &board, &piece, score)?;
    }

    execute!(
        stdout,
        MoveTo(WIDTH / 2, HEIGHT / 2),
        Print("Game Over!"),
        MoveTo(WIDTH / 2, HEIGHT / 2 + 1),
        Print(format!("Final Score: {}", score)),
        Show,
        LeaveAlternateScreen
    )?;
    disable_raw_mode()?;
    Ok(())
}