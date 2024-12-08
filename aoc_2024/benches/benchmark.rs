use aoc_2024::day_08::day_08;
use criterion::{criterion_group, criterion_main, Criterion};

fn criterion_benchmark(c: &mut Criterion) {
    c.bench_function("day 08", |b| b.iter(|| day_08()));
}

criterion_group!(benches, criterion_benchmark);
criterion_main!(benches);
