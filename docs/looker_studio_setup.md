# Building the dashboard in Looker Studio

The dashboard reads three Google Sheets (created from `data/dashboard/`):

| Sheet | Feeds | Key columns |
|-------|-------|-------------|
| Olist Dashboard - Monthly | Revenue trend, Orders by month, Average delivery days | `month` (date), `orders`, `revenue_brl`, `delivered_orders`, `delivery_days_total` |
| Olist Dashboard - Revenue by State | Revenue by region | `customer_state`, `state_iso` (BR-SP…), `customer_region`, `revenue_brl` |
| Olist Dashboard - Top Products | Top 10 products | `product_label`, `revenue_brl`, `units_sold` |

## 1. Create the report and connect the data

1. Go to <https://lookerstudio.google.com> → **Create** → **Report**.
2. In the connector list choose **Google Sheets** → pick **Olist Dashboard - Monthly** → worksheet `Olist Dashboard - Monthly` → tick *Use first row as headers* → **Add**.
3. Rename the report (top-left) to **Olist E-Commerce — Sales & Delivery Overview**.
4. Add the other two sources: **Add data** (toolbar) → Google Sheets → *Olist Dashboard - Revenue by State* → Add; repeat for *Olist Dashboard - Top Products*.
5. Open **Resource → Manage added data sources → Edit** on the Monthly source and check that `month` has type **Date** (not Text). If it shows Text, change it to *Date (YYYY-MM-DD)*. Set `revenue_brl` and `revenue_usd` to **Currency (BRL)** / **Currency (USD)**.

## 2. Add the five tiles

Page size: **File → Report settings** or Theme and layout → Canvas size 1200 × 900 works well. Suggested layout: the trend chart full width on top, four tiles in a row underneath.

### Tile 1 — Revenue trend (time series)
*Insert → Time series chart.* Data source: Monthly. Dimension `month`; Metric `revenue_brl` (SUM). Style: show data points, smooth line optional. Title: **Monthly revenue (R$)**.

### Tile 2 — Orders by month (column chart)
*Insert → Column chart.* Data source: Monthly. Dimension `month`; Metric `orders` (SUM). Sort by `month` ascending. Title: **Orders by month**.

### Tile 3 — Top 10 products (horizontal bar)
*Insert → Bar chart.* Data source: Top Products. Dimension `product_label`; Metric `revenue_brl` (SUM). Sort by `revenue_brl` descending; rows = 10. Title: **Top 10 products by revenue (R$)**. Products are labelled `category · first 6 characters of the product id` because Olist anonymises product IDs.

### Tile 4 — Revenue by region
Either of these:
- **Geo chart:** *Insert → Geo chart.* Data source: Revenue by State. Geo dimension `state_iso` (set its type to *Geo → Region*), Metric `revenue_brl`, Zoom area **Brazil**.
- **Bar chart:** Dimension `customer_region`, Metric `revenue_brl`, sorted descending. Title: **Revenue by region (R$)**.

### Tile 5 — Average delivery days (scorecard)
*Insert → Scorecard.* Data source: Monthly. The sheet's `avg_delivery_days` is a per-month average, so do **not** average it again. Instead create a calculated field on the Monthly source:

```
SUM(delivery_days_total) / SUM(delivered_orders)
```

Name it `Avg delivery days`, type Number, 1 decimal, and use it as the scorecard metric. Expected value: **12.6**. (Optionally add a second scorecard `SUM(revenue_brl)` → R$ 15.7M, and `SUM(orders)` → 98,199.)

## 3. Share by link
**Share** (top right) → **Manage access** → under *Link settings* choose **Anyone with the link can view** → copy the link into `README.md` where it says `PASTE_LOOKER_STUDIO_LINK_HERE`.

## 4. Screenshot
Click **View** (top right) to leave edit mode so the toolbar hides, then take a full-window screenshot and save it over `images/dashboard.png`. Until you do, that file is a copy of `images/dashboard_preview.png`, a matplotlib rendering of the same five tiles, so the README already shows a chart.
