import streamlit as st
import pandas as pd
import numpy as np
import json
import io
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- CONFIGURATION & STYLING ---
st.set_page_config(page_title="Prosperity 4 Quant Dashboard", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    :root {
        --bg-primary: #06080c;
        --bg-surface: #0c1017;
        --bg-elevated: #111820;
        --bg-hover: #161d27;
        --accent-blue: #58A6FF;
        --accent-purple: #a855f7;
        --accent-cyan: #06d6a0;
        --accent-amber: #f59e0b;
        --border-subtle: #1a2030;
        --border-default: #222d3d;
        --text-primary: #f0f4f8;
        --text-secondary: #8899aa;
        --text-tertiary: #b5bcc7;
        --status-green: #3FB950;
        --status-red: #F85149;
        --status-amber: #f59e0b;
        --glow-blue: rgba(88, 166, 255, 0.08);
    }

    code, pre { font-family: 'JetBrains Mono', monospace !important; }

    .main, .stApp { background-color: var(--bg-primary) !important; }
    header { background-color: transparent !important; pointer-events: none !important; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    .stDeployButton { display: none; }

    .block-container { padding-top: 1.5rem !important; }
    [data-testid="stHeader"] { 
        background: transparent !important;
        pointer-events: none !important;
    }

    [data-testid="collapsedControl"] {
        top: 14px !important;
        left: 14px !important;
        background: var(--bg-surface) !important;
        border-radius: 6px !important;
        padding: 6px !important;
        border: 1px solid var(--border-default) !important;
        z-index: 999999 !important;
        pointer-events: auto !important;
        transition: all 0.2s ease !important;
    }

    [data-testid="collapsedControl"]:hover {
        border-color: var(--accent-blue) !important;
        background: var(--bg-hover) !important;
    }

    [data-testid="collapsedControl"] svg,
    button[data-testid="stSidebarCollapseButton"] svg {
        fill: white !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #000000 !important;
        border-right: 1px solid var(--border-subtle) !important;
    }

    /* Browse Files Button: Force black text for legibility */
    [data-testid="stFileUploader"] button {
        background-color: #ffffff !important;
        font-weight: 700 !important;
    }
    [data-testid="stFileUploader"] button:hover {
        color: var(--accent-blue) !important;
    }
    
    /* Hide the 'Remove file' (X) button */
    [data-testid="stFileUploaderDeleteBtn"] {
        display: none !important;
    }

    /* Force white color for all text inside uploader zone safely */
    .stFileUploader section p, 
    .stFileUploader section span, 
    .stFileUploader small { 
        color: white !important; 
    }
    [data-testid="stFileUploaderFileName"] { color: white !important; }



    h1, h2, h3 {
        color: var(--text-primary) !important;
        font-family: 'JetBrains Mono', monospace !important;
        letter-spacing: -0.5px;
    }


    h5 {
        margin-bottom: 12px !important;
        color: var(--text-secondary) !important;
        font-size: 10px !important;
        letter-spacing: 2.5px;
        font-weight: 700;
        text-transform: uppercase;
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* ---- METRIC CARDS ---- */
    [data-testid="stMetric"] {
        background-color: transparent !important;
        border: none !important;
        padding: 0 !important;
    }

    /* Animated border card wrappers */
    .card-wrapper {
        position: relative;
        padding: 1px;
        background: var(--border-subtle);
        overflow: hidden;
        border-radius: 6px;
        margin-bottom: 8px;
    }
    .card-wrapper::before {
        content: '';
        position: absolute;
        width: 200%; height: 200%;
        background: conic-gradient(transparent, transparent, transparent, transparent, var(--accent-blue));
        top: -50%; left: -50%;
        animation: rotate 6s linear infinite;
    }
    .card-wrapper.purple::before {
        background: conic-gradient(transparent, transparent, transparent, transparent, var(--accent-purple));
    }
    .card-wrapper.cyan::before {
        background: conic-gradient(transparent, transparent, transparent, transparent, var(--accent-cyan));
    }
    .card-wrapper.amber::before {
        background: conic-gradient(transparent, transparent, transparent, transparent, var(--accent-amber));
    }
    .card-wrapper.red::before {
        background: conic-gradient(transparent, transparent, transparent, transparent, var(--status-red));
    }
    .card-wrapper.green::before {
        background: conic-gradient(transparent, transparent, transparent, transparent, var(--status-green));
    }

    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    .metric-card {
        background-color: var(--bg-surface);
        padding: 8px 14px;
        position: relative;
        border-radius: 5px;
        z-index: 1;
        height: 100%;
    }
    .metric-label {
        color: var(--text-tertiary);
        font-family: 'JetBrains Mono', monospace;
        font-size: 9px;
        font-weight: 600;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 2px;
    }
    .metric-value {
        color: #ffffff;
        font-family: 'JetBrains Mono', monospace;
        font-size: 16px;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    .metric-sub {
        color: var(--text-tertiary);
        font-family: 'JetBrains Mono', monospace;
        font-size: 9px;
        font-weight: 400;
        margin-top: 2px;
    }
    .metric-value.pos { color: var(--status-green) !important; }
    .metric-value.neg { color: var(--status-red) !important; }
    .metric-value.amber { color: var(--status-amber) !important; }
    .metric-value.cyan { color: var(--accent-cyan) !important; }
    .metric-value.blue { color: var(--accent-blue) !important; }
    .metric-value.purple { color: var(--accent-purple) !important; }

    /* Metric grid layouts */
    .metric-grid-5 {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 8px;
        margin-bottom: 2px;
    }
    .metric-grid-4 {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 8px;
        margin-bottom: 2px;
    }
    .metric-grid-3 {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 8px;
        margin-bottom: 2px;
    }

    /* ---- HEADER ---- */
    .header-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 4px 0 10px 0;
        margin-bottom: 4px;
        border-bottom: 1px solid var(--border-subtle);
    }
    .blip-container {
        display: flex;
        align-items: center;
        gap: 8px;
        background: var(--glow-blue);
        padding: 5px 14px;
        border-radius: 6px;
        border: 1px solid rgba(88, 166, 255, 0.25);
        backdrop-filter: blur(8px);
    }
    .blip {
        width: 7px; height: 7px;
        background-color: var(--accent-blue);
        border-radius: 50%;
        position: relative;
    }
    .blip::after {
        content: '';
        position: absolute;
        width: 100%; height: 100%;
        background-color: var(--accent-blue);
        border-radius: 50%;
        animation: blip-pulse 2s infinite;
    }
    @keyframes blip-pulse {
        0%   { transform: scale(1);   opacity: 0.8; }
        70%  { transform: scale(3.5); opacity: 0;   }
        100% { transform: scale(1);   opacity: 0;   }
    }
    .blip-text {
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        font-weight: 700;
        color: var(--accent-blue);
        letter-spacing: 1.5px;
        text-transform: uppercase;
    }
    .title-text {
        font-family: 'JetBrains Mono', monospace;
        font-size: 14px;
        font-weight: 700;
        letter-spacing: -0.5px;
        color: #ffffff;
        text-transform: uppercase;
    }

    /* ---- SECTION LABELS ---- */
    .section-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        font-weight: 700;
        color: #ffffff !important;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin: 4px 0 2px 0 !important;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .section-label::after {
        content: '';
        flex: 1;
        height: 1px;
        background: var(--border-subtle);
    }

    /* Reduce Streamlit element gap for layout */
    .element-container { margin-bottom: 0px !important; }

    /* ---- BUTTONS ---- */
    .stButton > button {
        background-color: transparent !important;
        color: var(--text-secondary) !important;
        border: 1px solid var(--border-default) !important;
        border-radius: 4px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 9px !important;
        font-weight: 700;
        padding: 4px 14px !important;
        letter-spacing: 1px;
        transition: all 0.2s ease;
        text-transform: uppercase;
    }
    .stButton > button:hover,
    [data-testid="stFileUploader"] button:hover {
        border-color: var(--accent-blue) !important;
        color: var(--accent-blue) !important;
        background: rgba(88, 166, 255, 0.05) !important;
    }

    /* ---- FILE UPLOADER ---- */
    .stFileUploader section {
        background-color: var(--bg-surface) !important;
        border: 1px dashed var(--border-default) !important;
        border-radius: 6px !important;
        padding: 20px !important;
    }
    .stFileUploader section:hover {
        border-color: var(--accent-blue) !important;
    }
    .stFileUploader svg { fill: var(--accent-blue) !important; }
    /* Force white color for all text inside uploader zone */
    .stFileUploader section p, .stFileUploader section span, .stFileUploader small { 
        color: var(--accent-blue) !important; 
    }
    [data-testid="stFileUploaderFileName"] { color: white !important; }

    .stFileUploader button {
        background-color: black !important;
    }

    /* ---- SELECTS ---- */
    .stSelectbox label, .stMultiSelect label, .stRadio label {
        color: var(--text-secondary) !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 10px !important;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    div[data-baseweb="select"] > div {
        background-color: var(--bg-surface) !important;
        border: 1px solid var(--border-default) !important;
        color: var(--text-primary) !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 12px !important;
    }

    /* ---- SLIDER ---- */
    .stSlider label {
        color: var(--text-secondary) !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 10px !important;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    /* ---- ALERTS ---- */
    .stAlert div[role="alert"] {
        background: var(--bg-surface) !important;
        border: 1px solid var(--border-default) !important;
        color: var(--text-secondary) !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 11px !important;
    }

    /* ---- DIVIDER ---- */
    hr { border-color: var(--border-subtle) !important; opacity: 0.6; }

    /* ---- SUCCESS / INFO ---- */
    .stSuccess, .stInfo {
        background: var(--bg-surface) !important;
        border: 1px solid var(--border-default) !important;
    }

    /* ---- SIDEBAR EXTRAS ---- */
    [data-testid="stSidebarUserContent"] { padding-top: 0rem !important; }

    .sidebar-divider {
        border: none;
        border-top: 1px solid var(--border-subtle);
        margin: 16px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Colors for Plotly (kept identical to original)
IMC_BLUE = '#58A6FF'
PROFIT_GREEN = '#3FB950'
LOSS_RED = '#F85149'
BG_COLOR = '#06080c'
PANEL_BG = '#0c1017'
GRID_COLOR = '#1a2030'
TEXT_COLOR = '#8899aa'

LIMITS = {'ASH_COATED_OSMIUM': 80, 'INTARIAN_PEPPER_ROOT': 80}

# --- DATA PROCESSING (UNCHANGED) ---
@st.cache_data
def process_log_file(uploaded_file):
    try:
        content = uploaded_file.read().decode('utf-8')
        if content.startswith('[WARNING:'):
            content = content.split('\n\n', 1)[1]
        data = json.loads(content)
        
        csv_string = data.get('activitiesLog', '')
        if not csv_string: return None, None, None, "No activitiesLog found."
        df_market = pd.read_csv(io.StringIO(csv_string), sep=';')
        df_market = df_market.sort_values(['product', 'timestamp']).reset_index(drop=True)
        df_market['profit_and_loss'] = df_market.groupby('product')['profit_and_loss'].ffill().fillna(0)
        
        for i in range(1, 4):
            b_cols = [f'bid_volume_{j}' for j in range(1, i + 1)]
            a_cols = [f'ask_volume_{j}' for j in range(1, i + 1)]
            bid_vols = df_market[b_cols].fillna(0).sum(axis=1)
            ask_vols = df_market[a_cols].fillna(0).sum(axis=1)
            total_vols = bid_vols + ask_vols
            df_market[f'imbalance_l{i}'] = np.where(total_vols > 0, bid_vols / total_vols, 0.5)

        trades_list = data.get('tradeHistory', [])
        if isinstance(trades_list, str): trades_list = json.loads(trades_list)
        if not trades_list: df_trades = pd.DataFrame()
        else:
            df_trades = pd.DataFrame(trades_list)
            if 'symbol' in df_trades.columns: df_trades = df_trades.rename(columns={'symbol': 'product'})
            df_trades['is_our_buy'] = df_trades['buyer'] == 'SUBMISSION'
            df_trades['is_our_sell'] = df_trades['seller'] == 'SUBMISSION'

        telemetry_rows = []
        raw_logs = data.get('logs', [])
        product_map = {
            'ASH_COATED_OSMIUM': ['OSM', 'ASH', 'OSMIUM'],
            'INTARIAN_PEPPER_ROOT': ['PEP', 'INT', 'PEPPER', 'ROOT']
        }

        for entry in raw_logs:
            t = entry.get('timestamp', 0)
            ll = entry.get('lambdaLog', '')
            if not ll: continue
            
            for line in ll.split('\n'):
                if '|' not in line: continue
                
                parts = [p.strip() for p in line.split('|')]
                tag = parts[0]
                line_upper = line.upper()
                target_product = "UNKNOWN"
                
                for p_name, variants in product_map.items():
                    if any(v in line_upper for v in (variants + [p_name])):
                        target_product = p_name
                        break
                
                row = {'timestamp': t, 'tag': tag, 'target_product': target_product}
                
                for p in parts[1:]:
                    if ':' in p:
                        kv = p.split(':', 1)
                        key = kv[0].strip().lower().replace(" ", "_")
                        val = kv[1].strip()
                        try:
                            row[key] = float(val)
                        except:
                            row[key] = val
                telemetry_rows.append(row)
                
        df_telemetry = pd.DataFrame(telemetry_rows)
            
        return df_market, df_trades, df_telemetry, None

    except Exception as e: return None, None, None, f"Error: {str(e)}"

def calculate_exact_position(df_market_product, df_trades_product):
    if df_trades_product.empty:
        df_market_product['exact_position'] = 0
        return df_market_product
    df_pos_changes = df_trades_product.copy()
    
    # Corrected: Only count trades where our bot participated
    df_pos_changes['qty_change'] = 0
    df_pos_changes.loc[df_pos_changes['is_our_buy'], 'qty_change'] += df_pos_changes['quantity']
    df_pos_changes.loc[df_pos_changes['is_our_sell'], 'qty_change'] -= df_pos_changes['quantity']
    
    # Correct Bucketing: Map granular trade timestamps to the NEXT market tick (multiples of 100)
    df_pos_changes['tick'] = (np.ceil(df_pos_changes['timestamp'] / 100.0) * 100).astype(int)
    pos_grouped = df_pos_changes.groupby('tick')['qty_change'].sum()
    
    df_market_product = df_market_product.set_index('timestamp')
    # Reindex using the next-tick mapping ensures no trades are dropped
    df_market_product['exact_position'] = pos_grouped.reindex(df_market_product.index).fillna(0).cumsum()
    df_market_product = df_market_product.reset_index()
    return df_market_product

# --- VISUALIZATIONS (logic unchanged, colors updated to match new theme) ---
def plot_pnl_inventory(df, selected_product):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    limit = LIMITS.get(selected_product, 80)
    
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['profit_and_loss'], name="Cumulative PnL", line=dict(color=IMC_BLUE, width=2), hoverinfo='skip'), secondary_y=False)
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['exact_position'], name="Inventory (+/-)", fill='tozeroy', line=dict(color='#556677', width=1, shape='hv'), fillcolor='rgba(85, 102, 119, 0.15)', hoverinfo='skip'), secondary_y=True)
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['profit_and_loss'], name="Metrics", mode='lines', line=dict(color='rgba(0,0,0,0)'), customdata=df['exact_position'], hovertemplate="PnL: %{y:,.0f} Xirecs<br>Inventory: %{customdata} Lots<extra></extra>", showlegend=False), secondary_y=False)
    
    fig.add_shape(type="line", x0=0, x1=1, xref="x domain", y0=limit, y1=limit, yref="y2", line=dict(color=LOSS_RED, width=1, dash="dash"))
    fig.add_shape(type="line", x0=0, x1=1, xref="x domain", y0=-limit, y1=-limit, yref="y2", line=dict(color=LOSS_RED, width=1, dash="dash"))
    fig.add_annotation(x=1.0, y=limit, text=str(limit), showarrow=False, xref="paper", yref="y2", font=dict(color=LOSS_RED, size=12, family="JetBrains Mono"), xanchor="right", xshift=-5)
    fig.add_annotation(x=1.0, y=-limit, text=str(-limit), showarrow=False, xref="paper", yref="y2", font=dict(color=LOSS_RED, size=12, family="JetBrains Mono"), xanchor="right", xshift=-5)

    fig.update_layout(
        title=dict(text="MACRO VIEW — PNL vs. INVENTORY LOCK", font=dict(color="#ffffff", size=11, family="JetBrains Mono"), x=0),
        plot_bgcolor=BG_COLOR, paper_bgcolor=PANEL_BG,
        font=dict(color="#ffffff", family="JetBrains Mono"),
        xaxis=dict(showgrid=True, gridcolor=GRID_COLOR, title="", range=[0, df['timestamp'].max()], tickfont=dict(size=9, color="#ffffff"), linecolor=GRID_COLOR),
        yaxis=dict(showgrid=True, gridcolor=GRID_COLOR, title=dict(text="PnL (Xirecs)", font=dict(color="#ffffff")), tickfont=dict(size=9, color="#ffffff")),
        yaxis2=dict(showgrid=False, title=dict(text="Net Position (Lots)", font=dict(color="#ffffff")), tickfont=dict(size=9, color="#ffffff"), range=[-(limit+20), limit+20]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color="#ffffff", size=9, family="JetBrains Mono")),
        margin=dict(l=0, r=40, t=15, b=0),
        hovermode="x",
    )
    return fig

