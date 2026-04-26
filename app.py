import streamlit as st
import pandas as pd
import numpy as np
import json
import io
import re
import math
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

LIMITS = {
    'ASH_COATED_OSMIUM': 80,
    'INTARIAN_PEPPER_ROOT': 80,
    'HYDROGEL_PACK': 200,
    'VELVETFRUIT_EXTRACT': 200,
    'VEV_4000': 300,
    'VEV_4500': 300,
    'VEV_5000': 300,
    'VEV_5100': 300,
    'VEV_5200': 300,
    'VEV_5300': 300,
    'VEV_5400': 300,
    'VEV_5500': 300,
    'VEV_6000': 300,
    'VEV_6500': 300,
}

OPTION_PRODUCTS = [
    'VEV_4000',
    'VEV_4500',
    'VEV_5000',
    'VEV_5100',
    'VEV_5200',
    'VEV_5300',
    'VEV_5400',
    'VEV_5500',
    'VEV_6000',
    'VEV_6500',
]
UNDERLYING_PRODUCT = 'VELVETFRUIT_EXTRACT'
DAYS_PER_YEAR = 365.0
ROUND3_TTE_DAYS = 5.0

PRODUCT_ALIASES = {
    'ASH_COATED_OSMIUM': ['OSM', 'ASH', 'OSMIUM'],
    'INTARIAN_PEPPER_ROOT': ['PEP', 'INT', 'PEPPER', 'ROOT'],
    'HYDROGEL_PACK': ['HYDROGEL', 'HYP'],
    'VELVETFRUIT_EXTRACT': ['VELVET', 'VELVETFRUIT', 'VFE'],
    'VEV_4000': ['VEV4000'],
    'VEV_4500': ['VEV4500'],
    'VEV_5000': ['VEV5000'],
    'VEV_5100': ['VEV5100'],
    'VEV_5200': ['VEV5200'],
    'VEV_5300': ['VEV5300'],
    'VEV_5400': ['VEV5400'],
    'VEV_5500': ['VEV5500'],
    'VEV_6000': ['VEV6000'],
    'VEV_6500': ['VEV6500'],
}

def extract_lambda_text_and_positions(lambda_log):
    """Prosperity lambdaLog is usually a JSON wrapper; return only flushed text logs."""
    if not lambda_log:
        return "", {}

    try:
        payload = json.loads(lambda_log)
    except (TypeError, json.JSONDecodeError):
        return str(lambda_log), {}

    if not isinstance(payload, list):
        return str(lambda_log), {}

    state_positions = {}
    if payload and isinstance(payload[0], list) and len(payload[0]) > 6 and isinstance(payload[0][6], dict):
        state_positions = payload[0][6]

    for item in reversed(payload):
        if isinstance(item, str) and ('|' in item or '\n' in item):
            return item, state_positions

    return "", state_positions

def infer_product_from_telemetry_line(line):
    line_upper = line.upper()
    for product, aliases in PRODUCT_ALIASES.items():
        if product in line_upper or any(alias in line_upper for alias in aliases):
            return product
    return "UNKNOWN"

def clean_telemetry_key(raw_key, product):
    key = raw_key.strip()
    aliases = PRODUCT_ALIASES.get(product, [])
    for alias in aliases + [product]:
        if key.upper().startswith(alias):
            key = key[len(alias):].strip()
            break
    key = key.strip(" -_:")
    return key.lower().replace(" ", "_")

def parse_telemetry_line(line):
    if '|' not in line:
        return None

    parts = [p.strip() for p in line.split('|') if p.strip()]
    if not parts:
        return None

    compact_type = parts[0].strip()

    explicit_product = None
    for part in parts:
        if ':' not in part:
            continue
        raw_key, raw_value = part.split(':', 1)
        key = raw_key.strip().lower().replace(" ", "_")
        if key in {'prod', 'product', 'symbol', 'asset'}:
            explicit_product = raw_value.strip()
            break

    if explicit_product is None and compact_type in {'P', 'H'}:
        explicit_product = UNDERLYING_PRODUCT if compact_type == 'H' else 'PORTFOLIO'
    target_product = explicit_product or infer_product_from_telemetry_line(line)
    tag = compact_type.split(':', 1)[0].strip()
    row = {'tag': tag, 'target_product': target_product}

    compact_key_map = {
        'p': 'prod',
        'm': 'mode',
        's': 'side',
        'q': 'qty',
        'e': 'edge',
        'd': 'delta',
        'v': 'vega',
        'od': 'option_delta',
        'rd': 'residual_delta',
        'upos': 'underlying_position',
        'tts': 'trade_ts',
    }

    for part in parts:
        if ':' not in part:
            continue
        raw_key, raw_value = part.split(':', 1)
        raw_key_clean = raw_key.strip().lower().replace(" ", "_")
        key = compact_key_map.get(raw_key_clean, clean_telemetry_key(raw_key, target_product))
        if not key:
            continue
        value = raw_value.strip()
        try:
            row[key] = float(value)
        except ValueError:
            row[key] = value

    return row

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
        
        # Fix Prosperity simulator bug where empty order books output a mid_price of 0.0
        df_market['mid_price'] = df_market['mid_price'].replace(0.0, np.nan)
        df_market['mid_price'] = df_market.groupby('product')['mid_price'].ffill()
        
        df_market['profit_and_loss'] = df_market.groupby('product')['profit_and_loss'].ffill().fillna(0)
        raw_logs = data.get('logs', [])
        sandbox_logs = [str(entry.get('sandboxLog', '')).strip() for entry in raw_logs if str(entry.get('sandboxLog', '')).strip()]
        df_market.attrs['sandbox_message_count'] = len(sandbox_logs)
        final_profit_matches = [
            float(match.group(1))
            for log in sandbox_logs
            for match in re.finditer(r"final profit of ([+-]?\d+(?:\.\d+)?)", log)
        ]
        if final_profit_matches:
            df_market.attrs['adjusted_final_profit'] = final_profit_matches[-1]
        
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
        for entry in raw_logs:
            t = entry.get('timestamp', 0)
            log_text, state_positions = extract_lambda_text_and_positions(entry.get('lambdaLog', ''))

            for line in log_text.splitlines():
                row = parse_telemetry_line(line)
                if row is None:
                    continue
                row['timestamp'] = t
                logged_position = state_positions.get(row['target_product'])
                if logged_position is not None:
                    row['logged_position'] = logged_position
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

def prefer_logged_position(df_market_product, df_telemetry, selected_product):
    df_market_product['reconstructed_position'] = df_market_product['exact_position']
    df_market_product['position_source'] = 'tradeHistory'

    if df_telemetry.empty or 'logged_position' not in df_telemetry.columns:
        return df_market_product

    logged = df_telemetry[df_telemetry['target_product'] == selected_product][['timestamp', 'logged_position']].copy()
    if logged.empty:
        return df_market_product

    logged['logged_position'] = pd.to_numeric(logged['logged_position'], errors='coerce')
    logged = logged.dropna(subset=['logged_position']).groupby('timestamp', as_index=False).last()
    if logged.empty:
        return df_market_product

    df_market_product = pd.merge(df_market_product, logged, on='timestamp', how='left')
    has_logged_position = df_market_product['logged_position'].notna()
    df_market_product.loc[has_logged_position, 'exact_position'] = df_market_product.loc[has_logged_position, 'logged_position']
    df_market_product.loc[has_logged_position, 'position_source'] = 'lambdaLog'
    return df_market_product

def build_product_frames(df_market, df_trades, df_telemetry):
    frames = {}
    for product in df_market['product'].unique():
        df_mkt_product = df_market[df_market['product'] == product].copy()
        if df_trades.empty:
            df_trades_product = pd.DataFrame()
        else:
            df_trades_product = df_trades[df_trades['product'] == product].copy()
        df_mkt_product = calculate_exact_position(df_mkt_product, df_trades_product)
        frames[product] = prefer_logged_position(df_mkt_product, df_telemetry, product)
    return frames

def combined_limit(products):
    return sum(LIMITS.get(product, 80) for product in products)

def build_portfolio_frame(product_frames):
    if not product_frames:
        return pd.DataFrame()

    pieces = []
    for product, df in product_frames.items():
        if df.empty:
            continue
        piece = df[['timestamp', 'profit_and_loss', 'exact_position']].copy()
        piece = piece.rename(columns={
            'profit_and_loss': f'pnl__{product}',
            'exact_position': f'pos__{product}',
        })
        pieces.append(piece.set_index('timestamp'))

    if not pieces:
        return pd.DataFrame()

    merged = pd.concat(pieces, axis=1).sort_index().ffill().fillna(0).reset_index()
    pnl_cols = [col for col in merged.columns if col.startswith('pnl__')]
    pos_cols = [col for col in merged.columns if col.startswith('pos__')]
    out = pd.DataFrame({
        'timestamp': merged['timestamp'],
        'profit_and_loss': merged[pnl_cols].sum(axis=1),
        'net_position': merged[pos_cols].sum(axis=1),
        'exact_position': merged[pos_cols].abs().sum(axis=1),
    })
    return out

