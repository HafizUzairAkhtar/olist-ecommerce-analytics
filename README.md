# Olist E-Commerce — Data Cleaning & Sales Dashboard

End-to-end analytics project on the [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce): ~100k real orders, 9 relational tables, Sept 2016 – Oct 2018. The raw export was cleaned with pandas and turned into a one-page Looker Studio dashboard.


---

## Problem

The client (an e-commerce marketplace operator) wanted a single page that answers five questions: *How is revenue trending? How many orders do we take each month? Which products earn the most? Where does our revenue come from? How long do customers wait for delivery?*

The data existed, but the raw Kaggle export could not be trusted to feed a dashboard:

- 261,831 exact duplicate rows in the geolocation table, and 814 customer reviews attached to more than one order (which double-counts review scores).
- 610 products with no category label, two categories with no English translation, and 8 orders marked "delivered" with no delivery date — any of which silently distorts averages and drops revenue off category charts.
- All 8 timestamp columns stored as text, so delivery times and monthly trends could not be calculated at all.
- Monetary columns with no currency unit, and 303 orders where payments did not reconcile to item totals.

## What I did

1. **Profiled every table** for duplicates, nulls, dtypes and referential gaps, and separated *meaningful* missing values (a cancelled order has no delivery date) from *data-quality* ones (a delivered order with no delivery date).
2. **Fixed each problem in its own documented section** of the notebook, so every change can be audited:
   - *Duplicates* — dropped exact duplicates; kept one review per order (the most recently answered).
   - *Nulls* — explicit `unknown` category so no revenue disappears; added the missing translations; flagged impossible delivery records; replaced empty review text with a `has_comment` flag.
   - *Date types* — parsed all timestamps to `datetime64`; derived `purchase_month`, `delivery_days`, `delivery_delay_days`, `delivered_on_time`.
   - *Currency* — explicit `_brl` columns rounded to cents, a `_usd` column at a documented reference rate (1 USD = 3.65 BRL, changeable in one constant), and a `payment_mismatch` flag instead of silently altering either side.
3. **Built two dashboard-ready tables** — an order-level fact table (98,199 billable orders) and a top-10 product table — then aggregated them to monthly, state and product grain so they load into Google Sheets as a lightweight source.
4. **Designed the one-page dashboard** in Looker Studio with five tiles: revenue trend, orders by month, top 10 products, revenue by region (Brazilian state → IBGE region), and average delivery days.

## What the client would see

- **Revenue:** R$ 15.7M across 98,199 orders. Monthly revenue grew ~8× from Jan 2017 to a Black Friday peak of R$ 1.17M in Nov 2017, then held at R$ 1.0–1.15M/month through 2018.
- **Orders by month:** a sustained 6,000–7,400 orders/month in 2018, up from under 1,000 in early 2017.
- **Top products:** the two highest-earning products are both in health & beauty; computers and accessories make up three of the top ten.
- **Revenue by region:** the Southeast (São Paulo, Rio, Minas) accounts for 65% of revenue; São Paulo alone is 37%.
- **Delivery:** the average order takes **12.6 days** to reach the customer, with 91.9% arriving on or before the promised date. São Paulo averages 8.8 days; states in the North and Northeast average 17–29 days, which is where delivery investment would have the most impact.

Every number on the dashboard traces back to a cell in the notebook, and the before/after summary table in section 7 shows exactly what was changed in each table.

## Tools

| Stage | Tool |
|-------|------|
| Data | Kaggle — Olist Brazilian E-Commerce dataset |
| Cleaning & analysis | Python 3, pandas, NumPy, Jupyter |
| Dashboard source | Google Sheets |
| Dashboard | Looker Studio (free, shareable by link) |
| Versioning | Git / GitHub |

## Repository layout

```
olist_data_cleaning.ipynb      the cleaning notebook (executed, with outputs)
data/dashboard/                monthly.csv, revenue_by_state.csv, top_products.csv, kpi.csv
src/build_dashboard_tables.py  rebuilds the aggregate tables from the order-level fact table
docs/looker_studio_setup.md    how the dashboard was built, tile by tile
images/                        dashboard screenshot
```

## Reproduce

```bash
pip install -r requirements.txt
# download the Kaggle dataset and unzip it into data/raw/
jupyter notebook olist_data_cleaning.ipynb      # run all cells → data/clean/, data/dashboard/
python src/build_dashboard_tables.py            # rebuild the aggregate tables
```
