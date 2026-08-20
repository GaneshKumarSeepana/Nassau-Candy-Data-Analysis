import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Nassau Candy Analytics",
    page_icon="🍫",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ==============================
       MAIN PAGE
       ============================== */

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    /* ==============================
       SIDEBAR
       ============================== */

    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #111827 0%,
            #172033 100%
        );
    }


    /* Make ALL normal sidebar text visible */

    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label {
        color: #f8fafc !important;
    }


    /* ==============================
       SIDEBAR MAIN TITLE
       ============================== */

    section[data-testid="stSidebar"] h3 {
        color: #ffffff !important;
        font-weight: 800 !important;
        letter-spacing: -0.01em;
    }


    /* ==============================
       SIDEBAR CAPTION
       ============================== */

    section[data-testid="stSidebar"] .stCaption {
        color: #cbd5e1 !important;
    }


    /* ==============================
       SIDEBAR SECTION TITLES
       ============================== */

    .sidebar-section-title {
        color: #ffffff !important;
        font-size: 0.82rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        margin-top: 1rem;
        margin-bottom: 0.45rem;
    }


    /* ==============================
       CURRENT FILTERS TITLE
       ============================== */

    section[data-testid="stSidebar"] h4 {
        color: #ffffff !important;
        font-weight: 800 !important;
        letter-spacing: 0.06em;
        margin-top: 1rem;
    }


    /* ==============================
       SIDEBAR SELECT BOXES
       ============================== */

    section[data-testid="stSidebar"]
    div[data-baseweb="select"] {
        background-color: #ffffff !important;
        border-radius: 10px !important;
        border: 1px solid #d1d5db !important;
    }


    section[data-testid="stSidebar"]
    div[data-baseweb="select"] span {
        color: #111827 !important;
    }


    section[data-testid="stSidebar"]
    div[data-baseweb="select"] input {
        color: #111827 !important;
    }


    /* ==============================
       SIDEBAR DATE INPUT
       ============================== */

    section[data-testid="stSidebar"]
    div[data-testid="stDateInput"] input {
        background-color: #ffffff !important;
        color: #111827 !important;
        border-radius: 10px !important;
    }


    /* ==============================
       RESET BUTTON
       ============================== */

    section[data-testid="stSidebar"]
    div.stButton > button {
        width: 100% !important;
        background: linear-gradient(
            135deg,
            #f97316,
            #ea580c
        ) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        min-height: 44px !important;
    }


    section[data-testid="stSidebar"]
    div.stButton > button:hover {
        background: linear-gradient(
            135deg,
            #fb923c,
            #f97316
        ) !important;
        color: white !important;
    }


    section[data-testid="stSidebar"]
    div.stButton > button p {
        color: white !important;
        font-weight: 700 !important;
    }


    /* ==============================
       KPI CARDS
       ============================== */

    /*
       Keep KPI cards readable in BOTH Streamlit light and dark modes.
       Streamlit changes the app theme, but these cards intentionally
       stay white with dark text so the numbers are always visible.
    */
    div[data-testid="stMetric"] {
        background: #ffffff !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 14px !important;
        padding: 18px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
        color: #172033 !important;
    }

    /* KPI labels */
    div[data-testid="stMetric"] label,
    div[data-testid="stMetric"] [data-testid="stMetricLabel"],
    div[data-testid="stMetric"] [data-testid="stMetricLabel"] * {
        color: #334155 !important;
    }

    /* KPI values - the important dark-mode fix */
    div[data-testid="stMetric"] [data-testid="stMetricValue"],
    div[data-testid="stMetric"] [data-testid="stMetricValue"] *,
    div[data-testid="stMetric"] [data-testid="stMetricValue"] div,
    div[data-testid="stMetric"] [data-testid="stMetricValue"] span,
    div[data-testid="stMetric"] [data-testid="stMetricValue"] p {
        color: #172033 !important;
        -webkit-text-fill-color: #172033 !important;
    }

    /* KPI delta / secondary text */
    div[data-testid="stMetric"] [data-testid="stMetricDelta"],
    div[data-testid="stMetric"] [data-testid="stMetricDelta"] * {
        color: #475569 !important;
        -webkit-text-fill-color: #475569 !important;
    }

    /*
       Do NOT use html[data-theme="dark"] here.
       Streamlit versions can expose the theme differently, and a
       dark-mode override can make white KPI text appear on white cards.
    */

    /* ==============================
       HEADINGS
       ============================== */

    h1 {
        font-weight: 800 !important;
        letter-spacing: -0.03em;
    }


    h2,
    h3 {
        font-weight: 700 !important;
    }


    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATA
# ============================================================

DATA_PATH = "data/Nassau Candy Distributor_Cleaned.csv"

df = pd.read_csv(DATA_PATH)

df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    errors="coerce"
)

df = df.dropna(
    subset=["Order Date"]
)


# ============================================================
# DATE INFORMATION
# ============================================================

min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()


# ============================================================
# SESSION STATE
# ============================================================

if "date_mode" not in st.session_state:
    st.session_state.date_mode = "All Data"

if "division_filter" not in st.session_state:
    st.session_state.division_filter = "All Divisions"

if "product_filter" not in st.session_state:
    st.session_state.product_filter = []

if "custom_start" not in st.session_state:
    st.session_state.custom_start = min_date

if "custom_end" not in st.session_state:
    st.session_state.custom_end = max_date

if "margin_threshold" not in st.session_state:
    st.session_state.margin_threshold = 20


# ============================================================
# RESET FILTERS
# ============================================================

def reset_filters():

    st.session_state.date_mode = "All Data"

    st.session_state.division_filter = "All Divisions"

    st.session_state.product_filter = []

    st.session_state.custom_start = min_date

    st.session_state.custom_end = max_date
    st.session_state.margin_threshold = 20


# ============================================================
# PAGE HEADER
# ============================================================

st.title("🍫 Nassau Candy Distributor")

st.subheader(
    "Product Profitability & Margin Performance Analysis"
)

