use crate::utils::io::get_file;
use std::collections::HashSet;

pub fn day_12() {
    let input = get_input("./src/day_12/input.txt");

    let solution_1 = part_one(&input);
    println!("\t- Solution 1 is : {solution_1}");

    // let solution_2 = part_two(&input);
    // println!("\t- Solution 2 is : {solution_2}");
}

fn get_input(file_name: &str) -> Vec<Vec<char>> {
    get_file(file_name)
        .lines()
        .map(|line| line.chars().collect())
        .collect()
}

fn flood_fill(
    map: &[Vec<char>],
    visited: &mut HashSet<(usize, usize)>,
    current_value: char,
    x: usize,
    y: usize,
) -> (usize, usize) {
    let mut count = 1;
    let mut perimeter = 0;
    visited.insert((y, x));

    let directions = [
        (1, 0),  // Right
        (-1, 0), // Left
        (0, 1),  // Down
        (0, -1), // Up
    ];

    for &(dx, dy) in &directions {
        let new_x_isize = x as isize + dx;
        let new_y_isize = y as isize + dy;

        let new_x = new_x_isize as usize;
        let new_y = new_y_isize as usize;

        if new_x_isize < 0
            || new_y_isize < 0
            || new_y >= map.len()
            || new_x >= map[new_y].len()
            || map[new_y][new_x] != current_value
        {
            perimeter += 1;
            continue;
        }
        if visited.contains(&(new_y, new_x)) {
            continue;
        }
        let (c, p) = flood_fill(map, visited, current_value, new_x, new_y);
        count += c;
        perimeter += p;
    }

    (count, perimeter)
}

fn part_one(map: &[Vec<char>]) -> usize {
    let mut total = 0;
    let mut visited = HashSet::new();

    for y in 0..map.len() {
        for x in 0..map[y].len() {
            if !visited.contains(&(y, x)) {
                let (count, perimeter) = flood_fill(map, &mut visited, map[y][x], x, y);
                total += count * perimeter;
            }
        }
    }
    total
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = get_input("./src/day_12/input_example.txt");
        assert_eq!(1930, part_one(&input));
    }
    //
    // #[test]
    // fn test_part_two() {
    //     let input = get_input("./src/day_12/input_example.txt");
    //     assert_eq!(1206, part_two(&input));
    // }
}
