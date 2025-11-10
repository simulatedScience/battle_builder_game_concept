"""
This module simulates round-based PvP battles and searches for 3-way RPS (Rock-Paper-Scissors)
cycles between archetypes (Offense, Tank, Balanced).

Author: OpenAI (ChatGPT, GPT-5)
"""

# Standard library imports
import random
import multiprocessing as mp
import sys
from dataclasses import dataclass
from typing import Optional
import matplotlib.pyplot as plt

from build_plotter import ARCHETYPE_TO_COLOR, plot_builds

# ------------------------------------------------------------
# Data structures
# ------------------------------------------------------------

@dataclass
class Build:
    """Represents a player archetype's stats."""
    name: str
    atk: int
    defense: int
    revenge: int
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

def simulate_battle(p1: Build, p2: Build, max_rounds: int = 100) -> BattleResult:
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
        BattleResult: The outcome (winner and number of rounds).
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

        # Log HP status
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
# RPS cycle search
# ------------------------------------------------------------

def proper_strategy_names(o: Build, b: Build, t: Build) -> bool:
    """
    Ensure that the build names correspond to their intended strategies.
    """
    if not (o.atk > b.atk and b.atk > t.atk):
        return False
    if not (t.defense > b.defense and b.defense > o.defense):
        return False
    if not (o.hp < b.hp and b.hp < t.hp):
        return False
    return True

def test_rps_cycle(o: Build, b: Build, t: Build, min_rounds: int = 3, max_rounds: int = 10) -> bool:
    """Return True if (O > T, T > B, B > O) with each win lasting 3–10 rounds."""
    r1, hp_log_1 = simulate_battle(o, t)
    r2, hp_log_2 = simulate_battle(t, b)
    r3, hp_log_3 = simulate_battle(b, o)

    if not (r1.winner == o.name and r2.winner == t.name and r3.winner == b.name):
        return False

    return all(min_rounds <= r.rounds <= max_rounds for r in (r1, r2, r3))

def _worker(args: tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]) -> Optional[tuple[Build, Build, Build]]:
    """Worker function for parallel RPS cycle testing."""
    stats_o, stats_t, stats_b = args
    ofns = Build("Offense", *stats_o)
    tank = Build("Tank", *stats_t)
    bal = Build("Balanced", *stats_b)
    # ensure names correspond to strategies:
    if not proper_strategy_names(ofns, bal, tank):
        return None
    if test_rps_cycle(ofns, bal, tank):
        return (ofns, bal, tank)
    return None

def search_parameters(
    atk_ranges: list[tuple[int, int]],
    def_ranges: list[tuple[int, int]],
    rev_ranges: list[tuple[int, int]],
    hp_ranges: list[tuple[int, int]],
    processes: int = 6,
    num_trials: int = 10000,
) -> list[tuple[Build, Build, Build]]:
    """
    Random search for RPS cycles over given stat ranges using parallel processing.

    Args:
        atk_range (range): Range of attack values.
        def_range (range): Range of defense values.
        hp_range (range): Range of HP values.
        revenge_equals_def (bool): If True, revenge = defense.
        processes (int): Number of parallel worker processes.

    Returns:
        list[tuple[Build, Build, Build]]: All (O, T, B) triples forming an RPS cycle.
    """
    def random_build(name, atk_range, def_range, rev_range, hp_range) -> Build:
        return (
            random.randint(*atk_range),
            random.randint(*def_range),
            random.randint(*rev_range),
            random.randint(*hp_range)
        )

    args_list = [
        (random_build("Offense", atk_ranges[0], def_ranges[0], rev_ranges[0], hp_ranges[0]),
         random_build("Balanced", atk_ranges[1], def_ranges[1], rev_ranges[1], hp_ranges[1]),
         random_build("Tank", atk_ranges[2], def_ranges[2], rev_ranges[2], hp_ranges[2]))
        for _ in range(num_trials)
    ]

    with mp.Pool(processes=processes) as pool:
        results = pool.map(_worker, args_list)

    return [res for res in results if res is not None]