st.write(
    "Interactive analysis of sales, profitability, products, "
    "divisions, trends, and margin performance."
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    # --------------------------------------------------------
    # SIDEBAR HEADER
    # --------------------------------------------------------

    st.markdown(
        """
        <div style="
            color: #ffffff;
            font-size: 1.25rem;
            font-weight: 800;
            margin-bottom: 4px;
        ">
            🎛️ Dashboard Filters
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="
            color: #cbd5e1;
            font-size: 0.85rem;
            margin-bottom: 18px;
        ">
            Refine your analysis instantly
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # DATE RANGE
    # ========================================================

    st.markdown(
        '<div class="sidebar-section-title">📅 DATE RANGE</div>',
        unsafe_allow_html=True
    )

    date_mode = st.selectbox(
        "Select period",
        [
            "All Data",
            "2024",
            "2025",
            "Custom Range"
        ],
        key="date_mode",
        label_visibility="collapsed"
    )


    # --------------------------------------------------------
    # CUSTOM DATE RANGE
    # --------------------------------------------------------

    if date_mode == "Custom Range":

        st.caption(
            "Choose your date range"
        )

        custom_start = st.date_input(
            "Start date",
            min_value=min_date,
            max_value=max_date,
            key="custom_start"
        )

        custom_end = st.date_input(
            "End date",
            min_value=min_date,
            max_value=max_date,
            key="custom_end"
        )

        if custom_start > custom_end:

            st.error(
                "Start date must be before end date."
            )


    # ========================================================
    # DIVISION
    # ========================================================

    st.markdown(
        '<div class="sidebar-section-title">🏢 DIVISION</div>',
        unsafe_allow_html=True
    )

    division_options = sorted(
        df["Division"]
        .dropna()
        .astype(str)
        .unique()
    )

    division_filter = st.selectbox(
        "Select division",
        ["All Divisions"] + division_options,
        key="division_filter",
        label_visibility="collapsed"
    )


    # ========================================================
    # PRODUCTS
    # ========================================================

    st.markdown(
        '<div class="sidebar-section-title">🍫 PRODUCTS</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Search and select products"
    )

    product_options = sorted(
        df["Product Name"]
        .dropna()
        .astype(str)
        .unique()
    )

    selected_products = st.multiselect(
        "Select products",
        product_options,
        key="product_filter",
        placeholder="All products",
        label_visibility="collapsed"
    )


    # ========================================================
    # MARGIN RISK THRESHOLD
    # ========================================================

    st.markdown(
        '<div class="sidebar-section-title">🎯 MARGIN RISK THRESHOLD</div>',
        unsafe_allow_html=True
    )

    margin_threshold = st.slider(
        "Margin risk threshold",
        min_value=0,
        max_value=100,
        value=st.session_state.margin_threshold,
        step=1,
        format="%d%%",
        key="margin_threshold",
        help="Products with gross margin below this threshold are flagged as margin risk."
    )

    st.caption(
        f"Products below {margin_threshold}% gross margin are flagged as margin risk."
    )


    # ========================================================
    # RESET BUTTON
    # ========================================================

    st.divider()

    st.button(
        "🔄  Reset All Filters",
        width="stretch",
        on_click=reset_filters
    )


    # ========================================================
    # CURRENT FILTERS
    # ========================================================

    st.markdown(
        """
        <div style="
            color: #ffffff;
            font-size: 0.82rem;
            font-weight: 800;
            letter-spacing: 0.08em;
            margin-top: 16px;
            margin-bottom: 10px;
        ">
            CURRENT FILTERS
        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # DATE SUMMARY
    # --------------------------------------------------------

    if date_mode == "All Data":

        date_summary = (
            f"{min_date.strftime('%d %b %Y')} "
            f"→ "
            f"{max_date.strftime('%d %b %Y')}"
        )

    elif date_mode == "2024":

        date_summary = "January 2024 → December 2024"

    elif date_mode == "2025":

        date_summary = "January 2025 → December 2025"

    else:

        if custom_start <= custom_end:

            date_summary = (
                f"{custom_start.strftime('%d %b %Y')} "
                f"→ "
                f"{custom_end.strftime('%d %b %Y')}"
            )

        else:

            date_summary = "Invalid date range"


    # --------------------------------------------------------
    # CURRENT FILTERS - DATE
    # --------------------------------------------------------

    with st.container(border=True):

        st.caption("📅 DATE")

        st.write(
            date_summary
        )


    # --------------------------------------------------------
    # CURRENT FILTERS - DIVISION
    # --------------------------------------------------------

    with st.container(border=True):

        st.caption("🏢 DIVISION")

        st.write(
            division_filter
        )


    # --------------------------------------------------------
    # CURRENT FILTERS - PRODUCTS
    # --------------------------------------------------------

    with st.container(border=True):

        st.caption("🍫 PRODUCTS")

        if not selected_products:

            st.write(
                "All products"
            )

        elif len(selected_products) == 1:

            st.write(
                selected_products[0]
            )

        else:

            st.write(
                f"{len(selected_products)} products selected"
            )


    # --------------------------------------------------------
    # CURRENT FILTERS - MARGIN THRESHOLD
    # --------------------------------------------------------

    with st.container(border=True):

        st.caption("🎯 MARGIN RISK")

        st.write(
            f"Below {margin_threshold}%"
        )


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()


# ============================================================
# DATE FILTER
# ============================================================

if date_mode == "2024":

    start_date = pd.Timestamp(
        "2024-01-01"
    )

    end_date = pd.Timestamp(
        "2025-01-01"
    )

    filtered_df = filtered_df[
        (filtered_df["Order Date"] >= start_date)
        &
        (filtered_df["Order Date"] < end_date)
    ]


elif date_mode == "2025":

    start_date = pd.Timestamp(
        "2025-01-01"
    )

    end_date = pd.Timestamp(
        "2026-01-01"
    )

    filtered_df = filtered_df[
        (filtered_df["Order Date"] >= start_date)
        &
        (filtered_df["Order Date"] < end_date)
    ]


elif date_mode == "Custom Range":

    if custom_start <= custom_end:

        start_date = pd.Timestamp(
            custom_start
        )

        end_date = (
            pd.Timestamp(custom_end)
            + pd.Timedelta(days=1)
        )

        filtered_df = filtered_df[
            (filtered_df["Order Date"] >= start_date)
            &
            (filtered_df["Order Date"] < end_date)
        ]

    else:

        filtered_df = filtered_df.iloc[0:0]


# ============================================================
# DIVISION FILTER
# ============================================================

if division_filter != "All Divisions":

    filtered_df = filtered_df[
        filtered_df["Division"]
        == division_filter
    ]


# ============================================================
# PRODUCT FILTER
# ============================================================

if selected_products:

    filtered_df = filtered_df[
        filtered_df["Product Name"].isin(
            selected_products
        )
    ]


# ============================================================
# ANALYSIS STATUS
# ============================================================

status_container = st.container(
    border=True
)

with status_container:

    st.markdown(
        "### 🔎 Analysis Status"
    )

    st.write(
        f"Showing **{len(filtered_df):,}** "
        f"records from **{len(df):,}** total records."
    )


# ============================================================
# EMPTY DATA CHECK
# ============================================================

if filtered_df.empty:

    st.warning(
        "⚠️ No data matches the selected filters. "
        "Try changing the date, division, or product."
    )

    st.stop()


# ============================================================
# KEY BUSINESS METRICS
# ============================================================

total_sales = filtered_df["Sales"].sum()

total_profit = filtered_df["Gross Profit"].sum()

total_units = filtered_df["Units"].sum()


if total_sales > 0:

    gross_margin = (
        total_profit
        / total_sales
        * 100
    )

else:

    gross_margin = 0


# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "💰 Total Sales",
        f"${total_sales:,.2f}"
    )


with col2:

    st.metric(
        "📈 Total Gross Profit",
        f"${total_profit:,.2f}"
    )


with col3:

    st.metric(
        "🎯 Gross Margin",
        f"{gross_margin:.2f}%"
    )


with col4:

    st.metric(
        "📦 Total Units Sold",
        f"{total_units:,.0f}"
    )


# ============================================================
# DATASET OVERVIEW
# ============================================================

st.divider()

st.header(
    "📊 Dataset Overview"
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Orders",
        f"{filtered_df['Order ID'].nunique():,}"
    )


with col2:

    st.metric(
        "Customers",
        f"{filtered_df['Customer ID'].nunique():,}"
    )


with col3:

    st.metric(
        "Products",
        f"{filtered_df['Product ID'].nunique():,}"
    )


with col4:

    st.metric(
        "Divisions",
        f"{filtered_df['Division'].nunique():,}"
    )


# ============================================================
# SELECTED DATA PERIOD
# ============================================================

st.divider()


actual_min_date = (
    filtered_df["Order Date"]
    .min()
    .strftime("%d %B %Y")
)


actual_max_date = (
    filtered_df["Order Date"]
    .max()
    .strftime("%d %B %Y")
)


st.write(
    f"📅 **Selected Data Period:** "
    f"{actual_min_date} → {actual_max_date}"
)


# ============================================================
# PRODUCT PROFITABILITY ANALYSIS
# ============================================================

st.divider()

st.header("🍫 Product Profitability Analysis")

st.write(
    "Compare product-level sales, gross profit, and margin "
    "to identify the most profitable products."
)


# ============================================================
# PRODUCT SUMMARY
# ============================================================

product_summary = (
    filtered_df
    .groupby("Product Name", as_index=False)
    .agg(
        Sales=("Sales", "sum"),
        Gross_Profit=("Gross Profit", "sum"),
        Units=("Units", "sum")
    )
)


# ============================================================
# CALCULATE GROSS MARGIN
# ============================================================

product_summary["Gross Margin %"] = (
    product_summary["Gross_Profit"]
    / product_summary["Sales"]
    * 100
)


# ============================================================
# SORT BY GROSS PROFIT
# ============================================================

product_summary = product_summary.sort_values(
    "Gross_Profit",
    ascending=False
)


# ============================================================
# DISPLAY TOP PRODUCTS
# ============================================================

st.subheader("🏆 Top Products by Gross Profit")

top_products = product_summary.head(10).copy()

top_products = top_products.set_index(
    "Product Name"
)


st.bar_chart(
    top_products["Gross_Profit"],
    width="stretch"
)


# ============================================================
# PRODUCT PERFORMANCE TABLE
# ============================================================

st.subheader("📋 Product Performance")

display_product_summary = product_summary.copy()

display_product_summary["Sales"] = (
    display_product_summary["Sales"]
    .map(lambda x: f"${x:,.2f}")
)

display_product_summary["Gross_Profit"] = (
    display_product_summary["Gross_Profit"]
    .map(lambda x: f"${x:,.2f}")
)

display_product_summary["Gross Margin %"] = (
    display_product_summary["Gross Margin %"]
    .map(lambda x: f"{x:.2f}%")
)

display_product_summary["Units"] = (
    display_product_summary["Units"]
    .map(lambda x: f"{x:,.0f}")
)


st.dataframe(
    display_product_summary,
    width="stretch",
    hide_index=True
)


# ============================================================
# DIVISION PERFORMANCE ANALYSIS
# ============================================================

st.divider()

st.header("🏢 Division Performance Analysis")

st.write(
    "Compare sales, gross profit, units sold, and gross margin "
    "across business divisions."
)


# ============================================================
# DIVISION SUMMARY
# ============================================================

division_summary = (
    filtered_df
    .groupby("Division", as_index=False)
    .agg(
        Sales=("Sales", "sum"),
        Gross_Profit=("Gross Profit", "sum"),
        Units=("Units", "sum")
    )
)


# ============================================================
# CALCULATE DIVISION GROSS MARGIN
# ============================================================

division_summary["Gross Margin %"] = (
    division_summary["Gross_Profit"]
    / division_summary["Sales"]
    * 100
)


# ============================================================
# SORT BY GROSS PROFIT
# ============================================================

division_summary = division_summary.sort_values(
    "Gross_Profit",
    ascending=False
)


# ============================================================
# DIVISION SUMMARY CARDS
# ============================================================

st.subheader("📊 Division Summary")

if not division_summary.empty:

    division_columns = st.columns(
        min(len(division_summary), 3)
    )

    for index, row in division_summary.reset_index(
        drop=True
    ).iterrows():

        if index >= 3:
            break

        with division_columns[index]:

            st.metric(
                row["Division"],
                f"${row['Gross_Profit']:,.2f}",
                f"{row['Gross Margin %']:.2f}% margin"
            )


# ============================================================
# DIVISION GROSS PROFIT CHART
# ============================================================

# ============================================================
# INTERACTIVE DIVISION GROSS PROFIT CHART
# ============================================================

st.subheader("💰 Gross Profit by Division")

if not division_summary.empty:

    division_chart = (
        division_summary
        .copy()
        .sort_values(
            "Gross_Profit",
            ascending=True
        )
    )

    fig_division_profit = px.bar(
        division_chart,
        x="Gross_Profit",
        y="Division",
        orientation="h",
        title="Gross Profit by Division",
        labels={
            "Gross_Profit": "Gross Profit ($)",
            "Division": "Division"
        },
        hover_data={
            "Sales": ":,.2f",
            "Gross_Profit": ":,.2f",
            "Units": ":,.0f",
            "Gross Margin %": ":.2f"
        }
    )

    fig_division_profit.update_layout(
        height=420,
        hovermode="closest",
        margin=dict(
            l=20,
            r=20,
            t=70,
            b=20
        ),
        xaxis_title="Gross Profit ($)",
        yaxis_title="Division"
    )

    fig_division_profit.update_traces(
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Gross Profit: $%{x:,.2f}"
            "<extra></extra>"
        )
    )

    st.plotly_chart(
        fig_division_profit,
        width="stretch"
    )


