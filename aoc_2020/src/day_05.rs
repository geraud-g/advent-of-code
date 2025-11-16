use crate::utils::get_file;
use itertools::Itertools;


pub fn day_05() {
    let mut seat_ids = get_input().lines().map(|l| get_seat_id(l)).collect_vec();

    println!("Part A: {}", &seat_ids.iter().max().unwrap());

    println!("Part B: {}", find_my_seat(&mut seat_ids));
}


fn get_input() -> String {
    get_file("./inputs/day_05.txt")
}


fn get_seat_id(line: &str) -> u32 {
    let (row, col) = get_seat_row_col(line);
    row * 8 + col
}


fn get_seat_row_col(line: &str) -> (u32, u32) {
    let (mut min_row, mut max_row) = (0, 127);
    let (mut min_col, mut max_col) = (0, 7);

    for chr in line.chars() {
        match chr {
            'F' => { max_row = (min_row + max_row) / 2 }
            'B' => { min_row = (min_row + max_row) / 2 }
            'L' => { max_col = (min_col + max_col) / 2 }
            'R' => { min_col = (min_col + max_col) / 2 }
            _ => panic!("Wrong value: {}", chr)
        }
    }
    (max_row, max_col)
}


fn find_my_seat(seat_ids: &mut Vec<u32>) -> u32 {
    seat_ids.sort();

    for (&seat_a, &seat_b) in seat_ids.iter().tuple_windows() {
        if seat_b != seat_a + 1 {
            return seat_a + 1;
        }
    }
    unreachable!()
}
