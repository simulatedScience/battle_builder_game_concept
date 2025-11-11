# Battle Builder Simulation

This program implements a simplified version of my own (in development) Battle Builder game. This is meant to simulate battles to help with the balancing of the game.

The first version tries to balance three strategies with distinct offensive and defensive parameters.

## Combat mechnism
Simultaneous turn-based combat where each side selects an action and Speed (how much stamina to spend) each turn. Actions are resolved in order of Speed, with ties handled by chance.

Each player has five core stats:
ATK, DEF, REV, HP, SPD
- ATK: Attack power, determines damage dealt
- DEF: Defense power, reduces damage taken
- REV: Revenge power, damage dealt when attacked
- HP: Health points, when it reaches 0 the player is defeated
- SPD: Speed, determines turn order

Later, ATK, DEF and REV may be described by a normal distribution via *mean* and *std*. Stamina will likely become a resource (STM) that players can then spend each turn to determine their speed.

## Strategies
We want to balance three strategies:
- Offense: High ATK, low DEF, low HP, low REV
- Balanced: Moderate ATK, DEF, HP, REV
- Defense: High DEF, low ATK, high HP, high REV

SPD is independent of these strategies to increase strategy diversity. For example a fast tank may have different strengths and weaknesses than a slow tank. This will need balancing later, once specific cards are created.