# ============================================================
# DIVISION PERFORMANCE TABLE
# ============================================================

st.subheader("📋 Division Performance")

display_division_summary = division_summary.copy()

display_division_summary["Sales"] = (
    display_division_summary["Sales"]
    .map(lambda x: f"${x:,.2f}")
)

display_division_summary["Gross_Profit"] = (
    display_division_summary["Gross_Profit"]
    .map(lambda x: f"${x:,.2f}")
)

display_division_summary["Gross Margin %"] = (
    display_division_summary["Gross Margin %"]
    .map(lambda x: f"{x:.2f}%")
)

display_division_summary["Units"] = (
    display_division_summary["Units"]
    .map(lambda x: f"{x:,.0f}")
)


display_division_summary = display_division_summary.rename(
    columns={
        "Division": "Division",
        "Sales": "Sales",
        "Gross_Profit": "Gross Profit",
        "Units": "Units Sold",
        "Gross Margin %": "Gross Margin"
    }
)


st.dataframe(
    display_division_summary,
    width="stretch",
    hide_index=True
)
# ============================================================
# TREND ANALYSIS
# ============================================================

st.divider()

st.header("📈 Trend Analysis")

st.write(
    "Analyze monthly sales, gross profit, units sold, and "
    "gross margin to identify business trends and patterns."
)


# ============================================================
# CREATE MONTHLY TREND DATA
# ============================================================

monthly_trend = (
    filtered_df
    .copy()
)

monthly_trend["Month"] = (
    monthly_trend["Order Date"]
    .dt.to_period("M")
    .dt.to_timestamp()
)


monthly_trend = (
    monthly_trend
    .groupby("Month", as_index=False)
    .agg(
        Sales=("Sales", "sum"),
        Gross_Profit=("Gross Profit", "sum"),
        Units=("Units", "sum")
    )
)


# ============================================================
# CALCULATE MONTHLY GROSS MARGIN
# ============================================================

monthly_trend["Gross Margin %"] = (
    monthly_trend["Gross_Profit"]
    / monthly_trend["Sales"]
    * 100
)


# ============================================================
# SORT BY MONTH
# ============================================================

monthly_trend = monthly_trend.sort_values(
    "Month"
)


# ============================================================
# MONTHLY SALES TREND
# ============================================================

# ============================================================
# INTERACTIVE MONTHLY SALES TREND
# ============================================================

st.subheader("💰 Monthly Sales Trend")

fig_monthly_sales = px.line(
    monthly_trend,
    x="Month",
    y="Sales",
    markers=True,
    title="Monthly Sales Trend",
    labels={
        "Month": "Month",
        "Sales": "Sales"
    },
    hover_data={
        "Sales": ":,.2f"
    }
)

fig_monthly_sales.update_layout(
    height=450,
    hovermode="x unified",
    margin=dict(
        l=20,
        r=20,
        t=70,
        b=20
    ),
    xaxis_title="Month",
    yaxis_title="Sales"
)

fig_monthly_sales.update_traces(
    line=dict(width=3),
    marker=dict(size=7)
)

st.plotly_chart(
    fig_monthly_sales,
    width="stretch"
)


# ============================================================
# MONTHLY GROSS PROFIT TREND
# ============================================================

# ============================================================
# INTERACTIVE MONTHLY GROSS PROFIT TREND
# ============================================================

st.subheader("📈 Monthly Gross Profit Trend")

fig_monthly_profit = px.line(
    monthly_trend,
    x="Month",
    y="Gross_Profit",
    markers=True,
    title="Monthly Gross Profit Trend",
    labels={
        "Month": "Month",
        "Gross_Profit": "Gross Profit"
    },
    hover_data={
        "Gross_Profit": ":,.2f"
    }
)

fig_monthly_profit.update_layout(
    height=450,
    hovermode="x unified",
    margin=dict(
        l=20,
        r=20,
        t=70,
        b=20
    ),
    xaxis_title="Month",
    yaxis_title="Gross Profit"
)

fig_monthly_profit.update_traces(
    line=dict(width=3),
    marker=dict(size=7)
)

st.plotly_chart(
    fig_monthly_profit,
    width="stretch"
)


# ============================================================
# MONTHLY UNITS TREND
# ============================================================

# ============================================================
# INTERACTIVE MONTHLY UNITS TREND
# ============================================================

st.subheader("📦 Monthly Units Sold Trend")

fig_monthly_units = px.line(
    monthly_trend,
    x="Month",
    y="Units",
    markers=True,
    title="Monthly Units Sold Trend",
    labels={
        "Month": "Month",
        "Units": "Units Sold"
    },
    hover_data={
        "Units": ":,.0f"
    }
)

fig_monthly_units.update_layout(
    height=450,
    hovermode="x unified",
    margin=dict(
        l=20,
        r=20,
        t=70,
        b=20
    ),
    xaxis_title="Month",
    yaxis_title="Units Sold"
)

fig_monthly_units.update_traces(
    line=dict(width=3),
    marker=dict(size=7)
)

st.plotly_chart(
    fig_monthly_units,
    width="stretch"
)

# ============================================================
# MONTHLY GROSS MARGIN TREND
# ============================================================

# ============================================================
# INTERACTIVE MONTHLY GROSS MARGIN TREND
# ============================================================

st.subheader("🎯 Monthly Gross Margin Trend")

fig_monthly_margin = px.line(
    monthly_trend,
    x="Month",
    y="Gross Margin %",
    markers=True,
    title="Monthly Gross Margin Trend",
    labels={
        "Month": "Month",
        "Gross Margin %": "Gross Margin (%)"
    },
    hover_data={
        "Gross Margin %": ":.2f"
    }
)

fig_monthly_margin.update_layout(
    height=450,
    hovermode="x unified",
    margin=dict(
        l=20,
        r=20,
        t=70,
        b=20
    ),
    xaxis_title="Month",
    yaxis_title="Gross Margin (%)"
)

fig_monthly_margin.update_traces(
    line=dict(width=3),
    marker=dict(size=7)
)

st.plotly_chart(
    fig_monthly_margin,
    width="stretch"
)

# ============================================================
# MONTHLY TREND TABLE
# ============================================================

st.subheader("📋 Monthly Trend Summary")

display_monthly_trend = monthly_trend.copy()

display_monthly_trend["Month"] = (
    display_monthly_trend["Month"]
    .dt.strftime("%B %Y")
)

display_monthly_trend["Sales"] = (
    display_monthly_trend["Sales"]
    .map(lambda x: f"${x:,.2f}")
)

display_monthly_trend["Gross_Profit"] = (
    display_monthly_trend["Gross_Profit"]
    .map(lambda x: f"${x:,.2f}")
)

display_monthly_trend["Units"] = (
    display_monthly_trend["Units"]
    .map(lambda x: f"{x:,.0f}")
)

display_monthly_trend["Gross Margin %"] = (
    display_monthly_trend["Gross Margin %"]
    .map(lambda x: f"{x:.2f}%")
)


display_monthly_trend = display_monthly_trend.rename(
    columns={
        "Month": "Month",
        "Sales": "Sales",
        "Gross_Profit": "Gross Profit",
        "Units": "Units Sold",
        "Gross Margin %": "Gross Margin"
    }
)


st.dataframe(
    display_monthly_trend,
    width="stretch",
    hide_index=True
)
# ============================================================
# SALES VS GROSS PROFIT ANALYSIS
# ============================================================

st.divider()

st.header("📊 Sales vs Gross Profit Analysis")

st.write(
    "Compare product sales and gross profit to identify "
    "products that generate strong revenue and profitability."
)


# ============================================================
# PRODUCT SALES & PROFIT SUMMARY
# ============================================================

sales_profit_summary = (
    filtered_df
    .groupby("Product Name", as_index=False)
    .agg(
        Sales=("Sales", "sum"),
        Gross_Profit=("Gross Profit", "sum"),
        Units=("Units", "sum")
    )
)


# ============================================================
# CALCULATE GROSS MARGIN
# ============================================================

sales_profit_summary["Gross Margin %"] = (
    sales_profit_summary["Gross_Profit"]
    / sales_profit_summary["Sales"]
    * 100
)


# ============================================================
# SORT BY SALES
# ============================================================

sales_profit_summary = (
    sales_profit_summary
    .sort_values(
        "Sales",
        ascending=False
    )
)


# ============================================================
# TOP PRODUCTS BY SALES
# ============================================================

# ============================================================
# INTERACTIVE SALES VS GROSS PROFIT CHART
# ============================================================

# ============================================================
# INTERACTIVE SALES VS GROSS PROFIT CHART
# ============================================================

st.subheader("💰 Top Products by Sales")

top_sales_products = (
    sales_profit_summary
    .head(10)
    .copy()
)

# Convert Sales and Gross Profit into a format
# that Plotly can display correctly
sales_profit_long = top_sales_products[
    [
        "Product Name",
        "Sales",
        "Gross_Profit"
    ]
].melt(
    id_vars="Product Name",
    value_vars=["Sales", "Gross_Profit"],
    var_name="Metric",
    value_name="Amount"
)

# Make the metric names easier to understand
sales_profit_long["Metric"] = sales_profit_long["Metric"].replace(
    {
        "Sales": "Sales",
        "Gross_Profit": "Gross Profit"
    }
)

# Sort products so the highest-sales product appears at the top
product_order = (
    top_sales_products
    .sort_values("Sales", ascending=True)["Product Name"]
    .tolist()
)

