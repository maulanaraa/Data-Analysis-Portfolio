import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io
import os

# ==========================================
# PAGE CONFIGURATION & STYLING
# ==========================================
st.set_page_config(
    page_title="Executive Dashboard - Superstore",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern executive styling
st.markdown("""
<style>
    /* Global styles */
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    
    /* Metric Card Styling */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08);
    }
    .metric-title {
        color: #64748b;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }
    .metric-value {
        color: #0f172a;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 4px;
    }
    .metric-subtitle {
        font-size: 0.8rem;
        font-weight: 500;
    }
    .positive-delta {
        color: #10b981;
    }
    .negative-delta {
        color: #ef4444;
    }
    
    /* Header styling */
    .dashboard-header {
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid #e2e8f0;
    }
    .dashboard-title {
        font-size: 2.1rem;
        font-weight: 800;
        color: #1e293b;
        letter-spacing: -0.02em;
    }
    .dashboard-subtitle {
        font-size: 0.95rem;
        color: #64748b;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        border-radius: 8px;
        font-weight: 600;
        padding: 0 20px;
    }
    
    /* Sidebar badge */
    .filter-badge {
        background-color: #e0f2fe;
        color: #0369a1;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# DATA LOADING & PREPROCESSING
# ==========================================
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_paths = [
        os.path.join(current_dir, "data", "Sample - Superstore.csv"),
        os.path.join(current_dir, "Sample - Superstore.csv"),
        "01_Executive_Superstore_Dashboard/data/Sample - Superstore.csv",
        "data/Sample - Superstore.csv",
        "Sample - Superstore.csv",
        "sample_superstore.csv",
        "data/sample_superstore.csv"
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
        # Fallback to direct raw download if file not found locally
        url = "https://raw.githubusercontent.com/zpio/datasets/main/sample_superstore.csv"
        try:
            df = pd.read_csv(url, encoding='windows-1252')
        except Exception:
            df = pd.read_csv(url)

    # Standardize column names to snake_case
    df.columns = [c.strip().lower().replace(" ", "_").replace("-", "_") for c in df.columns]
    
    # Parse dates
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    df['ship_date'] = pd.to_datetime(df['ship_date'], errors='coerce')
    
    # Drop rows without order_date
    df = df.dropna(subset=['order_date']).copy()
    
    # Add calculated columns
    df['year'] = df['order_date'].dt.year
    df['month'] = df['order_date'].dt.month
    df['year_month'] = df['order_date'].dt.to_period('M').astype(str)
    df['quarter'] = df['order_date'].dt.to_period('Q').astype(str)
    df['shipping_days'] = (df['ship_date'] - df['order_date']).dt.days
    df['profit_margin'] = np.where(df['sales'] != 0, (df['profit'] / df['sales']) * 100, 0)
    
    return df

df_raw = load_data()

# ==========================================
# SIDEBAR FILTERS
# ==========================================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/dashboard-layout.png", width=64)
    st.markdown("## **Executive Controls**")
    st.markdown("<span class='filter-badge'>Dataset: Sample Superstore</span>", unsafe_allow_html=True)
    
    # Date Range Filter
    min_date = df_raw['order_date'].min().date()
    max_date = df_raw['order_date'].max().date()
    
    st.markdown("### 📅 **Periode Transaksi**")
    date_selection = st.date_input(
        "Pilih Rentang Tanggal",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    if isinstance(date_selection, (tuple, list)) and len(date_selection) == 2:
        start_date, end_date = date_selection
    else:
        start_date, end_date = min_date, max_date
        
    st.divider()
    
    # Region Filter
    st.markdown("### 🌍 **Geografi & Segment**")
    all_regions = sorted(df_raw['region'].dropna().unique().tolist())
    selected_regions = st.multiselect(
        "Pilih Region",
        options=all_regions,
        default=all_regions
    )
    
    # Segment Filter
    all_segments = sorted(df_raw['segment'].dropna().unique().tolist())
    selected_segments = st.multiselect(
        "Pilih Segment Pelanggan",
        options=all_segments,
        default=all_segments
    )
    
    # Category & Sub-Category Filter
    st.markdown("### 📦 **Kategori Produk**")
    all_categories = sorted(df_raw['category'].dropna().unique().tolist())
    selected_categories = st.multiselect(
        "Pilih Kategori",
        options=all_categories,
        default=all_categories
    )
    
    # Filter Sub-Categories dynamically based on Category
    available_subcats = sorted(
        df_raw[df_raw['category'].isin(selected_categories if selected_categories else all_categories)]['sub_category']
        .dropna().unique().tolist()
    )
    selected_subcats = st.multiselect(
        "Pilih Sub-Kategori",
        options=available_subcats,
        default=available_subcats
    )
    
    # State Filter (Optional multi-select)
    available_states = sorted(
        df_raw[df_raw['region'].isin(selected_regions if selected_regions else all_regions)]['state']
        .dropna().unique().tolist()
    )
    selected_states = st.multiselect(
        "Pilih State (Opsional)",
        options=available_states,
        default=[]
    )
    
    st.divider()
    st.caption("💡 *Tip: Gunakan filter di atas untuk menganalisis performa bisnis berdasarkan segmen tertentu.*")

# ==========================================
# FILTERING DATA
# ==========================================
filtered_df = df_raw.copy()

# Date filter
filtered_df = filtered_df[
    (filtered_df['order_date'].dt.date >= start_date) & 
    (filtered_df['order_date'].dt.date <= end_date)
]

# Region filter
if selected_regions:
    filtered_df = filtered_df[filtered_df['region'].isin(selected_regions)]

# Segment filter
if selected_segments:
    filtered_df = filtered_df[filtered_df['segment'].isin(selected_segments)]

# Category filter
if selected_categories:
    filtered_df = filtered_df[filtered_df['category'].isin(selected_categories)]

# Sub-Category filter
if selected_subcats:
    filtered_df = filtered_df[filtered_df['sub_category'].isin(selected_subcats)]

# State filter
if selected_states:
    filtered_df = filtered_df[filtered_df['state'].isin(selected_states)]

# ==========================================
# MAIN DASHBOARD HEADER
# ==========================================
st.markdown("""
<div class="dashboard-header">
    <div class="dashboard-title">📈 Executive Dashboard — Superstore Sales & Profit</div>
    <div class="dashboard-subtitle">Ringkasan performa finansial, segmentasi pelanggan, analitik regional, dan efisiensi produk secara real-time.</div>
</div>
""", unsafe_allow_html=True)

if filtered_df.empty:
    st.warning("⚠️ Tidak ada data yang sesuai dengan kombinasi filter yang dipilih. Silakan sesuaikan filter pada sidebar.")
    st.stop()

# ==========================================
# EXECUTIVE KPI CARDS
# ==========================================
total_sales = filtered_df['sales'].sum()
total_profit = filtered_df['profit'].sum()
profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
total_orders = filtered_df['order_id'].nunique()
total_customers = filtered_df['customer_id'].nunique()
avg_order_value = (total_sales / total_orders) if total_orders > 0 else 0
avg_discount = filtered_df['discount'].mean() * 100

kpi_c1, kpi_c2, kpi_c3, kpi_c4, kpi_c5 = st.columns(5)

with kpi_c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">💰 Total Revenue</div>
        <div class="metric-value">${total_sales:,.0f}</div>
        <div class="metric-subtitle positive-delta">Total Penjualan</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_c2:
    margin_color = "positive-delta" if profit_margin >= 10 else ("negative-delta" if profit_margin < 0 else "")
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">📈 Net Profit</div>
        <div class="metric-value">${total_profit:,.0f}</div>
        <div class="metric-subtitle {margin_color}">Margin: <b>{profit_margin:.1f}%</b></div>
    </div>
    """, unsafe_allow_html=True)

with kpi_c3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">🛍️ Total Orders</div>
        <div class="metric-value">{total_orders:,}</div>
        <div class="metric-subtitle">Pesanan Unik</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_c4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">👥 Total Customers</div>
        <div class="metric-value">{total_customers:,}</div>
        <div class="metric-subtitle">Pelanggan Aktif</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_c5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">🎯 Avg. Order Value</div>
        <div class="metric-value">${avg_order_value:,.1f}</div>
        <div class="metric-subtitle">Rata-rata / Pesanan</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# DASHBOARD TABS
# ==========================================
tab_overview, tab_geo, tab_customer, tab_product, tab_data = st.tabs([
    "📊 Executive Overview",
    "🗺️ Regional & Geo Insights",
    "👥 Customer & Churn Analytics",
    "📦 Product & Pricing",
    "📋 Raw Data Explorer"
])

# ----------------------------------------------------
# TAB 1: EXECUTIVE OVERVIEW
# ----------------------------------------------------
with tab_overview:
    row1_left, row1_right = st.columns([7, 5])
    
    with row1_left:
        st.markdown("#### 📅 **Tren Penjualan & Laba Bulanan**")
        
        # Monthly aggregate
        monthly_df = filtered_df.groupby('year_month').agg(
            total_sales=('sales', 'sum'),
            total_profit=('profit', 'sum')
        ).reset_index().sort_values('year_month')
        
        fig_trend = go.Figure()
        
        fig_trend.add_trace(go.Scatter(
            x=monthly_df['year_month'],
            y=monthly_df['total_sales'],
            name="Revenue ($)",
            mode="lines+markers",
            line=dict(color="#3b82f6", width=3),
            fill='tozeroy',
            fillcolor='rgba(59, 130, 246, 0.1)'
        ))
        
        fig_trend.add_trace(go.Scatter(
            x=monthly_df['year_month'],
            y=monthly_df['total_profit'],
            name="Profit ($)",
            mode="lines+markers",
            line=dict(color="#10b981", width=2.5, dash="dot"),
            yaxis="y2"
        ))
        
        fig_trend.update_layout(
            height=380,
            margin=dict(l=20, r=20, t=30, b=30),
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis=dict(title="Periode (Tahun-Bulan)", showgrid=False),
            yaxis=dict(title="Revenue ($)", showgrid=True, gridcolor="#f1f5f9"),
            yaxis2=dict(
                title="Profit ($)",
                overlaying="y",
                side="right",
                showgrid=False
            ),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_trend, use_container_width=True)
        
    with row1_right:
        st.markdown("#### 🥧 **Kontribusi Penjualan per Segment**")
        segment_df = filtered_df.groupby('segment').agg(
            sales=('sales', 'sum'),
            profit=('profit', 'sum')
        ).reset_index()
        
        fig_segment = px.pie(
            segment_df,
            values='sales',
            names='segment',
            hole=0.48,
            color='segment',
            color_discrete_map={
                'Consumer': '#3b82f6',
                'Corporate': '#8b5cf6',
                'Home Office': '#06b6d4'
            }
        )
        fig_segment.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate="<b>%{label}</b><br>Sales: $%{value:,.0f}<br>Share: %{percent}"
        )
        fig_segment.update_layout(
            height=380,
            margin=dict(l=20, r=20, t=30, b=30),
            showlegend=False,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_segment, use_container_width=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Row 2: Sub-Category Breakdown & Profit Margins
    row2_left, row2_right = st.columns([6, 6])
    
    with row2_left:
        st.markdown("#### 📊 **Penjualan per Sub-Kategori**")
        subcat_df = filtered_df.groupby(['category', 'sub_category']).agg(
            sales=('sales', 'sum'),
            profit=('profit', 'sum')
        ).reset_index().sort_values('sales', ascending=True)
        
        fig_subcat = px.bar(
            subcat_df,
            x='sales',
            y='sub_category',
            color='category',
            orientation='h',
            labels={'sales': 'Total Sales ($)', 'sub_category': 'Sub-Kategori', 'category': 'Kategori'},
            color_discrete_sequence=['#3b82f6', '#10b981', '#f59e0b']
        )
        fig_subcat.update_layout(
            height=420,
            margin=dict(l=20, r=20, t=30, b=30),
            xaxis=dict(showgrid=True, gridcolor="#f1f5f9"),
            yaxis=dict(showgrid=False),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_subcat, use_container_width=True)
        
    with row2_right:
        st.markdown("#### 🎯 **Profit Margin per Sub-Kategori (%)**")
        subcat_df['profit_margin'] = (subcat_df['profit'] / subcat_df['sales']) * 100
        subcat_df = subcat_df.sort_values('profit_margin', ascending=True)
        
        colors = ['#ef4444' if m < 0 else '#10b981' for m in subcat_df['profit_margin']]
        
        fig_margin = go.Figure(go.Bar(
            x=subcat_df['profit_margin'],
            y=subcat_df['sub_category'],
            orientation='h',
            marker_color=colors,
            text=[f"{m:.1f}%" for m in subcat_df['profit_margin']],
            textposition='outside'
        ))
        
        fig_margin.update_layout(
            height=420,
            margin=dict(l=20, r=20, t=30, b=30),
            xaxis=dict(title="Profit Margin (%)", showgrid=True, gridcolor="#f1f5f9"),
            yaxis=dict(showgrid=False),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_margin, use_container_width=True)

# ----------------------------------------------------
# TAB 2: GEOGRAPHIC & REGIONAL INSIGHTS
# ----------------------------------------------------
with tab_geo:
    st.markdown("#### 🗺️ **Peta Sebaran Penjualan & Profit per State (US)**")
    
    state_df = filtered_df.groupby('state').agg(
        sales=('sales', 'sum'),
        profit=('profit', 'sum'),
        orders=('order_id', 'nunique')
    ).reset_index()
    state_df['profit_margin'] = (state_df['profit'] / state_df['sales']) * 100
    
    # State mapping dictionary for US 2-letter codes
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
    state_df['state_code'] = state_df['state'].map(us_state_to_code)
    
    geo_c1, geo_c2 = st.columns([8, 4])
    
    with geo_c1:
        fig_map = px.choropleth(
            state_df.dropna(subset=['state_code']),
            locations='state_code',
            locationmode="USA-states",
            color='sales',
            scope="usa",
            color_continuous_scale="Blues",
            hover_name='state',
            hover_data={'sales': ':$,.0f', 'profit': ':$,.0f', 'profit_margin': ':.1f%'},
            labels={'sales': 'Sales ($)', 'profit': 'Profit ($)', 'profit_margin': 'Margin'}
        )
        fig_map.update_layout(
            height=440,
            margin=dict(l=0, r=0, t=10, b=10),
            geo=dict(bgcolor='rgba(0,0,0,0)', lakecolor='#f8fafc')
        )
        st.plotly_chart(fig_map, use_container_width=True)
        
    with geo_c2:
        st.markdown("##### 🏆 **Top 5 State Berdasarkan Sales**")
        top_states = state_df.sort_values('sales', ascending=False).head(5)
        for _, row in top_states.iterrows():
            margin_badge = "🟢" if row['profit_margin'] >= 10 else ("🔴" if row['profit_margin'] < 0 else "🟡")
            st.markdown(f"""
            **{row['state']}**  
            Sales: **${row['sales']:,.0f}** | Profit: **${row['profit']:,.0f}** ({margin_badge} {row['profit_margin']:.1f}%)
            """)
            st.progress(min(1.0, float(row['sales'] / top_states['sales'].max())))
            st.divider()

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Heatmap: Region vs Category Profitability
    hm_left, hm_right = st.columns([6, 6])
    
    with hm_left:
        st.markdown("#### 🌡️ **Heatmap Profitability: Region vs Segment**")
        pivot_region_seg = filtered_df.pivot_table(
            index='region',
            columns='segment',
            values='profit',
            aggfunc='sum'
        ).fillna(0)
        
        fig_hm = px.imshow(
            pivot_region_seg,
            text_auto="$,.0f",
            color_continuous_scale="RdBu",
            aspect="auto",
            labels=dict(x="Segment", y="Region", color="Profit ($)")
        )
        fig_hm.update_layout(
            height=340,
            margin=dict(l=20, r=20, t=20, b=20),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_hm, use_container_width=True)
        
    with hm_right:
        st.markdown("#### 🚚 **Analisis Pengiriman (Ship Mode)**")
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
            labels={'sales': 'Sales ($)', 'ship_mode': 'Ship Mode', 'avg_days': 'Rata-rata Hari'},
            color_continuous_scale="Viridis"
        )
        fig_ship.update_layout(
            height=340,
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="#f1f5f9"),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_ship, use_container_width=True)

