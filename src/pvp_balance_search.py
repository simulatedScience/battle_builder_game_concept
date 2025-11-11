"""
This module simulates round-based PvP battles and searches for 3-way RPS (Rock-Paper-Scissors)
cycles between archetypes (Offense, Tank, Balanced).

Author: OpenAI (ChatGPT, GPT-5)
"""

# Standard library imports
from dataclasses import dataclass
from typing import Optional
import numpy as np
from scipy.optimize import differential_evolution

# ------------------------------------------------------------
# Constants
# ------------------------------------------------------------

STAT_RANGES = {
    'atk': (1., 10.),
    'defense': (1., 10.),
    'revenge': (-1., 1.),
    'hp': (5, 25)
}

# ------------------------------------------------------------
# Data structures
# ------------------------------------------------------------

@dataclass
class Build:
    """Represents a player archetype's stats."""
    name: str
    atk: float
    defense: float
    revenge: float
    hp: int
    
    def __str__(self):
        return (f"{self.name}(ATK: {self.atk}, DEF: {self.defense}, "
                f"REV: {self.revenge}, HP: {self.hp})")

@dataclass
class BattleResult:
    """Represents the outcome of a PvP battle."""
    winner: Optional[str]
    rounds: int
    
    def __str__(self):
        if self.winner is None:
            return f"Draw after {self.rounds} rounds"
        return f"{self.winner} wins in {self.rounds} rounds"

# ------------------------------------------------------------
# Battle simulator
# ------------------------------------------------------------

def simulate_battle(p1: Build, p2: Build, max_rounds: int = 100) -> tuple[BattleResult, list[tuple[int, int]]]:
    """
    Simulate a PvP battle between two builds until one dies or max_rounds is reached.

    Rules:
    - Both attack simultaneously each round.
    - If a defender survives the primary attack, they deal immediate revenge (flat damage).
    - No speed or turn order.

    Args:
        p1 (Build): Player 1's build.
        p2 (Build): Player 2's build.
        max_rounds (int): Upper limit to avoid infinite loops.

    Returns:
        tuple[BattleResult, list[tuple[int, int]]]: The outcome and HP log.
    """
    hp1, hp2 = p1.hp, p2.hp
    hp_log = [(hp1, hp2)]  # Log HP after each round
    for round_idx in range(1, max_rounds + 1):
        # Primary attacks (simultaneous)
        dmg_1_to_2 = max(0, p1.atk - p2.defense)
        dmg_2_to_1 = max(0, p2.atk - p1.defense)

        hp1 -= dmg_2_to_1
        hp2 -= dmg_1_to_2

        # Revenge (only if defender survived primary hit)
        if hp1 > 0:
            hp2 -= p1.revenge
        if hp2 > 0:
            hp1 -= p2.revenge

        hp_log.append((hp1, hp2))

        # Check end of battle
        if hp1 <= 0 and hp2 <= 0:
            return BattleResult(winner=None, rounds=round_idx), hp_log  # Draw
        elif hp2 <= 0:
            return BattleResult(winner=p1.name, rounds=round_idx), hp_log
        elif hp1 <= 0:
            return BattleResult(winner=p2.name, rounds=round_idx), hp_log

    return BattleResult(winner=None, rounds=max_rounds), hp_log

# ------------------------------------------------------------
# RPS cycle validation and fitness
# ------------------------------------------------------------

def _penalize_out_of_range(value: float, range_bounds: tuple[float, float], multiplier: float = 10) -> float:
    """Calculate penalty for value being outside the valid range."""
    return multiplier * (max(0.0, range_bounds[0] - value) + max(0.0, value - range_bounds[1]))

def _calculate_advantage(attacker: Build, defender: Build) -> float:
    """Calculate expected round advantage for attacker over defender."""
    defender_damage = max(0, defender.atk - attacker.defense + defender.revenge)
    attacker_damage = max(0, attacker.atk - defender.defense + attacker.revenge)
    
    if defender_damage <= 0:
        return float("inf")  # Avoid division by zero
    if attacker_damage <= 0:
        return 0.0  # Avoid division by zero
    
    return attacker.hp / defender_damage - defender.hp / attacker_damage

def _penalize_advantage(advantage: float, min_adv: float = 0.5, max_adv: float = 3.0) -> float:
    """Penalize advantage if too small or too large, reward if in range."""
    if advantage < min_adv:
        return 20.0 * (min_adv - advantage)  # Heavy penalty for too small
    elif advantage > max_adv:
        return 10.0 * (advantage - max_adv)  # Moderate penalty for too large
    else:
        return -2.0  # Reward for being in the sweet spot

