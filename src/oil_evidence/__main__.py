"""Run from the repository root using make evidence."""
import csv
from itertools import product
from pathlib import Path

from .models import capacity_path, first_shortfall, read_integers, sector_mix, us_history, world_history


def save(name, rows):
    with (Path("outputs") / name).open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: round(v, 6) if isinstance(v, float) else v
                             for k, v in row.items()})


def main():
    Path("outputs").mkdir(exist_ok=True)
    us = list(us_history(read_integers(Path("data/us_reserves.csv"))))
    world = list(world_history(read_integers(Path("data/world_crude.csv"))))
    save("us_history.csv", us)
    save("world_history.csv", world)
    print("World crude, final static R/P (years):", round(world[-1]["rp_years"], 2))
    print("US closing reserves, cumulative production and implied additions (million bbl):",
          us[-1]["reserves_mmbbl"], us[-1]["cumulative_since_base_mmbbl"],
          us[-1]["implied_net_additions_since_base_mmbbl"])
    with Path("data/sector_baseline.csv").open(newline="") as stream:
        base, = csv.DictReader(stream)
    mix = []
    for reduction, growth in product((0, 0.10, 0.25, 0.50), (-0.20, 0, 0.20)):
        result = sector_mix(float(base["world_mbd"]), float(base["road_mbd"]),
                            float(base["petrochemicals_mbd"]), reduction, growth)
        mix.append(dict(base_year=base["year"], road_reduction=reduction,
                        chemicals_growth=growth, **result))
    save("sector_mix.csv", mix)
    paths = []
    sweep = []
    for decline, additions, growth, delay in product(
            (0.02, 0.04, 0.06), (1, 3, 5), (-0.02, 0, 0.01), (0, 2)):
        parameters = dict(decline=decline, additions=additions, growth=growth, delay=delay)
        path = list(capacity_path(**parameters))
        crossing = first_shortfall(path)
        sweep.append(dict(**parameters, first_shortfall_year=crossing,
                          year10_margin=path[-1]["margin"]))
        for row in path:
            paths.append(dict(**parameters, **row))
        if decline == 0.04 and additions == 3 and growth in (0, -0.02):
            print(parameters, "first negative margin:", crossing,
                  "year 10 margin:", round(path[-1]["margin"], 2))
    save("capacity_paths.csv", paths)
    save("sensitivity.csv", sweep)


if __name__ == "__main__":
    main()
