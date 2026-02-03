use aoc_2020::day_02;
use aoc_2020::day_03;
use aoc_2020::day_04;
use aoc_2020::day_05;
use aoc_2020::day_06;
use aoc_2020::day_07;
use aoc_2020::day_08;
use aoc_2020::day_09;
use aoc_2020::day_10;
use aoc_2020::{
    day_01, day_11, day_12, day_13, day_15, day_16, day_17, day_18, day_19, day_21, day_22,
};
use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();
    match args.len() {
        2 => solve_day(
            args[1]
                .trim()
                .parse()
                .expect("You must enter a number between 1 and 25."),
        ),
        _ => panic!("You must enter a number between 1 and 25."),
    }
}

fn solve_day(day: i32) {
    let fn_day = match day {
        1 => day_01::day_01,
        2 => day_02::day_02,
        3 => day_03::day_03,
        4 => day_04::day_04,
        5 => day_05::day_05,
        6 => day_06::day_06,
        7 => day_07::day_07,
        8 => day_08::day_08,
        9 => day_09::day_09,
        10 => day_10::day_10,
        11 => day_11::day_11,
        12 => day_12::day_12,
        13 => day_13::day_13,
        14 => unimplemented!(),
        15 => day_15::day_15,
        16 => day_16::day_16,
        17 => day_17::day_17,
        18 => day_18::day_18,
        19 => day_19::day_19,
        20 => unimplemented!(),
        21 => day_21::day_21,
        22 => day_22::day_22,
        23 => unimplemented!(),
        24 => unimplemented!(),
        25 => unimplemented!(),
        _ => panic!("{} is not a valid value", day),
    };
    println!("# Processing Day {} :", day);
    fn_day()
}
