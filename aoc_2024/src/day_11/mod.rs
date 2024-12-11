use crate::utils::io::get_file;
use aoc_2024::parse_input;
use std::collections::HashMap;

pub fn day_11() {
    let input = get_input("./src/day_11/input.txt");

    let solution_1 = part_one(&input);
    println!("\t- Solution 1 is : {solution_1}");

    let solution_2 = part_two(&input);
    println!("\t- Solution 2 is : {solution_2}");
}

fn get_input(file_name: &str) -> Vec<u64> {
    get_file(file_name)
        .split_whitespace()
        .map(|element| parse_input!(element, u64))
        .collect()
}

fn blink(stones: &HashMap<u64, u64>, next_stones: &mut HashMap<u64, u64>) {
    for (&stone_value, &stone_nbr) in stones {
        if stone_value == 0 {
            *next_stones.entry(1).or_insert(0) += stone_nbr;
        } else if (stone_value.checked_ilog10().unwrap_or(0) + 1) % 2 == 0 {
            // Calculate the total number of digits
            let num_digits = stone_value.checked_ilog10().unwrap_or(0) + 1;

            // Find the splitting point (half the digits)
            let half_digits = num_digits / 2;

            // Calculate the divisor to separate the halves
            let divisor = 10u64.pow(half_digits);

            // Split the number into two parts
            let left = stone_value / divisor;
            let right = stone_value % divisor;
            *next_stones.entry(left).or_insert(0) += stone_nbr;
            *next_stones.entry(right).or_insert(0) += stone_nbr;
        } else {
            *next_stones.entry(stone_value * 2024).or_insert(0) += stone_nbr;
        }
    }
}

fn part_one(stones: &[u64]) -> u64 {
    let mut stones = stones.iter().map(|v| (*v, 1u64)).collect();
    let mut next_stones = HashMap::new();

    for _ in 0..25 {
        next_stones.clear();
        blink(&stones, &mut next_stones);
        std::mem::swap(&mut stones, &mut next_stones);
    }
    stones.iter().map(|(_, &v)| v).sum()
}

fn part_two(stones: &[u64]) -> u64 {
    let mut stones = stones.iter().map(|v| (*v, 1u64)).collect();
    let mut next_stones = HashMap::new();

    for _ in 0..75 {
        next_stones.clear();
        blink(&stones, &mut next_stones);
        std::mem::swap(&mut stones, &mut next_stones);
    }
    stones.iter().map(|(_, &v)| v).sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = get_input("./src/day_11/input_example.txt");
        assert_eq!(55312, part_one(&input));
    }

    #[test]
    fn test_part_two() {
        let input = get_input("./src/day_11/input_example.txt");
        assert_eq!(65601038650482, part_two(&input));
    }
}
