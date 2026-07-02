
import pandas as pd                          # for loading and working with CSV data
import plotly.express as px                  # for drawing charts
from dash import Dash, html, dcc, Output, Input, dash_table  # for building the webpage
 
import os
 
# ============================================================
# STEP 1 — LOAD THE DATA
# ============================================================
# os.path.join builds the full file path so the script always
# finds the CSVs no matter which folder you run it from.
 
BASE_DIR = r"C:\Users\anti0\OneDrive\Desktop\SCQF8_Final_Project"
 
# CSV 1: Corporation Tax gap broken into components, 2005–2024
ct_gap = pd.read_csv(os.path.join(BASE_DIR, "dashboard_ct_gap_timeseries.csv"))
 
# CSV 2: CT liabilities split by industry sector and year
sector_ts = pd.read_csv(os.path.join(BASE_DIR, "dashboard_sector_timeseries.csv"))
 
# CSV 3: Tax gap per taxpayer type (small biz, large biz, etc.) over time
seg_history = pd.read_csv(os.path.join(BASE_DIR, "dashboard_segment_gap_history.csv"))
 
# CSV 4: A single-year snapshot comparing taxpayer types on several metrics
seg_snap = pd.read_csv(os.path.join(BASE_DIR, "dashboard_segment_snapshot.csv"))
 
# ============================================================
# STEP 2 — CLEAN UP SECTOR CODES
# ============================================================
# The sector CSV uses single letters (A, B, C…) from the UK's
# standard industry classification (SIC 2007). We map them to
# full names so the charts are readable.
 
SECTOR_NAMES = {
    "A": "Agriculture, Forestry & Fishing",
    "B": "Mining & Quarrying",
    "C": "Manufacturing",
    "D": "Electricity, Gas & Steam",
    "E": "Water & Waste Management",
    "F": "Construction",
    "G": "Wholesale & Retail Trade",
    "H": "Transportation & Storage",
    "I": "Accommodation & Food Services",
    "J": "Information & Communication",
    "K": "Financial & Insurance",
    "L": "Real Estate",
    "M": "Professional, Scientific & Technical",
    "N": "Administrative & Support Services",
    "O": "Public Administration & Defence",
    "P": "Education",
    "Q": "Human Health & Social Work",
    "R": "Arts, Entertainment & Recreation",
    "S": "Other Service Activities",
    "T": "Households as Employers",
}
 
# Add a new column called "sector_name" with the full name
sector_ts["sector_name"] = sector_ts["sector_code"].map(SECTOR_NAMES)
 
# ============================================================
# STEP 3 — CREATE THE APP
# ============================================================
# Dash(__name__) creates the web application.
 
app = Dash(__name__)
 
# ============================================================
# STEP 4 — DEFINE THE LAYOUT (what the page looks like)
# ============================================================
# html.Div is like a <div> in HTML — a box that holds content.
# dcc.Tabs creates clickable tabs.
# dcc.Graph is where a chart will appear.
 
