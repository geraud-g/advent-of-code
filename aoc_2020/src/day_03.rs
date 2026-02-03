use crate::utils::get_file;
use itertools::{iterate, zip};

const TREE: char = '#';

pub fn day_03() {
    let data = get_input();

    let solution_a = traverse_map(&data, 1, 3);
    println!("Part A: {}", solution_a);

    let solution_b = solve_part_b(&data);
    println!("Part B: {}", solution_b);
}

fn get_input() -> Vec<Vec<char>> {
    let data = get_file("./inputs/day_03.txt");
    data.lines().map(|l| l.chars().collect()).collect()
}

fn traverse_map(area: &[Vec<char>], delta_y: usize, delta_x: usize) -> u64 {
    let x_len = area[0].len();
    let y_range = (0..area.len()).step_by(delta_y);
    let x_range = iterate(0, |&i| i + delta_x);
    zip(y_range, x_range)
        .filter(|(y, x)| area[*y][*x % x_len].eq(&TREE))
        .count() as u64
}

fn solve_part_b(area: &[Vec<char>]) -> u64 {
    traverse_map(&area, 1, 1)
        * traverse_map(&area, 1, 3)
        * traverse_map(&area, 1, 5)
        * traverse_map(&area, 1, 7)
        * traverse_map(&area, 2, 1)
}
