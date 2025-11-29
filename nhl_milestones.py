"""
Generate a simple CSV of NHL players, goalies, and coaches showing how close
they are to their next 100-stat milestones.

The script uses hard-coded sample data to keep dependencies light and focuses
on the fields needed for early betting-angle experiments: games played, goals,
assists, points, and wins (goalies/coaches only).
"""
from __future__ import annotations

import csv
from dataclasses import dataclass, field
from typing import Iterable, Optional


@dataclass
class PersonStats:
    name: str
    role: str
    team: str
    games_played: Optional[int] = None
    goals: Optional[int] = None
    assists: Optional[int] = None
    points: Optional[int] = None
    wins: Optional[int] = None
    closest_stat: Optional[str] = field(init=False, default=None)
    milestone_target: Optional[int] = field(init=False, default=None)
    remaining_to_milestone: Optional[int] = field(init=False, default=None)

    def compute_closest_milestone(self) -> None:
        milestones = {}
        for stat_name in ("games_played", "goals", "assists", "points", "wins"):
            value = getattr(self, stat_name)
            target, remaining = next_hundred_milestone(value)
            if remaining is not None:
                milestones[stat_name] = (target, remaining)

        if not milestones:
            return

        self.closest_stat, (self.milestone_target, self.remaining_to_milestone) = min(
            milestones.items(), key=lambda item: item[1][1]
        )


def next_hundred_milestone(value: Optional[int]) -> tuple[Optional[int], Optional[int]]:
    """Return the next 100-multiple milestone and the gap from the provided value."""
    if value is None:
        return None, None

    next_multiple = ((value // 100) + 1) * 100
    if value % 100 == 0:
        next_multiple = value + 100
    return next_multiple, next_multiple - value


def calculate_milestones(people: Iterable[PersonStats]) -> list[PersonStats]:
    results = []
    for person in people:
        person.compute_closest_milestone()
        results.append(person)
    return sorted(
        results,
        key=lambda p: (p.remaining_to_milestone if p.remaining_to_milestone is not None else float("inf"), p.name),
    )


def write_csv(people: Iterable[PersonStats], output_path: str = "nhl_milestones.csv") -> None:
    fieldnames = [
        "name",
        "role",
        "team",
        "games_played",
        "goals",
        "assists",
        "points",
        "wins",
        "closest_stat",
        "milestone_target",
        "remaining_to_milestone",
    ]

    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for person in people:
            writer.writerow({field: getattr(person, field) for field in fieldnames})


SAMPLE_STATS = [
    PersonStats(name="Connor Bedard", role="Forward", team="CHI", games_played=82, goals=39, assists=42, points=81),
    PersonStats(name="Connor McDavid", role="Forward", team="EDM", games_played=650, goals=335, assists=676, points=1011),
    PersonStats(name="Sidney Crosby", role="Forward", team="PIT", games_played=1230, goals=591, assists=960, points=1551),
    PersonStats(name="Auston Matthews", role="Forward", team="TOR", games_played=563, goals=368, assists=301, points=669),
    PersonStats(name="Cale Makar", role="Defense", team="COL", games_played=315, goals=100, assists=300, points=400),
    PersonStats(name="Igor Shesterkin", role="Goalie", team="NYR", games_played=210, goals=0, assists=8, points=8, wins=136),
    PersonStats(name="Andrei Vasilevskiy", role="Goalie", team="TBL", games_played=465, goals=0, assists=27, points=27, wins=293),
    PersonStats(name="Connor Hellebuyck", role="Goalie", team="WPG", games_played=445, goals=0, assists=20, points=20, wins=254),
    PersonStats(name="Rod Brind'Amour", role="Coach", team="CAR", games_played=410, wins=278),
    PersonStats(name="Jon Cooper", role="Coach", team="TBL", games_played=850, wins=480),
]


def main() -> None:
    sorted_people = calculate_milestones(SAMPLE_STATS)
    write_csv(sorted_people)
    print("Saved milestone snapshot to nhl_milestones.csv")


if __name__ == "__main__":
    main()