def attach_book_context_to_trades(df_trades, product_frames, products):
    if df_trades.empty:
        return pd.DataFrame()

    enriched = []
    for product in products:
        if product not in product_frames:
            continue

        trades = df_trades[df_trades['product'] == product].copy()
        if trades.empty:
            continue

        mkt = product_frames[product].copy()
        book_cols = ['timestamp', 'bid_price_1', 'ask_price_1', 'mid_price']
        book = mkt[book_cols].copy().dropna(subset=['timestamp']).sort_values('timestamp')
        trades = trades.sort_values('timestamp')

        if book.empty:
            trades['bid_price_1'] = np.nan
            trades['ask_price_1'] = np.nan
            trades['mid_price'] = np.nan
        else:
            trades = pd.merge_asof(trades, book, on='timestamp', direction='backward')

        trades['final_mid'] = float(mkt['mid_price'].iloc[-1]) if 'mid_price' in mkt.columns and not mkt['mid_price'].empty else np.nan
        trades['is_taker'] = False
        trades.loc[trades['is_our_buy'] & (trades['price'] >= trades['ask_price_1']), 'is_taker'] = True
        trades.loc[trades['is_our_sell'] & (trades['price'] <= trades['bid_price_1']), 'is_taker'] = True
        enriched.append(trades)

    if not enriched:
        return pd.DataFrame()

    return pd.concat(enriched, ignore_index=True).sort_values('timestamp').reset_index(drop=True)

def build_markout_trades(our_trades, product_frames, markout_horizon):
    if our_trades.empty:
        return pd.DataFrame()

    marked = []
    for product, trades in our_trades.groupby('product'):
        if product not in product_frames:
            continue
        df_mkt_future = product_frames[product][['timestamp', 'mid_price']].copy()
        df_mkt_future['timestamp'] = df_mkt_future['timestamp'] - (markout_horizon * 100)
        df_mkt_future = df_mkt_future.rename(columns={'mid_price': 'future_mid'})
        product_markouts = pd.merge(trades, df_mkt_future, on='timestamp', how='inner')
        if product_markouts.empty:
            continue
        product_markouts['m_edge'] = np.where(
            product_markouts['is_our_buy'],
            product_markouts['future_mid'] - product_markouts['price'],
            product_markouts['price'] - product_markouts['future_mid'],
        )
        marked.append(product_markouts)

    if not marked:
        return pd.DataFrame()

    return pd.concat(marked, ignore_index=True).sort_values('timestamp').reset_index(drop=True)

def build_options_risk_frame(product_frames, selected_products):
    option_products = [p for p in OPTION_PRODUCTS if p in product_frames and p in selected_products]
    if UNDERLYING_PRODUCT not in product_frames or not option_products:
        return pd.DataFrame(), option_products

    under = product_frames[UNDERLYING_PRODUCT][['timestamp', 'mid_price', 'profit_and_loss', 'exact_position']].copy()
    under = under.rename(columns={
        'mid_price': 'spot',
        'profit_and_loss': 'underlying_pnl',
        'exact_position': 'underlying_position',
    }).set_index('timestamp').sort_index().ffill()
    risk = under.copy()
    risk['voucher_pnl'] = 0.0
    risk['option_delta'] = 0.0
    risk['option_gamma'] = 0.0
    risk['option_vega'] = 0.0
    risk['gross_voucher_position'] = 0.0

    for product in option_products:
        frame = product_frames[product][['timestamp', 'mid_price', 'profit_and_loss', 'exact_position']].copy()
        frame = frame.rename(columns={
            'mid_price': f'mid__{product}',
            'profit_and_loss': f'pnl__{product}',
            'exact_position': f'pos__{product}',
        }).set_index('timestamp').sort_index().ffill()
        risk = risk.join(frame, how='left')
        risk[[f'mid__{product}', f'pnl__{product}', f'pos__{product}']] = risk[[f'mid__{product}', f'pnl__{product}', f'pos__{product}']].ffill().fillna(0)

        strike = strike_from_option(product)
        tte = np.maximum((ROUND3_TTE_DAYS - risk.index.to_series().astype(float) / 1_000_000.0) / DAYS_PER_YEAR, 0.25 / DAYS_PER_YEAR).values
        spot = risk['spot'].astype(float).values
        mid = risk[f'mid__{product}'].astype(float).values
        iv = np.array([implied_vol_scalar(price, s, strike, t) for price, s, t in zip(mid, spot, tte)])
        iv = pd.Series(iv, index=risk.index).ffill().fillna(0.0001).values
        delta, gamma, vega = bs_greeks_vector(spot, strike, tte, iv)
        pos = risk[f'pos__{product}'].astype(float).values

        risk[f'iv__{product}'] = iv
        risk[f'delta__{product}'] = pos * delta
        risk[f'gamma__{product}'] = pos * gamma
        risk[f'vega__{product}'] = pos * vega
        risk['voucher_pnl'] += risk[f'pnl__{product}']
        risk['option_delta'] += risk[f'delta__{product}']
        risk['option_gamma'] += risk[f'gamma__{product}']
        risk['option_vega'] += risk[f'vega__{product}']
        risk['gross_voucher_position'] += np.abs(pos)

    risk['portfolio_delta'] = risk['option_delta'] + risk['underlying_position']
    risk['portfolio_gamma'] = risk['option_gamma']
    risk['portfolio_vega_1pct'] = risk['option_vega'] * 0.01
    risk['combined_pnl'] = risk['voucher_pnl'] + risk['underlying_pnl']
    return risk.reset_index(), option_products

def options_drawdown_attribution(risk_df, product_frames, option_products):
    if risk_df.empty:
        return None, pd.DataFrame()
    window = max_drawdown_window(risk_df.set_index('timestamp')['combined_pnl'])
    if not window:
        return None, pd.DataFrame()
    peak_ts = window['peak_ts']
    trough_ts = window['trough_ts']
    peak_row = risk_df[risk_df['timestamp'] == peak_ts].iloc[0]
    trough_row = risk_df[risk_df['timestamp'] == trough_ts].iloc[0]
    spot_move = float(trough_row['spot'] - peak_row['spot'])
    window['spot_move'] = spot_move
    window['start_delta'] = float(peak_row['portfolio_delta'])
    window['delta_estimate'] = float(peak_row['portfolio_delta'] * spot_move)
    window['unexplained'] = float((trough_row['combined_pnl'] - peak_row['combined_pnl']) - window['delta_estimate'])

    rows = []
    for product in option_products + ([UNDERLYING_PRODUCT] if UNDERLYING_PRODUCT in product_frames else []):
        frame = product_frames[product].set_index('timestamp').sort_index()
        if peak_ts not in frame.index or trough_ts not in frame.index:
            continue
        start_pnl = float(frame.loc[peak_ts, 'profit_and_loss'])
        end_pnl = float(frame.loc[trough_ts, 'profit_and_loss'])
        start_pos = float(frame.loc[peak_ts, 'exact_position'])
        end_pos = float(frame.loc[trough_ts, 'exact_position'])
        rows.append({
            'product': product,
            'pnl_change': end_pnl - start_pnl,
            'start_pnl': start_pnl,
            'end_pnl': end_pnl,
            'start_pos': start_pos,
            'end_pos': end_pos,
        })
    return window, pd.DataFrame(rows).sort_values('pnl_change')

