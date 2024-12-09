use aoc_2024::day_09::day_09;
use criterion::{criterion_group, criterion_main, Criterion};

fn criterion_benchmark(c: &mut Criterion) {
    c.bench_function("day 09", |b| b.iter(|| day_09()));
}

criterion_group!(benches, criterion_benchmark);
criterion_main!(benches);
