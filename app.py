"""Interactive E-Commerce Business Intelligence dashboard."""
from pathlib import Path
import sys
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from dashboard.utils.data import load_data, category_summary, city_summary, customer_summary, sql_category_summary

st.set_page_config(page_title="CommerceIQ | Business Intelligence", page_icon="◈", layout="wide")
df = load_data()
if "theme" not in st.session_state: st.session_state.theme = "Dark"
if "filters" not in st.session_state: st.session_state.filters = {}
dark = st.session_state.theme == "Dark"
bg, panel, fg, muted = ("#0b1220", "#121d2e", "#e8eef8", "#91a0b8") if dark else ("#f3f6fb", "#ffffff", "#172338", "#62718a")
st.markdown(f"""<style>
.stApp{{background:{bg};color:{fg}}}[data-testid=stSidebar]{{background:{panel}}}
.block-container{{padding-top:1.5rem;max-width:1500px}}
.kpi{{background:{panel};border:1px solid {'#26354b' if dark else '#e0e6ef'};border-radius:14px;padding:18px 20px;min-height:108px;box-shadow:0 6px 18px #0002}}
.kl{{color:{muted};font-size:.82rem}}.kv{{font-size:1.6rem;font-weight:700;margin:8px 0;color:{fg}}}
.insight{{background:{panel};border-left:3px solid #41c6b2;padding:14px 16px;border-radius:9px;margin:8px 0;color:{fg}}}
</style>""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## ◈ CommerceIQ")
    st.caption("E-Commerce Business Intelligence")
    page = st.radio("NAVIGATION", ["Overview", "Sales Analytics", "Profitability", "Customer Analytics", "Product Analytics", "Geographic Analysis", "Payment & Orders", "Business Insights"])
    st.divider(); st.caption(f"{len(df):,} cleaned transaction rows")
    st.caption("Python · Pandas · SQLite")
left,right=st.columns([5,1])
with left:
    st.markdown('<span style="color:#41c6b2;letter-spacing:.14em">ECOMMERCE • ANALYTICS WORKSPACE</span>',unsafe_allow_html=True)
    st.title(page); st.caption("Explore sales performance, customer behavior and profitability.")
with right: st.session_state.theme=st.selectbox("Theme",["Dark","Light"],index=0 if dark else 1)

filters=st.session_state.filters
with st.expander("⌕  Global filters", expanded=page in ["Overview","Sales Analytics"]):
    with st.form("filter_form"):
        cols=st.columns(6); chosen={}
        for col,key in zip(cols[:5],["Category","City","Gender","Payment_Method","Order_Status"]):
            chosen[key]=col.multiselect(key.replace("_"," "),sorted(df[key].dropna().unique()),default=filters.get(key,[]))
        chosen["Discount"]=cols[5].multiselect("Discount",sorted(df.Discount.unique()),default=filters.get("Discount",[]),format_func=lambda x:f"{x:.0%}")
        a,b=st.columns(2); apply=a.form_submit_button("Apply filters",type="primary"); reset=b.form_submit_button("Reset")
        if apply: st.session_state.filters=chosen; st.rerun()
        if reset: st.session_state.filters={}; st.rerun()
data=df.copy()
for key,values in filters.items():
    if values: data=data[data[key].isin(values)]
if data.empty: st.warning("No records match these filters."); st.stop()

cats=category_summary(data); cities=city_summary(data); customers=customer_summary(data)
def money(v): return f"INR {v:,.0f}"
def metricrow(labels,values):
    for col,label,value in zip(st.columns(len(labels)),labels,values):
        col.markdown(f'<div class="kpi"><div class="kl">{label}</div><div class="kv">{value}</div><div class="kl">Filtered dataset</div></div>',unsafe_allow_html=True)
def totals(d):
    sales=d.Sales.sum(); profit=d.Profit.sum(); orders=d.Order_ID.nunique()
    return [money(sales),money(profit),f"{orders:,}",f"{d.Quantity.sum():,}",money(sales/orders if orders else 0),f"{profit/sales*100 if sales else 0:.1f}%"]
def kpis(d=data): metricrow(["Total Sales","Total Profit","Total Orders","Quantity Sold","Avg Order Value","Profit Margin"],totals(d))
def plot(fig,height=330):
    fig.update_layout(template="plotly_dark" if dark else "plotly_white",height=height,margin=dict(l=8,r=8,t=35,b=8),paper_bgcolor=panel,plot_bgcolor=panel,font_color=fg,legend_title_text="")
    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
def note(message): st.markdown(f'<div class="insight">✦ &nbsp; {message}</div>',unsafe_allow_html=True)
def cat_charts():
    a,b=st.columns(2)
    with a: st.subheader("Sales by category"); plot(px.bar(cats,x="Category",y="Sales",color="Category"))
    with b: st.subheader("Profit by category"); plot(px.bar(cats,x="Category",y="Profit",color="Category"))

if page=="Overview":
    kpis(); cat_charts(); a,b=st.columns(2)
    with a: st.subheader("Sales by city"); plot(px.bar(cities.head(10),x="Sales",y="City",orientation="h",color="Sales",color_continuous_scale="Teal"))
    with b: st.subheader("Order status mix"); plot(px.pie(data.groupby("Order_Status").Order_ID.nunique().reset_index(name="Orders"),names="Order_Status",values="Orders",hole=.6))
    a,b=st.columns(2)
    with a: st.subheader("Payment methods"); plot(px.pie(data.groupby("Payment_Method").Order_ID.nunique().reset_index(name="Orders"),names="Payment_Method",values="Orders",hole=.6))
    with b:
        st.subheader("Key business insights")
        note(f"{cats.iloc[0].Category} leads sales at {money(cats.iloc[0].Sales)}.")
        note(f"{cats.loc[cats.Profit.idxmax(),'Category']} generates the most profit.")
        note(f"{cities.iloc[0].City} is the leading city by sales.")
        note(f"{cats.loc[cats['Profit Margin %'].idxmax(),'Category']} has the highest category margin.")
elif page=="Sales Analytics":
    kpis(); a,b=st.columns(2)
    with a: st.subheader("Sales by category"); plot(px.bar(cats,x="Category",y="Sales",color="Category"))
    with b: st.subheader("Sales by city"); plot(px.bar(cities,x="City",y="Sales",color="Sales",color_continuous_scale="Teal"))
    a,b=st.columns(2)
    with a: st.subheader("Sales by gender"); plot(px.bar(data.groupby("Gender").Sales.sum().reset_index(),x="Gender",y="Sales",color="Gender"))
    with b: st.subheader("Sales by age group"); plot(px.bar(data.groupby("Age_Group",observed=True).Sales.sum().reset_index(),x="Age_Group",y="Sales",color="Sales",color_continuous_scale="Teal"))
    a,b=st.columns(2)
    with a: st.subheader("Quantity by category"); plot(px.bar(cats,x="Category",y="Quantity",color="Category"))
    with b: st.subheader("Sales distribution"); plot(px.histogram(data,x="Sales",nbins=30,color_discrete_sequence=["#41c6b2"]))
elif page=="Profitability":
    p=totals(data); metricrow(["Total Profit","Profit Margin","Avg Profit / Order","Top Profit Category"],[p[1],p[5],money(data.Profit.sum()/max(data.Order_ID.nunique(),1)),cats.loc[cats.Profit.idxmax(),"Category"]])
    cat_charts(); a,b=st.columns(2)
    with a: st.subheader("Profit margin by category"); plot(px.bar(cats,x="Category",y="Profit Margin %",color="Profit Margin %",color_continuous_scale="RdYlGn"))
    with b:
        st.subheader("Discount and profit margin")
        d=data.groupby("Discount").agg(Sales=("Sales","sum"),Profit=("Profit","sum")).reset_index(); d["Margin %"]=d.Profit/d.Sales*100
        plot(px.scatter(d,x="Discount",y="Margin %",size="Sales",hover_data=["Profit"]))
    st.subheader("Sales and profit comparison"); plot(px.bar(cats,x="Category",y=["Sales","Profit"],barmode="group"))
    st.subheader("Category profitability table"); st.dataframe(cats.style.background_gradient(subset=["Profit Margin %"],cmap="RdYlGn"),use_container_width=True,hide_index=True)
elif page=="Customer Analytics":
    metricrow(["Customers","Average Spend","Top Customer ID","Repeat Customers"],[f"{data.Customer_ID.nunique():,}",money(customers['Total Sales'].mean()),str(customers.iloc[0].Customer_ID),f"{(customers.Orders>1).sum():,}"])
    a,b=st.columns(2)
    with a: st.subheader("Top 10 customers by sales"); plot(px.bar(customers.head(10).sort_values("Total Sales"),x="Total Sales",y="Customer_ID",orientation="h",color="Total Sales",color_continuous_scale="Teal"))
    with b: st.subheader("Sales by gender"); plot(px.pie(data.groupby("Gender").Sales.sum().reset_index(),names="Gender",values="Sales",hole=.55))
    a,b=st.columns(2)
    with a: st.subheader("Sales by age group"); plot(px.bar(data.groupby("Age_Group",observed=True).Sales.sum().reset_index(),x="Age_Group",y="Sales",color="Sales",color_continuous_scale="Teal"))
    with b: st.subheader("Customer sales distribution"); plot(px.histogram(customers,x="Total Sales",nbins=30))
    st.subheader("Search customer details"); search=st.text_input("Customer ID, name or city")
    shown=customers[customers.astype(str).apply(lambda c:c.str.contains(search,case=False,na=False)).any(axis=1)] if search else customers
    st.dataframe(shown,use_container_width=True,hide_index=True)
elif page=="Product Analytics":
    st.subheader("Category comparison"); st.dataframe(cats.style.background_gradient(subset=["Profit Margin %"],cmap="RdYlGn"),use_container_width=True,hide_index=True)
    cat_charts(); a,b=st.columns(2)
    with a: st.subheader("Quantity by category"); plot(px.bar(cats,x="Category",y="Quantity",color="Category"))
    with b: st.subheader("Profit margin by category"); plot(px.bar(cats,x="Category",y="Profit Margin %",color="Profit Margin %",color_continuous_scale="RdYlGn"))
    note(f"Top sales: {cats.iloc[0].Category}. Most profitable: {cats.loc[cats.Profit.idxmax(),'Category']}. Highest margin: {cats.loc[cats['Profit Margin %'].idxmax(),'Category']}.")
    note(f"Lowest total profit: {cats.loc[cats.Profit.idxmin(),'Category']}.")
elif page=="Geographic Analysis":
    st.subheader("City performance"); st.dataframe(cities.style.background_gradient(subset=["Profit Margin %"],cmap="RdYlGn"),use_container_width=True,hide_index=True)
    a,b=st.columns(2)
    with a: st.subheader("Sales by city"); plot(px.bar(cities.sort_values("Sales"),x="Sales",y="City",orientation="h",color="Sales",color_continuous_scale="Teal"))
    with b: st.subheader("Profit by city"); plot(px.bar(cities.sort_values("Profit"),x="Profit",y="City",orientation="h",color="Profit",color_continuous_scale="Teal"))
    st.subheader("Orders by city"); plot(px.bar(cities.sort_values("Orders"),x="Orders",y="City",orientation="h",color="Orders",color_continuous_scale="Teal"))
    st.caption("A map needs city coordinates, which are not provided; ranked city performance is shown instead.")
elif page=="Payment & Orders":
    pay=data.groupby("Payment_Method").agg(Orders=("Order_ID","nunique"),Sales=("Sales","sum")).reset_index()
    status=data.groupby("Order_Status").agg(Orders=("Order_ID","nunique"),Sales=("Sales","sum")).reset_index(); status["Percentage"]=status.Orders/status.Orders.sum()*100
    a,b=st.columns(2)
    with a: st.subheader("Sales by payment method"); plot(px.bar(pay,x="Payment_Method",y="Sales",color="Payment_Method"))
    with b: st.subheader("Payment order share"); plot(px.pie(pay,names="Payment_Method",values="Orders",hole=.55))
    st.subheader("Order status"); st.dataframe(status.style.format({"Sales":"INR {:,.2f}","Percentage":"{:.1f}%"}),use_container_width=True,hide_index=True)
    plot(px.bar(status,x="Order_Status",y="Orders",color="Order_Status"))
    bad=status[status.Order_Status.astype(str).str.lower().isin(["returned","cancelled"])].Orders.sum()/status.Orders.sum()*100
    if bad>=20: st.warning(f"Returns and cancellations are {bad:.1f}% of orders; review fulfillment and customer feedback.")
    else: note(f"Returns and cancellations are {bad:.1f}% of orders.")
else:
    st.subheader("Calculated insights")
    note(f"{cats.iloc[0].Category} generates the highest sales ({money(cats.iloc[0].Sales)}).")
    note(f"{cats.loc[cats.Profit.idxmax(),'Category']} generates the highest profit.")
    note(f"{cats.loc[cats['Profit Margin %'].idxmax(),'Category']} has the highest profit margin ({cats['Profit Margin %'].max():.1f}%).")
    note(f"{cities.iloc[0].City} leads sales; the top three cities contribute {cities.head(3).Sales.sum()/cities.Sales.sum()*100:.1f}%.")
    d=data.groupby("Discount").agg(Sales=("Sales","sum"),Profit=("Profit","sum")); d["Margin"]=d.Profit/d.Sales
    corr=d.reset_index()[["Discount","Margin"]].corr().iloc[0,1] if len(d)>1 else float("nan")
    if pd.notna(corr): note(f"Discount level and category profit margin show a {('negative' if corr<0 else 'positive')} association (correlation {corr:.2f}); this is descriptive, not causal proof.")
    statuses=data.groupby("Order_Status").Order_ID.nunique(); bad=sum(v for k,v in statuses.items() if str(k).lower() in ["returned","cancelled"])/statuses.sum()*100
    note(f"Returns and cancellations account for {bad:.1f}% of filtered orders.")
    st.subheader("Recommended actions"); weak=cats.loc[cats['Profit Margin %'].idxmin()]
    note(f"Review discounting and unit costs in {weak.Category}, the lowest-margin category ({weak['Profit Margin %']:.1f}%).")
    issue=max(((str(k),v) for k,v in statuses.items() if str(k).lower() in ["returned","cancelled"]),key=lambda x:x[1],default=None)
    if issue: note(f"Investigate {issue[0]} orders ({issue[1]:,}) as the main fulfillment issue.")
    note(f"Focus local marketing tests in {cities.iloc[0].City}, the leading sales city.")
    st.divider(); st.subheader("Data quality")
    raw_path=ROOT/"data"/"raw_data.csv"; raw=pd.read_csv(raw_path) if raw_path.exists() else df
    metricrow(["Clean records","Missing values","Duplicates removed","Categories","Cities"],[f"{len(df):,}",f"{df.isna().sum().sum():,}",f"{max(len(raw)-len(df),0):,}",str(df.Category.nunique()),str(df.City.nunique())])

st.divider()
a,b=st.columns(2)
with a: st.download_button("Download filtered rows (CSV)",data.to_csv(index=False).encode("utf-8"),"filtered_ecommerce_data.csv","text/csv")
with b: st.download_button("Download summary report (CSV)",cats.to_csv(index=False).encode("utf-8"),"ecommerce_category_summary.csv","text/csv")
with st.expander("SQLite category summary"):
    sql=sql_category_summary()
    if sql.empty: st.info("Run python data/sql/setup_database.py to create the SQLite summary table.")
    else: st.dataframe(sql,use_container_width=True,hide_index=True)
st.caption("Source: cleaned_data.csv • SQL summaries use the existing SQLite sales table • No transaction date is present for time trends.")