app.layout = html.Div(
    style={
        "fontFamily": "Arial, sans-serif",
        "maxWidth": "1100px",   # centres the page and stops it going too wide
        "margin": "0 auto",
        "padding": "30px",
        "backgroundColor": "white",
    },
    children=[
 
        # ── Page title ──────────────────────────────────────────
        html.H1(
            "UK Corporation Tax Gap Dashboard",
            style={"color": "#1a2e44", "marginBottom": "4px"}
        ),
        html.P(
            "Exploring which sectors and taxpayer types carry the greatest compliance risk.",
            style={"color": "#555", "marginTop": "0", "marginBottom": "24px"}
        ),
 
        # ── Plain-English glossary box ───────────────────────────
        # Collapsed by default so it doesn't overwhelm the page.
        # Click the arrow to expand it.
        html.Details([
            html.Summary(
                "📖 What do these terms mean? (click to expand)",
                style={"fontWeight": "bold", "cursor": "pointer", "color": "#2980b9"}
            ),
            html.Div(style={"padding": "14px 0 4px 0", "lineHeight": "1.8"}, children=[
                html.P([html.Strong("Tax gap: "), "The difference between the tax HMRC thinks should be paid and the tax that is actually collected. Think of it as 'missing tax'."]),
                html.P([html.Strong("Gross tax gap: "), "The total missing tax before HMRC recovers any of it through compliance work."]),
                html.P([html.Strong("Net tax gap: "), "The missing tax that remains after HMRC's recovery efforts."]),
                html.P([html.Strong("Compliance yield: "), "The money HMRC successfully recovers through audits, investigations, and other enforcement activity."]),
                html.P([html.Strong("CT liability: "), "The amount of Corporation Tax a company legally owes. Higher liability in a sector = more tax at stake."]),
                html.P([html.Strong("Liability per company: "), "CT liability divided by number of companies. High values mean a small number of firms owe a lot — concentrated risk."]),
                html.P([html.Strong("Taxpayer segment: "), "HMRC groups taxpayers by size — Large Businesses, Mid-sized Businesses, Small Businesses, Wealthy Individuals, etc. Each group is handled by a different HMRC team."]),
                html.P([html.Strong("Yield % of gap: "), "What percentage of the tax gap HMRC is actually recovering. Higher = more efficient."]),
                html.P([html.Strong("Spend per £1 yield: "), "How much it costs HMRC to recover £1 of tax. Lower = better value."]),
            ])
        ], style={
            "backgroundColor": "#f0f6ff",
            "border": "1px solid #c0d8f0",
            "borderRadius": "8px",
            "padding": "14px 18px",
            "marginBottom": "28px",
        }),
 
        # ── Tabs ────────────────────────────────────────────────
        dcc.Tabs(
            id="tabs",
            value="tab-sector",   # which tab opens by default
            children=[
                dcc.Tab(label="① Which sectors owe the most tax?",    value="tab-sector"),
                dcc.Tab(label="② Is the tax gap growing over time?",  value="tab-ct"),
                dcc.Tab(label="③ Who is responsible for the gap?",    value="tab-seg"),
            ]
        ),
 
        # Tab content goes here — filled by the callback below
        html.Div(id="tab-content", style={"paddingTop": "24px"}),
    ]
)
 
# ============================================================
# STEP 5 — TAB CONTENT
# ============================================================
# A "callback" is a function that runs automatically when the
# user does something (like clicking a tab). The @app.callback
# decorator tells Dash: "when the tab changes, run this function
# and put the result into the 'tab-content' div".
 
