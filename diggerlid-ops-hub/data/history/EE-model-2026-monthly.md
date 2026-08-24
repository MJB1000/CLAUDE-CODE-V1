# EE 7.1 (Accelerate) — 2026 Monthly Totals snapshot

**Ingested:** 2026-08-12 from `DiggerLid Calendar 2026 Ecommerce Equation 7.1 Accelerate.xlsx`
(sheet "2026 Monthly Totals"). July final; **August is month-to-date (~as of 11 Aug)**; Sep–Dec blank.

**Basis note:** MER and VCR below are the model's *displayed* values (GST-inclusive revenue),
which flatter both by ~9% vs the ex-GST P&L basis. Ex-GST MER = Meta ÷ Revenue-ex-GST.

| Month | Rev ex-GST | Orders | Sessions | CVR | AOV | Meta spend | MER (incl) | MER (ex-GST) | VCR (incl) | Fixed | Net profit |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| Jan | 241,767 | 778 | 29,662 | 2.6% | 337.67 | 48,162 | 18.3% | 19.9% | 43.6% | 49,342 | +29,844 |
| Feb | 306,489 | 996 | 39,279 | 2.5% | 332.71 | 84,528 | 25.5% | 27.6% | 41.5% | 53,494 | +31,039 |
| Mar | 311,480 | 1,034 | 36,742 | 2.8% | 327.66 | 100,167 | 29.6% | 32.2% | 43.8% | 61,752 | +1,246 |
| Apr | 341,520 | 1,054 | 42,601 | 2.5% | 352.25 | 108,200 | 29.1% | 31.7% | 46.1% | 59,760 | +2,426 |
| May | 416,322 | 1,551 | 76,994 | 2.0% | 291.67 | 122,897 | 27.2% | 29.5% | 46.7% | 73,605 | +8,758 |
| Jun | 807,148 | 3,213 | 125,170 | 2.6% | 272.97 | 199,702 | 22.8% | 24.7% | 46.1% | 71,231 | +132,328 |
| Jul (final) | 383,948 | 1,654 | 116,417 | 1.4% | 252.24 | 162,275 | 38.9% | 42.3% | 43.7% | 74,831 | **−35,540** |
| Aug (MTD) | 144,208 | 433 | 40,913 | 1.1% | 361.89 | 47,041 | 30.0% | 32.6% | 39.7% | 26,553 | +8,460* |

\* August profit is month-to-date on partial fixed costs; not a full-month figure.

**YTD (Jan–Aug):** Revenue ex-GST $2,952,882 · Net profit **+$178,560** (June carries the year).

## Reconciliation notes
- **July revised** vs prior lock: rev ex-GST $382,884 → **$383,948**; MER 0.424 → **0.4226**; net now **−$35.5k** (deeper than the ~−$25/−31k earlier estimates). `forecast_engine.py` ACTUALS updated.
- **Blended product cost ~34%** (Jul 34.1%, Aug 33.6%) — confirms Pro Mat COGS headroom vs the 42.8% break-even used in the Father's Day margin logic (per-SKU still to confirm).
- **Fixed ~$74,831/mo** confirmed. **VCR** (ex-GST) assumptions in the engine (0.468 BAU / 0.503 sale) remain consistent with the model's GST-inclusive VCR.
- August MTD in the model matches our live daily tracking (AOV ~$362, CVR ~1.1%); the forward forecast (2026-W33) is unaffected by the July revision (~$1k, immaterial to H2).
