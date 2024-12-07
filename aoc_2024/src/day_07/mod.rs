use crate::parse_input;
use crate::utils::io::get_file;

#[derive(Debug)]
struct Equation {
    target: i64,
    values: Vec<i64>,
}

pub fn day_07() {
    let input = get_input("./src/day_07/input.txt");

    let solution_1 = part_one(&input);
    println!("\t- Solution 1 is : {solution_1}");

    let solution_2 = part_two(&input);
    println!("\t- Solution 2 is : {solution_2}");
}

fn get_input(file_name: &str) -> Vec<Equation> {
    let file = get_file(file_name);
    let mut equations = Vec::new();

    for line in file.lines() {
        if let Some((target, values)) = line.split_once(':') {
            let target = parse_input!(target, i64);
            let values = values
                .split_whitespace()
                .map(|s| parse_input!(s, i64))
                .collect();
            equations.push(Equation { target, values });
        }
    }

    equations
}

fn is_solvable(target: i64, values: &[i64], accumulator: i64, use_concatenation: bool) -> bool {
    match values {
        [] => accumulator == target,
        [next_value, rest @ ..] => {
            // Try addition
            is_solvable(target, rest, accumulator + next_value, use_concatenation)
                // Try multiplication
                || is_solvable(target, rest, accumulator * next_value, use_concatenation)
                // Try concatenation if part_2
                || (use_concatenation && {
                let concatenation_str = format!("{}{}", accumulator, next_value);
                let concatenation: i64 = concatenation_str.parse().expect("Invalid concatenation");
                is_solvable(target, rest, concatenation, use_concatenation)
            })
        }
    }
}

fn part_one(equations: &[Equation]) -> i64 {
    equations
        .iter()
        .filter(|equation| is_solvable(equation.target, &equation.values, 0, false))
        .map(|equation| equation.target)
        .sum()
}

fn part_two(equations: &[Equation]) -> i64 {
    equations
        .iter()
        .filter(|equation| is_solvable(equation.target, &equation.values, 0, true))
        .map(|equation| equation.target)
        .sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = get_input("./src/day_07/input_example.txt");
        assert_eq!(3749, part_one(&input));
    }

    #[test]
    fn test_part_two() {
        let input = get_input("./src/day_07/input_example.txt");
        assert_eq!(11387, part_two(&input));
    }
}