fig_sales_profit = px.bar(
    sales_profit_long,
    x="Amount",
    y="Product Name",
    color="Metric",
    orientation="h",
    barmode="group",
    category_orders={
        "Product Name": product_order,
        "Metric": ["Sales", "Gross Profit"]
    },
    title="Top Products — Sales vs Gross Profit",
    labels={
        "Amount": "Amount ($)",
        "Product Name": "Product",
        "Metric": "Metric"
    },
    hover_data={
        "Amount": ":,.2f"
    }
)

fig_sales_profit.update_layout(
    height=520,
    hovermode="closest",
    margin=dict(
        l=20,
        r=20,
        t=70,
        b=20
    ),
    xaxis_title="Amount ($)",
    yaxis_title="Product",
    legend_title="Metric"
)

fig_sales_profit.update_traces(
    hovertemplate=(
        "<b>%{y}</b><br>"
        "%{fullData.name}: $%{x:,.2f}"
        "<extra></extra>"
    )
)

st.plotly_chart(
    fig_sales_profit,
    width="stretch"
)

# ============================================================
# SALES VS PROFIT TABLE
# ============================================================

st.subheader("📋 Sales & Profitability Comparison")

display_sales_profit = (
    sales_profit_summary
    .head(20)
    .copy()
)


display_sales_profit["Sales"] = (
    display_sales_profit["Sales"]
    .map(lambda x: f"${x:,.2f}")
)


display_sales_profit["Gross_Profit"] = (
    display_sales_profit["Gross_Profit"]
    .map(lambda x: f"${x:,.2f}")
)


display_sales_profit["Units"] = (
    display_sales_profit["Units"]
    .map(lambda x: f"{x:,.0f}")
)


display_sales_profit["Gross Margin %"] = (
    display_sales_profit["Gross Margin %"]
    .map(lambda x: f"{x:.2f}%")
)


display_sales_profit = (
    display_sales_profit
    .rename(
        columns={
            "Product Name": "Product",
            "Sales": "Sales",
            "Gross_Profit": "Gross Profit",
            "Units": "Units Sold",
            "Gross Margin %": "Gross Margin"
        }
    )
)


st.dataframe(
    display_sales_profit,
    width="stretch",
    hide_index=True
)
# ============================================================
# PROFIT MARGIN ANALYSIS
# ============================================================

st.divider()

st.header("🎯 Profit Margin Analysis")

st.write(
    "Analyze gross margin performance to identify products "
    "with strong and weak profitability."
)


# ============================================================
# PRODUCT MARGIN SUMMARY
# ============================================================

margin_summary = (
    filtered_df
    .groupby("Product Name", as_index=False)
    .agg(
        Sales=("Sales", "sum"),
        Gross_Profit=("Gross Profit", "sum"),
        Units=("Units", "sum")
    )
)


# ============================================================
# CALCULATE GROSS MARGIN
# ============================================================

margin_summary["Gross Margin %"] = (
    margin_summary["Gross_Profit"]
    / margin_summary["Sales"]
    * 100
)


# Remove invalid margin values

margin_summary = margin_summary[
    margin_summary["Sales"] > 0
]


# ============================================================
# MARGIN KPI
# ============================================================

overall_margin = 0

if filtered_df["Sales"].sum() > 0:

    overall_margin = (
        filtered_df["Gross Profit"].sum()
        / filtered_df["Sales"].sum()
        * 100
    )


margin_col1, margin_col2, margin_col3 = st.columns(3)


with margin_col1:

    st.metric(
        "🎯 Overall Gross Margin",
        f"{overall_margin:.2f}%"
    )


with margin_col2:

    st.metric(
        "📈 Highest Product Margin",
        f"{margin_summary['Gross Margin %'].max():.2f}%"
    )


with margin_col3:

    st.metric(
        "📉 Lowest Product Margin",
        f"{margin_summary['Gross Margin %'].min():.2f}%"
    )


# ============================================================
# HIGHEST MARGIN PRODUCTS
# ============================================================

st.subheader("🏆 Highest Margin Products")

highest_margin = (
    margin_summary
    .sort_values(
        "Gross Margin %",
        ascending=False
    )
    .head(10)
)


highest_margin_chart = (
    highest_margin
    .sort_values("Gross Margin %", ascending=True)
    .copy()
)

fig_highest_margin = px.bar(
    highest_margin_chart,
    x="Gross Margin %",
    y="Product Name",
    orientation="h",
    title="Top 10 Products by Gross Margin",
    labels={
        "Gross Margin %": "Gross Margin (%)",
        "Product Name": "Product"
    },
    hover_data={
        "Gross Margin %": ":.2f",
        "Sales": ":,.2f",
        "Gross_Profit": ":,.2f",
        "Units": ":,.0f"
    }
)

fig_highest_margin.update_layout(
    height=500,
    hovermode="closest",
    margin=dict(
        l=20,
        r=20,
        t=70,
        b=20
    ),
    xaxis_title="Gross Margin (%)",
    yaxis_title="Product"
)

fig_highest_margin.update_traces(
    hovertemplate=(
        "<b>%{y}</b><br>"
        "Gross Margin: %{x:.2f}%"
        "<extra></extra>"
    )
)

st.plotly_chart(
    fig_highest_margin,
    width="stretch"
)


# ============================================================
# LOWEST MARGIN PRODUCTS
# ============================================================

st.subheader("⚠️ Lowest Margin Products")

lowest_margin = (
    margin_summary
    .sort_values(
        "Gross Margin %",
        ascending=True
    )
    .head(10)
)


# ============================================================
# INTERACTIVE LOWEST MARGIN PRODUCTS
# ============================================================

lowest_margin_chart = (
    lowest_margin
    .sort_values("Gross Margin %", ascending=False)
    .copy()
)

fig_lowest_margin = px.bar(
    lowest_margin_chart,
    x="Gross Margin %",
    y="Product Name",
    orientation="h",
    title="Bottom 10 Products by Gross Margin",
    labels={
        "Gross Margin %": "Gross Margin (%)",
        "Product Name": "Product"
    },
    hover_data={
        "Gross Margin %": ":.2f",
        "Sales": ":,.2f",
        "Gross_Profit": ":,.2f",
        "Units": ":,.0f"
    }
)

fig_lowest_margin.update_layout(
    height=500,
    hovermode="closest",
    margin=dict(
        l=20,
        r=20,
        t=70,
        b=20
    ),
    xaxis_title="Gross Margin (%)",
    yaxis_title="Product"
)

fig_lowest_margin.update_traces(
    hovertemplate=(
        "<b>%{y}</b><br>"
        "Gross Margin: %{x:.2f}%"
        "<extra></extra>"
    )
)

st.plotly_chart(
    fig_lowest_margin,
    width="stretch"
)


# ============================================================
# MARGIN PERFORMANCE TABLE
# ============================================================

st.subheader("📋 Margin Performance")

display_margin = (
    margin_summary
    .sort_values(
        "Gross Margin %",
        ascending=False
    )
    .copy()
)


display_margin["Sales"] = (
    display_margin["Sales"]
    .map(lambda x: f"${x:,.2f}")
)


display_margin["Gross_Profit"] = (
    display_margin["Gross_Profit"]
    .map(lambda x: f"${x:,.2f}")
)


display_margin["Units"] = (
    display_margin["Units"]
    .map(lambda x: f"{x:,.0f}")
)


display_margin["Gross Margin %"] = (
    display_margin["Gross Margin %"]
    .map(lambda x: f"{x:.2f}%")
)


display_margin = (
    display_margin
    .rename(
        columns={
            "Product Name": "Product",
            "Sales": "Sales",
            "Gross_Profit": "Gross Profit",
            "Units": "Units Sold",
            "Gross Margin %": "Gross Margin"
        }
    )
)


st.dataframe(
    display_margin,
    width="stretch",
    hide_index=True
)
# ============================================================
# MARGIN RISK ANALYSIS
# ============================================================

st.divider()

st.header("🚨 Margin Risk Analysis")

st.write(
    "Identify products whose gross margin falls below the selected "
    "risk threshold and prioritize them for pricing or cost review."
)


# ============================================================
# CREATE MARGIN RISK DATASET
# ============================================================

risk_products = margin_summary.copy()

risk_products["Cost"] = (
    risk_products["Sales"]
    - risk_products["Gross_Profit"]
)

risk_products["Profit per Unit"] = (
    risk_products["Gross_Profit"]
    / risk_products["Units"].replace(0, pd.NA)
).fillna(0)

risk_products = risk_products[
    risk_products["Gross Margin %"] < margin_threshold
].copy()


# ============================================================
# RISK CLASSIFICATION
# ============================================================

def classify_margin_risk(margin):

    if margin <= margin_threshold * 0.50:
        return "🔴 High Risk"

    if margin <= margin_threshold * 0.75:
        return "🟠 Medium Risk"

    return "🟡 Low Risk"


def recommended_action(margin):

    if margin <= margin_threshold * 0.50:
        return "Discontinuation Review"

    if margin <= margin_threshold * 0.75:
        return "Cost Renegotiation"

    return "Repricing Review"


if not risk_products.empty:

    risk_products["Risk Level"] = (
        risk_products["Gross Margin %"]
        .apply(classify_margin_risk)
    )

    risk_products["Suggested Action"] = (
        risk_products["Gross Margin %"]
        .apply(recommended_action)
    )


# ============================================================
# MARGIN RISK KPIs
# ============================================================

risk_col1, risk_col2, risk_col3 = st.columns(3)

with risk_col1:

    st.metric(
        "🚨 Products at Margin Risk",
        f"{len(risk_products):,}"
    )

with risk_col2:

    risk_sales = risk_products["Sales"].sum() if not risk_products.empty else 0

    st.metric(
        "💰 Sales Exposed to Risk",
        f"${risk_sales:,.2f}"
    )

