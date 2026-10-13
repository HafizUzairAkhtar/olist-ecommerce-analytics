import pandas as pd
f = pd.read_csv("data/dashboard/orders_fact.csv")
tp = pd.read_csv("data/dashboard/top_products.csv")
STATE_NAME = {"AC":"Acre","AL":"Alagoas","AM":"Amazonas","AP":"Amapá","BA":"Bahia","CE":"Ceará","DF":"Distrito Federal","ES":"Espírito Santo","GO":"Goiás","MA":"Maranhão","MG":"Minas Gerais","MS":"Mato Grosso do Sul","MT":"Mato Grosso","PA":"Pará","PB":"Paraíba","PE":"Pernambuco","PI":"Piauí","PR":"Paraná","RJ":"Rio de Janeiro","RN":"Rio Grande do Norte","RO":"Rondônia","RR":"Roraima","RS":"Rio Grande do Sul","SC":"Santa Catarina","SE":"Sergipe","SP":"São Paulo","TO":"Tocantins"}
monthly = (f.groupby("purchase_month").agg(orders=("order_id","count"), revenue_brl=("revenue_brl","sum"), revenue_usd=("revenue_usd","sum"),
            delivered_orders=("delivery_days","count"), delivery_days_total=("delivery_days","sum")).reset_index())
monthly["avg_delivery_days"] = (monthly.delivery_days_total/monthly.delivered_orders).round(1)
monthly["month"] = monthly.purchase_month + "-01"   # full date so Looker Studio parses it
monthly = monthly[["month","orders","revenue_brl","revenue_usd","delivered_orders","delivery_days_total","avg_delivery_days"]].round(2)
state = (f.groupby(["customer_state","customer_region"]).agg(orders=("order_id","count"), revenue_brl=("revenue_brl","sum"), revenue_usd=("revenue_usd","sum"),
          delivered_orders=("delivery_days","count"), delivery_days_total=("delivery_days","sum")).reset_index())
state["avg_delivery_days"] = (state.delivery_days_total/state.delivered_orders).round(1)
state["state_name"] = state.customer_state.map(STATE_NAME); state["state_iso"] = "BR-" + state.customer_state
state = state[["customer_state","state_name","state_iso","customer_region","orders","revenue_brl","revenue_usd","delivered_orders","delivery_days_total","avg_delivery_days"]].round(2).sort_values("revenue_brl", ascending=False)
kpi = pd.DataFrame([{"metric":"total_orders","value":len(f)},{"metric":"total_revenue_brl","value":round(f.revenue_brl.sum(),2)},
                    {"metric":"total_revenue_usd","value":round(f.revenue_usd.sum(),2)},{"metric":"avg_delivery_days","value":round(f.delivery_days.mean(),1)},
                    {"metric":"on_time_delivery_rate","value":round(f.delivered_on_time.mean(),4)},{"metric":"delivered_orders","value":int(f.delivery_days.count())}])
tp["rank"] = range(1, len(tp)+1); tp = tp[["rank","product_label","product_category_name_english","product_id","units_sold","revenue_brl","revenue_usd"]]
for name, df in [("monthly",monthly),("revenue_by_state",state),("top_products",tp),("kpi",kpi)]:
    df.to_csv(f"data/dashboard/{name}.csv", index=False)
with pd.ExcelWriter("data/dashboard/olist_dashboard_data.xlsx") as w:
    for name, df in [("monthly",monthly),("revenue_by_state",state),("top_products",tp),("kpi",kpi)]:
        df.to_excel(w, sheet_name=name, index=False)
print(monthly.head(3).to_string()); print(state.head(3).to_string()); print(kpi.to_string())
import os; print("xlsx bytes:", os.path.getsize("data/dashboard/olist_dashboard_data.xlsx"))
