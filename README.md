# 🛒 E-Commerce Sales Performance Analysis

[![Live Dashboard](https://img.shields.io/badge/Live-Tableau%20Dashboard-blue)](https://public.tableau.com/app/profile/tannu.kumari3904/viz/Ecommerce-Sales-Dashboard_17799746627200/Dashboard1)

> **Tools:** Python · Pandas · NumPy · Matplotlib · Seaborn  . Tableau
> **Domain:** Retail Analytics | Business Intelligence  
> **Author:** Tannu Kumari | IGDTUW Delhi | Batch 2026

---

## 📌 Project Overview

End-to-end exploratory data analysis on **5,000 e-commerce orders** across 5 product categories, 5 regions, and 3 customer segments — simulating a real-world Indian retail dataset.

The goal is to extract **actionable business insights** that help a retail company optimise revenue, reduce discount losses, and target high-value segments.

---

## 🎯 Business Questions Answered

| # | Question |
|---|----------|
| 1 | Which product category generates the highest revenue & profit? |
| 2 | How does revenue trend month-over-month and quarter-over-quarter? |
| 3 | Which region contributes the most to overall sales? |
| 4 | What is the impact of discount levels on profit margins? |
| 5 | Which customer segment (Consumer / Corporate / Home Office) is most valuable? |
| 6 | What is the preferred payment method, and how does it vary? |
| 7 | Which products are the top-10 revenue drivers? |
| 8 | On which days of the week does each category sell most? |

---

## 📊 Visualisations Generated

| Chart | Description |
|-------|-------------|
| `chart1_revenue_trends.png` | Monthly Revenue vs Profit line chart + Quarterly bar chart |
| `chart2_category_region.png` | Category horizontal bar chart + Regional pie chart |
| `chart3_discount_segment.png` | Discount-margin impact + Segment-category stacked bars |
| `chart4_heatmap_payment.png` | Weekday × Category heatmap + Payment method revenue |
| `chart5_top_products.png` | Top 10 products by revenue (ranked horizontal bars) |

---

## 📁 Project Structure

```
ecommerce-sales-analysis/
│
├── ecommerce_sales_analysis.py   # Main analysis script
├── ecommerce_sales_data.csv      # Auto-generated dataset (5000 rows)
├── chart1_revenue_trends.png
├── chart2_category_region.png
├── chart3_discount_segment.png
├── chart4_heatmap_payment.png
├── chart5_top_products.png
└── README.md
```

---

## 🔍 Key Findings

1. **Electronics** dominates revenue but has the highest cost variation — opportunity for dynamic pricing.
2. **Q3 & Q4** consistently outperform other quarters, confirming festive-season demand surge.
3. **20% discount** tier severely erodes profit margins — recommend capping at 10%.
4. **UPI** is the leading payment method — smooth UPI checkout = fewer cart abandonments.
5. **Corporate segment** shows the highest average order value — B2B loyalty programs recommended.
6. **North & South regions** together account for ~40% of revenue — key markets for expansion.

---

## 🚀 How to Run

```bash
# 1. Clone the repo
git clone https://github.com/Tannu067/ecommerce-sales-analysis.git
cd ecommerce-sales-analysis

# 2. Install dependencies
pip install pandas numpy matplotlib seaborn

# 3. Run analysis
python ecommerce_sales_analysis.py
```

All 5 charts will be saved automatically in the same folder.

---

## 🛠 Tech Stack

| Library | Version | Purpose |
|---------|---------|---------|
| Pandas | ≥ 1.5 | Data manipulation & aggregation |
| NumPy | ≥ 1.23 | Numerical computations & RNG |
| Matplotlib | ≥ 3.6 | Base plotting |
| Seaborn | ≥ 0.12 | Statistical visualisations |

---

## 📈 Skills Demonstrated

- Data cleaning & preprocessing with Pandas
- Feature engineering (month, quarter, discount groups)
- Business KPI calculation (revenue, profit, margin)
- 5 multi-panel publication-quality charts
- Deriving actionable business insights from raw data
- End-to-end EDA pipeline

---

*Part of Data Analytics portfolio — Tannu Kumari*
