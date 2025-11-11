"""
Script to run build optimization and visualize results.
"""

from pvp_balance_search import Build, optimize_builds, simulate_battle, test_rps_cycle, proper_strategy_names, fitness
from build_plotter import plot_builds
from test_builds import default_stats

def main():
    # Stat ranges for each archetype (Offense, Balanced, Tank)
    atk_ranges = [(1, 10), (1, 10), (1, 10)]
    def_ranges = [(1, 10), (1, 10), (1, 10)]
    rev_ranges = [(-2, 2), (-2, 2), (-2, 2)]
    hp_ranges = [(6, 23), (6, 24), (6, 25)]
    spd_ranges = [(0, 10), (0, 10), (0, 10)]   # added speed ranges
    
    # Get default builds to use as starting point
    initial_builds = default_stats()
    
    print("=" * 60)
    print("Starting builds:")
    print("=" * 60)
    for build in initial_builds:
        print(build)
    print(f"Initial fitness: {fitness(*initial_builds):.4f}")
    print()
    
    # Run optimization
    print("=" * 60)
    print("Optimizing builds using Differential Evolution")
    print("=" * 60)
    
    offense, balanced, tank = optimize_builds(
        atk_ranges,
        def_ranges,
        rev_ranges,
        hp_ranges,
        spd_ranges,            # pass speed ranges
        maxiter=2000,
        popsize=75,
        workers=-1,
        # seed=42,
        initial_builds=initial_builds  # Use test builds as starting point
    )
    
    # Display results
    print("\n" + "=" * 60)
    print("OPTIMIZED BUILDS")
    print("=" * 60)
    print(offense)
    print(balanced)
    print(tank)
    print()
    print(f"Valid strategy names: {proper_strategy_names(offense, balanced, tank)}")
    is_rps, rounds = test_rps_cycle(offense, balanced, tank)
    print(f"Forms RPS cycle: {is_rps} (rounds: {rounds})")
    print(f"Final fitness: {fitness(offense, balanced, tank):.4f}")
    
    # Test battles
    print("\n" + "=" * 60)
    print("BATTLE RESULTS")
    print("=" * 60)
    battles = [
        ("Offense vs Tank", offense, tank),
        ("Tank vs Balanced", tank, balanced),
        ("Balanced vs Offense", balanced, offense)
    ]
    
    for title, p1, p2 in battles:
        result, _ = simulate_battle(p1, p2)
        print(f"{title:25s} {result}")
    
    # Visualize the optimized builds
    plot_builds([offense, balanced, tank])

if __name__ == "__main__":
    main()
