# ═══════════════════════════════════════════════════════════════════════════════
#  DASHBOARD — IndabaX Cameroon 2026
#  Prédiction de la Qualité de l'Air (PM2.5) au Cameroun
#  Stack : Streamlit + Folium + Plotly + XGBoost
# ═══════════════════════════════════════════════════════════════════════════════
#
#  INSTALLATION :
#    pip install streamlit folium streamlit-folium plotly pandas numpy
#    pip install xgboost scikit-learn joblib requests
#
#  LANCEMENT :
#    streamlit run dashboard.py
#
#  STRUCTURE DU PROJET :
#    dashboard.py
#    models/
#      xgboost_pm25.pkl
#      model_meta.pkl
#    data/
#      dataset_complet_repare.csv
# ═══════════════════════════════════════════════════════════════════════════════

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
from streamlit_folium import st_folium
import joblib
import requests
import datetime
import os
import warnings
warnings.filterwarnings('ignore')

# ── CONFIG PAGE ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="IndabaX 2026 — Qualité de l'Air Cameroun",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── COULEURS INDABAX ──────────────────────────────────────────────────────────
GREEN    = "#2D8B4E"
DARK     = "#1A5C32"
LIGHT    = "#E8F5EE"
ACCENT   = "#F4A623"
RED_CM   = "#C0392B"
TEXT     = "#1A1A2E"
GRAY     = "#F5F5F5"

