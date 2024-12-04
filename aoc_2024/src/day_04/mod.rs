use crate::utils::io::get_file;

pub fn day_04() {
    let inputs = get_input("./src/day_04/input.txt");

    let solution_1 = part_one(&inputs);
    println!("\t- Solution 1 is : {solution_1}");

    let solution_2 = part_two(&inputs);
    println!("\t- Solution 2 is : {solution_2}");
}

fn get_input(file_name: &str) -> Vec<Vec<char>> {
    get_file(file_name)
        .lines()
        .map(|line| line.chars().collect())
        .collect()
}
fn count_xmas_down(grid: &[Vec<char>], y: usize, x: usize, height: usize, _width: usize) -> usize {
    if y + 3 >= height {
        return 0;
    }
    let positions = [(y, x), (y + 1, x), (y + 2, x), (y + 3, x)];
    count_xmas_samx(grid, &positions)
}

fn count_xmas_right(grid: &[Vec<char>], y: usize, x: usize, _height: usize, width: usize) -> usize {
    if x + 3 >= width {
        return 0;
    }
    let positions = [(y, x), (y, x + 1), (y, x + 2), (y, x + 3)];
    count_xmas_samx(grid, &positions)
}

fn count_xmas_down_right(
    grid: &[Vec<char>],
    y: usize,
    x: usize,
    height: usize,
    width: usize,
) -> usize {
    if y + 3 >= height || x + 3 >= width {
        return 0;
    }
    let positions = [(y, x), (y + 1, x + 1), (y + 2, x + 2), (y + 3, x + 3)];
    count_xmas_samx(grid, &positions)
}

fn count_xmas_up_right(
    grid: &[Vec<char>],
    y: usize,
    x: usize,
    _height: usize,
    width: usize,
) -> usize {
    if y < 3 || x + 3 >= width {
        return 0;
    }
    let positions = [(y, x), (y - 1, x + 1), (y - 2, x + 2), (y - 3, x + 3)];
    count_xmas_samx(grid, &positions)
}

fn count_xmas_samx(grid: &[Vec<char>], positions: &[(usize, usize)]) -> usize {
    let letters: Vec<char> = positions.iter().map(|&(y, x)| grid[y][x]).collect();
    let is_xmas = letters == ['X', 'M', 'A', 'S'];
    let is_samx = letters == ['S', 'A', 'M', 'X'];

    if is_xmas && is_samx {
        2
    } else if is_xmas || is_samx {
        1
    } else {
        0
    }
}

fn part_one(grid: &[Vec<char>]) -> usize {
    let mut xmas_count = 0;
    let height = grid.len();
    let width = grid[0].len();

    for y in 0..height {
        for x in 0..width {
            xmas_count += count_xmas_down(grid, y, x, height, width);
            xmas_count += count_xmas_right(grid, y, x, height, width);
            xmas_count += count_xmas_up_right(grid, y, x, height, width);
            xmas_count += count_xmas_down_right(grid, y, x, height, width);
        }
    }

    xmas_count
}

fn part_two(grid: &[Vec<char>]) -> usize {
    let mut xmas_count = 0;
    let height = grid.len();
    let width = grid[0].len();

    for y in 1..height - 1 {
        for x in 1..width - 1 {
            if grid[y][x] == 'A' {
                let diag1 = vec![grid[y - 1][x - 1], grid[y + 1][x + 1]];
                let diag2 = vec![grid[y + 1][x - 1], grid[y - 1][x + 1]];

                let is_diag1_valid = diag1 == ['M', 'S'] || diag1 == ['S', 'M'];
                let is_diag2_valid = diag2 == ['M', 'S'] || diag2 == ['S', 'M'];

                if is_diag1_valid && is_diag2_valid {
                    xmas_count += 1;
                }
            }
        }
    }

    xmas_count
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let inputs = get_input("./src/day_04/input_example.txt");
        assert_eq!(18, part_one(&inputs));
    }

    #[test]
    fn test_part_two() {
        let inputs = get_input("./src/day_04/input_example.txt");
        assert_eq!(9, part_two(&inputs));
    }
}