def plot_microstructure_xray(df_mkt, df_trd):
    fig = go.Figure()
    l2_bid, l2_ask = df_mkt['bid_price_2'].fillna(df_mkt['bid_price_1']), df_mkt['ask_price_2'].fillna(df_mkt['ask_price_1'])
    df_mkt['l2_mid'] = (l2_bid + l2_ask) / 2.0
    l3_bid, l3_ask = df_mkt['bid_price_3'].fillna(l2_bid), df_mkt['ask_price_3'].fillna(l2_ask)
    df_mkt['l3_mid'] = (l3_bid + l3_ask) / 2.0

    # --- RAW BID/ASK LINES (Hidden by default, grouped by Level) ---
    # Level 1
    fig.add_trace(go.Scatter(x=df_mkt['timestamp'], y=df_mkt['bid_price_1'], mode='lines', name='L1 Bid', line=dict(color='rgba(63, 185, 80, 0.8)', width=1), visible='legendonly', legendgroup='L1', legendgrouptitle_text='L1 BA'))
    fig.add_trace(go.Scatter(x=df_mkt['timestamp'], y=df_mkt['ask_price_1'], mode='lines', name='L1 Ask', line=dict(color='rgba(248, 81, 73, 0.8)', width=1), visible='legendonly', legendgroup='L1'))
    
    # Level 2
    fig.add_trace(go.Scatter(x=df_mkt['timestamp'], y=df_mkt['bid_price_2'], mode='lines', name='L2 Bid', line=dict(color='rgba(63, 185, 80, 0.5)', width=1, dash='dash'), visible='legendonly', legendgroup='L2', legendgrouptitle_text='L2 BA'))
    fig.add_trace(go.Scatter(x=df_mkt['timestamp'], y=df_mkt['ask_price_2'], mode='lines', name='L2 Ask', line=dict(color='rgba(248, 81, 73, 0.5)', width=1, dash='dash'), visible='legendonly', legendgroup='L2'))
    
    # Level 3
    fig.add_trace(go.Scatter(x=df_mkt['timestamp'], y=df_mkt['bid_price_3'], mode='lines', name='L3 Bid', line=dict(color='rgba(63, 185, 80, 0.3)', width=1, dash='dot'), visible='legendonly', legendgroup='L3', legendgrouptitle_text='L3 BA'))
    fig.add_trace(go.Scatter(x=df_mkt['timestamp'], y=df_mkt['ask_price_3'], mode='lines', name='L3 Ask', line=dict(color='rgba(248, 81, 73, 0.3)', width=1, dash='dot'), visible='legendonly', legendgroup='L3'))

    fig.add_trace(go.Scatter(x=df_mkt['timestamp'], y=df_mkt['mid_price'], mode='lines', name='L1 Mid', line=dict(color='#f0f4f8', width=2), opacity=0.9))
    fig.add_trace(go.Scatter(x=df_mkt['timestamp'], y=df_mkt['l2_mid'], mode='lines', name='L2 Mid', line=dict(color='#556677', width=1, dash='dash'), opacity=0.6))
    fig.add_trace(go.Scatter(x=df_mkt['timestamp'], y=df_mkt['l3_mid'], mode='lines', name='L3 Mid (Wall)', line=dict(color=IMC_BLUE, width=1, dash='dot'), opacity=0.6))

    if not df_trd.empty:
        m_buy  = df_trd[df_trd['is_our_buy']  & ~df_trd['is_taker']]
        t_buy  = df_trd[df_trd['is_our_buy']  &  df_trd['is_taker']]
        m_sell = df_trd[df_trd['is_our_sell'] & ~df_trd['is_taker']]
        t_sell = df_trd[df_trd['is_our_sell'] &  df_trd['is_taker']]
        
        def add_exec(df_sub, name, color, symbol, is_hollow):
            if df_sub.empty: return
            fig.add_trace(go.Scatter(
                x=df_sub['timestamp'], y=df_sub['price'], mode='markers', name=name,
                marker=dict(symbol=symbol, size=df_sub['quantity'] * 2, sizemin=8,
                            color=color if not is_hollow else 'rgba(0,0,0,0)',
                            line=dict(width=2, color=color)),
                text=df_sub['quantity'],
                hovertemplate=f"{name}: %{{text}} lots @ %{{y}}<extra></extra>"
            ))

        add_exec(m_buy,  "MAKER BOUGHT", PROFIT_GREEN, 'triangle-up',   False)
        add_exec(m_sell, "MAKER SOLD",   LOSS_RED,     'triangle-down', False)
        add_exec(t_buy,  "TAKER BOUGHT", PROFIT_GREEN, 'circle',        True)
        add_exec(t_sell, "TAKER SOLD",   LOSS_RED,     'circle',        True)

    fig.update_layout(
        title=dict(text="MICROSTRUCTURE X-RAY — EXECUTIONS vs. TRUE PRICE", font=dict(color="#ffffff", size=11, family="JetBrains Mono"), x=0),
        plot_bgcolor=BG_COLOR, paper_bgcolor=PANEL_BG,
        font=dict(color="#ffffff", family="JetBrains Mono"),
        xaxis=dict(showgrid=True, gridcolor=GRID_COLOR, title="", range=[0, df_mkt['timestamp'].max()], tickfont=dict(size=9, color="#ffffff")),
        yaxis=dict(showgrid=True, gridcolor=GRID_COLOR, title=dict(text="Price Level", font=dict(color="#ffffff")), tickfont=dict(size=9, color="#ffffff")),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color="#ffffff", size=9, family="JetBrains Mono")),
        margin=dict(l=0, r=40, t=40, b=0),
        hovermode="x unified"
    )
    return fig

