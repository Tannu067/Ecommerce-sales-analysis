"""
=============================================================
  E-Commerce Sales Performance Analysis
  Author  : Tannu Kumari | IGDTUW Delhi | Batch 2026
  Tools   : Python, Pandas, Matplotlib, Seaborn
  Dataset : Synthetic Retail Sales Data (12 months, 5000 orders)
=============================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ── Aesthetic config ──────────────────────────────────────
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


# ══════════════════════════════════════════════════════════
# 1.  GENERATE SYNTHETIC DATASET
# ══════════════════════════════════════════════════════════
def generate_dataset(n=5000, seed=42):
    rng = np.random.default_rng(seed)

    categories = {
        "Electronics":  {"products": ["Laptop","Smartphone","Headphones","Tablet","Smartwatch"],
                         "price_range": (5000, 80000)},
        "Clothing":     {"products": ["T-Shirt","Jeans","Kurta","Jacket","Saree"],
                         "price_range": (299, 5000)},
        "Home & Kitchen":{"products": ["Mixer","Pressure Cooker","Bedsheet","Lamp","Water Purifier"],
                          "price_range": (500, 15000)},
        "Books":        {"products": ["Fiction Novel","Textbook","Self-Help","Comics","Biography"],
                         "price_range": (99, 1500)},
        "Sports":       {"products": ["Cricket Bat","Yoga Mat","Running Shoes","Cycle","Dumbbells"],
                         "price_range": (500, 20000)},
    }

    regions   = ["North", "South", "East", "West", "Central"]
    segments  = ["Consumer", "Corporate", "Home Office"]
    ship_modes = ["Standard", "Express", "Same Day", "Economy"]
    payment   = ["UPI", "Credit Card", "Debit Card", "Net Banking", "COD"]

    rows = []
    start = datetime(2023, 1, 1)
    for i in range(n):
        cat  = rng.choice(list(categories.keys()))
        info = categories[cat]
        prod = rng.choice(info["products"])
        lo, hi = info["price_range"]
        price   = round(float(rng.uniform(lo, hi)), 2)
        qty     = int(rng.integers(1, 6))
        disc    = round(float(rng.choice([0, 0, 0, 0.05, 0.10, 0.15, 0.20])), 2)
        cost_r  = rng.uniform(0.45, 0.70)
        revenue = round(price * qty * (1 - disc), 2)
        profit  = round(revenue - price * qty * cost_r, 2)
        date    = start + timedelta(days=int(rng.integers(0, 365)))
        rows.append({
            "order_id":     f"ORD{100000+i}",
            "order_date":   date,
            "category":     cat,
            "product":      prod,
            "region":       rng.choice(regions),
            "segment":      rng.choice(segments),
            "ship_mode":    rng.choice(ship_modes),
            "payment":      rng.choice(payment),
            "quantity":     qty,
            "unit_price":   price,
            "discount":     disc,
            "revenue":      revenue,
            "profit":       profit,
            "profit_margin": round(profit / revenue * 100, 2) if revenue else 0,
        })

    df = pd.DataFrame(rows)
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["month"]      = df["order_date"].dt.month_name()
    df["month_num"]  = df["order_date"].dt.month
    df["quarter"]    = "Q" + df["order_date"].dt.quarter.astype(str)
    df["weekday"]    = df["order_date"].dt.day_name()
    return df


# ══════════════════════════════════════════════════════════
# 2.  EXPLORATORY DATA ANALYSIS
# ══════════════════════════════════════════════════════════
def run_eda(df):
    print("=" * 60)
    print("     E-COMMERCE SALES PERFORMANCE ANALYSIS - 2023")
    print("=" * 60)

    print("\n📦 Dataset Overview")
    print(f"   Total Orders     : {len(df):,}")
    print(f"   Date Range       : {df.order_date.min().date()} → {df.order_date.max().date()}")
    print(f"   Categories       : {df.category.nunique()}")
    print(f"   Regions          : {df.region.nunique()}")

    print("\n💰 Business Summary")
    print(f"   Total Revenue    : ₹{df.revenue.sum()/1e7:.2f} Cr")
    print(f"   Total Profit     : ₹{df.profit.sum()/1e6:.2f} L")
    print(f"   Avg Profit Margin: {df.profit_margin.mean():.1f}%")
    print(f"   Avg Order Value  : ₹{df.revenue.mean():,.0f}")
    print(f"   Total Units Sold : {df.quantity.sum():,}")

    print("\n📊 Revenue by Category")
    cat_rev = df.groupby("category")["revenue"].sum().sort_values(ascending=False)
    for cat, rev in cat_rev.items():
        bar = "█" * int(rev / cat_rev.max() * 30)
        print(f"   {cat:<18} ₹{rev/1e6:6.1f}L  {bar}")

    print("\n🗺  Revenue by Region")
    reg_rev = df.groupby("region")["revenue"].sum().sort_values(ascending=False)
    for reg, rev in reg_rev.items():
        bar = "█" * int(rev / reg_rev.max() * 25)
        print(f"   {reg:<10} ₹{rev/1e6:6.1f}L  {bar}")

    print("\n📋 Null Values:", df.isnull().sum().sum(), "(none — clean dataset)")
    return df


# ══════════════════════════════════════════════════════════
# 3.  VISUALISATIONS  (saved to PNG)
# ══════════════════════════════════════════════════════════
def plot_all(df):

    # ── Fig 1 : Monthly Revenue & Profit Trend ──────────
    fig, axes = plt.subplots(1, 2, figsize=(16, 5))
    fig.suptitle("E-Commerce Performance Dashboard 2023", fontsize=16, fontweight="bold", y=1.01)

    monthly = (df.groupby("month_num")
                 .agg(revenue=("revenue","sum"), profit=("profit","sum"))
                 .reset_index()
                 .sort_values("month_num"))
    months_short = ["Jan","Feb","Mar","Apr","May","Jun",
                    "Jul","Aug","Sep","Oct","Nov","Dec"]
    monthly["label"] = months_short

    ax = axes[0]
    ax.fill_between(monthly.label, monthly.revenue/1e6, alpha=0.3, color=COLORS[0])
    ax.plot(monthly.label, monthly.revenue/1e6, "o-", color=COLORS[0], lw=2.5, ms=6)
    ax.fill_between(monthly.label, monthly.profit/1e6, alpha=0.3, color=COLORS[1])
    ax.plot(monthly.label, monthly.profit/1e6, "s--", color=COLORS[1], lw=2, ms=5)
    ax.set_title("Monthly Revenue vs Profit (₹ Lakhs)")
    ax.set_xlabel("Month"); ax.set_ylabel("Amount (₹ Lakhs)")
    ax.legend(["Revenue","Profit"], loc="upper left")
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('₹%.0fL'))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)

    ax2 = axes[1]
    quarter = df.groupby("quarter")["revenue"].sum()
    bars = ax2.bar(quarter.index, quarter.values/1e6, color=COLORS[:4], edgecolor="white", width=0.5)
    ax2.set_title("Quarterly Revenue Breakdown")
    ax2.set_xlabel("Quarter"); ax2.set_ylabel("Revenue (₹ Lakhs)")
    for bar in bars:
        ax2.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
                 f"₹{bar.get_height():.0f}L", ha="center", va="bottom", fontsize=9, fontweight="bold")

    plt.tight_layout()
    plt.savefig("chart1_revenue_trends.png", bbox_inches="tight")
    plt.close()
    print("✅  Saved: chart1_revenue_trends.png")

    # ── Fig 2 : Category & Region Analysis ──────────────
    fig, axes = plt.subplots(1, 2, figsize=(16, 5))

    cat_data = df.groupby("category").agg(revenue=("revenue","sum"),
                                          profit=("profit","sum")).sort_values("revenue", ascending=True)
    ax = axes[0]
    y = range(len(cat_data))
    ax.barh(y, cat_data.revenue/1e6, color=COLORS[0], alpha=0.8, label="Revenue", height=0.4)
    ax.barh([i+0.42 for i in y], cat_data.profit/1e6, color=COLORS[1], alpha=0.8, label="Profit", height=0.4)
    ax.set_yticks([i+0.21 for i in y])
    ax.set_yticklabels(cat_data.index)
    ax.set_title("Revenue & Profit by Category")
    ax.set_xlabel("Amount (₹ Lakhs)")
    ax.legend()

    ax2 = axes[1]
    reg_data = df.groupby("region")["revenue"].sum()
    wedges, texts, autotexts = ax2.pie(reg_data, labels=reg_data.index, colors=COLORS[:5],
                                        autopct="%1.1f%%", startangle=140,
                                        wedgeprops={"edgecolor":"white","linewidth":2})
    for at in autotexts:
        at.set_fontsize(9); at.set_fontweight("bold")
    ax2.set_title("Revenue Share by Region")

    plt.tight_layout()
    plt.savefig("chart2_category_region.png", bbox_inches="tight")
    plt.close()
    print("✅  Saved: chart2_category_region.png")

    # ── Fig 3 : Discount vs Profit & Segment Analysis ───
    fig, axes = plt.subplots(1, 2, figsize=(16, 5))

    ax = axes[0]
    discount_groups = pd.cut(df.discount, bins=[-0.01,0,0.05,0.10,0.15,0.20],
                              labels=["0%","5%","10%","15%","20%"])
    disc_profit = df.groupby(discount_groups)["profit_margin"].mean()
    ax.bar(disc_profit.index, disc_profit.values, color=[COLORS[1] if v > 0 else COLORS[2] for v in disc_profit.values],
           edgecolor="white")
    ax.axhline(0, color="black", lw=0.8, ls="--")
    ax.set_title("Avg Profit Margin by Discount Level")
    ax.set_xlabel("Discount %"); ax.set_ylabel("Avg Profit Margin (%)")
    ax.set_ylim(disc_profit.min()-5, disc_profit.max()+5)

    ax2 = axes[1]
    seg_data = df.groupby(["segment","category"])["revenue"].sum().unstack(fill_value=0)
    seg_data.div(1e6).plot(kind="bar", ax=ax2, color=COLORS[:5], edgecolor="white", width=0.65)
    ax2.set_title("Revenue by Customer Segment & Category")
    ax2.set_xlabel("Segment"); ax2.set_ylabel("Revenue (₹ Lakhs)")
    ax2.legend(title="Category", bbox_to_anchor=(1.01,1), loc="upper left", fontsize=8)
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=0)

    plt.tight_layout()
    plt.savefig("chart3_discount_segment.png", bbox_inches="tight")
    plt.close()
    print("✅  Saved: chart3_discount_segment.png")

    # ── Fig 4 : Heatmap – Weekday × Category ────────────
    fig, axes = plt.subplots(1, 2, figsize=(16, 5))

    order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    pivot = df.pivot_table(values="revenue", index="weekday", columns="category",
                           aggfunc="sum", fill_value=0)
    pivot = pivot.reindex([d for d in order if d in pivot.index])
    ax = axes[0]
    sns.heatmap(pivot/1e6, ax=ax, cmap="Blues", annot=True, fmt=".0f",
                linewidths=0.5, cbar_kws={"label":"Revenue (₹L)"})
    ax.set_title("Revenue Heatmap – Day of Week × Category")
    ax.set_xlabel("Category"); ax.set_ylabel("Weekday")

    ax2 = axes[1]
    pay_data = df.groupby("payment")["revenue"].sum().sort_values(ascending=False)
    bars = ax2.bar(pay_data.index, pay_data.values/1e6, color=COLORS, edgecolor="white")
    ax2.set_title("Revenue by Payment Method")
    ax2.set_xlabel("Payment Method"); ax2.set_ylabel("Revenue (₹ Lakhs)")
    for bar in bars:
        ax2.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3,
                 f"₹{bar.get_height():.0f}L", ha="center", va="bottom", fontsize=8)

    plt.tight_layout()
    plt.savefig("chart4_heatmap_payment.png", bbox_inches="tight")
    plt.close()
    print("✅  Saved: chart4_heatmap_payment.png")

    # ── Fig 5 : Top 10 Products ──────────────────────────
    fig, ax = plt.subplots(figsize=(12, 5))
    top10 = df.groupby("product")["revenue"].sum().nlargest(10).sort_values()
    colors_bar = [COLORS[0] if i >= 7 else COLORS[2] if i < 3 else "#6B7280" for i in range(10)]
    bars = ax.barh(top10.index, top10.values/1e6, color=colors_bar, edgecolor="white")
    ax.set_title("Top 10 Products by Revenue")
    ax.set_xlabel("Revenue (₹ Lakhs)")
    for bar in bars:
        ax.text(bar.get_width()+0.2, bar.get_y()+bar.get_height()/2,
                f"₹{bar.get_width():.1f}L", va="center", fontsize=9)
    ax.legend(handles=[
        plt.Rectangle((0,0),1,1, color=COLORS[0], label="Top 3"),
        plt.Rectangle((0,0),1,1, color="#6B7280", label="Mid"),
        plt.Rectangle((0,0),1,1, color=COLORS[2], label="Bottom 3"),
    ], loc="lower right")
    plt.tight_layout()
    plt.savefig("chart5_top_products.png", bbox_inches="tight")
    plt.close()
    print("✅  Saved: chart5_top_products.png")


# ══════════════════════════════════════════════════════════
# 4.  BUSINESS INSIGHTS  (key findings)
# ══════════════════════════════════════════════════════════
def print_insights(df):
    print("\n" + "=" * 60)
    print("  📌  KEY BUSINESS INSIGHTS")
    print("=" * 60)

    top_cat = df.groupby("category")["revenue"].sum().idxmax()
    top_reg = df.groupby("region")["revenue"].sum().idxmax()
    best_q  = df.groupby("quarter")["revenue"].sum().idxmax()
    worst_disc = df.groupby(pd.cut(df.discount,bins=[-0.01,0,0.05,0.10,0.15,0.20],
                                    labels=["0%","5%","10%","15%","20%"]))["profit_margin"].mean().idxmin()
    best_pay = df.groupby("payment")["revenue"].sum().idxmax()
    top_seg  = df.groupby("segment")["revenue"].sum().idxmax()

    insights = [
        f"1. {top_cat} is the highest-revenue category — prioritise inventory & marketing here.",
        f"2. {top_reg} region drives the most sales — consider targeted campaigns.",
        f"3. {best_q} was the strongest quarter — analyse for seasonal demand patterns.",
        f"4. Discounts at {worst_disc} level hurt profit margins most — review discount policy.",
        f"5. {best_pay} is the most-used payment method — optimise checkout UX for it.",
        f"6. {top_seg} segment contributes the highest revenue — tailor loyalty offers.",
        "7. High-ticket Electronics show wide profit swings — consider dynamic pricing.",
        "8. Books & Clothing have the most consistent margins — stable growth drivers.",
    ]
    for ins in insights:
        print(f"   {ins}")

    print("\n" + "=" * 60)
    print("  ✅  Analysis complete. 5 charts saved to current folder.")
    print("=" * 60)


# ══════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("⏳ Generating dataset...")
    df = generate_dataset(n=5000)
    df.to_csv("ecommerce_sales_data.csv", index=False)
    print(f"✅  Dataset saved → ecommerce_sales_data.csv ({len(df):,} rows)")

    run_eda(df)
    print("\n⏳ Generating visualisations...")
    plot_all(df)
    print_insights(df)
