use crate::utils::io::get_file;
use itertools::Itertools;
use std::collections::HashMap;

pub fn day_01() {
    let (left_column, right_column) = get_input();

    let solution_1 = part_one(&left_column, &right_column);
    println!("\t- Solution 1 is : {solution_1}");

    let solution_2 = part_two(&left_column, &right_column);
    println!("\t- Solution 2 is : {solution_2}");
}

fn get_input() -> (Vec<i32>, Vec<i32>) {
    let file = get_file("./src/day_01/input.txt");
    let mut left_column = Vec::new();
    let mut right_column = Vec::new();
    for line in file.lines() {
        let split = line.split_whitespace().collect::<Vec<_>>();
        left_column.push(split[0].parse().unwrap());
        right_column.push(split[1].parse().unwrap());
    }
    (left_column, right_column)
}

fn part_one(left_column: &[i32], right_column: &[i32]) -> i32 {
    left_column
        .iter()
        .sorted()
        .zip(right_column.iter().sorted())
        .map(|(left, right)| (left - right).abs())
        .sum()
}

fn part_two(left_column: &[i32], right_column: &[i32]) -> i32 {
    let mut occurrences = HashMap::new();

    for &value in right_column {
        *occurrences.entry(value).or_insert(0) += 1;
    }
    left_column
        .iter()
        .map(|value| value * occurrences.get(value).unwrap_or(&0))
        .sum()
}
