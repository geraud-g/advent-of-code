use crate::utils::{get_file, LINE_ENDING};
use itertools::Itertools;
use lazy_static::lazy_static;
use regex::Regex;

lazy_static! {
    static ref REGEX_VALID_HEIGHT: Regex = Regex::new(r"^(\d+)\s*(in|cm)$").unwrap();
    static ref REGEX_VALID_HAIR_COLOR: Regex = Regex::new(r"^#[a-zA-Z0-9]{6}$").unwrap();
    static ref REGEX_VALID_PASSPORT_ID: Regex = Regex::new(r"^\d{9}$").unwrap();
}

pub fn day_04() {
    let input = get_input();

    let solution_a = input.iter().filter(|p| p.is_valid_part_a()).count();
    println!("Part A: {}", solution_a);

    let solution_b = input.iter().filter(|p| p.is_valid_part_b()).count();
    println!("Part B: {}", solution_b);
}

fn get_input() -> Vec<Passport> {
    let data = get_file("./inputs/day_04.txt");
    let mut passports = vec![];

    for raw_passport in data.split(&format!("{}{}", LINE_ENDING, LINE_ENDING)) {
        passports.push(get_passport(raw_passport));
    }
    passports
}

fn get_passport(input: &str) -> Passport {
    let mut new_passport = Passport::default();

    for line in input.split_whitespace() {
        let split_line = line.split(':').collect_vec();
        assert_eq!(split_line.len(), 2);
        match split_line[0] {
            "byr" => new_passport.byr = Some(split_line[1].to_string()),
            "iyr" => new_passport.iyr = Some(split_line[1].to_string()),
            "eyr" => new_passport.eyr = Some(split_line[1].to_string()),
            "hgt" => new_passport.hgt = Some(split_line[1].to_string()),
            "hcl" => new_passport.hcl = Some(split_line[1].to_string()),
            "ecl" => new_passport.ecl = Some(split_line[1].to_string()),
            "pid" => new_passport.pid = Some(split_line[1].to_string()),
            "cid" => new_passport.cid = Some(split_line[1].to_string()),
            _ => panic!("Wrong value for passport: {}", split_line[0]),
        }
    }
    new_passport
}

#[derive(Default)]
struct Passport {
    byr: Option<String>,
    iyr: Option<String>,
    eyr: Option<String>,
    hgt: Option<String>,
    hcl: Option<String>,
    ecl: Option<String>,
    pid: Option<String>,
    cid: Option<String>,
}

impl Passport {
    pub fn is_valid_part_a(&self) -> bool {
        self.byr.is_some()
            && self.iyr.is_some()
            && self.eyr.is_some()
            && self.hgt.is_some()
            && self.hcl.is_some()
            && self.ecl.is_some()
            && self.pid.is_some()
    }

    pub fn is_valid_part_b(&self) -> bool {
        self.is_valid_part_a()
            && is_valid_digit(self.byr.as_ref().unwrap(), 1920, 2002)
            && is_valid_digit(self.iyr.as_ref().unwrap(), 2010, 2020)
            && is_valid_digit(self.eyr.as_ref().unwrap(), 2020, 2030)
            && self.valid_height()
            && self.valid_hair_color()
            && self.valid_eye_color()
            && self.valid_passport_id()
    }

    fn valid_height(&self) -> bool {
        if let Some(result) = REGEX_VALID_HEIGHT.captures(self.hgt.as_ref().unwrap()) {
            match &result[2] {
                "in" => is_valid_digit(&result[1], 59, 76),
                "cm" => is_valid_digit(&result[1], 150, 193),
                _ => false,
            }
        } else {
            false
        }
    }

    fn valid_hair_color(&self) -> bool {
        REGEX_VALID_HAIR_COLOR.is_match(self.hcl.as_ref().unwrap())
    }

    fn valid_eye_color(&self) -> bool {
        match &self.ecl.as_ref().unwrap()[..] {
            "amb" | "blu" | "brn" | "gry" | "grn" | "hzl" | "oth" => true,
            _ => false,
        }
    }

    fn valid_passport_id(&self) -> bool {
        REGEX_VALID_PASSPORT_ID.is_match(&self.pid.as_ref().unwrap())
    }
}

fn is_valid_digit(value: &str, min_value: i32, max_value: i32) -> bool {
    match value.parse::<i32>() {
        Ok(value) => value >= min_value && value <= max_value,
        _ => false,
    }
}
