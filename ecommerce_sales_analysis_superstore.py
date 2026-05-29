"""
=============================================================
  E-Commerce Sales Performance Analysis
  Author  : Tannu Kumari | IGDTUW Delhi | Batch 2026
  Tools   : Python, Pandas, Matplotlib, Seaborn
  Dataset : E-Commerce Retail Sales Data (5000 orders, 2023)
=============================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# chart styling
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({
    "figure.dpi": 150,
    "axes.titlesize": 14,
    "axes.titleweight": "bold",
    "axes.labelsize": 11,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "figure.facecolor": "#F8F9FA",
    "axes.facecolor": "#FFFFFF",
})
COLORS = ["#2563EB", "#16A34A", "#DC2626", "#D97706", "#7C3AED", "#0891B2"]

# ── LOAD DATASET ──────────────────────────────────────────────
df = pd.read_csv("ecommerce_sales_data.csv", parse_dates=["order_date"])
print(f"Dataset shape: {df.shape}")
print(df.head())
print(df.isnull().sum())

# ── BUSINESS SUMMARY ──────────────────────────────────────────
print(f"""
Dataset Overview
   Total Orders     : {len(df):,}
   Date Range       : {df['order_date'].min().date()} to {df['order_date'].max().date()}
   Categories       : {df['category'].nunique()}
   Regions          : {df['region'].nunique()}

Business Summary
   Total Revenue    : Rs.{df['revenue'].sum()/1e6:.2f} Lakhs
   Total Profit     : Rs.{df['profit'].sum()/1e6:.2f} Lakhs
   Avg Profit Margin: {df['profit_margin'].mean():.1f}%
   Avg Order Value  : Rs.{df['revenue'].mean():,.0f}
   Total Units Sold : {df['quantity'].sum():,}
