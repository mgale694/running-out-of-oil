"""Regenerate figures from make evidence. Requires Matplotlib."""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

OUT = Path("outputs")
plt.rcParams.update({"axes.spines.top": False, "axes.spines.right": False,
                     "font.size": 11, "axes.titlelocation": "left",
                     "axes.labelcolor": "#36454f", "axes.axisbelow": True})


def read(name):
    with (OUT / name).open(newline="") as stream:
        return list(csv.DictReader(stream))


def finish(fig, ax, title, subtitle, source, filename):
    fig.subplots_adjust(left=.10, right=.96, top=.76, bottom=.22)
    fig.text(.10, .92, title, fontsize=18, weight="bold", color="#172f43")
    fig.text(.10, .84, subtitle, fontsize=11)
    fig.text(.10, .05, source, fontsize=9, color="#425563")
    ax.grid(axis="y", alpha=.22)
    ax.legend(frameon=False, fontsize=10)
    fig.savefig(OUT / filename, dpi=160)
    plt.close(fig)


us = read("us_history.csv")
years = [int(r["year"]) for r in us]
fig, ax = plt.subplots(figsize=(9.2, 5.3))
for col, label, colour, style in [
        ("reserves_mmbbl", "Proved reserves at year-end", "#11665f", "-"),
        ("cumulative_since_base_mmbbl", "Cumulative production since end-2014", "#a64b21", "--")]:
    ax.plot(years, [float(r[col])/1000 for r in us], style, color=colour, lw=2.7, label=label)
ax.set(ylabel="Billion barrels", ylim=(0, 56), xticks=years[::2], xlim=(2014, 2024))
finish(fig, ax, "A decade of production, a higher reserve balance",
       "US crude oil and lease condensate, 2014–24",
       "Source: EIA, year-end 2024 reserves report, Table 5. Cumulative production starts at zero.",
       "us-reserves.png")

paths = read("capacity_paths.csv")
fig, ax = plt.subplots(figsize=(9.2, 5.3))
for growth, delay, label, colour, style in [
        (0, 0, "Flat demand", "#275775", "-"),
        (0, 2, "Flat demand, two-year delivery delay", "#ad5428", "--"),
        (-0.02, 0, "Demand falls 2% per year", "#087668", "-.")]:
    case = [r for r in paths if float(r["growth"]) == growth and int(r["delay"]) == delay
            and float(r["decline"]) == .04 and int(r["additions"]) == 3]
    ax.plot([int(r["year"]) for r in case], [float(r["margin"]) for r in case],
            style, color=colour, lw=2.6, label=label)
ax.axhline(0, color="#2f3436", lw=.9)
ax.set(xlabel="Year of experiment", ylabel="Capacity minus demand (index points)", xlim=(0, 10))
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
finish(fig, ax, "How quickly can spare capacity disappear?",
       "Illustrative paths with opening capacity of 105 and demand of 100",
       "Assumptions: 4% annual capacity decline and 3 new flow units per year once deliveries start.",
       "capacity-margin.png")
