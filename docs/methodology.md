# Methodology

## 1. A stock divided by a flow

For each world year, multiply average thousand barrels/day by actual calendar days and divide by 1,000 to get million barrels/year. Divide the closing reserve balance by that flow. For 2024 the calculation is 1,566,869 / (72,584 × 366 / 1,000) = 58.98 years. The estimate holds extraction fixed and excludes future reserve changes. The 2020–24 observations range from 58.44 to 61.50. The pandemic-era production base, reporting conventions, country estimates and selected window affect this range. No depletion year follows from it.

## 2. Reconcile booked reserves with physical production

Closing reserves = opening reserves + extensions/discoveries + revisions/other changes + net acquisitions − production + rounding. Net acquisitions are the reporting survey's net figure. EIA labels revisions/other changes as a balancing item. Reserve additions should never be relabelled as discoveries. Proved reserves are only a subset of the physical resource.

Take end-2014 as the opening stock and sum production from 2015 through 2024 inclusive. Adding 2014 production to this flow would count barrels extracted before the start. In billion barrels the bridge is 39.933 + 46.695 − 40.677 = 45.951. The 46.695 is the implied net addition across all categories, including rounding. Annual source components reproduce the reported changes to within one million barrels; the exported residual preserves the signed differences. Changes in booked reserves do not measure physical replenishment or imply that US geology represents the world.

## 3. Deliverable flow and demand

Year zero starts with capacity C = 105 and demand D = 100. Both measure a flow relative to opening demand. In year t, C(t) = (1 − d) × C(t−1) + A(t), and D(t) = D(t−1) × (1 + g). A(t) is zero through the delay and equals a fixed addition thereafter. A two-year delay shifts the commissioning stream from years 1, 2, … to 3, 4, … . The annual additions are index points of capacity. New capacity also declines from the following year.

Sweep the Cartesian product of decline d in {2%, 4%, 6%}, additions in {1, 3, 5}, growth g in {−2%, 0%, 1%}, and delay in {0, 2} years. These are analyst-chosen stress settings; they do not represent investment forecasts or the IEA's field-level estimates. Capacity minus demand is positive when capacity exceeds planned use. Record the first negative annual observation; a blank means no crossing inside ten years. A tolerance of 1e-9 index points treats floating-point zero as zero.

The tests check the recurrence against a geometric sum over commissioned cohorts. Across the selected grid 35 paths cross and 19 do not. The count changes with grid design and carries no probability. With 4% decline, three annual additions and flat demand, the year-ten margin is −5.06. With the same capacity and demand falling 2% annually, it is +13.24. The alternative two-year delivery delay with flat demand gives −9.30. Distinguish capacity from actual production and intended demand from realised consumption. Market clearing, prices, inventory buffers, spare-capacity policy, trade and feedback into investment are outside this experiment. The model diagnoses the size of adjustment required under its assumptions.

To isolate the effect of building less capacity in a shrinking market, hold decline at 4%, demand growth at −2% and delay at zero. With one new flow unit annually from year one, the margin first turns negative in year five and reaches −3.52 index points in year ten. With three units, it stays positive and ends at +13.24. Both rows already appear in the [grid](../outputs/sensitivity.csv). These schedules are assumptions. A falling demand path alone does not determine project approvals or prices.

## 4. Persistent uses under substitution

Start from 103.7 million barrels/day, of which road transport accounts for 46.0 and petrochemicals for 15.5. Apply a proportional road reduction from {0%, 10%, 25%, 50%} and a petrochemical change from {−20%, 0%, +20%}. Hold all remaining uses constant. Recalculate both volume and share. With a 50% road reduction and 20% petrochemical reduction, chemical demand falls to 12.4 while its share rises to about 16% of 77.6. This is a composition effect. It establishes neither the crude feedstock of a particular product nor a ranking of social value. Fuel displaced in one use cannot automatically be delivered in a different grade or place.

## Checks before reusing a result

Record the Git revision, input edition, output row and unit. Compare levels at the same geography and product coverage. For any price or affordability claim, bring evidence on delivered prices, costs or constrained buyers. Nothing in the capacity equation maps an index point into a currency amount.
