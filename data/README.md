# Input provenance

Extracted 18 November 2026. Each CSV preserves one publication vintage. All input rows are reported historical estimates. No forward projection is included in the input files.

| File | Source and locator | Units and coverage |
| --- | --- | --- |
| us_reserves.csv | US EIA, *US Crude Oil and Natural Gas Proved Reserves, Year-End 2024*, Table 5, all eleven US rows and all six numerical columns. [Original table](https://www.eia.gov/naturalgas/crudeoilreserves/pdf/ARR_2024_TABLE_05.pdf) | Million barrels. Crude oil **and lease condensate**. End-December reserves and calendar-year production estimated from the reserves survey EIA-23L. EIA's Petroleum Supply Annual uses a different survey. |
| world_crude.csv | OPEC *Annual Statistical Bulletin 2025*, Table 3.1 p.22 and Table 3.5 p.26, “Total world” row, 2020–24. [Bulletin](https://www.opec.org/assets/assetdb/asb-2025.pdf) | End-year proven crude reserves in million barrels and annual-average crude production in thousand barrels/day. Preserve OPEC's country and product definitions, including the Canadian oil-sands exclusion on the reserve table. The denominator is crude production. Total liquids demand has broader coverage. |
| sector_baseline.csv | OPEC *World Oil Outlook 2025*, Table 3.3 p.132, 2024 column, World, Road and Petrochemicals rows. [Table](https://www.opec.org/assets/assetdb/woo-2025-1.pdf) | Million barrels/day of oil demand. Road and petrochemicals are disjoint subcategories. Other uses are the residual of the rounded world total. Avoid double-counting subgroup totals. |

The historical comparisons end in 2024 deliberately. The bulletin editions, US survey and demand table use different definitions. Compare within each experiment. OPEC's 2026 bulletin also reports 2025 production and demand; adding a single newer figure to a frozen time series would mix vintages. [2026 release](https://www.opec.org/pr-detail/601-29-april-2026.html)
