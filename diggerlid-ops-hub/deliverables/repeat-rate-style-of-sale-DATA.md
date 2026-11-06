# DiggerLid repeat rate and style of sale: source data appendix

Generated 22 September 2026. All figures from Shopify analytics (ShopifyQL) unless stated. Windows: lifetime = 2019-01-01 to 2026-09-20; TTM = 2025-09-01 to 2026-08-31.

## A. Store repeat rate (EE definition: customers with more than one order)

| metric | lifetime | ttm |
|---|---|---|
| customers | 27061 | 14552 |
| customers_with_2plus_orders | 4790 | 3112 |
| repeat_rate_pct | 17.70 | 21.39 |
| orders | 34301 | 16698 |
| returning_orders | 7235 | 3949 |
| net_sales_aud | 10549164 | 4592722 |
| returning_net_sales_aud | 2070988 | 1103077 |

Query: `FROM sales SHOW orders, customers, net_sales GROUP BY new_or_returning_customer SINCE <start> UNTIL <end>` (Returning customers = customers who placed a non-first order in the window).

### A2. Orders per customer distribution (lifetime)

| orders_per_customer | customers |
|---|---|
| 1 | 22260 |
| 2 | 3358 |
| 3 | 907 |
| 4 | 311 |
| 5 | 107 |
| 6 | 64 |
| 7 | 26 |
| 8 | 11 |
| 9 | 7 |
| 10 | 5 |
| 13 | 2 |
| 14 | 1 |
| 16 | 2 |

Query: `FROM customers SHOW total_number_of_orders GROUP BY customer_number_of_orders SINCE 2019-01-01 UNTIL 2026-09-20` (customers = total_number_of_orders / bucket).

## B. Without grease

Excluded titles: KAJO Grease Packs, Battery Grease Gun KAJO Adapter, Quick Release Grease Coupler, KAJO Grease Gun, Hydraulic Coupling Cap Set, Pack Mine First, Package Protection, all GWP items.

| metric | lifetime | ttm |
|---|---|---|
| non_grease_buyers | 17926 | 8316 |
| returning_non_grease_buyers | 2485 | 1362 |
| repeat_rate_pct | 13.86 | 16.38 |
| non_grease_orders | 20445 | 8870 |
| non_grease_net_sales_aud | 6263275 |  |
| returning_non_grease_net_aud | 763843 |  |

## C. PRO Mat only (product id 8213717909674, live since 2025-08-25)

| metric | value |
|---|---|
| buyers_total | 3168 |
| buyers_first_order_new_to_brand | 2962 |
| buyers_on_returning_order | 270 |
| bought_on_first_and_again | 64 |
| promat_first_then_any_second_order | 141 |
| since_launch_cohort_customers | 3055 |
| since_launch_cohort_2plus | 235 |
| benchmark_all_customers_since_launch | 13650 |
| benchmark_2plus | 1440 |
| lifetime_customers | 3167 |
| lifetime_2plus | 347 |
| promat_orders_total | 3249 |

### C2. PRO Mat buyers, orders-per-customer distribution (lifetime)

| orders_per_customer | customers |
|---|---|
| 1 | 2820 |
| 2 | 246 |
| 3 | 57 |
| 4 | 25 |
| 5 | 8 |
| 6 | 2 |
| 7 | 3 |
| 8 | 1 |
| 9 | 2 |
| 10 | 1 |
| 14 | 1 |
| 16 | 1 |

Query: `FROM customers SHOW total_number_of_orders WHERE products_purchased MATCHES (id = 8213717909674) GROUP BY customer_number_of_orders SINCE <start> UNTIL 2026-09-20`.

## D. Product-set repeat (all time; repeat_orders_per_buyer_pct = orders/buyers - 1)

