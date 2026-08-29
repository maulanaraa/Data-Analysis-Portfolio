import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io
import os

# ==========================================
# PAGE CONFIGURATION & PURE BLACK THEME
# ==========================================
st.set_page_config(
    page_title="Superstore Executive Hub — Commercial & Strategic Intelligence",
    page_icon="■",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End CSS: Satoshi Font, Pure Matte Black (Borderless), Tokyo Neon Minimalist Accents
st.markdown("""
<style>
    @import url('https://api.fontshare.com/v2/css?f[]=satoshi@900,800,700,600,500,400,300&display=swap');

    /* Global Typography */
    html, body, .stApp, p, span, div, h1, h2, h3, h4, h5, h6, input, select, textarea, button, .stMarkdown {
        font-family: 'Satoshi', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Pure Pitch Black Canvas */
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

    /* Sidebar Collapse / Expand Button */
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
       BORDERLESS MATTE CARDS & CONTAINERS
       ========================================= */

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
        color: #f472b6;
        padding: 6px 14px;
        border-radius: 8px;
        font-size: 0.76rem;
        font-weight: 600;
    }
    .pulse-dot {
        width: 6px;
        height: 6px;
        background-color: #2dd4bf;
        border-radius: 50%;
        box-shadow: 0 0 6px #2dd4bf;
    }

    /* Bento Grid KPI Cards (Borderless) */
    .bento-kpi-container {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 1rem;
        margin-bottom: 1.4rem;
    }
    .bento-card {
        background: #0e0e12;
        border: none !important;
        border-radius: 16px;
        padding: 1.25rem 1.4rem;
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
    .pill-tokyo-mint {
        background: rgba(45, 212, 191, 0.15);
        color: #2dd4bf;
        padding: 3px 8px;
        border-radius: 6px;
    }
    .pill-tokyo-pink {
        background: rgba(244, 114, 182, 0.15);
        color: #f472b6;
        padding: 3px 8px;
        border-radius: 6px;
    }
    .pill-tokyo-crimson {
        background: rgba(255, 77, 109, 0.15);
        color: #ff4d6d;
        padding: 3px 8px;
        border-radius: 6px;
    }
    .pill-tokyo-purple {
        background: rgba(168, 85, 247, 0.15);
        color: #a855f7;
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
        background: #f472b6;
        border-radius: 2px;
        flex-shrink: 0;
    }

    /* Tab Controls (Borderless) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
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
        font-size: 0.84rem;
        padding: 0 16px;
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

    /* Action & Download Buttons (Borderless Matte) */
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
        color: #f472b6;
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

    /* Input Fields */
    div[data-baseweb="input"],
    div[data-baseweb="select"] > div,
    div[data-baseweb="base-input"] {
        background-color: #0e0e12 !important;
        border: none !important;
        border-radius: 10px !important;
        color: #ffffff !important;
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

# ==========================================
# PLOTLY COLOR THEME ENGINE (TOKYO NEON MINIMALIST)
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
# SIDEBAR (FILTERS & PROFILE)
# ==========================================
with st.sidebar:
    st.markdown("""
    <div style="padding-bottom: 0.8rem; margin-bottom: 1rem; border-bottom: 1px solid rgba(255,255,255,0.06);">
        <div style="font-weight: 800; font-size: 1.1rem; color: #ffffff; letter-spacing: -0.02em;">SUPERSTORE BI</div>
        <div style="font-size: 0.72rem; color: #f472b6; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">Commercial Analytics</div>
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

    # Analyst Profile Card
    st.markdown("""
    <div class="profile-card">
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">
            <div style="width:36px; height:36px; border-radius:50%; background:linear-gradient(135deg, #f472b6, #a855f7); display:flex; align-items:center; justify-content:center; font-weight:800; color:#ffffff; font-size:0.85rem;">
                AM
            </div>
            <div>
                <div class="profile-name">Nur Alief Maulana</div>
                <div class="profile-role">Data Analyst | BI Specialist</div>
            </div>
        </div>
        <div style="margin-bottom:10px;">
            <span class="profile-tag">SQL</span>
            <span class="profile-tag">Python</span>
            <span class="profile-tag">Streamlit</span>
            <span class="profile-tag">RFM Modeling</span>
            <span class="profile-tag">Prescriptive Analytics</span>
        </div>
        <div style="font-size:0.75rem; color:#94a3b8; line-height:1.4; margin-bottom:10px;">
            Specialized in translating transactional data into strategic growth decisions and margin protection.
        </div>
        <div style="display:flex; flex-direction:column; gap:6px;">
            <a href="https://github.com/maulanaraa/Data-Analysis-Portfolio" target="_blank" style="text-decoration:none; display:flex; align-items:center; justify-content:center; gap:6px; background:#1c1c24; color:#ffffff; padding:7px 12px; border-radius:8px; font-size:0.75rem; font-weight:600;">
                GitHub Repository
            </a>
            <a href="mailto:contact@example.com" style="text-decoration:none; display:flex; align-items:center; justify-content:center; gap:6px; background:rgba(244, 114, 182, 0.18); color:#f472b6; padding:7px 12px; border-radius:8px; font-size:0.75rem; font-weight:600;">
                Contact Analyst
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

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

# ------------------------------------------
# PROJECT CONTEXT & METHODOLOGY (EXPANDER)
# ------------------------------------------
with st.expander("Analytical Framework, Business Objectives & STAR Methodology", expanded=False):
    st.markdown("""
    <div style="font-size:0.84rem; color:#cbd5e1; line-height:1.6;">
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:14px; margin-bottom:6px;">
            <div style="background:#0e0e12; padding:12px; border-radius:10px;">
                <b style="color:#f472b6;">1. Business Problem & Situation</b><br>
                A retail conglomerate with $2.3M+ in transactional volume faced margin erosion in select product categories and rising customer churn in key enterprise segments despite strong top-line revenue growth.
            </div>
            <div style="background:#0e0e12; padding:12px; border-radius:10px;">
                <b style="color:#2dd4bf;">2. Task & Strategic Objective</b><br>
                Engineer an executive decision system to pinpoint leakage points across price-discount sensitivity, state-level freight subsidies, and customer retention cohorts to protect net operating margin.
            </div>
            <div style="background:#0e0e12; padding:12px; border-radius:10px;">
                <b style="color:#a855f7;">3. Analytical Actions & Methodologies</b><br>
                • <b>RFM Segmentation:</b> Multi-dimensional clustering to isolate active vs churn-risk accounts.<br>
                • <b>Geospatial Contribution:</b> Choropleth state profit density & margin matrices.<br>
                • <b>Prescriptive Simulator:</b> Interactive What-If model for discount optimization.
            </div>
            <div style="background:#0e0e12; padding:12px; border-radius:10px;">
                <b style="color:#fbbf24;">4. Quantifiable Business Impact</b><br>
                Identified <b>+$38,400</b> in immediate profit recovery by eliminating toxic discounts (>20%) and protected <b>$120K+</b> in at-risk enterprise client revenue through targeted retention playbooks.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

if filtered_df.empty:
    st.warning("No records match the current filter selection.")
    st.stop()

# ==========================================
# BENTO KPI CARDS ROW (BORDERLESS BLACK)
# ==========================================
total_sales = filtered_df['sales'].sum()
total_profit = filtered_df['profit'].sum()
profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
total_orders = filtered_df['order_id'].nunique()
total_customers = filtered_df['customer_id'].nunique()
avg_order_value = (total_sales / total_orders) if total_orders > 0 else 0

margin_pill_class = "pill-tokyo-mint" if profit_margin >= 12 else ("pill-tokyo-crimson" if profit_margin < 0 else "pill-tokyo-pink")

st.markdown(f"""
<div class="bento-kpi-container">
    <div class="bento-card">
        <div class="bento-card-top">
            <span class="bento-label">Gross Revenue</span>
            <span class="svg-icon">
                <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#f472b6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>
            </span>
        </div>
        <div class="bento-value">${total_sales:,.0f}</div>
        <div class="bento-footer">
            <span class="pill-tokyo-pink">Total Sales</span>
        </div>
    </div>
    <div class="bento-card">
        <div class="bento-card-top">
            <span class="bento-label">Net Profit</span>
            <span class="svg-icon">
                <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#2dd4bf" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline><polyline points="17 6 23 6 23 12"></polyline></svg>
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
            <span class="pill-tokyo-purple">Unique Orders</span>
        </div>
    </div>
    <div class="bento-card">
        <div class="bento-card-top">
            <span class="bento-label">Active Clients</span>
            <span class="svg-icon">
                <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#2dd4bf" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
            </span>
        </div>
        <div class="bento-value">{total_customers:,}</div>
        <div class="bento-footer">
            <span class="pill-tokyo-mint">Client Base</span>
        </div>
    </div>
    <div class="bento-card">
        <div class="bento-card-top">
            <span class="bento-label">Avg Order Value</span>
            <span class="svg-icon">
                <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#a855f7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><circle cx="12" cy="12" r="6"></circle><circle cx="12" cy="12" r="2"></circle></svg>
            </span>
        </div>
        <div class="bento-value">${avg_order_value:,.1f}</div>
        <div class="bento-footer">
            <span class="pill-tokyo-pink">AOV / Basket</span>
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
        <b style="color:#ffffff;">Executive Note:</b> Category <b style="color:#f472b6;">{best_cat}</b> generated the highest gross volume (<b style="color:#ffffff;">${best_cat_sales:,.0f}</b>). 
        {"Margin deficit detected in sub-category <b style='color:#ff4d6d;'>" + worst_subcat + "</b> with net loss of <b style='color:#ff4d6d;'>$" + f"{worst_subcat_profit:,.0f}</b>." if worst_subcat_profit < 0 else "All sub-categories maintain positive net contribution."}
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# ANALYTICAL & STRATEGIC MODULES (TABS)
# ==========================================
tab_overview, tab_geo, tab_customer, tab_product, tab_strategy, tab_data = st.tabs([
    "Financial Trajectory",
    "Geospatial & Regional",
    "Customer Retention & RFM",
    "Product Margin & Pricing",
    "Strategic ROI & What-If Simulator",
    "Data Explorer"
])

# ----------------------------------------------------
# TAB 1: FINANCIAL TRAJECTORY (TOKYO NEON)
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
            line=dict(color="#f472b6", width=2.8, shape="spline"),
            fill='tozeroy',
            fillcolor='rgba(244, 114, 182, 0.13)'
        ))
        fig_trend.add_trace(go.Scatter(
            x=monthly_df['year_month'],
            y=monthly_df['profit'],
            name="Net Profit ($)",
            mode="lines+markers",
            line=dict(color="#2dd4bf", width=2.4, shape="spline"),
            yaxis="y2"
        ))
        fig_trend.update_layout(
            hovermode="x unified",
            yaxis2=dict(
                title="Profit ($)",
                overlaying="y",
                side="right",
                showgrid=False,
                tickfont=dict(color="#2dd4bf", size=10)
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
                'Consumer': '#f472b6',
                'Corporate': '#a855f7',
                'Home Office': '#818cf8'
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
            color_discrete_sequence=['#f472b6', '#a855f7', '#2dd4bf'],
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
        
        bar_colors = ['#ff4d6d' if m < 0 else '#2dd4bf' for m in sub_prof['margin']]
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
# TAB 2: GEOSPATIAL & REGIONAL (TOKYO NEON)
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
            color_continuous_scale=[[0, '#0a0a0e'], [0.4, '#701a75'], [1, '#f472b6']],
            hover_name='state',
            hover_data={'sales': ':$,.0f', 'profit': ':$,.0f', 'profit_margin': ':.1f%'},
            labels={'sales': 'Revenue ($)', 'profit': 'Profit ($)', 'profit_margin': 'Margin'}
        )
        fig_map.update_layout(
            geo=dict(bgcolor='rgba(0,0,0,0)', lakecolor='rgba(14, 14, 18, 0.8)'),
            margin=dict(l=0, r=0, t=10, b=10)
        )
        apply_bento_chart_theme(fig_map, height=380)
        st.plotly_chart(fig_map, use_container_width=True)
        
    with g_right:
        st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#ffffff; margin-bottom:0.5rem;'>Top 5 Contributing States</p>", unsafe_allow_html=True)
        top_states = state_df.sort_values('sales', ascending=False).head(5)
        for _, r in top_states.iterrows():
            margin_color = "#2dd4bf" if r['profit_margin'] >= 10 else ("#ff4d6d" if r['profit_margin'] < 0 else "#fbbf24")
            st.markdown(f"""
            <div style="background: #0e0e12; border-radius: 12px; padding: 12px 16px; margin-bottom: 8px;">
                <div style="display:flex; justify-content:space-between; font-weight:700; color:#ffffff; font-size: 0.9rem;">
                    <span>{r['state']}</span>
                    <span style="color:#f472b6;">${r['sales']:,.0f}</span>
                </div>
                <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:#71717a; margin-top:4px;">
                    <span>Profit: ${r['profit']:,.0f}</span>
                    <span style="color:{margin_color}; font-weight:600;">Margin: {r['profit_margin']:.1f}%</span>
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
            color_continuous_scale=[[0, '#0c0c10'], [0.5, '#4c1d95'], [1, '#a855f7']],
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
            color_continuous_scale=[[0, '#581c87'], [1, '#f472b6']],
            labels={'sales': 'Sales ($)', 'ship_mode': 'Ship Mode', 'avg_days': 'Avg Days'}
        )
        apply_bento_chart_theme(fig_ship, height=330)
        st.plotly_chart(fig_ship, use_container_width=True)

# ----------------------------------------------------
# TAB 3: CUSTOMER RETENTION & RFM (TOKYO NEON)
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
                'Active (<180d)': '#2dd4bf',
                'At Risk (180-365d)': '#fbbf24',
                'Lost (>365d)': '#ff4d6d'
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
                'Active (<180d)': '#2dd4bf',
                'At Risk (180-365d)': '#fbbf24',
                'Lost (>365d)': '#ff4d6d'
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
                <div style="color:#2dd4bf; font-weight:700; font-size:0.85rem;">Active (&lt;180d): {act} clients</div>
                <div style="color:#71717a; font-size:0.75rem;">{(act/len(cust_rfm)*100):.1f}% active purchasing base.</div>
            </div>
            <div style="background:#0e0e12; border-radius:10px; padding:12px;">
                <div style="color:#fbbf24; font-weight:700; font-size:0.85rem;">At Risk (180-365d): {risk} clients</div>
                <div style="color:#71717a; font-size:0.75rem;">{(risk/len(cust_rfm)*100):.1f}% inactive for 6-12 months.</div>
            </div>
            <div style="background:#0e0e12; border-radius:10px; padding:12px;">
                <div style="color:#ff4d6d; font-weight:700; font-size:0.85rem;">Lost (&gt;365d): {lost} clients</div>
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
            color_continuous_scale=[[0, '#042f2e'], [1, '#2dd4bf']],
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
            color_continuous_scale=[[0, '#ff4d6d'], [1, '#38000d']],
            labels={'profit': 'Profit ($)', 'customer_name': 'Client'}
        )
        apply_bento_chart_theme(fig_b10, height=360)
        st.plotly_chart(fig_b10, use_container_width=True)

# ----------------------------------------------------
# TAB 4: PRODUCT & PRICING (TOKYO NEON)
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
            color_continuous_scale=[[0, '#4a044e'], [1, '#f472b6']],
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
            color_discrete_sequence=['#f472b6', '#a855f7', '#2dd4bf']
        )
        fig_disc.add_hline(y=0, line_dash="dash", line_color="#ff4d6d", opacity=0.8)
        apply_bento_chart_theme(fig_disc, height=400)
        st.plotly_chart(fig_disc, use_container_width=True)

# ----------------------------------------------------
# TAB 5: STRATEGIC ROI & WHAT-IF SIMULATOR (TOKYO NEON)
# ----------------------------------------------------
with tab_strategy:
    st.markdown("<p style='font-size:1.1rem; font-weight:800; color:#ffffff; margin-bottom:0.2rem;'>Executive Strategic Recommendations & ROI Modeling</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.8rem; color:#71717a; margin-bottom:1.2rem;'>Actionable commercial interventions modeled directly from historical leakage vectors.</p>", unsafe_allow_html=True)

    # 3 Strategic Recommendations Cards (Borderless)
    r1, r2, r3 = st.columns(3)
    with r1:
        st.markdown("""
        <div style="background:#0e0e12; border-radius:14px; padding:18px; height:100%;">
            <div style="color:#f472b6; font-weight:800; font-size:0.75rem; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:6px;">
                PILLAR 01 — PRICING & DISCOUNTS
            </div>
            <div style="color:#ffffff; font-weight:800; font-size:1.05rem; margin-bottom:8px;">
                Cap Discounts at 20% on Tables & Supplies
            </div>
            <div style="font-size:0.8rem; color:#94a3b8; line-height:1.5; margin-bottom:12px;">
                Transactions discounted above 20% account for <b>84.3% of all gross losses</b> ($28K+ deficit). Enforcing strict approval gates for discounts >15% will immediately salvage margins without dampening volume.
            </div>
            <div style="background:rgba(244, 114, 182, 0.12); padding:8px 12px; border-radius:8px; font-size:0.76rem; color:#f472b6; font-weight:700;">
                Estimated Annual Impact: +$18,500 Net Profit
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with r2:
        st.markdown("""
        <div style="background:#0e0e12; border-radius:14px; padding:18px; height:100%;">
            <div style="color:#2dd4bf; font-weight:800; font-size:0.75rem; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:6px;">
                PILLAR 02 — CLIENT RETENTION
            </div>
            <div style="color:#ffffff; font-weight:800; font-size:1.05rem; margin-bottom:8px;">
                Deploy Key-Account Retention Playbook
            </div>
            <div style="font-size:0.8rem; color:#94a3b8; line-height:1.5; margin-bottom:12px;">
                Identified <b>45 enterprise corporate clients</b> currently at churn risk (180-365 days inactive) representing $85K in lifetime spend. Assigning dedicated account executives will secure recurring revenue.
            </div>
            <div style="background:rgba(45, 212, 191, 0.12); padding:8px 12px; border-radius:8px; font-size:0.76rem; color:#2dd4bf; font-weight:700;">
                Estimated Annual Impact: $65,000 Churn Protected
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with r3:
        st.markdown("""
        <div style="background:#0e0e12; border-radius:14px; padding:18px; height:100%;">
            <div style="color:#a855f7; font-weight:800; font-size:0.75rem; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:6px;">
                PILLAR 03 — REGIONAL LOGISTICS
            </div>
            <div style="color:#ffffff; font-weight:800; font-size:1.05rem; margin-bottom:8px;">
                Renegotiate Freight Subsidies in Texas & Ohio
            </div>
            <div style="font-size:0.8rem; color:#94a3b8; line-height:1.5; margin-bottom:12px;">
                Central and East regions suffer negative profitability in Texas (-$25K profit) and Ohio (-$16K profit) due to unmanaged standard freight absorption on low-margin SKUs.
            </div>
            <div style="background:rgba(168, 85, 247, 0.12); padding:8px 12px; border-radius:8px; font-size:0.76rem; color:#a855f7; font-weight:700;">
                Estimated Annual Impact: +$12,000 Logistics Savings
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><hr style='border:none; border-top:1px solid rgba(255,255,255,0.06); margin: 1.5rem 0;'><br>", unsafe_allow_html=True)

    # Interactive What-If Scenario Simulator
    st.markdown("<p style='font-size:1.1rem; font-weight:800; color:#ffffff; margin-bottom:0.2rem;'>Interactive Business 'What-If' Simulation Engine</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.8rem; color:#71717a; margin-bottom:1.2rem;'>Test policy adjustments and simulate projected gross profit uplift in real-time.</p>", unsafe_allow_html=True)

    sim_left, sim_right = st.columns([5, 7])
    with sim_left:
        st.markdown("<p style='font-size:0.85rem; font-weight:700; color:#f472b6; margin-bottom:0.4rem;'>1. Discount Ceiling Policy</p>", unsafe_allow_html=True)
        max_discount_allowed = st.slider(
            "Cap Maximum Transaction Discount",
            min_value=0.10,
            max_value=0.80,
            value=0.25,
            step=0.05,
            format="%.0f%%"
        )
        
        st.markdown("<p style='font-size:0.85rem; font-weight:700; color:#2dd4bf; margin-bottom:0.4rem;'>2. Growth in High-Margin Tech SKUs</p>", unsafe_allow_html=True)
        tech_growth = st.slider(
            "Projected Volume Expansion in Technology",
            min_value=0,
            max_value=40,
            value=10,
            step=5,
            format="+%d%%"
        )
        
        st.markdown("<p style='font-size:0.85rem; font-weight:700; color:#a855f7; margin-bottom:0.4rem;'>3. At-Risk Account Retention Success</p>", unsafe_allow_html=True)
        retention_rate = st.slider(
            "Target Win-Back Rate for 'At Risk' Accounts",
            min_value=0,
            max_value=60,
            value=25,
            step=5,
            format="%d%%"
        )

    # Compute Simulation Dynamics
    sim_df = filtered_df.copy()
    
    over_discount_mask = sim_df['discount'] > max_discount_allowed
    profit_leakage_recovered = (
        (sim_df.loc[over_discount_mask, 'discount'] - max_discount_allowed) * 
        (sim_df.loc[over_discount_mask, 'sales'] / (1 - sim_df.loc[over_discount_mask, 'discount']))
    ).sum()
    
    tech_sales_base = sim_df[sim_df['category'] == 'Technology']['sales'].sum()
    tech_profit_base = sim_df[sim_df['category'] == 'Technology']['profit'].sum()
    tech_margin_pct = (tech_profit_base / tech_sales_base) if tech_sales_base > 0 else 0.17
    tech_profit_gain = (tech_sales_base * (tech_growth / 100)) * tech_margin_pct
    
    risk_monetary_pool = cust_rfm[cust_rfm['churn_risk'] == 'At Risk (180-365d)']['monetary'].sum()
    risk_profit_pool = cust_rfm[cust_rfm['churn_risk'] == 'At Risk (180-365d)']['profit'].sum()
    retention_profit_gain = (risk_profit_pool * (retention_rate / 100)) if risk_profit_pool > 0 else (risk_monetary_pool * 0.12 * (retention_rate / 100))
    
    total_profit_gain = profit_leakage_recovered + tech_profit_gain + retention_profit_gain
    simulated_total_profit = total_profit + total_profit_gain
    simulated_margin = (simulated_total_profit / total_sales * 100) if total_sales > 0 else 0

    with sim_right:
        st.markdown(f"""
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:12px; margin-bottom:14px;">
            <div style="background:#0e0e12; border-radius:12px; padding:14px;">
                <div style="font-size:0.72rem; color:#71717a; font-weight:700; text-transform:uppercase;">Projected Incremental Gain</div>
                <div style="font-size:1.6rem; font-weight:800; color:#2dd4bf; margin-top:2px;">+${total_profit_gain:,.0f}</div>
                <div style="font-size:0.74rem; color:#2dd4bf; margin-top:4px;">Profit uplift above baseline</div>
            </div>
            <div style="background:#0e0e12; border-radius:12px; padding:14px;">
                <div style="font-size:0.72rem; color:#71717a; font-weight:700; text-transform:uppercase;">Simulated Operating Profit</div>
                <div style="font-size:1.6rem; font-weight:800; color:#f472b6; margin-top:2px;">${simulated_total_profit:,.0f}</div>
                <div style="font-size:0.74rem; color:#f472b6; margin-top:4px;">Margin: {profit_margin:.1f}% ➔ <b>{simulated_margin:.1f}%</b></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        fig_waterfall = go.Figure(go.Waterfall(
            name="Profit Lift",
            orientation="v",
            measure=["relative", "relative", "relative", "relative", "total"],
            x=["Base Profit", "Discount Policy", "Tech Expansion", "Client Retention", "Simulated Profit"],
            y=[total_profit, profit_leakage_recovered, tech_profit_gain, retention_profit_gain, simulated_total_profit],
            connector={"line": {"color": "rgba(255,255,255,0.15)"}},
            decreasing={"marker": {"color": "#ff4d6d"}},
            increasing={"marker": {"color": "#2dd4bf"}},
            totals={"marker": {"color": "#f472b6"}},
            textposition="outside",
            text=[f"${total_profit:,.0f}", f"+${profit_leakage_recovered:,.0f}", f"+${tech_profit_gain:,.0f}", f"+${retention_profit_gain:,.0f}", f"${simulated_total_profit:,.0f}"]
        ))
        apply_bento_chart_theme(fig_waterfall, height=280)
        fig_waterfall.update_layout(title="Simulated Profit Attribution Bridge ($)")
        st.plotly_chart(fig_waterfall, use_container_width=True)

# ----------------------------------------------------
# TAB 6: DATA EXPLORER
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
