use crate::parse_input;
use crate::utils::io::get_file;
use lazy_static::lazy_static;
use regex::Regex;

lazy_static! {
    static ref RE_MUL: Regex = Regex::new(r"mul\((\d{1,3}),(\d{1,3})\)").unwrap();
}

pub fn day_03() {
    let inputs = get_input("./src/day_03/input.txt");

    let solution_1 = part_one(&inputs);
    println!("\t- Solution 1 is : {solution_1}");

    let solution_2 = part_two(&inputs);
    println!("\t- Solution 2 is : {solution_2}");
}

fn get_input(file_name: &str) -> String {
    get_file(file_name)
}

fn part_one(instructions: &str) -> usize {
    RE_MUL
        .captures_iter(instructions)
        .map(|capture| {
            let x = capture.get(1).unwrap().as_str();
            let y = capture.get(2).unwrap().as_str();
            parse_input!(x, usize) * parse_input!(y, usize)
        })
        .sum()
}

fn part_two(instructions: &str) -> usize {
    let mut mul_enabled = true;
    let mut total = 0;
    let mut current_index = 0;

    loop {
        if mul_enabled {
            if let Some(index) = instructions[current_index..].find("don't()") {
                total += part_one(&instructions[current_index..current_index + index]);
                current_index += index + 7;
                mul_enabled = false;
            } else {
                total += part_one(&instructions[current_index..]);
                break;
            }
        } else if let Some(index) = instructions[current_index..].find("do()") {
            current_index += index + 4;
            mul_enabled = true;
        } else {
            break;
        }
    }
    total
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let inputs = get_input("./src/day_03/input_example_part_1.txt");
        assert_eq!(161, part_one(&inputs));
    }

    #[test]
    fn test_part_two() {
        let inputs = get_input("./src/day_03/input_example_part_2.txt");
        assert_eq!(48, part_two(&inputs));
    }
}
