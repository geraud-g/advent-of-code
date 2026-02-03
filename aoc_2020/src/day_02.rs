use crate::utils::get_file;
use regex::Regex;

pub fn day_02() {
    let input = get_input();

    let solution_a = input.iter().filter(|p| p.is_valid_part_a()).count();
    println!("Part A: {}", solution_a);

    let solution_b = input.iter().filter(|p| p.is_valid_part_b()).count();
    println!("Part B: {}", solution_b);
}

fn get_input() -> Vec<Password> {
    let data = get_file("./inputs/day_02.txt");
    let re = Regex::new(r"(\d+)-(\d+) (.): ([a-z]+)").unwrap();
    let mut passwords = vec![];

    for line in data.lines() {
        if let Some(result) = re.captures(line) {
            passwords.push(Password {
                min: result[1].parse().unwrap(),
                max: result[2].parse().unwrap(),
                letter: result[3].to_string(),
                password: result[4].to_string(),
            });
        }
    }
    passwords
}

struct Password {
    min: usize,
    max: usize,
    letter: String,
    password: String,
}

impl Password {
    pub fn is_valid_part_a(&self) -> bool {
        let letter_count = self.password.matches(&self.letter).count();
        letter_count >= self.min && letter_count <= self.max
    }

    pub fn is_valid_part_b(&self) -> bool {
        let password_as_bytes = self.password.as_bytes();
        let letter_as_bytes = self.letter.as_bytes()[0];
        let first_position_valid = password_as_bytes[self.min - 1] == letter_as_bytes;
        let second_position_valid = password_as_bytes[self.max - 1] == letter_as_bytes;
        first_position_valid ^ second_position_valid
    }
}