def option_product_summary(product_frames, df_trades, option_products, drawdown_rows):
    rows = []
    dd_map = {}
    if drawdown_rows is not None and not drawdown_rows.empty:
        dd_map = dict(zip(drawdown_rows['product'], drawdown_rows['pnl_change']))

    for product in option_products:
        frame = product_frames[product]
        trades = df_trades[df_trades['product'] == product].copy() if not df_trades.empty and 'product' in df_trades.columns else pd.DataFrame()
        our = trades[(trades.get('is_our_buy', False)) | (trades.get('is_our_sell', False))].copy() if not trades.empty else pd.DataFrame()
        buy_qty = int(our.loc[our['is_our_buy'], 'quantity'].sum()) if not our.empty else 0
        sell_qty = int(our.loc[our['is_our_sell'], 'quantity'].sum()) if not our.empty else 0
        avg_buy = (our.loc[our['is_our_buy'], 'price'] * our.loc[our['is_our_buy'], 'quantity']).sum() / buy_qty if buy_qty else np.nan
        avg_sell = (our.loc[our['is_our_sell'], 'price'] * our.loc[our['is_our_sell'], 'quantity']).sum() / sell_qty if sell_qty else np.nan
        abs_pos = frame['exact_position'].abs()
        limit = LIMITS.get(product, 300)
        rows.append({
            'Product': product,
            'Final PnL': float(frame['profit_and_loss'].iloc[-1]),
            'DD Chg': float(dd_map.get(product, 0.0)),
            'Final Pos': int(frame['exact_position'].iloc[-1]),
            'Max Abs Pos': int(abs_pos.max()),
            'Avg Abs Pos': float(abs_pos.mean()),
            'Time >50% Lim': float((abs_pos >= 0.5 * limit).mean() * 100),
            'Buy Qty': buy_qty,
            'Sell Qty': sell_qty,
            'Net Qty': buy_qty - sell_qty,
            'Avg Buy': avg_buy,
            'Avg Sell': avg_sell,
        })
    return pd.DataFrame(rows)

def fill_quality_table(df_trades, product_frames, option_products):
    enriched = attach_book_context_to_trades(df_trades, product_frames, option_products)
    if enriched.empty:
        return pd.DataFrame()
    our = enriched[enriched['is_our_buy'] | enriched['is_our_sell']].copy()
    if our.empty:
        return pd.DataFrame()
    rows = []
    for horizon in [1, 10, 50, 100]:
        marked = build_markout_trades(our, product_frames, horizon)
        if marked.empty:
            continue
        marked['side'] = np.where(marked['is_our_buy'], 'BUY', 'SELL')
        marked['style'] = np.where(marked['is_taker'], 'TAKE', 'MAKE')
        grouped = marked.groupby(['product', 'side', 'style'])
        for key, group in grouped:
            qty = group['quantity'].sum()
            edge = (group['m_edge'] * group['quantity']).sum() / qty if qty else np.nan
            rows.append({'Product': key[0], 'Side': key[1], 'Style': key[2], 'Horizon': f'T+{horizon*100}', 'Qty': qty, 'Avg Markout': edge})
    if not rows:
        return pd.DataFrame()
    out = pd.DataFrame(rows)
    pivot = out.pivot_table(index=['Product', 'Side', 'Style'], columns='Horizon', values='Avg Markout', aggfunc='mean').reset_index()
    qty = out.groupby(['Product', 'Side', 'Style'])['Qty'].max().reset_index()
    return pd.merge(qty, pivot, on=['Product', 'Side', 'Style'], how='left').sort_values(['Product', 'Side', 'Style'])

def max_drawdown_abs(pnl_series):
    if pnl_series.empty:
        return 0.0
    return abs((pnl_series - pnl_series.cummax()).min())

def norm_cdf(x):
    arr = np.asarray(x, dtype=float)
    values = 0.5 * (1.0 + np.vectorize(math.erf)(arr / np.sqrt(2.0)))
    return float(values) if values.shape == () else values

def norm_pdf(x):
    return np.exp(-0.5 * x * x) / np.sqrt(2.0 * np.pi)

def bs_call_price(spot, strike, tte, sigma):
    intrinsic = np.maximum(0.0, spot - strike)
    vol_sqrt_t = sigma * np.sqrt(np.maximum(tte, 1e-9))
    valid = (tte > 0) & (sigma > 0) & (spot > 0) & (strike > 0) & (vol_sqrt_t > 0)
    price = intrinsic.astype(float) if hasattr(intrinsic, 'astype') else float(intrinsic)
    if np.isscalar(price):
        if not valid:
            return price
        d1 = (np.log(spot / strike) + 0.5 * sigma * sigma * tte) / vol_sqrt_t
        d2 = d1 - vol_sqrt_t
        return spot * norm_cdf(d1) - strike * norm_cdf(d2)
    out = price.copy()
    d1 = np.zeros_like(out, dtype=float)
    d1[valid] = (np.log(spot[valid] / strike) + 0.5 * sigma[valid] * sigma[valid] * tte[valid]) / vol_sqrt_t[valid]
    d2 = d1 - vol_sqrt_t
    out[valid] = spot[valid] * norm_cdf(d1[valid]) - strike * norm_cdf(d2[valid])
    return out

def bs_greeks_vector(spot, strike, tte, sigma):
    spot = np.asarray(spot, dtype=float)
    tte = np.asarray(tte, dtype=float)
    sigma = np.asarray(sigma, dtype=float)
    vol_sqrt_t = sigma * np.sqrt(np.maximum(tte, 1e-9))
    valid = (tte > 0) & (sigma > 0) & (spot > 0) & (strike > 0) & (vol_sqrt_t > 0)
    delta = np.where(spot > strike, 1.0, 0.0).astype(float)
    gamma = np.zeros_like(delta, dtype=float)
    vega = np.zeros_like(delta, dtype=float)
    if valid.any():
        d1 = (np.log(spot[valid] / strike) + 0.5 * sigma[valid] * sigma[valid] * tte[valid]) / vol_sqrt_t[valid]
        pdf = norm_pdf(d1)
        delta[valid] = norm_cdf(d1)
        gamma[valid] = pdf / (spot[valid] * vol_sqrt_t[valid])
        vega[valid] = spot[valid] * pdf * np.sqrt(tte[valid])
    return delta, gamma, vega

def implied_vol_scalar(price, spot, strike, tte):
    if pd.isna(price) or pd.isna(spot) or spot <= 0 or strike <= 0 or tte <= 0:
        return np.nan
    intrinsic = max(0.0, spot - strike)
    if price <= intrinsic + 1e-9:
        return 0.0001
    lo, hi = 0.0001, 3.0
    for _ in range(45):
        mid = (lo + hi) / 2.0
        value = bs_call_price(float(spot), float(strike), float(tte), mid)
        if value < price:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0

def strike_from_option(product):
    try:
        return float(product.rsplit('_', 1)[1])
    except Exception:
        return np.nan

def max_drawdown_window(series):
    if series.empty:
        return None
    running_peak = series.cummax()
    drawdown = running_peak - series
    trough_idx = drawdown.idxmax()
    peak_candidates = series.loc[:trough_idx]
    peak_idx = peak_candidates.idxmax()
    return {
        'peak_ts': int(peak_idx),
        'trough_ts': int(trough_idx),
        'peak_value': float(series.loc[peak_idx]),
        'trough_value': float(series.loc[trough_idx]),
        'drawdown': float(drawdown.loc[trough_idx]),
    }

def pnl_buckets(df, bucket_count=5):
    if df.empty:
        return []

    df = df.sort_values('timestamp').reset_index(drop=True)
    chunks = [df.iloc[idx] for idx in np.array_split(np.arange(len(df)), min(bucket_count, len(df))) if len(idx) > 0]
    rows = []
    prev_pnl = 0.0

    for i, chunk in enumerate(chunks, start=1):
        end_pnl = float(chunk['profit_and_loss'].iloc[-1])
        bucket_pnl = end_pnl - prev_pnl
        rows.append({
            'bucket': f'B{i}',
            'start': int(chunk['timestamp'].iloc[0]),
            'end': int(chunk['timestamp'].iloc[-1]),
            'bucket_pnl': bucket_pnl
        })
        prev_pnl = end_pnl

    return rows

def portfolio_curve(df_market):
    curve = df_market.pivot_table(index='timestamp', columns='product', values='profit_and_loss', aggfunc='last')
    curve = curve.sort_index().ffill().fillna(0)
    return curve.sum(axis=1)

def summarize_products(product_frames):
    rows = []
    for product, df in product_frames.items():
        limit = LIMITS.get(product, 80)
        final_pnl = float(df['profit_and_loss'].iloc[-1]) if not df.empty else 0.0
        max_dd = max_drawdown_abs(df['profit_and_loss']) if not df.empty else 0.0
        abs_pos = df['exact_position'].abs() if not df.empty else pd.Series(dtype=float)
        avg_abs_pos = float(abs_pos.mean()) if not abs_pos.empty else 0.0
        max_abs_pos = float(abs_pos.max()) if not abs_pos.empty else 0.0
        near_50 = float((abs_pos >= 0.50 * limit).mean() * 100) if not abs_pos.empty else 0.0
        near_75 = float((abs_pos >= 0.75 * limit).mean() * 100) if not abs_pos.empty else 0.0
        near_90 = float((abs_pos >= 0.90 * limit).mean() * 100) if not abs_pos.empty else 0.0
        buckets = pnl_buckets(df)
        worst_bucket = min((b['bucket_pnl'] for b in buckets), default=0.0)
        negative_buckets = sum(1 for b in buckets if b['bucket_pnl'] < 0)
        rows.append({
            'product': product,
            'final_pnl': final_pnl,
            'max_dd': max_dd,
            'pnl_dd': final_pnl / max_dd if max_dd > 0 else np.nan,
            'avg_abs_pos': avg_abs_pos,
            'max_abs_pos': max_abs_pos,
            'pnl_avg_abs_pos': final_pnl / avg_abs_pos if avg_abs_pos > 0 else np.nan,
            'near_50_pct': near_50,
            'near_75_pct': near_75,
            'near_90_pct': near_90,
            'worst_bucket': worst_bucket,
            'negative_buckets': negative_buckets
        })

    return pd.DataFrame(rows).sort_values('final_pnl', ascending=False).reset_index(drop=True)

