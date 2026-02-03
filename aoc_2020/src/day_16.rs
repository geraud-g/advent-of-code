use crate::utils::{get_file, LINE_ENDING};
use lazy_static::lazy_static;
use regex::Regex;

lazy_static! {
    static ref REGEX_RANGES: Regex = Regex::new(r"(\w+): (\d+)-(\d+) or (\d+)-(\d+)").unwrap();
}

pub fn day_16() {
    let (ranges, _, tickets) = get_input();

    let (_, solution_a) = solve_part_a(&ranges, &tickets);
    println!("Part A: {}", solution_a);

    // let solution_b = solve_part_b_b(&ranges, my_ticket, &valid_tickets);
    // println!("Part B: {}", solution_b);
}

fn get_input() -> (Vec<Field>, Vec<u32>, Vec<Vec<u32>>) {
    let file: Vec<String> = get_file("./inputs/day_16.txt")
        .split(&format!("{}{}", LINE_ENDING, LINE_ENDING))
        .map(|l| l.to_string())
        .collect();
    // Fields
    let mut field_list = vec![];
    for line in file[0].lines() {
        let result = REGEX_RANGES.captures(line).unwrap();
        let field = Field {
            name: result[1].to_string(),
            range_a: (result[2].parse().unwrap(), result[3].parse().unwrap()),
            range_b: (result[4].parse().unwrap(), result[5].parse().unwrap()),
        };

        field_list.push(field);
    }
    // My tickets
    let my_ticket = file[1]
        .lines()
        .nth(1)
        .unwrap()
        .split(',')
        .map(|c| c.parse().unwrap())
        .collect();
    // Tickets
    let mut tickets = vec![];

    for (idx, line) in file[2].lines().enumerate() {
        if idx == 0 {
            continue;
        }
        let ticket: Vec<u32> = line.split(',').map(|c| c.parse().unwrap()).collect();
        tickets.push(ticket)
    }
    (field_list, my_ticket, tickets)
}

fn solve_part_a(ranges: &[Field], tickets: &[Vec<u32>]) -> (Vec<Vec<u32>>, u32) {
    let mut invalid_sum = 0;
    let mut valid_tickets = vec![];
    for ticket in tickets {
        if !ticket
            .iter()
            .any(|&t| !ranges.iter().any(|r| r.is_in_valid_range(t)))
        {
            valid_tickets.push(ticket.clone());
        } else {
            invalid_sum += ticket
                .iter()
                .filter(|&t| !ranges.iter().any(|r| r.is_in_valid_range(*t)))
                .sum::<u32>();
        }
    }

    (valid_tickets, invalid_sum)
}

#[derive(Debug)]
struct Field {
    name: String,
    range_a: (u32, u32),
    range_b: (u32, u32),
}

impl Field {
    fn is_in_valid_range(&self, value: u32) -> bool {
        (value >= self.range_a.0 && value <= self.range_a.1)
            || (value >= self.range_b.0 && value <= self.range_b.1)
    }
}