| set | buyers | orders | repeat_orders_per_buyer_pct |
|---|---|---|---|
| Grease system (packs, gun, adapter, coupler, caps) | 13300 | 17419 | 31.0 |
| Whole store | 27061 | 34301 | 26.8 |
| Covers (7 cover products) | 7035 | 7813 | 11.1 |
| Accessories (10 products) | 6236 | 6895 | 10.6 |
| Machine protection (all durables) | 13262 | 14556 | 9.8 |
| PRO Mat (portable protection) | 3168 | 3249 | 2.6 |

### D2. Products

| product | group | buyers | orders | repeat_orders_per_buyer_pct |
|---|---|---|---|---|
| KAJO Grease Packs | Grease | 8708 | 11039 | 26.8 |
| Battery Grease Gun KAJO Adapter | Grease | 7073 | 7668 | 8.4 |
| KAJO Grease Gun | Grease | 2059 | 2230 | 8.3 |
| Quick Release Grease Coupler | Grease | 6328 | 6582 | 4.0 |
| Hydraulic Coupling Cap Set | Accessories | 1460 | 1579 | 8.2 |
| Excavator Phone Cradle | Accessories | 3245 | 3418 | 5.3 |
| Digger Wipes | Accessories | 1029 | 1057 | 2.7 |
| Drink/ Tool Caddy | Accessories | 1515 | 1552 | 2.4 |
| Excavator Boom Bottle Opener | Accessories | 941 | 955 | 1.5 |
| Magnetic Tool Mat | Accessories | 172 | 177 | 2.9 |
| Trucker Cap | Accessories | 183 | 194 | 6.0 |
| DIGHEAD Beanie | Accessories | 116 | 121 | 4.3 |
| Proper Thicc Hoodie | Accessories | 56 | 56 | 0.0 |
| Work Tee | Accessories | 23 | 25 | 8.7 |
| Universal / Engine Covers | Covers | 935 | 1022 | 9.3 |
| Quicky Cover | Covers | 2383 | 2554 | 7.2 |
| Skid Steer Loader Cover | Covers | 233 | 248 | 6.4 |
| Mini Loader Cover | Covers | 808 | 857 | 6.1 |
| Draw Bar Cover | Covers | 921 | 944 | 2.5 |
| 1.7 Tonne Excavator Cover | Covers | 2503 | 2558 | 2.2 |
| Micro Excavator Cover | Covers | 270 | 274 | 1.5 |
| PRO Mat | Portable protection | 3168 | 3249 | 2.6 |
| Pro Excavator Enclosure | Other protection | 3248 | 3352 | 3.2 |
| DiggerShield Kit | Other protection | 622 | 644 | 3.5 |
| The Hauler Luggage Bag | Other protection | 73 | 74 | 1.4 |

### D3. Variants


**KAJO Grease Packs**

| variant | buyers | orders | repeat_pct |
|---|---|---|---|
| LZR2 | 4607 | 5240 | 13.7 |
| HD800 | 1452 | 1569 | 8.1 |
| LC002 | 1119 | 1234 | 10.3 |
| LZR2 / 20 pcs | 982 | 1056 | 7.5 |
| LC002 / 20 pcs | 368 | 393 | 6.8 |
| LC002 + 3% MOS2 | 310 | 332 | 7.1 |
| 9 pcs / 2050 | 252 | 260 | 3.2 |
| LZR2 / 40 pcs | 215 | 245 | 14.0 |
| 20 pcs / 2050 | 197 | 209 | 6.1 |
| CASX (580g) | 164 | 171 | 4.3 |
| Hammer Paste | 93 | 93 | 0.0 |
| LC002 + 3% MOS2 / 20 pcs | 87 | 98 | 12.6 |
| HD800 / 20 pcs | 86 | 86 | 0.0 |
| LC002 / 40 pcs | 66 | 76 | 15.2 |
| 40 pcs / 2050 | 64 | 73 | 14.1 |

**Battery Grease Gun KAJO Adapter**

