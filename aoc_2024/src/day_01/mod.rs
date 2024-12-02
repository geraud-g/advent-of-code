use crate::parse_input;
use crate::utils::io::get_file;
use itertools::Itertools;
use std::collections::HashMap;

pub fn day_01() {
    let (left_column, right_column) = get_input("./src/day_01/input.txt");

    let solution_1 = part_one(&left_column, &right_column);
    println!("\t- Solution 1 is : {solution_1}");

    let solution_2 = part_two(&left_column, &right_column);
    println!("\t- Solution 2 is : {solution_2}");
}

fn get_input(file_name: &str) -> (Vec<i32>, Vec<i32>) {
    let file = get_file(file_name);
    file.lines()
        .map(|line| {
            let mut split = line.split_whitespace();
            let left: i32 = parse_input!(split.next().unwrap(), i32);
            let right: i32 = parse_input!(split.next().unwrap(), i32);
            (left, right)
        })
        .unzip()
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

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let (left_column, right_column) = get_input("./src/day_01/input_example.txt");
        assert_eq!(11, part_one(&left_column, &right_column));
    }

    #[test]
    fn test_part_two() {
        let (left_column, right_column) = get_input("./src/day_01/input_example.txt");
        assert_eq!(31, part_two(&left_column, &right_column));
    }
}
