use crate::utils::get_file;
use regex::Regex;
use lazy_static::lazy_static;
use std::collections::HashMap;


lazy_static! {
    static ref REGEX_MASK: Regex = Regex::new(r"^mask = ([01X]+)$").unwrap();
    static ref REGEX_MEM: Regex = Regex::new(r"^mem\[(\d+)\] = (\d+)").unwrap();
}


pub fn day_14() {
    let actions = get_input();

    let solution_a = solve_part_a(&actions);
    println!("Part A: {}", solution_a);

    let solution_b = solve_part_b(&actions);
    println!("Part B: {}", solution_b);
}


fn get_input() -> Vec<Action> {
    let mut input = vec![];
    for line in get_file("./inputs/day_14.txt").lines() {
        if let Some(result) = REGEX_MASK.captures(line) {
            input.push(Action::Mask(result[1].chars().rev().collect()))
        }
        if let Some(result) = REGEX_MEM.captures(line) {
            input.push(Action::Mem(result[1].parse().unwrap(), result[2].parse().unwrap()))
        }
    }
    input
}


fn solve_part_a(actions: &[Action]) -> u64 {
    let mut current_mask = &String::new();
    let mut memory = HashMap::new();

    for action in actions {
        match action {
            Action::Mask(mask) => {
                current_mask = mask
            }
            Action::Mem(key, value) => {
                memory.insert(key, get_value_with_mask(*value, &current_mask));
            }
        }
    }
    memory.values().sum()
}


fn get_value_with_mask(value: u64, mask: &str) -> u64 {
    let mut new_value = value;

    for (idx, mask_val) in mask.chars().enumerate() {
        if !mask_val.eq(&'X') {
            let bit = if mask_val.eq(&'1') { 1 } else { 0 };
            new_value = set_nth_bit(new_value, idx as u64, bit)
        }
    }
    new_value
}


fn solve_part_b(actions: &[Action]) -> u64 {
    let mut current_mask = &String::new();
    let mut memory = HashMap::new();

    for action in actions {
        match action {
            Action::Mask(mask) => { current_mask = mask }
            Action::Mem(key, value) => {
                for addr in get_addresses_from_mask(&current_mask, key) {
                    memory.insert(addr, *value);
                }
            }
        }
    }
    memory.values().sum()
}


fn get_addresses_from_mask(mask: &str, key: &u64) -> Vec<u64> {
    let mut addresses = vec![];
    addresses.push(0);


    for (idx, mask_val) in mask.chars().enumerate() {
        match mask_val {
            '0' => {
                let bit = get_nth_bit(*key, idx as u64);
                for address in addresses.iter_mut() {
                    *address = set_nth_bit(*address, idx as u64, bit);
                }
            }
            '1' => {
                for address in addresses.iter_mut() {
                    *address = set_nth_bit(*address, idx as u64, 1);
                }
            }
            'X' => {
                let mut tmp_addresses = vec![];
                for address in addresses {
                    tmp_addresses.push(set_nth_bit(address, idx as u64, 0));
                    tmp_addresses.push(set_nth_bit(address, idx as u64, 1));
                }
                addresses = tmp_addresses;
            }
            _ => unreachable!()
        }
    }
    addresses
}


fn set_nth_bit(value: u64, nth_bit: u64, bit: u64) -> u64 {
    (value & (!(1 << nth_bit))) | (bit << nth_bit)
}


fn get_nth_bit(value: u64, nth_bit: u64) -> u64 {
    if nth_bit < 32 {
        (value & (1 << nth_bit) != 0) as u64
    } else {
        0
    }
}


#[derive(Debug)]
enum Action {
    Mask(String),
    Mem(u64, u64),
}

