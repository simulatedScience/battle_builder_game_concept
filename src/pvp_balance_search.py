"""
This module simulates round-based PvP battles and searches for 3-way RPS (Rock-Paper-Scissors)
cycles between archetypes (Offense, Tank, Balanced).

Author: OpenAI (ChatGPT, GPT-5)
"""

# Standard library imports
import itertools
import multiprocessing as mp
from dataclasses import dataclass
from typing import Tuple, Optional

import matplotlib.pyplot as plt

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

def test_rps_cycle(o: Build, t: Build, b: Build, min_rounds: int = 4, max_rounds: int = 6) -> bool:
    """Return True if (O > T, T > B, B > O) with each win lasting 4–6 rounds."""
    r1, hp_log_1 = simulate_battle(o, t)
    r2, hp_log_2 = simulate_battle(t, b)
    r3, hp_log_3 = simulate_battle(b, o)

    if not (r1.winner == o.name and r2.winner == t.name and r3.winner == b.name):
        return False

    return all(min_rounds <= r.rounds <= max_rounds for r in (r1, r2, r3))

def _worker(args: Tuple[Tuple[int, int, int], Tuple[int, int, int], Tuple[int, int, int]]) -> Optional[Tuple[Build, Build, Build]]:
    """Worker function for parallel RPS cycle testing."""
    stats_o, stats_t, stats_b = args
    ofns = Build("Offense", *stats_o)
    tank = Build("Tank", *stats_t)
    bal = Build("Balanced", *stats_b)
    if test_rps_cycle(ofns, tank, bal):
        return (ofns, tank, bal)
    return None

def search_parameters(
    atk_range: range,
    def_range: range,
    rev_range: range,
    hp_range: range,
    processes: int = 4,
) -> list[Tuple[Build, Build, Build]]:
    """
    Enumerate parameter combinations and find RPS cycles satisfying balance criteria.

    Args:
        atk_range (range): Range of attack values.
        def_range (range): Range of defense values.
        hp_range (range): Range of HP values.
        revenge_equals_def (bool): If True, revenge = defense.
        processes (int): Number of parallel worker processes.

    Returns:
        list[Tuple[Build, Build, Build]]: All (O, T, B) triples forming an RPS cycle.
    """
    # Cartesian product search space
    all_combos = itertools.product(
        itertools.product(atk_range, def_range, rev_range, hp_range),
        itertools.product(atk_range, def_range, rev_range, hp_range),
        itertools.product(atk_range, def_range, rev_range, hp_range)
    )

    with mp.Pool(processes=processes) as pool:
        results = pool.map(_worker, all_combos)

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
        hp=16
    )
    bal = Build(
        "Balanced",
        atk=4,
        defense=2,
        revenge=2,
        hp=20
    )
    tank = Build(
        "Tank",
        atk=1,
        defense=3,
        revenge=3,
        hp=23
    )
    return ofns, bal, tank

def test_default_battle(plot_hp_logs: bool = True):
    ofns, bal, tank = default_stats()
    res1, hp_log_1 = simulate_battle(ofns, tank)
    res2, hp_log_2 = simulate_battle(tank, bal)
    res3, hp_log_3 = simulate_battle(bal, ofns)
    print("Default Builds Battle Results:")
    print(f"Offense vs Tank:     {res1}")
    print(f"Tank vs Balanced:    {res2}")
    print(f"Balanced vs Offense: {res3}")
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
            label1 = f"{player1} (Avg. DMG: {((hp_log[0][0] - hp_log[-1][0]) / len(hp_log)):.2f})"
            label2 = f"{player2} (Avg. DMG: {((hp_log[0][1] - hp_log[-1][1]) / len(hp_log)):.2f})"
            hp1_log, hp2_log = zip(*hp_log)
            ax.plot(range(len(hp1_log)), hp1_log, label=label1)
            ax.plot(range(len(hp2_log)), hp2_log, label=label2)
            ax.plot((0, len(hp1_log)), (0, 0), 'k--', linewidth=0.8)  # Zero HP line
            ax.grid(color="#eee")
            ax.set_title(title)
            ax.set_xlabel('Round')
            ax.set_ylabel('HP')
            ax.legend()
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    test_default_battle()
    
    # atk_range = range(1, 7, 2)   # 1–6
    # def_range = range(1, 5, 2)   # 1–4
    # rev_range = range(1, 5, 2)   # 1–4
    # hp_range = range(5, 21, 5)  # 5,10,15,20
    # # total combinations: 6*4*4*4 = 384 per archetype, 384^3 = 56,623,104 total

    # print("Searching for RPS cycles... (this may take some seconds)")
    # found = search_parameters(atk_range, def_range, hp_range, rev_range, processes=mp.cpu_count())

    # print(f"Found {len(found)} RPS cycles. Example:")
    # if found:
    #     o, t, b = found[0]
    #     print(o)
    #     print(t)
    #     print(b)
