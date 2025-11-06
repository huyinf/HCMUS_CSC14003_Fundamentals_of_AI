"""
Shared constants and small utilities for Wumpus World logic projects.

This module centralizes:
- Canonical signal names and their opposites (W, P, S, B, G, A, V and -W, -P, -S, -B)
- Helpers to remove conflicting signals and normalize a cell's signal set
- A reader for map files in the FOL format (as used by fol_logic.py)
- Central scoring constants used across agents/visualization

Intended usage (example):
    from init import read_map, normalize_cell, SCORE_STEP

    grid, nG, nW = read_map('Input/map1.txt')
    grid[0][0] = normalize_cell(grid[0][0])

Newcomer notes:
- Positive signals: 'W' (Wumpus), 'P' (Pit), 'S' (Stench), 'B' (Breeze),
  'G' (Gold), 'A' (Agent), 'V' (Visited)
- Negative (safe) signals: '-W', '-P', '-S', '-B'
- A normalized cell should not contain both a positive and its negative counterpart
  (e.g., both 'W' and '-W').

Symbols:
- W: Wumpus present in this cell (lethal hazard)
- -W: No Wumpus in this cell (safe w.r.t. Wumpus)
- P: Pit present in this cell (lethal hazard)
- -P: No Pit in this cell (safe w.r.t. Pit)
- S: Stench perceived in this cell (some adjacent cell contains Wumpus)
- -S: No Stench perceived in this cell
- B: Breeze perceived in this cell (some adjacent cell contains Pit)
- -B: No Breeze perceived in this cell
- G: Gold present in this cell
- A: Agent is currently in this cell
- V: This cell has been visited by the agent
"""

from typing import List, Set, Tuple

# ---------------------------------------------------------------------------
# Canonical signal sets and opposites
# ---------------------------------------------------------------------------

# Positive signals observed or asserted in the grid
SIGNALS_POS: Set[str] = {"W", "P", "S", "B", "G", "A", "V"}

# Negative (safety) signals that denote absence of a hazard/symptom
SIGNALS_NEG: Set[str] = {"-W", "-P", "-S", "-B"}

# Opposite mapping (bidirectional) to ease conflict checks and transformations
OPPOSITE = {
    "W": "-W", "P": "-P", "S": "-S", "B": "-B",
    "-W": "W", "-P": "P", "-S": "S", "-B": "B",
}


# ---------------------------------------------------------------------------
# Conflict handling and cell normalization helpers
# ---------------------------------------------------------------------------
def remove_conflicts(signals: Set[str]) -> None:
    """
    In-place removal of contradictory signals from a cell.

    Policy: prefer safety (negative) over hazard (positive) when both appear.
            Example: if both 'W' and '-W' exist, keep '-W' and remove 'W'.
    Rationale: many reasoning steps add safety facts once hazards are disproved;
               keeping negatives avoids flipping back-and-forth in updates.
    """
    for pos, neg in (("W", "-W"), ("P", "-P"), ("S", "-S"), ("B", "-B")):
        if pos in signals and neg in signals:
            signals.discard(pos)


def normalize_cell(signals: Set[str]) -> Set[str]:
    """
    Return a normalized copy of the cell's signals with basic invariants:
    - Remove direct conflicts (prefer negatives via remove_conflicts)
    - If cell has Gold ('G'), it's safe from Wumpus/Pit at that cell
      (remove 'W'/'P', assert '-W'/'-P')
    - Ensure the result only contains known signals
    """
    s = set(signals)
    remove_conflicts(s)

    if "G" in s:
        # A gold cell cannot also be a hazard cell; mark safe instead
        s.discard("W"); s.discard("P")
        s.update({"-W", "-P"})

    # Filter out any unknown artifacts to keep cells clean
    allowed = SIGNALS_POS | SIGNALS_NEG
    return {x for x in s if x in allowed}


# ---------------------------------------------------------------------------
# Map I/O (FOL format) used by fol_logic.build_map
# ---------------------------------------------------------------------------
def read_map(path: str) -> Tuple[List[List[Set[str]]], int, int]:
    """
    Read a Wumpus map file and return (grid, nG, nW).

    File format (as used in fol_logic.py):
    - First line: size N (ignored here; we infer from data rows)
    - Next lines: grid rows; each row has dot-separated cell strings, e.g.:
        "A-S.B..G"  → will be split by '.' then each token -> set(chars)

    Each cell becomes a set of signals, then normalized via normalize_cell.
    Counts of Gold (G) and Wumpus (W) are computed from the normalized grid.
    """
    rows: List[List[str]] = []
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        # skip the first line (often size N); parse remaining lines
        rows = [
            [cell[:-1] if cell.endswith("\n") else cell for cell in line.split('.')]
            for line in lines[1:]
        ]

    grid: List[List[Set[str]]] = []
    for row in rows:
        grid.append([normalize_cell(set(cell)) for cell in row])

    nG = sum(1 for r in grid for c in r if "G" in c)
    nW = sum(1 for r in grid for c in r if "W" in c)
    return grid, nG, nW


# ---------------------------------------------------------------------------
# Scoring constants used by agents/visualization
# ---------------------------------------------------------------------------
# Step cost per move (forward) or tick
SCORE_STEP = -10

# Cost to shoot an arrow (consumes resource)
SCORE_SHOOT = -100

# Bonus for killing a Wumpus (if applicable in your scoring model)
SCORE_WUMPUS = 100

# Large penalty for death (falling into a pit or eaten by Wumpus)
SCORE_DEATH = -10000