def format_metric_number(value, decimals=1):
    if pd.isna(value):
        return "N/A"
    return f"{value:,.{decimals}f}"

def plot_pnl_bucket_stability(product_frames):
    bucket_rows = []
    for product, df in product_frames.items():
        for row in pnl_buckets(df):
            bucket_rows.append({'product': product, **row})

    if not bucket_rows:
        return go.Figure()

    bucket_df = pd.DataFrame(bucket_rows)
    pivot = bucket_df.pivot(index='product', columns='bucket', values='bucket_pnl').fillna(0)
    text = pivot.map(lambda v: f"{v:,.0f}") if hasattr(pivot, 'map') else pivot.applymap(lambda v: f"{v:,.0f}")

    max_abs = max(abs(pivot.min().min()), abs(pivot.max().max()), 1)
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=pivot.index,
        text=text.values,
        texttemplate="%{text}",
        colorscale=[[0.0, LOSS_RED], [0.5, PANEL_BG], [1.0, PROFIT_GREEN]],
        zmid=0,
        zmin=-max_abs,
        zmax=max_abs,
        colorbar=dict(title="PnL")
    ))
    fig.update_layout(
        title=dict(text="PNL BUCKET STABILITY — 5 EQUAL TIME WINDOWS", font=dict(color="#ffffff", size=11, family="JetBrains Mono"), x=0),
        plot_bgcolor=BG_COLOR, paper_bgcolor=PANEL_BG,
        font=dict(color="#ffffff", family="JetBrains Mono"),
        xaxis=dict(title="", tickfont=dict(size=9, color="#ffffff")),
        yaxis=dict(title="", tickfont=dict(size=9, color="#ffffff")),
        margin=dict(l=0, r=40, t=40, b=0)
    )
    return fig

def render_portfolio_submission_summary(df_market, product_frames):
    product_summary = summarize_products(product_frames)
    portfolio_pnl = portfolio_curve(df_market)
    portfolio_final_pnl = float(portfolio_pnl.iloc[-1]) if not portfolio_pnl.empty else 0.0
    portfolio_max_dd = max_drawdown_abs(portfolio_pnl)
    sandbox_messages = df_market.attrs.get('sandbox_message_count', 0)
    adjusted_final_profit = df_market.attrs.get('adjusted_final_profit')
    worst_drag = product_summary.sort_values('final_pnl').iloc[0] if not product_summary.empty else None
    best_concentration = (product_summary['final_pnl'].max() / portfolio_final_pnl * 100) if portfolio_final_pnl > 0 and not product_summary.empty else np.nan
    port_color = "pos" if portfolio_final_pnl >= 0 else "neg"
    dd_color = "neg" if portfolio_max_dd > 0 else ""
    msg_color = "amber" if sandbox_messages > 0 else "pos"
    concentration_sub = "best product / total PnL" if not pd.isna(best_concentration) else "not meaningful if total PnL <= 0"
    worst_name = worst_drag['product'] if worst_drag is not None else "N/A"
    worst_value = worst_drag['final_pnl'] if worst_drag is not None else np.nan
    final_pnl_sub = f"stored final: {adjusted_final_profit:,.0f} $" if adjusted_final_profit is not None else "all products"
    st.markdown('<div class="section-label">🏁&nbsp;&nbsp;PORTFOLIO SUBMISSION SUMMARY</div>', unsafe_allow_html=True)

    st.markdown(f"""
        <div class="metric-grid-5">
            {metric_card("TOTAL OFFICIAL PNL", f"{portfolio_final_pnl:,.0f} $", final_pnl_sub, port_color, "cyan")}
            {metric_card("PORTFOLIO MAX DD", f"{portfolio_max_dd:,.0f} $", "from official PnL curve", dd_color, "red")}
            {metric_card("WORST PRODUCT", worst_name, f"{format_metric_number(worst_value, 0)} $", "neg" if worst_value < 0 else "", "amber")}
            {metric_card("BEST CONCENTRATION", f"{format_metric_number(best_concentration, 1)}%", concentration_sub, "amber" if not pd.isna(best_concentration) and best_concentration > 80 else "", "")}
            {metric_card("SANDBOX MSGS", f"{sandbox_messages}", "non-empty sandbox logs", msg_color, "amber" if sandbox_messages > 0 else "green")}
        </div>
    """, unsafe_allow_html=True)

    table_cols = {
        'product': 'Product',
        'final_pnl': 'Final PnL',
        'max_dd': 'Max DD',
        'pnl_dd': 'PnL/DD',
        'avg_abs_pos': 'Avg |Pos|',
        'max_abs_pos': 'Max |Pos|',
        'near_75_pct': '>=75% Limit',
        'near_90_pct': '>=90% Limit',
        'worst_bucket': 'Worst Bucket',
        'negative_buckets': 'Neg Buckets'
    }
    product_table = product_summary[list(table_cols.keys())].rename(columns=table_cols)
    st.dataframe(
        product_table.style.format({
            'Final PnL': '{:,.0f}',
            'Max DD': '{:,.0f}',
            'PnL/DD': '{:,.2f}',
            'Avg |Pos|': '{:,.1f}',
            'Max |Pos|': '{:,.0f}',
            '>=75% Limit': '{:,.1f}%',
            '>=90% Limit': '{:,.1f}%',
            'Worst Bucket': '{:,.0f}',
            'Neg Buckets': '{:,.0f}'
        }),
        width='stretch',
        hide_index=True
    )

    st.plotly_chart(plot_pnl_bucket_stability(product_frames), width='stretch', key="portfolio_pnl_bucket_stability")

