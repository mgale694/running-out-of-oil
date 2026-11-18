"""Volumes are million barrels unless a column explicitly states another unit."""
import calendar
import csv
from pathlib import Path


def read_integers(path: Path):
    with path.open(newline="") as stream:
        return [{key: int(value) for key, value in row.items()}
                for row in csv.DictReader(stream)]


def world_history(records):
    """Divide year-end crude reserves by crude produced during that calendar year."""
    for row in records:
        year = row["year"]
        days = 366 if calendar.isleap(year) else 365
        production = row["production_thousand_bpd"] * days / 1000
        yield dict(year=year, calendar_days=days, production_mmbbl=production,
                   reserves_mmbbl=row["closing_reserves_mmbbl"],
                   rp_years=row["closing_reserves_mmbbl"] / production)


def us_history(records):
    """Use the first year-end as the opening balance for the cumulative experiment."""
    opening = records[0]["closing_reserves_mmbbl"]
    cumulative = 0
    for index, row in enumerate(records):
        production = row["production_mmbbl"]
        closing = row["closing_reserves_mmbbl"]
        if index:
            cumulative += production
            change = closing - records[index - 1]["closing_reserves_mmbbl"]
            if change != row["reported_change_mmbbl"]:
                raise ValueError(f"Inconsistent reported stock change in {row['year']}")
        contributions = (row["revisions_other_mmbbl"] + row["net_acquisitions_mmbbl"]
                         + row["extensions_discoveries_mmbbl"] - production)
        yield dict(year=row["year"], reserves_mmbbl=closing, production_mmbbl=production,
                   rp_years=closing / production, cumulative_since_base_mmbbl=cumulative,
                   implied_net_additions_since_base_mmbbl=closing - opening + cumulative,
                   balance_residual_mmbbl=row["reported_change_mmbbl"] - contributions)


def capacity_path(decline, additions, growth, delay=0, years=10):
    """Capacity and demand are flow indices. Opening demand = 100, capacity = 105.

    'additions' is new flow capacity delivered each year after the start-up delay.
    Each commissioned cohort faces the same fractional decline from the next year.
    """
    if not (0 <= decline <= 1 and additions >= 0 and growth >= -1):
        raise ValueError("Invalid decline, additions or demand growth")
    if any(not isinstance(n, int) or n < 0 for n in (delay, years)):
        raise ValueError("Delay and horizon must be nonnegative whole years")
    capacity, demand = 105.0, 100.0
    for year in range(years + 1):
        if year:
            capacity *= 1 - decline
            if year > delay:
                capacity += additions
            demand *= 1 + growth
        yield dict(year=year, capacity=capacity, demand=demand, margin=capacity-demand)


def first_shortfall(path):
    """Return first annual observation with a negative margin, allowing for roundoff."""
    return next((row["year"] for row in path if row["margin"] < -1e-9), None)


def sector_mix(world, road, chemicals, road_reduction, chemicals_growth):
    """Vary two disjoint end-use categories; hold all other uses at their base."""
    if min(world, road, chemicals) < 0 or road + chemicals > world:
        raise ValueError("End-use components must fit inside the baseline total")
    if not 0 <= road_reduction <= 1 or chemicals_growth < -1:
        raise ValueError("Invalid demand shock")
    revised_chemicals = chemicals * (1 + chemicals_growth)
    revised_world = world - road * road_reduction + chemicals * chemicals_growth
    share = 100 * revised_chemicals / revised_world if revised_world else None
    return dict(total_mbd=revised_world, chemicals_mbd=revised_chemicals,
                chemicals_share_pct=share)
