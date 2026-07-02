# UK Corporation Tax Gap Dashboard

An interactive Dash dashboard exploring where the UK's corporation tax gap sits, which sectors carry the most compliance risk, and how HMRC's recovery efforts have evolved. Built with real HMRC data covering 2005–2024.

## 📊 What Is This?

The **tax gap** is the difference between the tax owed to the government and the tax actually paid. For corporations, this gap runs to billions of pounds—and it's not evenly distributed.

This dashboard helps you explore three critical questions:

1. **Which sectors owe the most tax?** – Which industries represent the biggest compliance risk?
2. **Is the tax gap growing over time?** – Are we losing more money to non-compliance, or is HMRC catching up?
3. **Who is responsible for the gap?** – Is it large corporations dodging tax, or small businesses struggling to comply?

## 🎯 Key Features

**Three Main Sections:**

### ① Which Sectors Owe the Most Corporation Tax?
- **Bar chart** ranking all 20+ industry sectors by total CT liability
- **Toggle metrics:** Switch between total liability, average per company, or number of companies
- **Year selector:** See how the landscape has changed (2018–2024)
- **What it shows:** Financial & Insurance, Wholesale & Retail Trade, and Professional Services dominate the top

### ② Is the Tax Gap Growing Over Time?
- **Multi-line chart** tracking 2005–2024 with toggleable lines
- **Metrics included:**
  - **Gross tax gap** – The total missing tax
  - **Compliance yield** – What HMRC successfully recovers
  - **Net tax gap** – What's left after recovery efforts
  - **Liabilities & % breakdown** – Supporting context
- **What it shows:** The gap has generally shrunk, but recent years show volatility

### ③ Who Is Responsible for the Gap?
- **Segment breakdown** – Tax gap by taxpayer group:
  - Individual customers (37M people)
  - Wealthy individuals (950k high-earners)
  - Small businesses (5.1M companies)
  - Mid-sized businesses & charities (380k entities)
  - Large businesses (2k mega-corporations)
- **Toggle options:** View as £ billions or % of what should be paid
- **HMRC efficiency snapshot:** How much of the gap does HMRC recover from each group?
- **What it shows:** Small businesses account for the largest absolute gap (but there are 5M of them), while large businesses pay back a higher % of their gap

## 📂 Project Structure

```
uk-corporation-tax-gap/
├── Final_Project_Dashboard.py          # Main Dash application
├── FInal_Project.ipynb                 # Data analysis & visualization code
├── data/
│   ├── dashboard_ct_gap_timeseries.csv # CT gap components 2005–2024
│   ├── dashboard_sector_timeseries.csv # Sector liabilities by year
│   ├── dashboard_segment_gap_history.csv # Taxpayer group gap over time
│   └── dashboard_segment_snapshot.csv  # Current-year metrics by group
├── documentation/
│   ├── Data_Dictionary.docx            # Column definitions
│   ├── Data_Project_Handbook_v1_2.docx # Methodology & findings
│   └── README.md                       # This file
└── requirements.txt                    # Python dependencies
```

## 📋 Data Overview

### Key Datasets

**1. Corporation Tax Gap Time Series (2005–2024)**
- Gross tax gap (£bn)
- Compliance yield (what HMRC recovered)
- Net tax gap (what remains uncollected)
- Proportion of liabilities

**2. Sector Data (2018–2024)**
- CT liability per sector (£m)
- Number of liable companies
- Liability per company (£k)
- Effective CT rate (%)
- Loss ratio (%)
- CT share (% of total)

**3. Taxpayer Segment Data**
- Population size
- PAYE/NICS receipts
- Other receipts
- Compliance yield
- Compliance spend
- Tax gap
- Yield as % of gap
- Spend per pound of yield
- Gap per entity

### Data Source
HM Revenue & Customs (HMRC) – Official tax gap estimates and compliance data

## 🔬 How to Read the Dashboard

### The Tax Gap: Three Versions

- **Gross gap** – The total tax *not* paid (widest measure)
- **Compliance yield** – HMRC's recovery efforts (shown as a line, not a gap)
- **Net gap** – What's left after HMRC recovers some (the real problem)

Think of it this way: Businesses owe 100. They pay 70. HMRC chases them and recovers 10. The gross gap is 30, compliance yield is 10, net gap is 20.

### Taxpayer Segments Explained

HMRC groups taxpayers by size and type:

| Group | Size | Typical | Tax Gap Challenge |
|-------|------|---------|------------------|
| **Individual customers** | 37M | Employees, self-employed | Largest *group* gap (2.2bn), but smallest per person |
| **Wealthy individuals** | 950k | High-net-worth individuals | Complex returns, higher compliance spend per pound recovered |
| **Small businesses** | 5.1M | Traders, partnerships | Largest *absolute* gap (28bn)—sheer volume matters |
| **Mid-sized** | 380k | Charities, public bodies, medium firms | Moderate gap (4.4bn) |
| **Large businesses** | 2k | FTSE, major corporations | Small absolute gap (5.8bn) but HIGHEST % recovered (339.7%) |

**Key insight:** "Largest gap" ≠ "most dodgy." Small businesses dominate in absolute numbers because there are millions of them and compliance support is weaker.

## 🚀 Getting Started

### Prerequisites
- Python 3.7+
- pip

### Installation

```bash
git clone https://github.com/yourusername/uk-corporation-tax-gap.git
cd uk-corporation-tax-gap
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Running the Dashboard

```bash
python Final_Project_Dashboard.py
```

Open your browser to **http://127.0.0.1:8050/** and explore.

Press `Ctrl+C` to stop the server.

## 📊 Key Insights

**From the data:**

- **Financial services dominates:** Financial & Insurance sector accounts for ~£19.6bn (2023–24), almost double the second-place sector
- **Tax gap has shrunk overall:** From ~£8–9bn in 2005–06 down to ~£5–6bn by 2012, with some volatility since
- **Small businesses = big gap:** Despite being individually compliant, the sheer volume of small firms makes them the largest contributor (28bn in 2023–24)
- **HMRC's recovery varies wildly:** Large businesses recover 339.7% of their gap (they overpay!), while small businesses recover only 27.9%
- **Recent trends:** Individual customers' gap has grown from 19bn (2019–20) to 26bn (2023–24)

## 💡 Real-World Applications

This dashboard answers questions like:

- **For HMRC:** Where should we focus compliance resources for maximum return?
- **For policymakers:** Which sectors need better regulation or support?
- **For analysts:** Is the tax gap a structural problem or are we catching up?
- **For researchers:** What patterns emerge when you compare sectors, taxpayer types, and time periods?

## 📚 How the Data Was Built

See `FInal_Project.ipynb` for the full analysis pipeline:

1. **Data ingestion** – Loading HMRC published data
2. **Cleaning** – Handling missing values, sector code mapping
3. **Aggregation** – Rolling up by sector, year, and taxpayer group
4. **Calculations** – Deriving metrics like yield % of gap, spend per pound yield
5. **Validation** – Checking totals against official HMRC reports

## 🔍 Data Dictionary

See `Data_Dictionary.docx` for full column definitions, but here are the key ones:

| Column | Meaning |
|--------|---------|
| `tax_gap_gbp_bn` | Total CT not paid (£bn) |
| `compliance_yield_gbp_bn` | Amount HMRC recovered (£bn) |
| `yield_pct_of_gap` | % of gap that HMRC recovered |
| `ct_liability_gbp_m` | Total CT owed in that sector (£m) |
| `companies_liable` | Number of companies in that sector |
| `liability_per_company_gbp_k` | Average CT per firm (£k) |
| `gap_pct_of_receipts` | Tax gap as % of actual receipts (compliance rate) |

## ⚠️ Limitations

- **Published data only** – Based on HMRC's own estimates, which have margins of uncertainty
- **Sector classifications change** – Industry codes aren't perfectly stable across all years
- **Causation unclear** – Correlation doesn't explain why sectors have different gaps
- **Recent data provisional** – 2023–24 figures may be revised

## 🚧 Future Improvements

- Regional breakdowns (Scotland, Northern Ireland, etc.)
- Industry-specific deep dives with qualitative context
- Predictive modelling for future tax gap trends
- Comparison with other tax types (VAT, Income Tax)
- Drill-down from sector → individual company (privacy permitting)

## 📄 License

This project is provided for educational and analytical purposes. Data sourced from public HMRC reports.

## ✉️ Questions?

Have insights, spot errors, or want to collaborate? Open an issue or get in touch. Tax data can be dry—let's make it interesting.

---

**Built with:** Python • Pandas • Plotly • Dash  
**Data source:** HM Revenue & Customs  
**Last updated:** 2024