| variant | buyers | orders | repeat_pct |
|---|---|---|---|
| Milwaukee 18v | 4481 | 4797 | 7.1 |
| Makita 18v | 1877 | 1936 | 3.1 |
| Ryobi 18v | 348 | 359 | 3.2 |
| DeWALT 18v | 327 | 330 | 0.9 |
| AEG 18v | 154 | 154 | 0.0 |
| 400g Guns 18v/20v | 130 | 135 | 3.8 |
| Macnaught 18v | 102 | 108 | 5.9 |
| Metabo 18v | 40 | 41 | 2.5 |

**Quicky Cover**

| variant | buyers | orders | repeat_pct |
|---|---|---|---|
| (default) | 2026 | 2158 | 6.5 |
| Tan | 238 | 239 | 0.4 |
| Black | 94 | 96 | 2.1 |
| Grey Camo | 63 | 63 | 0.0 |

**Universal / Engine Covers**

| variant | buyers | orders | repeat_pct |
|---|---|---|---|
| 450x450x450mm | 598 | 633 | 5.9 |
| 600x600x450mm | 491 | 519 | 5.7 |


Query: `FROM sales SHOW orders, customers, net_sales GROUP BY product_title [, product_variant_title] SINCE 2019-01-01 UNTIL 2026-09-20`.

## E. Sale curves (net sales AUD, orders; New vs Returning)


### EOFY 2026 (launch 2026-06-17 13:55 AEST, close 2026-06-30)

| day_index | date | net_new | orders_new | net_returning | orders_returning | net_total | pct_of_sale | returning_rev_share_pct |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-06-17 | 46649.11 | 160 | 21595.41 | 68 | 68244.52 | 12.56 | 31.6 |
| 2 | 2026-06-18 | 26209.66 | 123 | 10949.93 | 39 | 37159.59 | 6.84 | 29.5 |
| 3 | 2026-06-19 | 19235.34 | 92 | 11722.43 | 41 | 30957.77 | 5.70 | 37.9 |
| 4 | 2026-06-20 | 17118.93 | 83 | 5031.96 | 17 | 22150.89 | 4.08 | 22.7 |
| 5 | 2026-06-21 | 20696.75 | 107 | 7292.50 | 28 | 27989.25 | 5.15 | 26.1 |
| 6 | 2026-06-22 | 18493.61 | 99 | 7126.54 | 29 | 25620.15 | 4.71 | 27.8 |
| 7 | 2026-06-23 | 16388.23 | 90 | 5568.23 | 28 | 21956.46 | 4.04 | 25.4 |
| 8 | 2026-06-24 | 18548.70 | 86 | 10547.03 | 30 | 29095.73 | 5.35 | 36.2 |
| 9 | 2026-06-25 | 15310.98 | 76 | 11111.00 | 25 | 26421.98 | 4.86 | 42.1 |
| 10 | 2026-06-26 | 19761.27 | 64 | 5758.53 | 27 | 25519.80 | 4.70 | 22.6 |
| 11 | 2026-06-27 | 14368.68 | 69 | 5677.06 | 21 | 20045.74 | 3.69 | 28.3 |
| 12 | 2026-06-28 | 26108.03 | 95 | 10456.80 | 32 | 36564.83 | 6.73 | 28.6 |
| 13 | 2026-06-29 | 48123.53 | 170 | 14774.20 | 52 | 62897.73 | 11.58 | 23.5 |
| 14 | 2026-06-30 | 80497.87 | 254 | 28262.28 | 102 | 108760.15 | 20.02 | 26.0 |

### BFCM 2025 (launch 2025-11-18 15:05 AEDT, close 2025-12-01)

