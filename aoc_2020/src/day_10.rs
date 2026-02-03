use crate::utils::get_file;
use itertools::max;
use std::collections::{HashMap, HashSet};

pub fn day_10() {
    let input = get_input();

    let solution_a = solve_part_a(&input, Counter::default());
    println!("Part A: {}", solution_a.unwrap());

    let solution_b = solve_part_b(&input);
    println!("Part B: {}", solution_b);
}

fn get_input() -> HashSet<i64> {
    get_file("./inputs/day_10.txt")
        .lines()
        .map(|line| line.parse::<i64>().unwrap())
        .collect()
}

pub fn solve_part_a(numbers: &HashSet<i64>, counter: Counter) -> Option<i64> {
    if counter.numbers_processed == numbers.len() {
        return Some(counter.one_diff * (counter.three_diff + 1));
    }

    for n in (counter.value + 1)..(counter.value + 4) {
        if numbers.contains(&n) {
            let diff = n - counter.value;
            let mut c = counter.new_from(n);
            match diff {
                1 => c.one_diff += 1,
                3 => c.three_diff += 1,
                _ => {}
            }
            let res = solve_part_a(numbers, c);
            if res.is_some() {
                return res;
            }
        }
    }
    None
}

fn solve_part_b(numbers: &HashSet<i64>) -> i64 {
    let max_val = max(numbers);
    let mut new_cache: HashMap<i64, i64> = HashMap::new();
    rec(&numbers, &mut new_cache, *max_val.unwrap())
}

fn rec(numbers: &HashSet<i64>, cache: &mut HashMap<i64, i64>, current_number: i64) -> i64 {
    if current_number == 0 {
        return 1;
    }
    let mut counter = 0;
    for n in ((current_number - 3)..current_number).rev() {
        if numbers.contains(&n) || n == 0 {
            if cache.contains_key(&n) {
                counter += cache.get(&n).unwrap();
            } else {
                let value = rec(numbers, cache, n);
                cache.insert(n, value);
                counter += value;
            }
        }
    }
    counter
}

#[derive(Debug, Default)]
pub struct Counter {
    value: i64,
    numbers_processed: usize,
    one_diff: i64,
    three_diff: i64,
}

impl Counter {
    fn new_from(&self, value: i64) -> Self {
        Counter {
            value,
            numbers_processed: self.numbers_processed + 1,
            one_diff: self.one_diff,
            three_diff: self.three_diff,
        }
    }
}
