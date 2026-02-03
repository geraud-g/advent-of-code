use crate::utils::{get_file, LINE_ENDING};
use fnv::FnvHashSet;
use std::collections::hash_map::DefaultHasher;
use std::collections::VecDeque;
use std::hash::{Hash, Hasher};

const PLAYER_A_WON: bool = true;

type Deck = VecDeque<usize>;

pub fn day_22() {
    let (mut player_1, mut player_2) = get_input();
    let solution_a = solve_part_a(&mut player_1, &mut player_2);
    println!("Part A: {}", solution_a);

    let (mut player_1, mut player_2) = get_input();
    let solution_b = solve_part_b(&mut player_1, &mut player_2);
    println!("Part B: {}", solution_b);
}

fn get_input() -> (Deck, Deck) {
    let players: Vec<String> = get_file("./inputs/day_22.txt")
        .split(&format!("{}{}", LINE_ENDING, LINE_ENDING))
        .map(|l| l.to_string())
        .collect();
    let player1 = players[0]
        .lines()
        .skip(1)
        .map(|l| l.parse().unwrap())
        .collect();
    let player2 = players[1]
        .lines()
        .skip(1)
        .map(|l| l.parse().unwrap())
        .collect();
    (player1, player2)
}

fn solve_part_a(deck_player_a: &mut Deck, deck_player_b: &mut Deck) -> usize {
    while !deck_player_a.is_empty() && !deck_player_b.is_empty() {
        let card_a = deck_player_a.pop_front().unwrap();
        let card_b = deck_player_b.pop_front().unwrap();

        if card_a > card_b {
            deck_player_a.push_back(card_a);
            deck_player_a.push_back(card_b);
        } else {
            deck_player_b.push_back(card_b);
            deck_player_b.push_back(card_a);
        }
    }
    if deck_player_b.is_empty() {
        get_score(deck_player_a)
    } else {
        get_score(deck_player_b)
    }
}

fn solve_part_b(deck_player_a: &mut Deck, deck_player_b: &mut Deck) -> usize {
    solve_part_b_rec(deck_player_a, deck_player_b);
    if deck_player_a.is_empty() {
        get_score(deck_player_b)
    } else {
        get_score(deck_player_a)
    }
}

fn solve_part_b_rec(deck_player_a: &mut Deck, deck_player_b: &mut Deck) -> bool {
    let mut past_rounds = FnvHashSet::default();

    while !deck_player_a.is_empty() && !deck_player_b.is_empty() {
        if !past_rounds.insert(get_game_hash(&deck_player_a, &deck_player_b)) {
            return PLAYER_A_WON;
        }
        let card_a = deck_player_a.pop_front().unwrap();
        let card_b = deck_player_b.pop_front().unwrap();

        let player_won = if card_a <= deck_player_a.len() && card_b <= deck_player_b.len() {
            let mut new_deck_a = deck_player_a.iter().take(card_a).cloned().collect();
            let mut new_deck_b = deck_player_b.iter().take(card_b).cloned().collect();
            solve_part_b_rec(&mut new_deck_a, &mut new_deck_b)
        } else {
            card_a > card_b
        };
        if player_won == PLAYER_A_WON {
            deck_player_a.push_back(card_a);
            deck_player_a.push_back(card_b);
        } else {
            deck_player_b.push_back(card_b);
            deck_player_b.push_back(card_a);
        }
    }
    deck_player_b.is_empty()
}

fn get_game_hash(player_a: &Deck, player_b: &Deck) -> u64 {
    let mut s = DefaultHasher::new();
    player_a.hash(&mut s);
    player_b.hash(&mut s);
    s.finish()
}

fn get_score(player: &Deck) -> usize {
    player
        .iter()
        .enumerate()
        .map(|(idx, card)| card * (player.len() - idx))
        .sum()
}
