use crate::utils::io::get_file;
use std::collections::HashSet;

use lazy_static::lazy_static;
use regex::Regex;

lazy_static! {
    static ref ROBOT_REGEX: Regex = Regex::new(r"p=(-?\d+),(-?\d+)\s+v=(-?\d+),(-?\d+)").unwrap();
}

#[derive(Debug, Copy, Clone)]
struct Point {
    x: i64,
    y: i64,
}

#[derive(Debug, Copy, Clone)]
struct Robot {
    position: Point,
    velocity: Point,
}

pub fn day_14() {
    let input = get_input("./src/day_14/input.txt");
    let map_size = Point { x: 101, y: 103 };
    let solution_1 = part_one(&input, map_size);
    println!("\t- Solution 1 is : {solution_1}");

    // let solution_2 = part_two(&input, map_size);
    // println!("\t- Solution 2 is : {solution_2}");
}

fn get_input(file_name: &str) -> Vec<Robot> {
    let data = get_file(file_name);
    let mut robots = Vec::new();

    for line in data.lines() {
        if let Some(caps) = ROBOT_REGEX.captures(line) {
            let x = caps[1].parse::<i64>().unwrap();
            let y = caps[2].parse::<i64>().unwrap();
            let vx = caps[3].parse::<i64>().unwrap();
            let vy = caps[4].parse::<i64>().unwrap();

            let robot = Robot {
                position: Point { x, y },
                velocity: Point { x: vx, y: vy },
            };

            robots.push(robot);
        }
    }

    robots
}

fn elapse_one_second(robot: &Robot, grid_size: Point) -> Robot {
    let new_x = (robot.position.x + robot.velocity.x).rem_euclid(grid_size.x);
    let new_y = (robot.position.y + robot.velocity.y).rem_euclid(grid_size.y);
    let new_position = Point { x: new_x, y: new_y };

    Robot {
        position: new_position,
        velocity: robot.velocity,
    }
}

fn get_safety_factor(robots: &[Robot], grid_size: Point) -> usize {
    let center_x = grid_size.x / 2;
    let center_y = grid_size.y / 2;
    let mut quadrant_counts = [0, 0, 0, 0];

    for robot in robots.iter() {
        let x = robot.position.x;
        let y = robot.position.y;

        if x == center_x || y == center_y {
            continue;
        }

        if x > center_x && y > center_y {
            quadrant_counts[0] += 1;
        } else if x < center_x && y > center_y {
            quadrant_counts[1] += 1;
        } else if x < center_x && y < center_y {
            quadrant_counts[2] += 1;
        } else if x > center_x && y < center_y {
            quadrant_counts[3] += 1;
        }
    }
    quadrant_counts.iter().product()
}

fn part_one(robots: &[Robot], grid_size: Point) -> usize {
    let mut robots = robots.to_vec();
    for _second in 0..100 {
        robots = robots
            .iter()
            .map(|robot| elapse_one_second(robot, grid_size))
            .collect();
    }
    get_safety_factor(&robots, grid_size)
}

#[allow(dead_code)]
fn part_two(robots: &[Robot], grid_size: Point) -> usize {
    let mut robots = robots.to_vec();
    let mut seconds = 0; // Starting from 0 seconds

    loop {
        let mut buffer = String::new();
        // Clear the screen
        buffer.push_str("\x1B[2J\x1B[1;1H");
        buffer.push_str(&format!("Seconds: {}\n", seconds));

        let robot_positions: HashSet<(i64, i64)> = robots
            .iter()
            .map(|r| (r.position.x, r.position.y))
            .collect();

        for y in 0..grid_size.y {
            for x in 0..grid_size.x {
                if robot_positions.contains(&(x, y)) {
                    buffer.push('■');
                } else {
                    buffer.push(' ');
                }
            }
            buffer.push('\n');
        }

        // Print the entire buffer at once
        print!("{}", buffer);

        // Update the positions of all robots for the next second
        robots = robots
            .iter()
            .map(|robot| elapse_one_second(robot, grid_size))
            .collect();

        seconds += 1;
        if seconds > 8050 {
            return seconds;
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = get_input("./src/day_14/input_example.txt");
        assert_eq!(215987200, part_one(&input, Point { x: 101, y: 103 }));
    }
}
