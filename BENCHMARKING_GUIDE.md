# Metro Schedule Generation - Benchmarking Guide

This guide explains how to use the comprehensive benchmarking system to measure schedule generation performance for your research paper.

## Overview

The benchmark system measures:
1. **Schedule Generation Time**: How long it takes to generate schedules for different fleet sizes
2. **Computational Efficiency**: Performance comparison between different optimization methods

## Data Generation

The benchmark uses **EnhancedMetroDataGenerator** from DataService to create complete, realistic synthetic data including:
- Trainset status and operational data
- Fitness certificates
- Job cards and maintenance records
- Component health monitoring
- IoT sensor data
- Performance metrics

This ensures that greedy optimizers are tested with realistic, complete datasets.

## Components Tested

### 1. MetroScheduleOptimizer (DataService)
- Primary scheduling system
- Fast, deterministic schedule generation
- Uses route-based optimization

### 2. Greedy Optimization Methods (greedyOptim)
- **GA** (Genetic Algorithm): Evolutionary optimization
- **CMA-ES**: Covariance Matrix Adaptation
- **PSO** (Particle Swarm): Swarm intelligence
- **SA** (Simulated Annealing): Probabilistic optimization
