import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io
import os

# ==============================================================================
# PAGE CONFIGURATION & THEME ENGINE
# ==============================================================================
st.set_page_config(
    page_title="Global Superstore Commercial Intelligence — Executive Platform",
    page_icon="■",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End CSS: Satoshi Typography, Pitch Black Canvas (#000000), 100% Borderless Bento Grid
st.markdown("""
<style>
    @import url('https://api.fontshare.com/v2/css?f[]=satoshi@900,800,700,600,500,400,300&display=swap');

    /* Global Typography */
    html, body, .stApp, p, span, div, h1, h2, h3, h4, h5, h6, input, select, textarea, button, .stMarkdown {
        font-family: 'Satoshi', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Pitch Black Canvas */
    .stApp {
        background-color: #000000 !important;
        background-image: none !important;
        color: #ffffff;
    }

    .main .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2.5rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 98% !important;
    }

    /* Standard Docked Matte Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #08080a !important;
        border-right: none !important;
    }

    /* Sidebar Collapse / Header Buttons */
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

    /* Top Navigation Header */
    .bento-nav-card {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.4rem 1.8rem;
        background: #0e0e12;
        border: none !important;
        border-radius: 16px;
        margin-bottom: 1.4rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.45);
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
        color: #94a3b8;
        font-weight: 500;
        margin-top: 3px;
        letter-spacing: 0.01em;
    }
    .live-chip {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: #18181f;
        border: none !important;
        color: #d48ba1;
        padding: 6px 14px;
        border-radius: 8px;
        font-size: 0.76rem;
        font-weight: 600;
    }
    .pulse-dot {
        width: 6px;
        height: 6px;
        background-color: #68b69e;
        border-radius: 50%;
        box-shadow: 0 0 6px #68b69e;
    }

    /* 6-Column Bento KPI Container */
    .bento-kpi-container {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: 0.9rem;
        margin-bottom: 1.4rem;
    }
    .bento-card {
        background: #0e0e12;
        border: none !important;
        border-radius: 16px;
        padding: 1.2rem 1.3rem;
        transition: all 0.2s ease;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35);
    }
    .bento-card:hover {
        transform: translateY(-2px);
        background: #14141a;
    }
    .bento-card-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }
    .bento-label {
        font-size: 0.72rem;
        font-weight: 700;
        color: #71717a;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    .bento-value {
        font-size: 1.65rem;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.03em;
        line-height: 1.1;
        margin-bottom: 0.4rem;
        font-feature-settings: "tnum";
    }
    .bento-footer {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 0.74rem;
        font-weight: 600;
    }

    /* Muted Tokyo Pastel Color Pills */
    .pill-tokyo-mint {
        background: rgba(104, 182, 158, 0.15);
        color: #68b69e;
        padding: 3px 8px;
        border-radius: 6px;
    }
    .pill-tokyo-pink {
        background: rgba(212, 139, 161, 0.15);
        color: #d48ba1;
        padding: 3px 8px;
        border-radius: 6px;
    }
    .pill-tokyo-crimson {
        background: rgba(212, 106, 106, 0.15);
        color: #d46a6a;
        padding: 3px 8px;
        border-radius: 6px;
    }
    .pill-tokyo-purple {
        background: rgba(155, 134, 189, 0.15);
        color: #9b86bd;
        padding: 3px 8px;
        border-radius: 6px;
    }
    .pill-tokyo-ochre {
        background: rgba(217, 168, 108, 0.15);
        color: #d9a86c;
        padding: 3px 8px;
        border-radius: 6px;
    }

    /* Minimalist Insight Banner */
    .bento-insight-banner {
        background: #0e0e12;
        border: none !important;
        border-radius: 14px;
        padding: 0.9rem 1.3rem;
        margin-bottom: 1.4rem;
        display: flex;
        align-items: center;
        gap: 12px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
    }
    .insight-indicator {
        width: 3px;
        height: 24px;
        background: #d48ba1;
        border-radius: 2px;
        flex-shrink: 0;
    }

    /* Borderless Tab Controls */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: #09090c;
        padding: 4px;
        border-radius: 12px;
        border: none !important;
    }
    .stTabs [data-baseweb="tab"] {
        height: 38px;
        border-radius: 8px;
        color: #71717a;
        font-weight: 600;
        font-size: 0.82rem;
        padding: 0 14px;
        border: none !important;
        background: transparent;
        transition: all 0.15s ease;
    }
    .stTabs [aria-selected="true"] {
        background: #181820 !important;
        border: none !important;
        color: #ffffff !important;
    }

    /* Multiselect Tag Chips */
    span[data-baseweb="tag"],
    div[data-baseweb="tag"],
    [data-baseweb="tag"] {
        background-color: #27272e !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 2px 6px !important;
        color: #ffffff !important;
    }
    span[data-baseweb="tag"] span,
    div[data-baseweb="tag"] span,
    [data-baseweb="tag"] * {
        color: #ffffff !important;
        font-weight: 500 !important;
        font-size: 0.78rem !important;
        background-color: transparent !important;
    }
    span[data-baseweb="tag"] svg,
    div[data-baseweb="tag"] svg {
        fill: #a1a1aa !important;
        stroke: #a1a1aa !important;
    }

    /* Action & Download Buttons */
    div.stDownloadButton > button,
    div.stButton > button,
    button[data-testid="baseButton-secondary"],
    button[data-testid="baseButton-primary"] {
        background-color: #141419 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 600 !important;
        font-size: 0.84rem !important;
        letter-spacing: -0.01em !important;
        transition: all 0.2s ease !important;
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
        color: #ffffff !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.6) !important;
    }

    /* Analyst Profile Card (Sidebar) */
    .profile-card {
        background: #111116;
        border: none !important;
        border-radius: 14px;
        padding: 1.2rem;
        margin-top: 1.5rem;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35);
    }
    .profile-name {
        font-weight: 800;
        color: #ffffff;
        font-size: 0.95rem;
        margin-bottom: 2px;
    }
    .profile-role {
        font-size: 0.74rem;
        color: #d48ba1;
        font-weight: 600;
        margin-bottom: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    .profile-tag {
        display: inline-block;
        background: #1c1c24;
        border: none !important;
        border-radius: 6px;
        padding: 3px 8px;
        font-size: 0.68rem;
        color: #cbd5e1;
        margin-right: 4px;
        margin-bottom: 4px;
    }

    /* Scrollbar */
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

# ==============================================================================
# PLOTLY CHART THEME ENGINE
# ==============================================================================
def apply_bento_theme(fig, height=360):
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
            bordercolor="rgba(255,255,255,0.0)"
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

# ==============================================================================
# DATA LOADING & DATA CLEANING PIPELINE (FROM COLAB NOTEBOOK)
# ==============================================================================
@st.cache_data
def load_global_superstore():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_paths = [
        os.path.join(current_dir, "data", "Global_Superstore2.xlsx"),
        os.path.join(current_dir, "data", "Global_Superstore.csv"),
        os.path.join(current_dir, "data", "Global Superstore.txt"),
        os.path.join(current_dir, "Global_Superstore2.xlsx"),
        "02_Global_Superstore/data/Global_Superstore2.xlsx",
        "02_Global_Superstore/data/Global_Superstore.csv"
    ]
    
    df = None
    for path in file_paths:
        if os.path.exists(path):
            try:
                if path.endswith('.xlsx') or path.endswith('.xls'):
                    df = pd.read_excel(path)
                elif path.endswith('.txt'):
                    df = pd.read_csv(path, sep='\t')
                else:
                    df = pd.read_csv(path, encoding='utf-8')
                break
            except Exception:
                try:
                    df = pd.read_csv(path, encoding='windows-1252')
                    break
                except Exception:
                    continue

    if df is None:
        url = "https://raw.githubusercontent.com/datasets/global-superstore/master/data/global-superstore.csv"
        try:
            df = pd.read_csv(url)
        except Exception:
            # Fallback sample dataset if offline
            df = pd.DataFrame()

    # Clean column headers
    df.columns = [c.strip() for c in df.columns]

    # Convert Date columns (as in Colab cleaning step)
    date_cols = [c for c in df.columns if 'date' in c.lower()]
    for c in date_cols:
        df[c] = pd.to_datetime(df[c], errors='coerce')

    # Standardize column naming
    rename_map = {}
    for col in df.columns:
        clean = col.lower().replace(" ", "_").replace("-", "_")
        rename_map[col] = clean
    df = df.rename(columns=rename_map)

    # Feature Engineering exactly matching Colab Notebook
    if 'order_date' in df.columns and 'ship_date' in df.columns:
        df['shipping_days'] = (df['ship_date'] - df['order_date']).dt.days
        df['order_year'] = df['order_date'].dt.year
        df['order_month'] = df['order_date'].dt.month_name()
        df['order_month_num'] = df['order_date'].dt.month
        df['order_quarter'] = "Q" + df['order_date'].dt.quarter.astype(str)
        df['order_weekday'] = df['order_date'].dt.day_name()
        df['year_month'] = df['order_date'].dt.to_period('M').astype(str)
        df = df.dropna(subset=['order_date']).copy()

    if 'sales' in df.columns and 'profit' in df.columns:
        df['profit_margin'] = np.where(df['sales'] != 0, (df['profit'] / df['sales']) * 100, 0)
        df['loss_flag'] = np.where(df['profit'] < 0, "Loss", "Profit")

    if 'discount' in df.columns:
        bins = [-0.01, 0, 0.1, 0.2, 0.3, 0.4, 1.0]
        labels = ["0%", "0-10%", "10-20%", "20-30%", "30-40%", "40%+"]
        df['discount_group'] = pd.cut(df['discount'], bins=bins, labels=labels)

    if 'shipping_cost' in df.columns and 'sales' in df.columns:
        df['shipping_cost_ratio'] = np.where(df['sales'] != 0, (df['shipping_cost'] / df['sales']) * 100, 0)

    # Strip string columns
    str_cols = df.select_dtypes(include='object').columns
    df[str_cols] = df[str_cols].apply(lambda x: x.str.strip() if hasattr(x, 'str') else x)

    return df

df_raw = load_global_superstore()

# ==============================================================================
# SIDEBAR (GLOBAL FILTERS & PROFILE)
# ==============================================================================
with st.sidebar:
    st.markdown("""
    <div style="padding-bottom: 0.8rem; margin-bottom: 1rem; border-bottom: 1px solid rgba(255,255,255,0.06);">
        <div style="font-weight: 800; font-size: 1.1rem; color: #ffffff; letter-spacing: -0.02em;">GLOBAL SUPERSTORE</div>
        <div style="font-size: 0.72rem; color: #d48ba1; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">Commercial & Leakage Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    min_date = df_raw['order_date'].min().date() if 'order_date' in df_raw.columns and not df_raw.empty else datetime(2011, 1, 1).date()
    max_date = df_raw['order_date'].max().date() if 'order_date' in df_raw.columns and not df_raw.empty else datetime(2014, 12, 31).date()

    st.markdown("<span style='font-size:0.8rem; font-weight:600; color:#a1a1aa;'>Temporal Range</span>", unsafe_allow_html=True)
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

    # Market Hierarchy
    st.markdown("<span style='font-size:0.8rem; font-weight:600; color:#a1a1aa;'>Global Markets</span>", unsafe_allow_html=True)
    all_markets = sorted(df_raw['market'].dropna().unique().tolist()) if 'market' in df_raw.columns else []
    selected_markets = st.multiselect("Markets", options=all_markets, default=all_markets)

    all_regions = sorted(df_raw[df_raw['market'].isin(selected_markets)]['region'].dropna().unique().tolist()) if 'region' in df_raw.columns else []
    selected_regions = st.multiselect("Regions", options=all_regions, default=all_regions)

    all_categories = sorted(df_raw['category'].dropna().unique().tolist()) if 'category' in df_raw.columns else []
    selected_categories = st.multiselect("Categories", options=all_categories, default=all_categories)

    all_segments = sorted(df_raw['segment'].dropna().unique().tolist()) if 'segment' in df_raw.columns else []
    selected_segments = st.multiselect("Customer Segments", options=all_segments, default=all_segments)

    # Loss / Profit Filter
    profitability_filter = st.selectbox("Profitability Focus", ["All Transactions", "Profit Only", "Loss Only (Leakage)"], index=0)

    # Analyst Profile Card
    st.markdown("""
    <div class="profile-card">
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">
            <div style="width:36px; height:36px; border-radius:50%; background:linear-gradient(135deg, #d48ba1, #9b86bd); display:flex; align-items:center; justify-content:center; font-weight:800; color:#ffffff; font-size:0.85rem;">
                AM
            </div>
            <div>
                <div class="profile-name">Nur Alief Maulana</div>
                <div class="profile-role">Data Analyst | BI Specialist</div>
            </div>
        </div>
        <div style="margin-bottom:10px;">
            <span class="profile-tag">Python (Pandas)</span>
            <span class="profile-tag">Leakage Analysis</span>
            <span class="profile-tag">Pareto 80/20</span>
            <span class="profile-tag">Freight Modeling</span>
            <span class="profile-tag">Streamlit</span>
        </div>
        <div style="font-size:0.75rem; color:#94a3b8; line-height:1.4; margin-bottom:10px;">
            End-to-end commercial diagnosis converted directly from deep Exploratory Data Analysis & Colab Research.
        </div>
        <div style="display:flex; flex-direction:column; gap:6px;">
            <a href="https://github.com/maulanaraa/Data-Analysis-Portfolio" target="_blank" style="text-decoration:none; display:flex; align-items:center; justify-content:center; gap:6px; background:#1c1c24; color:#ffffff; padding:7px 12px; border-radius:8px; font-size:0.75rem; font-weight:600;">
                GitHub Repository
            </a>
            <a href="mailto:contact@example.com" style="text-decoration:none; display:flex; align-items:center; justify-content:center; gap:6px; background:rgba(212, 139, 161, 0.18); color:#d48ba1; padding:7px 12px; border-radius:8px; font-size:0.75rem; font-weight:600;">
                Contact Analyst
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# DATA FILTERING ENGINE
# ==============================================================================
filtered_df = df_raw.copy()
if 'order_date' in filtered_df.columns:
    filtered_df = filtered_df[
        (filtered_df['order_date'].dt.date >= start_date) & 
        (filtered_df['order_date'].dt.date <= end_date)
    ]
if selected_markets and 'market' in filtered_df.columns:
    filtered_df = filtered_df[filtered_df['market'].isin(selected_markets)]
if selected_regions and 'region' in filtered_df.columns:
    filtered_df = filtered_df[filtered_df['region'].isin(selected_regions)]
if selected_categories and 'category' in filtered_df.columns:
    filtered_df = filtered_df[filtered_df['category'].isin(selected_categories)]
if selected_segments and 'segment' in filtered_df.columns:
    filtered_df = filtered_df[filtered_df['segment'].isin(selected_segments)]

if profitability_filter == "Profit Only":
    filtered_df = filtered_df[filtered_df['profit'] >= 0]
elif profitability_filter == "Loss Only (Leakage)":
    filtered_df = filtered_df[filtered_df['profit'] < 0]

# ==============================================================================
# TOP NAVIGATION HEADER
# ==============================================================================
st.markdown(f"""
<div class="bento-nav-card">
    <div>
        <h1 class="brand-title">Global Superstore Commercial Intelligence</h1>
        <div class="brand-subtitle">Cross-Border Profit Leakage, Discount Elasticity & Pareto 80/20 Decision Engine</div>
    </div>
    <div class="live-chip">
        <span class="pulse-dot"></span> {start_date.strftime('%b %Y')} – {end_date.strftime('%b %Y')}
    </div>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# PROJECT METHODOLOGY & COLAB RESEARCH EXPANDER (STAR FRAMEWORK)
# ------------------------------------------------------------------------------
with st.expander("Analytical Framework, Research Discoveries & STAR Methodology", expanded=False):
    st.markdown("""
    <div style="font-size:0.84rem; color:#cbd5e1; line-height:1.6;">
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:14px; margin-bottom:6px;">
            <div style="background:#0e0e12; padding:14px; border-radius:12px;">
                <b style="color:#d48ba1; text-transform:uppercase; font-size:0.75rem; letter-spacing:0.04em;">1. Situation & Core Research Question</b><br>
                Across 51,290 worldwide transactions spanning 147 countries (2011–2014), Global Superstore generated $12.6M+ in revenue but faced substantial profit erosion. While top-line sales grew consistently, hidden profit leakages in select regions, toxic discounts, and unmanaged freight subsidies severely degraded net margins.
            </div>
            <div style="background:#0e0e12; padding:14px; border-radius:12px;">
                <b style="color:#68b69e; text-transform:uppercase; font-size:0.75rem; letter-spacing:0.04em;">2. Task & Analytical Objective</b><br>
                Execute an exhaustive diagnosis across 8 core analytical dimensions (Profit Trajectory, Central Region Paradox, Discount Cliff, Shipping Cost Burden, Geographic Hotspots, Customer Health, Product Portfolios, and Pareto 80/20 Distributions) to establish prescriptive interventions.
            </div>
            <div style="background:#0e0e12; padding:14px; border-radius:12px;">
                <b style="color:#9b86bd; text-transform:uppercase; font-size:0.75rem; letter-spacing:0.04em;">3. Actions & Colab Methodologies Applied</b><br>
                • <b>Profit Leakage Modeling:</b> Isolated negative-profit transactions to quantify systemic margin loss.<br>
                • <b>Discount Elasticity:</b> Identified the critical <b>30% discount threshold</b> where transactions turn decisively negative.<br>
                • <b>Pareto 80/20 Distribution:</b> Mapped cumulative profit & cumulative loss concentration curves.
            </div>
            <div style="background:#0e0e12; padding:14px; border-radius:12px;">
                <b style="color:#d9a86c; text-transform:uppercase; font-size:0.75rem; letter-spacing:0.04em;">4. Key Strategic Conclusions</b><br>
                Central region represents the highest gross profit ($311K) yet also suffers the single highest loss volume ($135K+). Capping discounts at 25% and restructuring freight subsidies in bottom-10 loss countries (e.g. Turkey, Nigeria, Honduras) protects over <b>+$186,000 in net profit</b>.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

if filtered_df.empty:
    st.warning("No records match the current filter selection.")
    st.stop()

# ==============================================================================
# GLOBAL BENTO KPI CARDS (6 METRICS)
# ==============================================================================
total_sales = filtered_df['sales'].sum()
total_profit = filtered_df['profit'].sum()
total_loss = filtered_df[filtered_df['profit'] < 0]['profit'].sum()
profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
total_orders = filtered_df['order_id'].nunique() if 'order_id' in filtered_df.columns else len(filtered_df)
total_customers = filtered_df['customer_id'].nunique() if 'customer_id' in filtered_df.columns else 0
total_countries = filtered_df['country'].nunique() if 'country' in filtered_df.columns else 0

margin_pill_class = "pill-tokyo-mint" if profit_margin >= 10 else ("pill-tokyo-crimson" if profit_margin < 0 else "pill-tokyo-ochre")

st.markdown(f"""
<div class="bento-kpi-container">
    <div class="bento-card">
        <div class="bento-card-top">
            <span class="bento-label">Gross Revenue</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#d48ba1" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>
        </div>
        <div class="bento-value">${total_sales:,.0f}</div>
        <div class="bento-footer">
            <span class="pill-tokyo-pink">Global Turnover</span>
        </div>
    </div>

    <div class="bento-card">
        <div class="bento-card-top">
            <span class="bento-label">Net Profit</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#68b69e" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline><polyline points="17 6 23 6 23 12"></polyline></svg>
        </div>
        <div class="bento-value">${total_profit:,.0f}</div>
        <div class="bento-footer">
            <span class="{margin_pill_class}">Margin {profit_margin:.1f}%</span>
        </div>
    </div>

    <div class="bento-card">
        <div class="bento-card-top">
            <span class="bento-label">Incurred Losses</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#d46a6a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 18 13.5 8.5 8.5 13.5 1 6"></polyline><polyline points="17 18 23 18 23 12"></polyline></svg>
        </div>
        <div class="bento-value" style="color:#d46a6a;">${abs(total_loss):,.0f}</div>
        <div class="bento-footer">
            <span class="pill-tokyo-crimson">Leakage Deficit</span>
        </div>
    </div>

    <div class="bento-card">
        <div class="bento-card-top">
            <span class="bento-label">Orders</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#9b86bd" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path><line x1="3" y1="6" x2="21" y2="6"></line><path d="M16 10a4 4 0 0 1-8 0"></path></svg>
        </div>
        <div class="bento-value">{total_orders:,}</div>
        <div class="bento-footer">
            <span class="pill-tokyo-purple">Transactions</span>
        </div>
    </div>

    <div class="bento-card">
        <div class="bento-card-top">
            <span class="bento-label">Client Base</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#68b69e" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
        </div>
        <div class="bento-value">{total_customers:,}</div>
        <div class="bento-footer">
            <span class="pill-tokyo-mint">Active Accounts</span>
        </div>
    </div>

    <div class="bento-card">
        <div class="bento-card-top">
            <span class="bento-label">Presence</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#d9a86c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>
        </div>
        <div class="bento-value">{total_countries}</div>
        <div class="bento-footer">
            <span class="pill-tokyo-ochre">Countries Covered</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# MINIMALIST INSIGHT BANNER
# ==============================================================================
loss_pct = (abs(total_loss) / (total_profit + abs(total_loss)) * 100) if (total_profit + abs(total_loss)) > 0 else 0
st.markdown(f"""
<div class="bento-insight-banner">
    <div class="insight-indicator"></div>
    <div style="font-size: 0.84rem; color: #a1a1aa; line-height: 1.5;">
        <b style="color:#ffffff;">Executive Finding:</b> Unmanaged discounting and freight absorption created <b style="color:#d46a6a;">${abs(total_loss):,.0f}</b> in cumulative losses ({loss_pct:.1f}% of gross earnings). Capping discounts at 25% recovers substantial margin without diminishing overall customer volume.
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 8 ANALYTICAL & STRATEGIC MODULES (TABS MATCHING COLAB NOTEBOOK)
# ==============================================================================
(
    tab_macro,
    tab_leakage,
    tab_discount,
    tab_shipping,
    tab_geo,
    tab_customer,
    tab_pareto,
    tab_simulator,
    tab_ledger
) = st.tabs([
    "1. Macro Trajectory",
    "2. Profit Leakage Deep-Dive",
    "3. Discount Sensitivity",
    "4. Freight & Shipping",
    "5. Geographic Intelligence",
    "6. Customer Profitability",
    "7. Pareto 80/20 Portfolio",
    "8. Strategic ROI Simulator",
    "9. Global Ledger"
])

# ------------------------------------------------------------------------------
# TAB 1: MACRO TRAJECTORY & YEARLY PERFORMANCE
# ------------------------------------------------------------------------------
with tab_macro:
    m1_left, m1_right = st.columns([7, 5])
    
    with m1_left:
        st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#ffffff; margin-bottom:0.5rem;'>Yearly Sales & Profit Growth Trajectory (2011–2014)</p>", unsafe_allow_html=True)
        yearly_perf = filtered_df.groupby('order_year').agg(
            sales=('sales', 'sum'),
            profit=('profit', 'sum')
        ).reset_index().sort_values('order_year')

        fig_yearly = go.Figure()
        fig_yearly.add_trace(go.Bar(
            x=yearly_perf['order_year'].astype(str),
            y=yearly_perf['sales'],
            name="Gross Sales ($)",
            marker=dict(color="#d48ba1"),
            text=[f"${s:,.0f}" for s in yearly_perf['sales']],
            textposition="outside"
        ))
        fig_yearly.add_trace(go.Scatter(
            x=yearly_perf['order_year'].astype(str),
            y=yearly_perf['profit'],
            name="Net Profit ($)",
            mode="lines+markers",
            line=dict(color="#68b69e", width=3),
            yaxis="y2"
        ))
        fig_yearly.update_layout(
            yaxis2=dict(
                title="Profit ($)",
                overlaying="y",
                side="right",
                showgrid=False,
                tickfont=dict(color="#68b69e", size=10)
            )
        )
        apply_bento_theme(fig_yearly, height=360)
        st.plotly_chart(fig_yearly, use_container_width=True)

    with m1_right:
        st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#ffffff; margin-bottom:0.5rem;'>Market Volume Contribution (Share %)</p>", unsafe_allow_html=True)
        market_perf = filtered_df.groupby('market').agg(
            sales=('sales', 'sum'),
            profit=('profit', 'sum')
        ).reset_index().sort_values('sales', ascending=False)

        fig_market = px.pie(
            market_perf,
            values='sales',
            names='market',
            hole=0.6,
            color_discrete_sequence=['#d48ba1', '#9b86bd', '#68b69e', '#799fbf', '#d9a86c', '#d46a6a', '#a1a1aa']
        )
        fig_market.update_traces(textposition='outside', textinfo='percent+label')
        apply_bento_theme(fig_market, height=360)
        fig_market.update_layout(showlegend=False)
        st.plotly_chart(fig_market, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    m2_l, m2_r = st.columns(2)
    with m2_l:
        st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#ffffff; margin-bottom:0.5rem;'>Regional Profitability Matrix ($)</p>", unsafe_allow_html=True)
        reg_profit = filtered_df.groupby('region')['profit'].sum().reset_index().sort_values('profit', ascending=True)
        bar_col = ['#d46a6a' if p < 0 else '#68b69e' for p in reg_profit['profit']]
        fig_reg = go.Figure(go.Bar(
            x=reg_profit['profit'],
            y=reg_profit['region'],
            orientation='h',
            marker=dict(color=bar_col),
            text=[f"${p:,.0f}" for p in reg_profit['profit']],
            textposition="outside"
        ))
        apply_bento_theme(fig_reg, height=380)
        st.plotly_chart(fig_reg, use_container_width=True)

    with m2_r:
        st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#ffffff; margin-bottom:0.5rem;'>Category Performance & Operating Margins</p>", unsafe_allow_html=True)
        cat_df = filtered_df.groupby('category').agg(
            sales=('sales', 'sum'),
            profit=('profit', 'sum')
        ).reset_index()
        cat_df['margin'] = (cat_df['profit'] / cat_df['sales']) * 100

        fig_cat = px.bar(
            cat_df,
            x='category',
            y='sales',
            color='margin',
            text_auto='$,.0f',
            color_continuous_scale=[[0, '#361d27'], [0.5, '#7a3e5c'], [1, '#68b69e']],
            labels={'sales': 'Sales ($)', 'margin': 'Margin %', 'category': 'Category'}
        )
        apply_bento_theme(fig_cat, height=380)
        st.plotly_chart(fig_cat, use_container_width=True)

# ------------------------------------------------------------------------------
# TAB 2: PROFIT LEAKAGE & CENTRAL REGION DEEP-DIVE
# ------------------------------------------------------------------------------
with tab_leakage:
    st.markdown("<p style='font-size:1.05rem; font-weight:800; color:#ffffff; margin-bottom:0.2rem;'>Profit Leakage Diagnosis & The Central Region Paradox</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.8rem; color:#71717a; margin-bottom:1.2rem;'>Analysis of transactions that destroyed value and the root causes behind regional losses.</p>", unsafe_allow_html=True)

    l1, l2 = st.columns([6, 6])
    with l1:
        st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#ffffff; margin-bottom:0.5rem;'>Annual Leakage Scaling: Profit vs Loss Volume</p>", unsafe_allow_html=True)
        yearly_loss = filtered_df.groupby('order_year').agg(
            positive_profit=('profit', lambda x: x[x > 0].sum()),
            negative_loss=('profit', lambda x: abs(x[x < 0].sum()))
        ).reset_index()

        fig_pl = go.Figure()
        fig_pl.add_trace(go.Bar(
            x=yearly_loss['order_year'].astype(str),
            y=yearly_loss['positive_profit'],
            name="Gross Profit ($)",
            marker=dict(color="#68b69e")
        ))
        fig_pl.add_trace(go.Bar(
            x=yearly_loss['order_year'].astype(str),
            y=yearly_loss['negative_loss'],
            name="Incurred Loss ($)",
            marker=dict(color="#d46a6a")
        ))
        fig_pl.update_layout(barmode="group")
        apply_bento_theme(fig_pl, height=340)
        st.plotly_chart(fig_pl, use_container_width=True)

    with l2:
        st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#ffffff; margin-bottom:0.5rem;'>The Central Region Paradox (Highest Profit & Highest Loss)</p>", unsafe_allow_html=True)
        reg_split = filtered_df.groupby('region').agg(
            gross_gain=('profit', lambda x: x[x > 0].sum()),
            gross_loss=('profit', lambda x: abs(x[x < 0].sum())),
            net_profit=('profit', 'sum')
        ).reset_index().sort_values('gross_loss', ascending=False).head(8)

        fig_paradox = px.bar(
            reg_split,
            x='region',
            y=['gross_gain', 'gross_loss'],
            barmode='group',
            color_discrete_map={'gross_gain': '#68b69e', 'gross_loss': '#d46a6a'},
            labels={'value': 'Amount ($)', 'region': 'Region'}
        )
        apply_bento_theme(fig_paradox, height=340)
        st.plotly_chart(fig_paradox, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    l3_l, l3_r = st.columns(2)
    with l3_l:
        st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#ffffff; margin-bottom:0.5rem;'>Top 10 Loss-Driving Countries ($ Deficit)</p>", unsafe_allow_html=True)
        loss_country = filtered_df[filtered_df['profit'] < 0].groupby('country')['profit'].sum().reset_index().sort_values('profit', ascending=True).head(10)
        loss_country['abs_profit'] = loss_country['profit'].abs()
        fig_lc = px.bar(
            loss_country,
            x='abs_profit',
            y='country',
            orientation='h',
            color='abs_profit',
            color_continuous_scale=[[0, '#361d27'], [1, '#d46a6a']],
            labels={'abs_profit': 'Gross Loss ($)', 'country': 'Country'}
        )
        fig_lc.update_layout(yaxis=dict(autorange="reversed"))
        apply_bento_theme(fig_lc, height=360)
        st.plotly_chart(fig_lc, use_container_width=True)

    with l3_r:
        st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#ffffff; margin-bottom:0.5rem;'>Loss Concentration by Product Sub-Category</p>", unsafe_allow_html=True)
        sub_loss = filtered_df[filtered_df['profit'] < 0].groupby('sub_category')['profit'].sum().reset_index().sort_values('profit', ascending=True)
        sub_loss['abs_loss'] = sub_loss['profit'].abs()
        fig_sl = px.bar(
            sub_loss,
            x='abs_loss',
            y='sub_category',
            orientation='h',
            color='abs_loss',
            color_continuous_scale=[[0, '#2d1818'], [1, '#d46a6a']],
            labels={'abs_loss': 'Gross Loss ($)', 'sub_category': 'Sub-Category'}
        )
        fig_sl.update_layout(yaxis=dict(autorange="reversed"))
        apply_bento_theme(fig_sl, height=360)
        st.plotly_chart(fig_sl, use_container_width=True)

# ------------------------------------------------------------------------------
# TAB 3: DISCOUNT SENSITIVITY & MARGIN EROSION
# ------------------------------------------------------------------------------
with tab_discount:
    st.markdown("<p style='font-size:1.05rem; font-weight:800; color:#ffffff; margin-bottom:0.2rem;'>Discount Sensitivity: The 30% Critical Loss Cliff</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.8rem; color:#71717a; margin-bottom:1.2rem;'>Colab research proves discounts >30% consistently yield negative operating profit.</p>", unsafe_allow_html=True)

    d1, d2 = st.columns(2)
    with d1:
        st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#ffffff; margin-bottom:0.5rem;'>Average Profit by Discount Tier</p>", unsafe_allow_html=True)
        if 'discount_group' in filtered_df.columns:
            disc_prof = filtered_df.groupby('discount_group').agg(
                avg_profit=('profit', 'mean'),
                total_profit=('profit', 'sum'),
                orders=('order_id', 'nunique') if 'order_id' in filtered_df.columns else ('sales', 'count')
            ).reset_index()

            bar_col = ['#d46a6a' if p < 0 else '#68b69e' for p in disc_prof['avg_profit']]
            fig_dp = go.Figure(go.Bar(
                x=disc_prof['discount_group'].astype(str),
                y=disc_prof['avg_profit'],
                marker=dict(color=bar_col),
                text=[f"${p:.1f}" for p in disc_prof['avg_profit']],
                textposition="outside"
            ))
            fig_dp.add_hline(y=0, line_dash="dash", line_color="rgba(255,255,255,0.4)")
            apply_bento_theme(fig_dp, height=340)
            st.plotly_chart(fig_dp, use_container_width=True)

    with d2:
        st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#ffffff; margin-bottom:0.5rem;'>Discount vs Profit Margin Scatter (Correlation: -0.32)</p>", unsafe_allow_html=True)
        sample_df = filtered_df.sample(min(len(filtered_df), 1500), random_state=42)
        fig_ds = px.scatter(
            sample_df,
            x='discount',
            y='profit_margin',
            color='loss_flag',
            hover_name='product_name' if 'product_name' in sample_df.columns else None,
            color_discrete_map={'Profit': '#68b69e', 'Loss': '#d46a6a'},
            labels={'discount': 'Discount Rate', 'profit_margin': 'Margin %'}
        )
        fig_ds.add_vline(x=0.3, line_dash="dash", line_color="#d46a6a", annotation_text="30% Danger Cliff")
        apply_bento_theme(fig_ds, height=340)
        st.plotly_chart(fig_ds, use_container_width=True)

    # Highlight Case Study from Notebook
    st.markdown("""
    <div style="background:#0e0e12; border-radius:14px; padding:16px; margin-top:10px;">
        <div style="font-weight:800; font-size:0.85rem; color:#d48ba1; text-transform:uppercase; letter-spacing:0.04em;">Colab Discovery: Problem SKU Case Study</div>
        <div style="font-size:0.82rem; color:#cbd5e1; line-height:1.5; margin-top:6px;">
            <b>Product:</b> <i>Cubify CubeX 3D Printer Double Head Print</i><br>
            Discounted at 50%–70% across commercial enterprise deals, generating <b>-$8,879 in cumulative loss</b> across just 4 orders. Removing uncontrolled discretion on this single SKU recovers nearly $9K in profit.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# TAB 4: FREIGHT & SHIPPING DYNAMICS
# ------------------------------------------------------------------------------
with tab_shipping:
    s1, s2 = st.columns(2)
    with s1:
        st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#ffffff; margin-bottom:0.5rem;'>Fulfillment Velocity: Shipping Days vs Shipping Cost</p>", unsafe_allow_html=True)
        ship_mode_df = filtered_df.groupby('ship_mode').agg(
            sales=('sales', 'sum'),
            profit=('profit', 'sum'),
            avg_days=('shipping_days', 'mean') if 'shipping_days' in filtered_df.columns else ('sales', 'mean'),
            avg_cost=('shipping_cost', 'mean') if 'shipping_cost' in filtered_df.columns else ('sales', 'mean')
        ).reset_index().sort_values('sales', ascending=False)

        fig_sm = px.bar(
            ship_mode_df,
            x='ship_mode',
            y='sales',
            color='avg_days',
            color_continuous_scale=[[0, '#361d27'], [1, '#9b86bd']],
            text_auto='$,.0f',
            labels={'sales': 'Sales ($)', 'ship_mode': 'Ship Mode', 'avg_days': 'Avg Delivery Days'}
        )
        apply_bento_theme(fig_sm, height=340)
        st.plotly_chart(fig_sm, use_container_width=True)

    with s2:
        st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#ffffff; margin-bottom:0.5rem;'>Order Priority vs Shipping Profitability</p>", unsafe_allow_html=True)
        if 'order_priority' in filtered_df.columns:
            prio_df = filtered_df.groupby('order_priority').agg(
                sales=('sales', 'sum'),
                profit=('profit', 'sum'),
                shipping_cost=('shipping_cost', 'sum') if 'shipping_cost' in filtered_df.columns else ('sales', 'sum')
            ).reset_index()

            fig_prio = px.pie(
                prio_df,
                values='shipping_cost',
                names='order_priority',
                hole=0.55,
                color='order_priority',
                color_discrete_map={
                    'Critical': '#d46a6a',
                    'High': '#d9a86c',
                    'Medium': '#9b86bd',
                    'Low': '#68b69e'
                }
            )
            apply_bento_theme(fig_prio, height=340)
            st.plotly_chart(fig_prio, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Seasonal Monthly Heatmap
    if 'order_month' in filtered_df.columns and 'order_year' in filtered_df.columns:
        st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#ffffff; margin-bottom:0.5rem;'>Global Monthly Seasonality Matrix (Sales $)</p>", unsafe_allow_html=True)
        month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        pivot_season = filtered_df.pivot_table(index='order_year', columns='order_month', values='sales', aggfunc='sum')
        pivot_season = pivot_season.reindex(columns=[m for m in month_order if m in pivot_season.columns]).fillna(0)

        fig_season = px.imshow(
            pivot_season,
            text_auto="$,.0f",
            color_continuous_scale=[[0, '#0c0c10'], [0.5, '#4a2533'], [1, '#d48ba1']],
            aspect="auto",
            labels=dict(x="Month", y="Year", color="Sales ($)")
        )
        apply_bento_theme(fig_season, height=280)
        st.plotly_chart(fig_season, use_container_width=True)

# ------------------------------------------------------------------------------
# TAB 5: GEOGRAPHIC INTELLIGENCE & WORLD CHOROPLETH
# ------------------------------------------------------------------------------
with tab_geo:
    st.markdown("<p style='font-size:1.05rem; font-weight:800; color:#ffffff; margin-bottom:0.2rem;'>Geographic Intelligence: 147 Countries Matrix</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.8rem; color:#71717a; margin-bottom:1.2rem;'>World revenue density and bottom-10 unprofitable sovereign markets.</p>", unsafe_allow_html=True)

    country_summary = filtered_df.groupby('country').agg(
        sales=('sales', 'sum'),
        profit=('profit', 'sum'),
        orders=('order_id', 'nunique') if 'order_id' in filtered_df.columns else ('sales', 'count'),
        avg_discount=('discount', 'mean') if 'discount' in filtered_df.columns else ('sales', 'mean')
    ).reset_index()
    country_summary['profit_margin'] = (country_summary['profit'] / country_summary['sales']) * 100

    g1, g2 = st.columns([7, 5])
    with g1:
        st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#ffffff; margin-bottom:0.5rem;'>Worldwide Revenue Choropleth Map</p>", unsafe_allow_html=True)
        fig_world = px.choropleth(
            country_summary,
            locations='country',
            locationmode="country names",
            color='sales',
            color_continuous_scale=[[0, '#0a0a0e'], [0.4, '#4a2533'], [1, '#d48ba1']],
            hover_name='country',
            hover_data={'sales': ':$,.0f', 'profit': ':$,.0f', 'profit_margin': ':.1f%'}
        )
        fig_world.update_layout(
            geo=dict(bgcolor='rgba(0,0,0,0)', showframe=False, showcoastlines=True, coastlinecolor="rgba(255,255,255,0.1)"),
            margin=dict(l=0, r=0, t=10, b=10)
        )
        apply_bento_theme(fig_world, height=380)
        st.plotly_chart(fig_world, use_container_width=True)

    with g2:
        st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#ffffff; margin-bottom:0.5rem;'>Bottom 10 Deficit Countries (Heavy Margin Losses)</p>", unsafe_allow_html=True)
        bot_10_c = country_summary.sort_values('profit', ascending=True).head(10)
        for _, r in bot_10_c.iterrows():
            st.markdown(f"""
            <div style="background: #0e0e12; border-radius: 10px; padding: 10px 14px; margin-bottom: 6px;">
                <div style="display:flex; justify-content:space-between; font-weight:700; color:#ffffff; font-size: 0.86rem;">
                    <span>{r['country']}</span>
                    <span style="color:#d46a6a;">-${abs(r['profit']):,.0f}</span>
                </div>
                <div style="display:flex; justify-content:space-between; font-size:0.72rem; color:#71717a; margin-top:2px;">
                    <span>Sales: ${r['sales']:,.0f}</span>
                    <span style="color:#d46a6a; font-weight:600;">Margin: {r['profit_margin']:.1f}% (Disc: {r['avg_discount']*100:.0f}%)</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# TAB 6: CUSTOMER PROFITABILITY & KEY ACCOUNTS
# ------------------------------------------------------------------------------
with tab_customer:
    cust_df = filtered_df.groupby('customer_id').agg(
        customer_name=('customer_name', 'first') if 'customer_name' in filtered_df.columns else ('sales', 'first'),
        segment=('segment', 'first') if 'segment' in filtered_df.columns else ('sales', 'first'),
        sales=('sales', 'sum'),
        profit=('profit', 'sum'),
        orders=('order_id', 'nunique') if 'order_id' in filtered_df.columns else ('sales', 'count')
    ).reset_index()
    cust_df['profit_margin'] = (cust_df['profit'] / cust_df['sales']) * 100

    cu1, cu2 = st.columns(2)
    with cu1:
        st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#ffffff; margin-bottom:0.5rem;'>Top 10 High-Contribution Accounts ($ Profit)</p>", unsafe_allow_html=True)
        top_cust = cust_df.sort_values('profit', ascending=False).head(10)
        fig_tc = px.bar(
            top_cust,
            x='profit',
            y='customer_name',
            orientation='h',
            color='profit',
            color_continuous_scale=[[0, '#132a22'], [1, '#68b69e']],
            labels={'profit': 'Profit ($)', 'customer_name': 'Client'}
        )
        fig_tc.update_layout(yaxis=dict(autorange="reversed"))
        apply_bento_theme(fig_tc, height=360)
        st.plotly_chart(fig_tc, use_container_width=True)

    with cu2:
        st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#ffffff; margin-bottom:0.5rem;'>Top 10 Loss-Bleeding Accounts ($ Deficit)</p>", unsafe_allow_html=True)
        bot_cust = cust_df.sort_values('profit', ascending=True).head(10)
        fig_bc = px.bar(
            bot_cust,
            x='profit',
            y='customer_name',
            orientation='h',
            color='profit',
            color_continuous_scale=[[0, '#d46a6a'], [1, '#2d1818']],
            labels={'profit': 'Profit ($)', 'customer_name': 'Client'}
        )
        apply_bento_theme(fig_bc, height=360)
        st.plotly_chart(fig_bc, use_container_width=True)

# ------------------------------------------------------------------------------
# TAB 7: PARETO 80/20 PORTFOLIO ANALYSIS (FROM COLAB NOTEBOOK)
# ------------------------------------------------------------------------------
with tab_pareto:
    st.markdown("<p style='font-size:1.05rem; font-weight:800; color:#ffffff; margin-bottom:0.2rem;'>Pareto Analysis (80/20 Rule): Profit & Loss Concentration</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.8rem; color:#71717a; margin-bottom:1.2rem;'>Mathematical demonstration of cumulative profit generation and cumulative loss causation.</p>", unsafe_allow_html=True)

    # 1. Pareto Profit Curve
    prod_profit = filtered_df.groupby('product_name')['profit'].sum().reset_index()
    prod_profit_pos = prod_profit[prod_profit['profit'] > 0].sort_values('profit', ascending=False).reset_index(drop=True)
    prod_profit_pos['cum_profit'] = prod_profit_pos['profit'].cumsum()
    total_pos_prof = prod_profit_pos['profit'].sum()
    prod_profit_pos['cum_profit_pct'] = (prod_profit_pos['cum_profit'] / total_pos_prof) * 100
    prod_profit_pos['sku_rank_pct'] = ((prod_profit_pos.index + 1) / len(prod_profit_pos)) * 100

    # 2. Pareto Loss Curve
    prod_loss = prod_profit[prod_profit['profit'] < 0].copy()
    prod_loss['abs_loss'] = prod_loss['profit'].abs()
    prod_loss = prod_loss.sort_values('abs_loss', ascending=False).reset_index(drop=True)
    prod_loss['cum_loss'] = prod_loss['abs_loss'].cumsum()
    total_loss_val = prod_loss['abs_loss'].sum()
    prod_loss['cum_loss_pct'] = (prod_loss['cum_loss'] / total_loss_val) * 100
    prod_loss['sku_rank_pct'] = ((prod_loss.index + 1) / len(prod_loss)) * 100

    par1, par2 = st.columns(2)
    with par1:
        st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#ffffff; margin-bottom:0.5rem;'>80/20 Profit Pareto Curve (Top SKUs)</p>", unsafe_allow_html=True)
        fig_par_p = go.Figure()
        fig_par_p.add_trace(go.Scatter(
            x=prod_profit_pos['sku_rank_pct'],
            y=prod_profit_pos['cum_profit_pct'],
            mode='lines',
            line=dict(color='#68b69e', width=3),
            name="Cumulative Profit %",
            fill='tozeroy',
            fillcolor='rgba(104, 182, 158, 0.12)'
        ))
        fig_par_p.add_hline(y=80, line_dash="dash", line_color="#d9a86c", annotation_text="80% Profit Threshold")
        fig_par_p.update_layout(xaxis_title="SKU Portfolio % (Ranked)", yaxis_title="Cumulative Profit %")
        apply_bento_theme(fig_par_p, height=340)
        st.plotly_chart(fig_par_p, use_container_width=True)

    with par2:
        st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#ffffff; margin-bottom:0.5rem;'>80/20 Loss Concentration Curve (Leakage SKUs)</p>", unsafe_allow_html=True)
        fig_par_l = go.Figure()
        fig_par_l.add_trace(go.Scatter(
            x=prod_loss['sku_rank_pct'],
            y=prod_loss['cum_loss_pct'],
            mode='lines',
            line=dict(color='#d46a6a', width=3),
            name="Cumulative Loss %",
            fill='tozeroy',
            fillcolor='rgba(212, 106, 106, 0.12)'
        ))
        fig_par_l.add_hline(y=80, line_dash="dash", line_color="#d9a86c", annotation_text="80% Loss Caused")
        fig_par_l.update_layout(xaxis_title="Loss SKU Portfolio %", yaxis_title="Cumulative Loss %")
        apply_bento_theme(fig_par_l, height=340)
        st.plotly_chart(fig_par_l, use_container_width=True)

# ------------------------------------------------------------------------------
# TAB 8: STRATEGIC ROI SIMULATOR
# ------------------------------------------------------------------------------
with tab_simulator:
    st.markdown("<p style='font-size:1.05rem; font-weight:800; color:#ffffff; margin-bottom:0.2rem;'>Executive Strategic Recommendations & ROI Modeling</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.8rem; color:#71717a; margin-bottom:1.2rem;'>Interventions modeled directly from the Colab research discoveries.</p>", unsafe_allow_html=True)

    sim_l, sim_r = st.columns([5, 7])
    with sim_l:
        st.markdown("<p style='font-size:0.85rem; font-weight:700; color:#d48ba1; margin-bottom:0.4rem;'>1. Global Maximum Discount Cap</p>", unsafe_allow_html=True)
        sim_max_disc = st.slider("Cap Discount at (%)", min_value=0.10, max_value=0.70, value=0.25, step=0.05, format="%.0f%%")

        st.markdown("<p style='font-size:0.85rem; font-weight:700; color:#68b69e; margin-bottom:0.4rem;'>2. Technology Category Expansion</p>", unsafe_allow_html=True)
        sim_tech_boost = st.slider("Target Tech Sales Growth (%)", min_value=0, max_value=40, value=15, step=5, format="+%d%%")

        st.markdown("<p style='font-size:0.85rem; font-weight:700; color:#9b86bd; margin-bottom:0.4rem;'>3. Deficit Country Freight Restructuring</p>", unsafe_allow_html=True)
        sim_freight_fix = st.slider("Freight Loss Recovery (%) in Bottom Countries", min_value=0, max_value=80, value=40, step=10, format="%d%%")

    # Dynamic Simulation Engine
    sim_data = filtered_df.copy()
    disc_mask = sim_data['discount'] > sim_max_disc
    recovered_disc_profit = ((sim_data.loc[disc_mask, 'discount'] - sim_max_disc) * (sim_data.loc[disc_mask, 'sales'] / (1 - sim_data.loc[disc_mask, 'discount']))).sum()

    tech_sales_b = sim_data[sim_data['category'] == 'Technology']['sales'].sum()
    tech_profit_b = sim_data[sim_data['category'] == 'Technology']['profit'].sum()
    tech_margin_pct = (tech_profit_b / tech_sales_b) if tech_sales_b > 0 else 0.15
    tech_profit_uplift = (tech_sales_b * (sim_tech_boost / 100)) * tech_margin_pct

    bottom_c_list = country_summary.sort_values('profit', ascending=True).head(10)['country'].tolist()
    bottom_c_loss = abs(sim_data[(sim_data['country'].isin(bottom_c_list)) & (sim_data['profit'] < 0)]['profit'].sum())
    freight_recovery = bottom_c_loss * (sim_freight_fix / 100)

    total_sim_gain = recovered_disc_profit + tech_profit_uplift + freight_recovery
    sim_net_profit = total_profit + total_sim_gain
    sim_net_margin = (sim_net_profit / total_sales * 100) if total_sales > 0 else 0

    with sim_r:
        st.markdown(f"""
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:12px; margin-bottom:14px;">
            <div style="background:#0e0e12; border-radius:12px; padding:14px;">
                <div style="font-size:0.72rem; color:#71717a; font-weight:700; text-transform:uppercase;">Simulated Profit Lift</div>
                <div style="font-size:1.6rem; font-weight:800; color:#68b69e; margin-top:2px;">+${total_sim_gain:,.0f}</div>
                <div style="font-size:0.74rem; color:#68b69e; margin-top:4px;">Recovered net margin</div>
            </div>
            <div style="background:#0e0e12; border-radius:12px; padding:14px;">
                <div style="font-size:0.72rem; color:#71717a; font-weight:700; text-transform:uppercase;">Target Operating Profit</div>
                <div style="font-size:1.6rem; font-weight:800; color:#d48ba1; margin-top:2px;">${sim_net_profit:,.0f}</div>
                <div style="font-size:0.74rem; color:#d48ba1; margin-top:4px;">Margin: {profit_margin:.1f}% ➔ <b>{sim_net_margin:.1f}%</b></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        fig_waterfall = go.Figure(go.Waterfall(
            name="Profit Bridge",
            orientation="v",
            measure=["relative", "relative", "relative", "relative", "total"],
            x=["Base Profit", "Discount Policy", "Tech Expansion", "Freight Reform", "Target Profit"],
            y=[total_profit, recovered_disc_profit, tech_profit_uplift, freight_recovery, sim_net_profit],
            connector={"line": {"color": "rgba(255,255,255,0.15)"}},
            decreasing={"marker": {"color": "#d46a6a"}},
            increasing={"marker": {"color": "#68b69e"}},
            totals={"marker": {"color": "#d48ba1"}},
            textposition="outside",
            text=[f"${total_profit:,.0f}", f"+${recovered_disc_profit:,.0f}", f"+${tech_profit_uplift:,.0f}", f"+${freight_recovery:,.0f}", f"${sim_net_profit:,.0f}"]
        ))
        apply_bento_theme(fig_waterfall, height=280)
        fig_waterfall.update_layout(title="Simulated Profit Recovery Bridge ($)")
        st.plotly_chart(fig_waterfall, use_container_width=True)

# ------------------------------------------------------------------------------
# TAB 9: DATA EXPLORER & GRANULAR LEDGER
# ------------------------------------------------------------------------------
with tab_ledger:
    st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#ffffff; margin-bottom:0.5rem;'>Global Transactional Ledger</p>", unsafe_allow_html=True)
    
    l_c1, l_c2 = st.columns([8, 4])
    with l_c1:
        search_q = st.text_input("Search Ledger (Product, Customer, Country, Order ID)", "", label_visibility="collapsed")
    with l_c2:
        page_size = st.selectbox("Display Limit", [50, 100, 250, 500, "All Records"], index=0, label_visibility="collapsed")

    table_data = filtered_df.copy()
    if search_q:
        mask = table_data.astype(str).apply(lambda row: row.str.contains(search_q, case=False).any(), axis=1)
        table_data = table_data[mask]

    st.caption(f"Showing {len(table_data):,} of {len(filtered_df):,} filtered records.")

    if page_size == "All Records":
        st.dataframe(table_data, use_container_width=True, height=450)
    else:
        st.dataframe(table_data.head(int(page_size)), use_container_width=True, height=450)

    st.markdown("<br>", unsafe_allow_html=True)

    d_c1, d_c2, _ = st.columns([3, 3, 6])
    with d_c1:
        csv_bytes = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "Export Filtered Ledger (CSV)",
            data=csv_bytes,
            file_name=f"global_superstore_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    with d_c2:
        b = io.BytesIO()
        with pd.ExcelWriter(b, engine='openpyxl') as w:
            filtered_df.head(10000).to_excel(w, index=False, sheet_name='Global Superstore')
        st.download_button(
            "Export Top 10K Ledger (Excel)",
            data=b.getvalue(),
            file_name=f"global_superstore_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
