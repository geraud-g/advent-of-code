use crate::utils::io::get_file;
use aoc_2024::utils::io::LINE_ENDING;
use std::collections::HashSet;

#[derive(Debug, Eq, PartialEq, Hash, Copy, Clone)]
struct Point {
    x: usize,
    y: usize,
}

#[derive(Debug)]
enum Direction {
    Up,
    Down,
    Left,
    Right,
}

impl Direction {
    fn get_new_point(&self, point: &Point) -> Point {
        match self {
            Direction::Up => Point {
                x: point.x,
                y: point.y - 1,
            },
            Direction::Down => Point {
                x: point.x,
                y: point.y + 1,
            },
            Direction::Left => Point {
                x: point.x - 1,
                y: point.y,
            },
            Direction::Right => Point {
                x: point.x + 1,
                y: point.y,
            },
        }
    }
}

#[derive(Debug, Clone)]
struct Map {
    walls: HashSet<Point>,
    boxes: HashSet<Point>,
}

impl Map {
    fn is_wall(&self, point: &Point) -> bool {
        self.walls.contains(point)
    }

    fn is_box(&self, point: &Point) -> bool {
        self.boxes.contains(point)
    }

    fn move_robot(&mut self, robot: &Point, direction: &Direction) -> Option<Point> {
        let mut new_robot = direction.get_new_point(robot);
        if self.is_wall(&new_robot) {
            return None;
        }

        // Collect all consecutive boxes in the direction of movement
        let mut boxes_to_move = Vec::new();
        while self.is_box(&new_robot) {
            boxes_to_move.push(new_robot);
            new_robot = direction.get_new_point(&new_robot);
            if self.is_wall(&new_robot) {
                return None;
            }
        }

        // At this point, new_robot is the position after the last box
        // Check if this position is free
        if self.is_box(&new_robot) {
            // Another box is blocking the way; move is not possible
            return None;
        }
        // Move all boxes one step in the specified direction
        for &box_pos in boxes_to_move.iter().rev() {
            let new_box_pos = direction.get_new_point(&box_pos);
            // TODO : REMOVE ?
            // Double-check to prevent overlapping boxes
            if self.is_wall(&new_box_pos) || self.is_box(&new_box_pos) {
                return None;
            }
            self.boxes.remove(&box_pos);
            self.boxes.insert(new_box_pos);
        }

        Some(direction.get_new_point(robot))
    }
}

pub fn day_15() {
    let (map, directions, robot) = get_input("./src/day_15/input.txt");

    let solution_1 = part_one(&map, &directions, &robot);
    println!("\t- Solution 1 is : {solution_1}");

    // let solution_2 = part_two(&input);
    // println!("\t- Solution 2 is : {solution_2}");
}

fn get_input(file_name: &str) -> (Map, Vec<Direction>, Point) {
    let file = get_file(file_name);
    let split_separator = format!("{}{}", LINE_ENDING, LINE_ENDING);
    let sections: Vec<&str> = file.split(&split_separator).collect();
    let mut robot = Point { x: 0, y: 0 };
    let mut map = Map {
        walls: HashSet::new(),
        boxes: HashSet::new(),
    };
    let mut directions = vec![];

    // Map & Robot
    for (y, line) in sections[0].lines().enumerate() {
        for (x, c) in line.chars().enumerate() {
            let point = Point { x, y };
            match c {
                '#' => {
                    map.walls.insert(point);
                }
                'O' => {
                    map.boxes.insert(point);
                }
                '@' => robot = point,
                _ => {}
            };
        }
    }

    // Directions
    for char in sections[1].chars() {
        let direction = match char {
            '^' => Direction::Up,
            'v' => Direction::Down,
            '<' => Direction::Left,
            '>' => Direction::Right,
            '\n' | ' ' => continue,
            _ => panic!("Cannot get direction from value {}", char),
        };
        directions.push(direction);
    }
    (map, directions, robot)
}

fn part_one(map: &Map, directions: &Vec<Direction>, robot: &Point) -> usize {
    let mut map = map.clone();
    let mut robot = *robot;

    for direction in directions {
        if let Some(new_robot) = map.move_robot(&robot, direction) {
            robot = new_robot;
        }
    }
    map.boxes.iter().map(|point| point.y * 100 + point.x).sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let (map, directions, robot) = get_input("./src/day_15/input_example.txt");
        assert_eq!(10092, part_one(&map, &directions, &robot));
    }

    // #[test]
    // fn test_part_two() {
    //     let input = get_input("./src/day_15/input_example.txt");
    //     assert_eq!(875318608908, part_two(&input));
    // }
}
