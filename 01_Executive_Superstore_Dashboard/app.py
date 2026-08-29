import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io
import os

# ==========================================
# PAGE CONFIGURATION & BENTO DARK STYLING
# ==========================================
st.set_page_config(
    page_title="Superstore Executive Hub — Bento Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End CSS: Satoshi Font, Floating Sidebar, Bento Grid, Pure Black UI
st.markdown("""
<style>
    @import url('https://api.fontshare.com/v2/css?f[]=satoshi@900,800,700,600,500,400,300&display=swap');

    /* Global Typography & Deep Black Canvas */
    * {
        font-family: 'Satoshi', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    .stApp {
        background-color: #050505 !important;
        background-image: 
            radial-gradient(circle at 15% 15%, rgba(124, 58, 237, 0.05) 0%, transparent 40%),
            radial-gradient(circle at 85% 75%, rgba(6, 182, 212, 0.04) 0%, transparent 40%);
        color: #f4f4f5;
    }

    .main .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2.5rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 98% !important;
    }

    /* Floating Elevated Sidebar */
    section[data-testid="stSidebar"] {
        background-color: transparent !important;
    }
    section[data-testid="stSidebar"] > div:first-child {
        background: rgba(14, 14, 18, 0.85) !important;
        backdrop-filter: blur(24px) !important;
        -webkit-backdrop-filter: blur(24px) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 22px !important;
        margin: 16px 10px 16px 16px !important;
        height: calc(100vh - 32px) !important;
        box-shadow: 0 20px 50px -10px rgba(0, 0, 0, 0.8), 0 0 25px rgba(124, 58, 237, 0.04) !important;
        padding: 1.5rem 1.2rem !important;
    }

    /* Top Executive Bento Navigation Header */
    .bento-nav-card {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.2rem 1.8rem;
        background: rgba(15, 15, 20, 0.7);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 20px;
        margin-bottom: 1.4rem;
        box-shadow: 0 8px 32px -4px rgba(0, 0, 0, 0.6);
    }
    .brand-title {
        font-size: 1.65rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        background: linear-gradient(135deg, #ffffff 40%, #a1a1aa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .brand-subtitle {
        font-size: 0.84rem;
        color: #71717a;
        font-weight: 500;
        margin-top: 3px;
    }
    .live-chip {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        background: rgba(124, 58, 237, 0.12);
        color: #a78bfa;
        border: 1px solid rgba(124, 58, 237, 0.25);
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.01em;
    }
    .pulse-dot {
        width: 8px;
        height: 8px;
        background-color: #10b981;
        border-radius: 50%;
        box-shadow: 0 0 10px #10b981;
    }

    /* Bento Grid KPI Cards */
    .bento-kpi-container {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 1rem;
        margin-bottom: 1.4rem;
    }
    .bento-card {
        position: relative;
        background: rgba(18, 18, 24, 0.65);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 18px;
        padding: 1.2rem 1.4rem;
        overflow: hidden;
        transition: all 0.28s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 6px 24px -4px rgba(0, 0, 0, 0.4);
    }
    .bento-card:hover {
        transform: translateY(-3px);
        border-color: rgba(124, 58, 237, 0.45);
        box-shadow: 0 16px 36px -8px rgba(124, 58, 237, 0.18);
        background: rgba(22, 22, 30, 0.85);
    }
    .bento-accent-line {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
    }
    .line-violet { background: linear-gradient(90deg, #7c3aed, #a78bfa); }
    .line-emerald { background: linear-gradient(90deg, #10b981, #34d399); }
    .line-cyan { background: linear-gradient(90deg, #06b6d4, #67e8f9); }
    .line-fuchsia { background: linear-gradient(90deg, #d946ef, #f472b6); }
    .line-amber { background: linear-gradient(90deg, #f59e0b, #fcd34d); }

    .bento-card-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }
    .bento-label {
        font-size: 0.76rem;
        font-weight: 700;
        color: #71717a;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    .bento-icon {
        font-size: 1.15rem;
        opacity: 0.85;
    }
    .bento-value {
        font-size: 1.85rem;
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
        font-size: 0.78rem;
        font-weight: 600;
    }
    .pill-green {
        background: rgba(16, 185, 129, 0.12);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.2);
        padding: 2px 8px;
        border-radius: 6px;
    }
    .pill-red {
        background: rgba(244, 63, 94, 0.12);
        color: #fb7185;
        border: 1px solid rgba(244, 63, 94, 0.2);
        padding: 2px 8px;
        border-radius: 6px;
    }
    .pill-violet {
        background: rgba(124, 58, 237, 0.12);
        color: #c4b5fd;
        border: 1px solid rgba(124, 58, 237, 0.2);
        padding: 2px 8px;
        border-radius: 6px;
    }

    /* Bento Insight Banner */
    .bento-insight-banner {
        background: linear-gradient(135deg, rgba(24, 24, 32, 0.75) 0%, rgba(12, 12, 16, 0.85) 100%);
        border: 1px solid rgba(124, 58, 237, 0.22);
        border-radius: 18px;
        padding: 1rem 1.4rem;
        margin-bottom: 1.4rem;
        display: flex;
        align-items: center;
        gap: 14px;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.4);
    }
    .insight-badge {
        font-size: 1.3rem;
        background: rgba(124, 58, 237, 0.2);
        padding: 6px 10px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    /* Tab Controls */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(15, 15, 20, 0.6);
        padding: 5px;
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        border-radius: 10px;
        color: #71717a;
        font-weight: 600;
        font-size: 0.85rem;
        padding: 0 18px;
        border: none !important;
        background: transparent;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(124, 58, 237, 0.22) !important;
        color: #ffffff !important;
        border: 1px solid rgba(124, 58, 237, 0.4) !important;
        box-shadow: 0 4px 14px rgba(124, 58, 237, 0.25);
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #050505;
    }
    ::-webkit-scrollbar-thumb {
        background: #27272a;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #3f3f46;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# PLOTLY MODERN PURE DARK ENGINE
# ==========================================
def apply_bento_chart_theme(fig, height=360):
    fig.update_layout(
        template="plotly_dark",
        height=height,
        margin=dict(l=15, r=15, t=35, b=15),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Satoshi, sans-serif", color="#71717a", size=11),
        hoverlabel=dict(
            bgcolor="#0e0e12",
            font_size=12,
            font_family="Satoshi",
            bordercolor="rgba(255,255,255,0.12)"
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            color="#52525b",
            tickfont=dict(color="#71717a", size=10)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(255, 255, 255, 0.035)",
            zeroline=False,
            color="#52525b",
            tickfont=dict(color="#71717a", size=10)
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
# FLOATING SIDEBAR FILTERS
# ==========================================
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 1.2rem;">
        <div style="background: rgba(124,58,237,0.25); border: 1px solid rgba(124,58,237,0.4); padding: 8px; border-radius: 12px;">⚡</div>
        <div>
            <div style="font-weight: 800; font-size: 1.15rem; color: #ffffff; letter-spacing: -0.03em;">BENTO HUB</div>
            <div style="font-size: 0.72rem; color: #a78bfa; font-weight: 700; letter-spacing: 0.05em;">COMMERCIAL BI</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    min_date = df_raw['order_date'].min().date()
    max_date = df_raw['order_date'].max().date()
    
    st.markdown("#### 📅 **Timeline Range**")
    date_selection = st.date_input(
        "Date Selector",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        label_visibility="collapsed"
    )
    
    if isinstance(date_selection, (tuple, list)) and len(date_selection) == 2:
        start_date, end_date = date_selection
    else:
        start_date, end_date = min_date, max_date
        
    st.divider()
    
    st.markdown("#### 🌐 **Market Hierarchy**")
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
        "Categories",
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
    
    st.divider()
    st.markdown("""
    <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; padding: 12px; font-size: 0.74rem; color: #71717a; line-height: 1.4;">
        ✨ <b>Bento Grid Engine:</b> Dynamically renders analytics across high-dimensional retail parameters.
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
# TOP BENTO NAVIGATION HEADER
# ==========================================
st.markdown(f"""
<div class="bento-nav-card">
    <div>
        <h1 class="brand-title">Superstore Executive Performance Hub</h1>
        <div class="brand-subtitle">Commercial Velocity, RFM Churn Modeling & Regional Profitability Matrix</div>
    </div>
    <div class="live-chip">
        <span class="pulse-dot"></span> Filtered: {start_date.strftime('%b %Y')} – {end_date.strftime('%b %Y')}
    </div>
</div>
""", unsafe_allow_html=True)

if filtered_df.empty:
    st.warning("⚠️ No records match the current filter selection.")
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

margin_pill_class = "pill-green" if profit_margin >= 12 else ("pill-red" if profit_margin < 0 else "pill-violet")

st.markdown(f"""
<div class="bento-kpi-container">
    <div class="bento-card">
        <div class="bento-accent-line line-violet"></div>
        <div class="bento-card-top">
            <span class="bento-label">Gross Revenue</span>
            <span class="bento-icon">💎</span>
        </div>
        <div class="bento-value">${total_sales:,.0f}</div>
        <div class="bento-footer">
            <span class="pill-violet">Total Volume</span>
        </div>
    </div>
    <div class="bento-card">
        <div class="bento-accent-line line-emerald"></div>
        <div class="bento-card-top">
            <span class="bento-label">Net Profit</span>
            <span class="bento-icon">📈</span>
        </div>
        <div class="bento-value">${total_profit:,.0f}</div>
        <div class="bento-footer">
            <span class="{margin_pill_class}">Margin: {profit_margin:.1f}%</span>
        </div>
    </div>
    <div class="bento-card">
        <div class="bento-accent-line line-cyan"></div>
        <div class="bento-card-top">
            <span class="bento-label">Unique Orders</span>
            <span class="bento-icon">📦</span>
        </div>
        <div class="bento-value">{total_orders:,}</div>
        <div class="bento-footer">
            <span class="pill-violet">Transactions</span>
        </div>
    </div>
    <div class="bento-card">
        <div class="bento-accent-line line-fuchsia"></div>
        <div class="bento-card-top">
            <span class="bento-label">Active Clients</span>
            <span class="bento-icon">👥</span>
        </div>
        <div class="bento-value">{total_customers:,}</div>
        <div class="bento-footer">
            <span class="pill-green">Customer Base</span>
        </div>
    </div>
    <div class="bento-card">
        <div class="bento-accent-line line-amber"></div>
        <div class="bento-card-top">
            <span class="bento-label">Avg Order Value</span>
            <span class="bento-icon">🎯</span>
        </div>
        <div class="bento-value">${avg_order_value:,.1f}</div>
        <div class="bento-footer">
            <span class="pill-violet">AOV / Basket</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# BENTO INSIGHT BANNER
# ==========================================
best_cat = filtered_df.groupby('category')['sales'].sum().idxmax()
best_cat_sales = filtered_df.groupby('category')['sales'].sum().max()
worst_subcat = filtered_df.groupby('sub_category')['profit'].sum().idxmin()
worst_subcat_profit = filtered_df.groupby('sub_category')['profit'].sum().min()

st.markdown(f"""
<div class="bento-insight-banner">
    <div class="insight-badge">💡</div>
    <div style="font-size: 0.85rem; color: #a1a1aa; line-height: 1.5;">
        <b>Executive Takeaway:</b> Product category <b style="color:#ffffff;">{best_cat}</b> generated the highest gross volume (<b style="color:#a78bfa;">${best_cat_sales:,.0f}</b>). 
        {"⚠️ <b>Leakage Warning:</b> Sub-category <b style='color:#fb7185;'>" + worst_subcat + "</b> recorded an aggregate deficit of <b style='color:#fb7185;'>$" + f"{worst_subcat_profit:,.0f}</b> due to heavy promotional discounting." if worst_subcat_profit < 0 else "All sub-categories maintain positive net contribution."}
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# BENTO ANALYTICAL MODULES (TABS)
# ==========================================
tab_overview, tab_geo, tab_customer, tab_product, tab_data = st.tabs([
    "📊 Financial Velocity",
    "🗺️ Geospatial & Regional",
    "👥 Client Retention & RFM",
    "📦 Margin & Pricing Analysis",
    "📋 Data Intelligence Explorer"
])

# ----------------------------------------------------
# TAB 1: FINANCIAL VELOCITY
# ----------------------------------------------------
with tab_overview:
    b1_left, b1_right = st.columns([7, 5])
    
    with b1_left:
        st.markdown("##### 📈 **Monthly Trajectory: Revenue vs Net Profit**")
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
            line=dict(color="#7c3aed", width=3, shape="spline"),
            fill='tozeroy',
            fillcolor='rgba(124, 58, 237, 0.08)'
        ))
        fig_trend.add_trace(go.Scatter(
            x=monthly_df['year_month'],
            y=monthly_df['profit'],
            name="Net Profit ($)",
            mode="lines+markers",
            line=dict(color="#10b981", width=2.5, shape="spline"),
            yaxis="y2"
        ))
        fig_trend.update_layout(
            hovermode="x unified",
            yaxis2=dict(
                title="Profit ($)",
                overlaying="y",
                side="right",
                showgrid=False,
                tickfont=dict(color="#10b981", size=10)
            )
        )
        apply_bento_chart_theme(fig_trend, height=360)
        st.plotly_chart(fig_trend, use_container_width=True)
        
    with b1_right:
        st.markdown("##### 🍩 **Customer Segment Share**")
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
                'Consumer': '#7c3aed',
                'Corporate': '#06b6d4',
                'Home Office': '#d946ef'
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
        st.markdown("##### 📊 **Revenue by Sub-Category**")
        sub_sales = filtered_df.groupby(['category', 'sub_category'])['sales'].sum().reset_index().sort_values('sales', ascending=True)
        fig_sub = px.bar(
            sub_sales,
            x='sales',
            y='sub_category',
            color='category',
            orientation='h',
            color_discrete_sequence=['#7c3aed', '#06b6d4', '#10b981'],
            labels={'sales': 'Sales ($)', 'sub_category': 'Sub-Category', 'category': 'Category'}
        )
        apply_bento_chart_theme(fig_sub, height=420)
        st.plotly_chart(fig_sub, use_container_width=True)
        
    with b1_c4:
        st.markdown("##### 🎯 **Profit Margin Breakdown (%)**")
        sub_prof = filtered_df.groupby('sub_category').agg(
            sales=('sales', 'sum'),
            profit=('profit', 'sum')
        ).reset_index()
        sub_prof['margin'] = (sub_prof['profit'] / sub_prof['sales']) * 100
        sub_prof = sub_prof.sort_values('margin', ascending=True)
        
        bar_colors = ['#fb7185' if m < 0 else '#10b981' for m in sub_prof['margin']]
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
# TAB 2: GEOSPATIAL & REGIONAL
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
        st.markdown("##### 🗺️ **State-Level Revenue Density (US)**")
        fig_map = px.choropleth(
            state_df.dropna(subset=['state_code']),
            locations='state_code',
            locationmode="USA-states",
            color='sales',
            scope="usa",
            color_continuous_scale="Purples",
            hover_name='state',
            hover_data={'sales': ':$,.0f', 'profit': ':$,.0f', 'profit_margin': ':.1f%'},
            labels={'sales': 'Revenue ($)', 'profit': 'Profit ($)', 'profit_margin': 'Margin'}
        )
        fig_map.update_layout(
            geo=dict(bgcolor='rgba(0,0,0,0)', lakecolor='rgba(14, 14, 18, 0.5)'),
            margin=dict(l=0, r=0, t=10, b=10)
        )
        apply_bento_chart_theme(fig_map, height=380)
        st.plotly_chart(fig_map, use_container_width=True)
        
    with g_right:
        st.markdown("##### 🏆 **Top 5 Contributing States**")
        top_states = state_df.sort_values('sales', ascending=False).head(5)
        for _, r in top_states.iterrows():
            badge = "🟢" if r['profit_margin'] >= 10 else ("🔴" if r['profit_margin'] < 0 else "🟡")
            st.markdown(f"""
            <div style="background: rgba(18, 18, 24, 0.7); border: 1px solid rgba(255,255,255,0.06); border-radius: 14px; padding: 12px 16px; margin-bottom: 8px;">
                <div style="display:flex; justify-content:space-between; font-weight:700; color:#ffffff; font-size: 0.92rem;">
                    <span>{r['state']}</span>
                    <span style="color:#a78bfa;">${r['sales']:,.0f}</span>
                </div>
                <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:#71717a; margin-top:4px;">
                    <span>Profit: ${r['profit']:,.0f}</span>
                    <span>{badge} Margin: {r['profit_margin']:.1f}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown("<br>", unsafe_allow_html=True)
    
    g2_left, g2_right = st.columns(2)
    with g2_left:
        st.markdown("##### 🌡️ **Regional Profit Matrix (Region vs Segment)**")
        pivot_r = filtered_df.pivot_table(index='region', columns='segment', values='profit', aggfunc='sum').fillna(0)
        fig_hm = px.imshow(
            pivot_r,
            text_auto="$,.0f",
            color_continuous_scale="Spectral",
            aspect="auto",
            labels=dict(x="Segment", y="Region", color="Profit ($)")
        )
        apply_bento_chart_theme(fig_hm, height=330)
        st.plotly_chart(fig_hm, use_container_width=True)
        
    with g2_right:
        st.markdown("##### 🚚 **Fulfillment Dynamics by Shipping Mode**")
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
            color_continuous_scale="Teal",
            labels={'sales': 'Sales ($)', 'ship_mode': 'Ship Mode', 'avg_days': 'Avg Days'}
        )
        apply_bento_chart_theme(fig_ship, height=330)
        st.plotly_chart(fig_ship, use_container_width=True)

# ----------------------------------------------------
# TAB 3: CLIENT RETENTION & RFM
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
                'Active (<180d)': '#10b981',
                'At Risk (180-365d)': '#f59e0b',
                'Lost (>365d)': '#fb7185'
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
                'Active (<180d)': '#10b981',
                'At Risk (180-365d)': '#f59e0b',
                'Lost (>365d)': '#fb7185'
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
        
        st.markdown("##### 📌 **Client Cohort Health**")
        st.markdown(f"""
        <div style="display:flex; flex-direction:column; gap:10px; margin-top:8px;">
            <div style="background:rgba(16,185,129,0.08); border:1px solid rgba(16,185,129,0.25); border-radius:12px; padding:12px;">
                <div style="color:#34d399; font-weight:700; font-size:0.88rem;">🟢 Active (<180d): {act} clients</div>
                <div style="color:#71717a; font-size:0.75rem;">{(act/len(cust_rfm)*100):.1f}% healthy purchasing activity.</div>
            </div>
            <div style="background:rgba(245,158,11,0.08); border:1px solid rgba(245,158,11,0.25); border-radius:12px; padding:12px;">
                <div style="color:#fcd34d; font-weight:700; font-size:0.88rem;">🟡 At Risk (180-365d): {risk} clients</div>
                <div style="color:#71717a; font-size:0.75rem;">{(risk/len(cust_rfm)*100):.1f}% inactive for 6+ months.</div>
            </div>
            <div style="background:rgba(244,63,94,0.08); border:1px solid rgba(244,63,94,0.25); border-radius:12px; padding:12px;">
                <div style="color:#fb7185; font-weight:700; font-size:0.88rem;">🔴 Lost (>365d): {lost} clients</div>
                <div style="color:#71717a; font-size:0.75rem;">{(lost/len(cust_rfm)*100):.1f}% churned accounts.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    top_c_l, top_c_r = st.columns(2)
    with top_c_l:
        st.markdown("##### 🌟 **Top 10 High-Margin Clients**")
        top_10 = cust_rfm.sort_values('profit', ascending=False).head(10)
        fig_t10 = px.bar(
            top_10,
            x='profit',
            y='customer_name',
            orientation='h',
            color='profit',
            color_continuous_scale="Viridis",
            labels={'profit': 'Profit ($)', 'customer_name': 'Client'}
        )
        fig_t10.update_layout(yaxis=dict(autorange="reversed"))
        apply_bento_chart_theme(fig_t10, height=360)
        st.plotly_chart(fig_t10, use_container_width=True)
        
    with top_c_r:
        st.markdown("##### ⚠️ **Top 10 Loss-Making Clients**")
        bot_10 = cust_rfm.sort_values('profit', ascending=True).head(10)
        fig_b10 = px.bar(
            bot_10,
            x='profit',
            y='customer_name',
            orientation='h',
            color='profit',
            color_continuous_scale="Reds_r",
            labels={'profit': 'Profit ($)', 'customer_name': 'Client'}
        )
        apply_bento_chart_theme(fig_b10, height=360)
        st.plotly_chart(fig_b10, use_container_width=True)

# ----------------------------------------------------
# TAB 4: MARGIN & PRICING
# ----------------------------------------------------
with tab_product:
    p1, p2 = st.columns(2)
    with p1:
        st.markdown("##### 🏆 **Top 10 Revenue Generating SKUs**")
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
            color_continuous_scale="Plasma",
            labels={'sales': 'Sales ($)', 'product_name': 'SKU', 'profit': 'Profit ($)'}
        )
        fig_tp.update_layout(yaxis=dict(autorange="reversed"))
        apply_bento_chart_theme(fig_tp, height=400)
        st.plotly_chart(fig_tp, use_container_width=True)
        
    with p2:
        st.markdown("##### 📉 **Discount vs Margin Sensitivity**")
        sample_prod = filtered_df.sample(min(len(filtered_df), 1200), random_state=42)
        fig_disc = px.scatter(
            sample_prod,
            x='discount',
            y='profit_margin',
            color='category',
            size='sales',
            hover_name='product_name',
            labels={'discount': 'Discount (0.0 – 0.8)', 'profit_margin': 'Margin %', 'category': 'Category'},
            color_discrete_sequence=['#7c3aed', '#06b6d4', '#fb7185']
        )
        fig_disc.add_hline(y=0, line_dash="dash", line_color="#fb7185", opacity=0.8)
        apply_bento_chart_theme(fig_disc, height=400)
        st.plotly_chart(fig_disc, use_container_width=True)

# ----------------------------------------------------
# TAB 5: DATA EXPLORER
# ----------------------------------------------------
with tab_data:
    st.markdown("##### 📋 **Granular Transactional Ledger**")
    
    f1, f2 = st.columns([8, 4])
    with f1:
        q = st.text_input("🔍 Search Database (Product, Customer, State, City, ID)", "")
    with f2:
        page_size = st.selectbox("Display Limit", [50, 100, 250, 500, "All Records"], index=0)
        
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
            "📥 Export Filtered Ledger (CSV)",
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
            "📊 Export Filtered Ledger (Excel)",
            data=b.getvalue(),
            file_name=f"superstore_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
