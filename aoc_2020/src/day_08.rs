use crate::utils::get_file;
use std::collections::HashSet;
use itertools::Itertools;


pub fn day_08() {
    let instructions = get_input();

    println!("Part A: {}", solve_part_a(&instructions));

    println!("Part B: {}", solve_part_b(&instructions));
}


fn get_input() -> Vec<Instruction> {
    let mut input = vec![];
    for line in get_file("./inputs/day_08.txt").lines() {
        let split = line.split(' ').collect_vec();
        let value = split[1].parse::<i32>().unwrap();
        let instruction = match split[0] {
            "acc" => Instruction { action: Action::Acc, value },
            "jmp" => Instruction { action: Action::Jmp, value },
            "nop" => Instruction { action: Action::Nop, value },
            _ => panic!("Wrong value: {}", line)
        };
        input.push(instruction);
    }
    input
}


fn solve_part_a(instructions: &[Instruction]) -> usize {
    let mut cpu = Cpu::new();
    cpu.run(instructions);
    cpu.accumulator
}


fn solve_part_b(instructions: &[Instruction]) -> usize {
    for (idx, instruction) in instructions.iter().enumerate() {
        let new_action = match instruction.action {
            Action::Nop => { Some(Action::Jmp) }
            Action::Jmp => { Some(Action::Nop) }
            _ => None
        };
        if let Some(action) = new_action {
            let mut new_vec = instructions.to_owned();
            new_vec[idx] = Instruction { action, value: instruction.value };
            let mut cpu = Cpu::new();
            cpu.run(&new_vec);
            if cpu.idx >= instructions.len() {
                return cpu.accumulator;
            }
        }
    }
    unreachable!()
}


#[derive(Debug, Copy, Clone)]
pub struct Instruction {
    action: Action,
    value: i32,
}


#[derive(Debug, Copy, Clone)]
pub enum Action {
    Acc,
    Jmp,
    Nop,
}


#[derive(Debug, Default)]
struct Cpu {
    idx: usize,
    pub accumulator: usize,
    history: HashSet<usize>,
}


impl Cpu {
    fn new() -> Self {
        Cpu {
            idx: 0,
            accumulator: 0,
            history: Default::default(),
        }
    }

    fn acc(&mut self, value: &i32) {
        self.accumulator = (self.accumulator as i32 + value) as usize;
        self.idx += 1
    }

    fn jmp(&mut self, value: &i32) {
        self.idx = (self.idx as i32 + value) as usize
    }

    fn nop(&mut self, _: &i32) {
        self.idx += 1
    }

    fn run(&mut self, instructions: &[Instruction]) {
        while self.idx < instructions.len() {
            let instruction = instructions.get(self.idx).unwrap();
            let state = self.idx;
            if self.history.contains(&state) { return; }
            self.history.insert(state);

            match instruction.action {
                Action::Acc => self.acc(&instruction.value),
                Action::Jmp => self.jmp(&instruction.value),
                Action::Nop => self.nop(&instruction.value),
            };
        }
    }
}
