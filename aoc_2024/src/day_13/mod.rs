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

    // let solution_2 = part_two(&input);
    // println!("\t- Solution 2 is : {solution_2}");
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
        .map(|chunk| get_machine(chunk))
        .collect()
}

fn calculate_buttons_press_nbr(machine: &Machine) -> Option<(usize, usize)> {
    let xa = machine.button_a.x;
    let xb = machine.button_b.x;
    let ya = machine.button_a.y;
    let yb = machine.button_b.y;
    let xp = machine.prize.x;
    let yp = machine.prize.y;

    // Construct the matrix m
    let _m = [[xa, xb], [ya, yb]];

    // Calculate the determinant of m
    let det = (xa * yb) - (xb * ya);

    // Check if the matrix is singular
    if det.abs() < 1e-10 {
        return None; // Matrix is singular or nearly singular
    }

    // Calculate the inverse of m by dividing each element by det
    let m_inv = [[yb / det, -xb / det], [-ya / det, xa / det]];

    // Prize vector
    let p = [xp, yp];

    // Calculate the vector of button presses
    let q_a = m_inv[0][0] * p[0] + m_inv[0][1] * p[1];
    let q_b = m_inv[1][0] * p[0] + m_inv[1][1] * p[1];

    let epsilon = 1e-6;

    // Check if q_a and q_b are close enough to integers
    let q_a_round = q_a.round();
    let q_b_round = q_b.round();

    // Ensure that the rounded values are within the allowed range
    if (q_a - q_a_round).abs() <= epsilon
        && (q_b - q_b_round).abs() <= epsilon
        && q_a_round >= 0.0
        && q_b_round >= 0.0
        && q_a_round <= 100.0
        && q_b_round <= 100.0
    {
        Some((q_a_round as usize, q_b_round as usize))
    } else {
        None
    }
}

fn part_one(machines: &[Machine]) -> usize {
    let mut total = 0;
    for machine in machines {
        if let Some((button_a_press, button_b_press)) = calculate_buttons_press_nbr(machine) {
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
        // let input = get_input("./src/day_13/input_example.txt");
        // assert_eq!(1930, part_one(&input));
    }

    // #[test]
    // fn test_part_two() {
    //     let input = get_input("./src/day_13/input_example.txt");
    //     assert_eq!(1306, part_two(&input));
    // }
}
