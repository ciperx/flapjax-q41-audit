# FlapJax Receipt Relay Q41 - 14-day buyback audit (10-09 to 10-22, program days in COT)

Treasury `0x7C34E9e21eE28A49Ff0b84B61774119E6633359f`, pool PancakeSwap V3 FLAPJAX/WBNB 1% `0xcA93EC685b8623688E6B236f9068034B298c2150`.

Every row below was decoded from the pool's `Swap` event and the treasury's own receipts on BSC; block numbers let anyone re-check each one on BscScan.

## Every buyback swap

| # | UTC | COT (UTC-5) | block | tx | BNB in | FLAPJAX out | effective BNB/FJ | pool price before |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-10-09 18:30:53Z | 2026-10-09 13:30:53 | 126684151 | `0xbeefabdc89f9148f9daaef6082d34a60dc5b4b612972ca0fd39d6bd4eb03b4b0` | 0.01 | 24052995.3083 | 4.1575e-10 | 4.1097e-10 |
| 2 | 2026-10-10 18:27:56Z | 2026-10-10 13:27:56 | 126875701 | `0x8ce8e8578da26f8c7acb0f44c6ca0d0b8dcba868cafe2d729bb48562863f2d62` | 0.01 | 23979958.5574 | 4.1701e-10 | 4.1222e-10 |
| 3 | 2026-10-11 18:30:35Z | 2026-10-11 13:30:35 | 127067713 | `0x82d01172ae26f1c86287643e123af1675ca5c18b984b7740c1a0c1647d2801eb` | 0.01 | 23907253.9656 | 4.1828e-10 | 4.1347e-10 |
| 4 | 2026-10-12 18:46:27Z | 2026-10-12 13:46:27 | 127261246 | `0x9afdc96e3ca876b5b617a26ba5105012ed8c33e805c77b1616bf48c198d5cbf1` | 0.01 | 23834879.5218 | 4.1955e-10 | 4.1473e-10 |
| 5 | 2026-10-13 18:41:15Z | 2026-10-13 13:41:15 | 127452454 | `0xc94de373d1fb00093431224a97475b3b2b48b9a4962d15acbe9d9c5c016d720c` | 0.01 | 23762833.2300 | 4.2083e-10 | 4.1599e-10 |
| 6 | 2026-10-14 18:32:29Z | 2026-10-14 13:32:29 | 127643212 | `0x172349c64ed3c45663650049f9e2ad3d763b1243c5c849b7d66f144f221d3186` | 0.01 | 23691113.1095 | 4.2210e-10 | 4.1725e-10 |
| 7 | 2026-10-17 02:00:51Z | 2026-10-16 21:00:51 | 128086717 | `0xc999000f16f326e8868fe37f83871219be1a63f98043b0aef9ee57f469232156` | 0.01 | 23669235.4659 | 4.2249e-10 | 4.1763e-10 |
| 8 | 2026-10-17 13:29:27Z | 2026-10-17 08:29:27 | 128178495 | `0x6ec66780e0518da7c3c8b55d13b66d57400046f89ebe9df479c3c878f7b3311f` | 0.01 | 23597938.3497 | 4.2377e-10 | 4.1890e-10 |
| 9 | 2026-10-18 13:28:39Z | 2026-10-18 08:28:39 | 128370339 | `0x05a9acf81b0eae4b7ff9a12168aead25964b6b2c0a16d3d1e667b7db6f17ad99` | 0.01 | 23506585.1567 | 4.2541e-10 | 4.2053e-10 |
| 10 | 2026-10-19 09:28:47Z | 2026-10-19 04:28:47 | 128530306 | `0xd5210869e5cec642146b3f39590647b313d102f70a51b7c7bbf0c287ceff095d` | 0.01 | 23545510.4210 | 4.2471e-10 | 4.1983e-10 |
| 11 | 2026-10-20 13:29:06Z | 2026-10-20 08:29:06 | 128754269 | `0xe9ea4a165aae8eb4228ef073a93c4c1983894104a426e9f5d64b0214cfde3369` | 0.01 | 23439984.3303 | 4.2662e-10 | 4.2172e-10 |
| 12 | 2026-10-21 13:29:29Z | 2026-10-21 08:29:29 | 128946201 | `0xbf984ef91d8df34f75998aa40bb539db84085cc1f1654cd5106de7e3db0be48f` | 0.01 | 23429832.7347 | 4.2681e-10 | 4.2190e-10 |
| 13 | 2026-10-22 18:26:28Z | 2026-10-22 13:26:28 | 129177690 | `0x594519c2b2179e7a31f25221de1c979f5b87027641bd846c1c7029e5f7e297b2` | 0.01 | 23435077.9716 | 4.2671e-10 | 4.2181e-10 |

**Totals: 0.13 BNB spent, 307853198.1225 FLAPJAX received across 13 buys.**

## Rule by rule

| Rule announced 10-08 | Verdict | Evidence |
|---|---|---|
| each buy spends 0.01 BNB | **KEPT** | all 13 swaps carry exactly `10000000000000000` wei of WBNB in |
| buy only, never sell FLAPJAX back into the pool | **KEPT** | in all 13 treasury swaps `amount0` (FLAPJAX) is negative and `amount1` (WBNB) is positive; no swap with FLAPJAX flowing into the pool from the treasury in the window |
| at most one buy per program day, counted in COT | **KEPT** | 13 buys on 13 distinct COT days, exactly one per day (10-09 .. 10-22) |
| skip a day if it would leave the treasury under 0.025 BNB | **NOT TRIGGERED, but one day was missed** | treasury BNB before each buy ranged 0.046165 to 0.284743, never under 0.025, so the floor never justified a skip. Program day **2026-10-15 (COT) has no buy** while the balance that day was above the floor - that is a **BROKEN** day-count: 14 program days, 13 buys |

## Days

Program days 10-09 .. 10-22 = **14**. Days with a buy: **13**. Days missed: **1** (2026-10-15 COT).

## What I could not classify

- The treasury's BNB balance moved between program days for reasons other than the buybacks (inflows and outflows); I read the balance immediately before and after each buy, which is what the floor rule needs, and did not attempt to explain every transfer.

- No sell of FLAPJAX by the treasury into this pool exists in the window. Transfers of FLAPJAX out of the treasury to other addresses are not pool sells and are out of scope.

## How to re-check

1. Open the pool `0xcA93EC685b8623688E6B236f9068034B298c2150` on BscScan and read the `Swap` event at each block above.

2. `amount0` is FLAPJAX (token0, 18 decimals), `amount1` is WBNB (token1, 18 decimals).

3. Effective price = BNB in / FLAPJAX out, both 18 decimals: `10000000000000000 / amount0`.

4. Pool price before = price from `slot0.sqrtPriceX96` read at block-1: `(sqrtPriceX96 / 2^96)^2` gives token1 per token0 in raw units; invert and scale by 10^18 for BNB per FLAPJAX.

5. Raw rows: `buys_raw.json` in this repository, produced by `analyze.py` (RPC: bsc-mainnet.public.blastapi.io, archive reads included).