# ── CSS PERSONNALISÉ ──────────────────────────────────────────────────────────
st.markdown(f"""
<style>
  /* Police et fond */
  html, body, [class*="css"] {{
    font-family: 'Segoe UI', sans-serif;
  }}
  .main {{ background-color: #F8FAF9; }}

  /* Header principal */
  .main-header {{
    background: linear-gradient(135deg, {DARK} 0%, {GREEN} 60%, #3DAB6A 100%);
    padding: 1.5rem 2rem;
    border-radius: 12px;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 1.5rem;
    box-shadow: 0 4px 20px rgba(45,139,78,0.25);
  }}
  .header-text h1 {{
    color: white !important;
    font-size: 1.7rem;
    font-weight: 700;
    margin: 0;
    line-height: 1.2;
  }}
  .header-text p {{
    color: rgba(255,255,255,0.85);
    font-size: 0.9rem;
    margin: 4px 0 0 0;
  }}

  /* Métriques KPI */
  .kpi-card {{
    background: white;
    border-radius: 12px;
    padding: 1.2rem 1rem;
    text-align: center;
    border-left: 4px solid {GREEN};
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    margin-bottom: 0.5rem;
  }}
  .kpi-card.accent {{ border-left-color: {ACCENT}; }}
  .kpi-card.red    {{ border-left-color: {RED_CM}; }}
  .kpi-card.blue   {{ border-left-color: #3498DB; }}
  .kpi-value {{
    font-size: 2rem;
    font-weight: 700;
    color: {TEXT};
    line-height: 1.1;
  }}
  .kpi-label {{
    font-size: 0.75rem;
    color: #666;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-top: 4px;
  }}
  .kpi-sub {{
    font-size: 0.8rem;
    color: {GREEN};
    font-weight: 600;
    margin-top: 2px;
  }}

  /* Alerte niveaux */
  .alerte-bon     {{ background:#E8F5EE; border:2px solid {GREEN}; border-radius:10px; padding:0.8rem 1rem; }}
  .alerte-modere  {{ background:#FFF8E1; border:2px solid {ACCENT}; border-radius:10px; padding:0.8rem 1rem; }}
  .alerte-mauvais {{ background:#FFF0EE; border:2px solid #E67E22; border-radius:10px; padding:0.8rem 1rem; }}
  .alerte-danger  {{ background:#FDEDEC; border:2px solid {RED_CM}; border-radius:10px; padding:0.8rem 1rem; }}

  /* Section title */
  .section-title {{
    color: {DARK};
    font-size: 1.1rem;
    font-weight: 700;
    border-left: 4px solid {GREEN};
    padding-left: 10px;
    margin: 1.5rem 0 0.8rem 0;
  }}

  /* Sidebar */
  .css-1d391kg, [data-testid="stSidebar"] {{
    background: white;
    border-right: 1px solid #E0E0E0;
  }}

  /* Scrollbar */
  ::-webkit-scrollbar {{ width: 6px; }}
  ::-webkit-scrollbar-thumb {{ background: {GREEN}; border-radius: 3px; }}

  /* Badge modèle */
  .model-badge {{
    display:inline-block;
    background:{GREEN};
    color:white;
    padding:3px 10px;
    border-radius:20px;
    font-size:0.75rem;
    font-weight:600;
  }}

  /* Footer */
  .footer {{
    text-align:center;
    color:#999;
    font-size:0.75rem;
    padding: 1rem 0;
    border-top: 1px solid #E0E0E0;
    margin-top: 2rem;
  }}
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# DONNÉES ET MODÈLE
# ════════════════════════════════════════════════════════════════════════════

@st.cache_data
def load_data():
    df = pd.read_csv("data/dataset_complet_repare.csv")
    df['time'] = pd.to_datetime(df['time'])
    return df

@st.cache_resource
def load_model():
    model = joblib.load("models/xgboost_pm25.pkl")
    meta  = joblib.load("models/model_meta.pkl")
    return model, meta

@st.cache_data(ttl=3600)
def fetch_openmeteo_forecast(lat, lon, city_name):
    """Récupère les prévisions météo 16 jours depuis Open-Meteo."""
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat, "longitude": lon,
            "daily": ",".join([
                "temperature_2m_max","temperature_2m_min","temperature_2m_mean",
                "apparent_temperature_mean","precipitation_sum","rain_sum",
                "precipitation_hours","wind_speed_10m_max","wind_gusts_10m_max",
                "shortwave_radiation_sum","et0_fao_evapotranspiration",
                "sunshine_duration","daylight_duration",
            ]),
            "forecast_days": 16,
            "timezone": "Africa/Douala",
        }
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()["daily"]
        df = pd.DataFrame(data)
        df['time'] = pd.to_datetime(df['time'])
        df['city'] = city_name
        return df
    except Exception as e:
        return None

@st.cache_data(ttl=3600)
def fetch_openmeteo_dust(lat, lon):
    """Récupère les prévisions de poussière (dust) depuis l'API qualité de l'air."""
    try:
        url = "https://air-quality-api.open-meteo.com/v1/air-quality"
        params = {
            "latitude": lat, "longitude": lon,
            "hourly": "dust",
            "forecast_days": 7,
        }
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()["hourly"]
        df = pd.DataFrame({"time": pd.to_datetime(data["time"]), "dust_h": data["dust"]})
        df['date'] = df['time'].dt.date
        dust_daily = df.groupby('date')['dust_h'].mean().reset_index()
        dust_daily.columns = ['date', 'dust']
        dust_daily['date'] = pd.to_datetime(dust_daily['date'])
        return dust_daily
    except:
        return None


# ── Niveaux OMS ───────────────────────────────────────────────────────────────
def get_oms_level(pm25):
    if pm25 < 15:
        return "🟢 BON",        "#2D8B4E", "alerte-bon",     "Air de bonne qualité"
    elif pm25 < 35:
        return "🟡 MODÉRÉ",     "#F4A623", "alerte-modere",  "Personnes sensibles concernées"
    elif pm25 < 55:
        return "🟠 MAUVAIS",    "#E67E22", "alerte-mauvais", "Risque pour la santé générale"
    else:
        return "🔴 TRÈS MAUVAIS","#C0392B", "alerte-danger",  "Alerte sanitaire — éviter sorties"

def color_marker(pm25):
    if pm25 < 15:   return "green"
    elif pm25 < 35: return "orange"
    elif pm25 < 55: return "red"
    else:           return "darkred"


# ── Prédiction PM2.5 ──────────────────────────────────────────────────────────
def predict_pm25(model, meta, row_dict):
    """Prédit le PM2.5 à partir d'un dict de features."""
    from sklearn.preprocessing import LabelEncoder
    le_city   = meta['label_encoder_city']
    le_region = meta['label_encoder_region']
    FEATURES  = meta['features']

    city   = row_dict.get('city', 'Yaounde')
    region = row_dict.get('region', 'Centre')

    try:
        city_enc   = int(le_city.transform([city])[0])
        region_enc = int(le_region.transform([region])[0])
    except:
        city_enc, region_enc = 0, 0

    row_dict['city_enc']   = city_enc
    row_dict['region_enc'] = region_enc

    row = pd.DataFrame([{f: row_dict.get(f, 0) for f in FEATURES}])
    pred = float(model.predict(row)[0])
    return max(0.0, round(pred, 2))


def prepare_forecast_features(df_fc, dust_df, city, region, lat, lon,
                               df_hist, model, meta):
    """Prépare les features pour les 16 jours de prévisions et prédit."""
    results = []
    # Historique récent pour les lags
    df_city = df_hist[(df_hist['city'] == city) & df_hist['pm25'].notna()].copy()
    df_city = df_city.sort_values('time').tail(30)

    # PM2.5 récents pour les lags
    pm25_recent = df_city['pm25'].values.tolist() if len(df_city) > 0 else [15.0]*10
    temp_recent = df_city['temperature_2m_mean'].values.tolist() if len(df_city) > 0 else [25.0]*10
    wind_recent = df_city['wind_speed_10m_max'].values.tolist() if len(df_city) > 0 else [10.0]*10
    dust_recent_hist = df_city['dust'].values.tolist() if len(df_city) > 0 else [5.0]*10

    # Remplir les lags avec des listes glissantes
    pm25_series = pm25_recent.copy()
    temp_series = temp_recent.copy()
    wind_series = wind_recent.copy()
    dust_series = dust_recent_hist.copy()

    for i, row in df_fc.iterrows():
        month      = row['time'].month
        day_of_year= row['time'].dayofyear
        month_sin  = np.sin(2 * np.pi * month / 12)
        month_cos  = np.cos(2 * np.pi * month / 12)

        t_mean = row.get('temperature_2m_mean', 25.0) or 25.0
        t_max  = row.get('temperature_2m_max',  30.0) or 30.0
        t_min  = row.get('temperature_2m_min',  20.0) or 20.0
        t_app  = row.get('apparent_temperature_mean', t_mean) or t_mean
        precip = row.get('precipitation_sum', 0.0) or 0.0
        rain   = row.get('rain_sum', 0.0) or 0.0
        prec_h = row.get('precipitation_hours', 0.0) or 0.0
        wind   = row.get('wind_speed_10m_max', 10.0) or 10.0
        gusts  = row.get('wind_gusts_10m_max', 15.0) or 15.0
        rad    = row.get('shortwave_radiation_sum', 18.0) or 18.0
        sun    = row.get('sunshine_duration', 30000.0) or 30000.0
        daylight = row.get('daylight_duration', 43000.0) or 43000.0

        # Dust depuis API qualité de l'air
        dust_val = 5.0
        if dust_df is not None:
            day_row = dust_df[dust_df['date'] == row['time']]
            if not day_row.empty:
                dust_val = float(day_row['dust'].iloc[0]) or 5.0

        sunshine_ratio = sun / (daylight + 1e-6)
        temp_amplitude = t_max - t_min
        is_no_wind     = 1 if wind < 5 else 0
        is_no_rain     = 1 if precip < 0.1 else 0
        is_dry_season  = 1 if month in [11,12,1,2,3] else 0

        def lag(series, n, default=None):
            if len(series) >= n:
                return float(series[-n])
            return default if default is not None else (series[0] if series else 15.0)

        def roll(series, n=7):
            tail = series[-n:] if len(series) >= n else series
            return float(np.mean(tail)) if tail else 15.0

        feat = {
            'city': city, 'region': region,
            'temperature_2m_mean'      : t_mean,
            'temperature_2m_max'       : t_max,
            'temperature_2m_min'       : t_min,
            'apparent_temperature_mean': t_app,
            'precipitation_sum'        : precip,
            'rain_sum'                 : rain,
            'precipitation_hours'      : prec_h,
            'wind_speed_10m_max'       : wind,
            'wind_gusts_10m_max'       : gusts,
            'shortwave_radiation_sum'  : rad,
            'sunshine_ratio'           : sunshine_ratio,
            'dust'                     : dust_val,
            'temp_amplitude'           : temp_amplitude,
            'is_no_wind'               : is_no_wind,
            'is_no_rain'               : is_no_rain,
            'is_dry_season'            : is_dry_season,
            'month_sin'                : month_sin,
            'month_cos'                : month_cos,
            'day_of_year'              : day_of_year,
            'temp_lag1'                : lag(temp_series, 1, t_mean),
            'temp_lag3'                : lag(temp_series, 3, t_mean),
            'temp_lag7'                : lag(temp_series, 7, t_mean),
            'wind_lag1'                : lag(wind_series, 1, wind),
            'wind_lag3'                : lag(wind_series, 3, wind),
            'dust_lag1'                : lag(dust_series, 1, dust_val),
            'dust_lag3'                : lag(dust_series, 3, dust_val),
            'dust_lag7'                : lag(dust_series, 7, dust_val),
            'temp_roll7'               : roll(temp_series),
            'dust_roll7'               : roll(dust_series),
            'pm25_lag1'                : lag(pm25_series, 1, 15.0),
            'pm25_lag3'                : lag(pm25_series, 3, 15.0),
            'pm25_lag7'                : lag(pm25_series, 7, 15.0),
            'pm25_roll7'               : roll(pm25_series),
            'latitude'                 : lat,
            'longitude'                : lon,
        }

        pm25_pred = predict_pm25(model, meta, feat.copy())
        results.append({
            'date'             : row['time'],
            'pm25_pred'        : pm25_pred,
            'temperature_mean' : t_mean,
            'precipitation'    : precip,
            'wind'             : wind,
            'dust'             : dust_val,
        })

        # Mise à jour des séries glissantes
        pm25_series.append(pm25_pred)
        temp_series.append(t_mean)
        wind_series.append(wind)
        dust_series.append(dust_val)

    return pd.DataFrame(results)


# ════════════════════════════════════════════════════════════════════════════
# CHARGEMENT
# ════════════════════════════════════════════════════════════════════════════
try:
    df       = load_data()
    model, meta = load_model()
    MODEL_OK = True
except Exception as e:
    MODEL_OK = False
    st.error(f"Erreur chargement modèle : {e}")
    st.stop()

# Données de référence par ville
CITY_INFO = (df.groupby('city')
               .agg(region=('region','first'),
                    lat=('latitude','first'),
                    lon=('longitude','first'))
               .reset_index())
CITY_DICT = {r['city']: r for _, r in CITY_INFO.iterrows()}
CITIES    = sorted(CITY_DICT.keys())


# ════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    # Logo IndabaX
    st.markdown(f"""
    <div style="text-align:center; padding:1rem 0; border-bottom:1px solid #E0E0E0; margin-bottom:1rem;">
      <div style="font-size:2.5rem;">🌿</div>
      <div style="font-weight:800; font-size:1.1rem; color:{DARK}; line-height:1.1;">
        DEEP LEARNING<br><span style="color:{GREEN}; font-size:1.4rem;">INDABAX</span><br>
        <span style="color:{RED_CM}; font-size:1rem;">CAMEROON</span>
        <span style="color:{ACCENT}; font-size:1rem;"> 2026</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🏙️ Sélection de la ville")
    selected_city = st.selectbox("Ville", CITIES, index=CITIES.index("Yaounde"))
    city_data     = CITY_DICT[selected_city]

    st.markdown(f"""
    <div style="background:{LIGHT}; border-radius:8px; padding:0.8rem; margin:0.5rem 0;">
      <div style="font-size:0.8rem; color:#666;">📍 Région</div>
      <div style="font-weight:700; color:{DARK};">{city_data['region']}</div>
      <div style="font-size:0.8rem; color:#666; margin-top:6px;">🌐 Coordonnées</div>
      <div style="font-weight:600; color:{TEXT}; font-size:0.85rem;">
        {city_data['lat']:.4f}°N, {city_data['lon']:.4f}°E
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### ⚙️ Options")
    show_hist = st.checkbox("Afficher historique", value=True)
    forecast_days = st.slider("Jours de prévision", 3, 16, 7)

    st.markdown("---")
    st.markdown("### 📊 Modèle")
    st.markdown(f"""
    <div style="background:{LIGHT}; border-radius:8px; padding:0.8rem;">
      <span class="model-badge">XGBoost</span>
      <div style="margin-top:8px; font-size:0.82rem; color:{TEXT};">
        <b>R²</b> = 0.9074 &nbsp;|&nbsp; <b>MAE</b> = 3.21 µg/m³<br>
        <span style="color:#666;">Validation temporelle 2025</span>
      </div>
    </div>
    <div style="margin-top:8px; font-size:0.78rem; color:#888;">
      Source PM2.5 : CAMS/Copernicus<br>
      Météo : Open-Meteo API
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🚦 Seuils OMS (PM2.5)")
    oms_table = pd.DataFrame({
        "Niveau": ["🟢 BON", "🟡 MODÉRÉ", "🟠 MAUVAIS", "🔴 TRÈS MAUVAIS"],
        "PM2.5 (µg/m³)": ["< 15", "15 – 35", "35 – 55", "> 55"]
    })
    st.dataframe(oms_table, hide_index=True, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# HEADER
# ════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="main-header">
  <div style="font-size:3rem; flex-shrink:0;">🌍</div>
  <div class="header-text">
    <h1>Qualité de l'Air au Cameroun — Prédiction PM2.5</h1>
    <p>Hackathon IndabaX Cameroon 2026 · 40 villes · 10 régions · Modèle XGBoost</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# ONGLETS PRINCIPAUX
# ════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4 = st.tabs([
    "🗺️ Carte & Alertes",
    "📈 Prévisions 16 jours",
    "📊 Analyse historique",
    "🔮 Simulateur manuel",
])


# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — CARTE & ALERTES
# ════════════════════════════════════════════════════════════════════════════
with tab1:
    # KPI globaux
    df_valid = df[df['pm25'].notna()]
    pm25_moy_national = df_valid['pm25'].mean()
    pm25_max_national = df_valid['pm25'].max()
    n_villes_alerte   = (df_valid.groupby('city')['pm25'].mean() > 35).sum()
    pm25_ville        = df_valid[df_valid['city'] == selected_city]['pm25'].mean()
    level, lcolor, lcss, ldesc = get_oms_level(pm25_ville if not np.isnan(pm25_ville) else 15)

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""
        <div class="kpi-card">
          <div class="kpi-value">{pm25_moy_national:.1f}</div>
          <div class="kpi-label">PM2.5 national moyen</div>
          <div class="kpi-sub">µg/m³ · 2022-2025</div>
        </div>""", unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
        <div class="kpi-card accent">
          <div class="kpi-value">{pm25_ville:.1f}</div>
          <div class="kpi-label">PM2.5 — {selected_city}</div>
          <div class="kpi-sub">{level}</div>
        </div>""", unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
        <div class="kpi-card red">
          <div class="kpi-value">{n_villes_alerte}</div>
          <div class="kpi-label">Villes PM2.5 > 35 µg/m³</div>
          <div class="kpi-sub">Sur 40 villes</div>
        </div>""", unsafe_allow_html=True)
    with k4:
        st.markdown(f"""
        <div class="kpi-card blue">
          <div class="kpi-value">3.21</div>
          <div class="kpi-label">MAE du modèle</div>
          <div class="kpi-sub">µg/m³ · Validation 2025</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-title">🗺️ Carte de la Pollution — PM2.5 moyen par ville</div>',
                unsafe_allow_html=True)

    col_map, col_rank = st.columns([3, 1])

    with col_map:
        # Données carte
        city_pm25 = df_valid.groupby('city').agg(
            pm25_moy=('pm25','mean'), pm25_max=('pm25','max'),
            dust_moy=('dust','mean'),
            region=('region','first'),
            lat=('latitude','first'), lon=('longitude','first')
        ).reset_index().round(2)

        # Carte Folium centrée sur le Cameroun
        m = folium.Map(
            location=[5.5, 12.5],
            zoom_start=6,
            tiles="CartoDB positron",
            control_scale=True,
        )

        # Heatmap layer (cercles colorés)
        for _, row in city_pm25.iterrows():
            lv, lc, _, ld = get_oms_level(row['pm25_moy'])
            color = color_marker(row['pm25_moy'])
            radius = 8 + row['pm25_moy'] / 5

            popup_html = f"""
            <div style="font-family:sans-serif; min-width:180px;">
              <div style="background:{GREEN}; color:white; padding:6px 10px;
                          border-radius:6px 6px 0 0; font-weight:700;">
                📍 {row['city']}
              </div>
              <div style="padding:8px 10px; background:white;">
                <b>Région :</b> {row['region']}<br>
                <b>PM2.5 moyen :</b> {row['pm25_moy']} µg/m³<br>
                <b>PM2.5 max :</b> {row['pm25_max']} µg/m³<br>
                <b>Poussière :</b> {row['dust_moy']} µg/m³<br>
                <hr style="margin:6px 0;">
                <b>Niveau OMS :</b> <span style="color:{lc};">{lv}</span><br>
                <small style="color:#666;">{ld}</small>
              </div>
            </div>
            """
            folium.CircleMarker(
                location=[row['lat'], row['lon']],
                radius=radius,
                color=color, fill=True, fill_color=color,
                fill_opacity=0.7, weight=2,
                popup=folium.Popup(popup_html, max_width=220),
                tooltip=f"{row['city']} — {row['pm25_moy']} µg/m³",
            ).add_to(m)

        # Marquer la ville sélectionnée
        sel = city_pm25[city_pm25['city'] == selected_city]
        if not sel.empty:
            r = sel.iloc[0]
            folium.Marker(
                location=[r['lat'], r['lon']],
                popup=f"<b>{r['city']}</b> — Sélectionnée",
                tooltip=f"✅ {r['city']}",
                icon=folium.Icon(color='green', icon='star', prefix='fa'),
            ).add_to(m)

        # Légende
        legend_html = f"""
        <div style="position:fixed; bottom:30px; left:30px; z-index:1000;
                    background:white; padding:10px 14px; border-radius:8px;
                    border:2px solid {GREEN}; font-family:sans-serif; font-size:12px;
                    box-shadow:0 2px 8px rgba(0,0,0,0.2);">
          <b style="color:{DARK};">🚦 Niveaux OMS PM2.5</b><br>
          <span style="color:green;">●</span> Bon (&lt;15 µg/m³)<br>
          <span style="color:orange;">●</span> Modéré (15-35)<br>
          <span style="color:red;">●</span> Mauvais (35-55)<br>
          <span style="color:darkred;">●</span> Très mauvais (&gt;55)
        </div>"""
        m.get_root().html.add_child(folium.Element(legend_html))

        st_folium(m, width=None, height=480, returned_objects=[])

    with col_rank:
        st.markdown("**🏆 Classement villes**")
        st.markdown("<small style='color:#666;'>PM2.5 moyen (µg/m³)</small>", unsafe_allow_html=True)
        city_rank = city_pm25.sort_values('pm25_moy', ascending=False)
        for _, r in city_rank.iterrows():
            lv, lc, _, _ = get_oms_level(r['pm25_moy'])
            bg = LIGHT if r['city'] == selected_city else "white"
            bord = f"2px solid {GREEN}" if r['city'] == selected_city else "1px solid #EEE"
            st.markdown(f"""
            <div style="background:{bg}; border:{bord}; border-radius:6px;
                        padding:4px 8px; margin-bottom:3px; font-size:0.8rem;">
              <b>{r['city']}</b>
              <span style="float:right; color:{lc}; font-weight:700;">{r['pm25_moy']}</span>
            </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — PRÉVISIONS 16 JOURS
# ════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown(f'<div class="section-title">📈 Prévisions PM2.5 — {selected_city} ({forecast_days} jours)</div>',
                unsafe_allow_html=True)

    lat = city_data['lat']
    lon = city_data['lon']

    with st.spinner(f"Récupération des données météo Open-Meteo pour {selected_city}..."):
        df_fc   = fetch_openmeteo_forecast(lat, lon, selected_city)
        dust_fc = fetch_openmeteo_dust(lat, lon)

    if df_fc is None:
        st.warning("⚠️ Impossible de récupérer les prévisions météo (vérifier la connexion internet).")
    else:
        df_fc = df_fc.head(forecast_days)

        with st.spinner("Calcul des prédictions PM2.5..."):
            fc_results = prepare_forecast_features(
                df_fc, dust_fc, selected_city, city_data['region'],
                lat, lon, df, model, meta
            )

        # Alertes futures
        n_alert = (fc_results['pm25_pred'] > 35).sum()
        n_danger= (fc_results['pm25_pred'] > 55).sum()
        max_fc  = fc_results['pm25_pred'].max()
        mean_fc = fc_results['pm25_pred'].mean()

        # KPI prévisions
        f1, f2, f3, f4 = st.columns(4)
        with f1:
            lv, lc, _, _ = get_oms_level(mean_fc)
            st.markdown(f"""<div class="kpi-card">
              <div class="kpi-value" style="color:{lc};">{mean_fc:.1f}</div>
              <div class="kpi-label">PM2.5 moyen prévu</div>
              <div class="kpi-sub">{lv}</div></div>""", unsafe_allow_html=True)
        with f2:
            lv2, lc2, _, _ = get_oms_level(max_fc)
            st.markdown(f"""<div class="kpi-card accent">
              <div class="kpi-value" style="color:{lc2};">{max_fc:.1f}</div>
              <div class="kpi-label">PM2.5 max prévu</div>
              <div class="kpi-sub">{lv2}</div></div>""", unsafe_allow_html=True)
        with f3:
            st.markdown(f"""<div class="kpi-card {'red' if n_alert > 0 else ''}">
              <div class="kpi-value">{n_alert}</div>
              <div class="kpi-label">Jours > 35 µg/m³</div>
              <div class="kpi-sub">Niveau mauvais</div></div>""", unsafe_allow_html=True)
        with f4:
            st.markdown(f"""<div class="kpi-card {'red' if n_danger > 0 else ''}">
              <div class="kpi-value">{n_danger}</div>
              <div class="kpi-label">Jours > 55 µg/m³</div>
              <div class="kpi-sub">Alerte sanitaire</div></div>""", unsafe_allow_html=True)

        # Graphique prévisions
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            row_heights=[0.6, 0.4],
            vertical_spacing=0.08,
            subplot_titles=["PM2.5 prédit (µg/m³)", "Météo associée"]
        )

        # Zones de couleur OMS
        x_range = [fc_results['date'].min(), fc_results['date'].max()]
        zones = [(0, 15, "rgba(45,139,78,0.08)"), (15, 35, "rgba(244,166,35,0.1)"),
                 (35, 55, "rgba(230,126,34,0.12)"), (55, 999, "rgba(192,57,43,0.1)")]
        for ymin, ymax, color in zones:
            fig.add_hrect(y0=ymin, y1=min(ymax, max_fc*1.1+5),
                          fillcolor=color, line_width=0, row=1, col=1)

        # Seuils OMS
        for val, label, color in [(15, "OMS 15", "green"), (35, "OMS 35", "orange"),
                                   (55, "OMS 55", "red")]:
            if val <= max_fc * 1.2:
                fig.add_hline(y=val, line_dash="dot", line_color=color,
                              line_width=1.5, row=1, col=1,
                              annotation_text=label, annotation_position="right")

        # Courbe PM2.5
        pm25_colors = [color_marker(v) for v in fc_results['pm25_pred']]
        fig.add_trace(go.Scatter(
            x=fc_results['date'], y=fc_results['pm25_pred'],
            mode='lines+markers',
            line=dict(color=GREEN, width=2.5),
            marker=dict(size=9, color=pm25_colors, line=dict(color='white', width=1.5)),
            name="PM2.5 prédit",
            hovertemplate="<b>%{x|%d %b}</b><br>PM2.5 : %{y:.1f} µg/m³<extra></extra>",
        ), row=1, col=1)

        # Zone remplie sous la courbe
        fig.add_trace(go.Scatter(
            x=fc_results['date'], y=fc_results['pm25_pred'],
            fill='tozeroy', mode='none',
            fillcolor='rgba(45,139,78,0.1)',
            showlegend=False, hoverinfo='skip',
        ), row=1, col=1)

        # Barres météo
        fig.add_trace(go.Bar(
            x=fc_results['date'], y=fc_results['precipitation'],
            name="Précipitations (mm)", marker_color='rgba(52,152,219,0.7)',
            yaxis='y3', hovertemplate="%{y:.1f} mm<extra></extra>",
        ), row=2, col=1)
        fig.add_trace(go.Scatter(
            x=fc_results['date'], y=fc_results['temperature_mean'],
            name="Température (°C)", line=dict(color='tomato', width=2),
            yaxis='y4', hovertemplate="%{y:.1f}°C<extra></extra>",
        ), row=2, col=1)

        fig.update_layout(
            height=520,
            plot_bgcolor='white', paper_bgcolor='white',
            font=dict(family="Segoe UI", size=11),
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
            hovermode='x unified',
            margin=dict(l=10, r=60, t=30, b=10),
        )
        fig.update_yaxes(title_text="PM2.5 (µg/m³)", row=1, col=1, gridcolor='#F0F0F0')
        fig.update_yaxes(title_text="Précip. (mm)", row=2, col=1, gridcolor='#F0F0F0')

        st.plotly_chart(fig, use_container_width=True)

        # Tableau détaillé
        st.markdown("**📋 Détail journalier**")
        fc_display = fc_results.copy()
        fc_display['date'] = fc_display['date'].dt.strftime('%a %d %b')
        fc_display['niveau'] = fc_display['pm25_pred'].apply(
            lambda x: get_oms_level(x)[0])
        fc_display.columns = ['Date','PM2.5 prédit','Temp. (°C)','Précip. (mm)','Vent (km/h)','Dust (µg/m³)','Niveau OMS']
        fc_display['PM2.5 prédit'] = fc_display['PM2.5 prédit'].round(1)
        st.dataframe(fc_display, hide_index=True, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — ANALYSE HISTORIQUE
# ════════════════════════════════════════════════════════════════════════════
with tab3:
    df_city_hist = df[(df['city'] == selected_city) & df['pm25'].notna()].copy()
    df_city_hist['month'] = df_city_hist['time'].dt.month
    df_city_hist['year']  = df_city_hist['time'].dt.year

    st.markdown(f'<div class="section-title">📊 Historique PM2.5 — {selected_city}</div>',
                unsafe_allow_html=True)

    h1, h2 = st.columns([2, 1])

    with h1:
        # Série temporelle historique
        fig_hist = go.Figure()
        fig_hist.add_trace(go.Scatter(
            x=df_city_hist['time'], y=df_city_hist['pm25'],
            mode='lines', name='PM2.5 réel',
            line=dict(color=GREEN, width=1.5),
            hovertemplate="<b>%{x|%d %b %Y}</b><br>PM2.5 : %{y:.1f} µg/m³<extra></extra>",
        ))
        # Moyenne mobile 30j
        df_city_hist_sorted = df_city_hist.sort_values('time')
        fig_hist.add_trace(go.Scatter(
            x=df_city_hist_sorted['time'],
            y=df_city_hist_sorted['pm25'].rolling(30, min_periods=1).mean(),
            mode='lines', name='Moy. mobile 30j',
            line=dict(color=ACCENT, width=2, dash='dash'),
        ))
        for val, color, label in [(15,'green','OMS 15'),(35,'orange','OMS 35'),(55,'red','OMS 55')]:
            fig_hist.add_hline(y=val, line_dash='dot', line_color=color,
                               line_width=1, annotation_text=label,
                               annotation_position='right')
        fig_hist.update_layout(
            title=f"Évolution temporelle — {selected_city}",
            height=320, plot_bgcolor='white', paper_bgcolor='white',
            font=dict(family="Segoe UI", size=11),
            legend=dict(orientation='h', y=1.02),
            hovermode='x unified',
            yaxis=dict(title="PM2.5 (µg/m³)", gridcolor='#F0F0F0'),
            xaxis=dict(gridcolor='#F0F0F0'),
            margin=dict(l=10, r=60, t=40, b=10),
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    with h2:
        # Stats summary
        q1, q3 = df_city_hist['pm25'].quantile([0.25, 0.75])
        n_bon     = (df_city_hist['pm25'] < 15).sum()
        n_modere  = ((df_city_hist['pm25'] >= 15) & (df_city_hist['pm25'] < 35)).sum()
        n_mauvais = ((df_city_hist['pm25'] >= 35) & (df_city_hist['pm25'] < 55)).sum()
        n_danger  = (df_city_hist['pm25'] >= 55).sum()
        total     = len(df_city_hist)

        st.markdown(f"""
        <div style="background:white; border-radius:10px; padding:1rem;
                    border:1px solid #E0E0E0;">
          <div style="font-weight:700; color:{DARK}; margin-bottom:10px;">
            📊 Statistiques — {selected_city}
          </div>
          <table style="width:100%; font-size:0.83rem;">
            <tr><td style="color:#666;">Moyenne</td>
                <td style="font-weight:700;">{df_city_hist['pm25'].mean():.2f} µg/m³</td></tr>
            <tr><td style="color:#666;">Médiane</td>
                <td>{df_city_hist['pm25'].median():.2f} µg/m³</td></tr>
            <tr><td style="color:#666;">Max</td>
                <td style="color:{RED_CM}; font-weight:700;">{df_city_hist['pm25'].max():.1f} µg/m³</td></tr>
            <tr><td style="color:#666;">Q1 – Q3</td>
                <td>{q1:.1f} – {q3:.1f}</td></tr>
            <tr><td style="color:#666;">Observations</td>
                <td>{total}</td></tr>
          </table>
          <hr style="margin:8px 0;">
          <div style="font-size:0.82rem;">
            <div><span style="color:green;">●</span> Bon : {n_bon} jours ({n_bon/total*100:.0f}%)</div>
            <div><span style="color:orange;">●</span> Modéré : {n_modere} jours ({n_modere/total*100:.0f}%)</div>
            <div><span style="color:#E67E22;">●</span> Mauvais : {n_mauvais} jours ({n_mauvais/total*100:.0f}%)</div>
            <div><span style="color:{RED_CM};">●</span> Danger : {n_danger} jours ({n_danger/total*100:.0f}%)</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # Saisonnalité
    st.markdown('<div class="section-title">📅 Saisonnalité PM2.5 par mois</div>',
                unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        monthly = df_city_hist.groupby('month')['pm25'].agg(['mean','max','min']).reset_index()
        mois = ['Jan','Fév','Mar','Avr','Mai','Juin','Juil','Aoû','Sep','Oct','Nov','Déc']
        monthly['mois_label'] = monthly['month'].apply(lambda x: mois[x-1])

        fig_monthly = go.Figure()
        # Zone min-max
        fig_monthly.add_trace(go.Scatter(
            x=monthly['mois_label'], y=monthly['max'],
            mode='lines', line=dict(width=0), showlegend=False, hoverinfo='skip',
        ))
        fig_monthly.add_trace(go.Scatter(
            x=monthly['mois_label'], y=monthly['min'],
            mode='lines', line=dict(width=0), fill='tonexty',
            fillcolor='rgba(45,139,78,0.15)', name='Min-Max', showlegend=True,
        ))
        fig_monthly.add_trace(go.Scatter(
            x=monthly['mois_label'], y=monthly['mean'],
            mode='lines+markers', name='Moyenne mensuelle',
            line=dict(color=GREEN, width=2.5),
            marker=dict(size=8, color=[color_marker(v) for v in monthly['mean']],
                       line=dict(color='white', width=1.5)),
        ))
        fig_monthly.add_hline(y=15, line_dash='dot', line_color='green',
                              annotation_text='OMS 15', line_width=1.5)
        fig_monthly.update_layout(
            title=f"PM2.5 mensuel — {selected_city}",
            height=300, plot_bgcolor='white', paper_bgcolor='white',
            font=dict(family="Segoe UI", size=11),
            yaxis=dict(title="PM2.5 (µg/m³)", gridcolor='#F0F0F0'),
            xaxis=dict(gridcolor='#F0F0F0'),
            legend=dict(orientation='h', y=1.1),
            margin=dict(l=10, r=40, t=40, b=10),
        )
        st.plotly_chart(fig_monthly, use_container_width=True)

    with c2:
        # Comparaison régionale
        region_pm25 = df_valid.groupby('region')['pm25'].mean().reset_index().sort_values('pm25', ascending=True)
        colors_bar = [GREEN if r != city_data['region'] else ACCENT for r in region_pm25['region']]

        fig_reg = go.Figure(go.Bar(
            x=region_pm25['pm25'], y=region_pm25['region'],
            orientation='h',
            marker_color=colors_bar,
            text=region_pm25['pm25'].round(1),
            textposition='outside',
            hovertemplate="%{y} : %{x:.1f} µg/m³<extra></extra>",
        ))
        fig_reg.add_vline(x=15, line_dash='dot', line_color='green',
                          annotation_text='OMS 15', line_width=1.5)
        fig_reg.update_layout(
            title="PM2.5 moyen par région",
            height=300, plot_bgcolor='white', paper_bgcolor='white',
            font=dict(family="Segoe UI", size=11),
            xaxis=dict(title="PM2.5 (µg/m³)", gridcolor='#F0F0F0'),
            margin=dict(l=10, r=60, t=40, b=10),
        )
        st.plotly_chart(fig_reg, use_container_width=True)

    # Corrélations
    st.markdown('<div class="section-title">🔗 Corrélations PM2.5 vs météo</div>',
                unsafe_allow_html=True)

    corr_vars = ['temperature_2m_mean','precipitation_sum','wind_speed_10m_max',
                 'shortwave_radiation_sum','dust','pm25']
    corr_labels = ['Température','Précipitations','Vent','Rayonnement','Poussière','PM2.5']
    corr_matrix = df_city_hist[corr_vars].corr()

    fig_corr = px.imshow(
        corr_matrix,
        x=corr_labels, y=corr_labels,
        color_continuous_scale=[[0,'#C0392B'],[0.5,'white'],[1,GREEN]],
        zmin=-1, zmax=1,
        text_auto='.2f',
        title=f"Matrice de corrélation — {selected_city}",
    )
    fig_corr.update_layout(
        height=350, margin=dict(l=10, r=10, t=40, b=10),
        font=dict(family="Segoe UI", size=11),
        coloraxis_showscale=True,
    )
    st.plotly_chart(fig_corr, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# TAB 4 — SIMULATEUR MANUEL
# ════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-title">🔮 Simulateur de Prédiction PM2.5</div>',
                unsafe_allow_html=True)
    st.markdown(
        "Entrez des conditions météo pour n'importe quelle ville "
        "(y compris hors dataset) et obtenez une prédiction PM2.5 instantanée.",
        unsafe_allow_html=False
    )

    s1, s2, s3 = st.columns([1, 1, 1])

    with s1:
        st.markdown("**🌡️ Température**")
        sim_temp_mean = st.slider("Température moyenne (°C)", 10.0, 45.0, 25.0, 0.5)
        sim_temp_max  = st.slider("Température max (°C)", 15.0, 50.0, 31.0, 0.5)
        sim_temp_min  = st.slider("Température min (°C)", 5.0,  35.0, 19.0, 0.5)
        sim_app_mean  = st.slider("Temp. ressentie (°C)", 5.0,  50.0, 24.0, 0.5)
        st.markdown("**🌍 Localisation**")
        sim_city   = st.selectbox("Ville", CITIES, key="sim_city",
                                   index=CITIES.index(selected_city))
        sim_lat    = st.number_input("Latitude", -5.0, 15.0,
                                     float(CITY_DICT[sim_city]['lat']), 0.01)
        sim_lon    = st.number_input("Longitude", 7.0, 17.0,
                                     float(CITY_DICT[sim_city]['lon']), 0.01)

    with s2:
        st.markdown("**🌧️ Précipitations & Vent**")
        sim_precip = st.slider("Précipitations (mm)", 0.0, 100.0, 0.0, 0.5)
        sim_rain   = st.slider("Pluie (mm)", 0.0, 100.0, 0.0, 0.5)
        sim_prec_h = st.slider("Heures de précip.", 0.0, 24.0, 0.0, 0.5)
        sim_wind   = st.slider("Vent max (km/h)", 0.0, 80.0, 12.0, 0.5)
        sim_gusts  = st.slider("Rafales (km/h)", 0.0, 100.0, 20.0, 0.5)
        st.markdown("**☀️ Rayonnement**")
        sim_rad    = st.slider("Rayonnement (MJ/m²)", 0.0, 30.0, 18.0, 0.5)
        sim_sun    = st.slider("Ensoleillement (h)", 0.0, 12.0, 8.0, 0.25)

    with s3:
        st.markdown("**🌫️ Poussière & Contexte**")
        sim_dust     = st.slider("Poussière Harmattan (µg/m³)", 0.0, 500.0, 10.0, 5.0)
        sim_month    = st.selectbox("Mois", range(1,13), format_func=lambda x:
                                    ['Jan','Fév','Mar','Avr','Mai','Juin',
                                     'Juil','Aoû','Sep','Oct','Nov','Déc'][x-1],
                                    index=0)
        sim_dry      = st.checkbox("Saison sèche (Harmattan)", value=sim_month in [11,12,1,2,3])
        st.markdown("**📅 Lags PM2.5 récents**")
        sim_pm25_lag1= st.slider("PM2.5 hier (lag 1j)", 0.0, 150.0, 15.0, 0.5)
        sim_pm25_lag3= st.slider("PM2.5 lag 3j", 0.0, 150.0, 15.0, 0.5)
        sim_pm25_lag7= st.slider("PM2.5 lag 7j", 0.0, 150.0, 15.0, 0.5)

    # Bouton prédire
    if st.button("🔮 Prédire le PM2.5", type="primary", use_container_width=True):
        sim_region  = CITY_DICT[sim_city]['region']
        day_of_year = datetime.date(2025, sim_month, 15).timetuple().tm_yday
        sun_sec     = sim_sun * 3600
        daylight    = 43000.0

        feat = {
            'city': sim_city, 'region': sim_region,
            'temperature_2m_mean'      : sim_temp_mean,
            'temperature_2m_max'       : sim_temp_max,
            'temperature_2m_min'       : sim_temp_min,
            'apparent_temperature_mean': sim_app_mean,
            'precipitation_sum'        : sim_precip,
            'rain_sum'                 : sim_rain,
            'precipitation_hours'      : sim_prec_h,
            'wind_speed_10m_max'       : sim_wind,
            'wind_gusts_10m_max'       : sim_gusts,
            'shortwave_radiation_sum'  : sim_rad,
            'sunshine_ratio'           : sun_sec / (daylight + 1e-6),
            'dust'                     : sim_dust,
            'temp_amplitude'           : sim_temp_max - sim_temp_min,
            'is_no_wind'               : 1 if sim_wind < 5 else 0,
            'is_no_rain'               : 1 if sim_precip < 0.1 else 0,
            'is_dry_season'            : 1 if sim_dry else 0,
            'month_sin'                : np.sin(2 * np.pi * sim_month / 12),
            'month_cos'                : np.cos(2 * np.pi * sim_month / 12),
            'day_of_year'              : day_of_year,
            'temp_lag1'                : sim_temp_mean,
            'temp_lag3'                : sim_temp_mean,
            'temp_lag7'                : sim_temp_mean,
            'wind_lag1'                : sim_wind,
            'wind_lag3'                : sim_wind,
            'dust_lag1'                : sim_dust,
            'dust_lag3'                : sim_dust,
            'dust_lag7'                : sim_dust,
            'temp_roll7'               : sim_temp_mean,
            'dust_roll7'               : sim_dust,
            'pm25_lag1'                : sim_pm25_lag1,
            'pm25_lag3'                : sim_pm25_lag3,
            'pm25_lag7'                : sim_pm25_lag7,
            'pm25_roll7'               : (sim_pm25_lag1+sim_pm25_lag3+sim_pm25_lag7)/3,
            'latitude'                 : sim_lat,
            'longitude'                : sim_lon,
        }

        pred = predict_pm25(model, meta, feat)
        lv, lc, lcss, ld = get_oms_level(pred)

        # Résultat
        st.markdown(f"""
        <div class="{lcss}" style="text-align:center; margin-top:1rem;">
          <div style="font-size:3rem; font-weight:800; color:{lc};">{pred} µg/m³</div>
          <div style="font-size:1.4rem; font-weight:700; margin:6px 0;">{lv}</div>
          <div style="font-size:0.95rem; color:#444;">{ld}</div>
          <hr style="margin:10px 0; border-color: rgba(0,0,0,0.1);">
          <div style="font-size:0.85rem; color:#666;">
            📍 <b>{sim_city}</b> ({sim_region}) · 
            🌡️ {sim_temp_mean}°C · 💨 {sim_wind} km/h · 
            🌫️ Dust: {sim_dust} µg/m³ ·
            🌧️ {sim_precip} mm
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Jauge
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=pred,
            delta={'reference': 15, 'valueformat': '.1f',
                   'increasing': {'color': RED_CM},
                   'decreasing': {'color': GREEN}},
            title={'text': f"PM2.5 — {sim_city}", 'font': {'size': 14}},
            number={'suffix': " µg/m³", 'font': {'size': 28}},
            gauge={
                'axis': {'range': [0, 120], 'tickwidth': 1},
                'bar': {'color': lc, 'thickness': 0.25},
                'steps': [
                    {'range': [0,  15], 'color': 'rgba(45,139,78,0.15)'},
                    {'range': [15, 35], 'color': 'rgba(244,166,35,0.15)'},
                    {'range': [35, 55], 'color': 'rgba(230,126,34,0.15)'},
                    {'range': [55,120], 'color': 'rgba(192,57,43,0.15)'},
                ],
                'threshold': {
                    'line': {'color': 'red', 'width': 3},
                    'thickness': 0.8, 'value': 55
                },
            }
        ))
        fig_gauge.update_layout(
            height=280, margin=dict(l=20, r=20, t=40, b=10),
            paper_bgcolor='white', font=dict(family="Segoe UI"),
        )
        st.plotly_chart(fig_gauge, use_container_width=True)


# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="footer">
  🌍 <b>Hackathon IndabaX Cameroon 2026</b> — L'IA au service de la résilience climatique et sanitaire<br>
  Modèle : XGBoost · R²=0.9074 · MAE=3.21 µg/m³ · Données : Open-Meteo (CAMS/Copernicus) · 40 villes · 10 régions
</div>
""", unsafe_allow_html=True)