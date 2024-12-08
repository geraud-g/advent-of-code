use crate::utils::io::get_file;
use itertools::Itertools;
use std::collections::{HashMap, HashSet};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
struct Map {
    width: usize,
    height: usize,
}

// Greatest common divisor
fn gcd(a: isize, b: isize) -> isize {
    if b == 0 {
        a
    } else {
        gcd(b, a % b)
    }
}

impl Map {
    /// https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm
    /// Generates all the points that form a straight line between `start` and `end`,
    /// extending the line in both forward and backward directions until it goes out of bounds.
    fn trace_line(&self, start: Point, end: Point) -> HashSet<Point> {
        let mut line_positions = HashSet::new();

        // Calculate the change (difference) in the x and y directions
        let delta_x = end.x as isize - start.x as isize;
        let delta_y = end.y as isize - start.y as isize;

        // Determine the smallest "step" to move along the line.
        let step_factor = gcd(delta_x.abs(), delta_y.abs());
        let step_x = delta_x / step_factor;
        let step_y = delta_y / step_factor;

        // Extend the line forward from the starting point
        let mut forward_x = start.x as isize;
        let mut forward_y = start.y as isize;

        // Keep adding points in the forward direction while within bounds
        while forward_x >= 0
            && forward_x < self.width as isize
            && forward_y >= 0
            && forward_y < self.height as isize
        {
            line_positions.insert(Point {
                x: forward_x as usize,
                y: forward_y as usize,
            });
            forward_x += step_x;
            forward_y += step_y;
        }

        // Extend the line backward from the starting point
        let mut backward_x = start.x as isize - step_x;
        let mut backward_y = start.y as isize - step_y;

        // Keep adding points in the backward direction while within bounds
        while backward_x >= 0
            && backward_x < self.width as isize
            && backward_y >= 0
            && backward_y < self.height as isize
        {
            line_positions.insert(Point {
                x: backward_x as usize,
                y: backward_y as usize,
            });
            backward_x -= step_x;
            backward_y -= step_y;
        }

        line_positions
    }

    fn mirrored_point(&self, point_a: &Point, point_b: &Point) -> Option<Point> {
        let x = 2isize * (point_a.x as isize) - (point_b.x as isize);
        let y = 2isize * (point_a.y as isize) - (point_b.y as isize);

        if x >= 0 && x < self.width as isize && y >= 0 && y < self.height as isize {
            Some(Point {
                x: x as usize,
                y: y as usize,
            })
        } else {
            None
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
struct Point {
    x: usize,
    y: usize,
}

pub fn day_08() {
    let (map, antennas) = get_input("./src/day_08/input.txt");

    let solution_1 = part_one(&map, &antennas);
    println!("\t- Solution 1 is : {solution_1}");

    let solution_2 = part_two(&map, &antennas);
    println!("\t- Solution 2 is : {solution_2}");
}

fn get_input(file_name: &str) -> (Map, HashMap<char, Vec<Point>>) {
    let lines: Vec<_> = get_file(file_name)
        .lines()
        .map(|line| line.to_string())
        .collect();
    let height = lines.len();
    let width = lines.first().map_or(0, |line| line.len());

    let mut antennas: HashMap<char, Vec<Point>> = HashMap::new();

    for (y, line) in lines.iter().enumerate() {
        for (x, ch) in line.chars().enumerate() {
            if ch != '.' {
                antennas.entry(ch).or_default().push(Point { x, y });
            }
        }
    }

    (Map { width, height }, antennas)
}

fn part_one(map: &Map, antennas: &HashMap<char, Vec<Point>>) -> usize {
    let mut antinodes = HashSet::new();
    for points in antennas.values() {
        for (point_a, point_b) in points.iter().tuple_combinations() {
            if let Some(mirrored_point) = map.mirrored_point(point_a, point_b) {
                antinodes.insert(mirrored_point);
            }
            if let Some(mirrored_point) = map.mirrored_point(point_b, point_a) {
                antinodes.insert(mirrored_point);
            }
        }
    }
    antinodes.len()
}

fn part_two(map: &Map, antennas: &HashMap<char, Vec<Point>>) -> usize {
    let mut antinodes = HashSet::new();
    for (_antenna, points) in antennas.iter() {
        for (point_a, point_b) in points.iter().tuple_combinations() {
            for point in map.trace_line(*point_a, *point_b) {
                antinodes.insert(point);
            }
        }
    }
    antinodes.len()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let (map, antennas) = get_input("./src/day_08/input_example.txt");
        assert_eq!(14, part_one(&map, &antennas));
    }

    #[test]
    fn test_part_two() {
        let (map, antennas) = get_input("./src/day_08/input_example.txt");
        assert_eq!(34, part_two(&map, &antennas));
    }
}