# ----------------------------------------------------
# TAB 3: CUSTOMER & CHURN ANALYTICS
# ----------------------------------------------------
with tab_customer:
    st.markdown("#### 👥 **Analisis Retensi & Churn Pelanggan**")
    
    # Calculate RFM / Churn metrics per customer
    ref_date = filtered_df['order_date'].max()
    
    cust_rfm = filtered_df.groupby('customer_id').agg(
        customer_name=('customer_name', 'first'),
        segment=('segment', 'first'),
        recency=('order_date', lambda x: (ref_date - x.max()).days),
        frequency=('order_id', 'nunique'),
        monetary=('sales', 'sum'),
        profit=('profit', 'sum')
    ).reset_index()
    
    # Churn Risk Definition (e.g. Inactive > 180 days)
    cust_rfm['churn_risk'] = np.where(
        cust_rfm['recency'] > 365, "Tinggi (Lost)",
        np.where(cust_rfm['recency'] > 180, "Sedang (At Risk)", "Rendah (Active)")
    )
    
    churn_c1, churn_c2, churn_c3 = st.columns([4, 4, 4])
    
    with churn_c1:
        churn_dist = cust_rfm['churn_risk'].value_counts().reset_index()
        churn_dist.columns = ['Status Churn', 'Jumlah Pelanggan']
        
        fig_churn = px.pie(
            churn_dist,
            values='Jumlah Pelanggan',
            names='Status Churn',
            hole=0.45,
            color='Status Churn',
            color_discrete_map={
                'Rendah (Active)': '#10b981',
                'Sedang (At Risk)': '#f59e0b',
                'Tinggi (Lost)': '#ef4444'
            }
        )
        fig_churn.update_layout(
            title="Distribusi Risiko Churn",
            height=320,
            margin=dict(l=10, r=10, t=40, b=10)
        )
        st.plotly_chart(fig_churn, use_container_width=True)
        
    with churn_c2:
        fig_rfm = px.scatter(
            cust_rfm,
            x='recency',
            y='monetary',
            size='frequency',
            color='churn_risk',
            hover_name='customer_name',
            labels={'recency': 'Hari Sejak Order Terakhir', 'monetary': 'Total Belanja ($)', 'churn_risk': 'Status'},
            color_discrete_map={
                'Rendah (Active)': '#10b981',
                'Sedang (At Risk)': '#f59e0b',
                'Tinggi (Lost)': '#ef4444'
            }
        )
        fig_rfm.update_layout(
            title="Recency vs Total Spending",
            height=320,
            margin=dict(l=10, r=10, t=40, b=10),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_rfm, use_container_width=True)
        
    with churn_c3:
        active_count = (cust_rfm['churn_risk'] == 'Rendah (Active)').sum()
        risk_count = (cust_rfm['churn_risk'] == 'Sedang (At Risk)').sum()
        lost_count = (cust_rfm['churn_risk'] == 'Tinggi (Lost)').sum()
        
        st.markdown("##### 📌 **Ringkasan Kesehatan Pelanggan**")
        st.info(f"🟢 **Active (< 180 hari):** {active_count} pelanggan ({(active_count/len(cust_rfm)*100):.1f}%)")
        st.warning(f"🟡 **At Risk (180-365 hari):** {risk_count} pelanggan ({(risk_count/len(cust_rfm)*100):.1f}%)")
        st.error(f"🔴 **Lost (> 365 hari):** {lost_count} pelanggan ({(lost_count/len(cust_rfm)*100):.1f}%)")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Top 10 Most Profitable Customers & Top 10 Loss-making Customers
    top_cust_col, bottom_cust_col = st.columns(2)
    
    with top_cust_col:
        st.markdown("#### 🌟 **Top 10 Pelanggan Paling Menguntungkan**")
        top_10_cust = cust_rfm.sort_values('profit', ascending=False).head(10)
        fig_top_c = px.bar(
            top_10_cust,
            x='profit',
            y='customer_name',
            orientation='h',
            color='profit',
            color_continuous_scale="Greens",
            labels={'profit': 'Total Profit ($)', 'customer_name': 'Pelanggan'}
        )
        fig_top_c.update_layout(
            height=380,
            margin=dict(l=20, r=20, t=20, b=20),
            yaxis=dict(autorange="reversed")
        )
        st.plotly_chart(fig_top_c, use_container_width=True)
        
    with bottom_cust_col:
        st.markdown("#### ⚠️ **Top 10 Pelanggan dengan Kerugian Tertinggi**")
        bottom_10_cust = cust_rfm.sort_values('profit', ascending=True).head(10)
        fig_bot_c = px.bar(
            bottom_10_cust,
            x='profit',
            y='customer_name',
            orientation='h',
            color='profit',
            color_continuous_scale="Reds_r",
            labels={'profit': 'Total Profit ($)', 'customer_name': 'Pelanggan'}
        )
        fig_bot_c.update_layout(
            height=380,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig_bot_c, use_container_width=True)

