use crate::utils::get_file;
use ring_algorithm::chinese_remainder_theorem;


pub fn day_13() {
    let (earlier_bus, buses) = get_input();

    let solution_a = solve_part_a(earlier_bus, &buses);
    println!("Part A: {}", solution_a);


    let solution_b = solve_part_b(&buses);
    println!("Part B: {}", solution_b);
}


fn get_input() -> (i64, Vec<Bus>) {
    let input = get_file("./inputs/day_13.txt").lines().map(|l| l.to_string()).collect::<Vec<String>>();
    let earlier_bus = input[0].parse::<i64>().unwrap();
    let mut bus_list = vec![];
    for (idx, val) in input[1].split(',').enumerate() {
        if let Ok(res) = val.parse::<i64>() {
            bus_list.push(Bus { id: res, index: res - idx as i64 });
        }
    }
    (earlier_bus, bus_list)
}

fn solve_part_a(earlier_bus: i64, bus_list: &[Bus]) -> i64 {
    let mut current_time = earlier_bus;
    let mut minutes_waited = 0;

    loop {
        for bus in bus_list {
            if current_time % bus.id == 0 {
                return bus.id * minutes_waited;
            }
        }
        current_time += 1;
        minutes_waited += 1;
    }
}


fn solve_part_b(buses: &[Bus]) -> i64 {
    let numbers = buses.iter().map(|b| b.id).collect::<Vec<i64>>();
    let mods = buses.iter().map(|b| b.index).collect::<Vec<i64>>();

    chinese_remainder_theorem(&mods, &numbers).unwrap()
}


#[derive(Debug)]
struct Bus {
    id: i64,
    index: i64,
}