with risk_col3:

    if not risk_products.empty:
        average_risk_margin = risk_products["Gross Margin %"].mean()
    else:
        average_risk_margin = 0

    st.metric(
        "📉 Average Risk Margin",
        f"{average_risk_margin:.2f}%"
    )


# ============================================================
# MARGIN RISK CHART
# ============================================================

if not risk_products.empty:

    risk_chart = (
        risk_products
        .sort_values("Gross Margin %", ascending=True)
        .head(15)
        .copy()
    )

    fig_risk = px.bar(
        risk_chart,
        x="Gross Margin %",
        y="Product Name",
        orientation="h",
        title=f"Products Below {margin_threshold}% Gross Margin",
        labels={
            "Gross Margin %": "Gross Margin (%)",
            "Product Name": "Product"
        },
        hover_data={
            "Gross Margin %": ":.2f",
            "Sales": ":,.2f",
            "Cost": ":,.2f",
            "Gross_Profit": ":,.2f",
            "Units": ":,.0f"
        }
    )

    fig_risk.add_vline(
        x=margin_threshold,
        line_dash="dash",
        annotation_text=f"Risk Threshold: {margin_threshold}%",
        annotation_position="top right"
    )

    fig_risk.update_layout(
        height=520,
        hovermode="closest",
        margin=dict(
            l=20,
            r=20,
            t=80,
            b=20
        ),
        xaxis_title="Gross Margin (%)",
        yaxis_title="Product"
    )

    fig_risk.update_traces(
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Gross Margin: %{x:.2f}%<br>"
            "<extra></extra>"
        )
    )

    st.plotly_chart(
        fig_risk,
        width="stretch"
    )


# ============================================================
# MARGIN RISK TABLE
# ============================================================

st.subheader("📋 Margin Risk Products")

if risk_products.empty:

    st.success(
        f"✅ No products fall below the {margin_threshold}% gross margin threshold."
    )

else:

    display_risk = (
        risk_products
        .sort_values("Gross Margin %", ascending=True)
        [[
            "Product Name",
            "Sales",
            "Cost",
            "Gross_Profit",
            "Units",
            "Profit per Unit",
            "Gross Margin %",
            "Risk Level",
            "Suggested Action"
        ]]
        .copy()
    )

    display_risk["Sales"] = display_risk["Sales"].map(
        lambda x: f"${x:,.2f}"
    )

    display_risk["Cost"] = display_risk["Cost"].map(
        lambda x: f"${x:,.2f}"
    )

    display_risk["Gross_Profit"] = display_risk["Gross_Profit"].map(
        lambda x: f"${x:,.2f}"
    )

    display_risk["Units"] = display_risk["Units"].map(
        lambda x: f"{x:,.0f}"
    )

    display_risk["Profit per Unit"] = display_risk["Profit per Unit"].map(
        lambda x: f"${x:,.2f}"
    )

    display_risk["Gross Margin %"] = display_risk["Gross Margin %"].map(
        lambda x: f"{x:.2f}%"
    )

    display_risk = display_risk.rename(
        columns={
            "Product Name": "Product",
            "Gross_Profit": "Gross Profit",
            "Units": "Units Sold",
            "Gross Margin %": "Gross Margin"
        }
    )

    st.dataframe(
        display_risk,
        width="stretch",
        hide_index=True
    )
# ============================================================
# COST VS SALES DIAGNOSTICS
# ============================================================

st.divider()

st.header("💰 Cost vs Sales Diagnostics")

st.write(
    "Analyze the relationship between product sales and manufacturing "
    "cost to identify cost-heavy and margin-poor products."
)

# ============================================================
# PRODUCT-LEVEL COST & SALES SUMMARY
# ============================================================

cost_sales_summary = (
    filtered_df
    .groupby("Product Name", as_index=False)
    .agg(
        Sales=("Sales", "sum"),
        Cost=("Cost", "sum"),
        Gross_Profit=("Gross Profit", "sum"),
        Units=("Units", "sum")
    )
)

# ============================================================
# CALCULATE GROSS MARGIN
# ============================================================

cost_sales_summary["Gross Margin %"] = (
    cost_sales_summary["Gross_Profit"]
    / cost_sales_summary["Sales"]
    * 100
)

# Avoid invalid values
cost_sales_summary = cost_sales_summary.replace(
    [np.inf, -np.inf],
    np.nan
).dropna(
    subset=["Sales", "Cost", "Gross Margin %"]
)

# ============================================================
# COST VS SALES SCATTER PLOT
# ============================================================

fig_cost_sales = px.scatter(
    cost_sales_summary,
    x="Sales",
    y="Cost",
    size="Gross_Profit",
    color="Gross Margin %",
    hover_name="Product Name",
    hover_data={
        "Sales": ":,.2f",
        "Cost": ":,.2f",
        "Gross_Profit": ":,.2f",
        "Gross Margin %": ":.2f",
        "Units": ":,.0f"
    },
    title="Cost vs Sales by Product",
    labels={
        "Sales": "Sales ($)",
        "Cost": "Manufacturing Cost ($)",
        "Gross Margin %": "Gross Margin (%)",
        "Gross_Profit": "Gross Profit"
    }
)

fig_cost_sales.update_layout(
    height=600,
    hovermode="closest",
    margin=dict(
        l=20,
        r=20,
        t=70,
        b=20
    ),
    xaxis_title="Sales ($)",
    yaxis_title="Cost ($)"
)

fig_cost_sales.update_traces(
    marker=dict(
        opacity=0.80
    )
)

st.plotly_chart(
    fig_cost_sales,
    width="stretch"
)

# ============================================================
# COST-HEAVY / MARGIN-POOR PRODUCTS
# ============================================================

st.subheader("⚠️ Cost-Heavy & Margin-Poor Products")

cost_heavy_products = cost_sales_summary[
    cost_sales_summary["Gross Margin %"] < margin_threshold
].copy()

cost_heavy_products["Risk Reason"] = np.where(
    cost_heavy_products["Cost"] > cost_heavy_products["Sales"] * 0.70,
    "High cost and low margin",
    "Low margin"
)

cost_heavy_products = cost_heavy_products.sort_values(
    "Gross Margin %",
    ascending=True
)

if cost_heavy_products.empty:

    st.success(
        f"✅ No products are below the selected "
        f"{margin_threshold:.0f}% margin threshold."
    )

else:

    st.warning(
        f"⚠️ {len(cost_heavy_products)} product(s) "
        f"are below the selected {margin_threshold:.0f}% "
        f"gross-margin threshold."
    )

    display_cost_risk = cost_heavy_products[
        [
            "Product Name",
            "Sales",
            "Cost",
            "Gross_Profit",
            "Gross Margin %",
            "Risk Reason"
        ]
    ].copy()

    display_cost_risk["Sales"] = (
        display_cost_risk["Sales"]
        .map(lambda x: f"${x:,.2f}")
    )

    display_cost_risk["Cost"] = (
        display_cost_risk["Cost"]
        .map(lambda x: f"${x:,.2f}")
    )

    display_cost_risk["Gross_Profit"] = (
        display_cost_risk["Gross_Profit"]
        .map(lambda x: f"${x:,.2f}")
    )

    display_cost_risk["Gross Margin %"] = (
        display_cost_risk["Gross Margin %"]
        .map(lambda x: f"{x:.2f}%")
    )

    display_cost_risk = display_cost_risk.rename(
        columns={
            "Product Name": "Product",
            "Sales": "Sales",
            "Cost": "Cost",
            "Gross_Profit": "Gross Profit",
            "Gross Margin %": "Gross Margin",
            "Risk Reason": "Risk Reason"
        }
    )

    st.dataframe(
        display_cost_risk,
        width="stretch",
        hide_index=True
    )

# ============================================================
# COST STRUCTURE SUMMARY
# ============================================================

st.subheader("📊 Cost Structure Summary")

col1, col2, col3 = st.columns(3)

with col1:
    highest_cost_product = cost_sales_summary.loc[
        cost_sales_summary["Cost"].idxmax()
    ]

    st.metric(
        "Highest Cost Product",
        highest_cost_product["Product Name"]
    )

with col2:
    average_cost_ratio = (
        cost_sales_summary["Cost"]
        / cost_sales_summary["Sales"]
        * 100
    ).mean()

    st.metric(
        "Average Cost-to-Sales",
        f"{average_cost_ratio:.2f}%"
    )

with col3:
    risk_count = len(cost_heavy_products)

    st.metric(
        "Margin-Risk Products",
        risk_count
    )

# ============================================================
# PARETO ANALYSIS
# ============================================================

st.divider()

st.header("📊 Pareto Analysis")

st.write(
    "Identify the products that contribute most to total gross "
    "profit using the 80/20 Pareto principle."
)


# ============================================================
# PRODUCT PROFIT SUMMARY
# ============================================================

pareto_df = (
    filtered_df
    .groupby("Product Name", as_index=False)
    .agg(
        Gross_Profit=("Gross Profit", "sum")
    )
)


# ============================================================
# SORT BY GROSS PROFIT
# ============================================================

pareto_df = pareto_df.sort_values(
    "Gross_Profit",
    ascending=False
).reset_index(drop=True)


# ============================================================
# TOTAL PROFIT
# ============================================================

total_pareto_profit = (
    pareto_df["Gross_Profit"].sum()
)


# ============================================================
# PROFIT CONTRIBUTION %
# ============================================================

if total_pareto_profit != 0:

    pareto_df["Profit Contribution %"] = (
        pareto_df["Gross_Profit"]
        / total_pareto_profit
        * 100
    )

else:

    pareto_df["Profit Contribution %"] = 0


# ============================================================
# CUMULATIVE PROFIT %
# ============================================================

pareto_df["Cumulative Profit %"] = (
    pareto_df["Profit Contribution %"]
    .cumsum()
)


