use crate::utils::io::get_file;
use std::collections::{HashSet, VecDeque};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
struct Point {
    x: usize,
    y: usize,
}

pub fn day_10() {
    let input = get_input("./src/day_10/input.txt");

    let solution_1 = part_one(&input);
    println!("\t- Solution 1 is : {solution_1}");

    let solution_2 = part_two(&input);
    println!("\t- Solution 2 is : {solution_2}");
}

fn get_input(file_name: &str) -> Vec<Vec<u8>> {
    let mut topographic_map = vec![];
    for line in get_file(file_name).lines() {
        let row = line
            .chars()
            .map(|c| c.to_digit(10).unwrap() as u8)
            .collect();
        topographic_map.push(row);
    }
    topographic_map
}

fn get_trailheads(topographic_map: &[Vec<u8>]) -> Vec<Point> {
    let mut trailheads = vec![];
    for (y, row) in topographic_map.iter().enumerate() {
        for (x, val) in row.iter().enumerate() {
            if *val == 0 {
                trailheads.push(Point { y, x });
            }
        }
    }
    trailheads
}

/// Returns the neighbors of a given point,
/// if they are in the map, and have a value of current_height + 1.
fn get_neighbors(topographic_map: &[Vec<u8>], point: Point) -> Vec<Point> {
    let mut neighbors = Vec::new();
    let max_x = topographic_map.len();
    let max_y = if max_x > 0 {
        topographic_map[0].len()
    } else {
        0
    };

    let current_height = topographic_map[point.y][point.x];
    if current_height == 9 {
        return neighbors; // We reached the maximum height so we stop here
    }

    // UP, DOWN, LEFT, RIGHT
    if point.x > 0 {
        let neighbor = Point {
            x: point.x - 1,
            y: point.y,
        };
        if topographic_map[neighbor.y][neighbor.x] == current_height + 1 {
            neighbors.push(neighbor);
        }
    }
    if point.x + 1 < max_x {
        let neighbor = Point {
            x: point.x + 1,
            y: point.y,
        };
        if topographic_map[neighbor.y][neighbor.x] == current_height + 1 {
            neighbors.push(neighbor);
        }
    }
    if point.y > 0 {
        let neighbor = Point {
            x: point.x,
            y: point.y - 1,
        };
        if topographic_map[neighbor.y][neighbor.x] == current_height + 1 {
            neighbors.push(neighbor);
        }
    }
    if point.y + 1 < max_y {
        let neighbor = Point {
            x: point.x,
            y: point.y + 1,
        };
        if topographic_map[neighbor.y][neighbor.x] == current_height + 1 {
            neighbors.push(neighbor);
        }
    }

    neighbors
}

/// Returns the number of hiking trails that can be taken from a given starting point.
/// Under the hood, this is a BFS algorithm.
fn get_hiking_trails_nbr(topographic_map: &[Vec<u8>], starting_point: &Point) -> usize {
    let mut frontier = VecDeque::new();
    let mut visited = HashSet::new();
    frontier.push_back(*starting_point);

    while let Some(current_node) = frontier.pop_front() {
        for neighbor in get_neighbors(topographic_map, current_node) {
            if !visited.contains(&neighbor) {
                visited.insert(neighbor);
                frontier.push_back(neighbor);
            }
        }
    }
    visited
        .iter()
        .filter(|point| topographic_map[point.y][point.x] == 9)
        .count()
}

fn part_one(topographic_map: &[Vec<u8>]) -> usize {
    get_trailheads(topographic_map)
        .iter()
        .map(|trailhead| get_hiking_trails_nbr(topographic_map, trailhead))
        .sum()
}

fn dfs(map: &[Vec<u8>], point: &Point, visited: &mut HashSet<Point>) -> usize {
    let mut paths = 0;
    for neighbor in get_neighbors(map, *point) {
        let neighbor_height = map[neighbor.y][neighbor.x];
        if !visited.contains(&neighbor) {
            if neighbor_height == 9 {
                paths += 1;
            } else {
                visited.insert(neighbor);
                paths += dfs(map, &neighbor, visited);
                visited.remove(&neighbor);
            }
        }
    }
    paths
}

fn get_hiking_trails_rating(topographic_map: &[Vec<u8>], starting_point: &Point) -> usize {
    let mut visited = HashSet::new();
    visited.insert(*starting_point);
    dfs(topographic_map, starting_point, &mut visited)
}

fn part_two(topographic_map: &[Vec<u8>]) -> usize {
    get_trailheads(topographic_map)
        .iter()
        .map(|trailhead| get_hiking_trails_rating(topographic_map, trailhead))
        .sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = get_input("./src/day_10/input_example.txt");
        assert_eq!(36, part_one(&input));
    }

    #[test]
    fn test_part_two() {
        let input = get_input("./src/day_10/input_example.txt");
        assert_eq!(81, part_two(&input));
    }
}
