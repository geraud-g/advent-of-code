use crate::utils::{get_file, LINE_ENDING};
use lazy_static::lazy_static;
use regex::Regex;
use std::collections::HashMap;

lazy_static! {
    static ref REGEX_VALUE: Regex = Regex::new(r####"(\d+): "(\w+)""####).unwrap();
}

#[test]
fn test() {
    day_19()
}

pub fn day_19() {
    let (rules, inputs) = get_input();

    let solution_a = inputs.iter().filter(|t| is_valid(&rules, t)).count();
    println!("Part A: {}", solution_a);
}

fn is_valid(rules: &HashMap<usize, Node>, input: &str) -> bool {
    if let Some(val) = eval(rules, input, rules.get(&0).unwrap()) {
        val == input.len()
    } else {
        false
    }
}

fn eval(rules: &HashMap<usize, Node>, input: &str, current_rule: &Node) -> Option<usize> {
    if input.is_empty() {
        return None;
    }
    if let Some(value) = current_rule.value {
        return if input.chars().next().unwrap().eq(&value) {
            Some(1)
        } else {
            None
        };
    }
    'rules_list: for rules_list in &current_rule.children {
        let mut idx = 0;

        for rule_idx in rules_list {
            let rule = rules.get(&rule_idx).unwrap();
            if let Some(value) = eval(rules, &input[idx..], rule) {
                idx += value;
            } else {
                continue 'rules_list;
            }
        }
        return Some(idx);
    }
    None
}

fn get_input() -> (HashMap<usize, Node>, Vec<String>) {
    let mut nodes = HashMap::new();
    let parts: Vec<String> = get_file("./inputs/day_19.txt")
        .split(&format!("{}{}", LINE_ENDING, LINE_ENDING))
        .map(|l| l.to_string())
        .collect();

    for line in parts[0].lines() {
        let node = get_node(line);
        nodes.insert(node.idx, node);
    }
    let sentences: Vec<String> = parts[1].lines().map(|s| s.to_string()).collect();
    (nodes, sentences)
}

fn get_node(line: &str) -> Node {
    if let Some(result) = REGEX_VALUE.captures(line) {
        return Node {
            idx: result[1].parse().unwrap(),
            value: Some(result[2].chars().next().unwrap()),
            children: vec![],
        };
    }
    let splitted: Vec<&str> = line.split(':').collect();
    let mut rules_list = vec![];
    for str_rule in splitted[1].split('|') {
        let rules: Vec<usize> = str_rule
            .split(' ')
            .filter(|&p| !p.eq(""))
            .map(|s| s.parse().unwrap())
            .collect();
        rules_list.push(rules);
    }
    Node {
        idx: splitted[0].parse().unwrap(),
        value: None,
        children: rules_list,
    }
}

#[derive(Debug)]
struct Node {
    idx: usize,
    value: Option<char>,
    children: Vec<Vec<usize>>,
}
