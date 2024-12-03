use crate::parse_input;
use crate::utils::io::get_file;
use itertools::Itertools;

pub fn day_02() {
    let inputs = get_input("./src/day_02/input.txt");

    let solution_1 = part_one(&inputs);
    println!("\t- Solution 1 is : {solution_1}");

    let solution_2 = part_two(&inputs);
    println!("\t- Solution 2 is : {solution_2}");
}

fn get_input(file_name: &str) -> Vec<Vec<i16>> {
    let file = get_file(file_name);
    file.lines()
        .map(|line| {
            line.split_whitespace()
                .map(|x| parse_input!(x, i16))
                .collect()
        })
        .collect()
}

fn part_one(reports: &[Vec<i16>]) -> usize {
    reports
        .iter()
        .filter(|report| is_valid_report(report))
        .count()
}

fn is_valid_report(report: &[i16]) -> bool {
    let (mut desc, mut asc) = (true, true);

    for (left, right) in report.iter().tuple_windows() {
        if left < right {
            desc = false;
        }
        if left > right {
            asc = false;
        }
        let diff = (left - right).abs();
        if !(1..=3).contains(&diff) {
            return false;
        }
    }
    desc || asc
}

fn part_two(reports: &[Vec<i16>]) -> usize {
    reports
        .iter()
        .filter(|report| is_valid_report_with_tolerance_of_one(report))
        .count()
}

fn is_valid_report_with_tolerance_of_one(report: &[i16]) -> bool {
    if is_valid_report(report) {
        return true;
    }

    for i in 0..report.len() {
        let mut modified_report = report.to_vec();
        modified_report.remove(i);
        if is_valid_report(&modified_report) {
            return true;
        }
    }
    false
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let inputs = get_input("./src/day_02/input_example_part_1.txt");
        assert_eq!(2, part_one(&inputs));
    }

    #[test]
    fn test_part_two() {
        let inputs = get_input("./src/day_02/input_example_part_1.txt");
        assert_eq!(4, part_two(&inputs));
    }
}