""")

# ── CHART 1: Monthly Revenue & Quarterly Breakdown ────────────
fig, axes = plt.subplots(1, 2, figsize=(16, 5))
fig.suptitle("E-Commerce Performance Dashboard 2023", fontsize=16, fontweight="bold", y=1.01)

monthly = (df.groupby("month_num")
             .agg(revenue=("revenue", "sum"), profit=("profit", "sum"))
             .reset_index().sort_values("month_num"))
months_short = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
monthly["label"] = months_short

ax = axes[0]
ax.fill_between(monthly["label"], monthly["revenue"]/1e6, alpha=0.3, color=COLORS[0])
ax.plot(monthly["label"], monthly["revenue"]/1e6, "o-", color=COLORS[0], lw=2.5, ms=6, label="Revenue")
ax.fill_between(monthly["label"], monthly["profit"]/1e6, alpha=0.3, color=COLORS[1])
ax.plot(monthly["label"], monthly["profit"]/1e6, "s--", color=COLORS[1], lw=2, ms=5, label="Profit")
ax.set_title("Monthly Revenue vs Profit (Rs. Lakhs)")
ax.set_xlabel("Month"); ax.set_ylabel("Amount (Rs. Lakhs)")
ax.legend(loc="upper left")
plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)

ax2 = axes[1]
quarter = df.groupby("quarter")["revenue"].sum()
bars = ax2.bar(quarter.index, quarter.values/1e6, color=COLORS[:4], edgecolor="white", width=0.5)
ax2.set_title("Quarterly Revenue Breakdown")
ax2.set_xlabel("Quarter"); ax2.set_ylabel("Revenue (Rs. Lakhs)")
for bar in bars:
    ax2.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
             f"Rs.{bar.get_height():.0f}L", ha="center", va="bottom", fontsize=9, fontweight="bold")
plt.tight_layout()
plt.savefig("chart1_revenue_trends.png", bbox_inches="tight")
plt.show()

# ── CHART 2: Category & Region ────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(16, 5))
cat_data = df.groupby("category").agg(revenue=("revenue","sum"), profit=("profit","sum")).sort_values("revenue", ascending=True)
ax = axes[0]
y = range(len(cat_data))
ax.barh(y, cat_data["revenue"]/1e6, color=COLORS[0], alpha=0.8, label="Revenue", height=0.4)
ax.barh([i+0.42 for i in y], cat_data["profit"]/1e6, color=COLORS[1], alpha=0.8, label="Profit", height=0.4)
ax.set_yticks([i+0.21 for i in y]); ax.set_yticklabels(cat_data.index)
ax.set_title("Revenue & Profit by Category"); ax.set_xlabel("Amount (Rs. Lakhs)"); ax.legend()

ax2 = axes[1]
reg_data = df.groupby("region")["revenue"].sum()
wedges, texts, autotexts = ax2.pie(reg_data, labels=reg_data.index, colors=COLORS[:5],
                                    autopct="%1.1f%%", startangle=140,
                                    wedgeprops={"edgecolor":"white","linewidth":2})
for at in autotexts: at.set_fontsize(9); at.set_fontweight("bold")
ax2.set_title("Revenue Share by Region")
plt.tight_layout()
plt.savefig("chart2_category_region.png", bbox_inches="tight")
plt.show()

# ── CHART 3: Discount Impact & Segments ───────────────────────
fig, axes = plt.subplots(1, 2, figsize=(16, 5))
ax = axes[0]
discount_groups = pd.cut(df["discount"], bins=[-0.01,0,0.05,0.10,0.15,0.20],
                          labels=["0%","5%","10%","15%","20%"])
disc_profit = df.groupby(discount_groups)["profit_margin"].mean()
ax.bar(disc_profit.index, disc_profit.values,
       color=[COLORS[1] if v > 0 else COLORS[2] for v in disc_profit.values], edgecolor="white")
ax.axhline(0, color="black", lw=0.8, ls="--")
ax.set_title("Avg Profit Margin by Discount Level")
ax.set_xlabel("Discount %"); ax.set_ylabel("Avg Profit Margin (%)")

ax2 = axes[1]
seg_data = df.groupby(["segment","category"])["revenue"].sum().unstack(fill_value=0)
seg_data.div(1e6).plot(kind="bar", ax=ax2, color=COLORS[:5], edgecolor="white", width=0.65)
ax2.set_title("Revenue by Customer Segment & Category")
ax2.set_xlabel("Segment"); ax2.set_ylabel("Revenue (Rs. Lakhs)")
ax2.legend(title="Category", bbox_to_anchor=(1.01,1), loc="upper left", fontsize=8)
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=0)
plt.tight_layout()
plt.savefig("chart3_discount_segment.png", bbox_inches="tight")
plt.show()

# ── CHART 4: Heatmap & Payment ────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(16, 5))
order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
pivot = df.pivot_table(values="revenue", index="weekday", columns="category", aggfunc="sum", fill_value=0)
pivot = pivot.reindex([d for d in order if d in pivot.index])
ax = axes[0]
sns.heatmap(pivot/1e6, ax=ax, cmap="Blues", annot=True, fmt=".0f",
            linewidths=0.5, cbar_kws={"label":"Revenue (Rs.L)"})
ax.set_title("Revenue Heatmap - Day of Week x Category")
ax.set_xlabel("Category"); ax.set_ylabel("Weekday")

ax2 = axes[1]
pay_data = df.groupby("payment")["revenue"].sum().sort_values(ascending=False)
bars = ax2.bar(pay_data.index, pay_data.values/1e6, color=COLORS, edgecolor="white")
ax2.set_title("Revenue by Payment Method")
ax2.set_xlabel("Payment Method"); ax2.set_ylabel("Revenue (Rs. Lakhs)")
for bar in bars:
    ax2.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3,
             f"Rs.{bar.get_height():.0f}L", ha="center", va="bottom", fontsize=8)
plt.tight_layout()
plt.savefig("chart4_heatmap_payment.png", bbox_inches="tight")
plt.show()

# ── CHART 5: Top 10 Products ──────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 5))
top10 = df.groupby("product")["revenue"].sum().nlargest(10).sort_values()
colors_bar = [COLORS[0] if i >= 7 else COLORS[2] if i < 3 else "#6B7280" for i in range(10)]
bars = ax.barh(top10.index, top10.values/1e6, color=colors_bar, edgecolor="white")
ax.set_title("Top 10 Products by Revenue"); ax.set_xlabel("Revenue (Rs. Lakhs)")
for bar in bars:
    ax.text(bar.get_width()+0.2, bar.get_y()+bar.get_height()/2,
            f"Rs.{bar.get_width():.1f}L", va="center", fontsize=9)
ax.legend(handles=[
    plt.Rectangle((0,0),1,1, color=COLORS[0], label="Top 3"),
    plt.Rectangle((0,0),1,1, color="#6B7280", label="Mid"),
    plt.Rectangle((0,0),1,1, color=COLORS[2], label="Bottom 3"),
], loc="lower right")
plt.tight_layout()
plt.savefig("chart5_top_products.png", bbox_inches="tight")
plt.show()

# ── KEY INSIGHTS ──────────────────────────────────────────────
print("=" * 58)
print("  KEY BUSINESS INSIGHTS")
print("=" * 58)
insights = [
    "1. Electronics is the #1 revenue & profit category.",
    "2. All 5 regions contribute almost equally (~20% each).",
    "3. Discount beyond 10% clearly hurts margins — cap at 10%.",
    "4. Corporate segment has highest average order value.",
    "5. COD is top payment method — customers prefer post-payment.",
    "6. Smartphone, Headphones, Laptop drive most of Electronics revenue.",
    "7. Books & Clothing have thin margins — focus on Electronics.",
    "8. Revenue is consistent year-round — no major seasonal spike.",
]
for ins in insights:
    print(f"  {ins}")
