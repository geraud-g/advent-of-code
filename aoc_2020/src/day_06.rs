use crate::utils::{get_file, LINE_ENDING};
use std::collections::HashSet;


pub fn day_06() {
    let input = get_input();

    let result_a = solve_part_a(&input);
    println!("Part A: {}", result_a);

    let result_b = solve_part_b(&input);
    println!("Part B: {}", result_b);
}


fn get_input() -> Vec<String> {
    get_file("./inputs/day_06.txt")
        .split(&format!("{}{}", LINE_ENDING, LINE_ENDING)).map(|l| l.to_string())
        .collect()
}


fn solve_part_a(groups: &[String]) -> usize {
    groups.iter()
        .map(
            |g| g.chars().filter(|c| c.is_alphabetic()).collect::<HashSet<_>>().len()
        )
        .sum()
}


fn solve_part_b(groups: &[String]) -> usize {
    let mut answered_questions = 0;

    for group in groups {
        let answers = group.split_whitespace()
            .map(|f| f.chars().collect())
            .fold(
                (b'a'..=b'z').map(char::from).collect::<HashSet<_>>(),
                |acc, val| acc.intersection(&val).cloned().collect::<HashSet<_>>(),
            ).len();

        answered_questions += answers;
    }
    answered_questions
}