| day_index | date | net_new | orders_new | net_returning | orders_returning | net_total | pct_of_sale | returning_rev_share_pct |
|---|---|---|---|---|---|---|---|---|
| 1 | 2025-11-18 | 67384.73 | 171 | 28339.71 | 80 | 95724.44 | 17.91 | 29.6 |
| 2 | 2025-11-19 | 59768.46 | 164 | 12593.78 | 53 | 72362.24 | 13.54 | 17.4 |
| 3 | 2025-11-20 | 32343.71 | 108 | 8099.79 | 32 | 40443.50 | 7.57 | 20.0 |
| 4 | 2025-11-21 | 28973.21 | 101 | 5331.75 | 21 | 34304.96 | 6.42 | 15.5 |
| 5 | 2025-11-22 | 25142.50 | 94 | 3748.24 | 15 | 28890.74 | 5.40 | 13.0 |
| 6 | 2025-11-23 | 23398.33 | 85 | 5502.88 | 18 | 28901.21 | 5.41 | 19.0 |
| 7 | 2025-11-24 | 19268.29 | 66 | 2872.75 | 14 | 22141.04 | 4.14 | 13.0 |
| 8 | 2025-11-25 | 18504.39 | 61 | 10826.03 | 33 | 29330.42 | 5.49 | 36.9 |
| 9 | 2025-11-26 | 23594.41 | 85 | 5290.68 | 21 | 28885.09 | 5.40 | 18.3 |
| 10 | 2025-11-27 | 19845.00 | 66 | 3182.60 | 20 | 23027.60 | 4.31 | 13.8 |
| 11 | 2025-11-28 | 20914.05 | 72 | 410.69 | 18 | 21324.74 | 3.99 | 1.9 |
| 12 | 2025-11-29 | 22501.98 | 75 | 5306.97 | 16 | 27808.95 | 5.20 | 19.1 |
| 13 | 2025-11-30 | 25630.43 | 84 | 4178.20 | 9 | 29808.63 | 5.58 | 14.0 |
| 14 | 2025-12-01 | 29463.01 | 105 | 22167.60 | 72 | 51630.61 | 9.66 | 42.9 |


Pre-sale baseline net/day: EOFY (13-16 Jun) 10906; BFCM (13-17 Nov) 7136. BAU reference Aug 2026: net 454597.24, returning net 111217.31, orders 1650, returning orders 409.


EE reference curves (approximate traces of the Style of Sale slides, 12-day sale, % of revenue per day):

| day | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hybrid | 30 | 17 | 10 | 8.5 | 6.5 | 5.5 | 5 | 4.5 | 4 | 4.5 | 5 | 6 |
| low_repeat | 20 | 14 | 9.5 | 8.5 | 8 | 7.5 | 7.5 | 7.5 | 7 | 6.5 | 6 | 5.5 |
| high_repeat | 41 | 20 | 9 | 8 | 6 | 3 | 2.5 | 2 | 1.5 | 5 | 3 | 4 |

Query: `FROM sales SHOW net_sales, orders GROUP BY new_or_returning_customer TIMESERIES day SINCE <launch> UNTIL <close> ORDER BY day ASC`.

## F. Klaviyo send log used to define sale windows

| sale | send | date |
|---|---|---|
| EOFY 2026 | Account warming (Engaged 180D) | 2026-06-10 |
| EOFY 2026 | Hype #1 AU/INT | 2026-06-15 |
| EOFY 2026 | Launch #1 AU/INT | 2026-06-17 |
| EOFY 2026 | Plain text follow #1 | 2026-06-19 |
| EOFY 2026 | Email #3 grease customers | 2026-06-21 |
| EOFY 2026 | Mid email #4 | 2026-06-24 |
| EOFY 2026 | Plain text follow #2 | 2026-06-28 |
| EOFY 2026 | Last day #6 / Thank you #7 | 2026-06-30 |
| BFCM 2025 | Hype #1 | 2025-11-15 |
| BFCM 2025 | Hype #2 | 2025-11-16 |
| BFCM 2025 | Launch | 2025-11-18 |
| BFCM 2025 | Plain text 24h after launch | 2025-11-19 |
| BFCM 2025 | Mid sale #1 (Engaged 30D) | 2025-11-25 |
| BFCM 2025 | Black Friday | 2025-11-28 |

## G. Ecommerce Equation bands

| band | repeat_rate | share_of_ee_cohort_pct |
|---|---|---|
| Low repeat | 0-19% | 25 |
| Hybrid | 20-39% | 48 |
| High repeat | 40%+ | 27 |