@app.callback(
    Output("tab-content", "children"),   # where to put the result
    Input("tabs", "value")               # what triggers the function
)
def show_tab(selected_tab):
 
    # ── TAB 1: Which sectors owe the most tax? ─────────────────
    if selected_tab == "tab-sector":
 
        years = sorted(sector_ts["year"].dropna().unique().tolist())
 
        return html.Div([
 
            html.H2("Which sectors owe the most Corporation Tax?"),
            html.P(
                "This bar chart ranks every industry sector by how much Corporation Tax companies in that "
                "sector owe. Sectors at the top are where the most money — and therefore the most compliance "
                "risk — sits. Use the dropdown to switch between total liability, average per company, or "
                "number of companies."
            ),
 
            # Controls row
            html.Div([
                html.Div([
                    html.Label("Select year:", style={"fontWeight": "bold"}),
                    dcc.Dropdown(
                        id="sector-year",
                        options=[{"label": y, "value": y} for y in years],
                        value=years[-1],   # default: most recent year
                        clearable=False,
                    ),
                ], style={"width": "160px", "display": "inline-block", "marginRight": "24px", "verticalAlign": "top"}),
 
                html.Div([
                    html.Label("Show me:", style={"fontWeight": "bold"}),
                    dcc.Dropdown(
                        id="sector-metric",
                        options=[
                            {"label": "Total tax owed by sector (£m)",         "value": "ct_liability_gbp_m"},
                            {"label": "Average tax per company (£k)",          "value": "liability_per_company_gbp_k"},
                            {"label": "Number of companies paying tax",        "value": "companies_liable"},
                        ],
                        value="ct_liability_gbp_m",
                        clearable=False,
                    ),
                ], style={"width": "340px", "display": "inline-block", "verticalAlign": "top"}),
            ], style={"marginBottom": "16px"}),
 
            dcc.Graph(id="sector-chart", style={"height": "540px"}),
        ])
 
    # ── TAB 2: Is the tax gap growing over time? ───────────────
    elif selected_tab == "tab-ct":
 
        components = ct_gap["component"].unique().tolist()
 
        return html.Div([
 
            html.H2("Is the Corporation Tax gap getting bigger?"),
            html.P(
                "Each line shows a different part of the tax gap story over time. "
                "The gross gap is the total missing tax. The net gap is what's left after HMRC recovers some. "
                "Compliance yield is what HMRC successfully chases down. Tick or untick lines to focus on what matters to you."
            ),
 
            dcc.Checklist(
                id="ct-lines",
                options=[{"label": c, "value": c} for c in components],
                value=["Gross tax gap", "Net tax gap", "Compliance yield"],
                inline=True,
                style={"marginBottom": "14px"},
            ),
 
            dcc.Graph(id="ct-chart", style={"height": "480px"}),
        ])
 
    # ── TAB 3: Who is responsible for the gap? ─────────────────
    elif selected_tab == "tab-seg":
 
        segments = seg_history["segment"].unique().tolist()
 
        return html.Div([
 
            html.H2("Who is responsible for the tax gap?"),
            html.P(
                "HMRC divides taxpayers into groups by size. This chart shows how much of the tax gap "
                "each group accounts for, and how that has changed since 2019. Small businesses "
                "typically make up the largest share — not because they're dishonest, but because "
                "there are so many of them and they have less support to get their tax right."
            ),
 
            html.Div([
                html.Label("Select groups to compare:", style={"fontWeight": "bold"}),
                dcc.Checklist(
                    id="seg-groups",
                    options=[{"label": s, "value": s} for s in segments],
                    value=segments,
                    inline=True,
                    style={"marginBottom": "12px"},
                ),
                html.Label("Show:", style={"fontWeight": "bold"}),
                dcc.RadioItems(
                    id="seg-metric",
                    options=[
                        {"label": "Tax gap in £ billions",                "value": "gap_gbp_bn"},
                        {"label": "Tax gap as % of what should be paid",  "value": "gap_pct_of_liabilities"},
                    ],
                    value="gap_gbp_bn",
                    inline=True,
                    style={"marginBottom": "14px"},
                ),
            ]),
 
            dcc.Graph(id="seg-chart", style={"height": "460px"}),
 
            html.Hr(),
 
            # Snapshot bar chart below the line chart
            html.H3("How efficient is HMRC at recovering tax from each group? (2023–24)"),
            html.P(
                "This compares HMRC's performance across groups for the most recent year. "
                "Use the dropdown to switch between different measures of efficiency."
            ),
 
            dcc.Dropdown(
                id="snap-metric",
                options=[
                    {"label": "Tax gap (£bn) — how much is missing",                 "value": "tax_gap_gbp_bn"},
                    {"label": "Compliance yield (£bn) — how much HMRC recovered",    "value": "compliance_yield_gbp_bn"},
                    {"label": "% of missing tax that HMRC recovered",                "value": "yield_pct_of_gap"},
                    {"label": "Cost to HMRC of recovering £1",                       "value": "spend_per_pound_yield"},
                ],
                value="yield_pct_of_gap",
                clearable=False,
                style={"width": "440px", "marginBottom": "14px"},
            ),
 
            dcc.Graph(id="snap-chart", style={"height": "420px"}),
        ])
 
 
