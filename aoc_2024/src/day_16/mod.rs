use crate::utils::io::get_file;
use std::cmp::Ordering;
use std::collections::{BinaryHeap, HashMap};

#[derive(Debug, Clone, Copy, Eq, PartialEq, Hash, Ord, PartialOrd)]
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
#[derive(Debug, Eq, PartialEq, Clone, Copy)]
struct State {
    cost: usize,
    position: Point,
    direction: Direction,
}

impl Ord for State {
    fn cmp(&self, other: &Self) -> Ordering {
        other
            .cost
            .cmp(&self.cost)
            .then_with(|| self.position.y.cmp(&other.position.y))
            .then_with(|| self.position.x.cmp(&other.position.x))
            .then_with(|| self.direction.cmp(&other.direction))
    }
}

impl PartialOrd for State {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

#[derive(Debug, Clone, Eq, PartialEq)]
struct Reindeer {
    direction: Direction,
    position: Point,
}

impl Reindeer {
    fn move_if_possible(
        &self,
        obstacles: &[Vec<bool>],
        from_position: Point,
        from_direction: Direction,
    ) -> Option<Point> {
        let (new_y, new_x) = match from_direction {
            Direction::Up => (from_position.y.checked_sub(1), Some(from_position.x)),
            Direction::Down => (from_position.y.checked_add(1), Some(from_position.x)),
            Direction::Left => (Some(from_position.y), from_position.x.checked_sub(1)),
            Direction::Right => (Some(from_position.y), from_position.x.checked_add(1)),
        };

        if let (Some(y), Some(x)) = (new_y, new_x) {
            if y < obstacles.len() && x < obstacles[0].len() && !obstacles[y][x] {
                return Some(Point { x, y });
            }
        }
        None
    }
}

pub fn day_16() {
    let (reindeer, obstacles, exit) = get_input("./src/day_16/input.txt");

    let solution_1 = part_one(&reindeer, &obstacles, &exit);
    println!("\t- Solution 1 is : {solution_1}");

    // let solution_2 = part_two(&input);
    // println!("\t- Solution 2 is : {solution_2}");
}

fn get_input(file_name: &str) -> (Reindeer, Vec<Vec<bool>>, Point) {
    let file = get_file(file_name);
    let mut obstacles: Vec<Vec<bool>> = Vec::new();
    let mut start_position: Option<Point> = None;
    let mut end_position: Option<Point> = None;

    for (y, line) in file.lines().enumerate() {
        let mut row: Vec<bool> = Vec::new();
        for (x, ch) in line.chars().enumerate() {
            match ch {
                '#' => {
                    row.push(true);
                }
                'S' => {
                    start_position = Some(Point { x, y });
                    row.push(false);
                }
                'E' => {
                    end_position = Some(Point { x, y });
                    row.push(false);
                }
                '.' => {
                    row.push(false);
                }
                _ => {
                    row.push(false);
                }
            }
        }
        obstacles.push(row);
    }

    let start = start_position.unwrap();
    let end = end_position.unwrap();

    let reindeer = Reindeer {
        direction: Direction::Right,
        position: start,
    };

    (reindeer, obstacles, end)
}

enum Action {
    Move,
    TurnLeft,
    TurnRight,
}

const ACTIONS: [Action; 3] = [Action::Move, Action::TurnLeft, Action::TurnRight];

fn part_one(reindeer: &Reindeer, obstacles: &[Vec<bool>], exit: &Point) -> usize {
    let mut dist: HashMap<(Point, Direction), usize> = HashMap::new();
    let mut heap = BinaryHeap::new();

    let initial_state = State {
        cost: 0,
        position: reindeer.position,
        direction: reindeer.direction,
    };

    heap.push(initial_state);
    dist.insert((initial_state.position, initial_state.direction), 0);

    while let Some(current_state) = heap.pop() {
        if current_state.position == *exit {
            return current_state.cost;
        }

        if let Some(&current_dist) = dist.get(&(current_state.position, current_state.direction)) {
            if current_state.cost > current_dist {
                continue;
            }
        }

        for action in ACTIONS.iter() {
            let mut next_position = current_state.position;
            let mut next_direction = current_state.direction;
            let mut next_cost = current_state.cost;

            match action {
                Action::Move => {
                    if let Some(new_pos) = reindeer.move_if_possible(
                        obstacles,
                        current_state.position,
                        current_state.direction,
                    ) {
                        next_position = new_pos;
                        next_cost += 1;
                    }
                }
                Action::TurnLeft => {
                    next_direction = match next_direction {
                        Direction::Up => Direction::Left,
                        Direction::Left => Direction::Down,
                        Direction::Down => Direction::Right,
                        Direction::Right => Direction::Up,
                    };
                    next_cost += 1000;
                }
                Action::TurnRight => {
                    next_direction = match next_direction {
                        Direction::Up => Direction::Right,
                        Direction::Right => Direction::Down,
                        Direction::Down => Direction::Left,
                        Direction::Left => Direction::Up,
                    };
                    next_cost += 1000;
                }
            }

            let next_state = State {
                cost: next_cost,
                position: next_position,
                direction: next_direction,
            };

            let key = (next_state.position, next_state.direction);
            if next_cost < *dist.get(&key).unwrap_or(&usize::MAX) {
                dist.insert(key, next_cost);
                heap.push(next_state);
            }
        }
    }
    panic!("No solution found");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let (map, directions, robot) = get_input("./src/day_16/input_example.txt");
        assert_eq!(7036, part_one(&map, &directions, &robot));
    }

    // #[test]
    // fn test_part_two() {
    //     let input = get_input("./src/day_16/input_example.txt");
    //     assert_eq!(875318608908, part_two(&input));
    // }
}
