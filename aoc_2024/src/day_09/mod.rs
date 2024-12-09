use crate::utils::io::get_file;

#[derive(Debug, Copy, Clone)]
struct Block(Option<usize>);

impl Block {
    fn is_file(&self) -> bool {
        self.0.is_some()
    }

    fn is_free(&self) -> bool {
        self.0.is_none()
    }
}

pub fn day_09() {
    let input = get_input("./src/day_09/input.txt");

    let solution_1 = part_one(&input);
    println!("\t- Solution 1 is : {solution_1}");

    let input = get_input_part_2("./src/day_09/input.txt");
    let solution_2 = part_two(&input);
    println!("\t- Solution 2 is : {solution_2}");
}

///////////////////////////////////////////////////////////////////////////////
// PART ONE
///////////////////////////////////////////////////////////////////////////////
fn get_input(file_name: &str) -> Vec<Block> {
    let mut parts = vec![];
    let mut current_idx = 0;

    for (idx, char) in get_file(file_name).trim().chars().enumerate() {
        let length = char.to_digit(10).unwrap() as usize;
        if idx % 2 == 0 {
            for _ in 0..length {
                parts.push(Block(Some(current_idx)));
            }
            current_idx += 1;
        } else {
            for _ in 0..length {
                parts.push(Block(None));
            }
        }
    }
    parts
}

fn has_gaps_between_file_blocks(block: &[Block]) -> bool {
    let mut has_gaps = false;

    for bloc in block {
        if bloc.is_free() {
            has_gaps = true;
        } else if has_gaps {
            // If there is free space, and we have already seen a file block,
            // then there is a gap between file blocks.
            return true;
        }
    }
    false
}

fn get_blocks_to_swap(blocks: &[Block]) -> (usize, usize) {
    let mut file_idx = None;
    let mut space_idx = None;

    for (idx, block) in blocks.iter().enumerate().rev() {
        if block.is_file() {
            file_idx = Some(idx);
            break;
        }
    }
    for (idx, block) in blocks.iter().enumerate() {
        if block.is_free() {
            space_idx = Some(idx);
            break;
        }
    }
    (file_idx.unwrap(), space_idx.unwrap())
}

fn part_one(blocks: &[Block]) -> usize {
    let mut blocks = blocks.to_vec();

    while has_gaps_between_file_blocks(&blocks) {
        let idx_to_swap = get_blocks_to_swap(&blocks);
        blocks.swap(idx_to_swap.0, idx_to_swap.1);
    }
    blocks
        .iter()
        .enumerate()
        .map(|(idx, block)| {
            if block.is_file() {
                idx * block.0.unwrap()
            } else {
                0
            }
        })
        .sum()
}

///////////////////////////////////////////////////////////////////////////////
// PART TWO
///////////////////////////////////////////////////////////////////////////////

#[derive(Debug, Copy, Clone)]
struct AtomicBlock {
    file: Option<u16>,
    length: usize,
}

impl AtomicBlock {
    fn is_file(&self) -> bool {
        self.file.is_some()
    }

    fn is_free(&self) -> bool {
        self.file.is_none()
    }
}

fn get_input_part_2(file_name: &str) -> Vec<AtomicBlock> {
    let mut blocks = vec![];
    let mut current_idx = 0;

    for (idx, char) in get_file(file_name).trim().chars().enumerate() {
        let length = char.to_digit(10).unwrap() as usize;
        if idx % 2 == 0 {
            blocks.push(AtomicBlock {
                file: Some(current_idx),
                length,
            });
            current_idx += 1;
        } else {
            blocks.push(AtomicBlock { file: None, length });
        }
    }
    blocks
}

fn get_highest_idx_file(blocks: &[AtomicBlock]) -> u16 {
    blocks
        .iter()
        .filter_map(|block| block.file)
        .max()
        .expect("No AtomicBlock instances contain a file index")
}

fn find_swappable_blocks(blocks: &[AtomicBlock], block_idx: u16) -> Option<(usize, usize)> {
    let mut file_idx = None;
    let mut space_idx = None;

    // Find the index of the file block with the given file_idx
    for (idx, block) in blocks.iter().enumerate().rev() {
        if block.is_file() && block.file.unwrap() == block_idx {
            file_idx = Some(idx);
            break;
        }
    }

    let file_position = file_idx?;

    // Search for the leftmost free block that is **before** the file block
    for (idx, block) in blocks.iter().enumerate() {
        if block.is_free() && block.length >= blocks[file_position].length && idx < file_position {
            space_idx = Some(idx);
            break;
        }
    }

    match (file_idx, space_idx) {
        (Some(from), Some(to)) if to < from => Some((from, to)),
        _ => None,
    }
}

fn move_atomic_block(blocks: &mut Vec<AtomicBlock>, from: usize, to: usize) {
    let block = blocks[from];
    blocks[from].file = None;

    // Store the original length of the free space block
    let original_length = blocks[to].length;

    // Update the length of the destination block to match the file's length
    blocks[to].length = block.length;
    blocks[to].file = block.file;

    // Calculate the remaining free space
    let remaining_space = original_length - block.length;

    // If there is remaining space, create a new free block after 'to'
    if remaining_space > 0 {
        let new_block = AtomicBlock {
            file: None,
            length: remaining_space,
        };
        blocks.insert(to + 1, new_block);
    }
}

fn part_two(blocks: &[AtomicBlock]) -> usize {
    let mut blocks = blocks.to_vec();
    let max_file_idx = get_highest_idx_file(&blocks);

    for idx in (0..=max_file_idx).rev() {
        let idx_to_swap = find_swappable_blocks(&blocks, idx);
        if let Some(idx_to_swap) = idx_to_swap {
            move_atomic_block(&mut blocks, idx_to_swap.0, idx_to_swap.1);
        }
    }

    let mut current_idx = 0;
    let mut total = 0;
    for block in blocks {
        if block.is_file() {
            for _ in 0..block.length {
                total += current_idx * block.file.unwrap() as usize;
                current_idx += 1;
            }
        } else {
            current_idx += block.length;
        }
    }
    total
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = get_input("./src/day_09/input_example.txt");
        assert_eq!(1928, part_one(&input));
    }

    #[test]
    fn test_part_two() {
        let input = get_input_part_2("./src/day_09/input_example.txt");
        assert_eq!(2858, part_two(&input));
    }
}
