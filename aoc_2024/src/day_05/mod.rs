use crate::parse_input;
use crate::utils::io::{get_file, LINE_ENDING};
use itertools::Itertools;

pub fn day_05() {
    let (rules, updates) = get_input("./src/day_05/input.txt");
    let solution_1 = part_one(&rules, &updates);
    println!("\t- Solution 1 is : {solution_1}");

    let solution_2 = part_two(&rules, &updates);
    println!("\t- Solution 2 is : {solution_2}");
}

fn get_input(file_name: &str) -> (Vec<(u8, u8)>, Vec<Vec<u8>>) {
    let file = get_file(file_name);
    let split_separator = format!("{}{}", LINE_ENDING, LINE_ENDING);
    let sections: Vec<&str> = file.split(&split_separator).collect();

    // Parse the page ordering rules
    let ordering_rules = sections[0]
        .lines()
        .map(|line| {
            line.split('|')
                .map(|num| parse_input!(num, u8))
                .collect_tuple::<(u8, u8)>()
                .unwrap()
        })
        .collect();

    // Parse the updates
    let updates = sections[1]
        .lines()
        .map(|line| {
            line.split(',')
                .map(|num| parse_input!(num, u8))
                .collect::<Vec<u8>>()
        })
        .collect();

    (ordering_rules, updates)
}

fn is_update_valid(rules: &[(u8, u8)], update: &[u8]) -> bool {
    for rule in rules {
        let left_position = update.iter().position(|&x| x == rule.0);
        let right_position = update.iter().position(|&x| x == rule.1);

        if let (Some(left), Some(right)) = (left_position, right_position) {
            if left > right {
                return false;
            }
        }
    }
    true
}

fn custom_compare(a: &u8, b: &u8, rules: &[(u8, u8)]) -> std::cmp::Ordering {
    for (left, right) in rules {
        if left == a && right == b {
            return std::cmp::Ordering::Less;
        }
        if left == b && right == a {
            return std::cmp::Ordering::Greater;
        }
    }
    std::cmp::Ordering::Equal
}

fn part_one(rules: &[(u8, u8)], updates: &[Vec<u8>]) -> usize {
    updates
        .iter()
        .filter(|update| is_update_valid(rules, update))
        .map(|update| update[update.len() / 2] as usize)
        .sum()
}

fn part_two(rules: &[(u8, u8)], updates: &[Vec<u8>]) -> usize {
    let mut total = 0;
    for update in updates {
        let ordered: Vec<u8> = update
            .iter()
            .copied()
            .sorted_by(|a, b| custom_compare(a, b, rules))
            .collect();

        if !ordered.eq(update) {
            total += ordered[update.len() / 2] as usize;
        }
    }
    total
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let (rules, update) = get_input("./src/day_05/input_example.txt");
        assert_eq!(143, part_one(&rules, &update));
    }

    #[test]
    fn test_part_two() {
        let (rules, update) = get_input("./src/day_05/input_example.txt");
        assert_eq!(123, part_two(&rules, &update));
    }
}