# ----------------------------------------------------
# TAB 4: PRODUCT & PRICING
# ----------------------------------------------------
with tab_product:
    st.markdown("#### 📦 **Performa Produk & Strategi Diskon**")
    
    prod_row1, prod_row2 = st.columns([6, 6])
    
    with prod_row1:
        st.markdown("##### 🏆 **Top 10 Produk Terlaris (Revenue)**")
        top_products = filtered_df.groupby('product_name').agg(
            sales=('sales', 'sum'),
            profit=('profit', 'sum')
        ).reset_index().sort_values('sales', ascending=False).head(10)
        
        fig_prod = px.bar(
            top_products,
            x='sales',
            y='product_name',
            orientation='h',
            color='profit',
            color_continuous_scale='Blues',
            labels={'sales': 'Sales ($)', 'product_name': 'Produk', 'profit': 'Profit ($)'}
        )
        fig_prod.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=20, b=20),
            yaxis=dict(autorange="reversed")
        )
        st.plotly_chart(fig_prod, use_container_width=True)
        
    with prod_row2:
        st.markdown("##### ⚠️ **Dampak Diskon Terhadap Margin Laba**")
        
        # Sample points to keep plotly snappy if dataset is huge
        sample_df = filtered_df.sample(min(len(filtered_df), 1500), random_state=42)
        
        fig_scatter = px.scatter(
            sample_df,
            x='discount',
            y='profit_margin',
            color='category',
            size='sales',
            hover_name='product_name',
            labels={'discount': 'Tingkat Diskon (0.0 - 1.0)', 'profit_margin': 'Profit Margin (%)', 'category': 'Kategori'},
            color_discrete_sequence=['#3b82f6', '#10b981', '#ef4444']
        )
        fig_scatter.add_hline(y=0, line_dash="dash", line_color="black", opacity=0.6)
        fig_scatter.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=20, b=20),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

