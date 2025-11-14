#!/usr/bin/env python3
"""
Simple example of running the benchmark
This demonstrates how to collect performance data for a research paper

NOTE: The benchmark uses EnhancedMetroDataGenerator from DataService
to create complete, realistic synthetic data for testing greedy optimizers.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from benchmark_schedule_performance import SchedulePerformanceBenchmark

def run_simple_benchmark():
    """Run a simple benchmark for demonstration"""
    print("="*70)
    print("SIMPLE BENCHMARK EXAMPLE")
    print("="*70)
    print("\nThis example demonstrates benchmarking for research paper results.")
    print("It tests 3 fleet sizes with 2 runs each.")
    print("\nNOTE: Synthetic data is generated using DataService/EnhancedMetroDataGenerator")
    print("      This includes trainset status, fitness certificates, job cards, etc.\n")
    
    # Create benchmark instance
    benchmark = SchedulePerformanceBenchmark()
    
    # Run benchmark with small configuration
    benchmark.run_comprehensive_benchmark(
        fleet_sizes=[10, 20, 30],  # Test with 10, 20, and 30 trains
        greedy_methods=['ga', 'pso'],  # Test GA and PSO
        num_runs=2  # 2 runs for quick results
    )
    
    # Save results
    json_file = benchmark.save_results()
    report_file = benchmark.generate_report()
    
    print("\n" + "="*70)
    print("RESULTS FOR YOUR PAPER")
    print("="*70)
    
    if "summary" in benchmark.results and "fastest_optimizer" in benchmark.results["summary"]:
        fastest = benchmark.results["summary"]["fastest_optimizer"]
        fastest_time = benchmark.results["summary"]["fastest_time_seconds"]
        print(f"\nFastest Method: {fastest}")
        print(f"Average Time: {fastest_time:.4f} seconds")
    
    print("\nYou can use the following data in your Results section:")
    print(f"- Detailed JSON data: {json_file}")
    print(f"- Formatted report: {report_file}")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    run_simple_benchmark()