def plot_toxicity_markout(m_trades, markout_horizon):
    fig = go.Figure()
    if m_trades.empty or 'm_edge' not in m_trades.columns:
        fig.update_layout(title=dict(text="PANEL 1 — NO TRADES TO ANALYZE", font=dict(color="#ffffff", size=11, family="JetBrains Mono"), x=0), plot_bgcolor=BG_COLOR, paper_bgcolor=PANEL_BG)
        return fig
    
    colors = np.where(m_trades['m_edge'] >= 0, PROFIT_GREEN, LOSS_RED)
    
    fig.add_trace(go.Scatter(
        x=m_trades['timestamp'], y=m_trades['price'], mode='markers', name='Executions',
        marker=dict(color=colors, size=m_trades['quantity'] * 1.5, sizemin=6,
                    line=dict(width=1, color='rgba(255,255,255,0.2)'), opacity=0.85),
        customdata=m_trades['m_edge'],
        hovertemplate="Time: %{x}<br>Exec Price: %{y}<br>Markout Edge: %{customdata:.2f} ticks<br>Volume: %{text} lots<extra></extra>",
        text=m_trades['quantity']
    ))
    fig.update_layout(
        title=dict(text=f"PANEL 1 — TOXICITY & MARKOUT (T+{markout_horizon*100})", font=dict(color="#ffffff", size=11, family="JetBrains Mono"), x=0),
        plot_bgcolor=BG_COLOR, paper_bgcolor=PANEL_BG,
        font=dict(color="#ffffff", family="JetBrains Mono"),
        xaxis=dict(showgrid=True, gridcolor=GRID_COLOR, title="", tickfont=dict(size=9, color="#ffffff")),
        yaxis=dict(showgrid=True, gridcolor=GRID_COLOR, title=dict(text="Execution Price", font=dict(color="#ffffff")), tickfont=dict(size=9, color="#ffffff")),
        margin=dict(l=0, r=40, t=40, b=0)
    )
    return fig

def plot_spread_capture(our_trades, df_mkt):
    if our_trades.empty: return go.Figure()
    
    trades_with_mid = pd.merge_asof(our_trades.sort_values('timestamp'), df_mkt[['timestamp', 'mid_price']].sort_values('timestamp'), on='timestamp')
    trades_with_mid['quoted_edge'] = np.where(trades_with_mid['is_our_buy'], trades_with_mid['mid_price'] - trades_with_mid['price'], trades_with_mid['price'] - trades_with_mid['mid_price'])
    
    fig = go.Figure()
    
    # Trace 1: Quoted Edge
    fig.add_trace(go.Box(
        x=['Quoted Edge'] * len(trades_with_mid),
        y=trades_with_mid['quoted_edge'],
        marker_color=IMC_BLUE,
        fillcolor='rgba(88, 166, 255, 0.4)',
        line_color=IMC_BLUE,
        boxpoints='outliers',
        jitter=0.3,
        pointpos=-1.8,
        name="",
        hoverinfo="y"
    ))
    
    # Trace 2: Realized Edge
    if 'm_edge' in trades_with_mid.columns:
        fig.add_trace(go.Box(
            x=['Realized Edge (Markout)'] * len(trades_with_mid),
            y=trades_with_mid['m_edge'],
            marker_color=PROFIT_GREEN,
            fillcolor='rgba(63, 185, 80, 0.4)',
            line_color=PROFIT_GREEN,
            boxpoints='outliers',
            jitter=0.3,
            pointpos=-1.8,
            name="",
            hoverinfo="y"
        ))
    
    fig.update_layout(
        title=dict(text="PANEL 2 — QUOTED vs. REALIZED SPREAD EDGE", font=dict(color="#ffffff", size=11, family="JetBrains Mono"), x=0),
        plot_bgcolor=BG_COLOR, paper_bgcolor=PANEL_BG,
        font=dict(color="#ffffff", family="JetBrains Mono"),
        yaxis=dict(title=dict(text="Edge (Ticks)", font=dict(color="#ffffff")), zeroline=True, zerolinewidth=1, zerolinecolor=GRID_COLOR, showgrid=True, gridcolor=GRID_COLOR, tickfont=dict(size=9, color="#ffffff")),
        xaxis=dict(tickfont=dict(size=9, color="#ffffff")),
        showlegend=False,
        margin=dict(l=0, r=40, t=40, b=0)
    )
    return fig

