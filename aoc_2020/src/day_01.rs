use crate::utils::get_file;
use itertools::Itertools;

pub fn day_01() {
    let input = get_input();

    let solution_a = solve(&input, 2).expect("No solution found for Part A");
    println!("Part A: {}", solution_a);

    let solution_b = solve(&input, 3).expect("No solution found for Part B");
    println!("Part B: {}", solution_b);
}

fn get_input() -> Vec<i32> {
    let data = get_file("./inputs/day_01.txt");
    data.lines().map(|s| s.parse().unwrap()).collect()
}

fn solve(input: &[i32], entries_nbr: usize) -> Option<i32> {
    let valid_combinations = input
        .iter()
        .filter(|i| **i < 2020)
        .cloned()
        .combinations(entries_nbr)
        .find(|comb| comb.iter().sum::<i32>() == 2020);

    match valid_combinations {
        Some(value) => Some(value.iter().product()),
        _ => None,
    }
}
