import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io
import os

# ==========================================
# PAGE CONFIGURATION & MONOCHROME BLACK THEME
# ==========================================
st.set_page_config(
    page_title="Superstore Executive Hub — Commercial Intelligence",
    page_icon="■",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End CSS: Satoshi Font, Luxury Monochrome UI & Soft Accents
st.markdown("""
<style>
    @import url('https://api.fontshare.com/v2/css?f[]=satoshi@900,800,700,600,500,400,300&display=swap');

    /* Global Typography */
    html, body, .stApp, p, span, div, h1, h2, h3, h4, h5, h6, input, select, textarea, button, .stMarkdown {
        font-family: 'Satoshi', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background-color: #000000 !important;
        color: #ffffff;
    }

    .main .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2.5rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 98% !important;
    }

    /* Standard Docked Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #070709 !important;
        border-right: none !important;
    }

    /* Sidebar Collapse / Expand Arrow Button */
    [data-testid="stSidebarCollapseButton"],
    [data-testid="baseButton-headerNoPadding"],
    [data-testid="stSidebarHeader"] button,
    [data-testid="stHeader"] button,
    button[kind="header"] {
        color: #ffffff !important;
        fill: #ffffff !important;
        background-color: transparent !important;
        opacity: 0.9 !important;
        visibility: visible !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    [data-testid="stSidebarCollapseButton"]:hover,
    [data-testid="baseButton-headerNoPadding"]:hover,
    [data-testid="stHeader"] button:hover {
        opacity: 1 !important;
        background-color: rgba(255, 255, 255, 0.08) !important;
        border-radius: 8px !important;
    }
    [data-testid="stSidebarCollapseButton"] svg,
    [data-testid="stSidebarHeader"] svg,
    [data-testid="stHeader"] svg {
        stroke: #ffffff !important;
        fill: #ffffff !important;
        width: 1.25rem !important;
        height: 1.25rem !important;
        visibility: visible !important;
    }

    /* =========================================
       FIXED MULTISELECT TAG CHIPS & BUTTONS
       ========================================= */
    
    span[data-baseweb="tag"],
    div[data-baseweb="tag"],
    [data-baseweb="tag"] {
        background-color: #27272e !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 6px !important;
        padding: 2px 6px !important;
        color: #ffffff !important;
    }
    span[data-baseweb="tag"] span,
    div[data-baseweb="tag"] span,
    span[data-baseweb="tag"] div,
    div[data-baseweb="tag"] div,
    [data-baseweb="tag"] * {
        color: #ffffff !important;
        font-weight: 500 !important;
        font-size: 0.78rem !important;
        background-color: transparent !important;
    }
    span[data-baseweb="tag"] svg,
    div[data-baseweb="tag"] svg,
    [data-baseweb="tag"] svg {
        fill: #a1a1aa !important;
        stroke: #a1a1aa !important;
    }
    span[data-baseweb="tag"] svg:hover,
    div[data-baseweb="tag"] svg:hover {
        fill: #ffffff !important;
        stroke: #ffffff !important;
    }

    div[data-baseweb="select"] > div {
        background-color: #0e0e12 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 10px !important;
        color: #ffffff !important;
    }
    div[data-baseweb="select"] > div:hover {
        border-color: rgba(255, 255, 255, 0.2) !important;
    }
    div[data-baseweb="select"] > div:focus-within {
        border-color: rgba(255, 255, 255, 0.4) !important;
    }

    /* Action & Download Buttons */
    div.stDownloadButton > button,
    div.stButton > button,
    button[data-testid="baseButton-secondary"],
    button[data-testid="baseButton-primary"] {
        background-color: #141419 !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 12px !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 600 !important;
        font-size: 0.84rem !important;
        letter-spacing: -0.01em !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.4) !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 8px !important;
    }

    div.stDownloadButton > button:hover,
    div.stButton > button:hover,
    button[data-testid="baseButton-secondary"]:hover,
    button[data-testid="baseButton-primary"]:hover {
        background-color: #22222b !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
        color: #ffffff !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.6) !important;
    }

    div.stDownloadButton > button:active,
    div.stButton > button:active {
        transform: scale(0.98) !important;
    }

    div[data-baseweb="input"],
    div[data-baseweb="base-input"] {
        background-color: #0e0e12 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 10px !important;
        color: #ffffff !important;
    }

    /* Top Executive Navigation Header */
    .bento-nav-card {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.3rem 1.8rem;
        background: #0e0e12;
        border-radius: 16px;
        margin-bottom: 1.4rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
    }
    .brand-title {
        font-size: 1.55rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        color: #ffffff;
        margin: 0;
    }
    .brand-subtitle {
        font-size: 0.82rem;
        color: #71717a;
        font-weight: 500;
        margin-top: 3px;
        letter-spacing: 0.01em;
    }
    .live-chip {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: #18181b;
        color: #e4e4e7;
        padding: 6px 14px;
        border-radius: 8px;
        font-size: 0.76rem;
        font-weight: 600;
    }
    .pulse-dot {
        width: 6px;
        height: 6px;
        background-color: #8ebaa3;
        border-radius: 50%;
        box-shadow: 0 0 6px rgba(142, 186, 163, 0.6);
    }

    /* Bento Grid KPI Cards */
    .bento-kpi-container {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 1rem;
        margin-bottom: 1.4rem;
    }
    .bento-card {
        background: #0e0e12;
        border-radius: 16px;
        padding: 1.25rem 1.4rem;
        transition: all 0.2s ease;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
    }
    .bento-card:hover {
        transform: translateY(-2px);
        background: #141419;
    }

    .bento-card-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.6rem;
    }
    .bento-label {
        font-size: 0.74rem;
        font-weight: 700;
        color: #71717a;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    .svg-icon {
        color: #a1a1aa;
        display: flex;
        align-items: center;
    }
    .bento-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.03em;
        line-height: 1.1;
        margin-bottom: 0.45rem;
        font-feature-settings: "tnum";
    }
    .bento-footer {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 0.76rem;
        font-weight: 600;
    }
    .pill-soft-green {
        background: rgba(142, 186, 163, 0.15);
        color: #8ebaa3;
        padding: 3px 8px;
        border-radius: 6px;
    }
    .pill-soft-red {
        background: rgba(217, 130, 116, 0.15);
        color: #d98274;
        padding: 3px 8px;
        border-radius: 6px;
    }
    .pill-soft-blue {
        background: rgba(126, 158, 184, 0.15);
        color: #7e9eb8;
        padding: 3px 8px;
        border-radius: 6px;
    }

    /* Minimalist Insight Banner */
    .bento-insight-banner {
        background: #0e0e12;
        border-radius: 14px;
        padding: 0.9rem 1.3rem;
        margin-bottom: 1.4rem;
        display: flex;
        align-items: center;
        gap: 12px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
    }
    .insight-indicator {
        width: 3px;
        height: 24px;
        background: #7e9eb8;
        border-radius: 2px;
        flex-shrink: 0;
    }

    /* Tab Controls */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: #0a0a0d;
        padding: 4px;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 38px;
        border-radius: 8px;
        color: #71717a;
        font-weight: 600;
        font-size: 0.84rem;
        padding: 0 16px;
        border: none !important;
        background: transparent;
        transition: all 0.15s ease;
    }
    .stTabs [aria-selected="true"] {
        background: #181820 !important;
        color: #ffffff !important;
    }

    /* Clean Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #000000;
    }
    ::-webkit-scrollbar-thumb {
        background: #27272a;
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# PLOTLY SOFT COLOR PALETTE THEME ENGINE
# ==========================================
def apply_bento_chart_theme(fig, height=360):
    fig.update_layout(
        template="plotly_dark",
        height=height,
        margin=dict(l=15, r=15, t=35, b=15),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Satoshi, sans-serif", color="#8e8e93", size=11),
        hoverlabel=dict(
            bgcolor="#141419",
            font_size=12,
            font_family="Satoshi",
            bordercolor="rgba(255,255,255,0.08)"
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            color="#52525b",
            tickfont=dict(color="#8e8e93", size=10)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(255, 255, 255, 0.03)",
            zeroline=False,
            color="#52525b",
            tickfont=dict(color="#8e8e93", size=10)
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color="#a1a1aa", size=10),
            bgcolor="rgba(0,0,0,0)"
        )
    )
    return fig

# ==========================================
# DATA LOADING & CACHING
# ==========================================
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_paths = [
        os.path.join(current_dir, "data", "Sample - Superstore.csv"),
        os.path.join(current_dir, "Sample - Superstore.csv"),
        "01_Executive_Superstore_Dashboard/data/Sample - Superstore.csv",
        "data/Sample - Superstore.csv",
        "Sample - Superstore.csv"
    ]
    
    df = None
    for path in file_paths:
        if os.path.exists(path):
            try:
                df = pd.read_csv(path, encoding='utf-8')
                break
            except UnicodeDecodeError:
                df = pd.read_csv(path, encoding='windows-1252')
                break
                
    if df is None:
        url = "https://raw.githubusercontent.com/zpio/datasets/main/sample_superstore.csv"
        try:
            df = pd.read_csv(url, encoding='windows-1252')
        except Exception:
            df = pd.read_csv(url)

    df.columns = [c.strip().lower().replace(" ", "_").replace("-", "_") for c in df.columns]
    
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    df['ship_date'] = pd.to_datetime(df['ship_date'], errors='coerce')
    df = df.dropna(subset=['order_date']).copy()
    
    df['year'] = df['order_date'].dt.year
    df['month'] = df['order_date'].dt.month
    df['year_month'] = df['order_date'].dt.to_period('M').astype(str)
    df['shipping_days'] = (df['ship_date'] - df['order_date']).dt.days
    df['profit_margin'] = np.where(df['sales'] != 0, (df['profit'] / df['sales']) * 100, 0)
    
    return df

df_raw = load_data()

# ==========================================
# SIDEBAR FILTERS
# ==========================================
with st.sidebar:
    st.markdown("""
    <div style="padding-bottom: 0.8rem; margin-bottom: 1rem; border-bottom: 1px solid rgba(255,255,255,0.06);">
        <div style="font-weight: 800; font-size: 1.1rem; color: #ffffff; letter-spacing: -0.02em;">SUPERSTORE BI</div>
        <div style="font-size: 0.72rem; color: #7e9eb8; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">Commercial Analytics</div>
    </div>
    """, unsafe_allow_html=True)
    
    min_date = df_raw['order_date'].min().date()
    max_date = df_raw['order_date'].max().date()
    
    st.markdown("<span style='font-size:0.8rem; font-weight:600; color:#a1a1aa;'>Date Range</span>", unsafe_allow_html=True)
    date_selection = st.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        label_visibility="collapsed"
    )
    
    if isinstance(date_selection, (tuple, list)) and len(date_selection) == 2:
        start_date, end_date = date_selection
    else:
        start_date, end_date = min_date, max_date
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("<span style='font-size:0.8rem; font-weight:600; color:#a1a1aa;'>Market Hierarchy</span>", unsafe_allow_html=True)
    all_regions = sorted(df_raw['region'].dropna().unique().tolist())
    selected_regions = st.multiselect(
        "Regions",
        options=all_regions,
        default=all_regions
    )
    
    all_segments = sorted(df_raw['segment'].dropna().unique().tolist())
    selected_segments = st.multiselect(
        "Customer Segments",
        options=all_segments,
        default=all_segments
    )
    
    all_categories = sorted(df_raw['category'].dropna().unique().tolist())
    selected_categories = st.multiselect(
        "Product Categories",
        options=all_categories,
        default=all_categories
    )
    
    available_subcats = sorted(
        df_raw[df_raw['category'].isin(selected_categories if selected_categories else all_categories)]['sub_category']
        .dropna().unique().tolist()
    )
    selected_subcats = st.multiselect(
        "Sub-Categories",
        options=available_subcats,
        default=available_subcats
    )

# ==========================================
# FILTER DATA ENGINE
# ==========================================
filtered_df = df_raw[
    (df_raw['order_date'].dt.date >= start_date) & 
    (df_raw['order_date'].dt.date <= end_date)
]
if selected_regions:
    filtered_df = filtered_df[filtered_df['region'].isin(selected_regions)]
if selected_segments:
    filtered_df = filtered_df[filtered_df['segment'].isin(selected_segments)]
if selected_categories:
    filtered_df = filtered_df[filtered_df['category'].isin(selected_categories)]
if selected_subcats:
    filtered_df = filtered_df[filtered_df['sub_category'].isin(selected_subcats)]

# ==========================================
# TOP NAVIGATION HEADER
# ==========================================
st.markdown(f"""
<div class="bento-nav-card">
    <div>
        <h1 class="brand-title">Executive Performance Hub</h1>
        <div class="brand-subtitle">Commercial Velocity, RFM Retention & Regional Contribution Matrix</div>
    </div>
    <div class="live-chip">
        <span class="pulse-dot"></span> {start_date.strftime('%b %Y')} – {end_date.strftime('%b %Y')}
    </div>
</div>
""", unsafe_allow_html=True)

if filtered_df.empty:
    st.warning("No records match the current filter selection.")
    st.stop()

# ==========================================
# BENTO KPI CARDS ROW
# ==========================================
total_sales = filtered_df['sales'].sum()
total_profit = filtered_df['profit'].sum()
profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
total_orders = filtered_df['order_id'].nunique()
total_customers = filtered_df['customer_id'].nunique()
avg_order_value = (total_sales / total_orders) if total_orders > 0 else 0

margin_pill_class = "pill-soft-green" if profit_margin >= 12 else ("pill-soft-red" if profit_margin < 0 else "pill-soft-blue")

st.markdown(f"""
<div class="bento-kpi-container">
    <div class="bento-card">
        <div class="bento-card-top">
            <span class="bento-label">Gross Revenue</span>
            <span class="svg-icon">
                <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#7e9eb8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>
            </span>
        </div>
        <div class="bento-value">${total_sales:,.0f}</div>
        <div class="bento-footer">
            <span class="pill-soft-blue">Total Sales</span>
        </div>
    </div>
    <div class="bento-card">
        <div class="bento-card-top">
            <span class="bento-label">Net Profit</span>
            <span class="svg-icon">
                <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#8ebaa3" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline><polyline points="17 6 23 6 23 12"></polyline></svg>
            </span>
        </div>
        <div class="bento-value">${total_profit:,.0f}</div>
        <div class="bento-footer">
            <span class="{margin_pill_class}">Margin {profit_margin:.1f}%</span>
        </div>
    </div>
    <div class="bento-card">
        <div class="bento-card-top">
            <span class="bento-label">Total Orders</span>
            <span class="svg-icon">
                <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#a1a1aa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path><line x1="3" y1="6" x2="21" y2="6"></line><path d="M16 10a4 4 0 0 1-8 0"></path></svg>
            </span>
        </div>
        <div class="bento-value">{total_orders:,}</div>
        <div class="bento-footer">
            <span class="pill-soft-blue">Unique Orders</span>
        </div>
    </div>
    <div class="bento-card">
        <div class="bento-card-top">
            <span class="bento-label">Active Clients</span>
            <span class="svg-icon">
                <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#8ebaa3" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
            </span>
        </div>
        <div class="bento-value">{total_customers:,}</div>
        <div class="bento-footer">
            <span class="pill-soft-green">Client Base</span>
        </div>
    </div>
    <div class="bento-card">
        <div class="bento-card-top">
            <span class="bento-label">Avg Order Value</span>
            <span class="svg-icon">
                <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#9fa8da" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><circle cx="12" cy="12" r="6"></circle><circle cx="12" cy="12" r="2"></circle></svg>
            </span>
        </div>
        <div class="bento-value">${avg_order_value:,.1f}</div>
        <div class="bento-footer">
            <span class="pill-soft-blue">AOV / Basket</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# MINIMALIST INSIGHT BANNER
# ==========================================
best_cat = filtered_df.groupby('category')['sales'].sum().idxmax()
best_cat_sales = filtered_df.groupby('category')['sales'].sum().max()
worst_subcat = filtered_df.groupby('sub_category')['profit'].sum().idxmin()
worst_subcat_profit = filtered_df.groupby('sub_category')['profit'].sum().min()

st.markdown(f"""
<div class="bento-insight-banner">
    <div class="insight-indicator"></div>
    <div style="font-size: 0.84rem; color: #a1a1aa; line-height: 1.5;">
        <b style="color:#ffffff;">Executive Note:</b> Category <b style="color:#7e9eb8;">{best_cat}</b> generated the highest gross volume (<b style="color:#ffffff;">${best_cat_sales:,.0f}</b>). 
        {"Margin deficit detected in sub-category <b style='color:#d98274;'>" + worst_subcat + "</b> with net loss of <b style='color:#d98274;'>$" + f"{worst_subcat_profit:,.0f}</b>." if worst_subcat_profit < 0 else "All sub-categories maintain positive net contribution."}
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# ANALYTICAL MODULES (TABS)
# ==========================================
tab_overview, tab_geo, tab_customer, tab_product, tab_data = st.tabs([
    "Financial Trajectory",
    "Geospatial & Regional",
    "Customer Retention & RFM",
    "Product Margin & Pricing",
    "Data Explorer"
])

# ----------------------------------------------------
# TAB 1: FINANCIAL TRAJECTORY (SOFT PALETTE)
# ----------------------------------------------------
with tab_overview:
    b1_left, b1_right = st.columns([7, 5])
    
    with b1_left:
        st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#ffffff; margin-bottom:0.5rem;'>Monthly Revenue & Profit Trajectory</p>", unsafe_allow_html=True)
        monthly_df = filtered_df.groupby('year_month').agg(
            sales=('sales', 'sum'),
            profit=('profit', 'sum')
        ).reset_index().sort_values('year_month')
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=monthly_df['year_month'],
            y=monthly_df['sales'],
            name="Gross Sales ($)",
            mode="lines+markers",
            line=dict(color="#7e9eb8", width=2.8, shape="spline"),
            fill='tozeroy',
            fillcolor='rgba(126, 158, 184, 0.12)'
        ))
        fig_trend.add_trace(go.Scatter(
            x=monthly_df['year_month'],
            y=monthly_df['profit'],
            name="Net Profit ($)",
            mode="lines+markers",
            line=dict(color="#8ebaa3", width=2.4, shape="spline"),
            yaxis="y2"
        ))
        fig_trend.update_layout(
            hovermode="x unified",
            yaxis2=dict(
                title="Profit ($)",
                overlaying="y",
                side="right",
                showgrid=False,
                tickfont=dict(color="#8ebaa3", size=10)
            )
        )
        apply_bento_chart_theme(fig_trend, height=360)
        st.plotly_chart(fig_trend, use_container_width=True)
        
    with b1_right:
        st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#ffffff; margin-bottom:0.5rem;'>Customer Segment Distribution</p>", unsafe_allow_html=True)
        seg_df = filtered_df.groupby('segment').agg(
            sales=('sales', 'sum'),
            profit=('profit', 'sum')
        ).reset_index()
        
        fig_seg = px.pie(
            seg_df,
            values='sales',
            names='segment',
            hole=0.62,
            color='segment',
            color_discrete_map={
                'Consumer': '#7e9eb8',
                'Corporate': '#9fa8da',
                'Home Office': '#b0a8a0'
            }
        )
        fig_seg.update_traces(
            textposition='outside',
            textinfo='percent+label',
            hovertemplate="<b>%{label}</b><br>Sales: $%{value:,.0f}<br>Share: %{percent}"
        )
        apply_bento_chart_theme(fig_seg, height=360)
        fig_seg.update_layout(showlegend=False)
        st.plotly_chart(fig_seg, use_container_width=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    b1_c3, b1_c4 = st.columns([6, 6])
    with b1_c3:
        st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#ffffff; margin-bottom:0.5rem;'>Sales by Sub-Category</p>", unsafe_allow_html=True)
        sub_sales = filtered_df.groupby(['category', 'sub_category'])['sales'].sum().reset_index().sort_values('sales', ascending=True)
        fig_sub = px.bar(
            sub_sales,
            x='sales',
            y='sub_category',
            color='category',
            orientation='h',
            color_discrete_sequence=['#7e9eb8', '#9fa8da', '#8ebaa3'],
            labels={'sales': 'Sales ($)', 'sub_category': 'Sub-Category', 'category': 'Category'}
        )
        apply_bento_chart_theme(fig_sub, height=420)
        st.plotly_chart(fig_sub, use_container_width=True)
        
    with b1_c4:
        st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#ffffff; margin-bottom:0.5rem;'>Profit Margin Spectrum (%)</p>", unsafe_allow_html=True)
        sub_prof = filtered_df.groupby('sub_category').agg(
            sales=('sales', 'sum'),
            profit=('profit', 'sum')
        ).reset_index()
        sub_prof['margin'] = (sub_prof['profit'] / sub_prof['sales']) * 100
        sub_prof = sub_prof.sort_values('margin', ascending=True)
        
        bar_colors = ['#d98274' if m < 0 else '#8ebaa3' for m in sub_prof['margin']]
        fig_m = go.Figure(go.Bar(
            x=sub_prof['margin'],
            y=sub_prof['sub_category'],
            orientation='h',
            marker=dict(color=bar_colors, line=dict(width=0)),
            text=[f"{m:+.1f}%" for m in sub_prof['margin']],
            textposition='outside'
        ))
        apply_bento_chart_theme(fig_m, height=420)
        fig_m.update_layout(xaxis=dict(title="Profit Margin %"))
        st.plotly_chart(fig_m, use_container_width=True)

# ----------------------------------------------------
# TAB 2: GEOSPATIAL & REGIONAL (SOFT PALETTE)
# ----------------------------------------------------
with tab_geo:
    us_state_to_code = {
        'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
        'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
        'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
        'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
        'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
        'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH',
        'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC',
        'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA',
        'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN',
        'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA',
        'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY', 'District of Columbia': 'DC'
    }
    
    state_df = filtered_df.groupby('state').agg(
        sales=('sales', 'sum'),
        profit=('profit', 'sum'),
        orders=('order_id', 'nunique')
    ).reset_index()
    state_df['profit_margin'] = (state_df['profit'] / state_df['sales']) * 100
    state_df['state_code'] = state_df['state'].map(us_state_to_code)
    
    g_left, g_right = st.columns([7, 5])
    with g_left:
        st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#ffffff; margin-bottom:0.5rem;'>State-Level Revenue Density (US)</p>", unsafe_allow_html=True)
        fig_map = px.choropleth(
            state_df.dropna(subset=['state_code']),
            locations='state_code',
            locationmode="USA-states",
            color='sales',
            scope="usa",
            color_continuous_scale=[[0, '#0e1117'], [0.4, '#364f6b'], [1, '#7e9eb8']],
            hover_name='state',
            hover_data={'sales': ':$,.0f', 'profit': ':$,.0f', 'profit_margin': ':.1f%'},
            labels={'sales': 'Revenue ($)', 'profit': 'Profit ($)', 'profit_margin': 'Margin'}
        )
        fig_map.update_layout(
            geo=dict(bgcolor='rgba(0,0,0,0)', lakecolor='rgba(14, 17, 23, 0.6)'),
            margin=dict(l=0, r=0, t=10, b=10)
        )
        apply_bento_chart_theme(fig_map, height=380)
        st.plotly_chart(fig_map, use_container_width=True)
        
    with g_right:
        st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#ffffff; margin-bottom:0.5rem;'>Top 5 Contributing States</p>", unsafe_allow_html=True)
        top_states = state_df.sort_values('sales', ascending=False).head(5)
        for _, r in top_states.iterrows():
            margin_color = "#8ebaa3" if r['profit_margin'] >= 10 else ("#d98274" if r['profit_margin'] < 0 else "#d8b384")
            st.markdown(f"""
            <div style="background: #0e0e12; border-radius: 12px; padding: 12px 16px; margin-bottom: 8px;">
                <div style="display:flex; justify-content:space-between; font-weight:700; color:#ffffff; font-size: 0.9rem;">
                    <span>{r['state']}</span>
                    <span style="color:#7e9eb8;">${r['sales']:,.0f}</span>
                </div>
                <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:#71717a; margin-top:4px;">
                    <span>Profit: ${r['profit']:,.0f}</span>
                    <span style="color:{margin_color};">Margin: {r['profit_margin']:.1f}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown("<br>", unsafe_allow_html=True)
    
    g2_left, g2_right = st.columns(2)
    with g2_left:
        st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#ffffff; margin-bottom:0.5rem;'>Regional Profitability Matrix (Region vs Segment)</p>", unsafe_allow_html=True)
        pivot_r = filtered_df.pivot_table(index='region', columns='segment', values='profit', aggfunc='sum').fillna(0)
        fig_hm = px.imshow(
            pivot_r,
            text_auto="$,.0f",
            color_continuous_scale=[[0, '#10141a'], [0.5, '#2c4257'], [1, '#7e9eb8']],
            aspect="auto",
            labels=dict(x="Segment", y="Region", color="Profit ($)")
        )
        apply_bento_chart_theme(fig_hm, height=330)
        st.plotly_chart(fig_hm, use_container_width=True)
        
    with g2_right:
        st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#ffffff; margin-bottom:0.5rem;'>Fulfillment Dynamics by Shipping Mode</p>", unsafe_allow_html=True)
        ship_df = filtered_df.groupby('ship_mode').agg(
            sales=('sales', 'sum'),
            profit=('profit', 'sum'),
            avg_days=('shipping_days', 'mean')
        ).reset_index().sort_values('sales', ascending=False)
        
        fig_ship = px.bar(
            ship_df,
            x='ship_mode',
            y='sales',
            color='avg_days',
            text_auto='$,.0f',
            color_continuous_scale=[[0, '#4b6584'], [1, '#7e9eb8']],
            labels={'sales': 'Sales ($)', 'ship_mode': 'Ship Mode', 'avg_days': 'Avg Days'}
        )
        apply_bento_chart_theme(fig_ship, height=330)
        st.plotly_chart(fig_ship, use_container_width=True)

# ----------------------------------------------------
# TAB 3: CUSTOMER RETENTION & RFM (SOFT PALETTE)
# ----------------------------------------------------
with tab_customer:
    ref_date = filtered_df['order_date'].max()
    cust_rfm = filtered_df.groupby('customer_id').agg(
        customer_name=('customer_name', 'first'),
        segment=('segment', 'first'),
        recency=('order_date', lambda x: (ref_date - x.max()).days),
        frequency=('order_id', 'nunique'),
        monetary=('sales', 'sum'),
        profit=('profit', 'sum')
    ).reset_index()
    
    cust_rfm['churn_risk'] = np.where(
        cust_rfm['recency'] > 365, "Lost (>365d)",
        np.where(cust_rfm['recency'] > 180, "At Risk (180-365d)", "Active (<180d)")
    )
    
    c1, c2, c3 = st.columns([4, 4, 4])
    with c1:
        churn_counts = cust_rfm['churn_risk'].value_counts().reset_index()
        churn_counts.columns = ['Status', 'Count']
        fig_c_pie = px.pie(
            churn_counts,
            values='Count',
            names='Status',
            hole=0.55,
            color='Status',
            color_discrete_map={
                'Active (<180d)': '#8ebaa3',
                'At Risk (180-365d)': '#d8b384',
                'Lost (>365d)': '#d98274'
            }
        )
        fig_c_pie.update_traces(textposition='inside', textinfo='percent+label')
        apply_bento_chart_theme(fig_c_pie, height=320)
        fig_c_pie.update_layout(title="Churn Risk Cohorts", showlegend=False)
        st.plotly_chart(fig_c_pie, use_container_width=True)
        
    with c2:
        fig_c_rfm = px.scatter(
            cust_rfm,
            x='recency',
            y='monetary',
            size='frequency',
            color='churn_risk',
            hover_name='customer_name',
            color_discrete_map={
                'Active (<180d)': '#8ebaa3',
                'At Risk (180-365d)': '#d8b384',
                'Lost (>365d)': '#d98274'
            },
            labels={'recency': 'Days Since Last Transaction', 'monetary': 'Monetary Value ($)', 'churn_risk': 'Cohort'}
        )
        apply_bento_chart_theme(fig_c_rfm, height=320)
        fig_c_rfm.update_layout(title="Recency vs Lifetime Spend")
        st.plotly_chart(fig_c_rfm, use_container_width=True)
        
    with c3:
        act = (cust_rfm['churn_risk'] == 'Active (<180d)').sum()
        risk = (cust_rfm['churn_risk'] == 'At Risk (180-365d)').sum()
        lost = (cust_rfm['churn_risk'] == 'Lost (>365d)').sum()
        
        st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#ffffff; margin-bottom:0.5rem;'>Client Cohort Health</p>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="display:flex; flex-direction:column; gap:8px;">
            <div style="background:#0e0e12; border-radius:10px; padding:12px;">
                <div style="color:#8ebaa3; font-weight:700; font-size:0.85rem;">Active (&lt;180d): {act} clients</div>
                <div style="color:#71717a; font-size:0.75rem;">{(act/len(cust_rfm)*100):.1f}% active purchasing base.</div>
            </div>
            <div style="background:#0e0e12; border-radius:10px; padding:12px;">
                <div style="color:#d8b384; font-weight:700; font-size:0.85rem;">At Risk (180-365d): {risk} clients</div>
                <div style="color:#71717a; font-size:0.75rem;">{(risk/len(cust_rfm)*100):.1f}% inactive for 6-12 months.</div>
            </div>
            <div style="background:#0e0e12; border-radius:10px; padding:12px;">
                <div style="color:#d98274; font-weight:700; font-size:0.85rem;">Lost (&gt;365d): {lost} clients</div>
                <div style="color:#71717a; font-size:0.75rem;">{(lost/len(cust_rfm)*100):.1f}% churned accounts.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    top_c_l, top_c_r = st.columns(2)
    with top_c_l:
        st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#ffffff; margin-bottom:0.5rem;'>Top 10 High-Margin Accounts</p>", unsafe_allow_html=True)
        top_10 = cust_rfm.sort_values('profit', ascending=False).head(10)
        fig_t10 = px.bar(
            top_10,
            x='profit',
            y='customer_name',
            orientation='h',
            color='profit',
            color_continuous_scale=[[0, '#1c2826'], [1, '#8ebaa3']],
            labels={'profit': 'Profit ($)', 'customer_name': 'Client'}
        )
        fig_t10.update_layout(yaxis=dict(autorange="reversed"))
        apply_bento_chart_theme(fig_t10, height=360)
        st.plotly_chart(fig_t10, use_container_width=True)
        
    with top_c_r:
        st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#ffffff; margin-bottom:0.5rem;'>Top 10 Loss-Driving Accounts</p>", unsafe_allow_html=True)
        bot_10 = cust_rfm.sort_values('profit', ascending=True).head(10)
        fig_b10 = px.bar(
            bot_10,
            x='profit',
            y='customer_name',
            orientation='h',
            color='profit',
            color_continuous_scale=[[0, '#d98274'], [1, '#241a1a']],
            labels={'profit': 'Profit ($)', 'customer_name': 'Client'}
        )
        apply_bento_chart_theme(fig_b10, height=360)
        st.plotly_chart(fig_b10, use_container_width=True)

# ----------------------------------------------------
# TAB 4: PRODUCT & PRICING (SOFT PALETTE)
# ----------------------------------------------------
with tab_product:
    p1, p2 = st.columns(2)
    with p1:
        st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#ffffff; margin-bottom:0.5rem;'>Top 10 Revenue Generating SKUs</p>", unsafe_allow_html=True)
        top_prod = filtered_df.groupby('product_name').agg(
            sales=('sales', 'sum'),
            profit=('profit', 'sum')
        ).reset_index().sort_values('sales', ascending=False).head(10)
        
        fig_tp = px.bar(
            top_prod,
            x='sales',
            y='product_name',
            orientation='h',
            color='profit',
            color_continuous_scale=[[0, '#2d4059'], [1, '#7e9eb8']],
            labels={'sales': 'Sales ($)', 'product_name': 'SKU', 'profit': 'Profit ($)'}
        )
        fig_tp.update_layout(yaxis=dict(autorange="reversed"))
        apply_bento_chart_theme(fig_tp, height=400)
        st.plotly_chart(fig_tp, use_container_width=True)
        
    with p2:
        st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#ffffff; margin-bottom:0.5rem;'>Discount vs Margin Sensitivity</p>", unsafe_allow_html=True)
        sample_prod = filtered_df.sample(min(len(filtered_df), 1200), random_state=42)
        fig_disc = px.scatter(
            sample_prod,
            x='discount',
            y='profit_margin',
            color='category',
            size='sales',
            hover_name='product_name',
            labels={'discount': 'Discount (0.0 – 0.8)', 'profit_margin': 'Margin %', 'category': 'Category'},
            color_discrete_sequence=['#7e9eb8', '#9fa8da', '#8ebaa3']
        )
        fig_disc.add_hline(y=0, line_dash="dash", line_color="#d98274", opacity=0.8)
        apply_bento_chart_theme(fig_disc, height=400)
        st.plotly_chart(fig_disc, use_container_width=True)

# ----------------------------------------------------
# TAB 5: DATA EXPLORER
# ----------------------------------------------------
with tab_data:
    st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#ffffff; margin-bottom:0.5rem;'>Granular Transactional Ledger</p>", unsafe_allow_html=True)
    
    f1, f2 = st.columns([8, 4])
    with f1:
        q = st.text_input("Search Ledger (Product, Customer, State, City, ID)", "", label_visibility="collapsed")
    with f2:
        page_size = st.selectbox("Display Limit", [50, 100, 250, 500, "All Records"], index=0, label_visibility="collapsed")
        
    table_df = filtered_df.copy()
    if q:
        mask = table_df.astype(str).apply(lambda row: row.str.contains(q, case=False).any(), axis=1)
        table_df = table_df[mask]
        
    st.caption(f"Showing {len(table_df):,} of {len(filtered_df):,} filtered transactions.")
    
    if page_size == "All Records":
        st.dataframe(table_df, use_container_width=True, height=450)
    else:
        st.dataframe(table_df.head(int(page_size)), use_container_width=True, height=450)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    e1, e2, _ = st.columns([3, 3, 6])
    with e1:
        csv_bytes = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "Export Filtered Ledger (CSV)",
            data=csv_bytes,
            file_name=f"superstore_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    with e2:
        b = io.BytesIO()
        with pd.ExcelWriter(b, engine='openpyxl') as w:
            filtered_df.to_excel(w, index=False, sheet_name='Superstore Data')
        st.download_button(
            "Export Filtered Ledger (Excel)",
            data=b.getvalue(),
            file_name=f"superstore_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
