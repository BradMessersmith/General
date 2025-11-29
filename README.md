# This is a general repository for various items

## NHL milestone snapshot prototype
A lightweight script, `nhl_milestones.py`, builds a CSV of sample NHL players,
goalies, and coaches sorted by how close they are to their next 100-stat
milestone. Stats include games played, goals, assists, points, and wins (for
goalies or coaches).

**To generate the CSV:**

```bash
python nhl_milestones.py
```

Running the script creates `nhl_milestones.csv` in the repository root, ready
for ad-hoc milestone/odds comparisons.
