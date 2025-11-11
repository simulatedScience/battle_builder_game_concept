"""
Plot a build's parameters: ATK, DEF, REV, HP, SPD in a radar chart.
Given three named builds, plot them next to each other for comparison.
"""

import matplotlib.pyplot as plt
import numpy as np

ARCHETYPE_TO_COLOR: dict[str, str] = {
    "Offense": "#FF5733",  # Red-Orange
    "Balanced": "#33FF57",  # Green
    "Tank": "#3375FF",     # Blue
}

def plot_build_radar(ax: plt.Axes, build: "Build", max_values: tuple[int, int, int, int, int], color: str|None = None) -> None:
    """
    Plot a build's parameters: ATK, DEF, REV, HP, SPD in a radar chart.
    
    Args:
        ax (plt.Axes): The axes to plot on.
        build (Build): The build to plot.
        color (str): Color for the plot lines and fill.
    """
    labels = ['ATK', 'DEF', 'REV', 'HP', 'SPD']
    stats = [
        build.atk / max_values[0],
        build.defense / max_values[1],
        build.revenge / max_values[2],
        build.hp / max_values[3],
        build.spd / max_values[4],
    ]
    stats += stats[:1]  # Close the loop

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]  # Close the loop

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    plt.xticks(angles[:-1], labels)

    ax.plot(angles, stats, color=color, linewidth=2, linestyle='solid', label=build.name)
    ax.fill(angles, stats, color=color, alpha=0.25)
    ax.set_title(build.name)


def plot_builds(builds: list["Build"]) -> None:
    """
    Plot multiple builds in a radar chart for comparison.
    Each drawn on the same axes.
    """
    num_builds = len(builds)
    # max_atk = max(build.atk for build in builds)
    # max_def = max(build.defense for build in builds)
    # max_rev = max(build.revenge for build in builds)
    # max_hp = max(build.hp for build in builds)
    # max_spd = max(build.spd for build in builds)
    # max_values = (max_atk, max_def, max_rev, max_hp, max_spd)
    max_values = (1, 1, 1, 1)

    fig, axs = plt.subplots(1, 1, subplot_kw=dict(polar=True), figsize=(5 * num_builds, 5))
    for build in builds:
        color = ARCHETYPE_TO_COLOR.get(build.name, None)
        plot_build_radar(axs, build, max_values, color)
    plt.show()