def plot_imbalance_matrix(m_trades, df_mkt, imbalance_level):
    if m_trades.empty or 'm_edge' not in m_trades.columns: return go.Figure()
    
    imbalance_col = f'imbalance_l{imbalance_level}'
    m_trades_imb = pd.merge(m_trades, df_mkt[['timestamp', imbalance_col]], on='timestamp', how='left')
    colors = np.where(m_trades_imb['m_edge'] >= 0, PROFIT_GREEN, LOSS_RED)
    
    fig = go.Figure(data=go.Scatter(
        x=m_trades_imb[imbalance_col], y=m_trades_imb['m_edge'], mode='markers',
        marker=dict(color=colors, size=m_trades_imb['quantity'] * 1.5, sizemin=6,
                    opacity=0.75, line=dict(width=1, color='rgba(255,255,255,0.1)')),
        hovertemplate=f"L{imbalance_level} Imbalance: %{{x:.2f}}<br>Markout Edge: %{{y:.2f}} ticks<br>Volume: %{{text}} lots<extra></extra>",
        text=m_trades_imb['quantity']
    ))
    
    fig.update_layout(
        title=dict(text=f"PANEL 3 — L{imbalance_level} IMBALANCE vs. PROFITABILITY", font=dict(color="#ffffff", size=11, family="JetBrains Mono"), x=0),
        xaxis=dict(title=dict(text=f"L{imbalance_level} Order Book Imbalance", font=dict(color="#ffffff")), range=[0, 1], showgrid=True, gridcolor=GRID_COLOR, tickfont=dict(size=9, color="#ffffff")),
        yaxis=dict(title=dict(text="Trade Markout (Ticks)", font=dict(color="#ffffff")), showgrid=True, gridcolor=GRID_COLOR, tickfont=dict(size=9, color="#ffffff")),
        plot_bgcolor=BG_COLOR, paper_bgcolor=PANEL_BG,
        font=dict(color="#ffffff", family="JetBrains Mono"),
        margin=dict(l=0, r=40, t=40, b=0)
    )
    return fig

def plot_whale_profiler(df_trd):
    if df_trd.empty: return go.Figure()
    
    mkt_trades = df_trd[(~df_trd['is_our_buy']) & (~df_trd['is_our_sell'])]
    if mkt_trades.empty: return go.Figure()
    
    fig = go.Figure(data=[go.Histogram(x=mkt_trades['quantity'], nbinsx=50, marker_color=IMC_BLUE, opacity=0.75, marker_line_color=GRID_COLOR, marker_line_width=0.5)])
    fig.update_layout(
        title=dict(text="PANEL 4 — MARKET FLOW / VOLUME PROFILER", font=dict(color="#ffffff", size=11, family="JetBrains Mono"), x=0),
        xaxis=dict(title=dict(text="Trade Volume (Lots)", font=dict(color="#ffffff")), showgrid=True, gridcolor=GRID_COLOR, tickfont=dict(size=9, color="#ffffff")),
        yaxis=dict(title=dict(text="Frequency", font=dict(color="#ffffff")), showgrid=True, gridcolor=GRID_COLOR, tickfont=dict(size=9, color="#ffffff")),
        plot_bgcolor=BG_COLOR, paper_bgcolor=PANEL_BG,
        font=dict(color="#ffffff", family="JetBrains Mono"),
        margin=dict(l=0, r=40, t=40, b=0)
    )
    return fig



def plot_magic_size_fingerprinter(df_mkt, df_trd, markout_horizon):
    if df_trd.empty: return go.Figure()
    
    # 1. Filter for NPC trades
    npc_trades = df_trd[(~df_trd['is_our_buy']) & (~df_trd['is_our_sell'])].copy()
    if npc_trades.empty: return go.Figure()
    
    # 2. Determine trade direction (heuristic based on L1 quotes)
    # L1 quotes are already merged into df_trd in the main block
    npc_trades['is_npc_buy'] = npc_trades['price'] >= npc_trades['ask_price_1']
    npc_trades['is_npc_sell'] = npc_trades['price'] <= npc_trades['bid_price_1']
    
    # 3. Calculate Markout at T+horizon
    df_mkt_future = df_mkt[['timestamp', 'mid_price']].copy()
    df_mkt_future['timestamp'] = df_mkt_future['timestamp'] - (markout_horizon * 100)
    df_mkt_future = df_mkt_future.rename(columns={'mid_price': 'future_mid'})
    
    m_trades = pd.merge(npc_trades, df_mkt_future, on='timestamp', how='inner')
    if m_trades.empty: return go.Figure()
    
    m_trades['npc_edge'] = np.where(m_trades['is_npc_buy'], m_trades['future_mid'] - m_trades['price'], m_trades['price'] - m_trades['future_mid'])
    
    # Filter out trades where we couldn't determine direction clearly
    m_trades = m_trades[m_trades['is_npc_buy'] | m_trades['is_npc_sell']]

    fig = go.Figure()
    
    # Trace for NPC Edge
    fig.add_trace(go.Box(
        x=m_trades['quantity'],
        y=m_trades['npc_edge'],
        marker_color=IMC_BLUE,
        fillcolor='rgba(88, 166, 255, 0.4)',
        line_color=IMC_BLUE,
        boxpoints='outliers',
        jitter=0.3,
        pointpos=-1.8,
        name="NPC Edge",
        hoverinfo="y",
        hovertemplate="Size: %{x}<br>NPC Edge: %{y:.2f}<extra></extra>"
    ))
    
    fig.update_layout(
        title=dict(text=f"MAGIC SIZE FINGERPRINTER (NPC EDGE T+{markout_horizon*100})", font=dict(color="#ffffff", size=11, family="JetBrains Mono"), x=0),
        plot_bgcolor=BG_COLOR, paper_bgcolor=PANEL_BG,
        font=dict(color="#ffffff", family="JetBrains Mono"),
        yaxis=dict(title=dict(text="NPC Markout Edge (Ticks)", font=dict(color="#ffffff")), zeroline=True, zerolinewidth=1, zerolinecolor=GRID_COLOR, showgrid=True, gridcolor=GRID_COLOR, tickfont=dict(size=9, color="#ffffff")),
        xaxis=dict(title=dict(text="Trade Size (Lots)", font=dict(color="#ffffff")), type='category', tickfont=dict(size=9, color="#ffffff"), categoryorder='category ascending'),
        showlegend=False,
        margin=dict(l=0, r=40, t=40, b=0)
    )
    return fig

def plot_liquidation_radar(df_mkt, df_trd):
    if df_trd.empty: return go.Figure()
    
    npc_trades = df_trd[(~df_trd['is_our_buy']) & (~df_trd['is_our_sell'])].copy()
    if npc_trades.empty: return go.Figure()
    
    # L1 quotes are already merged into df_trd in the main block
    npc_trades['is_npc_buy'] = npc_trades['price'] >= npc_trades['ask_price_1']
    npc_trades['is_npc_sell'] = npc_trades['price'] <= npc_trades['bid_price_1']
    
    npc_trades['signed_vol'] = 0
    npc_trades.loc[npc_trades['is_npc_buy'], 'signed_vol'] = npc_trades['quantity']
    npc_trades.loc[npc_trades['is_npc_sell'], 'signed_vol'] = -npc_trades['quantity']
    
    # Map back to market timestamps to keep alignment with price
    # We calculate the sum of signed volume for each market tick, then cumulative sum
    npc_trades['tick'] = (np.ceil(npc_trades['timestamp'] / 100.0) * 100).astype(int)
    flow_grouped = npc_trades.groupby('tick')['signed_vol'].sum()
    
    df_mkt_flow = df_mkt.set_index('timestamp').copy()
    df_mkt_flow['net_flow_cum'] = flow_grouped.reindex(df_mkt_flow.index).fillna(0).cumsum()
    df_mkt_flow = df_mkt_flow.reset_index()

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(go.Scatter(x=df_mkt_flow['timestamp'], y=df_mkt_flow['mid_price'], name="Mid Price", line=dict(color='#f0f4f8', width=2), opacity=0.6, hoverinfo='skip'), secondary_y=False)
    fig.add_trace(go.Scatter(x=df_mkt_flow['timestamp'], y=df_mkt_flow['net_flow_cum'], name="Cumulative NPC Flow", fill='tozeroy', line=dict(color=IMC_BLUE, width=1), fillcolor='rgba(88, 166, 255, 0.15)', hoverinfo='skip'), secondary_y=True)
    
    fig.add_trace(go.Scatter(x=df_mkt_flow['timestamp'], y=df_mkt_flow['mid_price'], name="Metrics", mode='lines', line=dict(color='rgba(0,0,0,0)'), customdata=df_mkt_flow['net_flow_cum'], hovertemplate="Mid Price: %{y:,.1f}<br>Net Flow: %{customdata} lots<extra></extra>", showlegend=False), secondary_y=False)

    fig.update_layout(
        title=dict(text="LIQUIDATION RADAR (CUMULATIVE NPC FLOW)", font=dict(color="#ffffff", size=11, family="JetBrains Mono"), x=0),
        plot_bgcolor=BG_COLOR, paper_bgcolor=PANEL_BG,
        font=dict(color="#ffffff", family="JetBrains Mono"),
        xaxis=dict(showgrid=True, gridcolor=GRID_COLOR, title="", range=[0, df_mkt['timestamp'].max()], tickfont=dict(size=9, color="#ffffff"), linecolor=GRID_COLOR),
        yaxis=dict(showgrid=True, gridcolor=GRID_COLOR, title=dict(text="Mid Price", font=dict(color="#ffffff")), tickfont=dict(size=9, color="#ffffff")),
        yaxis2=dict(showgrid=False, title=dict(text="Net NPC Flow (Lots)", font=dict(color="#ffffff")), tickfont=dict(size=9, color="#ffffff")),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color="#ffffff", size=9, family="JetBrains Mono")),
        margin=dict(l=0, r=40, t=40, b=0),
        hovermode="x",
    )
    return fig