# ============================================================
# IDENTIFY PRODUCTS WITHIN 80%
# ============================================================

products_80 = (
    pareto_df[
        pareto_df["Cumulative Profit %"] <= 80
    ]
)


# Include the first product that crosses 80%

crossing_80 = pareto_df[
    pareto_df["Cumulative Profit %"] > 80
]

if not crossing_80.empty:

    first_crossing = crossing_80.iloc[[0]]

    products_80 = pd.concat(
        [
            products_80,
            first_crossing
        ]
    )


products_80_count = (
    products_80["Product Name"].nunique()
)


total_products = (
    pareto_df["Product Name"].nunique()
)


# ============================================================
# PARETO KPI CARDS
# ============================================================

pareto_col1, pareto_col2, pareto_col3 = st.columns(3)


with pareto_col1:

    st.metric(
        "🍫 Total Products",
        f"{total_products:,}"
    )


with pareto_col2:

    st.metric(
        "🎯 Products Driving 80% Profit",
        f"{products_80_count:,}"
    )


with pareto_col3:

    if total_products > 0:

        percentage_products = (
            products_80_count
            / total_products
            * 100
        )

    else:

        percentage_products = 0

    st.metric(
        "📊 Share of Products",
        f"{percentage_products:.2f}%"
    )


# ============================================================
# TOP PROFIT PRODUCTS
# ============================================================

st.subheader("🏆 Top Products by Gross Profit")

top_pareto = (
    pareto_df.head(15)
    .copy()
    .sort_values("Gross_Profit", ascending=True)
)

fig_top_products = px.bar(
    top_pareto,
    x="Gross_Profit",
    y="Product Name",
    orientation="h",
    title="Top Products by Gross Profit",
    labels={
        "Gross_Profit": "Gross Profit",
        "Product Name": "Product"
    },
    hover_data={
        "Gross_Profit": ":,.2f",
        "Profit Contribution %": ":.2f",
        "Cumulative Profit %": ":.2f"
    }
)

fig_top_products.update_layout(
    height=520,
    hovermode="closest",
    margin=dict(l=20, r=20, t=70, b=20),
    xaxis_title="Gross Profit",
    yaxis_title="Product"
)

st.plotly_chart(
    fig_top_products,
    width="stretch"
)


# ============================================================
# PARETO TABLE
# ============================================================

st.subheader("📋 Pareto Contribution")


display_pareto = pareto_df.copy()


display_pareto["Gross_Profit"] = (
    display_pareto["Gross_Profit"]
    .map(lambda x: f"${x:,.2f}")
)


display_pareto["Profit Contribution %"] = (
    display_pareto["Profit Contribution %"]
    .map(lambda x: f"{x:.2f}%")
)


display_pareto["Cumulative Profit %"] = (
    display_pareto["Cumulative Profit %"]
    .map(lambda x: f"{x:.2f}%")
)


display_pareto = (
    display_pareto
    .rename(
        columns={
            "Product Name": "Product",
            "Gross_Profit": "Gross Profit",
            "Profit Contribution %": "Profit Contribution",
            "Cumulative Profit %": "Cumulative Profit"
        }
    )
)


st.dataframe(
    display_pareto,
    width="stretch",
    hide_index=True
)
# ============================================================
# EXECUTIVE SUMMARY & BUSINESS INSIGHTS
# ============================================================

st.divider()

st.header("💡 Executive Summary & Business Insights")

st.write(
    "Key business insights generated automatically from the "
    "currently selected filters."
)


# ============================================================
# PRODUCT INSIGHTS
# ============================================================

insight_product_summary = (
    filtered_df
    .groupby("Product Name", as_index=False)
    .agg(
        Sales=("Sales", "sum"),
        Gross_Profit=("Gross Profit", "sum")
    )
)


insight_product_summary["Gross Margin %"] = (
    insight_product_summary["Gross_Profit"]
    / insight_product_summary["Sales"]
    * 100
)


# ============================================================
# TOP PRODUCT BY SALES
# ============================================================

top_sales_product = (
    insight_product_summary
    .sort_values(
        "Sales",
        ascending=False
    )
    .iloc[0]
)


# ============================================================
# TOP PRODUCT BY GROSS PROFIT
# ============================================================

top_profit_product = (
    insight_product_summary
    .sort_values(
        "Gross_Profit",
        ascending=False
    )
    .iloc[0]
)


# ============================================================
# HIGHEST MARGIN PRODUCT
# ============================================================

highest_margin_product = (
    insight_product_summary
    .sort_values(
        "Gross Margin %",
        ascending=False
    )
    .iloc[0]
)


# ============================================================
# DIVISION INSIGHTS
# ============================================================

insight_division_summary = (
    filtered_df
    .groupby("Division", as_index=False)
    .agg(
        Sales=("Sales", "sum"),
        Gross_Profit=("Gross Profit", "sum")
    )
)


# ============================================================
# TOP DIVISION BY SALES
# ============================================================

top_division = (
    insight_division_summary
    .sort_values(
        "Sales",
        ascending=False
    )
    .iloc[0]
)


# ============================================================
# MONTHLY INSIGHTS
# ============================================================

insight_monthly = (
    filtered_df
    .copy()
)


insight_monthly["Month"] = (
    insight_monthly["Order Date"]
    .dt.to_period("M")
    .dt.to_timestamp()
)


insight_monthly = (
    insight_monthly
    .groupby("Month", as_index=False)
    .agg(
        Sales=("Sales", "sum"),
        Gross_Profit=("Gross Profit", "sum")
    )
)


# ============================================================
# BEST SALES MONTH
# ============================================================

best_month = (
    insight_monthly
    .sort_values(
        "Sales",
        ascending=False
    )
    .iloc[0]
)


# ============================================================
# LOWEST SALES MONTH
# ============================================================

lowest_month = (
    insight_monthly
    .sort_values(
        "Sales",
        ascending=True
    )
    .iloc[0]
)


# ============================================================
# EXECUTIVE KPI CARDS
# ============================================================

insight_col1, insight_col2, insight_col3, insight_col4 = (
    st.columns(4)
)


with insight_col1:

    st.metric(
        "🏆 Top Product by Sales",
        top_sales_product["Product Name"]
    )


with insight_col2:

    st.metric(
        "💰 Top Product by Profit",
        top_profit_product["Product Name"]
    )


with insight_col3:

    st.metric(
        "🎯 Highest Margin Product",
        highest_margin_product["Product Name"]
    )


with insight_col4:

    st.metric(
        "🏢 Top Division",
        top_division["Division"]
    )


# ============================================================
# BUSINESS INSIGHTS
# ============================================================

st.subheader("🔎 Key Business Insights")


st.info(
    f"💰 **Sales Leader:** "
    f"{top_sales_product['Product Name']} generated "
    f"${top_sales_product['Sales']:,.2f} in sales."
)


st.success(
    f"🏆 **Profit Leader:** "
    f"{top_profit_product['Product Name']} generated "
    f"${top_profit_product['Gross_Profit']:,.2f} "
    f"in gross profit."
)


st.warning(
    f"🎯 **Margin Leader:** "
    f"{highest_margin_product['Product Name']} achieved "
    f"{highest_margin_product['Gross Margin %']:.2f}% "
    f"gross margin."
)


st.info(
    f"🏢 **Division Leader:** "
    f"{top_division['Division']} generated "
    f"${top_division['Sales']:,.2f} in sales."
)


st.success(
    f"📈 **Best Sales Month:** "
    f"{best_month['Month'].strftime('%B %Y')} recorded "
    f"${best_month['Sales']:,.2f} in sales."
)


st.warning(
    f"📉 **Lowest Sales Month:** "
    f"{lowest_month['Month'].strftime('%B %Y')} recorded "
    f"${lowest_month['Sales']:,.2f} in sales."
)


# ============================================================
# INSIGHT SUMMARY TABLE
# ============================================================

st.subheader("📋 Business Insight Summary")


insight_table = pd.DataFrame(
    {
        "Metric": [
            "Top Product by Sales",
            "Top Product by Gross Profit",
            "Highest Margin Product",
            "Top Division",
            "Best Sales Month",
            "Lowest Sales Month"
        ],

        "Result": [
            top_sales_product["Product Name"],
            top_profit_product["Product Name"],
            highest_margin_product["Product Name"],
            top_division["Division"],
            best_month["Month"].strftime("%B %Y"),
            lowest_month["Month"].strftime("%B %Y")
        ]
    }
)


st.dataframe(
    insight_table,
    width="stretch",
    hide_index=True
)
# ============================================================
# CUSTOMER & ORDER ANALYSIS
# ============================================================

st.divider()

st.header("👥 Customer & Order Analysis")

st.write(
    "Analyze customer sales, profitability, order activity, "
    "and customer-level performance."
)


# ============================================================
# CUSTOMER SUMMARY
# ============================================================

customer_summary = (
    filtered_df
    .groupby("Customer ID", as_index=False)
    .agg(
        Sales=("Sales", "sum"),
        Gross_Profit=("Gross Profit", "sum"),
        Units=("Units", "sum"),
        Orders=("Order ID", "nunique"),
        Products=("Product ID", "nunique")
    )
)


# ============================================================
# CUSTOMER GROSS MARGIN
# ============================================================

customer_summary["Gross Margin %"] = (
    customer_summary["Gross_Profit"]
    / customer_summary["Sales"]
    * 100
)

customer_summary = customer_summary[
    customer_summary["Sales"] > 0
]


# ============================================================
# CUSTOMER KPI CARDS
# ============================================================

customer_col1, customer_col2, customer_col3, customer_col4 = (
    st.columns(4)
)

with customer_col1:
    st.metric(
        "👥 Total Customers",
        f"{customer_summary['Customer ID'].nunique():,}"
    )