# --- VISUALIZATIONS (logic unchanged, colors updated to match new theme) ---
def plot_pnl_inventory(df, selected_product, limit_override=None, inventory_label="Net Position (Lots)", show_negative_limit=True):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    limit = limit_override if limit_override is not None else LIMITS.get(selected_product, 80)
    
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['profit_and_loss'], name="Cumulative PnL", line=dict(color=IMC_BLUE, width=2), hoverinfo='skip'), secondary_y=False)
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['exact_position'], name="Inventory (+/-)", fill='tozeroy', line=dict(color='#556677', width=1, shape='hv'), fillcolor='rgba(85, 102, 119, 0.15)', hoverinfo='skip'), secondary_y=True)
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['profit_and_loss'], name="Metrics", mode='lines', line=dict(color='rgba(0,0,0,0)'), customdata=df['exact_position'], hovertemplate="PnL: %{y:,.0f} Xirecs<br>Inventory: %{customdata} Lots<extra></extra>", showlegend=False), secondary_y=False)
    
    fig.add_shape(type="line", x0=0, x1=1, xref="x domain", y0=limit, y1=limit, yref="y2", line=dict(color=LOSS_RED, width=1, dash="dash"))
    fig.add_annotation(x=1.0, y=limit, text=str(limit), showarrow=False, xref="paper", yref="y2", font=dict(color=LOSS_RED, size=12, family="JetBrains Mono"), xanchor="right", xshift=-5)
    if show_negative_limit:
        fig.add_shape(type="line", x0=0, x1=1, xref="x domain", y0=-limit, y1=-limit, yref="y2", line=dict(color=LOSS_RED, width=1, dash="dash"))
        fig.add_annotation(x=1.0, y=-limit, text=str(-limit), showarrow=False, xref="paper", yref="y2", font=dict(color=LOSS_RED, size=12, family="JetBrains Mono"), xanchor="right", xshift=-5)

    position_range = [-(limit + 20), limit + 20] if show_negative_limit else [0, limit + 20]

    fig.update_layout(
        title=dict(text="MACRO VIEW — PNL vs. INVENTORY LOCK", font=dict(color="#ffffff", size=11, family="JetBrains Mono"), x=0),
        plot_bgcolor=BG_COLOR, paper_bgcolor=PANEL_BG,
        font=dict(color="#ffffff", family="JetBrains Mono"),
        xaxis=dict(showgrid=True, gridcolor=GRID_COLOR, title="", range=[0, df['timestamp'].max()], tickfont=dict(size=9, color="#ffffff"), linecolor=GRID_COLOR),
        yaxis=dict(showgrid=True, gridcolor=GRID_COLOR, title=dict(text="PnL (Xirecs)", font=dict(color="#ffffff")), tickfont=dict(size=9, color="#ffffff")),
        yaxis2=dict(showgrid=False, title=dict(text=inventory_label, font=dict(color="#ffffff")), tickfont=dict(size=9, color="#ffffff"), range=position_range),
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
        title=dict(text="MICROSTRUCTURE X-RAY — EXECUTIONS vs. BOOK MID", font=dict(color="#ffffff", size=11, family="JetBrains Mono"), x=0),
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
    if our_trades.empty:
        return go.Figure()

    trades_with_mid = our_trades.sort_values('timestamp').copy()

    if not df_mkt.empty and {'timestamp', 'mid_price'}.issubset(df_mkt.columns):
        market_mid = (
            df_mkt[['timestamp', 'mid_price']]
            .dropna(subset=['timestamp'])
            .sort_values('timestamp')
            .rename(columns={'mid_price': 'book_mid'})
        )
        if not market_mid.empty:
            trades_with_mid = pd.merge_asof(trades_with_mid, market_mid, on='timestamp', direction='backward')

    if 'book_mid' not in trades_with_mid.columns:
        trades_with_mid['book_mid'] = np.nan
    if 'mid_price' in trades_with_mid.columns:
        trades_with_mid['book_mid'] = trades_with_mid['book_mid'].fillna(trades_with_mid['mid_price'])

    trades_with_mid = trades_with_mid.dropna(subset=['book_mid', 'price'])
    if trades_with_mid.empty:
        return go.Figure()

    trades_with_mid['quoted_edge'] = np.where(
        trades_with_mid['is_our_buy'],
        trades_with_mid['book_mid'] - trades_with_mid['price'],
        trades_with_mid['price'] - trades_with_mid['book_mid'],
    )
    
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
    
    # Calculate an L3 wall-mid candidate with graceful degradation.
    
    # BIDS
    l2_bid = df['bid_price_2'].fillna(df['bid_price_1'])
    l3_bid = df['bid_price_3'].fillna(l2_bid)
    
    # ASKS
    l2_ask = df['ask_price_2'].fillna(df['ask_price_1'])
    l3_ask = df['ask_price_3'].fillna(l2_ask)
    
    df['wall_mid'] = (l3_bid + l3_ask) / 2.0
    
    fig = go.Figure()
    
    # L1 mid can be noisy when best quotes are being pennyed.
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['mid_price'], mode='lines', name='L1 Mid', line=dict(color='#556677', width=1, dash='dot'), opacity=0.8, hovertemplate="L1 Mid: %{y:.1f}<extra></extra>"))
    
    # Candidate structural mid, not ground truth.
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['wall_mid'], mode='lines', name='L3 Wall Mid Candidate', line=dict(color=IMC_BLUE, width=2), hovertemplate="L3 Wall Mid: %{y:.1f}<extra></extra>"))
    
    # Shade the divergence (when L1 Mid disconnects from Wall Mid)
    df['divergence'] = df['mid_price'] - df['wall_mid']
    
    fig.update_layout(
        title=dict(text=f"L3 WALL MID CANDIDATE vs. L1 MID", font=dict(color="#ffffff", size=11, family="JetBrains Mono"), x=0),
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

def plot_options_risk_timeline(risk_df):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(
        x=risk_df['timestamp'], y=risk_df['combined_pnl'], name="Combined PnL",
        line=dict(color=IMC_BLUE, width=2)
    ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=risk_df['timestamp'], y=risk_df['voucher_pnl'], name="Voucher PnL",
        line=dict(color=PROFIT_GREEN, width=1.5, dash="dot")
    ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=risk_df['timestamp'], y=risk_df['portfolio_delta'], name="Portfolio Delta",
        line=dict(color=LOSS_RED, width=1.5)
    ), secondary_y=True)
    fig.add_trace(go.Scatter(
        x=risk_df['timestamp'], y=risk_df['portfolio_vega_1pct'], name="Vega / 1 vol pt",
        line=dict(color='#a855f7', width=1.2)
    ), secondary_y=True)
    fig.add_trace(go.Scatter(
        x=risk_df['timestamp'], y=risk_df['portfolio_gamma'], name="Gamma",
        line=dict(color='#06d6a0', width=1.2, dash="dot")
    ), secondary_y=True)
    fig.add_trace(go.Scatter(
        x=risk_df['timestamp'], y=risk_df['underlying_position'], name="Underlying Pos",
        line=dict(color='#f59e0b', width=1, dash="dash")
    ), secondary_y=True)

    for level in [-50, -30, -20, 20, 30, 50]:
        fig.add_hline(y=level, line=dict(color="rgba(255,255,255,0.18)", width=1, dash="dash"), secondary_y=True)

    fig.update_layout(
        title=dict(text="OPTIONS RISK TIMELINE — PNL VS DELTA / VEGA", font=dict(color="#ffffff", size=11, family="JetBrains Mono"), x=0),
        plot_bgcolor=BG_COLOR, paper_bgcolor=PANEL_BG,
        font=dict(color=TEXT_COLOR, family="JetBrains Mono", size=10),
        height=440,
        margin=dict(l=0, r=40, t=42, b=0),
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    fig.update_yaxes(title_text="PnL (Xirecs)", secondary_y=False, gridcolor=GRID_COLOR)
    fig.update_yaxes(title_text="Greeks / Position", secondary_y=True, gridcolor=GRID_COLOR)
    return fig

def plot_options_inventory_heatmap(product_frames, option_products):
    if not option_products:
        return go.Figure()
    timestamps = product_frames[option_products[0]]['timestamp'].values
    matrix = []
    for product in option_products:
        frame = product_frames[product].set_index('timestamp').reindex(timestamps).ffill().fillna(0)
        limit = LIMITS.get(product, 300)
        matrix.append((frame['exact_position'].values / limit) * 100.0)
    fig = go.Figure(data=go.Heatmap(
        z=matrix, x=timestamps, y=option_products,
        colorscale=[[0, LOSS_RED], [0.5, BG_COLOR], [1, PROFIT_GREEN]],
        zmid=0,
        colorbar=dict(title="% Limit")
    ))
    fig.update_layout(
        title=dict(text="VOUCHER INVENTORY HEATMAP — POSITION AS % OF LIMIT", font=dict(color="#ffffff", size=11, family="JetBrains Mono"), x=0),
        plot_bgcolor=BG_COLOR, paper_bgcolor=PANEL_BG,
        font=dict(color=TEXT_COLOR, family="JetBrains Mono", size=10),
        height=330,
        margin=dict(l=0, r=20, t=42, b=0)
    )
    return fig

def build_option_detail_frame(product_frames, option_product):
    if option_product not in product_frames or UNDERLYING_PRODUCT not in product_frames:
        return pd.DataFrame()
    opt = product_frames[option_product].copy().sort_values('timestamp')
    under = product_frames[UNDERLYING_PRODUCT][['timestamp', 'mid_price', 'exact_position', 'profit_and_loss']].copy()
    under = under.rename(columns={
        'mid_price': 'spot',
        'exact_position': 'underlying_position',
        'profit_and_loss': 'underlying_pnl',
    }).sort_values('timestamp')
    detail = pd.merge(opt, under, on='timestamp', how='left').ffill()
    strike = strike_from_option(option_product)
    tte = np.maximum((detail['timestamp'].astype(float) / -1_000_000.0 + ROUND3_TTE_DAYS) / DAYS_PER_YEAR, 0.25 / DAYS_PER_YEAR).values
    iv = np.array([implied_vol_scalar(price, spot, strike, t) for price, spot, t in zip(detail['mid_price'], detail['spot'], tte)])
    iv = pd.Series(iv).ffill().fillna(0.0001).values
    delta, gamma, vega = bs_greeks_vector(detail['spot'].values, strike, tte, iv)
    position = detail['exact_position'].astype(float).values
    detail['iv'] = iv
    detail['delta_contrib'] = position * delta
    detail['gamma_contrib'] = position * gamma
    detail['vega_1pct'] = position * vega * 0.01
    return detail

def telemetry_for_option(df_telemetry, option_product):
    if df_telemetry.empty or 'target_product' not in df_telemetry.columns:
        return pd.DataFrame()
    tel = df_telemetry[df_telemetry['target_product'] == option_product].copy()
    if tel.empty:
        return tel
    for col in tel.columns:
        if col not in ['timestamp', 'tag', 'target_product']:
            tel[col] = pd.to_numeric(tel[col], errors='coerce')
    return tel

def plot_option_strike_detail(option_product, detail, trades, telemetry):
    fig = make_subplots(
        rows=3,
        cols=1,
        shared_xaxes=True,
        specs=[[{"secondary_y": False}], [{"secondary_y": True}], [{"secondary_y": True}]],
        vertical_spacing=0.06,
        row_heights=[0.42, 0.32, 0.26],
    )

    fig.add_trace(go.Scatter(
        x=detail['timestamp'], y=detail['ask_price_1'], name="Ask",
        line=dict(color="rgba(248,81,73,0.45)", width=1), hovertemplate="Ask %{y}<extra></extra>"
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=detail['timestamp'], y=detail['bid_price_1'], name="Bid",
        line=dict(color="rgba(63,185,80,0.45)", width=1), fill='tonexty',
        fillcolor="rgba(88,166,255,0.08)", hovertemplate="Bid %{y}<extra></extra>"
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=detail['timestamp'], y=detail['mid_price'], name="Mid",
        line=dict(color=IMC_BLUE, width=2), hovertemplate="Mid %{y}<extra></extra>"
    ), row=1, col=1)

    if not trades.empty:
        our = trades[(trades['product'] == option_product) & (trades['is_our_buy'] | trades['is_our_sell'])].copy()
        buys = our[our['is_our_buy']]
        sells = our[our['is_our_sell']]
        if not buys.empty:
            fig.add_trace(go.Scatter(
                x=buys['timestamp'], y=buys['price'], name="Our Buys",
                mode="markers", marker=dict(color=PROFIT_GREEN, size=9, symbol="triangle-up", line=dict(color="#ffffff", width=1)),
                customdata=buys['quantity'],
                hovertemplate="BUY %{customdata} @ %{y}<extra></extra>"
            ), row=1, col=1)
        if not sells.empty:
            fig.add_trace(go.Scatter(
                x=sells['timestamp'], y=sells['price'], name="Our Sells",
                mode="markers", marker=dict(color=LOSS_RED, size=9, symbol="triangle-down", line=dict(color="#ffffff", width=1)),
                customdata=sells['quantity'],
                hovertemplate="SELL %{customdata} @ %{y}<extra></extra>"
            ), row=1, col=1)

    fair_col = None
    for col in ['fair', 'FAIR']:
        if col in telemetry.columns:
            fair_col = col
            break
    if fair_col is not None and not telemetry.empty:
        fair = telemetry[['timestamp', fair_col]].dropna().groupby('timestamp', as_index=False).last()
        fig.add_trace(go.Scatter(
            x=fair['timestamp'], y=fair[fair_col], name="Logged Fair",
            line=dict(color="#f59e0b", width=1.5, dash="dot"),
            hovertemplate="Fair %{y:.2f}<extra></extra>"
        ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=detail['timestamp'], y=detail['profit_and_loss'], name="PnL",
        line=dict(color=IMC_BLUE, width=2), hovertemplate="PnL %{y:,.0f}<extra></extra>"
    ), row=2, col=1, secondary_y=False)
    fig.add_trace(go.Scatter(
        x=detail['timestamp'], y=detail['exact_position'], name="Position",
        fill='tozeroy', line=dict(color="#8899aa", width=1, shape="hv"), fillcolor="rgba(136,153,170,0.15)",
        hovertemplate="Pos %{y}<extra></extra>"
    ), row=2, col=1, secondary_y=True)
    limit = LIMITS.get(option_product, 300)
    fig.add_hline(y=limit, line=dict(color="rgba(248,81,73,0.5)", width=1, dash="dash"), row=2, col=1, secondary_y=True)
    fig.add_hline(y=-limit, line=dict(color="rgba(248,81,73,0.5)", width=1, dash="dash"), row=2, col=1, secondary_y=True)

    fig.add_trace(go.Scatter(
        x=detail['timestamp'], y=detail['delta_contrib'], name="Delta",
        line=dict(color=LOSS_RED, width=1.5), hovertemplate="Delta %{y:.2f}<extra></extra>"
    ), row=3, col=1, secondary_y=False)
    fig.add_trace(go.Scatter(
        x=detail['timestamp'], y=detail['vega_1pct'], name="Vega / 1 vol pt",
        line=dict(color="#a855f7", width=1.2), hovertemplate="Vega1% %{y:.2f}<extra></extra>"
    ), row=3, col=1, secondary_y=False)
    fig.add_trace(go.Scatter(
        x=detail['timestamp'], y=detail['gamma_contrib'], name="Gamma",
        line=dict(color="#06d6a0", width=1.2, dash="dot"), hovertemplate="Gamma %{y:.4f}<extra></extra>"
    ), row=3, col=1, secondary_y=True)

    for sig_col, color in [('z', '#f59e0b'), ('edge', '#ffffff')]:
        if sig_col in telemetry.columns and not telemetry.empty:
            sig = telemetry[['timestamp', sig_col]].dropna().groupby('timestamp', as_index=False).last()
            if not sig.empty:
                fig.add_trace(go.Scatter(
                    x=sig['timestamp'], y=sig[sig_col], name=sig_col.upper(),
                    line=dict(color=color, width=1, dash="dash"),
                    hovertemplate=f"{sig_col.upper()} " + "%{y:.2f}<extra></extra>"
                ), row=3, col=1, secondary_y=True)

    fig.update_layout(
        title=dict(text=f"{option_product} — STRIKE DETAIL", font=dict(color="#ffffff", size=11, family="JetBrains Mono"), x=0),
        plot_bgcolor=BG_COLOR, paper_bgcolor=PANEL_BG,
        font=dict(color=TEXT_COLOR, family="JetBrains Mono", size=10),
        height=760,
        margin=dict(l=0, r=50, t=42, b=0),
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="right", x=1)
    )
    fig.update_yaxes(title_text="Price", row=1, col=1, gridcolor=GRID_COLOR)
    fig.update_yaxes(title_text="PnL", row=2, col=1, secondary_y=False, gridcolor=GRID_COLOR)
    fig.update_yaxes(title_text="Position", row=2, col=1, secondary_y=True, gridcolor=GRID_COLOR)
    fig.update_yaxes(title_text="Delta / Vega", row=3, col=1, secondary_y=False, gridcolor=GRID_COLOR)
    fig.update_yaxes(title_text="Gamma / Signal", row=3, col=1, secondary_y=True, gridcolor=GRID_COLOR)
    return fig