def plot_true_mid_divergence(df_mkt):
    if df_mkt.empty: return go.Figure()
    
    df = df_mkt.copy()
    
    # Calculate True Mid based on L3 (The Wall) with graceful degradation
    
    # BIDS
    l2_bid = df['bid_price_2'].fillna(df['bid_price_1'])
    l3_bid = df['bid_price_3'].fillna(l2_bid)
    
    # ASKS
    l2_ask = df['ask_price_2'].fillna(df['ask_price_1'])
    l3_ask = df['ask_price_3'].fillna(l2_ask)
    
    df['wall_mid'] = (l3_bid + l3_ask) / 2.0
    
    fig = go.Figure()
    
    # Fake Mid (Noisy, Pennying)
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['mid_price'], mode='lines', name='L1 Mid (Fade)', line=dict(color='#556677', width=1, dash='dot'), opacity=0.8, hovertemplate="Fake Mid: %{y:.1f}<extra></extra>"))
    
    # True Mid (Wall Mid, Structural)
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['wall_mid'], mode='lines', name='L3 Wall Mid (True)', line=dict(color=IMC_BLUE, width=2), hovertemplate="True Mid: %{y:.1f}<extra></extra>"))
    
    # Shade the divergence (when L1 Mid disconnects from Wall Mid)
    df['divergence'] = df['mid_price'] - df['wall_mid']
    
    fig.update_layout(
        title=dict(text=f"L3 WALL MID vs. L1 MID DIVERGENCE", font=dict(color="#ffffff", size=11, family="JetBrains Mono"), x=0),
        plot_bgcolor=BG_COLOR, paper_bgcolor=PANEL_BG,
        font=dict(color="#ffffff", family="JetBrains Mono"),
        xaxis=dict(showgrid=True, gridcolor=GRID_COLOR, title="", range=[0, df['timestamp'].max()], tickfont=dict(size=9, color="#ffffff")),
        yaxis=dict(showgrid=True, gridcolor=GRID_COLOR, title=dict(text="Price", font=dict(color="#ffffff")), tickfont=dict(size=9, color="#ffffff")),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color="#ffffff", size=9, family="JetBrains Mono")),
        margin=dict(l=0, r=40, t=40, b=0),
        hovermode="x unified"
    )
    return fig

def plot_vwap_momentum(df_mkt, df_trd, rolling_window=10):
    if df_trd.empty: return go.Figure()
    
    # Calculate VWAP of ALL market trades per tick
    df_t = df_trd.copy()
    df_t['tick'] = (np.ceil(df_t['timestamp'] / 100.0) * 100).astype(int)
    df_t['notional'] = df_t['price'] * df_t['quantity']
    
    # Aggregate volume and notional per tick
    tick_agg = df_t.groupby('tick').agg({'quantity': 'sum', 'notional': 'sum'}).reset_index()
    tick_agg['tick_vwap'] = tick_agg['notional'] / tick_agg['quantity']
    
    # Merge with Market Data
    df = df_mkt[['timestamp', 'mid_price']].copy()
    df = pd.merge(df, tick_agg, left_on='timestamp', right_on='tick', how='left')
    
    # Calculate Rolling VWAP
    # We use a rolling sum of notional and volume to properly weight the VWAP over time
    df['roll_vol'] = df['quantity'].fillna(0).rolling(window=rolling_window, min_periods=1).sum()
    df['roll_notional'] = df['notional'].fillna(0).rolling(window=rolling_window, min_periods=1).sum()
    
    # Only calculate VWAP where there is volume, otherwise fallback to 0 difference
    df['rolling_vwap'] = np.where(df['roll_vol'] > 0, df['roll_notional'] / df['roll_vol'], df['mid_price'])
    
    # The Oscillator: Rolling VWAP - Resting Mid Price
    df['vwap_momentum'] = df['rolling_vwap'] - df['mid_price']
    
    fig = go.Figure()
    
    # The Zero Line (Resting L1 Mid)
    fig.add_trace(go.Scatter(x=df['timestamp'], y=[0]*len(df), mode='lines', name='Resting Mid Baseline', line=dict(color='#556677', width=1), hoverinfo='skip'))
    
    # The Histogram (Momentum)
    colors = np.where(df['vwap_momentum'] >= 0, PROFIT_GREEN, LOSS_RED)
    
    fig.add_trace(go.Bar(
        x=df['timestamp'],
        y=df['vwap_momentum'],
        marker_color=colors,
        name='VWAP Momentum',
        opacity=0.8,
        hovertemplate="Momentum: %{y:.2f} ticks<extra></extra>"
    ))
    
    fig.update_layout(
        title=dict(text=f"VWAP MOMENTUM CROSSOVER ({rolling_window}-TICK ROLL)", font=dict(color="#ffffff", size=11, family="JetBrains Mono"), x=0),
        plot_bgcolor=BG_COLOR, paper_bgcolor=PANEL_BG,
        font=dict(color="#ffffff", family="JetBrains Mono"),
        xaxis=dict(showgrid=True, gridcolor=GRID_COLOR, title="", range=[0, df['timestamp'].max()], tickfont=dict(size=9, color="#ffffff")),
        yaxis=dict(title=dict(text="VWAP vs Mid (Ticks)", font=dict(color="#ffffff")), zeroline=True, zerolinewidth=1, zerolinecolor=GRID_COLOR, showgrid=True, gridcolor=GRID_COLOR, tickfont=dict(size=9, color="#ffffff")),
        showlegend=False,
        margin=dict(l=0, r=40, t=40, b=0),
        hovermode="x unified"
    )
    return fig

def plot_telemetry_brainwaves(df_mkt, df_trd, df_tel, selected_signals):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    if df_mkt.empty: return fig
    
    # 1. Baseline: Market Mid Price
    fig.add_trace(
        go.Scatter(x=df_mkt['timestamp'], y=df_mkt['mid_price'], mode='lines', name='L1 Mid Price', line=dict(color='#f0f4f8', width=2), opacity=0.7),
        secondary_y=False
    )
    
    # 2. Executions (To see EXACTLY when the bot acted based on the signals)
    if not df_trd.empty:
        our_buys = df_trd[df_trd['is_our_buy']]
        our_sells = df_trd[df_trd['is_our_sell']]
        
        if not our_buys.empty:
            fig.add_trace(go.Scatter(
                x=our_buys['timestamp'], y=our_buys['price'], mode='markers', name='Our Buys',
                marker=dict(symbol='triangle-up', size=10, color=PROFIT_GREEN, line=dict(width=1, color='white')),
                hovertemplate="BOUGHT %{text} @ %{y}<extra></extra>", text=our_buys['quantity']
            ), secondary_y=False)
            
        if not our_sells.empty:
            fig.add_trace(go.Scatter(
                x=our_sells['timestamp'], y=our_sells['price'], mode='markers', name='Our Sells',
                marker=dict(symbol='triangle-down', size=10, color=LOSS_RED, line=dict(width=1, color='white')),
                hovertemplate="SOLD %{text} @ %{y}<extra></extra>", text=our_sells['quantity']
            ), secondary_y=False)

    # 3. The Brainwaves (Telemetry Signals)
    if not df_tel.empty and selected_signals:
        # Get typical market price to determine if a signal needs a secondary axis
        avg_price = df_mkt['mid_price'].mean() if not df_mkt['mid_price'].isna().all() else 10000
        
        color_palette = [IMC_BLUE, '#a855f7', '#06d6a0', '#f59e0b', '#ff6b6b', '#4ecdc4', '#ffe66d']
        
        for i, sig in enumerate(selected_signals):
            if sig not in df_tel.columns: continue
            
            sig_data = df_tel[['timestamp', sig]].dropna()
            if sig_data.empty: continue
            
            # Determine Axis
            # If the signal's mean magnitude is tiny compared to the price (e.g., a Z-Score of 2.5 vs a price of 10000), 
            # or if it's negative, put it on the secondary Y-axis.
            sig_mean_abs = sig_data[sig].abs().mean()
            use_secondary = False
            
            if sig_mean_abs < (avg_price * 0.1) or sig_data[sig].min() < 0:
                use_secondary = True
                
            line_color = color_palette[i % len(color_palette)]
            
            fig.add_trace(
                go.Scatter(
                    x=sig_data['timestamp'], y=sig_data[sig], 
                    mode='lines', name=sig.upper(), 
                    line=dict(color=line_color, width=1.5, dash='solid' if not use_secondary else 'dot'),
                    hovertemplate=f"{sig.upper()}: %{{y:.3f}}<extra></extra>"
                ),
                secondary_y=use_secondary
            )

    fig.update_layout(
        title=dict(text="LOG YOUR INTERNAL VARS SO YOU CAN SEE HOW YOUR ALGO OPERATES<br><span style='font-size:9px; color:#8899aa; font-weight:400;'>REQUIRED FORMAT: [TAG] | PROD: ASSET_NAME | MY_ALPHA: 123.45 | Z_SCORE: 2.1</span>", font=dict(color="#ffffff", size=11, family="JetBrains Mono"), x=0),
        plot_bgcolor=BG_COLOR, paper_bgcolor=PANEL_BG,
        font=dict(color="#ffffff", family="JetBrains Mono"),
        xaxis=dict(showgrid=True, gridcolor=GRID_COLOR, title="", range=[0, df_mkt['timestamp'].max()], tickfont=dict(size=9, color="#ffffff")),
        yaxis=dict(showgrid=True, gridcolor=GRID_COLOR, title=dict(text="Price / Fair Value", font=dict(color="#ffffff")), tickfont=dict(size=9, color="#ffffff")),
        yaxis2=dict(showgrid=False, title=dict(text="Oscillators / Z-Scores", font=dict(color="#ffffff")), tickfont=dict(size=9, color="#ffffff")),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color="#ffffff", size=9, family="JetBrains Mono")),
        margin=dict(l=0, r=40, t=40, b=0),
        hovermode="x unified"
    )
    return fig

