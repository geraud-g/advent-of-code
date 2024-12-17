use crate::utils::io::get_file;
use aoc_2024::utils::io::LINE_ENDING;
use std::cmp::Ordering;
use std::collections::{BinaryHeap, HashMap, HashSet};

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

// fn part_one(reindeer: &Reindeer, obstacles: &Vec<Vec<bool>>, exit: &Point) -> usize {
//     0
// }

fn part_one(reindeer: &Reindeer, obstacles: &Vec<Vec<bool>>, exit: &Point) -> usize {
    let mut dist: HashMap<(Point, Direction), usize> = HashMap::new();
    let mut heap = BinaryHeap::new();

    let initial_state = State {
        cost: 0,
        position: reindeer.position,
        direction: reindeer.direction,
    };

    heap.push(initial_state.clone());
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

        let actions = vec!["move", "turn_left", "turn_right"];

        for action in actions {
            let mut next_position = current_state.position;
            let mut next_direction = current_state.direction;
            let mut next_cost = current_state.cost;

            match action {
                "move" => {
                    let maybe_next = match next_direction {
                        Direction::Up => {
                            if next_position.y > 0 {
                                Some(Point {
                                    x: next_position.x,
                                    y: next_position.y - 1,
                                })
                            } else {
                                None
                            }
                        }
                        Direction::Down => {
                            if next_position.y + 1 < obstacles.len() {
                                Some(Point {
                                    x: next_position.x,
                                    y: next_position.y + 1,
                                })
                            } else {
                                None
                            }
                        }
                        Direction::Left => {
                            if next_position.x > 0 {
                                Some(Point {
                                    x: next_position.x - 1,
                                    y: next_position.y,
                                })
                            } else {
                                None
                            }
                        }
                        Direction::Right => {
                            if next_position.x + 1 < obstacles[0].len() {
                                Some(Point {
                                    x: next_position.x + 1,
                                    y: next_position.y,
                                })
                            } else {
                                None
                            }
                        }
                    };

                    if let Some(new_pos) = maybe_next {
                        if !obstacles[new_pos.y][new_pos.x] {
                            next_position = new_pos;
                            next_cost += 1;
                        } else {
                            // Si la case est un mur, cette action n'est pas possible
                            continue;
                        }
                    } else {
                        // Position en dehors des limites, ignorer
                        continue;
                    }
                }
                "turn_left" => {
                    // Tourner à gauche
                    next_direction = match next_direction {
                        Direction::Up => Direction::Left,
                        Direction::Left => Direction::Down,
                        Direction::Down => Direction::Right,
                        Direction::Right => Direction::Up,
                    };
                    next_cost += 1000;
                }
                "turn_right" => {
                    // Tourner à droite
                    next_direction = match next_direction {
                        Direction::Up => Direction::Right,
                        Direction::Right => Direction::Down,
                        Direction::Down => Direction::Left,
                        Direction::Left => Direction::Up,
                    };
                    next_cost += 1000;
                }
                _ => {}
            }

            let next_state = State {
                cost: next_cost,
                position: next_position,
                direction: next_direction,
            };

            // Vérifier si ce chemin est meilleur
            let key = (next_state.position, next_state.direction);
            if next_cost < *dist.get(&key).unwrap_or(&usize::MAX) {
                dist.insert(key, next_cost);
                heap.push(next_state);
            }
        }
    }

    // Si la sortie n'est pas atteignable
    usize::MAX
}
#[cfg(test)]
mod tests {
    use super::*;

    // #[test]
    // fn test_part_one() {
    //     let (map, directions, robot) = get_input("./src/day_16/input_example.txt");
    //     assert_eq!(10092, part_one(&map, &directions, &robot));
    // }

    // #[test]
    // fn test_part_two() {
    //     let input = get_input("./src/day_16/input_example.txt");
    //     assert_eq!(875318608908, part_two(&input));
    // }
}
