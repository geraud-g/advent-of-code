use crate::utils::get_file;
use lazy_static::lazy_static;
use regex::Regex;
use std::collections::HashMap;

lazy_static! {
    static ref REGEX_TWO_PARS: Regex = Regex::new(r"([\w ]+) bags? contain ([\w ,]+)").unwrap();
    static ref REGEX_CONTAINS_BAGS: Regex = Regex::new(r"(\d+) ([\w ]+) bags?").unwrap();
}

pub fn day_07() {
    let rules = get_rules(get_input());

    let counter = &rules.iter().filter(|r| contains_shiny(r.0, &rules)).count();
    println!("Part A: {}", counter);

    let count_2 = count_bags("shiny gold", &rules);
    println!("Part B: {}", count_2 - 1);
}

fn get_input() -> String {
    get_file("./inputs/day_07.txt")
}

fn get_rules(input: String) -> HashMap<String, Vec<Bag>> {
    input
        .lines()
        .map(|l| get_rule(l))
        .collect::<HashMap<String, Vec<Bag>>>()
}

fn get_rule(rule: &str) -> (String, Vec<Bag>) {
    let result = REGEX_TWO_PARS.captures(rule).unwrap();
    let key = result[1].trim().to_string();
    let bags = match &result[2] {
        "no other bags" => vec![],
        _ => result[2]
            .split(", ")
            .map(|bag| REGEX_CONTAINS_BAGS.captures(bag).unwrap())
            .map(|result| Bag {
                name: result[2].to_string(),
                quantity: result[1].parse().unwrap(),
            })
            .collect(),
    };
    (key, bags)
}

fn contains_shiny(key: &str, bags: &HashMap<String, Vec<Bag>>) -> bool {
    bags.get(key)
        .unwrap()
        .iter()
        .any(|bag| bag.name.eq("shiny gold") || contains_shiny(&bag.name, bags))
}

fn count_bags(key: &str, bags: &HashMap<String, Vec<Bag>>) -> u64 {
    bags.get(key).unwrap().iter().fold(1, |acc, bag| {
        acc + bag.quantity * count_bags(&bag.name, bags)
    })
}

#[derive(Debug, Hash)]
struct Bag {
    name: String,
    quantity: u64,
}