def proper_strategy_names(o: Build, b: Build, t: Build) -> bool:
    """
    Ensure that the build names correspond to their intended strategies.
    O = Offense (high ATK, low DEF, low HP)
    B = Balanced (medium ATK, medium DEF, medium HP)
    T = Tank (low ATK, high DEF, high HP)
    """
    stat_order = [
        (o.atk > b.atk and b.atk > t.atk),                      # Attack: O > B > T
        (t.defense > b.defense and b.defense > o.defense),      # Defense: T > B > O
        (o.hp < b.hp and b.hp < t.hp)                          # HP: O < B < T
    ]
    return all(stat_order)

def test_rps_cycle(o: Build, b: Build, t: Build) -> tuple[bool, tuple[int, int, int]]:
    """Return True if (O > T, T > B, B > O) with each win lasting 3–10 rounds."""
    r1, _ = simulate_battle(o, t)
    r2, _ = simulate_battle(t, b)
    r3, _ = simulate_battle(b, o)

    rps_valid = (r1.winner == o.name and r2.winner == t.name and r3.winner == b.name)
    round_lengths = (r1.rounds, r2.rounds, r3.rounds)
    
    return rps_valid, round_lengths

def fitness(offense: Build, balanced: Build, tank: Build, min_rounds: int = 3, max_rounds: int = 10) -> float:
    """
    Continuous fitness function to estimate the quality of an RPS cycle formed by the three builds.
    Lower is better.
    """
    out_of_range_factor: float = 10000
    names_factor: float = 1000
    rps_factor: float = 100
    rounds_factor: float = 10
    
    score = 0.0
    # Penalize distance to valid ranges for all builds
    for build in (offense, balanced, tank):
        score += _penalize_out_of_range(build.atk, STAT_RANGES['atk'], multiplier=out_of_range_factor)
        score += _penalize_out_of_range(build.defense, STAT_RANGES['defense'], multiplier=out_of_range_factor)
        score += _penalize_out_of_range(build.revenge, STAT_RANGES['revenge'], multiplier=out_of_range_factor)
        score += _penalize_out_of_range(build.hp, STAT_RANGES['hp'], multiplier=out_of_range_factor)
    
    # Large penalty for not forming RPS cycle
    is_rps_cycle, round_lengths = test_rps_cycle(offense, balanced, tank)
    if not is_rps_cycle:
        score += rps_factor
    
    # Penalize RPS cycle length deviations
    for length in round_lengths:
        if length < min_rounds:
            score += 5 * rounds_factor * (min_rounds - length)
        elif length > max_rounds:
            score += rounds_factor * (length - max_rounds)
    
    # Penalize improper strategy names
    score += names_factor * (1.0 - proper_strategy_names(offense, balanced, tank))

    # Evaluate advantages for each matchup in the RPS cycle
    matchups = [
        (offense, tank),
        (tank, balanced),
        (balanced, offense)
    ]
    
    # total_advantage = 0.0
    # for attacker, defender in matchups:
    #     advantage = _calculate_advantage(attacker, defender)
    #     score += _penalize_advantage(advantage)
        # total_advantage += advantage

    # score += total_advantage

    return score

# ------------------------------------------------------------
# Optimization
# ------------------------------------------------------------

def _fitness_wrapper(params: np.ndarray) -> float:
    """
    Wrapper for fitness function that accepts a flat array of 12 parameters.
    
    Args:
        params: Array of [atk_o, def_o, rev_o, hp_o, atk_b, def_b, rev_b, hp_b, atk_t, def_t, rev_t, hp_t]
    
    Returns:
        Fitness score (lower is better)
    """
    # Round HP values to integers during fitness evaluation
    offense = Build("Offense", params[0], params[1], params[2], int(round(params[3])))
    balanced = Build("Balanced", params[4], params[5], params[6], int(round(params[7])))
    tank = Build("Tank", params[8], params[9], params[10], int(round(params[11])))
    
    return fitness(offense, balanced, tank)

