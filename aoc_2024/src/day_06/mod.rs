use crate::utils::io::get_file;
use std::collections::HashSet;

#[derive(Debug, Clone, Copy, Eq, PartialEq, Hash)]
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

#[derive(Debug, Clone, Eq, PartialEq)]
struct Guard {
    direction: Direction,
    position: Point,
}

impl Guard {
    fn get_next_position(&self, obstacles: &[Vec<bool>]) -> Option<Point> {
        let (new_y, new_x) = match self.direction {
            Direction::Up => (self.position.y.checked_sub(1), Some(self.position.x)),
            Direction::Down => (self.position.y.checked_add(1), Some(self.position.x)),
            Direction::Left => (Some(self.position.y), self.position.x.checked_sub(1)),
            Direction::Right => (Some(self.position.y), self.position.x.checked_add(1)),
        };

        // Now check if the coordinates are within bounds
        if let (Some(y), Some(x)) = (new_y, new_x) {
            if y < obstacles.len() && x < obstacles[0].len() {
                return Some(Point { x, y });
            }
        }
        None
    }

    fn move_one_step(&mut self, obstacles: &[Vec<bool>]) -> Result<(), ()> {
        let new_position = self.get_next_position(obstacles);
        if let Some(new_position) = new_position {
            if obstacles[new_position.y][new_position.x] {
                self.rotate_right();
            } else {
                self.position = new_position;
            }
            Ok(())
        } else {
            Err(())
        }
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

    let solution_2 = part_two(&guard, &obstacles);
    println!("\t- Solution 2 is : {solution_2}");
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

fn does_loop(mut_guard: &Guard, obstacles: &[Vec<bool>], _initial_guard: &Guard) -> bool {
    let mut guard_copy = mut_guard.clone();
    let mut visited = HashSet::new();
    visited.insert((guard_copy.position, guard_copy.direction));

    while guard_copy.move_one_step(obstacles).is_ok() {
        let state = (guard_copy.position, guard_copy.direction);
        if !visited.insert(state) {
            return true;
        }
    }
    false
}

fn part_two(guard: &Guard, obstacles: &[Vec<bool>]) -> usize {
    let mut loop_count = 0;
    let mut visited_positions = HashSet::new();
    let mut guard_copy = guard.clone();

    while guard_copy.move_one_step(obstacles).is_ok() {
        visited_positions.insert(guard_copy.position);
    }

    // Now, try placing an obstacle in each visited position that isn't the start
    let mut new_obstacles = obstacles.to_vec();
    for pos in &visited_positions {
        if *pos == guard.position {
            // Skip starting position
            continue;
        }
        if !obstacles[pos.y][pos.x] {
            // Temporarily place an obstacle
            new_obstacles[pos.y][pos.x] = true;
            if does_loop(&guard, &new_obstacles, &guard) {
                loop_count += 1;
            }
            new_obstacles[pos.y][pos.x] = false;
        }
    }

    loop_count
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let (rules, update) = get_input("./src/day_06/input_example.txt");
        assert_eq!(41, part_one(&rules, &update));
    }

    #[test]
    fn test_part_two() {
        let (rules, update) = get_input("./src/day_06/input_example.txt");
        assert_eq!(6, part_two(&rules, &update));
    }
}