def render_options_risk_page(df_market, df_trades, product_frames, selected_assets):
    option_products = [p for p in OPTION_PRODUCTS if p in selected_assets and p in product_frames]
    risk_df, option_products = build_options_risk_frame(product_frames, selected_assets)
    if risk_df.empty:
        st.warning("Options Risk needs VELVETFRUIT_EXTRACT and at least one VEV_* voucher selected.")
        return

    window, dd_rows = options_drawdown_attribution(risk_df, product_frames, option_products)
    final_combined = float(risk_df['combined_pnl'].iloc[-1])
    final_voucher = float(risk_df['voucher_pnl'].iloc[-1])
    final_underlying = float(risk_df['underlying_pnl'].iloc[-1])
    max_dd = window['drawdown'] if window else 0.0
    avg_abs_delta = float(risk_df['portfolio_delta'].abs().mean())
    max_abs_delta = float(risk_df['portfolio_delta'].abs().max())
    avg_abs_vega = float(risk_df['portfolio_vega_1pct'].abs().mean())
    max_abs_vega = float(risk_df['portfolio_vega_1pct'].abs().max())
    avg_abs_gamma = float(risk_df['portfolio_gamma'].abs().mean())
    max_abs_gamma = float(risk_df['portfolio_gamma'].abs().max())
    max_gross = float(risk_df['gross_voucher_position'].max())

    st.markdown('<div class="section-label">OPTIONS RISK / VOUCHER BOOK</div>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="metric-grid-5">
            {metric_card("COMBINED PNL", f"{final_combined:,.0f} $", "vouchers + underlying", "pos" if final_combined >= 0 else "neg", "cyan")}
            {metric_card("VOUCHER PNL", f"{final_voucher:,.0f} $", "options only", "pos" if final_voucher >= 0 else "neg", "")}
            {metric_card("UNDERLYING PNL", f"{final_underlying:,.0f} $", "hedge / delta-1", "pos" if final_underlying >= 0 else "neg", "amber")}
            {metric_card("MAX DRAWDOWN", f"{max_dd:,.0f} $", "combined curve", "neg" if max_dd > 0 else "", "red")}
            {metric_card("MAX GROSS VOUCHERS", f"{max_gross:,.0f}", "sum abs voucher pos", "amber" if max_gross > 600 else "", "purple")}
        </div>
        <div class="metric-grid-4">
            {metric_card("AVG |DELTA|", f"{avg_abs_delta:,.1f}", "portfolio", "amber" if avg_abs_delta > 20 else "pos", "")}
            {metric_card("MAX |DELTA|", f"{max_abs_delta:,.1f}", "portfolio", "neg" if max_abs_delta > 50 else ("amber" if max_abs_delta > 30 else "pos"), "red")}
            {metric_card("AVG |VEGA|", f"{avg_abs_vega:,.1f}", "per 1 vol point", "", "")}
            {metric_card("MAX |VEGA|", f"{max_abs_vega:,.1f}", "per 1 vol point", "amber" if max_abs_vega > 300 else "", "purple")}
        </div>
        <div class="metric-grid-3">
            {metric_card("AVG |GAMMA|", f"{avg_abs_gamma:,.3f}", "portfolio", "", "cyan")}
            {metric_card("MAX |GAMMA|", f"{max_abs_gamma:,.3f}", "portfolio", "amber" if max_abs_gamma > 2 else "", "cyan")}
            {metric_card("VOUCHERS TRACKED", f"{len(option_products)}", "selected VEV products", "", "")}
        </div>
    """, unsafe_allow_html=True)

    st.plotly_chart(plot_options_risk_timeline(risk_df), width='stretch', key="options_risk_timeline")

    if window:
        st.markdown('<div class="section-label">DRAWDOWN ATTRIBUTION</div>', unsafe_allow_html=True)
        st.markdown(f"""
            <div class="metric-grid-5">
                {metric_card("DD WINDOW", f"{window['peak_ts']} -> {window['trough_ts']}", "peak to trough", "", "")}
                {metric_card("SPOT MOVE", f"{window['spot_move']:,.1f}", "underlying points", "amber" if abs(window['spot_move']) > 5 else "", "amber")}
                {metric_card("START DELTA", f"{window['start_delta']:,.1f}", "portfolio delta at peak", "neg" if abs(window['start_delta']) > 40 else "amber", "red")}
                {metric_card("DELTA EST PNL", f"{window['delta_estimate']:,.0f} $", "start delta x spot move", "neg" if window['delta_estimate'] < 0 else "pos", "")}
                {metric_card("UNEXPLAINED", f"{window['unexplained']:,.0f} $", "actual minus delta estimate", "neg" if window['unexplained'] < 0 else "pos", "purple")}
            </div>
        """, unsafe_allow_html=True)
        dd_show = dd_rows.rename(columns={
            'product': 'Product',
            'pnl_change': 'PnL Chg',
            'start_pos': 'Start Pos',
            'end_pos': 'End Pos',
            'start_pnl': 'Start PnL',
            'end_pnl': 'End PnL',
        })
        st.dataframe(
            dd_show.style.format({'PnL Chg': '{:,.0f}', 'Start PnL': '{:,.0f}', 'End PnL': '{:,.0f}', 'Start Pos': '{:,.0f}', 'End Pos': '{:,.0f}'}),
            width='stretch',
            height=260,
        )

    st.markdown('<div class="section-label">PER-VOUCHER RISK MATRIX</div>', unsafe_allow_html=True)
    summary = option_product_summary(product_frames, df_trades, option_products, dd_rows)
    if not summary.empty:
        st.dataframe(
            summary.style.format({
                'Final PnL': '{:,.0f}', 'DD Chg': '{:,.0f}', 'Avg Abs Pos': '{:,.1f}',
                'Time >50% Lim': '{:,.1f}%', 'Avg Buy': '{:,.2f}', 'Avg Sell': '{:,.2f}'
            }),
            width='stretch',
            height=330,
        )

    st.plotly_chart(plot_options_inventory_heatmap(product_frames, option_products), width='stretch', key="options_inventory_heatmap")

    st.markdown('<div class="section-label">PER-STRIKE DIAGNOSTIC</div>', unsafe_allow_html=True)
    default_idx = option_products.index('VEV_5200') if 'VEV_5200' in option_products else 0
    focus_option = st.selectbox(
        "FOCUS VOUCHER",
        option_products,
        index=default_idx,
        help="Inspect one strike at a time: market/fills, PnL/position, Greeks, and logged signal overlays.",
    )
    detail = build_option_detail_frame(product_frames, focus_option)
    tel = telemetry_for_option(df_telemetry, focus_option)
    if detail.empty:
        st.info("No detail data available for selected voucher.")
    else:
        st.plotly_chart(
            plot_option_strike_detail(focus_option, detail, df_trades, tel),
            width='stretch',
            key=f"option_detail_{focus_option}",
        )

    st.markdown('<div class="section-label">FILL QUALITY / MARKOUTS</div>', unsafe_allow_html=True)
    quality = fill_quality_table(df_trades, product_frames, option_products)
    if quality.empty:
        st.info("No own voucher fills found.")
    else:
        markout_cols = [c for c in quality.columns if c.startswith('T+')]
        fmt = {col: '{:,.2f}' for col in markout_cols}
        fmt['Qty'] = '{:,.0f}'
        st.dataframe(quality.style.format(fmt), width='stretch', height=360)

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
selected_assets = []
metric_scope = "SELECTED ASSETS"
page_mode = st.sidebar.radio(
    "PAGE",
    ["EXECUTION DASHBOARD", "OPTIONS RISK"],
    index=0,
    help="OPTIONS RISK is a dedicated voucher-book page for PnL, Greeks, drawdowns, fills, and inventory.",
)

if uploaded_file:
    df_market, df_trades, df_telemetry, error = process_log_file(uploaded_file)
    if error:
        st.error(error)
        st.stop()
    st.sidebar.success("✓ LOG PARSED SUCCESSFULLY")
    product_options = list(df_market['product'].dropna().unique())
    if len(product_options) > 0:
        product_signature = tuple(product_options)
        if st.session_state.get("asset_filter_signature") != product_signature:
            st.session_state["asset_filter_signature"] = product_signature
            st.session_state["selected_assets"] = product_options.copy()

        asset_btn_col1, asset_btn_col2 = st.sidebar.columns(2)
        if asset_btn_col1.button("SELECT ALL", use_container_width=True):
            st.session_state["selected_assets"] = product_options.copy()
        if asset_btn_col2.button("CLEAR", use_container_width=True):
            st.session_state["selected_assets"] = []

        selected_assets = st.sidebar.multiselect(
            "SELECT ASSETS",
            product_options,
            key="selected_assets",
            help="Use SELECT ALL for full-round logs, then remove any product tag such as HYDROGEL_PACK with one click.",
        )

        if selected_assets:
            selected_product = st.sidebar.selectbox("FOCUS ASSET", selected_assets)
            if len(selected_assets) > 1:
                metric_scope = st.sidebar.radio(
                    "METRIC SCOPE",
                    ["SELECTED ASSETS", "FOCUS ASSET"],
                    index=0,
                    help="Top metrics and the macro chart use this scope. Product-specific forensic panels still use the focus asset.",
                )
            df_market = df_market[df_market['product'].isin(selected_assets)].copy()
            if not df_trades.empty and 'product' in df_trades.columns:
                df_trades = df_trades[df_trades['product'].isin(selected_assets)].copy()
            if not df_telemetry.empty and 'target_product' in df_telemetry.columns:
                df_telemetry = df_telemetry[df_telemetry['target_product'].isin(selected_assets)].copy()
        else:
            st.sidebar.warning("Select at least one asset to render the dashboard.")

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
    product_frames = build_product_frames(df_market, df_trades, df_telemetry)

    if page_mode == "OPTIONS RISK":
        render_options_risk_page(df_market, df_trades, product_frames, selected_assets)
        st.stop()

    df_mkt_focus = product_frames[selected_product].copy()
    df_trd_focus = attach_book_context_to_trades(df_trades, product_frames, [selected_product])

    scope_products = selected_assets if metric_scope == "SELECTED ASSETS" else [selected_product]
    scope_is_portfolio = metric_scope == "SELECTED ASSETS" and len(scope_products) > 1
    scope_label = "SELECTED_ASSETS" if scope_is_portfolio else selected_product
    if scope_is_portfolio:
        df_mkt_prod = build_portfolio_frame({product: product_frames[product] for product in scope_products if product in product_frames})
        df_trd_prod = attach_book_context_to_trades(df_trades, product_frames, scope_products)
        inventory_label = "Total |Position| (Lots)"
        show_negative_limit = False
        limit = combined_limit(scope_products)
    else:
        df_mkt_prod = df_mkt_focus.copy()
        df_trd_prod = df_trd_focus.copy()
        inventory_label = "Net Position (Lots)"
        show_negative_limit = True
        limit = LIMITS.get(selected_product, 80)
    
    # --- METRIC CALCULATIONS ---
    final_pnl = df_mkt_prod['profit_and_loss'].iloc[-1]
    pnl_series = df_mkt_prod['profit_and_loss']
    pnl_diff = pnl_series.diff().fillna(0)
    max_drawdown = abs((pnl_series - pnl_series.cummax()).min())
    
    # Granular Profit Factor
    maker_pnl, taker_pnl = 0.0, 0.0
    if not df_trd_prod.empty:
        our_trades = df_trd_prod[df_trd_prod['is_our_buy'] | df_trd_prod['is_our_sell']].copy()
        if not our_trades.empty:
            # Value each trade against its own product's end-of-log mid price.
            our_trades['trade_pnl'] = np.where(our_trades['is_our_buy'], 
                                               (our_trades['final_mid'] - our_trades['price']) * our_trades['quantity'],
                                               (our_trades['price'] - our_trades['final_mid']) * our_trades['quantity'])
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
    abs_position = df_mkt_prod['exact_position'].abs()
    time_locked = np.mean(abs_position.values >= limit) * 100
    near_50 = np.mean(abs_position.values >= 0.50 * limit) * 100
    near_75 = np.mean(abs_position.values >= 0.75 * limit) * 100
    near_90 = np.mean(abs_position.values >= 0.90 * limit) * 100
    max_abs_position = abs_position.max()
    avg_abs_position = abs_position.mean()
    skew_bias = df_mkt_prod['net_position'].mean() if 'net_position' in df_mkt_prod.columns else df_mkt_prod['exact_position'].mean()
    pnl_per_max_dd = final_pnl / max_drawdown if max_drawdown > 0 else np.nan
    pnl_per_avg_abs_position = final_pnl / avg_abs_position if avg_abs_position > 0 else np.nan
    selected_buckets = pnl_buckets(df_mkt_prod)
    worst_selected_bucket = min((b['bucket_pnl'] for b in selected_buckets), default=0.0)
    negative_selected_buckets = sum(1 for b in selected_buckets if b['bucket_pnl'] < 0)

    adv_selection, win_rate, info_ratio = 0, 0, 0
    m_trades = pd.DataFrame()
    if not df_trd_prod.empty:
        our_trades = df_trd_prod[df_trd_prod['is_our_buy'] | df_trd_prod['is_our_sell']].copy()
        if not our_trades.empty:
            m_trades = build_markout_trades(our_trades, product_frames, markout_horizon)
            if not m_trades.empty:
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
        pnl_tooltip = "M/T values mark trades to final mid; not official realized PnL attribution."
        pnl_subtext = f"<span title='{pnl_tooltip}'>M: <span style='color:{m_color}; font-weight:600;'>{maker_pnl:,.0f}</span> | T: <span style='color:{t_color}; font-weight:600;'>{taker_pnl:,.0f}</span></span>"
        
        st.markdown(f"""
            <div class="metric-grid-5">
                {metric_card("FINAL PNL", f"{final_pnl:,.0f} $", pnl_subtext, pnl_color, "cyan")}
                {metric_card("VOLUME TRADED", f"{total_vol:,.0f}", "Lots", "", "")}
                {metric_card("PNL PER LOT", f"{pnl_per_lot:,.2f} $", "Xirecs / Lot", ppl_color, "purple")}
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

        # Row 3: Position & Risk Efficiency
        st.markdown('<div class="section-label">📉&nbsp;&nbsp;POSITION & RISK EFFICIENCY</div>', unsafe_allow_html=True)

        near75_color = "neg" if near_75 > 25 else ("amber" if near_75 > 5 else "pos")
        near90_color = "neg" if near_90 > 10 else ("amber" if near_90 > 2 else "pos")
        risk_color = "pos" if not pd.isna(pnl_per_max_dd) and pnl_per_max_dd >= 3 else ("amber" if not pd.isna(pnl_per_max_dd) and pnl_per_max_dd >= 1 else "neg")
        inv_eff_color = "pos" if not pd.isna(pnl_per_avg_abs_position) and pnl_per_avg_abs_position > 0 else ("neg" if not pd.isna(pnl_per_avg_abs_position) and pnl_per_avg_abs_position < 0 else "")
        bucket_color = "neg" if worst_selected_bucket < 0 else "pos"

        st.markdown(f"""
            <div class="metric-grid-4">
                {metric_card("TIME >= 50% LIMIT", f"{near_50:.1f}%", "early inventory pressure", "amber" if near_50 > 25 else "", "")}
                {metric_card("TIME >= 75% LIMIT", f"{near_75:.1f}%", "near lockup zone", near75_color, "amber")}
                {metric_card("TIME >= 90% LIMIT", f"{near_90:.1f}%", "danger zone", near90_color, "red")}
                {metric_card("AVG ABS POSITION", f"{avg_abs_position:,.1f}", "risk carried", "amber" if avg_abs_position >= 0.50 * limit else "", "")}
            </div>
            <div class="metric-grid-3">
                {metric_card("PNL / MAX DD", format_metric_number(pnl_per_max_dd, 2), "higher is cleaner", risk_color, "cyan")}
                {metric_card("PNL / AVG ABS POS", format_metric_number(pnl_per_avg_abs_position, 1), "PnL per lot carried", inv_eff_color, "purple")}
                {metric_card("WORST PNL BUCKET", f"{worst_selected_bucket:,.0f} $", f"{negative_selected_buckets} negative buckets", bucket_color, "red")}
            </div>
        """, unsafe_allow_html=True)

        # Row 4: Advanced Forensics
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
    scope_key_prefix = scope_label.replace(" ", "_").replace("/", "_")
    chart_key_prefix = selected_product.replace(" ", "_").replace("/", "_")
    st.plotly_chart(
        plot_pnl_inventory(
            df_mkt_prod,
            scope_label,
            limit_override=limit,
            inventory_label=inventory_label,
            show_negative_limit=show_negative_limit,
        ),
        width='stretch',
        key=f"{scope_key_prefix}_pnl_inventory",
    )

    focus_our_trades = df_trd_focus[df_trd_focus['is_our_buy'] | df_trd_focus['is_our_sell']].copy() if not df_trd_focus.empty else pd.DataFrame()
    m_trades_focus = build_markout_trades(focus_our_trades, product_frames, markout_horizon)

    st.plotly_chart(plot_microstructure_xray(df_mkt_focus, df_trd_focus), width='stretch', key=f"{chart_key_prefix}_microstructure_xray")
    
    st.markdown("---")
    st.markdown('<div class="section-label">🤖&nbsp;&nbsp;BOT BEHAVIOR & FLOW DYNAMICS</div>', unsafe_allow_html=True)
    
    c5, c6 = st.columns(2)
    with c5: st.plotly_chart(plot_magic_size_fingerprinter(df_mkt_focus, df_trd_focus, markout_horizon), width='stretch', key=f"{chart_key_prefix}_magic_size")
    with c6: st.plotly_chart(plot_liquidation_radar(df_mkt_focus, df_trd_focus), width='stretch', key=f"{chart_key_prefix}_liquidation_radar")
    
    st.markdown("---")
    st.markdown('<div class="section-label">🎯&nbsp;&nbsp;MOMENTUM & WALL ANALYTICS</div>', unsafe_allow_html=True)
    
    st.plotly_chart(plot_true_mid_divergence(df_mkt_focus), width='stretch', key=f"{chart_key_prefix}_true_mid_divergence")
    st.plotly_chart(plot_vwap_momentum(df_mkt_focus, df_trd_focus, vwap_window), width='stretch', key=f"{chart_key_prefix}_vwap_momentum")
    
    st.markdown("---")
    st.markdown('<div class="section-label">🔬&nbsp;&nbsp;EXECUTION & FLOW ANALYSIS</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1: st.plotly_chart(plot_toxicity_markout(m_trades_focus, markout_horizon), width='stretch', key=f"{chart_key_prefix}_toxicity_markout")
    with c2: st.plotly_chart(plot_spread_capture(m_trades_focus, df_mkt_focus), width='stretch', key=f"{chart_key_prefix}_spread_capture")

    c3, c4 = st.columns(2)
    with c3: st.plotly_chart(plot_imbalance_matrix(m_trades_focus, df_mkt_focus, imbalance_level), width='stretch', key=f"{chart_key_prefix}_imbalance_matrix")
    with c4: st.plotly_chart(plot_whale_profiler(df_trd_focus), width='stretch', key=f"{chart_key_prefix}_whale_profiler")

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
        st.plotly_chart(
            plot_telemetry_brainwaves(df_mkt_focus, df_trd_focus, df_tel_prod, selected_signals),
            width='stretch',
            key=f"{chart_key_prefix}_telemetry_brainwaves",
        )

    st.markdown("---")
    render_portfolio_submission_summary(df_market, product_frames)

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