# ------------------------------------------------------------
# Example usage (when run directly)
# ------------------------------------------------------------

def default_stats():
    ofns = Build(
        "Offense",
        atk=6,
        defense=1,
        revenge=1,
        hp=14
    )
    bal = Build(
        "Balanced",
        atk=4,
        defense=2,
        revenge=2,
        hp=15
    )
    tank = Build(
        "Tank",
        atk=1,
        defense=3,
        revenge=3,
        hp=16
    )
    return ofns, bal, tank

def test_default_battle(plot_hp_logs: bool = True):
    ofns, bal, tank = default_stats()
    # plot_builds([ofns, bal, tank])
    print(f"Default builds are valid: {proper_strategy_names(ofns, bal, tank)}")
    res1, hp_log_1 = simulate_battle(ofns, tank)
    res2, hp_log_2 = simulate_battle(tank, bal)
    res3, hp_log_3 = simulate_battle(bal, ofns)
    print("Default Builds Battle Results:")
    print(f"Offense vs Tank:     {res1}")
    print(f"Tank vs Balanced:    {res2}")
    print(f"Balanced vs Offense: {res3}")
    print(f"Form RPS cycle: {test_rps_cycle(ofns, bal, tank)}")
    if plot_hp_logs:
        # 3 subplots, one for each battle
        fig, axs = plt.subplots(3, 1, figsize=(5, 8))
        battles = [("Offense vs Tank", hp_log_1),
                   ("Tank vs Balanced", hp_log_2),
                   ("Balanced vs Offense", hp_log_3)]
        for ax, (title, hp_log) in zip(axs, battles):
            # recover player names
            player1, player2 = title.split(" vs ")
            # add avg. damage per turn to labels
            label1 = f"{player1} (Avg. DMG: {((hp_log[0][1] - hp_log[-1][1]) / len(hp_log)):.2f})"
            label2 = f"{player2} (Avg. DMG: {((hp_log[0][0] - hp_log[-1][0]) / len(hp_log)):.2f})"
            hp1_log, hp2_log = zip(*hp_log)
            ax.plot(range(len(hp1_log)), hp1_log, label=label1, color=ARCHETYPE_TO_COLOR.get(player1, None))
            ax.plot(range(len(hp2_log)), hp2_log, label=label2, color=ARCHETYPE_TO_COLOR.get(player2, None))
            ax.plot((0, len(hp1_log)), (0, 0), 'k--', linewidth=0.8)  # Zero HP line
            ax.grid(color="#eee")
            ax.set_title(title)
            ax.set_xlabel('Round')
            ax.set_ylabel('HP')
            ax.legend()
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    # test_default_battle()
    # sys.exit()
    # Stat ranges for each archetype (Offense, Balanced, Tank)
    atk_ranges = ((3, 9), (2, 7), (1, 5))
    def_ranges = ((1, 5), (2, 8), (3, 10))
    rev_ranges = ((1, 10), (1, 10), (1, 10))
    hp_ranges = ((6, 15), (8, 20), (8, 25))
    n_trials = 10_000_000

    print("Searching for RPS cycles... (this may take some seconds)")
    found = search_parameters(
        atk_ranges,
        def_ranges,
        rev_ranges,
        hp_ranges,
        processes=mp.cpu_count()*2,
        num_trials=n_trials
    )
    # save found to file
    with open("found_rps_cycles.txt", "w") as file:
        for ofns, bal, tank in found:
            file.write(f"Offense: {ofns}\n")
            file.write(f"Balanced:{bal}\n")
            file.write(f"Tank:    {tank}\n")
            file.write("\n")

    print(f"Found {len(found)} RPS cycles. Example:")
    for ofns, bal, tank in found[:20]:
        plot_builds([ofns, bal, tank])