use crate::utils::io::get_file;
use aoc_2024::utils::io::LINE_ENDING;
use lazy_static::lazy_static;
use regex::Regex;

lazy_static! {
    static ref COORD_REGEX: Regex = Regex::new(r"[Xx][+=](\d+),\s*[Yy][+=](\d+)").unwrap();
}

#[derive(Debug)]
struct Point {
    x: f64,
    y: f64,
}
impl std::fmt::Display for Point {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(f, "({}, {})", self.x, self.y)
    }
}

#[derive(Debug)]
struct Machine {
    button_a: Point,
    button_b: Point,
    prize: Point,
}

impl std::fmt::Display for Machine {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(
            f,
            "[A: {}, B: {}, Prize: {}]",
            self.button_a, self.button_b, self.prize
        )
    }
}

pub fn day_13() {
    let input = get_input("./src/day_13/input.txt");

    let solution_1 = part_one(&input);
    println!("\t- Solution 1 is : {solution_1}");

    let solution_2 = part_two(&input);
    println!("\t- Solution 2 is : {solution_2}");
}

fn get_machine(text: &str) -> Machine {
    let mut coords: Vec<(f64, f64)> = Vec::new();

    for cap in COORD_REGEX.captures_iter(text) {
        let x = cap[1].parse::<f64>().expect("Invalid X coordinate");
        let y = cap[2].parse::<f64>().expect("Invalid Y coordinate");
        coords.push((x, y));
    }

    Machine {
        button_a: Point {
            x: coords[0].0,
            y: coords[0].1,
        },
        button_b: Point {
            x: coords[1].0,
            y: coords[1].1,
        },
        prize: Point {
            x: coords[2].0,
            y: coords[2].1,
        },
    }
}

fn get_input(file_name: &str) -> Vec<Machine> {
    let split_separator = format!("{}{}", LINE_ENDING, LINE_ENDING);
    get_file(file_name)
        .split(&split_separator)
        .map(get_machine)
        .collect()
}

fn calculate_buttons_press_nbr(machine: &Machine, part_two: bool) -> Option<(usize, usize)> {
    let xa = machine.button_a.x as i64;
    let xb = machine.button_b.x as i64;
    let ya = machine.button_a.y as i64;
    let yb = machine.button_b.y as i64;
    let mut xp = machine.prize.x as i64;
    let mut yp = machine.prize.y as i64;

    if part_two {
        xp += 10000000000000;
        yp += 10000000000000;
    }

    let det = xa * yb - xb * ya;

    if (xp * yb - xb * yp) % det != 0 || (xa * yp - ya * xp) % det != 0 {
        return None;
    }

    let a = (xp * yb - xb * yp) / det;
    let b = (xa * yp - ya * xp) / det;

    if a >= 0 && b >= 0 {
        Some((a as usize, b as usize))
    } else {
        None
    }
}

fn part_one(machines: &[Machine]) -> usize {
    let mut total = 0;
    for machine in machines {
        if let Some((button_a_press, button_b_press)) = calculate_buttons_press_nbr(machine, false)
        {
            total += (button_a_press * 3) + button_b_press;
        }
    }
    total
}

fn part_two(machines: &[Machine]) -> usize {
    let mut total = 0;
    for machine in machines {
        if let Some((button_a_press, button_b_press)) = calculate_buttons_press_nbr(machine, true) {
            total += (button_a_press * 3) + button_b_press;
        }
    }
    total
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = get_input("./src/day_13/input_example.txt");
        assert_eq!(480, part_one(&input));
    }

    #[test]
    fn test_part_two() {
        let input = get_input("./src/day_13/input_example.txt");
        assert_eq!(875318608908, part_two(&input));
    }
}