def plot_telemetry_brainwaves(df_mkt, df_trd, df_tel, selected_signals):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    if df_mkt.empty: return fig
    
    # 1. Baseline: Market Mid Price
    fig.add_trace(
        go.Scatter(x=df_mkt['timestamp'], y=df_mkt['mid_price'], mode='lines', name='L1 Mid Price', line=dict(color='#f0f4f8', width=2), opacity=0.7),
        secondary_y=False
    )
    
    # 2. Executions (To see EXACTLY when the bot acted based on the signals)
    if not df_trd.empty:
        our_buys = df_trd[df_trd['is_our_buy']]
        our_sells = df_trd[df_trd['is_our_sell']]
        
        if not our_buys.empty:
            fig.add_trace(go.Scatter(
                x=our_buys['timestamp'], y=our_buys['price'], mode='markers', name='Our Buys',
                marker=dict(symbol='triangle-up', size=10, color=PROFIT_GREEN, line=dict(width=1, color='white')),
                hovertemplate="BOUGHT %{text} @ %{y}<extra></extra>", text=our_buys['quantity']
            ), secondary_y=False)
            
        if not our_sells.empty:
            fig.add_trace(go.Scatter(
                x=our_sells['timestamp'], y=our_sells['price'], mode='markers', name='Our Sells',
                marker=dict(symbol='triangle-down', size=10, color=LOSS_RED, line=dict(width=1, color='white')),
                hovertemplate="SOLD %{text} @ %{y}<extra></extra>", text=our_sells['quantity']
            ), secondary_y=False)

    # 3. The Brainwaves (Telemetry Signals)
    if not df_tel.empty and selected_signals:
        # Get typical market price to determine if a signal needs a secondary axis
        avg_price = df_mkt['mid_price'].mean() if not df_mkt['mid_price'].isna().all() else 10000
        
        color_palette = [IMC_BLUE, '#a855f7', '#06d6a0', '#f59e0b', '#ff6b6b', '#4ecdc4', '#ffe66d']
        
        for i, sig in enumerate(selected_signals):
            if sig not in df_tel.columns: continue
            
            sig_data = df_tel[['timestamp', sig]].dropna()
            if sig_data.empty: continue
            
            # Determine Axis
            # If the signal's mean magnitude is tiny compared to the price (e.g., a Z-Score of 2.5 vs a price of 10000), 
            # or if it's negative, put it on the secondary Y-axis.
            sig_mean_abs = sig_data[sig].abs().mean()
            use_secondary = False
            
            if sig_mean_abs < (avg_price * 0.1) or sig_data[sig].min() < 0:
                use_secondary = True
                
            line_color = color_palette[i % len(color_palette)]
            
            fig.add_trace(
                go.Scatter(
                    x=sig_data['timestamp'], y=sig_data[sig], 
                    mode='lines', name=sig.upper(), 
                    line=dict(color=line_color, width=1.5, dash='solid' if not use_secondary else 'dot'),
                    hovertemplate=f"{sig.upper()}: %{{y:.3f}}<extra></extra>"
                ),
                secondary_y=use_secondary
            )

    fig.update_layout(
        title=dict(text="LOG YOUR INTERNAL VARS SO YOU CAN SEE HOW YOUR ALGO OPERATES<br><span style='font-size:9px; color:#8899aa; font-weight:400;'>REQUIRED FORMAT: [TAG] | PROD: ASSET_NAME | MY_ALPHA: 123.45 | Z_SCORE: 2.1</span>", font=dict(color="#ffffff", size=11, family="JetBrains Mono"), x=0),
        plot_bgcolor=BG_COLOR, paper_bgcolor=PANEL_BG,
        font=dict(color="#ffffff", family="JetBrains Mono"),
        xaxis=dict(showgrid=True, gridcolor=GRID_COLOR, title="", range=[0, df_mkt['timestamp'].max()], tickfont=dict(size=9, color="#ffffff")),
        yaxis=dict(showgrid=True, gridcolor=GRID_COLOR, title=dict(text="Price / Fair Value", font=dict(color="#ffffff")), tickfont=dict(size=9, color="#ffffff")),
        yaxis2=dict(showgrid=False, title=dict(text="Oscillators / Z-Scores", font=dict(color="#ffffff")), tickfont=dict(size=9, color="#ffffff")),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color="#ffffff", size=9, family="JetBrains Mono")),
        margin=dict(l=0, r=40, t=40, b=0),
        hovermode="x unified"
    )
    return fig

def plot_telemetry_brainwaves(df_mkt, df_trd, df_tel, selected_signals):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    if df_mkt.empty: return fig
    
    # 1. Baseline: Market Mid Price
    fig.add_trace(
        go.Scatter(x=df_mkt['timestamp'], y=df_mkt['mid_price'], mode='lines', name='L1 Mid Price', line=dict(color='#f0f4f8', width=2), opacity=0.7),
        secondary_y=False
    )
    
    # 2. Executions (To see EXACTLY when the bot acted based on the signals)
    if not df_trd.empty:
        our_buys = df_trd[df_trd['is_our_buy']]
        our_sells = df_trd[df_trd['is_our_sell']]
        
        if not our_buys.empty:
            fig.add_trace(go.Scatter(
                x=our_buys['timestamp'], y=our_buys['price'], mode='markers', name='Our Buys',
                marker=dict(symbol='triangle-up', size=10, color=PROFIT_GREEN, line=dict(width=1, color='white')),
                hovertemplate="BOUGHT %{text} @ %{y}<extra></extra>", text=our_buys['quantity']
            ), secondary_y=False)
            
        if not our_sells.empty:
            fig.add_trace(go.Scatter(
                x=our_sells['timestamp'], y=our_sells['price'], mode='markers', name='Our Sells',
                marker=dict(symbol='triangle-down', size=10, color=LOSS_RED, line=dict(width=1, color='white')),
                hovertemplate="SOLD %{text} @ %{y}<extra></extra>", text=our_sells['quantity']
            ), secondary_y=False)

    # 3. The Brainwaves (Telemetry Signals)
    if not df_tel.empty and selected_signals:
        # Get typical market price to determine if a signal needs a secondary axis
        avg_price = df_mkt['mid_price'].mean() if not df_mkt['mid_price'].isna().all() else 10000
        
        color_palette = [IMC_BLUE, '#a855f7', '#06d6a0', '#f59e0b', '#ff6b6b', '#4ecdc4', '#ffe66d']
        
        for i, sig in enumerate(selected_signals):
            if sig not in df_tel.columns: continue
            
            sig_data = df_tel[['timestamp', sig]].dropna()
            if sig_data.empty: continue
            
            # Determine Axis
            # If the signal's mean magnitude is tiny compared to the price (e.g., a Z-Score of 2.5 vs a price of 10000), 
            # or if it's negative, put it on the secondary Y-axis.
            sig_mean_abs = sig_data[sig].abs().mean()
            use_secondary = False
            
            if sig_mean_abs < (avg_price * 0.1) or sig_data[sig].min() < 0:
                use_secondary = True
                
            line_color = color_palette[i % len(color_palette)]
            
            fig.add_trace(
                go.Scatter(
                    x=sig_data['timestamp'], y=sig_data[sig], 
                    mode='lines', name=sig.upper(), 
                    line=dict(color=line_color, width=1.5, dash='solid' if not use_secondary else 'dot'),
                    hovertemplate=f"{sig.upper()}: %{{y:.3f}}<extra></extra>"
                ),
                secondary_y=use_secondary
            )

    fig.update_layout(
        title=dict(text="LOG YOUR INTERNAL VARS SO YOU CAN SEE HOW YOUR ALGO OPERATES<br><span style='font-size:9px; color:#8899aa; font-weight:400;'>REQUIRED FORMAT: [TAG] | PROD: ASSET_NAME | MY_ALPHA: 123.45 | Z_SCORE: 2.1</span>", font=dict(color="#ffffff", size=11, family="JetBrains Mono"), x=0),
        plot_bgcolor=BG_COLOR, paper_bgcolor=PANEL_BG,
        font=dict(color="#ffffff", family="JetBrains Mono"),
        xaxis=dict(showgrid=True, gridcolor=GRID_COLOR, title="", range=[0, df_mkt['timestamp'].max()], tickfont=dict(size=9, color="#ffffff")),
        yaxis=dict(showgrid=True, gridcolor=GRID_COLOR, title=dict(text="Price / Fair Value", font=dict(color="#ffffff")), tickfont=dict(size=9, color="#ffffff")),
        yaxis2=dict(showgrid=False, title=dict(text="Oscillators / Z-Scores", font=dict(color="#ffffff")), tickfont=dict(size=9, color="#ffffff")),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color="#ffffff", size=9, family="JetBrains Mono")),
        margin=dict(l=0, r=40, t=40, b=0),
        hovermode="x unified"
    )
    return fig

