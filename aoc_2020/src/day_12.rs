use crate::utils::get_file;


pub fn day_12() {
    let actions = get_input();

    let solution_a = solve_part_a(&actions);
    println!("Part A: {}", solution_a);
}


fn get_input() -> Vec<Action> {
    let mut actions = vec![];
    for line in get_file("./inputs/day_12.txt").lines() {
        let value = line[1..].parse().unwrap();
        let action = match &line[0..1] {
            "N" => Action::Direction(Direction::North(value)),
            "S" => Action::Direction(Direction::South(value)),
            "E" => Action::Direction(Direction::East(value)),
            "W" => Action::Direction(Direction::West(value)),
            "L" => Action::RelativeDirection(RelativeDirection::Left(value)),
            "R" => Action::RelativeDirection(RelativeDirection::Right(value)),
            "F" => Action::RelativeDirection(RelativeDirection::Forward(value)),
            _ => panic!("Wrong value: {}", &line)
        };
        actions.push(action)
    }
    actions
}


fn solve_part_a(actions: &[Action]) -> i32 {
    let mut ship = Ship { direction: Direction::East(0), position: Point { x: 0, y: 0 } };
    for action in actions {
        ship.perform_action(action);
    }
    ship.position.y.abs() + ship.position.x.abs()
}


enum Action {
    Direction(Direction),
    RelativeDirection(RelativeDirection),
}


#[derive(Debug)]
struct Ship {
    direction: Direction,
    position: Point<i32>,
}

impl Ship {
    fn perform_action(&mut self, action: &Action) {
        match action {
            Action::Direction(val) => self.eval_direction(val),
            Action::RelativeDirection(val) => self.eval_relative_direction(val)
        }
    }

    fn eval_direction(&mut self, direction: &Direction) {
        match direction {
            Direction::North(val) => { self.position.y -= val }
            Direction::South(val) => { self.position.y += val }
            Direction::East(val) => { self.position.x += val }
            Direction::West(val) => { self.position.x -= val }
        }
    }

    fn eval_relative_direction(&mut self, direction: &RelativeDirection) {
        match direction {
            RelativeDirection::Forward(val) => self.move_forward(*val),
            RelativeDirection::Left(val) => self.update_direction(-(val / 90)),
            RelativeDirection::Right(val) => self.update_direction(val / 90)
        };
    }

    fn move_forward(&mut self, value: i32) {
        let new_position = match self.direction {
            Direction::North(_) => Point { x: self.position.x, y: self.position.y - value },
            Direction::East(_) => Point { x: self.position.x + value, y: self.position.y },
            Direction::South(_) => Point { x: self.position.x, y: self.position.y + value },
            Direction::West(_) => Point { x: self.position.x - value, y: self.position.y }
        };
        self.position = new_position;
    }

    fn update_direction(&mut self, value: i32) {
        let directions = [
            Direction::North(0),
            Direction::East(0),
            Direction::South(0),
            Direction::West(0)
        ];
        let old_direction_idx = match self.direction {
            Direction::North(_) => 0,
            Direction::East(_) => 1,
            Direction::South(_) => 2,
            Direction::West(_) => 3
        };
        let new_index = neg_mod(old_direction_idx as i32 + value, 4);
        self.direction = directions[new_index as usize];
    }
}


#[derive(Debug, Copy, Clone)]
enum Direction {
    North(i32),
    South(i32),
    East(i32),
    West(i32),
}


#[derive(Debug)]
enum RelativeDirection {
    Left(i32),
    Right(i32),
    Forward(i32),
}


#[derive(Debug, Default)]
struct Point<T> {
    x: T,
    y: T,
}


fn neg_mod(x: i32, m: i32) -> i32 {
    (x % m + m) % m
}