# ----------------------------------------------------
# TAB 5: RAW DATA EXPLORER & EXPORT
# ----------------------------------------------------
with tab_data:
    st.markdown("#### 📋 **Eksplorasi Data & Unduh Laporan**")
    
    col_search, col_rows = st.columns([8, 4])
    with col_search:
        search_query = st.text_input("🔍 Cari Data (Ketik Nama Produk, Pelanggan, Kota, dll.)", "")
    with col_rows:
        num_rows = st.selectbox("Jumlah Baris Ditampilkan", options=[50, 100, 250, 500, "Semua"], index=0)
        
    display_df = filtered_df.copy()
    if search_query:
        mask = display_df.astype(str).apply(lambda row: row.str.contains(search_query, case=False).any(), axis=1)
        display_df = display_df[mask]
        
    st.caption(f"Menampilkan {len(display_df):,} dari total {len(filtered_df):,} transaksi yang difilter.")
    
    if num_rows == "Semua":
        st.dataframe(display_df, use_container_width=True, height=450)
    else:
        st.dataframe(display_df.head(int(num_rows)), use_container_width=True, height=450)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Export options
    exp_c1, exp_c2, _ = st.columns([3, 3, 6])
    
    with exp_c1:
        csv_data = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Data Filtered (CSV)",
            data=csv_data,
            file_name=f"superstore_filtered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
        
    with exp_c2:
        # Buffer for Excel
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            filtered_df.to_excel(writer, index=False, sheet_name='Superstore Data')
        
        st.download_button(
            label="📊 Download Data Filtered (Excel)",
            data=buffer.getvalue(),
            file_name=f"superstore_filtered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