# --- HELPER: render a metric card ---
def metric_card(label, value, sub=None, color_class="", wrapper_class=""):
    sub_html = f'<div class="metric-sub">{sub}</div>' if sub else ""
    return f"""
    <div class="card-wrapper {wrapper_class}"><div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value {color_class}">{value}</div>
        {sub_html}
    </div></div>"""

# ========== UI LAYOUT ==========

# --- HEADER ---
st.markdown("""
    <div class='header-container'>
        <div style='display:flex; align-items:center; gap:15px;'>
            <div class="blip-container">
                <div class="blip"></div>
                <div class="blip-text">LIVE ANALYSIS</div>
            </div>
            <div class='title-text'>PROSPERITY 4 QUANT DASHBOARD
                <span style='color:var(--text-tertiary); font-weight:400; font-size:11px;'>
                    &nbsp;/ EXECUTION ENGINE
                </span>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.markdown("""
    <div style="padding: 8px 0 16px 0; border-bottom: 1px solid var(--border-subtle); margin-bottom: 16px;">
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 10px; font-weight: 700;
            color: var(--text-tertiary); letter-spacing: 3px; text-transform: uppercase;">
            DASHBOARD CONTROLS
        </div>
    </div>
""", unsafe_allow_html=True)

uploaded_file = st.sidebar.file_uploader("DROP LOG FILE (.log)", type=['log'])
selected_product = None

if uploaded_file:
    df_market, df_trades, df_telemetry, error = process_log_file(uploaded_file)
    if error:
        st.error(error)
        st.stop()
    st.sidebar.success("✓ LOG PARSED SUCCESSFULLY")
    product_options = df_market['product'].unique()
    if len(product_options) > 0:
        selected_product = st.sidebar.selectbox("SELECT ASSET", product_options)

st.sidebar.markdown("<hr class='sidebar-divider'>", unsafe_allow_html=True)
st.sidebar.markdown("""
    <div style="font-family: 'JetBrains Mono', monospace; font-size: 10px; font-weight: 700;
        color: var(--text-tertiary); letter-spacing: 3px; text-transform: uppercase; margin-bottom: 12px;">
        FORENSICS TUNING
    </div>
""", unsafe_allow_html=True)

markout_horizon = st.sidebar.slider(
    "MARKOUT HORIZON (TICKS)", min_value=1, max_value=100, value=50, step=1,
    help="How far in the future to look to judge trade profitability (1 tick = 100 timestamps)."
)
imbalance_level = st.sidebar.radio(
    "IMBALANCE LEVEL", [1, 2, 3], index=0, horizontal=True,
    help="Which level of book depth to use for the Imbalance Matrix."
)

st.sidebar.markdown("<hr class='sidebar-divider'>", unsafe_allow_html=True)
st.sidebar.markdown("""
    <div style="font-family: 'JetBrains Mono', monospace; font-size: 10px; font-weight: 700;
        color: var(--text-tertiary); letter-spacing: 3px; text-transform: uppercase; margin-bottom: 12px;">
        MOMENTUM TUNING
    </div>
""", unsafe_allow_html=True)

vwap_window = st.sidebar.slider(
    "VWAP ROLL WINDOW (TICKS)", min_value=1, max_value=50, value=5, step=1,
    help="Number of ticks to include in the rolling VWAP calculation for the momentum oscillator."
)


if selected_product:
    df_mkt_prod = df_market[df_market['product'] == selected_product].copy()
    if not df_trades.empty:
        df_trd_prod = df_trades[df_trades['product'] == selected_product].copy()
        df_mkt_l1 = df_mkt_prod[['timestamp', 'bid_price_1', 'ask_price_1']].copy().dropna()
        df_trd_prod = pd.merge_asof(df_trd_prod.sort_values('timestamp'), df_mkt_l1.sort_values('timestamp'), on='timestamp', direction='backward')
        df_trd_prod['is_taker'] = False
        df_trd_prod.loc[df_trd_prod['is_our_buy']  & (df_trd_prod['price'] >= df_trd_prod['ask_price_1']), 'is_taker'] = True
        df_trd_prod.loc[df_trd_prod['is_our_sell'] & (df_trd_prod['price'] <= df_trd_prod['bid_price_1']), 'is_taker'] = True
    else:
        df_trd_prod = pd.DataFrame()
    df_mkt_prod = calculate_exact_position(df_mkt_prod, df_trd_prod)
    
    # --- METRIC CALCULATIONS ---
    final_pnl = df_mkt_prod['profit_and_loss'].iloc[-1]
    last_mid = df_mkt_prod['mid_price'].iloc[-1]
    pnl_series = df_mkt_prod['profit_and_loss']
    pnl_diff = pnl_series.diff().fillna(0)
    max_drawdown = abs((pnl_series - pnl_series.cummax()).min())
    
    # Granular Profit Factor
    maker_pnl, taker_pnl = 0.0, 0.0
    if not df_trd_prod.empty:
        our_trades = df_trd_prod[df_trd_prod['is_our_buy'] | df_trd_prod['is_our_sell']].copy()
        if not our_trades.empty:
            # Value each trade against the end-of-log mid price
            our_trades['trade_pnl'] = np.where(our_trades['is_our_buy'], 
                                               (last_mid - our_trades['price']) * our_trades['quantity'],
                                               (our_trades['price'] - last_mid) * our_trades['quantity'])
            maker_pnl = our_trades[~our_trades['is_taker']]['trade_pnl'].sum()
            taker_pnl = our_trades[our_trades['is_taker']]['trade_pnl'].sum()
            gross_p = our_trades[our_trades['trade_pnl'] > 0]['trade_pnl'].sum()
            gross_l = abs(our_trades[our_trades['trade_pnl'] < 0]['trade_pnl'].sum())
            profit_factor = (gross_p / gross_l) if gross_l > 0 else (2.0 if gross_p > 0 else 0.0)
        else: profit_factor = 0.0
    else: profit_factor = 0.0

    sharpe = (pnl_diff.mean() / pnl_diff.std()) * np.sqrt(10000) if pnl_diff.std() > 0 else 0
    total_vol = df_trd_prod[df_trd_prod['is_our_buy'] | df_trd_prod['is_our_sell']]['quantity'].sum() if not df_trd_prod.empty else 0
    maker_pct = (df_trd_prod[(df_trd_prod['is_our_buy'] | df_trd_prod['is_our_sell']) & ~df_trd_prod['is_taker']]['quantity'].sum() / total_vol * 100) if total_vol > 0 else 0
    pnl_per_lot = final_pnl / total_vol if total_vol > 0 else 0
    if not df_trd_prod.empty:
        our_trades = df_trd_prod[df_trd_prod['is_our_buy'] | df_trd_prod['is_our_sell']].copy()
        if not our_trades.empty:
            our_trades['mid'] = (our_trades['bid_price_1'] + our_trades['ask_price_1']) / 2.0
            our_trades['half_spread'] = (our_trades['ask_price_1'] - our_trades['bid_price_1']) / 2.0
            our_trades['captured'] = np.where(our_trades['is_our_buy'], our_trades['mid'] - our_trades['price'], our_trades['price'] - our_trades['mid'])
            # Avoid div by zero if spread is 0
            spread_capture = (our_trades['captured'].sum() / our_trades['half_spread'].sum() * 100) if our_trades['half_spread'].sum() > 0 else 0
        else: spread_capture = 0
    else: spread_capture = 0
    limit = LIMITS.get(selected_product, 80)
    time_locked = np.mean(np.abs(df_mkt_prod['exact_position'].values) >= limit) * 100
    skew_bias = df_mkt_prod['exact_position'].mean()

    adv_selection, win_rate, info_ratio = 0, 0, 0
    m_trades = pd.DataFrame()
    if not df_trd_prod.empty:
        our_trades = df_trd_prod[df_trd_prod['is_our_buy'] | df_trd_prod['is_our_sell']].copy()
        if not our_trades.empty:
            df_mkt_future = df_mkt_prod[['timestamp', 'mid_price']].copy()
            # Corrected: Look into the FUTURE (T+horizon)
            df_mkt_future['timestamp'] = df_mkt_future['timestamp'] - (markout_horizon * 100)
            df_mkt_future = df_mkt_future.rename(columns={'mid_price': 'future_mid'})
            m_trades = pd.merge(our_trades, df_mkt_future, on='timestamp', how='inner')
            if not m_trades.empty:
                m_trades['m_edge'] = np.where(m_trades['is_our_buy'], m_trades['future_mid'] - m_trades['price'], m_trades['price'] - m_trades['future_mid'])
                
                # Volume-Weighted Metrics
                total_m_vol = m_trades['quantity'].sum()
                if total_m_vol > 0:
                    win_rate = (m_trades[m_trades['m_edge'] > 0]['quantity'].sum() / total_m_vol) * 100
                    adv_selection = (m_trades[m_trades['m_edge'] < 0]['quantity'].sum() / total_m_vol) * 100
                    
                    # Volume-Weighted IR (Sample-Independent)
                    w_mean = (m_trades['m_edge'] * m_trades['quantity']).sum() / total_m_vol
                    w_var = (m_trades['quantity'] * (m_trades['m_edge'] - w_mean)**2).sum() / total_m_vol
                    w_std = np.sqrt(w_var)
                    info_ratio = (w_mean / w_std) if w_std > 0 else 0
                else:
                    win_rate, adv_selection, info_ratio = 0, 0, 0

        # Row 1: Execution Stats
        st.markdown('<div class="section-label">⚡&nbsp;&nbsp;EXECUTION STATS</div>', unsafe_allow_html=True)
        
        pnl_color = "pos" if final_pnl >= 0 else "neg"
        ppl_color = "pos" if pnl_per_lot >= 0 else "neg"
        
        m_color = "#3FB950" if maker_pnl >= 0 else "#F85149"
        t_color = "#3FB950" if taker_pnl >= 0 else "#F85149"
        pnl_subtext = f"M: <span style='color:{m_color}; font-weight:600;'>{maker_pnl:,.0f}</span> | T: <span style='color:{t_color}; font-weight:600;'>{taker_pnl:,.0f}</span>"
        
        st.markdown(f"""
            <div class="metric-grid-5">
                {metric_card("FINAL PNL", f"{final_pnl:,.0f} $", pnl_subtext, pnl_color, "cyan")}
                {metric_card("VOLUME TRADED", f"{total_vol:,.0f}", "Lots", "", "")}
                {metric_card("PNL PER LOT", f"{pnl_per_lot:,.2f}", "Xirecs / Lot", ppl_color, "purple")}
                {metric_card("% MAKER FILLS", f"{maker_pct:.1f}%", "of total volume", "", "")}
                {metric_card("SPREAD CAPTURE", f"{spread_capture:.1f}%", "avg per trade", "", "amber")}
            </div>
        """, unsafe_allow_html=True)

        # Row 2: Risk & Consistency
        st.markdown('<div class="section-label">🛡&nbsp;&nbsp;RISK & CONSISTENCY</div>', unsafe_allow_html=True)

        dd_color = "neg" if max_drawdown > 0 else ""
        sh_color = "pos" if sharpe >= 1.0 else ("amber" if sharpe >= 0 else "neg")
        wr_color = "pos" if win_rate >= 55 else ("amber" if win_rate >= 45 else "neg")
        lock_color = "neg" if time_locked > 5 else ("amber" if time_locked > 1 else "pos")

        st.markdown(f"""
            <div class="metric-grid-4">
                {metric_card("MAX DRAWDOWN", f"{max_drawdown:,.0f} $", "Xirecs", dd_color, "red")}
                {metric_card("SHARPE RATIO", f"S = {sharpe:.2f}", "Daily", sh_color, "")}
                {metric_card(f"WIN RATE T+{markout_horizon*100}", f"{win_rate:.1f}%", "by markout edge (vol-weighted)", wr_color, "")}
                {metric_card("TIME @ LIMIT", f"{time_locked:.1f}%", "position locked", lock_color, "amber")}
            </div>
        """, unsafe_allow_html=True)

        # Row 3: Advanced Forensics
        st.markdown('<div class="section-label">📊&nbsp;&nbsp;ADVANCED FORENSICS</div>', unsafe_allow_html=True)

    as_color = "neg" if adv_selection > 30 else ("amber" if adv_selection > 20 else "pos")
    ir_color = "pos" if info_ratio > 0.1 else ("neg" if info_ratio < -0.1 else "amber")
    sk_color = "amber" if abs(skew_bias) > 10 else ""

    st.markdown(f"""
        <div class="metric-grid-3">
            {metric_card(f"ADVERSE SELECTION T+{markout_horizon*100}", f"{adv_selection:.1f}%", "trades with negative edge", as_color, "red")}
            {metric_card("INFORMATION RATIO", f"{info_ratio:.2f}", "avg markout / stddev", ir_color, "cyan")}
            {metric_card("AVERAGE NET POSITION", f"{skew_bias:.1f} lots", "mean inventory exposure", sk_color, "purple")}
        </div>
        <hr style="margin: 8px 0 -55px 0 !important; border-color: var(--border-subtle) !important; opacity: 0.6;">
    """, unsafe_allow_html=True)

    # ---- MACRO CHARTS ----
    st.plotly_chart(plot_pnl_inventory(df_mkt_prod, selected_product), width='stretch')
    st.plotly_chart(plot_microstructure_xray(df_mkt_prod, df_trd_prod), width='stretch')
    
    st.markdown("---")
    st.markdown('<div class="section-label">🤖&nbsp;&nbsp;BOT BEHAVIOR & FLOW DYNAMICS</div>', unsafe_allow_html=True)
    
    c5, c6 = st.columns(2)
    with c5: st.plotly_chart(plot_magic_size_fingerprinter(df_mkt_prod, df_trd_prod, markout_horizon), width='stretch')
    with c6: st.plotly_chart(plot_liquidation_radar(df_mkt_prod, df_trd_prod), width='stretch')
    
    st.markdown("---")
    st.markdown('<div class="section-label">🎯&nbsp;&nbsp;MOMENTUM & WALL ANALYTICS</div>', unsafe_allow_html=True)
    
    st.plotly_chart(plot_true_mid_divergence(df_mkt_prod), width='stretch')
    st.plotly_chart(plot_vwap_momentum(df_mkt_prod, df_trd_prod, vwap_window), width='stretch')
    
    st.markdown("---")
    st.markdown('<div class="section-label">🔬&nbsp;&nbsp;EXECUTION & FLOW ANALYSIS</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1: st.plotly_chart(plot_toxicity_markout(m_trades, markout_horizon), width='stretch')
    with c2: st.plotly_chart(plot_spread_capture(m_trades, df_mkt_prod), width='stretch')

    c3, c4 = st.columns(2)
    with c3: st.plotly_chart(plot_imbalance_matrix(m_trades, df_mkt_prod, imbalance_level), width='stretch')
    with c4: st.plotly_chart(plot_whale_profiler(df_trd_prod), width='stretch')

    st.markdown("---")
    st.markdown('<div class="section-label">🧠&nbsp;&nbsp;TELEMETRY & SIGNAL DIAGNOSTICS</div>', unsafe_allow_html=True)
    
    # Filter telemetry for current product
    df_tel_prod = df_telemetry[df_telemetry['target_product'] == selected_product].copy() if not df_telemetry.empty else pd.DataFrame()
    
    available_signals = []
    if not df_tel_prod.empty:
        for col in df_tel_prod.columns:
            if col not in ['timestamp', 'tag', 'target_product']:
                # safely convert to numeric, dropping non-numerics
                df_tel_prod[col] = pd.to_numeric(df_tel_prod[col], errors='coerce')
                if not df_tel_prod[col].isna().all():
                    available_signals.append(col)
                    
    # Create empty container for plot to render ABOVE the controls
    telemetry_plot_container = st.container()
    
    # Create the multi-select visually BELOW the plot
    st.markdown("<br>", unsafe_allow_html=True)
    selected_signals = st.multiselect(
        "SELECT TELEMETRY SIGNALS TO OVERLAY", 
        options=available_signals,
        default=[],
        help="Select any logged numerical value to overlay on the price chart."
    )
    
    # Render plot into the container
    with telemetry_plot_container:
        st.plotly_chart(plot_telemetry_brainwaves(df_mkt_prod, df_trd_prod, df_tel_prod, selected_signals), width='stretch')

else:
    st.markdown("""
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center;
            padding: 80px 0; gap: 16px;">
            <div style="font-family:'JetBrains Mono',monospace; font-size:11px; font-weight:700;
                color:var(--text-tertiary); letter-spacing:3px; text-transform:uppercase;">
                AWAITING INPUT
            </div>
            <div style="font-family:'JetBrains Mono',monospace; font-size:13px;
                color:var(--text-secondary);">
                Drop a <span style="color:var(--accent-blue);">.log</span> file in the sidebar to begin analysis
            </div>
        </div>
    """, unsafe_allow_html=True)