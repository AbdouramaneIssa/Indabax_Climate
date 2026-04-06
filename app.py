# ════════════════════════════════════════════════════════════════════════════════
#  HACKATHON INDABAX CAMEROON 2026
#  Dashboard — Qualité de l'Air au Cameroun
#  Modèle : LightGBM  |  Cible : PM2.5 proxy
#  Design : Biopunk Organique · Nature & Technologie
# ════════════════════════════════════════════════════════════════════════════════

import streamlit as st
import streamlit.components.v1 as components
import joblib
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ── Configuration de la page ──────────────────────────────────────────────────
st.set_page_config(
    page_title="IndabaX · IndabaX Cameroon 2026",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ════════════════════════════════════════════════════════════════════════════════
#  STYLES GLOBAUX — Design Biopunk Organique
# ════════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,100;0,9..144,300;0,9..144,400;0,9..144,700;1,9..144,100;1,9..144,300;1,9..144,700&family=Syne:wght@400;600;700;800&family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Nunito:wght@300;400;600&display=swap');

  :root {
    --night:    #050d0a;
    --deep:     #091410;
    --forest:   #0d1f18;
    --moss:     #122b22;
    --card:     rgba(12,28,22,0.82);
    --glass:    rgba(15,35,28,0.65);
    --jade:     #00c896;
    --mint:     #4dffc3;
    --sage:     #7fc9a8;
    --fern:     #2a8a64;
    --lime:     #a8e63d;
    --amber:    #f5a623;
    --fire:     #ff5e3a;
    --crimson:  #e8354a;
    --gold:     #ffd166;
    --sky:      #38bdf8;
    --mist:     #7eb8d4;
    --text:     #d8efe7;
    --muted:    #5a8a78;
    --ghost:    #2a4a3a;
    --light:    #c2dfd5;
    --border:   rgba(0,200,150,0.10);
    --glow:     rgba(0,200,150,0.15);
    --r:  8px;
    --rl: 16px;
    --rxl: 24px;
  }

  html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
    background: var(--night) !important;
    color: var(--text) !important;
  }

  .stApp {
    background:
      radial-gradient(ellipse 90% 60% at 5% 5%,   rgba(0,200,150,0.06) 0%, transparent 55%),
      radial-gradient(ellipse 70% 50% at 95% 90%,  rgba(168,230,61,0.04) 0%, transparent 50%),
      radial-gradient(ellipse 60% 70% at 50% 100%, rgba(0,200,150,0.05) 0%, transparent 60%),
      radial-gradient(ellipse 80% 40% at 80% 15%,  rgba(56,189,248,0.03) 0%, transparent 50%),
      linear-gradient(175deg, #050d0a 0%, #071209 40%, #050d0a 100%) !important;
    min-height: 100vh;
    position: relative;
    overflow-x: hidden;
  }

  .stApp::before {
    content: '';
    position: fixed;
    top: -200px; left: -200px;
    width: 500px; height: 500px;
    background: radial-gradient(circle, rgba(0,200,150,0.04) 0%, transparent 65%);
    border-radius: 50%;
    animation: orbFloat 18s ease-in-out infinite;
    pointer-events: none;
    z-index: 0;
  }
  .stApp::after {
    content: '';
    position: fixed;
    bottom: -150px; right: -150px;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(168,230,61,0.04) 0%, transparent 65%);
    border-radius: 50%;
    animation: orbFloat 22s ease-in-out infinite reverse;
    pointer-events: none;
    z-index: 0;
  }

  @keyframes orbFloat {
    0%, 100% { transform: translate(0, 0) scale(1); }
    33%       { transform: translate(60px, 40px) scale(1.1); }
    66%       { transform: translate(-30px, 70px) scale(0.95); }
  }

  [data-testid="stSidebar"] {
    background: rgba(5,13,10,0.97) !important;
    border-right: 1px solid var(--border) !important;
    backdrop-filter: blur(24px) saturate(150%);
    position: relative;
  }
  [data-testid="stSidebar"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, transparent, var(--jade), var(--lime), transparent);
    animation: scanLine 4s ease-in-out infinite;
  }
  @keyframes scanLine {
    0%   { opacity: 0.3; transform: scaleX(0.8); }
    50%  { opacity: 1;   transform: scaleX(1); }
    100% { opacity: 0.3; transform: scaleX(0.8); }
  }
  [data-testid="stSidebar"] > div { padding-top: 0 !important; }

  .logo-block {
    padding: 1.5rem 1.4rem 1.2rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
    background: linear-gradient(180deg, rgba(0,200,150,0.04) 0%, transparent 100%);
  }
  .logo-block::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0;
    height: 1px; width: 40%;
    background: linear-gradient(90deg, var(--jade), transparent);
    animation: logoUnderline 3s ease-in-out infinite;
  }
  @keyframes logoUnderline {
    0%   { width: 30%; opacity: 0.5; }
    50%  { width: 70%; opacity: 1; }
    100% { width: 30%; opacity: 0.5; }
  }

  .indabax-logo-wrap {
    display: flex; align-items: center; gap: 10px; margin-bottom: 0.6rem;
  }
  .indabax-tree-badge {
    width: 48px; height: 48px; border-radius: 50%;
    border: 1.5px solid rgba(0,200,150,0.30);
    background: rgba(0,200,150,0.06);
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0; animation: glyphBreath 4s ease-in-out infinite;
  }
  @keyframes glyphBreath {
    0%, 100% { box-shadow: 0 0 16px rgba(0,200,150,0.15); }
    50%       { box-shadow: 0 0 32px rgba(0,200,150,0.35); }
  }
  .indabax-wordmark { display: flex; flex-direction: column; gap: 1px; }
  .indabax-deep {
    font-family: 'Space Mono', monospace;
    font-size: 7px; letter-spacing: 3px; color: var(--ghost);
    text-transform: uppercase; line-height: 1;
  }
  .indabax-main {
    font-family: 'Syne', sans-serif;
    font-size: 1.45rem; font-weight: 800; line-height: 1; letter-spacing: -0.5px;
  }
  .indabax-main .ix  { color: var(--jade); }
  .indabax-main .dot { color: var(--lime); font-size: 1rem; }
  .indabax-main .cam { color: var(--text); font-weight: 400; font-style: italic; font-family: 'Fraunces', serif; }
  .indabax-sub {
    font-family: 'Space Mono', monospace;
    font-size: 7.5px; letter-spacing: 2.5px; color: var(--muted);
    text-transform: uppercase; margin-top: 2px;
  }
  .indabax-year-badge {
    display: inline-flex; align-items: center; gap: 5px;
    background: rgba(168,230,61,0.08); border: 1px solid rgba(168,230,61,0.18);
    border-radius: 12px; padding: 2px 8px;
    font-family: 'Space Mono', monospace; font-size: 8px;
    color: var(--lime); letter-spacing: 1px; margin-top: 6px;
  }

  .sb-label {
    font-family: 'Space Mono', monospace;
    font-size: 8px; letter-spacing: 3px; text-transform: uppercase;
    color: var(--ghost); margin: 1.2rem 0 0.4rem 0.2rem;
    display: flex; align-items: center; gap: 8px;
  }
  .sb-label::before {
    content: ''; display: inline-block;
    width: 14px; height: 1px; background: var(--jade); opacity: 0.5;
  }

  .model-panel {
    background: linear-gradient(135deg, rgba(0,200,150,0.05) 0%, rgba(42,138,100,0.03) 100%);
    border: 1px solid rgba(0,200,150,0.12);
    border-radius: var(--r);
    padding: 1rem 1.1rem; margin: 0.5rem 0;
    position: relative; overflow: hidden;
  }
  .model-panel::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,200,150,0.4), transparent);
  }
  .mp-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: 6px 0; border-bottom: 1px solid rgba(0,200,150,0.05);
  }
  .mp-row:last-child { border: none; }
  .mp-label { font-size: 11px; color: var(--muted); font-family: 'Nunito'; }
  .mp-val { font-family: 'Space Mono', monospace; font-size: 11px; color: var(--jade); }

  .active-pill {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(0,200,150,0.08); border: 1px solid rgba(0,200,150,0.20);
    border-radius: 20px; padding: 4px 10px;
    font-family: 'Space Mono', monospace; font-size: 9px;
    color: var(--jade); letter-spacing: 1px; margin-bottom: 1rem;
  }
  .active-dot {
    width: 5px; height: 5px; border-radius: 50%; background: var(--jade);
    animation: pulse 2s ease-in-out infinite;
  }
  @keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.4; transform: scale(0.7); }
  }

  .hero {
    position: relative; border: 1px solid var(--border); border-radius: var(--rxl);
    padding: 3rem 3.5rem; margin-bottom: 2rem; overflow: hidden;
    background: var(--glass); backdrop-filter: blur(16px);
    animation: heroReveal 0.8s cubic-bezier(0.16,1,0.3,1) both;
  }
  @keyframes heroReveal {
    from { opacity: 0; transform: translateY(-24px); }
    to   { opacity: 1; transform: translateY(0); }
  }
  .hero::before {
    content: ''; position: absolute; top: -100px; right: -100px;
    width: 350px; height: 350px;
    background: radial-gradient(circle, rgba(0,200,150,0.08) 0%, transparent 65%);
    border-radius: 50%; animation: heroOrb1 8s ease-in-out infinite;
  }
  .hero::after {
    content: ''; position: absolute; bottom: -80px; left: 40%;
    width: 280px; height: 280px;
    background: radial-gradient(circle, rgba(168,230,61,0.05) 0%, transparent 65%);
    border-radius: 50%; animation: heroOrb1 11s ease-in-out infinite reverse;
  }
  @keyframes heroOrb1 {
    0%, 100% { transform: translate(0,0) scale(1); }
    50%       { transform: translate(20px, -20px) scale(1.1); }
  }
  .hero-scan {
    position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    background: repeating-linear-gradient(
      0deg, transparent, transparent 2px,
      rgba(0,200,150,0.012) 2px, rgba(0,200,150,0.012) 4px
    );
    pointer-events: none;
  }
  .hero-badge {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(0,200,150,0.07); border: 1px solid rgba(0,200,150,0.22);
    border-radius: 30px; padding: 6px 16px 6px 10px;
    font-family: 'Space Mono', monospace; font-size: 9.5px;
    color: var(--jade); letter-spacing: 2px; text-transform: uppercase;
    margin-bottom: 1.2rem; position: relative; z-index: 1;
  }
  .hero-badge-icon {
    width: 22px; height: 22px; border-radius: 50%;
    background: linear-gradient(135deg, var(--jade), var(--fern));
    display: flex; align-items: center; justify-content: center; font-size: 11px;
  }
  .hero-title {
    font-family: 'Fraunces', serif;
    font-size: clamp(2.2rem, 4vw, 3.6rem); font-weight: 300; font-style: italic;
    color: var(--text); line-height: 1.1; margin: 0 0 0.3rem;
    position: relative; z-index: 1; letter-spacing: -1px;
  }
  .hero-title em {
    font-style: normal; font-weight: 700; color: var(--jade);
    background: linear-gradient(90deg, var(--jade), var(--mint));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
  }
  .hero-sub {
    font-family: 'Nunito', sans-serif; font-size: 0.9rem; color: var(--muted);
    font-weight: 300; margin: 0 0 1.5rem; position: relative; z-index: 1;
    max-width: 640px; line-height: 1.6;
  }
  .hero-chips { display: flex; gap: 10px; flex-wrap: wrap; position: relative; z-index: 1; }
  .hero-chip {
    display: inline-flex; align-items: center; gap: 7px;
    background: rgba(0,200,150,0.06); border: 1px solid rgba(0,200,150,0.14);
    border-radius: var(--r); padding: 6px 13px;
    font-family: 'Space Mono', monospace; font-size: 9.5px;
    color: var(--sage); letter-spacing: 0.5px; transition: all 0.25s;
  }
  .hero-chip.active { background: rgba(0,200,150,0.12); border-color: rgba(0,200,150,0.30); color: var(--jade); }
  .chip-dot { width: 5px; height: 5px; border-radius: 50%; }

  .kpi-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.1rem; margin-bottom: 2rem; }
  .kpi {
    background: var(--glass); border: 1px solid var(--border); border-radius: var(--rl);
    padding: 1.5rem 1.6rem 1.2rem; backdrop-filter: blur(12px);
    position: relative; overflow: hidden;
    transition: transform 0.3s cubic-bezier(0.34,1.56,0.64,1), border-color 0.3s, box-shadow 0.3s;
    animation: kpiReveal 0.6s cubic-bezier(0.16,1,0.3,1) both; cursor: default;
  }
  .kpi:hover {
    transform: translateY(-5px) scale(1.01);
    border-color: rgba(0,200,150,0.22);
    box-shadow: 0 12px 40px rgba(0,0,0,0.3), 0 0 0 1px rgba(0,200,150,0.08);
  }
  @keyframes kpiReveal {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
  }
  .kpi:nth-child(1) { animation-delay: 0.1s; }
  .kpi:nth-child(2) { animation-delay: 0.18s; }
  .kpi:nth-child(3) { animation-delay: 0.26s; }
  .kpi:nth-child(4) { animation-delay: 0.34s; }
  .kpi::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    border-radius: var(--rl) var(--rl) 0 0; transition: opacity 0.3s;
  }
  .kpi.jade::before   { background: linear-gradient(90deg, var(--jade), var(--mint)); }
  .kpi.amber::before  { background: linear-gradient(90deg, var(--amber), var(--gold)); }
  .kpi.sky::before    { background: linear-gradient(90deg, var(--sky), #7dd3fc); }
  .kpi.lime::before   { background: linear-gradient(90deg, var(--lime), #d9f99d); }
  .kpi-icon { font-size: 1.2rem; margin-bottom: 0.8rem; display: block; }
  .kpi-label {
    font-family: 'Space Mono', monospace; font-size: 8.5px; letter-spacing: 2.5px;
    text-transform: uppercase; color: var(--ghost); margin-bottom: 0.6rem;
  }
  .kpi-val {
    font-family: 'Fraunces', serif; font-size: 3rem; font-weight: 700;
    line-height: 1; margin-bottom: 0.3rem; position: relative; z-index: 1;
  }
  .kpi-val.jade-c  { color: var(--jade); }
  .kpi-val.amber-c { color: var(--amber); }
  .kpi-val.sky-c   { color: var(--sky); }
  .kpi-val.lime-c  { color: var(--lime); }
  .kpi-hint { font-size: 11px; color: var(--ghost); font-weight: 300; }

  .sec-head { display: flex; align-items: center; gap: 12px; margin-bottom: 1.3rem; }
  .sec-icon {
    width: 32px; height: 32px; border-radius: 8px;
    background: linear-gradient(135deg, rgba(0,200,150,0.15), rgba(0,200,150,0.05));
    border: 1px solid rgba(0,200,150,0.15);
    display: flex; align-items: center; justify-content: center; font-size: 15px; flex-shrink: 0;
  }
  .sec-text { font-family: 'Fraunces', serif; font-size: 1.05rem; font-weight: 600; color: var(--light); letter-spacing: 0.02em; }
  .sec-line { flex: 1; height: 1px; background: linear-gradient(90deg, rgba(0,200,150,0.15), transparent); }
  .sec-tag {
    font-family: 'Space Mono', monospace; font-size: 8.5px; color: var(--ghost);
    background: rgba(0,200,150,0.04); border: 1px solid var(--border); border-radius: 4px;
    padding: 3px 9px; letter-spacing: 1px; text-transform: uppercase;
  }

  .chart-wrap {
    background: var(--glass); border: 1px solid var(--border); border-radius: var(--rl);
    padding: 1.4rem 1.4rem 0.8rem; backdrop-filter: blur(12px);
    transition: border-color 0.3s; animation: kpiReveal 0.7s ease both;
    position: relative; overflow: hidden;
  }
  .chart-wrap::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,200,150,0.25), transparent);
  }
  .chart-wrap:hover { border-color: rgba(0,200,150,0.18); }

  .stTabs [data-baseweb="tab-list"] {
    background: rgba(5,13,10,0.95) !important; border-radius: 14px !important;
    padding: 5px !important; gap: 3px !important;
    border: 1px solid var(--border) !important; backdrop-filter: blur(20px) !important;
  }
  .stTabs [data-baseweb="tab"] {
    background: transparent !important; border-radius: 10px !important;
    color: var(--muted) !important; font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important; font-size: 13px !important; padding: 10px 22px !important;
    border: 1px solid transparent !important;
    transition: all 0.25s cubic-bezier(0.34,1.56,0.64,1) !important; letter-spacing: 0.02em !important;
  }
  .stTabs [data-baseweb="tab"]:hover { color: var(--sage) !important; background: rgba(0,200,150,0.04) !important; }
  .stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(0,200,150,0.12), rgba(0,200,150,0.06)) !important;
    border-color: rgba(0,200,150,0.25) !important; color: var(--jade) !important;
    box-shadow: 0 2px 16px rgba(0,200,150,0.10) !important;
  }
  .stTabs [data-baseweb="tab-highlight"] { display: none !important; }
  .stTabs [data-baseweb="tab-border"]    { display: none !important; }

  .al-bon {
    background: rgba(0,200,150,0.07); border: 1px solid rgba(0,200,150,0.22);
    border-left: 3px solid var(--jade); padding: 12px 16px;
    border-radius: 0 var(--r) var(--r) 0; color: var(--jade);
    font-family: 'Nunito', sans-serif; font-weight: 600; font-size: 0.87rem;
  }
  .al-moyen {
    background: rgba(245,166,35,0.07); border: 1px solid rgba(245,166,35,0.22);
    border-left: 3px solid var(--amber); padding: 12px 16px;
    border-radius: 0 var(--r) var(--r) 0; color: var(--amber);
    font-family: 'Nunito', sans-serif; font-weight: 600; font-size: 0.87rem;
  }
  .al-bad {
    background: rgba(232,53,74,0.07); border: 1px solid rgba(232,53,74,0.22);
    border-left: 3px solid var(--crimson); padding: 12px 16px;
    border-radius: 0 var(--r) var(--r) 0; color: var(--crimson);
    font-family: 'Nunito', sans-serif; font-weight: 600; font-size: 0.87rem;
  }

  .legend-wrap { display: flex; gap: 10px; flex-wrap: wrap; margin: 1rem 0 0; }
  .leg {
    display: inline-flex; align-items: center; gap: 8px;
    background: var(--glass); border: 1px solid var(--border); border-radius: 20px;
    padding: 5px 13px; font-size: 11.5px; color: var(--muted);
    font-family: 'Nunito', sans-serif; transition: border-color 0.2s;
  }
  .leg:hover { border-color: rgba(0,200,150,0.20); }
  .leg-dot { width: 7px; height: 7px; border-radius: 50%; }

  .streamlit-expanderHeader {
    background: var(--glass) !important; border: 1px solid var(--border) !important;
    border-radius: var(--r) !important; color: var(--text) !important;
    font-family: 'Syne', sans-serif !important; font-size: 13px !important;
    backdrop-filter: blur(10px); transition: border-color 0.2s !important;
  }
  .streamlit-expanderHeader:hover { border-color: rgba(0,200,150,0.20) !important; }
  .streamlit-expanderContent {
    background: rgba(5,13,10,0.92) !important; border: 1px solid var(--border) !important;
    border-top: none !important; border-radius: 0 0 var(--r) var(--r) !important;
  }

  [data-testid="metric-container"] {
    background: var(--glass) !important; border: 1px solid var(--border) !important;
    border-radius: var(--r) !important; padding: 1rem 1.2rem !important;
    backdrop-filter: blur(10px); transition: border-color 0.2s !important;
  }
  [data-testid="metric-container"]:hover { border-color: rgba(0,200,150,0.18) !important; }
  [data-testid="metric-container"] label {
    color: var(--muted) !important; font-size: 10px !important;
    font-family: 'Space Mono', monospace !important; letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
  }
  [data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: var(--jade) !important; font-family: 'Fraunces', serif !important; font-size: 1.8rem !important;
  }

  .stSelectbox > div > div,
  .stMultiSelect > div > div {
    background: rgba(12,28,22,0.9) !important;
    border-color: rgba(0,200,150,0.22) !important;
    color: var(--text) !important; border-radius: var(--r) !important;
    font-family: 'Nunito', sans-serif !important; font-size: 13px !important;
    transition: border-color 0.2s !important;
  }
  .stSelectbox > div > div:hover,
  .stMultiSelect > div > div:hover { border-color: rgba(0,200,150,0.40) !important; }
  .stSelectbox [data-baseweb="select"] svg,
  .stMultiSelect [data-baseweb="select"] svg { color: var(--jade) !important; }
  [data-baseweb="tag"] {
    background: rgba(0,200,150,0.15) !important;
    border: 1px solid rgba(0,200,150,0.28) !important;
    border-radius: 6px !important;
  }
  [data-baseweb="tag"] span { color: var(--jade) !important; font-family: 'Space Mono', monospace !important; font-size: 10px !important; }
  [data-baseweb="tag"] button svg { fill: var(--jade) !important; }
  [data-baseweb="menu"] {
    background: rgba(8,20,16,0.98) !important;
    border: 1px solid rgba(0,200,150,0.20) !important;
    border-radius: var(--r) !important;
    backdrop-filter: blur(16px) !important;
  }
  [data-baseweb="menu"] li {
    color: var(--light) !important;
    font-family: 'Nunito', sans-serif !important; font-size: 13px !important;
  }
  [data-baseweb="menu"] li:hover { background: rgba(0,200,150,0.08) !important; }
  .stSelectbox label, .stMultiSelect label {
    font-family: 'Space Mono', monospace !important;
    font-size: 8px !important; letter-spacing: 2.5px !important;
    text-transform: uppercase !important; color: var(--ghost) !important;
  }

  .stSlider [data-baseweb="slider"] .bar { background: var(--jade) !important; }
  .stSlider [data-testid="stTickBarMin"],
  .stSlider [data-testid="stTickBarMax"] {
    font-family: 'Space Mono', monospace !important; font-size: 10px !important; color: var(--ghost) !important;
  }

  .stButton > button {
    background: linear-gradient(135deg, var(--fern) 0%, var(--jade) 100%) !important;
    color: var(--night) !important; border: none !important; border-radius: 12px !important;
    font-family: 'Syne', sans-serif !important; font-weight: 700 !important; font-size: 14px !important;
    padding: 0.75rem 2.2rem !important; letter-spacing: 0.04em !important;
    box-shadow: 0 4px 24px rgba(0,200,150,0.22), inset 0 1px 0 rgba(255,255,255,0.15) !important;
    transition: all 0.3s cubic-bezier(0.34,1.56,0.64,1) !important;
  }
  .stButton > button:hover {
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: 0 10px 36px rgba(0,200,150,0.38), inset 0 1px 0 rgba(255,255,255,0.2) !important;
  }

  .pred-card {
    background: var(--glass); border: 1px solid var(--border); border-radius: var(--rl);
    padding: 2.4rem; text-align: center; backdrop-filter: blur(14px);
    position: relative; overflow: hidden; animation: kpiReveal 0.5s ease both;
  }
  .pred-city {
    font-family: 'Space Mono', monospace; font-size: 9px; letter-spacing: 3px;
    text-transform: uppercase; color: var(--ghost); margin-bottom: 0.8rem;
  }
  .pred-num {
    font-family: 'Fraunces', serif; font-size: 5.5rem; font-weight: 700;
    line-height: 1; margin: 0.2rem 0; letter-spacing: -2px;
  }
  .pred-unit {
    font-family: 'Space Mono', monospace; font-size: 11px; color: var(--ghost);
    letter-spacing: 2px; margin-bottom: 1.3rem;
  }
  .pred-meta {
    font-family: 'Space Mono', monospace; font-size: 9px; letter-spacing: 1.5px;
    color: var(--ghost); margin-top: 1.2rem; line-height: 2;
  }

  .stat-banner { display: flex; gap: 1rem; margin-bottom: 1.5rem; }
  .stat-b {
    flex: 1; border-radius: var(--rl); padding: 1.3rem 1.5rem; text-align: center;
    border: 1px solid; backdrop-filter: blur(10px); transition: transform 0.25s;
  }
  .stat-b:hover { transform: translateY(-3px); }
  .stat-b-val { font-family: 'Fraunces', serif; font-size: 2.8rem; font-weight: 700; line-height: 1; margin-bottom: 4px; }
  .stat-b-label { font-family: 'Space Mono', monospace; font-size: 8px; text-transform: uppercase; letter-spacing: 2px; color: var(--muted); }

  [data-testid="stForm"] {
    background: var(--glass); border: 1px solid var(--border); border-radius: var(--rxl);
    padding: 1.8rem !important; backdrop-filter: blur(14px);
  }
  [data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, var(--fern) 0%, var(--jade) 100%) !important;
    color: var(--night) !important; font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important; font-size: 15px !important; letter-spacing: 0.05em !important;
    padding: 0.85rem 2rem !important; border-radius: 14px !important;
    box-shadow: 0 6px 30px rgba(0,200,150,0.25) !important;
    transition: all 0.3s cubic-bezier(0.34,1.56,0.64,1) !important;
  }
  [data-testid="stFormSubmitButton"] > button:hover {
    transform: translateY(-3px) !important; box-shadow: 0 12px 40px rgba(0,200,150,0.38) !important;
  }
  .cond-box {
    background: rgba(12,28,22,0.85); border: 1px solid var(--border);
    border-radius: var(--r); padding: 12px 16px; backdrop-filter: blur(8px);
  }
  .cond-item {
    display: flex; align-items: center; gap: 10px; padding: 8px 0;
    border-bottom: 1px solid rgba(0,200,150,0.05); font-size: 12.5px;
    color: var(--light); font-family: 'Nunito', sans-serif;
  }
  .cond-item:last-child { border: none; padding-bottom: 0; }
  .cond-led { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; }
  .loc-box {
    background: rgba(12,28,22,0.80); border: 1px solid var(--border); border-radius: var(--r);
    padding: 11px 14px; font-size: 12px; color: var(--muted); margin: 8px 0;
    backdrop-filter: blur(8px); transition: border-color 0.2s;
  }
  .loc-box:hover { border-color: rgba(0,200,150,0.18); }
  .loc-label { font-family: 'Space Mono', monospace; font-size: 9px; letter-spacing: 1.5px; color: var(--ghost); text-transform: uppercase; margin-bottom: 3px; }
  .loc-val   { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 13.5px; color: var(--light); margin-bottom: 2px; }
  .loc-coords { font-family: 'Space Mono', monospace; font-size: 9.5px; color: var(--ghost); }

  .stInfo    { background: rgba(56,189,248,0.06) !important; border-color: rgba(56,189,248,0.18) !important; color: #93c5fd !important; border-radius: var(--r) !important; }
  .stSuccess { background: rgba(0,200,150,0.06)  !important; border-color: rgba(0,200,150,0.18)  !important; color: var(--mint) !important; border-radius: var(--r) !important; }
  .stWarning { background: rgba(245,166,35,0.06) !important; border-color: rgba(245,166,35,0.18) !important; color: var(--gold) !important; border-radius: var(--r) !important; }
  .stError   { background: rgba(232,53,74,0.06)  !important; border-color: rgba(232,53,74,0.18)  !important; color: #fca5a5 !important; border-radius: var(--r) !important; }

  .footer {
    display: flex; justify-content: space-between; align-items: center;
    flex-wrap: wrap; gap: 12px; padding: 1.2rem 0 0.6rem; margin-top: 1rem;
    border-top: 1px solid var(--border);
  }
  .foot-brand { font-family: 'Fraunces', serif; font-size: 1rem; font-style: italic; font-weight: 300; color: var(--muted); }
  .foot-brand b { color: var(--jade); font-style: normal; font-weight: 700; }
  .foot-meta { font-family: 'Space Mono', monospace; font-size: 9px; color: var(--ghost); letter-spacing: 1.5px; text-transform: uppercase; }

  .seuils {
    background: var(--glass); border: 1px solid var(--border); border-radius: var(--rl);
    padding: 1.3rem 1.5rem; margin-top: 1.5rem; backdrop-filter: blur(12px);
  }
  .seuils-head {
    font-family: 'Space Mono', monospace; font-size: 8.5px; text-transform: uppercase;
    letter-spacing: 2.5px; color: var(--ghost); margin-bottom: 1rem;
  }
  .seuils-row { display: flex; gap: 1rem; flex-wrap: wrap; }
  .seuil {
    flex: 1; min-width: 90px; border-radius: var(--r); padding: 12px;
    text-align: center; border: 1px solid; transition: transform 0.2s;
  }
  .seuil:hover { transform: translateY(-2px); }
  .seuil-v { font-family: 'Fraunces', serif; font-size: 1.5rem; font-weight: 700; line-height: 1; margin-bottom: 4px; }
  .seuil-l { font-family: 'Space Mono', monospace; font-size: 8px; letter-spacing: 1px; color: var(--muted); }

  ::-webkit-scrollbar       { width: 4px; height: 4px; }
  ::-webkit-scrollbar-track { background: var(--night); }
  ::-webkit-scrollbar-thumb { background: var(--fern); border-radius: 2px; }
  ::-webkit-scrollbar-thumb:hover { background: var(--jade); }

  hr { border-color: var(--border) !important; margin: 1.5rem 0 !important; }
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
#  THÈME PLOTLY
# ════════════════════════════════════════════════════════════════════════════════
PL = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Nunito', color='#5a8a78', size=11.5),
    title_font=dict(family='Fraunces', color='#c2dfd5', size=16),
    xaxis=dict(
        gridcolor='rgba(0,200,150,0.06)',
        linecolor='rgba(0,200,150,0.08)',
        tickcolor='rgba(0,200,150,0.08)',
        zerolinecolor='rgba(0,200,150,0.06)',
        tickfont=dict(family='Space Mono', size=10, color='#5a8a78'),
    ),
    yaxis=dict(
        gridcolor='rgba(0,200,150,0.06)',
        linecolor='rgba(0,200,150,0.08)',
        tickcolor='rgba(0,200,150,0.08)',
        zerolinecolor='rgba(0,200,150,0.06)',
        tickfont=dict(family='Space Mono', size=10, color='#5a8a78'),
    ),
    legend=dict(
        bgcolor='rgba(12,28,22,0.85)',
        bordercolor='rgba(0,200,150,0.12)',
        borderwidth=1,
        font=dict(family='Nunito', size=11, color='#c2dfd5'),
    ),
    margin=dict(l=20, r=20, t=52, b=20),
    coloraxis_colorbar=dict(
        bgcolor='rgba(12,28,22,0.85)',
        outlinecolor='rgba(0,200,150,0.12)',
        tickcolor='#5a8a78',
        tickfont=dict(family='Space Mono', size=9, color='#5a8a78'),
        title_font=dict(family='Nunito', size=11, color='#c2dfd5'),
    ),
)

COLOR_SCALE = [[0, "#00c896"], [0.45, "#f5a623"], [1, "#e8354a"]]


# ════════════════════════════════════════════════════════════════════════════════
#  FONCTIONS UTILITAIRES
# ════════════════════════════════════════════════════════════════════════════════
def get_alerte(v):
    if v < 15:
        return "✦ Bon", "al-bon", "Qualité de l'air satisfaisante — aucun risque sanitaire détecté."
    elif v < 25:
        return "◈ Modéré", "al-moyen", "Qualité acceptable — risque modéré pour les personnes sensibles."
    else:
        return "⚠ Mauvais", "al-bad", "Qualité dégradée — réduire les activités extérieures prolongées."

def get_alerte_short(v):
    if v < 15:   return "Bon",     "bon"
    elif v < 25: return "Modéré",  "moyen"
    else:        return "Mauvais", "bad"

def alert_color(v):
    if v < 15:   return "#00c896"
    elif v < 25: return "#f5a623"
    else:        return "#e8354a"

def fill_na_features(X):
    X = X.copy()
    for col in X.columns:
        is_cat = isinstance(X[col].dtype, pd.CategoricalDtype)
        if is_cat:
            if X[col].isnull().values.any():
                m = X[col].mode()
                if len(m) > 0:
                    X[col] = X[col].fillna(m.iloc[0])
        else:
            if X[col].isnull().values.any():
                X[col] = X[col].fillna(X[col].median())
    return X

def sec(icon, text, tag=""):
    tag_html = f'<span class="sec-tag">{tag}</span>' if tag else ""
    st.markdown(f"""
    <div class="sec-head">
      <div class="sec-icon">{icon}</div>
      <span class="sec-text">{text}</span>
      <div class="sec-line"></div>
      {tag_html}
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
#  CHARGEMENT DES DONNÉES ET DU MODÈLE
# ════════════════════════════════════════════════════════════════════════════════
@st.cache_data
def load_data():
    df = pd.read_excel("data/Dataset_complet_Meteo.xlsx")
    if not pd.api.types.is_datetime64_any_dtype(df['time']):
        df['time'] = pd.to_datetime(df['time'])

    num_cols = [
        'temperature_2m_max', 'temperature_2m_min', 'temperature_2m_mean',
        'apparent_temperature_mean', 'precipitation_sum', 'rain_sum',
        'wind_speed_10m_max', 'wind_gusts_10m_max',
        'shortwave_radiation_sum', 'et0_fao_evapotranspiration',
        'sunshine_duration', 'latitude', 'longitude'
    ]
    for col in num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    df['month']          = df['time'].dt.month
    df['year']           = df['time'].dt.year
    df['quarter']        = df['time'].dt.quarter
    df['day_of_year']    = df['time'].dt.dayofyear
    df['month_sin']      = np.sin(2 * np.pi * df['month'] / 12)
    df['month_cos']      = np.cos(2 * np.pi * df['month'] / 12)
    df['is_dry_season']  = df['month'].isin([11, 12, 1, 2, 3]).astype(int)
    df['temp_amplitude'] = df['temperature_2m_max'] - df['temperature_2m_min']

    daylight_col = 'daylight_duration' if 'daylight_duration' in df.columns else None
    if daylight_col:
        df['sunshine_ratio'] = df['sunshine_duration'] / (df[daylight_col] + 1e-6)
    else:
        df['sunshine_ratio'] = df['sunshine_duration'] / 12.0

    df['is_no_wind'] = (df['wind_speed_10m_max'] < 5).astype(int)
    df['is_no_rain'] = (df['precipitation_sum'] < 0.1).astype(int)

    df = df.sort_values(['city', 'time']).reset_index(drop=True)
    for lag in [1, 7]:
        df[f'temp_lag{lag}'] = df.groupby('city')['temperature_2m_mean'].shift(lag)
    df['wind_lag1']  = df.groupby('city')['wind_speed_10m_max'].shift(1)
    df['temp_roll7'] = df.groupby('city')['temperature_2m_mean'].transform(
                           lambda x: x.shift(1).rolling(7).mean())

    df['city']   = df['city'].astype('category')
    df['region'] = df['region'].astype('category')

    df['pm25_proxy'] = (
        0.35 * df['temperature_2m_mean'].fillna(df['temperature_2m_mean'].mean())
        + 0.25 * df['shortwave_radiation_sum'].fillna(0)
        + 0.20 * df['et0_fao_evapotranspiration'].fillna(0)
        + 8.0  * df['is_no_wind']
        + 5.0  * df['is_no_rain']
        + 4.0  * df['is_dry_season']
    ).clip(lower=0)

    return df


@st.cache_resource
def load_model():
    return joblib.load("models/lightgbm_pm25.pkl")


FEATURES_LGB = [
    'temperature_2m_mean', 'temperature_2m_max', 'temperature_2m_min',
    'precipitation_sum', 'wind_speed_10m_max', 'wind_gusts_10m_max',
    'shortwave_radiation_sum', 'et0_fao_evapotranspiration', 'sunshine_ratio',
    'temp_amplitude', 'is_no_wind', 'is_no_rain', 'is_dry_season',
    'month_sin', 'month_cos', 'day_of_year',
    'temp_lag1', 'temp_lag7', 'wind_lag1', 'temp_roll7',
    'latitude', 'longitude', 'city', 'region'
]

df    = load_data()
model = load_model()

cols_to_keep = list(set(FEATURES_LGB + ['city', 'region', 'time', 'month', 'year',
                                         'temperature_2m_mean', 'precipitation_sum',
                                         'wind_speed_10m_max', 'latitude', 'longitude',
                                         'pm25_proxy']))
df_model = df[cols_to_keep].copy().reset_index(drop=True)
X_all    = fill_na_features(df_model[FEATURES_LGB].copy())

try:
    df_model['pm25_pred'] = model.predict(X_all[FEATURES_LGB])
except Exception as e:
    st.error(f"Erreur prédiction globale : {e}")
    df_model['pm25_pred'] = df_model['pm25_proxy']


# ════════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ════════════════════════════════════════════════════════════════════════════════
mois_noms = ["Janvier","Février","Mars","Avril","Mai","Juin",
             "Juillet","Août","Septembre","Octobre","Novembre","Décembre"]

with st.sidebar:
    st.markdown("""
    <div class="logo-block">
      <div class="indabax-logo-wrap">
        <div class="indabax-tree-badge">
          <svg width="28" height="28" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="12.5" y="16" width="3" height="8" rx="1.5" fill="#2a8a64"/>
            <path d="M12.5 23 Q10 25 8 24" stroke="#2a8a64" stroke-width="1.2" stroke-linecap="round" fill="none"/>
            <path d="M15.5 23 Q17 25.5 19.5 24.5" stroke="#2a8a64" stroke-width="1.2" stroke-linecap="round" fill="none"/>
            <path d="M14 24 Q14 26 14 28" stroke="#2a8a64" stroke-width="1.2" stroke-linecap="round" fill="none"/>
            <ellipse cx="14" cy="10" rx="8" ry="7" fill="#00c896" opacity="0.85"/>
            <ellipse cx="8" cy="12" rx="5" ry="4" fill="#2a8a64" opacity="0.75"/>
            <ellipse cx="20" cy="11" rx="5" ry="4.5" fill="#2a8a64" opacity="0.75"/>
            <ellipse cx="14" cy="6" rx="5" ry="4" fill="#4dffc3" opacity="0.55"/>
          </svg>
        </div>
        <div class="indabax-wordmark">
          <div class="indabax-deep">Deep Learning</div>
          <div class="indabax-main">
            <span class="ix">IndabaX</span><span class="dot">·</span><span class="cam">Cam</span>
          </div>
        </div>
      </div>
      <div class="indabax-sub">Hackathon · IA &amp; Résilience Climatique</div>
      <div class="indabax-year-badge">
        <span style="width:5px;height:5px;border-radius:50%;background:#a8e63d;display:inline-block;"></span>
        Cameroon 2026
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="active-pill">
      <span class="active-dot"></span>
      MODÈLE ACTIF
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-label">Période</div>', unsafe_allow_html=True)
    annee_sel = st.selectbox(
        "Année",
        sorted(df['year'].unique(), reverse=True),
        label_visibility="collapsed"
    )

    st.markdown('<div class="sb-label">Mois</div>', unsafe_allow_html=True)
    mois_sel = st.multiselect(
        "Mois",
        options=list(range(1, 13)),
        default=list(range(1, 13)),
        format_func=lambda x: mois_noms[x - 1],
        label_visibility="collapsed",
    )
    if not mois_sel:
        mois_sel = list(range(1, 13))

    st.markdown('<div class="sb-label">Régions</div>', unsafe_allow_html=True)
    all_regions = sorted(df['region'].astype(str).unique())
    region_sel = st.multiselect(
        "Régions",
        options=all_regions,
        default=all_regions,
        label_visibility="collapsed",
    )
    if not region_sel:
        region_sel = all_regions

    st.markdown("---")

    st.markdown('<div class="sb-label">Performance modèle</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="model-panel">
      <div class="mp-row"><span class="mp-label">Algorithme</span><span class="mp-val">LightGBM</span></div>
      <div class="mp-row"><span class="mp-label">R² Score</span><span class="mp-val">0.9990</span></div>
      <div class="mp-row"><span class="mp-label">MAE</span><span class="mp-val">0.0595</span></div>
      <div class="mp-row"><span class="mp-label">Villes</span><span class="mp-val">42 · 10 rég.</span></div>
      <div class="mp-row"><span class="mp-label">Observations</span><span class="mp-val">87 240</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="font-family:'Space Mono',monospace; font-size:8px; color:#2a4a3a;
                text-align:center; line-height:2.2; letter-spacing:1px;">
      OPEN-METEO · 2020–2025<br>
      IA &amp; RÉSILIENCE CLIMATIQUE
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
#  FILTRAGE
# ════════════════════════════════════════════════════════════════════════════════
mask = (
    (df_model['year'] == annee_sel) &
    (df_model['month'].isin(mois_sel)) &
    (df_model['region'].astype(str).isin(region_sel))
)
df_f = df_model[mask].copy()

pm25_moy = df_f['pm25_pred'].mean() if not df_f.empty else 0
pm25_max = df_f['pm25_pred'].max()  if not df_f.empty else 0
n_villes = df_f['city'].nunique()
label_al, css_al, msg_al = get_alerte(pm25_moy)
col_al = alert_color(pm25_moy)


# ════════════════════════════════════════════════════════════════════════════════
#  HERO HEADER
# ════════════════════════════════════════════════════════════════════════════════
mois_label = (
    " · ".join([mois_noms[m-1][:3] for m in sorted(mois_sel)])
    if len(mois_sel) <= 3
    else f"{len(mois_sel)} mois"
)

st.markdown(f"""
<div class="hero">
  <div class="hero-scan"></div>
  <div class="hero-badge">
    <div class="hero-badge-icon">🌍</div>
    INDABAX CAMEROON · HACKATHON 2026
  </div>
  <h1 class="hero-title">
    Qualité de l'<em>Air</em><br>au Cameroun
  </h1>
  <p class="hero-sub">
    Surveillance et prédiction PM2.5 via LightGBM · Couverture nationale ·
    42 villes · 10 régions administratives · 2020–2025
  </p>
  <div class="hero-chips">
    <div class="hero-chip active">
      <span class="chip-dot" style="background:#00c896"></span>
      LightGBM · R² 0.9990
    </div>
    <div class="hero-chip active">
      <span class="chip-dot" style="background:#a8e63d"></span>
      MAE · 0.0595 μg/m³
    </div>
    <div class="hero-chip">
      <span class="chip-dot" style="background:#38bdf8"></span>
      {annee_sel} · {mois_label}
    </div>
    <div class="hero-chip">
      <span class="chip-dot" style="background:#f5a623"></span>
      {n_villes} villes actives
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ── KPI Cards ─────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="kpi jade">
      <span class="kpi-icon">🌫️</span>
      <div class="kpi-label">PM2.5 Moyen Prédit</div>
      <div class="kpi-val jade-c" style="color:{col_al}">{pm25_moy:.2f}</div>
      <div class="kpi-hint">μg/m³ · période filtrée</div>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="kpi amber">
      <span class="kpi-icon">📈</span>
      <div class="kpi-label">PM2.5 Maximum</div>
      <div class="kpi-val amber-c">{pm25_max:.2f}</div>
      <div class="kpi-hint">μg/m³ · valeur pic</div>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="kpi sky">
      <span class="kpi-icon">🗺️</span>
      <div class="kpi-label">Villes Couvertes</div>
      <div class="kpi-val sky-c">{n_villes}<span style="font-size:1.1rem;color:var(--ghost);font-family:Nunito">/42</span></div>
      <div class="kpi-hint">sélection active</div>
    </div>""", unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="kpi lime">
      <span class="kpi-icon">🚦</span>
      <div class="kpi-label">Indice Qualité</div>
      <div class="kpi-val" style="font-size:1.5rem;color:{col_al};padding-top:0.6rem;font-family:Fraunces,serif">{label_al}</div>
      <div class="kpi-hint">{annee_sel} · filtres actifs</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
#  ONGLETS
# ════════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4 = st.tabs([
    "  🗺  Carte de chaleur  ",
    "  📊  Analyse climatique  ",
    "  🚦  Alertes par ville  ",
    "  🔮  Simulateur  ",
])


# ────────────────────────────────────────────────────────────────────────────────
#  ONGLET 1 — CARTE
# ────────────────────────────────────────────────────────────────────────────────
with tab1:
    sec("🗺", "Distribution spatiale — PM2.5 moyen par ville", "CARTE CHOROPLÈTHE")

    if not df_f.empty:
        left_col, right_col = st.columns([2.5, 1])

        city_map = df_f.groupby('city', observed=True).agg(
            pm25_moy  = ('pm25_pred', 'mean'),
            pm25_max  = ('pm25_pred', 'max'),
            latitude  = ('latitude',  'first'),
            longitude = ('longitude', 'first'),
            region    = ('region',    'first'),
            n_obs     = ('pm25_pred', 'count'),
        ).reset_index().round(3)
        city_map['alerte'] = city_map['pm25_moy'].apply(
            lambda v: "Bon" if v < 15 else ("Modéré" if v < 25 else "Mauvais"))

        with left_col:
            try:
                fig_map = px.scatter_map(
                    city_map,
                    lat='latitude', lon='longitude',
                    color='pm25_moy', size='pm25_moy', size_max=44,
                    map_style="carto-darkmatter",
                    zoom=5, center={"lat": 5.5, "lon": 12.3},
                    hover_name='city',
                    hover_data={'pm25_moy': ':.2f', 'pm25_max': ':.2f', 'region': True,
                                'latitude': False, 'longitude': False, 'n_obs': True},
                    color_continuous_scale=COLOR_SCALE,
                    labels={'pm25_moy': 'PM2.5 moy.', 'pm25_max': 'PM2.5 max', 'n_obs': 'Obs.'},
                )
                fig_map.update_layout(**PL, height=570)
            except AttributeError:
                fig_map = px.scatter_mapbox(
                    city_map,
                    lat='latitude', lon='longitude',
                    color='pm25_moy', size='pm25_moy', size_max=44,
                    mapbox_style="carto-darkmatter",
                    zoom=5, center={"lat": 5.5, "lon": 12.3},
                    hover_name='city',
                    hover_data={'pm25_moy': ':.2f', 'pm25_max': ':.2f', 'region': True,
                                'latitude': False, 'longitude': False, 'n_obs': True},
                    color_continuous_scale=COLOR_SCALE,
                    labels={'pm25_moy': 'PM2.5 moy.', 'pm25_max': 'PM2.5 max', 'n_obs': 'Obs.'},
                )
                fig_map.update_layout(**PL, height=570,
                                      mapbox=dict(style="carto-darkmatter"))

            fig_map.update_coloraxes(colorbar_title_text="PM2.5<br>μg/m³")
            st.plotly_chart(fig_map, use_container_width=True)

        with right_col:
            sec("🏆", "Top 10 Villes", "PM2.5 ↓")
            top10 = city_map.nlargest(10, 'pm25_moy')[
                ['city', 'region', 'pm25_moy', 'alerte']].reset_index(drop=True)

            fig_bar = go.Figure()
            fig_bar.add_trace(go.Bar(
                x=top10['pm25_moy'], y=top10['city'],
                orientation='h',
                marker=dict(
                    color=[alert_color(v) for v in top10['pm25_moy']],
                    opacity=0.82, line=dict(width=0),
                ),
                text=[f"{v:.1f}" for v in top10['pm25_moy']],
                textposition='outside',
                textfont=dict(size=10, color='#5a8a78', family='Space Mono'),
                hovertemplate='<b>%{y}</b><br>PM2.5 : %{x:.2f} μg/m³<extra></extra>',
            ))
            layout_bar = {**PL}
            layout_bar['yaxis'] = dict(
                autorange='reversed',
                gridcolor='rgba(0,200,150,0.06)',
                linecolor='rgba(0,200,150,0.08)',
                tickfont=dict(family='Nunito', size=11, color='#c2dfd5')
            )
            fig_bar.update_layout(**layout_bar, height=530,
                                   xaxis_title="PM2.5 μg/m³", showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("""
        <div class="legend-wrap">
          <div class="leg"><span class="leg-dot" style="background:#00c896"></span>Bon · PM2.5 &lt; 15 μg/m³</div>
          <div class="leg"><span class="leg-dot" style="background:#f5a623"></span>Modéré · 15–25 μg/m³</div>
          <div class="leg"><span class="leg-dot" style="background:#e8354a"></span>Mauvais · &gt; 25 μg/m³</div>
          <div class="leg" style="margin-left:auto">Open-Meteo · LightGBM · IndabaX 2026</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("⚠ Aucune donnée disponible pour les filtres sélectionnés.")


# ────────────────────────────────────────────────────────────────────────────────
#  ONGLET 2 — ANALYSE
# ────────────────────────────────────────────────────────────────────────────────
with tab2:
    sec("📊", "Corrélations climatiques & évolution temporelle", "ANALYSE")

    if not df_f.empty:
        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
            fig_scat = px.scatter(
                df_f, x='temperature_2m_mean', y='pm25_pred',
                color='pm25_pred', color_continuous_scale=COLOR_SCALE, opacity=0.5,
                labels={'temperature_2m_mean': 'Température moyenne (°C)', 'pm25_pred': 'PM2.5 (μg/m³)'},
                title="Température vs PM2.5",
            )
            fig_scat.update_traces(marker=dict(size=4))
            fig_scat.update_layout(**PL, height=380)
            fig_scat.update_coloraxes(showscale=False)
            st.plotly_chart(fig_scat, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_b:
            st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
            df_ts = df_f.groupby('time').agg(
                pm25_pred  = ('pm25_pred',  'mean'),
                pm25_proxy = ('pm25_proxy', 'mean')
            ).reset_index()
            fig_line = go.Figure()
            fig_line.add_trace(go.Scatter(
                x=df_ts['time'], y=df_ts['pm25_pred'],
                name="Prédit (LightGBM)",
                line=dict(color='#00c896', width=2.5),
                fill='tozeroy', fillcolor='rgba(0,200,150,0.06)',
            ))
            fig_line.add_trace(go.Scatter(
                x=df_ts['time'], y=df_ts['pm25_proxy'],
                name="Proxy (Cible)",
                line=dict(color='#a8e63d', width=1.5, dash='dot'),
            ))
            ll = {**PL}
            ll['legend'] = dict(x=0.01, y=0.99,
                bgcolor='rgba(12,28,22,0.85)', bordercolor='rgba(0,200,150,0.12)', borderwidth=1)
            fig_line.update_layout(**ll, height=380, title="Prédit vs Cible — Évolution temporelle")
            st.plotly_chart(fig_line, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_c, col_d = st.columns(2)

        with col_c:
            sec("📉", "Distribution PM2.5")
            st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
            fig_hist = go.Figure()
            fig_hist.add_trace(go.Histogram(
                x=df_f['pm25_pred'], nbinsx=40,
                marker=dict(
                    color=df_f['pm25_pred'].apply(alert_color).tolist(),
                    opacity=0.78, line=dict(width=0),
                ),
            ))
            fig_hist.update_layout(**PL, height=300, title="Distribution PM2.5",
                                    xaxis_title="PM2.5 (μg/m³)", yaxis_title="Fréquence", showlegend=False)
            fig_hist.add_vline(x=15, line_dash="dash", line_color="#f5a623",
                               annotation_text="Modéré",
                               annotation_font=dict(color="#f5a623", family="Space Mono", size=9))
            fig_hist.add_vline(x=25, line_dash="dash", line_color="#e8354a",
                               annotation_text="Mauvais",
                               annotation_font=dict(color="#e8354a", family="Space Mono", size=9))
            st.plotly_chart(fig_hist, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_d:
            sec("📆", "Saisonnalité mensuelle")
            st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
            df_month = df_f.groupby('month')['pm25_pred'].mean().reset_index()
            df_month['mois_label'] = df_month['month'].apply(lambda x: mois_noms[x - 1][:3])
            fig_month = go.Figure()
            fig_month.add_trace(go.Bar(
                x=df_month['mois_label'], y=df_month['pm25_pred'],
                marker=dict(color=[alert_color(v) for v in df_month['pm25_pred']],
                            opacity=0.80, line=dict(width=0)),
                text=[f"{v:.1f}" for v in df_month['pm25_pred']],
                textposition='outside',
                textfont=dict(size=10, color='#5a8a78', family='Space Mono'),
                hovertemplate='<b>%{x}</b><br>PM2.5 : %{y:.2f} μg/m³<extra></extra>',
            ))
            fig_month.update_layout(**PL, height=300, title="PM2.5 moyen par mois", showlegend=False)
            st.plotly_chart(fig_month, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        sec("🔍", "PM2.5 vs Vent & Précipitations", "CORRÉLATIONS")
        col_e, col_f = st.columns(2)

        with col_e:
            st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
            sample_size = min(2000, len(df_f))
            fig_wind = px.scatter(
                df_f.sample(sample_size),
                x='wind_speed_10m_max', y='pm25_pred',
                color='pm25_pred', color_continuous_scale=COLOR_SCALE, opacity=0.48,
                labels={'wind_speed_10m_max': 'Vitesse vent (km/h)', 'pm25_pred': 'PM2.5 (μg/m³)'},
                title="Vent vs PM2.5",
            )
            fig_wind.update_traces(marker=dict(size=3))
            fig_wind.update_layout(**PL, height=280)
            fig_wind.update_coloraxes(showscale=False)
            st.plotly_chart(fig_wind, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_f:
            st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
            fig_rain = px.scatter(
                df_f.sample(sample_size),
                x='precipitation_sum', y='pm25_pred',
                color='pm25_pred', color_continuous_scale=COLOR_SCALE, opacity=0.48,
                labels={'precipitation_sum': 'Précipitations (mm)', 'pm25_pred': 'PM2.5 (μg/m³)'},
                title="Précipitations vs PM2.5",
            )
            fig_rain.update_traces(marker=dict(size=3))
            fig_rain.update_layout(**PL, height=280)
            fig_rain.update_coloraxes(showscale=False)
            st.plotly_chart(fig_rain, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.warning("⚠ Aucune donnée disponible pour les filtres sélectionnés.")


# ════════════════════════════════════════════════════════════════════════════════
#  ONGLET 3 — ALERTES PAR VILLE
#  FIX CRITIQUE : utilisation de st.columns() natif Streamlit pour chaque card
#  au lieu d'un seul bloc HTML monolithique avec des f-strings complexes.
#  Cela évite tout problème d'échappement HTML dans Streamlit.
# ════════════════════════════════════════════════════════════════════════════════
with tab3:
    sec("🚦", "Tableau de bord des alertes — toutes les villes", "TEMPS RÉEL")

    if not df_f.empty:
        city_alerts = df_f.groupby('city', observed=True).agg(
            pm25_moy = ('pm25_pred', 'mean'),
            pm25_max = ('pm25_pred', 'max'),
            pm25_min = ('pm25_pred', 'min'),
            region   = ('region',    'first'),
            n_obs    = ('pm25_pred', 'count'),
        ).reset_index().round(3)

        city_alerts = city_alerts[city_alerts['n_obs'] > 0].sort_values(
            'pm25_moy', ascending=False
        ).reset_index(drop=True)

        if city_alerts.empty:
            st.warning("⚠ Aucune ville avec données pour les filtres sélectionnés.")
        else:
            n_bon     = int((city_alerts['pm25_moy'] < 15).sum())
            n_modere  = int(((city_alerts['pm25_moy'] >= 15) & (city_alerts['pm25_moy'] < 25)).sum())
            n_mauvais = int((city_alerts['pm25_moy'] >= 25).sum())

            # ── Bannière stats ─────────────────────────────────────────────────
            st.markdown(f"""
            <div class="stat-banner">
              <div class="stat-b" style="background:rgba(0,200,150,0.06);border-color:rgba(0,200,150,0.18)">
                <div class="stat-b-val" style="color:#00c896">{n_bon}</div>
                <div class="stat-b-label">villes &middot; bonne qualité</div>
              </div>
              <div class="stat-b" style="background:rgba(245,166,35,0.06);border-color:rgba(245,166,35,0.18)">
                <div class="stat-b-val" style="color:#f5a623">{n_modere}</div>
                <div class="stat-b-label">villes &middot; alerte modérée</div>
              </div>
              <div class="stat-b" style="background:rgba(232,53,74,0.06);border-color:rgba(232,53,74,0.18)">
                <div class="stat-b-val" style="color:#e8354a">{n_mauvais}</div>
                <div class="stat-b-label">villes &middot; alerte rouge</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            # ── Cards des villes — 4 colonnes avec st.columns() ───────────────
            # On regroupe les villes par lots de 4 et on crée une ligne par lot.
            # Chaque card est rendue via st.markdown() DANS sa propre colonne,
            # ce qui évite les problèmes d'échappement du HTML monolithique.

            max_pm25_global = float(city_alerts['pm25_moy'].max())
            N_COLS = 4
            rows = [
                city_alerts.iloc[i:i + N_COLS]
                for i in range(0, len(city_alerts), N_COLS)
            ]

            for row_df in rows:
                cols = st.columns(N_COLS)
                for col_idx, (_, row) in enumerate(row_df.iterrows()):
                    v           = float(row['pm25_moy'])
                    v_max       = float(row['pm25_max'])
                    v_min       = float(row['pm25_min'])
                    n_obs_val   = int(row['n_obs'])
                    region_str  = str(row['region'])
                    city_str    = str(row['city'])
                    amplitude   = round(v_max - v_min, 1)

                    label_short, css_key = get_alerte_short(v)
                    color        = alert_color(v)
                    card_class   = f"c-{css_key}"
                    progress_pct = min(100.0, (v / max(max_pm25_global, 1.0)) * 100.0)

                    # Couleurs fixes par niveau (pas de f-string dans style inline)
                    if css_key == "bon":
                        top_grad    = "linear-gradient(90deg,#00c896,#4dffc3)"
                        top_border  = "rgba(0,200,150,0.25)"
                        badge_bg    = "rgba(0,200,150,0.12)"
                        badge_bc    = "rgba(0,200,150,0.22)"
                        badge_color = "#00c896"
                        glow_bg     = "rgba(0,200,150,0.07)"
                        hover_bc    = "rgba(0,200,150,0.28)"
                    elif css_key == "moyen":
                        top_grad    = "linear-gradient(90deg,#f5a623,#ffd166)"
                        top_border  = "rgba(245,166,35,0.25)"
                        badge_bg    = "rgba(245,166,35,0.12)"
                        badge_bc    = "rgba(245,166,35,0.22)"
                        badge_color = "#f5a623"
                        glow_bg     = "rgba(245,166,35,0.07)"
                        hover_bc    = "rgba(245,166,35,0.28)"
                    else:
                        top_grad    = "linear-gradient(90deg,#e8354a,#ff5e3a)"
                        top_border  = "rgba(232,53,74,0.25)"
                        badge_bg    = "rgba(232,53,74,0.12)"
                        badge_bc    = "rgba(232,53,74,0.22)"
                        badge_color = "#e8354a"
                        glow_bg     = "rgba(232,53,74,0.07)"
                        hover_bc    = "rgba(232,53,74,0.28)"

                    card_html = (
                        '<div style="'
                        'background:rgba(15,35,28,0.65);'
                        f'border:1px solid {top_border};'
                        'border-radius:16px;'
                        'padding:1.1rem 1rem 0.9rem;'
                        'position:relative;'
                        'overflow:hidden;'
                        'backdrop-filter:blur(12px);'
                        'margin-bottom:0.5rem;'
                        '">'
                        # Barre top colorée
                        f'<div style="position:absolute;top:0;left:0;right:0;height:2.5px;background:{top_grad};border-radius:16px 16px 0 0;"></div>'
                        # Glow bottom-right
                        f'<div style="position:absolute;bottom:-20px;right:-20px;width:80px;height:80px;border-radius:50%;background:radial-gradient(circle,{glow_bg},transparent 70%);"></div>'
                        # Header ville + badge
                        '<div style="display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:0.7rem;">'
                        f'<div style="font-family:Syne,sans-serif;font-weight:700;font-size:12.5px;color:#c2dfd5;letter-spacing:0.02em;line-height:1.2;flex:1;padding-right:6px;">{city_str}</div>'
                        f'<div style="font-family:Space Mono,monospace;font-size:7.5px;padding:3px 7px;border-radius:10px;white-space:nowrap;flex-shrink:0;background:{badge_bg};color:{badge_color};border:1px solid {badge_bc};">{label_short}</div>'
                        '</div>'
                        # Région
                        f'<div style="font-family:Space Mono,monospace;font-size:8px;letter-spacing:1.5px;color:#2a4a3a;text-transform:uppercase;margin-bottom:0.75rem;">{region_str}</div>'
                        # Valeur principale PM2.5
                        '<div style="display:flex;align-items:baseline;gap:5px;margin-bottom:0.7rem;">'
                        f'<div style="font-family:Fraunces,serif;font-weight:700;font-size:2.1rem;line-height:1;letter-spacing:-1px;color:{color};">{v:.1f}</div>'
                        '<div style="font-family:Space Mono,monospace;font-size:9px;color:#2a4a3a;letter-spacing:1px;">μg/m³</div>'
                        '</div>'
                        # Stats Min / Max
                        '<div style="display:grid;grid-template-columns:1fr 1fr;gap:5px;margin-bottom:0.7rem;">'
                        '<div style="background:rgba(0,200,150,0.04);border:1px solid rgba(0,200,150,0.08);border-radius:6px;padding:5px 7px;text-align:center;">'
                        f'<div style="font-family:Fraunces,serif;font-size:0.88rem;font-weight:700;line-height:1;color:#f5a623;">{v_max:.1f}</div>'
                        '<div style="font-family:Space Mono,monospace;font-size:7px;letter-spacing:1px;color:#2a4a3a;text-transform:uppercase;margin-top:2px;">Max</div>'
                        '</div>'
                        '<div style="background:rgba(0,200,150,0.04);border:1px solid rgba(0,200,150,0.08);border-radius:6px;padding:5px 7px;text-align:center;">'
                        f'<div style="font-family:Fraunces,serif;font-size:0.88rem;font-weight:700;line-height:1;color:#00c896;">{v_min:.1f}</div>'
                        '<div style="font-family:Space Mono,monospace;font-size:7px;letter-spacing:1px;color:#2a4a3a;text-transform:uppercase;margin-top:2px;">Min</div>'
                        '</div>'
                        '</div>'
                        # Barre de progression
                        '<div style="margin-top:0.5rem;">'
                        '<div style="display:flex;justify-content:space-between;font-family:Space Mono,monospace;font-size:7.5px;color:#2a4a3a;letter-spacing:1px;margin-bottom:4px;">'
                        '<span>Intensit&#233; relative</span>'
                        f'<span style="color:{color};">{progress_pct:.0f}%</span>'
                        '</div>'
                        '<div style="height:3px;background:rgba(0,200,150,0.08);border-radius:2px;overflow:hidden;">'
                        f'<div style="height:100%;width:{progress_pct:.1f}%;background:{color};border-radius:2px;"></div>'
                        '</div>'
                        '</div>'
                        # Observations
                        f'<div style="font-family:Space Mono,monospace;font-size:8px;color:#2a4a3a;letter-spacing:1px;margin-top:6px;text-align:right;">{n_obs_val} obs &middot; &Delta; {amplitude} &#956;g/m&#179;</div>'
                        '</div>'
                    )

                    with cols[col_idx]:
                        st.markdown(card_html, unsafe_allow_html=True)

            # Légende
            st.markdown("""
            <div class="legend-wrap" style="margin-top:1.2rem">
              <div class="leg"><span class="leg-dot" style="background:#00c896"></span>Bon &middot; PM2.5 &lt; 15 μg/m³</div>
              <div class="leg"><span class="leg-dot" style="background:#f5a623"></span>Modéré &middot; 15–25 μg/m³</div>
              <div class="leg"><span class="leg-dot" style="background:#e8354a"></span>Mauvais &middot; &gt; 25 μg/m³</div>
              <div class="leg" style="margin-left:auto;font-size:10px;font-family:'Space Mono',monospace;color:var(--ghost)">
                &Delta; = amplitude min–max &middot; obs = jours couverts
              </div>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.warning("⚠ Aucune donnée disponible pour les filtres sélectionnés.")


# ────────────────────────────────────────────────────────────────────────────────
#  ONGLET 4 — SIMULATEUR
# ────────────────────────────────────────────────────────────────────────────────
with tab4:
    sec("🔮", "Simulateur de prédiction PM2.5 en temps réel", "LIGHTGBM")

    st.markdown("""
    <p style="color:var(--muted); font-size:0.88rem; margin-bottom:1.5rem;
              font-family:'Nunito',sans-serif; font-weight:300; line-height:1.6;">
      Configurez les paramètres météorologiques pour obtenir une estimation instantanée
      via le modèle LightGBM entraîné sur 87 240 observations.
    </p>
    """, unsafe_allow_html=True)

    with st.form(key="prediction_form"):
        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown("##### 🏙 Localisation")
            city_input   = st.selectbox("Ville cible", sorted(df['city'].unique()))
            region_input = df[df['city'] == city_input]['region'].iloc[0]
            lat          = df[df['city'] == city_input]['latitude'].iloc[0]
            lon          = df[df['city'] == city_input]['longitude'].iloc[0]

            st.markdown(f"""
            <div class="loc-box">
              <div class="loc-label">Région</div>
              <div class="loc-val">{region_input}</div>
              <div class="loc-coords">{lat:.4f}°N · {lon:.4f}°E</div>
            </div>
            """, unsafe_allow_html=True)

            mois_input = st.selectbox("Mois de simulation", list(range(1, 13)),
                                       format_func=lambda x: mois_noms[x - 1])
            st.markdown("##### 🌡 Températures")
            temp_mean = st.slider("Température moyenne (°C)", 10.0, 45.0, 27.0, 0.5)
            temp_max  = st.slider("Température maximale (°C)", temp_mean, 52.0,
                                   min(temp_mean + 5, 52.0), 0.5)
            temp_min  = st.slider("Température minimale (°C)", 0.0, temp_mean,
                                   max(temp_mean - 5, 0.0), 0.5)

        with c2:
            st.markdown("##### 🌧 Précipitations & Vent")
            pluie   = st.slider("Précipitations (mm)", 0.0, 150.0, 0.0, 0.5)
            vent    = st.slider("Vitesse du vent (km/h)", 0.0, 60.0, 8.0, 0.5)
            rafales = st.slider("Rafales de vent (km/h)", vent, 120.0,
                                 min(vent + 10, 120.0), 0.5)
            st.markdown("##### ☀ Rayonnement")
            rayonnement = st.slider("Rayonnement solaire (MJ/m²)", 0.0, 40.0, 22.0, 0.5)
            ensoleil    = st.slider("Ensoleillement (h)", 0.0, 14.0, 8.0, 0.1)
            daylight    = st.slider("Durée du jour (h)", 10.0, 14.0, 12.0, 0.1)

        with c3:
            st.markdown("##### 🌱 Indicateurs agricoles")
            et0 = st.slider("Évapotranspiration FAO (mm)", 0.0, 15.0, 4.0, 0.1)

            is_no_wind    = 1 if vent < 5 else 0
            is_no_rain    = 1 if pluie < 0.1 else 0
            is_dry_season = 1 if mois_input in [11, 12, 1, 2, 3] else 0

            conditions = []
            if is_no_wind:    conditions.append(("Absence de vent",  "#e8354a"))
            else:             conditions.append(("Vent actif",        "#00c896"))
            if is_no_rain:    conditions.append(("Absence de pluie",  "#f5a623"))
            else:             conditions.append(("Précipitations",    "#00c896"))
            if is_dry_season: conditions.append(("Saison sèche",      "#e8354a"))
            else:             conditions.append(("Saison des pluies", "#00c896"))

            cond_items = "".join([
                f'<div class="cond-item">'
                f'<span class="cond-led" style="background:{color}"></span>'
                f'{label}</div>'
                for label, color in conditions
            ])
            st.markdown("##### 📋 Conditions détectées")
            st.markdown(f'<div class="cond-box">{cond_items}</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        submit = st.form_submit_button(
            "🔮  Lancer la simulation PM2.5",
            use_container_width=True,
            type="primary"
        )

    if submit:
        sunshine_ratio = ensoleil / (daylight + 1e-6)
        temp_amplitude = temp_max - temp_min
        month_sin      = np.sin(2 * np.pi * mois_input / 12)
        month_cos      = np.cos(2 * np.pi * mois_input / 12)
        day_of_year    = pd.Timestamp(year=2024, month=mois_input, day=15).dayofyear

        df_ref     = df[(df['city'].astype(str) == str(city_input)) & (df['month'] == mois_input)]
        temp_lag1  = df_ref['temp_lag1'].median()  if not df_ref['temp_lag1'].isna().all()  else temp_mean
        temp_lag7  = df_ref['temp_lag7'].median()  if not df_ref['temp_lag7'].isna().all()  else temp_mean
        wind_lag1  = df_ref['wind_lag1'].median()  if not df_ref['wind_lag1'].isna().all()  else vent
        temp_roll7 = df_ref['temp_roll7'].median() if not df_ref['temp_roll7'].isna().all() else temp_mean

        X_input = pd.DataFrame([{
            'temperature_2m_mean':        temp_mean,
            'temperature_2m_max':         temp_max,
            'temperature_2m_min':         temp_min,
            'precipitation_sum':          pluie,
            'wind_speed_10m_max':         vent,
            'wind_gusts_10m_max':         rafales,
            'shortwave_radiation_sum':    rayonnement,
            'et0_fao_evapotranspiration': et0,
            'sunshine_ratio':             sunshine_ratio,
            'temp_amplitude':             temp_amplitude,
            'is_no_wind':                 is_no_wind,
            'is_no_rain':                 is_no_rain,
            'is_dry_season':              is_dry_season,
            'month_sin':                  month_sin,
            'month_cos':                  month_cos,
            'day_of_year':                day_of_year,
            'temp_lag1':                  temp_lag1,
            'temp_lag7':                  temp_lag7,
            'wind_lag1':                  wind_lag1,
            'temp_roll7':                 temp_roll7,
            'latitude':                   lat,
            'longitude':                  lon,
            'city':                       city_input,
            'region':                     region_input,
        }])

        X_input['city']   = pd.Categorical(X_input['city'],   categories=df['city'].cat.categories)
        X_input['region'] = pd.Categorical(X_input['region'], categories=df['region'].cat.categories)
        X_input           = fill_na_features(X_input)

        pm25_result         = model.predict(X_input[FEATURES_LGB])[0]
        label, css, message = get_alerte(pm25_result)
        color_res           = alert_color(pm25_result)

        st.markdown("<br>", unsafe_allow_html=True)
        sec("📊", "Résultat de la simulation", city_input)

        res_col, gauge_col = st.columns([1, 1.6])

        with res_col:
            glow_color = color_res.replace('#', '')
            r_hex = int(glow_color[0:2], 16)
            g_hex = int(glow_color[2:4], 16)
            b_hex = int(glow_color[4:6], 16)
            st.markdown(f"""
            <div class="pred-card" style="
              background: radial-gradient(circle at 50% 0,
                rgba({r_hex},{g_hex},{b_hex},0.08) 0%, transparent 60%),
              var(--glass);
              border-color: rgba({r_hex},{g_hex},{b_hex},0.22);
            ">
              <div class="pred-city">PM2.5 estimé · {city_input}</div>
              <div class="pred-num" style="color:{color_res}">{pm25_result:.2f}</div>
              <div class="pred-unit">μg / m³</div>
              <div class="{css}">{label}<br>
                <span style="font-weight:300; font-size:12px;">{message}</span>
              </div>
              <div class="pred-meta">
                {mois_noms[mois_input-1].upper()} · {str(region_input).upper()}<br>
                {lat:.4f}°N · {lon:.4f}°E
              </div>
            </div>
            """, unsafe_allow_html=True)

        with gauge_col:
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=pm25_result,
                delta={'reference': 15, 'valueformat': '.2f',
                       'font': {'size': 14, 'color': '#5a8a78', 'family': 'Space Mono'}},
                number={'valueformat': '.2f',
                        'font': {'size': 56, 'color': color_res, 'family': 'Fraunces'}},
                title={
                    'text': (f"<b style='color:#c2dfd5;font-family:Fraunces'>PM2.5</b>"
                             f"<br><span style='font-size:0.65em;color:#5a8a78;font-family:Space Mono'>"
                             f"μg/m³ · {city_input}</span>"),
                    'font': {'size': 15}
                },
                gauge={
                    'axis': {'range': [0, 50], 'tickwidth': 1, 'tickcolor': '#1a3a2a',
                             'tickfont': {'color': '#5a8a78', 'size': 10, 'family': 'Space Mono'}},
                    'bar':  {'color': color_res, 'thickness': 0.18},
                    'bgcolor': 'rgba(0,0,0,0)',
                    'borderwidth': 0,
                    'steps': [
                        {'range': [0,  15], 'color': 'rgba(0,200,150,0.06)'},
                        {'range': [15, 25], 'color': 'rgba(245,166,35,0.06)'},
                        {'range': [25, 50], 'color': 'rgba(232,53,74,0.06)'},
                    ],
                    'threshold': {
                        'line': {'color': color_res, 'width': 2},
                        'thickness': 0.82,
                        'value': pm25_result,
                    },
                },
            ))
            fig_gauge.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Nunito', color='#5a8a78'),
                height=340,
                margin=dict(l=30, r=30, t=55, b=20),
            )
            st.plotly_chart(fig_gauge, use_container_width=True)

        st.markdown(f"""
        <div class="seuils">
          <div class="seuils-head">Seuils de référence · OMS / IndabaX 2026</div>
          <div class="seuils-row">
            <div class="seuil" style="background:rgba(0,200,150,0.05);border-color:rgba(0,200,150,0.16)">
              <div class="seuil-v" style="color:#00c896">&lt; 15</div>
              <div class="seuil-l">Bon · μg/m³</div>
            </div>
            <div class="seuil" style="background:rgba(245,166,35,0.05);border-color:rgba(245,166,35,0.16)">
              <div class="seuil-v" style="color:#f5a623">15–25</div>
              <div class="seuil-l">Modéré · μg/m³</div>
            </div>
            <div class="seuil" style="background:rgba(232,53,74,0.05);border-color:rgba(232,53,74,0.16)">
              <div class="seuil-v" style="color:#e8354a">&gt; 25</div>
              <div class="seuil-l">Mauvais · μg/m³</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
#  FOOTER
# ════════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="footer">
  <div class="foot-brand">
    <b>IndabaX·Cam</b> Dashboard · Hackathon IndabaX Cameroon 2026 · IA &amp; Résilience Climatique
  </div>
  <div class="foot-meta">
    LightGBM · Open-Meteo · 42 villes · 87 240 obs. · 2020–2025
  </div>
</div>
""", unsafe_allow_html=True)
