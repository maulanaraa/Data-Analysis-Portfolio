import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io
import os

# ==========================================
# PAGE CONFIGURATION & LUXURY STYLING
# ==========================================
st.set_page_config(
    page_title="Executive BI — Superstore Global Performance",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End CSS with Google Fonts & Glassmorphism
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* Global Typography & Background */
    * {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgba(99, 102, 241, 0.05) 0%, transparent 40%),
                    radial-gradient(circle at 90% 80%, rgba(6, 182, 212, 0.04) 0%, transparent 40%),
                    #0b0f19;
        color: #f3f4f6;
    }

    .main .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2.5rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 98% !important;
    }

    /* Top Executive Navigation Bar */
    .top-navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.2rem 1.8rem;
        background: rgba(17, 24, 39, 0.7);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
    }
    .brand-title {
        font-size: 1.6rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        background: linear-gradient(135deg, #ffffff 30%, #94a3b8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .brand-subtitle {
        font-size: 0.85rem;
        color: #94a3b8;
        font-weight: 400;
        margin-top: 3px;
    }
    .live-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(99, 102, 241, 0.15);
        color: #818cf8;
        border: 1px solid rgba(99, 102, 241, 0.3);
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.02em;
    }
    .live-dot {
        width: 8px;
        height: 8px;
        background-color: #10b981;
        border-radius: 50%;
        box-shadow: 0 0 8px #10b981;
    }

    /* Sophisticated KPI Glass Cards */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    .kpi-glass-card {
        position: relative;
        background: rgba(17, 24, 39, 0.65);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
        overflow: hidden;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.25);
    }
    .kpi-glass-card:hover {
        transform: translateY(-3px);
        border-color: rgba(99, 102, 241, 0.4);
        box-shadow: 0 12px 28px -4px rgba(99, 102, 241, 0.15);
    }
    .kpi-glow-bar {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
    }
    .glow-indigo { background: linear-gradient(90deg, #6366f1, #818cf8); }
    .glow-emerald { background: linear-gradient(90deg, #10b981, #34d399); }
    .glow-cyan { background: linear-gradient(90deg, #06b6d4, #38bdf8); }
    .glow-purple { background: linear-gradient(90deg, #a855f7, #c084fc); }
    .glow-amber { background: linear-gradient(90deg, #f59e0b, #fbbf24); }

    .kpi-header-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.6rem;
    }
    .kpi-label {
        font-size: 0.78rem;
        font-weight: 600;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    .kpi-icon {
        font-size: 1.1rem;
        opacity: 0.8;
    }
    .kpi-value {
        font-size: 1.85rem;
        font-weight: 800;
        color: #f8fafc;
        letter-spacing: -0.03em;
        line-height: 1.1;
        margin-bottom: 0.5rem;
        font-feature-settings: "tnum";
    }
    .kpi-footer {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 0.8rem;
        font-weight: 500;
    }
    .badge-pill-positive {
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.25);
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .badge-pill-negative {
        background: rgba(239, 68, 68, 0.15);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.25);
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .badge-pill-neutral {
        background: rgba(148, 163, 184, 0.15);
        color: #cbd5e1;
        border: 1px solid rgba(148, 163, 184, 0.25);
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
    }

    /* Executive Insights Box */
    .insights-banner {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 14px;
        padding: 1rem 1.4rem;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 14px;
        box-shadow: 0 4px 15px -3px rgba(0, 0, 0, 0.3);
    }
    .insights-icon {
        font-size: 1.5rem;
        background: rgba(99, 102, 241, 0.2);
        padding: 8px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(17, 24, 39, 0.5);
        padding: 6px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .stTabs [data-baseweb="tab"] {
        height: 42px;
        border-radius: 8px;
        color: #94a3b8;
        font-weight: 600;
        font-size: 0.88rem;
        padding: 0 18px;
        border: none !important;
        background: transparent;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(99, 102, 241, 0.2) !important;
        color: #ffffff !important;
        border: 1px solid rgba(99, 102, 241, 0.4) !important;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2);
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0d1322 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.06);
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# PLOTLY MODERN DARK THEME CONFIG
# ==========================================
def apply_chart_theme(fig, height=360):
    fig.update_layout(
        template="plotly_dark",
        height=height,
        margin=dict(l=15, r=15, t=35, b=15),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#94a3b8", size=11),
        hoverlabel=dict(
            bgcolor="#111827",
            font_size=12,
            font_family="Plus Jakarta Sans",
            bordercolor="rgba(255,255,255,0.15)"
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            color="#64748b",
            tickfont=dict(color="#94a3b8", size=10)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(255, 255, 255, 0.04)",
            zeroline=False,
            color="#64748b",
            tickfont=dict(color="#94a3b8", size=10)
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color="#cbd5e1", size=10),
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
# SIDEBAR FILTERS (EXECUTIVE CONTROLS)
# ==========================================
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 1rem;">
        <span style="font-size: 1.6rem;">⚡</span>
        <div>
            <div style="font-weight: 800; font-size: 1.1rem; color: #f8fafc; letter-spacing: -0.02em;">SUPERSTORE BI</div>
            <div style="font-size: 0.75rem; color: #818cf8; font-weight: 600;">EXECUTIVE ANALYTICS</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    min_date = df_raw['order_date'].min().date()
    max_date = df_raw['order_date'].max().date()
    
    st.markdown("#### 📅 **Timeline Selection**")
    date_selection = st.date_input(
        "Select Date Range",
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
    
    st.markdown("#### 🌐 **Market & Hierarchy**")
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
    
    st.divider()
    st.markdown("""
    <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 8px; padding: 10px; font-size: 0.75rem; color: #94a3b8;">
        💡 <b>Executive Tip:</b> Cross-filter regions and categories to isolate margin leakages across states.
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
# TOP EXECUTIVE NAVIGATION BAR
# ==========================================
current_time_str = datetime.now().strftime("%d %b %Y, %H:%M")
st.markdown(f"""
<div class="top-navbar">
    <div>
        <h1 class="brand-title">Executive Performance & Profitability Hub</h1>
        <div class="brand-subtitle">Commercial Intelligence, Churn Risk Modeling & Regional Profit Heatmaps</div>
    </div>
    <div class="live-badge">
        <span class="live-dot"></span> Active Filter: {start_date.strftime('%b %Y')} – {end_date.strftime('%b %Y')}
    </div>
</div>
""", unsafe_allow_html=True)

if filtered_df.empty:
    st.warning("⚠️ No transactional records match your current filter parameters. Please widen your selection.")
    st.stop()

# ==========================================
# EXECUTIVE KPI SUMMARY CARDS
# ==========================================
total_sales = filtered_df['sales'].sum()
total_profit = filtered_df['profit'].sum()
profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
total_orders = filtered_df['order_id'].nunique()
total_customers = filtered_df['customer_id'].nunique()
avg_order_value = (total_sales / total_orders) if total_orders > 0 else 0

margin_badge_class = "badge-pill-positive" if profit_margin >= 12 else ("badge-pill-negative" if profit_margin < 0 else "badge-pill-neutral")

st.markdown(f"""
<div class="kpi-grid">
    <div class="kpi-glass-card">
        <div class="kpi-glow-bar glow-indigo"></div>
        <div class="kpi-header-row">
            <span class="kpi-label">Gross Revenue</span>
            <span class="kpi-icon">💎</span>
        </div>
        <div class="kpi-value">${total_sales:,.0f}</div>
        <div class="kpi-footer">
            <span class="badge-pill-positive">Total Sales</span>
            <span style="color: #64748b;">Filtered</span>
        </div>
    </div>
    <div class="kpi-glass-card">
        <div class="kpi-glow-bar glow-emerald"></div>
        <div class="kpi-header-row">
            <span class="kpi-label">Net Profit</span>
            <span class="kpi-icon">📈</span>
        </div>
        <div class="kpi-value">${total_profit:,.0f}</div>
        <div class="kpi-footer">
            <span class="{margin_badge_class}">Margin: {profit_margin:.1f}%</span>
        </div>
    </div>
    <div class="kpi-glass-card">
        <div class="kpi-glow-bar glow-cyan"></div>
        <div class="kpi-header-row">
            <span class="kpi-label">Unique Orders</span>
            <span class="kpi-icon">📦</span>
        </div>
        <div class="kpi-value">{total_orders:,}</div>
        <div class="kpi-footer">
            <span class="badge-pill-neutral">Transactions</span>
        </div>
    </div>
    <div class="kpi-glass-card">
        <div class="kpi-glow-bar glow-purple"></div>
        <div class="kpi-header-row">
            <span class="kpi-label">Active Clients</span>
            <span class="kpi-icon">👥</span>
        </div>
        <div class="kpi-value">{total_customers:,}</div>
        <div class="kpi-footer">
            <span class="badge-pill-positive">Unique Buyers</span>
        </div>
    </div>
    <div class="kpi-glass-card">
        <div class="kpi-glow-bar glow-amber"></div>
        <div class="kpi-header-row">
            <span class="kpi-label">Avg Order Value</span>
            <span class="kpi-icon">🎯</span>
        </div>
        <div class="kpi-value">${avg_order_value:,.1f}</div>
        <div class="kpi-footer">
            <span class="badge-pill-neutral">AOV / Basket</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# DYNAMIC EXECUTIVE INSIGHTS BANNER
# ==========================================
best_cat = filtered_df.groupby('category')['sales'].sum().idxmax()
best_cat_sales = filtered_df.groupby('category')['sales'].sum().max()
worst_subcat = filtered_df.groupby('sub_category')['profit'].sum().idxmin()
worst_subcat_profit = filtered_df.groupby('sub_category')['profit'].sum().min()

st.markdown(f"""
<div class="insights-banner">
    <div class="insights-icon">💡</div>
    <div style="font-size: 0.86rem; color: #cbd5e1; line-height: 1.5;">
        <b>Executive Summary:</b> Category <b>{best_cat}</b> leads total volume with <b>${best_cat_sales:,.0f}</b>. 
        {"⚠️ Loss alert: Sub-category <b>" + worst_subcat + "</b> recorded negative profit of <b>$" + f"{worst_subcat_profit:,.0f}</b> due to steep discounting." if worst_subcat_profit < 0 else "All sub-categories operate with positive net contributions."}
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# MAIN ANALYTICAL TABS
# ==========================================
tab_overview, tab_geo, tab_customer, tab_product, tab_data = st.tabs([
    "📊 Financial Velocity",
    "🗺️ Geospatial & Regional",
    "👥 Client Retention & RFM",
    "📦 Margin & Pricing Analysis",
    "📋 Data Intelligence Explorer"
])

# ----------------------------------------------------
# TAB 1: FINANCIAL VELOCITY & TRENDS
# ----------------------------------------------------
with tab_overview:
    col_t1, col_t2 = st.columns([7, 5])
    
    with col_t1:
        st.markdown("##### 📈 **Monthly Revenue & Net Profit Trajectory**")
        monthly_df = filtered_df.groupby('year_month').agg(
            sales=('sales', 'sum'),
            profit=('profit', 'sum')
        ).reset_index().sort_values('year_month')
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=monthly_df['year_month'],
            y=monthly_df['sales'],
            name="Revenue ($)",
            mode="lines+markers",
            line=dict(color="#6366f1", width=3, shape="spline"),
            fill='tozeroy',
            fillcolor='rgba(99, 102, 241, 0.08)'
        ))
        fig_trend.add_trace(go.Scatter(
            x=monthly_df['year_month'],
            y=monthly_df['profit'],
            name="Net Profit ($)",
            mode="lines+markers",
            line=dict(color="#10b981", width=2.5, dash="solid", shape="spline"),
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
        apply_chart_theme(fig_trend, height=360)
        st.plotly_chart(fig_trend, use_container_width=True)
        
    with col_t2:
        st.markdown("##### 🍩 **Customer Segment Distribution**")
        seg_df = filtered_df.groupby('segment').agg(
            sales=('sales', 'sum'),
            profit=('profit', 'sum')
        ).reset_index()
        
        fig_seg = px.pie(
            seg_df,
            values='sales',
            names='segment',
            hole=0.6,
            color='segment',
            color_discrete_map={
                'Consumer': '#6366f1',
                'Corporate': '#06b6d4',
                'Home Office': '#a855f7'
            }
        )
        fig_seg.update_traces(
            textposition='outside',
            textinfo='percent+label',
            hovertemplate="<b>%{label}</b><br>Sales: $%{value:,.0f}<br>Contribution: %{percent}"
        )
        apply_chart_theme(fig_seg, height=360)
        fig_seg.update_layout(showlegend=False)
        st.plotly_chart(fig_seg, use_container_width=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_t3, col_t4 = st.columns([6, 6])
    with col_t3:
        st.markdown("##### 📊 **Revenue Contribution by Sub-Category**")
        sub_sales = filtered_df.groupby(['category', 'sub_category'])['sales'].sum().reset_index().sort_values('sales', ascending=True)
        fig_sub = px.bar(
            sub_sales,
            x='sales',
            y='sub_category',
            color='category',
            orientation='h',
            color_discrete_sequence=['#6366f1', '#06b6d4', '#10b981'],
            labels={'sales': 'Sales ($)', 'sub_category': 'Sub-Category', 'category': 'Category'}
        )
        apply_chart_theme(fig_sub, height=420)
        st.plotly_chart(fig_sub, use_container_width=True)
        
    with col_t4:
        st.markdown("##### 🎯 **Profit Margin Spectrum (%)**")
        sub_prof = filtered_df.groupby('sub_category').agg(
            sales=('sales', 'sum'),
            profit=('profit', 'sum')
        ).reset_index()
        sub_prof['margin'] = (sub_prof['profit'] / sub_prof['sales']) * 100
        sub_prof = sub_prof.sort_values('margin', ascending=True)
        
        bar_colors = ['#f43f5e' if m < 0 else '#10b981' for m in sub_prof['margin']]
        fig_m = go.Figure(go.Bar(
            x=sub_prof['margin'],
            y=sub_prof['sub_category'],
            orientation='h',
            marker=dict(color=bar_colors, line=dict(width=0)),
            text=[f"{m:+.1f}%" for m in sub_prof['margin']],
            textposition='outside'
        ))
        apply_chart_theme(fig_m, height=420)
        fig_m.update_layout(xaxis=dict(title="Profit Margin %"))
        st.plotly_chart(fig_m, use_container_width=True)

# ----------------------------------------------------
# TAB 2: GEOSPATIAL & REGIONAL PERFORMANCE
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
    
    geo_left, geo_right = st.columns([7, 5])
    with geo_left:
        st.markdown("##### 🗺️ **State-Level Revenue & Profit Density**")
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
            geo=dict(bgcolor='rgba(0,0,0,0)', lakecolor='rgba(15, 23, 42, 0.5)'),
            margin=dict(l=0, r=0, t=10, b=10)
        )
        apply_chart_theme(fig_map, height=380)
        st.plotly_chart(fig_map, use_container_width=True)
        
    with geo_right:
        st.markdown("##### 🏆 **Market Leaders: Top 5 States**")
        top_states = state_df.sort_values('sales', ascending=False).head(5)
        for _, r in top_states.iterrows():
            badge = "🟢" if r['profit_margin'] >= 10 else ("🔴" if r['profit_margin'] < 0 else "🟡")
            st.markdown(f"""
            <div style="background: rgba(17, 24, 39, 0.6); border: 1px solid rgba(255,255,255,0.06); border-radius: 10px; padding: 10px 14px; margin-bottom: 8px;">
                <div style="display:flex; justify-content:space-between; font-weight:700; color:#f8fafc; font-size: 0.9rem;">
                    <span>{r['state']}</span>
                    <span style="color:#818cf8;">${r['sales']:,.0f}</span>
                </div>
                <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:#94a3b8; margin-top:4px;">
                    <span>Profit: ${r['profit']:,.0f}</span>
                    <span>{badge} Margin: {r['profit_margin']:.1f}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown("<br>", unsafe_allow_html=True)
    
    g_row2_left, g_row2_right = st.columns(2)
    with g_row2_left:
        st.markdown("##### 🌡️ **Regional Profitability Heatmap (Region vs Segment)**")
        pivot_r = filtered_df.pivot_table(index='region', columns='segment', values='profit', aggfunc='sum').fillna(0)
        fig_hm = px.imshow(
            pivot_r,
            text_auto="$,.0f",
            color_continuous_scale="Spectral",
            aspect="auto",
            labels=dict(x="Segment", y="Region", color="Profit ($)")
        )
        apply_chart_theme(fig_hm, height=330)
        st.plotly_chart(fig_hm, use_container_width=True)
        
    with g_row2_right:
        st.markdown("##### 🚚 **Fulfillment Efficiency: Shipping Modes**")
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
        apply_chart_theme(fig_ship, height=330)
        st.plotly_chart(fig_ship, use_container_width=True)

# ----------------------------------------------------
# TAB 3: CLIENT RETENTION & RFM CHURN
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
    
    c_col1, c_col2, c_col3 = st.columns([4, 4, 4])
    with c_col1:
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
                'Lost (>365d)': '#f43f5e'
            }
        )
        fig_c_pie.update_traces(textposition='inside', textinfo='percent+label')
        apply_chart_theme(fig_c_pie, height=320)
        fig_c_pie.update_layout(title="Churn Risk Cohort", showlegend=False)
        st.plotly_chart(fig_c_pie, use_container_width=True)
        
    with c_col2:
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
                'Lost (>365d)': '#f43f5e'
            },
            labels={'recency': 'Days Since Last Order', 'monetary': 'Total Spent ($)', 'churn_risk': 'Cohort'}
        )
        apply_chart_theme(fig_c_rfm, height=320)
        fig_c_rfm.update_layout(title="Recency vs Lifetime Value")
        st.plotly_chart(fig_c_rfm, use_container_width=True)
        
    with c_col3:
        act = (cust_rfm['churn_risk'] == 'Active (<180d)').sum()
        risk = (cust_rfm['churn_risk'] == 'At Risk (180-365d)').sum()
        lost = (cust_rfm['churn_risk'] == 'Lost (>365d)').sum()
        
        st.markdown("##### 📌 **Client Retention Health**")
        st.markdown(f"""
        <div style="display:flex; flex-direction:column; gap:10px; margin-top:10px;">
            <div style="background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.3); border-radius:10px; padding:12px;">
                <div style="color:#34d399; font-weight:700; font-size:0.9rem;">🟢 Active Clients: {act}</div>
                <div style="color:#94a3b8; font-size:0.75rem;">{(act/len(cust_rfm)*100):.1f}% of client base purchased recently.</div>
            </div>
            <div style="background:rgba(245,158,11,0.1); border:1px solid rgba(245,158,11,0.3); border-radius:10px; padding:12px;">
                <div style="color:#fbbf24; font-weight:700; font-size:0.9rem;">🟡 At Risk: {risk}</div>
                <div style="color:#94a3b8; font-size:0.75rem;">{(risk/len(cust_rfm)*100):.1f}% inactive for 6-12 months.</div>
            </div>
            <div style="background:rgba(244,63,94,0.1); border:1px solid rgba(244,63,94,0.3); border-radius:10px; padding:12px;">
                <div style="color:#f87171; font-weight:700; font-size:0.9rem;">🔴 Churned / Lost: {lost}</div>
                <div style="color:#94a3b8; font-size:0.75rem;">{(lost/len(cust_rfm)*100):.1f}% require re-engagement campaign.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    top_c_left, top_c_right = st.columns(2)
    with top_c_left:
        st.markdown("##### 🌟 **Top 10 High-Value Clients (Profit)**")
        top_10 = cust_rfm.sort_values('profit', ascending=False).head(10)
        fig_t10 = px.bar(
            top_10,
            x='profit',
            y='customer_name',
            orientation='h',
            color='profit',
            color_continuous_scale="Viridis",
            labels={'profit': 'Net Profit ($)', 'customer_name': 'Client'}
        )
        fig_t10.update_layout(yaxis=dict(autorange="reversed"))
        apply_chart_theme(fig_t10, height=360)
        st.plotly_chart(fig_t10, use_container_width=True)
        
    with top_c_right:
        st.markdown("##### ⚠️ **Top 10 Loss-Driving Accounts**")
        bot_10 = cust_rfm.sort_values('profit', ascending=True).head(10)
        fig_b10 = px.bar(
            bot_10,
            x='profit',
            y='customer_name',
            orientation='h',
            color='profit',
            color_continuous_scale="Reds_r",
            labels={'profit': 'Net Profit ($)', 'customer_name': 'Client'}
        )
        apply_chart_theme(fig_b10, height=360)
        st.plotly_chart(fig_b10, use_container_width=True)

# ----------------------------------------------------
# TAB 4: MARGIN & PRICING ANALYSIS
# ----------------------------------------------------
with tab_product:
    p_col1, p_col2 = st.columns(2)
    with p_col1:
        st.markdown("##### 🏆 **Top 10 Revenue Generating Products**")
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
            labels={'sales': 'Sales ($)', 'product_name': 'Product', 'profit': 'Profit ($)'}
        )
        fig_tp.update_layout(yaxis=dict(autorange="reversed"))
        apply_chart_theme(fig_tp, height=400)
        st.plotly_chart(fig_tp, use_container_width=True)
        
    with p_col2:
        st.markdown("##### 📉 **Discount vs Profit Margin Erosion**")
        sample_prod = filtered_df.sample(min(len(filtered_df), 1200), random_state=42)
        fig_disc = px.scatter(
            sample_prod,
            x='discount',
            y='profit_margin',
            color='category',
            size='sales',
            hover_name='product_name',
            labels={'discount': 'Discount Rate (0.0 – 0.8)', 'profit_margin': 'Profit Margin %', 'category': 'Category'},
            color_discrete_sequence=['#6366f1', '#06b6d4', '#f43f5e']
        )
        fig_disc.add_hline(y=0, line_dash="dash", line_color="#ef4444", opacity=0.8)
        apply_chart_theme(fig_disc, height=400)
        st.plotly_chart(fig_disc, use_container_width=True)

# ----------------------------------------------------
# TAB 5: DATA INTELLIGENCE EXPLORER
# ----------------------------------------------------
with tab_data:
    st.markdown("##### 📋 **Granular Transaction Explorer**")
    
    f1, f2 = st.columns([8, 4])
    with f1:
        q = st.text_input("🔍 Full-Text Search (Product, Customer, State, City, ID)", "")
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
            "📥 Export Filtered Data (CSV)",
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
            "📊 Export Filtered Data (Excel)",
            data=b.getvalue(),
            file_name=f"superstore_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