def optimize_builds(
    atk_ranges: list[tuple[int, int]],
    def_ranges: list[tuple[int, int]],
    rev_ranges: list[tuple[int, int]],
    hp_ranges: list[tuple[int, int]],
    maxiter: int = 100,
    popsize: int = 15,
    workers: int = -1, # Use all available CPUs
    seed: Optional[int] = None,
    initial_builds: Optional[tuple[Build, Build, Build]] = None
) -> tuple[Build, Build, Build]:
    """
    Use differential evolution to optimize the 12 build parameters.
    
    Args:
        atk_ranges: Attack ranges for [Offense, Balanced, Tank]
        def_ranges: Defense ranges for [Offense, Balanced, Tank]
        rev_ranges: Revenge ranges for [Offense, Balanced, Tank]
        hp_ranges: HP ranges for [Offense, Balanced, Tank]
        maxiter: Maximum number of generations
        popsize: Population size multiplier (population = popsize * 12)
        workers: Number of parallel workers (-1 for all CPUs)
        seed: Random seed for reproducibility
        initial_builds: Optional tuple of (Offense, Balanced, Tank) builds to seed the population
    
    Returns:
        Tuple of optimized (Offense, Balanced, Tank) builds
    """
    # Construct bounds: [atk_o, def_o, rev_o, hp_o, atk_b, def_b, rev_b, hp_b, atk_t, def_t, rev_t, hp_t]
    bounds: list[tuple[float, float]] = [
        atk_ranges[0], def_ranges[0], rev_ranges[0], hp_ranges[0],
        atk_ranges[1], def_ranges[1], rev_ranges[1], hp_ranges[1],
        atk_ranges[2], def_ranges[2], rev_ranges[2], hp_ranges[2],
    ]
    
    # Prepare initial population if provided
    init_population: str = 'latinhypercube'  # Default
    if initial_builds is not None:
        offense, balanced, tank = initial_builds
        init_vector = np.array([
            offense.atk, offense.defense, offense.revenge, float(offense.hp),
            balanced.atk, balanced.defense, balanced.revenge, float(balanced.hp),
            tank.atk, tank.defense, tank.revenge, float(tank.hp)
        ], dtype=float)
        
        # # Clip to bounds
        # lower_bounds = np.array([b[0] for b in bounds])
        # upper_bounds = np.array([b[1] for b in bounds])
        # init_vector = np.clip(init_vector, lower_bounds, upper_bounds)
        
        print(f"Using initial builds as seed:")
        print(f"  Offense:  ATK={init_vector[0]:.2f}, DEF={init_vector[1]:.2f}, REV={init_vector[2]:.2f}, HP={int(init_vector[3])}")
        print(f"  Balanced: ATK={init_vector[4]:.2f}, DEF={init_vector[5]:.2f}, REV={init_vector[6]:.2f}, HP={int(init_vector[7])}")
        print(f"  Tank:     ATK={init_vector[8]:.2f}, DEF={init_vector[9]:.2f}, REV={init_vector[10]:.2f}, HP={int(init_vector[11])}")
        print(f"  Initial fitness: {_fitness_wrapper(init_vector):.2f}")
        
        # Generate a full population with the initial build as the first individual
        # Population size must be at least 5
        n_params: int = len(bounds)
        pop_size: int = max(5, popsize * n_params)
        
        # Set seed for reproducibility
        if seed is not None:
            np.random.seed(seed)
        
        # Create population: first row is our initial build, rest are random
        if initial_builds is not None:
            init_population: np.ndarray = np.zeros((pop_size, n_params))
            for i in range(pop_size):
                init_population[i] = init_vector * (1 + np.random.normal(0, .1, size=n_params))
        
            # # Fill rest with random Latin Hypercube samples
            # for i in range(0, pop_size):
            #     for j, (lower, upper) in enumerate(bounds):
            #         init_population[i, j] = np.random.uniform(lower, upper)
        
        print(f"  Generated population of size {pop_size}")
    
    print(f"\nOptimizing 12 parameters with differential evolution...")
    print(f"Effective population size: {pop_size}, Max iterations: {maxiter}")

    def callback(xk, convergence):
        """Callback to monitor optimization progress."""
        current_fitness = _fitness_wrapper(xk)
        print(f"Generation complete - Best fitness: {current_fitness:.2f}")
        return False
    
    result = differential_evolution(
        _fitness_wrapper,
        bounds=bounds,
        strategy='best1bin',
        maxiter=maxiter,
        popsize=popsize,
        tol=0.00001,
        mutation=(0.5, 1.5),
        recombination=0.9,
        seed=seed,
        workers=workers,
        updating='deferred',
        polish=True,
        disp=True,
        callback=callback,
        init=init_population if initial_builds is not None else 'latinhypercube'
        # init='latinhypercube'
    )

    # Extract optimized builds (keep float precision; HP displayed as int)
    offense = Build("Offense", result.x[0], result.x[1], result.x[2], int(round(result.x[3])))
    balanced = Build("Balanced", result.x[4], result.x[5], result.x[6], int(round(result.x[7])))
    tank = Build("Tank", result.x[8], result.x[9], result.x[10], int(round(result.x[11])))

    print(f"\nOptimization complete!")
    print(f"Final fitness score: {result.fun:.4f}")
    print(f"Function evaluations: {result.nfev}")

    return offense, balanced, tank