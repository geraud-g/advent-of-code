use crate::utils::get_file;
use regex::Regex;
use std::collections::{HashSet, HashMap};
use lazy_static::lazy_static;
use itertools::Itertools;

type Ingredient = String;
type Allergen = String;


lazy_static! {
    static ref REGEX_CONTAINS: Regex = Regex::new(r"(.*) \(contains (.*)\)").unwrap();
}


pub fn day_21() {
    let ingredients = get_input();

    let (solution_a, solution_b) = solve_part_a(&ingredients);
    println!("Part A: {}", solution_a);

    println!("Part B: {}", solution_b);
}


fn get_input() -> Vec<(HashSet<Ingredient>, HashSet<Allergen>)> {
    let mut ingredients = vec![];
    for line in get_file("./inputs/day_21.txt").lines() {
        let matches = REGEX_CONTAINS.captures(line).unwrap();
        let foods: HashSet<String> = matches.get(1).unwrap().as_str().split(' ').map(|l| l.to_string()).collect();
        let allergens: HashSet<String> = matches.get(2).unwrap().as_str().split(", ").map(|l| l.to_string()).collect();
        ingredients.push((foods, allergens))
    }
    ingredients
}


fn solve_part_a(foods: &[(HashSet<Ingredient>, HashSet<Allergen>)]) -> (usize, String) {
    let mut allergen_map = HashMap::new();
    let mut safe_ingredients = foods.iter().flat_map(|(ingredient, _)| ingredient).cloned().collect();
    let allergens: &HashSet<Allergen> = &foods.iter().flat_map(|(_, allergen)| allergen).cloned().collect();

    while allergen_map.len() != allergens.len() {
        for allergen in allergens {
            if let Some(ingredient) = get_allergen_ingredient(&allergen, &safe_ingredients, foods) {
                safe_ingredients.remove(&ingredient);
                allergen_map.insert(allergen, ingredient);
            }
        }
    }

    (get_solution_part_a(&safe_ingredients, foods), get_solution_part_b(allergen_map, allergens))
}


fn get_allergen_ingredient(allergen: &str, food_list: &HashSet<Ingredient>, foods: &[(HashSet<Ingredient>, HashSet<Allergen>)]) -> Option<Ingredient> {
    let mut remaining_suspect_food = food_list.clone();

    for (ingredients, _) in foods.iter().filter(|(_, allergens)| allergens.contains(allergen)) {
        remaining_suspect_food = remaining_suspect_food.intersection(ingredients).cloned().collect();
    }
    if remaining_suspect_food.len() == 1 {
        Some(remaining_suspect_food.iter().next().unwrap().clone())
    } else {
        None
    }
}


fn get_solution_part_a(safe_ingredients: &HashSet<Ingredient>, foods: &[(HashSet<Ingredient>, HashSet<Allergen>)]) -> usize{
    let mut counter = 0;
    for safe_ingredient in safe_ingredients {
        counter += foods.iter().filter(|(ingredients, _)|ingredients.contains(safe_ingredient)).count();
    }
    counter
}


fn get_solution_part_b(allergen_map: HashMap<&Allergen, Ingredient>, allergens: &HashSet<Allergen>) -> String {
    let mut ingredients = vec![];
    for allergen in allergens.iter().sorted() {
        ingredients.push(allergen_map.get(allergen).unwrap().clone());
    }
    ingredients.join(",")
}