with customer_col2:
    st.metric(
        "📦 Total Orders",
        f"{filtered_df['Order ID'].nunique():,}"
    )

with customer_col3:
    if not customer_summary.empty:
        avg_customer_sales = customer_summary["Sales"].mean()
    else:
        avg_customer_sales = 0

    st.metric(
        "💰 Avg Sales / Customer",
        f"${avg_customer_sales:,.2f}"
    )

with customer_col4:
    if not customer_summary.empty:
        avg_customer_profit = customer_summary["Gross_Profit"].mean()
    else:
        avg_customer_profit = 0

    st.metric(
        "📈 Avg Profit / Customer",
        f"${avg_customer_profit:,.2f}"
    )


# ============================================================
# TOP CUSTOMERS BY SALES
# ============================================================

st.subheader("🏆 Top Customers by Sales")

top_customers_sales = (
    customer_summary
    .sort_values(
        "Sales",
        ascending=False
    )
    .head(10)
    .copy()
)


top_customer_sales_chart = (
    top_customers_sales[
        [
            "Customer ID",
            "Sales"
        ]
    ]
    .set_index("Customer ID")
)


st.bar_chart(
    top_customer_sales_chart,
    width="stretch"
)


# ============================================================
# TOP CUSTOMERS BY GROSS PROFIT
# ============================================================

st.subheader("💰 Top Customers by Gross Profit")

top_customers_profit = (
    customer_summary
    .sort_values(
        "Gross_Profit",
        ascending=False
    )
    .head(10)
    .copy()
)


top_customer_profit_chart = (
    top_customers_profit[
        [
            "Customer ID",
            "Gross_Profit"
        ]
    ]
    .set_index("Customer ID")
)


st.bar_chart(
    top_customer_profit_chart,
    width="stretch"
)


# ============================================================
# CUSTOMER ORDER ACTIVITY
# ============================================================

st.subheader("📦 Top Customers by Number of Orders")

top_customers_orders = (
    customer_summary
    .sort_values(
        "Orders",
        ascending=False
    )
    .head(10)
    .copy()
)


top_customer_orders_chart = (
    top_customers_orders[
        [
            "Customer ID",
            "Orders"
        ]
    ]
    .set_index("Customer ID")
)


st.bar_chart(
    top_customer_orders_chart,
    width="stretch"
)


# ============================================================
# CUSTOMER PERFORMANCE TABLE
# ============================================================

st.subheader("📋 Customer Performance")

display_customer_summary = (
    customer_summary
    .sort_values(
        "Sales",
        ascending=False
    )
    .copy()
)


display_customer_summary["Sales"] = (
    display_customer_summary["Sales"]
    .map(lambda x: f"${x:,.2f}")
)


display_customer_summary["Gross_Profit"] = (
    display_customer_summary["Gross_Profit"]
    .map(lambda x: f"${x:,.2f}")
)


display_customer_summary["Units"] = (
    display_customer_summary["Units"]
    .map(lambda x: f"{x:,.0f}")
)


display_customer_summary["Gross Margin %"] = (
    display_customer_summary["Gross Margin %"]
    .map(lambda x: f"{x:.2f}%")
)


display_customer_summary = (
    display_customer_summary
    .rename(
        columns={
            "Customer ID": "Customer",
            "Sales": "Sales",
            "Gross_Profit": "Gross Profit",
            "Units": "Units Sold",
            "Orders": "Orders",
            "Products": "Products Purchased",
            "Gross Margin %": "Gross Margin"
        }
    )
)


st.dataframe(
    display_customer_summary,
    width="stretch",
    hide_index=True
)
# ============================================================
# FACTORY PERFORMANCE ANALYSIS
# ============================================================

st.divider()

st.header("🏭 Factory Performance Analysis")

st.write(
    "Connect products to their factories and compare factory-level "
    "sales, cost, gross profit, margin, and profit contribution."
)


# ------------------------------------------------------------
# PRODUCT → FACTORY MAPPING
# ------------------------------------------------------------

product_factory = {

    "Wonka Bar - Nutty Crunch Surprise": "Lot's O' Nuts",
    "Wonka Bar - Fudge Mallows": "Lot's O' Nuts",
    "Wonka Bar - Scrumdiddlyumptious": "Lot's O' Nuts",
    "Wonka Bar -Scrumdiddlyumptious": "Lot's O' Nuts",

    "Wonka Bar - Milk Chocolate": "Wicked Choccy's",
    "Wonka Bar - Triple Dazzle Caramel": "Wicked Choccy's",

    "Laffy Taffy": "Sugar Shack",
    "SweeTARTS": "Sugar Shack",
    "SweetTARTS": "Sugar Shack",
    "Nerds": "Sugar Shack",
    "Fun Dip": "Sugar Shack",
    "Fizzy Lifting Drinks": "Sugar Shack",

    "Everlasting Gobstopper": "Secret Factory",
    "Lickable Wallpaper": "Secret Factory",
    "Wonka Gum": "Secret Factory",

    "Hair Toffee": "The Other Factory",
    "Kazookles": "The Other Factory"
}


# ------------------------------------------------------------
# CREATE FACTORY DATA
# ------------------------------------------------------------

factory_df = filtered_df.copy()

factory_df["Factory"] = (
    factory_df["Product Name"]
    .map(product_factory)
)



# ------------------------------------------------------------
# CHECK UNMAPPED PRODUCTS
# ------------------------------------------------------------

