use crate::utils::get_file;


pub fn day_18() {
    let input = get_input();

    let solution_a: u64 = input.iter().map(|t| eval(&t, get_opp_index_part_a)).sum();
    println!("Part A: {}", solution_a);

    let solution_b: u64 = input.iter().map(|t| eval(&t, get_opp_index_part_b)).sum();
    println!("Part B: {}", solution_b);
}


fn get_input() -> Vec<Vec<Token>> {
    let mut token_lines = vec![];
    for line in get_file("./inputs/day_18.txt").lines() {
        let token_line = line.replace("(", " ( ")
            .replace(")", " ) ")
            .split(' ')
            .filter(|x| !x.eq(&""))
            .map(|x| match x {
                "(" => Token::LeftBracket,
                ")" => Token::RightBracket,
                "+" => Token::Add,
                "*" => Token::Mul,
                val => Token::Value(val.parse().unwrap())
            }).collect();
        token_lines.push(token_line);
    }
    token_lines
}


fn eval(tokens: &[Token], get_opp_idx: fn(&[(usize, &Token)]) -> usize) -> u64 {
    // Remove useless brackets
    if tokens[0].eq(&Token::LeftBracket) {
        let p_end = get_end_bracket_idx(&tokens);
        if p_end == tokens.len() {
            return eval(&tokens[1..p_end - 1], get_opp_idx);
        }
    }

    if tokens.len() == 1 {
        return tokens[0].get_value();
    }

    // Get only operators which are not in brackets
    let mut bracket = 0;
    let mut tokens_with_idx: Vec<(usize, &Token)> = vec![];
    for (idx, token) in tokens.iter().enumerate() {
        match token {
            Token::Add | Token::Mul => {
                if bracket == 0 { tokens_with_idx.push((idx, token)) }
            }
            Token::RightBracket => bracket += 1,
            Token::LeftBracket => bracket -= 1,
            _ => {}
        }
    }

    // Select operator by priority
    let idx = get_opp_idx(&tokens_with_idx);
    tokens[idx].compute(
        eval(&tokens[..idx], get_opp_idx),
        eval(&tokens[idx + 1..], get_opp_idx),
    )
}


fn get_end_bracket_idx(tokens: &[Token]) -> usize {
    let mut bracket_end_idx = 0;
    let mut open_bracket = 0;

    for token in tokens {
        bracket_end_idx += 1;
        match token {
            Token::LeftBracket => {
                open_bracket += 1
            }
            Token::RightBracket => {
                open_bracket -= 1;
                if open_bracket == 0 {
                    break;
                }
            }
            _ => {}
        }
    }
    bracket_end_idx
}


fn get_opp_index_part_a(tokens_with_idx: &[(usize, &Token)]) -> usize {
    tokens_with_idx.last().unwrap().0
}


fn get_opp_index_part_b(tokens_with_idx: &[(usize, &Token)]) -> usize {
    if let Some((idx, _)) = tokens_with_idx.iter().find(|(_, &t)| t.eq(&Token::Mul)) {
        return *idx;
    }
    if let Some((idx, _)) = tokens_with_idx.iter().find(|(_, &t)| t.eq(&Token::Add)) {
        return *idx;
    }
    unreachable!()
}


#[derive(Debug, Eq, PartialEq, Copy, Clone)]
enum Token {
    LeftBracket,
    RightBracket,
    Add,
    Mul,
    Value(u64),
}


impl Token {
    fn get_value(&self) -> u64 {
        match &self {
            Token::Value(val) => *val,
            _ => panic!("Tried to get value from : {:?}", &self)
        }
    }

    fn compute(&self, value_a: u64, value_b: u64) -> u64 {
        match &self {
            Token::Add => value_a + value_b,
            Token::Mul => value_a * value_b,
            _ => panic!("Tried to compute value from : {:?}", &self)
        }
    }
}