# ============================================================
# STEP 6 — CHART CALLBACKS
# ============================================================
# These functions draw the actual charts. Each one:
# 1. Filters the data based on what the user selected
# 2. Builds a chart using plotly.express (px)
# 3. Returns the chart to be displayed
 
# Tab 1 chart
@app.callback(
    Output("sector-chart", "figure"),
    Input("sector-year", "value"),
    Input("sector-metric", "value"),
)
def draw_sector_chart(year, metric):
    # Filter data to just the selected year, remove rows with missing values
    df = sector_ts[sector_ts["year"] == year].dropna(subset=[metric]).copy()
    df = df.sort_values(metric, ascending=True)  # sort so biggest bar is at top
 
    # Friendly axis labels
    axis_label = {
        "ct_liability_gbp_m":          "Total CT Liability (£m)",
        "liability_per_company_gbp_k": "Average per Company (£k)",
        "companies_liable":            "Number of Companies",
    }[metric]
 
    fig = px.bar(
        df,
        x=metric,
        y="sector_name",
        orientation="h",                    # horizontal bar chart
        color=metric,
        color_continuous_scale="Blues",
        title=f"{axis_label} by Sector — {year}",
        labels={metric: axis_label, "sector_name": "Sector"},
        text=metric,
    )
    fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
    fig.update_layout(coloraxis_showscale=False, yaxis_title="", margin={"l": 280})
    return fig
 
 
# Tab 2 chart
@app.callback(
    Output("ct-chart", "figure"),
    Input("ct-lines", "value"),
)
def draw_ct_chart(selected_lines):
    df = ct_gap[ct_gap["component"].isin(selected_lines or [])]
    fig = px.line(
        df,
        x="year",
        y="value_gbp_bn",
        color="component",
        markers=True,
        title="Corporation Tax Gap Over Time (2005–2024)",
        labels={"year": "Year", "value_gbp_bn": "Amount (£bn)", "component": ""},
    )
    fig.update_layout(xaxis_tickangle=-45, legend_title_text="")
    return fig
 
 
# Tab 3 — segment trend chart
@app.callback(
    Output("seg-chart", "figure"),
    Input("seg-groups", "value"),
    Input("seg-metric", "value"),
)
def draw_seg_chart(selected_groups, metric):
    df = seg_history[seg_history["segment"].isin(selected_groups or [])]
    y_label = {
        "gap_gbp_bn":             "Tax Gap (£bn)",
        "gap_pct_of_liabilities": "Gap as % of Liabilities",
    }[metric]
    fig = px.line(
        df,
        x="year",
        y=metric,
        color="segment",
        markers=True,
        title=f"Tax Gap by Taxpayer Group — {y_label}",
        labels={"year": "Year", metric: y_label, "segment": ""},
    )
    fig.update_layout(xaxis_tickangle=-40, legend_title_text="")
    return fig
 
 
# Tab 3 — snapshot bar chart
@app.callback(
    Output("snap-chart", "figure"),
    Input("snap-metric", "value"),
)
def draw_snap_chart(metric):
    axis_label = {
        "tax_gap_gbp_bn":          "Tax Gap (£bn)",
        "compliance_yield_gbp_bn": "Compliance Yield (£bn)",
        "yield_pct_of_gap":        "% of Gap Recovered by HMRC",
        "spend_per_pound_yield":   "Cost per £1 Recovered (£)",
    }[metric]
 
    df = seg_snap.sort_values(metric, ascending=False)
    fig = px.bar(
        df,
        x="segment",
        y=metric,
        color=metric,
        color_continuous_scale="Teal",
        title=f"2023–24 Snapshot: {axis_label} by Taxpayer Group",
        labels={"segment": "Taxpayer Group", metric: axis_label},
        text=metric,
    )
    fig.update_traces(texttemplate="%{text:,.2f}", textposition="outside")
    fig.update_layout(coloraxis_showscale=False, xaxis_tickangle=-10)
    return fig


# ── Run ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)