unmapped_products = sorted(
    factory_df.loc[
        factory_df["Factory"].isna(),
        "Product Name"
    ]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

if unmapped_products:

    st.warning(
        "⚠️ Some products do not have a factory mapping yet: "
        + ", ".join(unmapped_products)
    )


# ------------------------------------------------------------
# FACTORY SUMMARY
# ------------------------------------------------------------

factory_summary = (
    factory_df
    .dropna(subset=["Factory"])
    .groupby("Factory", as_index=False)
    .agg(
        Sales=("Sales", "sum"),
        Cost=("Cost", "sum"),
        Gross_Profit=("Gross Profit", "sum"),
        Units=("Units", "sum"),
        Product_Count=("Product Name", "nunique")
    )
)


if not factory_summary.empty:

    # --------------------------------------------------------
    # GROSS MARGIN
    # --------------------------------------------------------

    factory_summary["Gross Margin %"] = (
        factory_summary["Gross_Profit"]
        .div(
            factory_summary["Sales"].replace(0, pd.NA)
        )
        .mul(100)
    )


    # --------------------------------------------------------
    # PROFIT PER UNIT
    # --------------------------------------------------------

    factory_summary["Profit per Unit"] = (
        factory_summary["Gross_Profit"]
        .div(
            factory_summary["Units"].replace(0, pd.NA)
        )
    )


    # --------------------------------------------------------
    # REVENUE CONTRIBUTION
    # --------------------------------------------------------

    total_factory_sales = (
        factory_summary["Sales"].sum()
    )

    factory_summary["Revenue Contribution %"] = (
        factory_summary["Sales"]
        .div(
            total_factory_sales
            if total_factory_sales
            else pd.NA
        )
        .mul(100)
    )


    # --------------------------------------------------------
    # PROFIT CONTRIBUTION
    # --------------------------------------------------------

    total_factory_profit = (
        factory_summary["Gross_Profit"].sum()
    )

    factory_summary["Profit Contribution %"] = (
        factory_summary["Gross_Profit"]
        .div(
            total_factory_profit
            if total_factory_profit
            else pd.NA
        )
        .mul(100)
    )


    # --------------------------------------------------------
    # SORT BY PROFIT
    # --------------------------------------------------------

    factory_summary = (
        factory_summary
        .sort_values(
            "Gross_Profit",
            ascending=False
        )
        .reset_index(drop=True)
    )


    # ========================================================
    # FACTORY KPI CARDS
    # ========================================================

    st.subheader("📊 Factory Performance Summary")

    best_factory_sales = factory_summary.loc[
        factory_summary["Sales"].idxmax()
    ]

    best_factory_profit = factory_summary.loc[
        factory_summary["Gross_Profit"].idxmax()
    ]

    best_factory_margin = factory_summary.loc[
        factory_summary["Gross Margin %"].idxmax()
    ]


    factory_columns = st.columns(4)


    with factory_columns[0]:

        st.metric(
            "🏆 Top Factory by Sales",
            best_factory_sales["Factory"],
            f"${best_factory_sales['Sales']:,.2f}"
        )


    with factory_columns[1]:

        st.metric(
            "💰 Top Factory by Profit",
            best_factory_profit["Factory"],
            f"${best_factory_profit['Gross_Profit']:,.2f}"
        )


    with factory_columns[2]:

        st.metric(
            "🎯 Highest Margin Factory",
            best_factory_margin["Factory"],
            f"{best_factory_margin['Gross Margin %']:.2f}% margin"
        )


    with factory_columns[3]:

        st.metric(
            "🏭 Factories Represented",
            f"{len(factory_summary):,}"
        )


    # ========================================================
    # FACTORY SALES VS PROFIT
    # ========================================================

    st.subheader("📈 Factory Sales vs Gross Profit")


    factory_chart = (
        factory_summary
        .set_index("Factory")[
            ["Sales", "Gross_Profit"]
        ]
        .rename(
            columns={
                "Gross_Profit": "Gross Profit"
            }
        )
    )


    st.bar_chart(
        factory_chart,
        width="stretch"
    )


    # ========================================================
    # FACTORY PERFORMANCE TABLE
    # ========================================================

    st.subheader("📋 Factory Performance")


    display_factory_summary = (
        factory_summary.copy()
    )


    display_factory_summary["Sales"] = (
        display_factory_summary["Sales"]
        .map(lambda x: f"${x:,.2f}")
    )


    display_factory_summary["Cost"] = (
        display_factory_summary["Cost"]
        .map(lambda x: f"${x:,.2f}")
    )


    display_factory_summary["Gross_Profit"] = (
        display_factory_summary["Gross_Profit"]
        .map(lambda x: f"${x:,.2f}")
    )


    display_factory_summary["Units"] = (
        display_factory_summary["Units"]
        .map(lambda x: f"{x:,.0f}")
    )


    display_factory_summary["Gross Margin %"] = (
        display_factory_summary["Gross Margin %"]
        .map(lambda x: f"{x:.2f}%")
    )


    display_factory_summary["Profit per Unit"] = (
        display_factory_summary["Profit per Unit"]
        .map(lambda x: f"${x:,.2f}")
    )


    display_factory_summary["Revenue Contribution %"] = (
        display_factory_summary["Revenue Contribution %"]
        .map(lambda x: f"{x:.2f}%")
    )


    display_factory_summary["Profit Contribution %"] = (
        display_factory_summary["Profit Contribution %"]
        .map(lambda x: f"{x:.2f}%")
    )


    display_factory_summary = (
        display_factory_summary.rename(
            columns={
                "Factory": "Factory",
                "Sales": "Sales",
                "Cost": "Cost",
                "Gross_Profit": "Gross Profit",
                "Units": "Units Sold",
                "Product_Count": "Products",
                "Gross Margin %": "Gross Margin",
                "Profit per Unit": "Profit per Unit",
                "Revenue Contribution %": "Revenue Contribution",
                "Profit Contribution %": "Profit Contribution"
            }
        )
    )


    st.dataframe(
        display_factory_summary,
        width="stretch",
        hide_index=True
    )


    # ========================================================
    # PRODUCT → FACTORY MAPPING
    # ========================================================

    st.subheader("🔗 Product → Factory Mapping")


    mapping_table = (
        factory_df[
            ["Product Name", "Division", "Factory"]
        ]
        .drop_duplicates()
        .sort_values(
            ["Factory", "Product Name"]
        )
    )


    st.dataframe(
        mapping_table,
        width="stretch",
        hide_index=True
    )
    # ========================================================
    # FACTORY INSIGHTS & RECOMMENDATIONS
    # ========================================================

    st.divider()

    st.header("💡 Factory Insights & Recommendations")

    st.write(
        "Automatically generated recommendations based on "
        "factory sales, profit, margin, and contribution."
    )

    # --------------------------------------------------------
    # FACTORY INSIGHTS
    # --------------------------------------------------------

    recommendation_count = 0

    # Highest revenue factory
    highest_revenue_factory = factory_summary.loc[
        factory_summary["Sales"].idxmax()
    ]

    # Highest profit factory
    highest_profit_factory = factory_summary.loc[
        factory_summary["Gross_Profit"].idxmax()
    ]

    # Highest margin factory
    highest_margin_factory = factory_summary.loc[
        factory_summary["Gross Margin %"].idxmax()
    ]

    # Lowest margin factory
    lowest_margin_factory = factory_summary.loc[
        factory_summary["Gross Margin %"].idxmin()
    ]

    # Lowest profit factory
    lowest_profit_factory = factory_summary.loc[
        factory_summary["Gross_Profit"].idxmin()
    ]

    # --------------------------------------------------------
    # KPI INSIGHTS
    # --------------------------------------------------------

    insight_columns = st.columns(3)

    with insight_columns[0]:

        st.info(
            f"🏆 **Revenue Leader**\n\n"
            f"{highest_revenue_factory['Factory']} generates "
            f"${highest_revenue_factory['Sales']:,.2f} in sales."
        )

    with insight_columns[1]:

        st.success(
            f"💰 **Profit Leader**\n\n"
            f"{highest_profit_factory['Factory']} generates "
            f"${highest_profit_factory['Gross_Profit']:,.2f} "
            f"in gross profit."
        )

    with insight_columns[2]:

        st.success(
            f"🎯 **Margin Leader**\n\n"
            f"{highest_margin_factory['Factory']} achieves "
            f"{highest_margin_factory['Gross Margin %']:.2f}% "
            f"gross margin."
        )

    # --------------------------------------------------------
    # RECOMMENDATIONS
    # --------------------------------------------------------

    st.subheader("📌 Recommended Actions")

    # 1. Margin risk
    margin_risk_factories = factory_summary[
        factory_summary["Gross Margin %"] < margin_threshold
    ]

    if not margin_risk_factories.empty:

        recommendation_count += 1

        risk_factory_names = ", ".join(
            margin_risk_factories["Factory"].astype(str).tolist()
        )

        st.warning(
            f"⚠️ **Margin Risk:** "
            f"{risk_factory_names} have gross margins below "
            f"the selected {margin_threshold}% threshold. "
            f"Review pricing, product mix, and production costs."
        )

    # 2. High revenue but lower margin
    revenue_median = factory_summary["Sales"].median()

    high_revenue_low_margin = factory_summary[
        (factory_summary["Sales"] >= revenue_median)
        & (factory_summary["Gross Margin %"] < margin_threshold)
    ]

    if not high_revenue_low_margin.empty:

        recommendation_count += 1

        factory_names = ", ".join(
            high_revenue_low_margin["Factory"].astype(str).tolist()
        )

        st.warning(
            f"📉 **Improve High-Revenue Factories:** "
            f"{factory_names} generate significant revenue "
            f"but have margins below the target. "
            f"Consider reducing costs or improving pricing."
        )

    # 3. Strong profit performers
    high_profit_factories = factory_summary[
        factory_summary["Gross_Profit"]
        >= factory_summary["Gross_Profit"].median()
    ]

    if not high_profit_factories.empty:

        recommendation_count += 1

        factory_names = ", ".join(
            high_profit_factories["Factory"].astype(str).tolist()
        )

        st.success(
            f"🚀 **Scale Strong Performers:** "
            f"{factory_names} are among the stronger profit "
            f"contributors. Consider prioritizing these factories "
            f"for growth and inventory availability."
        )

    # 4. Lowest margin factory
    if lowest_margin_factory["Gross Margin %"] < margin_threshold:

        recommendation_count += 1

        st.warning(
            f"🔍 **Priority Factory Review:** "
            f"{lowest_margin_factory['Factory']} has the lowest "
            f"gross margin at "
            f"{lowest_margin_factory['Gross Margin %']:.2f}%. "
            f"Investigate its cost structure and product mix."
        )

    # 5. Lowest profit factory
    if len(factory_summary) > 1:

        recommendation_count += 1

        st.info(
            f"📊 **Profit Improvement Opportunity:** "
            f"{lowest_profit_factory['Factory']} has the lowest "
            f"gross profit at "
            f"${lowest_profit_factory['Gross_Profit']:,.2f}. "
            f"Review whether its products, pricing, or costs "
            f"are limiting profitability."
        )

    # --------------------------------------------------------
    # NO PROBLEMS FOUND
    # --------------------------------------------------------

    if recommendation_count == 0:

        st.success(
            "✅ **No major factory issues detected** "
            "under the current filters and margin threshold."
        )

    # --------------------------------------------------------
    # RECOMMENDATION SUMMARY TABLE
    # --------------------------------------------------------

    st.subheader("📋 Factory Recommendation Summary")

    recommendation_table = factory_summary[
        [
            "Factory",
            "Sales",
            "Gross_Profit",
            "Gross Margin %",
            "Revenue Contribution %",
            "Profit Contribution %"
        ]
    ].copy()

    recommendation_table["Status"] = recommendation_table[
        "Gross Margin %"
    ].apply(
        lambda x:
        "⚠️ Margin Risk"
        if x < margin_threshold
        else "✅ Healthy"
    )

    recommendation_table["Action"] = recommendation_table[
        "Gross Margin %"
    ].apply(
        lambda x:
        "Review pricing & costs"
        if x < margin_threshold
        else "Maintain / grow"
    )

    recommendation_table = recommendation_table.rename(
        columns={
            "Gross_Profit": "Gross Profit",
            "Gross Margin %": "Gross Margin",
            "Revenue Contribution %": "Revenue Contribution",
            "Profit Contribution %": "Profit Contribution"
        }
    )

    st.dataframe(
        recommendation_table,
        width="stretch",
        hide_index=True
    )

else:

    st.info(
        "No factory data is available for the selected filters."
    )

# ============================================================
# CUSTOMER INSIGHTS
# ============================================================

st.subheader("🔎 Customer Insights")

if not customer_summary.empty:

    top_sales_customer = (
        customer_summary
        .sort_values(
            "Sales",
            ascending=False
        )
        .iloc[0]
    )

    top_profit_customer = (
        customer_summary
        .sort_values(
            "Gross_Profit",
            ascending=False
        )
        .iloc[0]
    )

    top_orders_customer = (
        customer_summary
        .sort_values(
            "Orders",
            ascending=False
        )
        .iloc[0]
    )

    highest_margin_customer = (
        customer_summary
        .sort_values(
            "Gross Margin %",
            ascending=False
        )
        .iloc[0]
    )


    st.info(
        f"💰 **Sales Leader:** "
        f"Customer {top_sales_customer['Customer ID']} generated "
        f"${top_sales_customer['Sales']:,.2f} in sales."
    )


    st.success(
        f"🏆 **Profit Leader:** "
        f"Customer {top_profit_customer['Customer ID']} generated "
        f"${top_profit_customer['Gross_Profit']:,.2f} "
        f"in gross profit."
    )


    st.warning(
        f"📦 **Most Active Customer:** "
        f"Customer {top_orders_customer['Customer ID']} placed "
        f"{top_orders_customer['Orders']:,} orders."
    )


    st.info(
        f"🎯 **Highest Margin Customer:** "
        f"Customer {highest_margin_customer['Customer ID']} achieved "
        f"{highest_margin_customer['Gross Margin %']:.2f}% gross margin."
    )