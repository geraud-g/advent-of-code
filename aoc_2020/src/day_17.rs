use std::collections::{HashMap, HashSet};
use crate::utils::get_file;


pub fn day_17() {
    let input = get_input();

    let solution_a = solve(&input, false);
    println!("Part A: {}", solution_a);

    let solution_b = solve(&input, true);
    println!("Part B: {}", solution_b);
}


fn get_input() -> HashMap<Point, bool> {
    let mut points = HashMap::new();
    for (y, line) in get_file("./inputs/day_17.txt").lines().enumerate() {
        for (x, value) in line.chars().enumerate() {
            let active = value.eq(&'#');
            points.insert(Point {
                x: x as i64,
                y: y as i64,
                z: 0,
                w: 0,
            }, active);
        }
    }
    points
}


fn solve(points: &HashMap<Point, bool>, part_b: bool) -> i64 {
    let mut points: HashMap<Point, bool> = points.clone();

    for _ in 0..6 {
        let points_to_eval: HashSet<Point> = points.iter()
            .filter(|(_, &is_active)| is_active)
            .map(|p| p.0.get_neighbours(part_b).to_vec())
            .flatten()
            .collect();

        points = points_to_eval.iter()
            .filter(|&p| is_active(part_b, p, &points))
            .map(|p| (*p, true))
            .collect();
    }
    points.values().filter(|&&p| p).count() as i64
}


fn is_active(part_b: bool, point: &Point, current_points: &HashMap<Point, bool>) -> bool {
    let state = current_points.get(point).unwrap_or(&false);
    let active_neighbours = point.get_neighbours(part_b).iter()
        .filter(|n| *current_points.get(n).unwrap_or(&false))
        .count();
    if *state {
        active_neighbours == 2 || active_neighbours == 3
    } else {
        active_neighbours == 3
    }
}


#[derive(Debug, Hash, Eq, PartialEq, Copy, Clone, Default)]
struct Point {
    x: i64,
    y: i64,
    z: i64,
    w: i64,
}


impl Point {
    fn get_neighbours(&self, part_b: bool) -> Box<[Point]> {
        if part_b {
            Box::new(self.get_neighbours_part_b())
        } else {
            Box::new(self.get_neighbours_part_a())
        }
    }

    fn get_neighbours_part_a(&self) -> [Point; 26] {
        let mut neighbours = [Point::default(); 26];
        let mut counter = 0;
        for z in 0..3 {
            for y in 0..3 {
                for x in 0..3 {
                    if z == 1 && y == 1 && x == 1 {
                        continue;
                    }
                    neighbours[counter].y = self.y + (y - 1);
                    neighbours[counter].x = self.x + (x - 1);
                    neighbours[counter].z = self.z + (z - 1);
                    counter += 1;
                }
            }
        }
        neighbours
    }

    fn get_neighbours_part_b(&self) -> [Point; 80] {
        let mut neighbours = [Point::default(); 80];
        let mut counter = 0;
        for w in 0..3 {
            for z in 0..3 {
                for y in 0..3 {
                    for x in 0..3 {
                        if z == 1 && y == 1 && x == 1 && w == 1 {
                            continue;
                        }
                        neighbours[counter].y = self.y + (y - 1);
                        neighbours[counter].x = self.x + (x - 1);
                        neighbours[counter].z = self.z + (z - 1);
                        neighbours[counter].w = self.w + (w - 1);
                        counter += 1;
                    }
                }
            }
        }
        neighbours
    }
}
