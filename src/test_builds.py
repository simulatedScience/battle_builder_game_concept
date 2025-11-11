"""
Script to test default builds and visualize battle HP logs.
"""
import numpy as np
import matplotlib.pyplot as plt
from pvp_balance_search import Build, simulate_battle, test_rps_cycle, proper_strategy_names, fitness
from build_plotter import ARCHETYPE_TO_COLOR, plot_builds

def default_stats() -> tuple[Build, Build, Build]:
    """Return default builds for Offense, Balanced, and Tank archetypes."""
    offense  = Build("Offense",  atk=6, defense=1, revenge=.8, hp=13)
    balanced = Build("Balanced", atk=4, defense=2, revenge=1.6, hp=15)
    tank     = Build("Tank",     atk=1, defense=3, revenge=2.7, hp=16)
    return offense, balanced, tank

def default_stats2() -> tuple[Build, Build, Build]:
    """Return default builds for Offense, Balanced, and Tank archetypes."""
    offense  = Build("Offense",  atk=6, defense=3.5, revenge=0., hp=7)
    balanced = Build("Balanced", atk=5, defense=4, revenge=0.5, hp=9)
    tank     = Build("Tank",     atk=3.5, defense=4.5, revenge=.9, hp=11)
    return offense, balanced, tank

def stats_from_matrix(scale_factor: float) -> tuple[Build, Build, Build]:
    weight_matrix = np.array([
        [6., 3.5, 0., 7],
        [5., 4., 0.5, 9.],
        [3.5, 4.5, .9, 11.]
    ])
    scaled_matrix = weight_matrix * scale_factor
    # round
    for row in scaled_matrix:
        row[3] = int(round(row[3]))  # Round HP to nearest integer
        for i in range(3):
            row[i] = round(row[i], 2)  # Round other stats to 2 decimal places
    offense = Build("Offense", atk=scaled_matrix[0,0], defense=scaled_matrix[0,1], revenge=scaled_matrix[0,2], hp=scaled_matrix[0,3])
    balanced = Build("Balanced", atk=scaled_matrix[1,0], defense=scaled_matrix[1,1], revenge=scaled_matrix[1,2], hp=scaled_matrix[1,3])
    tank = Build("Tank", atk=scaled_matrix[2,0], defense=scaled_matrix[2,1], revenge=scaled_matrix[2,2], hp=scaled_matrix[2,3])
    # print new builds
    print(f"Builds with scale factor {scale_factor}:")
    print(f"Offense: {offense}")
    print(f"Balanced: {balanced}")
    print(f"Tank: {tank}")
    return offense, balanced, tank

def plot_battle(ax: plt.Axes, title: str, hp_log: list[tuple[int, int]]):
    """Plot HP logs for a single battle on given axis."""
    player1, player2 = title.split(" vs ")
    hp1_log, hp2_log = zip(*hp_log)
    
    # Calculate average damage per turn
    avg_dmg_1 = (hp_log[0][1] - hp_log[-1][1]) / len(hp_log)
    avg_dmg_2 = (hp_log[0][0] - hp_log[-1][0]) / len(hp_log)
    
    label1 = f"{player1} (Avg. DMG: {avg_dmg_1:.2f})"
    label2 = f"{player2} (Avg. DMG: {avg_dmg_2:.2f})"
    
    ax.plot(range(len(hp1_log)), hp1_log, label=label1, 
            color=ARCHETYPE_TO_COLOR.get(player1, None))
    ax.plot(range(len(hp2_log)), hp2_log, label=label2, 
            color=ARCHETYPE_TO_COLOR.get(player2, None))
    ax.plot((0, len(hp1_log)), (0, 0), 'k--', linewidth=0.8)
    ax.grid(color="#eee")
    ax.set_title(title)
    ax.set_xlabel('Round')
    ax.set_ylabel('HP')
    ax.legend()

def test_default_battle(plot_hp_logs: bool = True):
    """Test default builds and optionally plot HP logs."""
    # offense, balanced, tank = default_stats2()
    offense, balanced, tank = stats_from_matrix(scale_factor=.6)
    
    print(f"Default builds are valid: {proper_strategy_names(offense, balanced, tank)}")
    
    # Run all battles
    battles = [
        ("Offense vs Tank", offense, tank),
        ("Tank vs Balanced", tank, balanced),
        ("Balanced vs Offense", balanced, offense)
    ]
    
    results_and_logs = [(title, *simulate_battle(p1, p2)) for title, p1, p2 in battles]
    
    print("Default Builds Battle Results:")
    for title, result, _ in results_and_logs:
        print(f"{title:20s} {result}")
    
    is_rps, rounds = test_rps_cycle(offense, balanced, tank)
    print(f"Form RPS cycle: {is_rps} (rounds: {rounds})")
    print(f"Fitness score: {fitness(offense, balanced, tank):.4f}")
    
    # plot_builds([offense, balanced, tank])
    if plot_hp_logs:
        fig, axs = plt.subplots(3, 1, figsize=(5, 8))
        for ax, (title, _, hp_log) in zip(axs, results_and_logs):
            plot_battle(ax, title, hp_log)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    test_default_battle()
