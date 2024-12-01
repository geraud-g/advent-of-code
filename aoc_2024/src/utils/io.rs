use std::fs;

pub fn get_file(file_name: &str) -> String {
    fs::read_to_string(file_name).expect("Unable to read file")
}
