use aoc_2024::day_06::day_06;
use criterion::{criterion_group, criterion_main, Criterion};

fn criterion_benchmark(c: &mut Criterion) {
    c.bench_function("day 06", |b| b.iter(|| day_06()));
}

criterion_group!(benches, criterion_benchmark);
criterion_main!(benches);
