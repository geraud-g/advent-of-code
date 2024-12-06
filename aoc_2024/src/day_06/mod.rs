use crate::utils::io::get_file;
use std::collections::HashSet;

#[derive(Debug, Clone, Copy)]
enum Direction {
    Up,
    Down,
    Left,
    Right,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
struct Point {
    x: usize,
    y: usize,
}

#[derive(Debug, Clone)]
struct Guard {
    direction: Direction,
    position: Point,
}

impl Guard {
    fn move_one_step(&mut self, obstacles: &[Vec<bool>]) -> Result<(), ()> {
        match self.direction {
            Direction::Up => {
                if self.position.y == 0 {
                    return Err(());
                }
                if obstacles[self.position.y - 1][self.position.x] {
                    self.rotate_right();
                } else {
                    self.position.y -= 1;
                }
            }
            Direction::Down => {
                if self.position.y == (obstacles.len()) - 1 {
                    return Err(());
                }
                if obstacles[self.position.y + 1][self.position.x] {
                    self.rotate_right();
                } else {
                    self.position.y += 1;
                }
            }
            Direction::Left => {
                if self.position.x == 0 {
                    return Err(());
                }
                if obstacles[self.position.y][self.position.x - 1] {
                    self.rotate_right();
                } else {
                    self.position.x -= 1;
                }
            }
            Direction::Right => {
                if self.position.x == obstacles[0].len() {
                    return Err(());
                }
                if obstacles[self.position.y][self.position.x + 1] {
                    self.rotate_right();
                } else {
                    self.position.x += 1;
                }
            }
        }
        Ok(())
    }

    fn rotate_right(&mut self) {
        self.direction = match self.direction {
            Direction::Up => Direction::Right,
            Direction::Right => Direction::Down,
            Direction::Down => Direction::Left,
            Direction::Left => Direction::Up,
        }
    }
}

pub fn day_06() {
    let (guard, obstacles) = get_input("./src/day_06/input.txt");

    let solution_1 = part_one(&guard, &obstacles);
    println!("\t- Solution 1 is : {solution_1}");

    // let solution_2 = part_two(&inputs);
    // println!("\t- Solution 2 is : {solution_2}");
}

fn get_input(file_name: &str) -> (Guard, Vec<Vec<bool>>) {
    let file = get_file(file_name);
    let mut obstacles = Vec::new();

    let mut guard = Guard {
        direction: Direction::Up,
        position: Point { x: 0, y: 0 },
    };

    for (y, line) in file.lines().enumerate() {
        let mut obstacles_line = Vec::new();
        for (x, value) in line.chars().enumerate() {
            if value == '#' {
                obstacles_line.push(true);
            } else {
                obstacles_line.push(false);
                if value == '^' {
                    guard.position = Point { x, y };
                }
            }
        }
        obstacles.push(obstacles_line);
    }

    (guard, obstacles)
}

fn part_one(guard: &Guard, obstacles: &[Vec<bool>]) -> usize {
    let mut mut_guard = guard.clone();
    let mut hash_set = HashSet::new();
    hash_set.insert(mut_guard.position);

    while mut_guard.move_one_step(obstacles).is_ok() {
        hash_set.insert(mut_guard.position);
    }

    hash_set.len()
}

fn part_two() {}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let (rules, update) = get_input("./src/day_06/input_example.txt");
        assert_eq!(41, part_one(&rules, &update));
    }

    // #[test]
    // fn test_part_two() {
    //     let (rules, update) = get_input("./src/day_05/input_example.txt");
    //     assert_eq!(123, part_two(&rules, &update));
    // }
}
