import unittest
from itertools import product
from pathlib import Path

from oil_evidence.models import (
    capacity_path, first_shortfall, read_integers, sector_mix, us_history, world_history,
)


class ReserveTests(unittest.TestCase):
    def test_stock_flow_reconciliation_at_source_precision(self):
        rows = list(us_history(read_integers(Path("data/us_reserves.csv"))))
        self.assertEqual([row["year"] for row in rows], list(range(2014, 2025)))
        self.assertEqual(rows[0]["cumulative_since_base_mmbbl"], 0)
        self.assertEqual(rows[-1]["cumulative_since_base_mmbbl"], 40677)
        self.assertEqual(rows[-1]["implied_net_additions_since_base_mmbbl"], 46695)
        self.assertLessEqual(max(abs(r["balance_residual_mmbbl"]) for r in rows), 1)

    def test_unit_conversion_in_both_year_lengths(self):
        for year, days in [(2023, 365), (2024, 366)]:
            record = dict(year=year, production_thousand_bpd=1000,
                          closing_reserves_mmbbl=days * 10)
            row, = world_history([record])
            self.assertEqual(row["production_mmbbl"], days)
            self.assertEqual(row["rp_years"], 10)


class CapacityTests(unittest.TestCase):
    def test_flat_capacity_when_decline_is_replaced(self):
        path = list(capacity_path(0.04, 4.2, 0))
        for row in path:
            self.assertAlmostEqual(row["capacity"], 105)
        self.assertIsNone(first_shortfall(path))

    def test_delay_affects_first_two_deliveries(self):
        path = list(capacity_path(0.04, 3, 0, delay=2, years=3))
        self.assertAlmostEqual(path[2]["capacity"], 105 * 0.96**2)
        self.assertAlmostEqual(path[3]["capacity"], 105 * 0.96**3 + 3)
        self.assertEqual(first_shortfall(path), 2)

    def test_reference_and_declining_demand(self):
        self.assertEqual(first_shortfall(capacity_path(0.04, 3, 0)), 5)
        self.assertIsNone(first_shortfall(capacity_path(0.04, 3, -0.02)))

    def test_paths_match_independent_geometric_sum(self):
        for decline, additions, growth, delay in product(
                (0, 0.02, 0.04, 0.06), (1, 3, 5), (-0.02, 0, 0.01), (0, 2)):
            for row in capacity_path(decline, additions, growth, delay):
                t = row["year"]
                retained = 1 - decline
                capacity = 105 * retained**t + additions * sum(
                    retained**age for age in range(max(0, t-delay)))
                self.assertAlmostEqual(row["margin"], capacity - 100*(1+growth)**t)

    def test_zero_horizon_and_equality(self):
        self.assertEqual(len(list(capacity_path(1, 0, -1, years=0))), 1)
        self.assertIsNone(first_shortfall([{"year": 1, "margin": 0}]))
        with self.assertRaises(ValueError):
            list(capacity_path(1.1, 0, 0))


class SectorTests(unittest.TestCase):
    def test_only_specified_uses_change(self):
        result = sector_mix(103.7, 46, 15.5, 0.5, 0)
        self.assertAlmostEqual(result["total_mbd"], 80.7)
        self.assertEqual(result["chemicals_mbd"], 15.5)
        self.assertAlmostEqual(result["chemicals_share_pct"], 1550/80.7)
        self.assertIsNone(sector_mix(100, 100, 0, 1, 0)["chemicals_share_pct"])
