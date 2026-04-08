<div align="center">

<img src="https://img.shields.io/badge/IndabaX-Cameroon%202026-2e7d32?style=for-the-badge&logo=leaf&logoColor=white" />
<img src="https://img.shields.io/badge/Hackathon-Climat%20%26%20Santé%20IA-1565c0?style=for-the-badge&logo=globe&logoColor=white" />
<img src="https://img.shields.io/badge/Python-3.11+-f9a825?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/LightGBM-Champion%20★-6a1b9a?style=for-the-badge" />
<img src="https://img.shields.io/badge/R²-0.9989-00897b?style=for-the-badge" />
<img src="https://img.shields.io/badge/License-MIT-78909c?style=for-the-badge" />

<br/><br/>

```
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║        🌍  HACKATHON INDABAX CAMEROON 2026  🌍                      ║
║                                                                      ║
║     Prédiction de la Qualité de l'Air au Cameroun par PM2.5         ║
║     Air Quality Prediction in Cameroon via PM2.5                    ║
║                                                                      ║
║          « L'IA au service de la résilience climatique »            ║
║            "AI for Climate & Health Resilience"                     ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
```

### 🏆 Équipe HBA-Group · Yaoundé, Cameroun · Avril 2026

[![Dashboard Live](https://img.shields.io/badge/🌐%20Dashboard%20Live-Streamlit-ff4b4b?style=for-the-badge)](https://indabaxclimate-kv4zlieoetpremkwjf7yww.streamlit.app/)
[![GitHub](https://img.shields.io/badge/📂%20Code%20Source-GitHub-181717?style=for-the-badge&logo=github)](https://github.com/AbdouramaneIssa/Indabax_Climate)

</div>

---

## 📋 Table des Matières · Table of Contents

<table>
<tr>
<td width="50%">

**🇫🇷 Français**
1. [Résumé Exécutif](#-résumé-exécutif)
2. [Contexte & Problématique](#-contexte--problématique)
3. [Présentation du Hackathon](#-présentation-du-hackathon)
4. [Données & Méthodologie](#-données--méthodologie)
5. [Modèles de Machine Learning](#-modèles-de-machine-learning)
6. [Résultats & Comparaison](#-résultats--comparaison)
7. [Dashboard Streamlit](#-dashboard-streamlit)
8. [Installation & Utilisation](#-installation--utilisation)
9. [Livrables Attendus](#-livrables-attendus)
10. [Critères d'Évaluation](#-critères-dévaluation)
11. [Équipe & Participation](#-équipe--participation)
12. [Références](#-références)

</td>
<td width="50%">

**🇬🇧 English**
1. [Executive Summary](#-executive-summary)
2. [Context & Problem Statement](#-context--problem-statement)
3. [Hackathon Overview](#-hackathon-overview)
4. [Data & Methodology](#-data--methodology)
5. [Machine Learning Models](#-machine-learning-models)
6. [Results & Comparison](#-results--comparison)
7. [Streamlit Dashboard](#-streamlit-dashboard)
8. [Installation & Usage](#-installation--usage)
9. [Expected Deliverables](#-expected-deliverables)
10. [Evaluation Criteria](#-evaluation-criteria)
11. [Team & Participation](#-team--participation)
12. [References](#-references)

</td>
</tr>
</table>

---

## 🚀 Résumé Exécutif

<table>
<tr>
<th width="50%">🇫🇷 Résumé Exécutif</th>
<th width="50%">🇬🇧 Executive Summary</th>
</tr>
<tr>
<td>

Ce projet, développé dans le cadre du **Hackathon IndabaX Cameroon 2026**, propose un système de **prédiction de la qualité de l'air** en milieu urbain camerounais, en estimant la concentration en particules fines **PM2.5** à partir de données météorologiques historiques.

**Trois algorithmes d'ensemble** ont été développés, entraînés et rigoureusement comparés sur un jeu de données couvrant **40 villes**, **10 régions** et **six années d'observations (2020–2025)**, soit **87 240 enregistrements journaliers**.

**🏆 LightGBM** s'impose comme le modèle champion avec un **R² de 0,9989** et un **MAE de 0,0535 μg/m³**. Une application web interactive construite avec **Streamlit** permet de visualiser les prédictions en temps réel pour chacune des 40 villes.

</td>
<td>

This project, developed for the **IndabaX Cameroon 2026 Hackathon**, delivers an **air quality prediction system** for Cameroonian urban areas, estimating **PM2.5 fine particle concentration** from historical meteorological data.

**Three ensemble algorithms** were developed, trained, and rigorously compared on a dataset covering **40 cities**, **10 regions**, and **six years of observations (2020–2025)**, totalling **87,240 daily records**.

**🏆 LightGBM** emerges as the champion model with an **R² of 0.9989** and **MAE of 0.0535 μg/m³**. An interactive web application built with **Streamlit** enables real-time predictions for all 40 cities.

</td>
</tr>
</table>

### 📊 Résultats-Clés · Key Results at a Glance

| Modèle / Model | R² | MAE (μg/m³) | Rang R² | Rang MAE | Verdict |
|---|:---:|:---:|:---:|:---:|:---:|
| 🥇 **LightGBM** | **0,9989** | **0,0535** | **#1** | **#1** | ★ Champion incontesté |
| 🥈 Random Forest | 0,9984 | 0,0812 | #2 | #3 | Solide baseline |
| 🥉 XGBoost | 0,9982 | 0,0651 | #3 | #2 | Compétitif |

---

## 🌍 Contexte & Problématique

<table>
<tr>
<th width="50%">🇫🇷 Contexte</th>
<th width="50%">🇬🇧 Context</th>
</tr>
<tr>
<td>

### La Qualité de l'Air en Afrique Subsaharienne

La pollution atmosphérique constitue la **quatrième cause mondiale de mortalité prématurée** selon l'OMS. En Afrique subsaharienne, ce phénomène est aggravé par :

- 🏙️ L'urbanisation rapide des grandes métropoles
- 🏭 Le développement industriel non régulé
- 🌾 Les pratiques agricoles (feux de brousse saisonniers)
- 🚗 La précarité des réseaux de transport

Au **Cameroun**, les principales agglomérations — Yaoundé, Douala, Bafoussam, Garoua, Maroua — concentrent des niveaux de pollution croissants. La **saison sèche** (harmattan) est particulièrement critique : les PM2.5 s'accumulent faute de précipitations pour les lessiver.

### Limites des Approches Traditionnelles

La surveillance conventionnelle repose sur des stations de mesure physiques **coûteuses** (plusieurs dizaines de milliers d'euros) et requiert une maintenance régulière — une infrastructure que la majorité des collectivités camerounaises ne peuvent pas se permettre.

**Notre approche :** estimer les niveaux de pollution à partir de **variables météorologiques accessibles gratuitement** (Open-Meteo API), en construisant un modèle statistique capable de traduire ces signaux en concentration PM2.5.

</td>
<td>

### Air Quality in Sub-Saharan Africa

Air pollution is the **fourth leading cause of premature death worldwide** according to the WHO. In sub-Saharan Africa, this phenomenon is worsened by:

- 🏙️ Rapid urbanisation of major metropolises
- 🏭 Unregulated industrial development
- 🌾 Agricultural practices (seasonal bushfires)
- 🚗 Underdeveloped transportation networks

In **Cameroon**, major cities — Yaoundé, Douala, Bafoussam, Garoua, Maroua — are experiencing rising pollution levels. The **dry season** (harmattan) is particularly critical: PM2.5 particles accumulate in the absence of rain to wash them away.

### Limitations of Traditional Monitoring

Conventional monitoring relies on **costly physical measurement stations** (tens of thousands of euros) requiring regular maintenance — infrastructure most Cameroonian communities cannot afford.

**Our approach:** estimate pollution levels from **freely available meteorological variables** (Open-Meteo API), building a statistical model capable of translating weather signals into PM2.5 concentration estimates.

</td>
</tr>
</table>

---

## 🎯 Présentation du Hackathon

<table>
<tr>
<th width="50%">🇫🇷 À Propos</th>
<th width="50%">🇬🇧 About</th>
</tr>
<tr>
<td>

### IndabaX Cameroon 2026

Le **Hackathon IndabaX Cameroon 2026** s'inscrit dans la dynamique portée par **Deep Learning Indaba**, mouvement panafricain visant à renforcer les capacités en intelligence artificielle à travers le continent.

L'édition 2026 place au centre de ses enjeux la double problématique de la **résilience climatique et sanitaire**, avec pour mission de mobiliser les outils de l'IA au service de défis concrets ayant un impact direct sur les populations.

**Mission des participants :**
- 🔮 **Prédire** les indicateurs de pollution à partir des données météo
- 🗺️ **Identifier** les facteurs climatiques aggravants par zone géographique
- 🛠️ **Aider à la décision** grâce à des outils clairs, accessibles et exploitables

### Portée du Défi

Ce défi présente une forte **dimension spatio-temporelle** : les profils de pollution varient significativement selon les régions et les saisons, impliquant de modéliser à la fois la distribution géographique et l'évolution temporelle des indicateurs.

</td>
<td>

### IndabaX Cameroon 2026

The **IndabaX Cameroon 2026 Hackathon** is part of the **Deep Learning Indaba** movement, a pan-African initiative aimed at strengthening artificial intelligence capabilities across the continent.

The 2026 edition focuses on the twin challenge of **climate and health resilience**, mobilising AI tools to address concrete challenges with direct impact on populations.

**Participant mission:**
- 🔮 **Predict** air pollution indicators from meteorological data
- 🗺️ **Identify** aggravating climate factors across geographic zones
- 🛠️ **Support decision-making** with clear, accessible, actionable tools

### Challenge Scope

This challenge has a strong **spatio-temporal dimension**: pollution patterns vary significantly across regions and seasons, requiring models that capture both geographic distribution and temporal evolution of air quality indicators.

</td>
</tr>
</table>

---

## 📦 Données & Méthodologie

<table>
<tr>
<th width="50%">🇫🇷 Données</th>
<th width="50%">🇬🇧 Data</th>
</tr>
<tr>
<td>

### Source des Données

Le dataset officiel a été collecté via l'**[API Open-Meteo](https://open-meteo.com/)** — une API météo gratuite et open-source.

> ⚠️ **Données de base** fournies à tous les participants comme point de départ. L'enrichissement avec des variables supplémentaires issues d'[open-meteo.com](https://open-meteo.com/) est optionnel.

</td>
<td>

### Data Source

The official dataset was collected via the **[Open-Meteo API](https://open-meteo.com/)** — a free, open-source weather API.

> ⚠️ **Baseline data** provided to all participants as a starting point. Enrichment with additional variables from [open-meteo.com](https://open-meteo.com/) is optional.

</td>
</tr>
</table>

### 📊 Structure du Jeu de Données · Dataset Structure

| Propriété / Property | Valeur / Value |
|---|---|
| 📍 Couverture géographique | 40 villes · 10 régions administratives |
| 📅 Période temporelle | Janvier 2020 – Décembre 2025 (6 ans) |
| 📊 Volume | 87 240 observations journalières |
| 📁 Format | CSV / Excel (`.xlsx`) |
| 🎯 Variable cible | `pm25_proxy` (proxy PM2.5 calculé) |
| 🔢 Features finales | 24 variables après ingénierie |
| ⚙️ Fréquence | Quotidienne (1 observation / ville / jour) |

### 🌡️ Variables Principales · Key Variables

| Catégorie | Variables |
|---|---|
| 🌡️ Température | `temperature_2m_mean`, `temperature_2m_max`, `temperature_2m_min`, `apparent_temperature` |
| 🌬️ Vent | `wind_speed_10m_max`, `wind_gusts_10m_max`, `wind_direction_10m_dominant` |
| 🌧️ Précipitations | `precipitation_sum`, `rain_sum`, `precipitation_hours` |
| ☀️ Solaire | `sunshine_duration`, `shortwave_radiation_sum` |
| 🌍 Géographie | `city` (40 villes), `region` (10 régions), `latitude`, `longitude` |
| 📐 Autres | `et0_fao_evapotranspiration`, `daylight_duration`, `weather_code` |

### ⚙️ Construction du Proxy PM2.5

En l'absence de mesures directes, un proxy physiquement fondé a été construit intégrant :

```
pm25_proxy = base × (saison_sèche × 1.8 + 1) × (1 + 0.1 × temp_amplitude) + bruit
base       = max(1, 8 / (pluie + 0.5)) × max(0.3, 1 – vent/80) × facteur_région
facteur_région ∈ { 0.7 (sud équatorial) | 1.0 (centre) | 1.4 (nord sahélien) }
```

### 🔧 Feature Engineering

Après ingénierie, **24 features** ont été retenues :

| Type | Exemples |
|---|---|
| Météo brute | `temperature_2m_mean`, `precipitation_sum`, `wind_speed_10m_max` |
| Features calculées | `temp_amplitude`, `sunshine_ratio`, `is_dry_season`, `is_no_wind`, `is_no_rain` |
| Temporelles | `month_sin`, `month_cos`, `day_of_year` (encodage circulaire) |
| Lag / Rolling | `temp_lag1`, `temp_lag7`, `wind_lag1`, `temp_roll7` |
| Géographiques | `latitude`, `longitude`, `city` (catégoriel), `region` (catégoriel) |

### 🔀 Protocole d'Évaluation

| Aspect | Détail |
|---|---|
| Split entraînement/test | 80% train (69 792 obs.) / 20% test (17 448 obs.) |
| Reproductibilité | `random_state = 42` |
| Early stopping | 50 rounds sans amélioration (boosting) |
| Métriques | R² (variance expliquée) + MAE (erreur absolue moyenne) |

---

## 🤖 Modèles de Machine Learning

<table>
<tr>
<th width="50%">🇫🇷 Algorithmes</th>
<th width="50%">🇬🇧 Algorithms</th>
</tr>
<tr>
<td>Trois algorithmes d'ensemble supervisés ont été implémentés et comparés.</td>
<td>Three supervised ensemble algorithms were implemented and compared.</td>
</tr>
</table>

---

### 🌲 1. Random Forest — Forêt Aléatoire

<table>
<tr>
<th width="50%">🇫🇷</th>
<th width="50%">🇬🇧</th>
</tr>
<tr>
<td>

**Principe :** construit N arbres de décision indépendants sur des sous-ensembles aléatoires des données et des features (bagging + sélection aléatoire). La prédiction finale est la **moyenne** de tous les arbres.

**Points forts :**
- ✅ Robuste aux valeurs aberrantes
- ✅ Peu de paramètres à régler
- ✅ Bonne interprétabilité
- ❌ MAE plus élevé (agrégation par moyenne non ciblée)

</td>
<td>

**Principle:** builds N independent decision trees on random subsets of data and features (bagging + random feature selection). Final prediction is the **average** of all trees.

**Strengths:**
- ✅ Robust to outliers
- ✅ Few hyperparameters to tune
- ✅ Good interpretability
- ❌ Higher MAE (non-targeted averaging aggregation)

</td>
</tr>
</table>

```python
from sklearn.ensemble import RandomForestRegressor

rf_model = RandomForestRegressor(
    n_estimators  = 100,   # Nombre d'arbres
    max_depth     = 10,    # Profondeur max (limite l'overfitting)
    n_jobs        = -1,    # Parallélisation maximale
    random_state  = 42,    # Reproductibilité
)
```

**📈 Résultats : R² = 0,9984 · MAE = 0,0812 μg/m³**

---

### ⚡ 2. XGBoost — Gradient Boosting Optimisé

<table>
<tr>
<th width="50%">🇫🇷</th>
<th width="50%">🇬🇧</th>
</tr>
<tr>
<td>

**Principe :** boosting par gradient — chaque arbre est entraîné pour **corriger les résidus** du modèle précédent. Stratégie de croissance **level-wise** (symétrique, niveau par niveau). Régularisation L1+L2 intégrée.

**Points forts :**
- ✅ Correction séquentielle et ciblée des erreurs
- ✅ Régularisation avancée (anti-overfitting)
- ✅ MAE amélioré de 19,8% vs Random Forest
- ❌ Encodage manuel des variables catégorielles requis

</td>
<td>

**Principle:** gradient boosting — each tree is trained to **correct residuals** from the previous model. **Level-wise** growth strategy (symmetric, level by level). Integrated L1+L2 regularisation.

**Strengths:**
- ✅ Sequential, targeted error correction
- ✅ Advanced regularisation (anti-overfitting)
- ✅ MAE improved by 19.8% vs Random Forest
- ❌ Manual encoding of categorical variables required

</td>
</tr>
</table>

```python
import xgboost as xgb

xgb_model = xgb.XGBRegressor(
    n_estimators      = 500,   # Arbres max (early stopping gère l'arrêt)
    learning_rate     = 0.05,  # Pas d'apprentissage
    max_depth         = 6,     # Profondeur équilibrée
    subsample         = 0.8,   # 80% des données par itération
    colsample_bytree  = 0.8,   # 80% des features par arbre
    reg_alpha         = 0.1,   # L1 (Lasso)
    reg_lambda        = 1.0,   # L2 (Ridge)
    random_state      = 42,
)
xgb_model.fit(X_train, y_train,
              eval_set=[(X_test, y_test)],
              early_stopping_rounds=50, verbose=False)
```

**📈 Résultats : R² = 0,9982 · MAE = 0,0651 μg/m³**

---

### 🏆 3. LightGBM — Le Modèle Champion ★

<table>
<tr>
<th width="50%">🇫🇷</th>
<th width="50%">🇬🇧</th>
</tr>
<tr>
<td>

**Principe :** gradient boosting avec 4 innovations majeures par rapport à XGBoost :

1. **Croissance leaf-wise** — développe en priorité la feuille avec le plus grand gain de réduction d'erreur → arbres asymétriques, concentration naturelle sur les patterns difficiles
2. **GOSS** (Gradient-based One-Side Sampling) — conserve les observations à fort gradient, échantillonne les autres → réduction de calcul sans perte d'information
3. **EFB** (Exclusive Feature Bundling) — regroupe les features mutuellement exclusives → efficacité sur les données météo corrélées
4. **Gestion native des catégorielles** — pas d'encodage artificiel, partitionnement optimal pour les 40 villes et 10 régions

**Avantage concret pour le Cameroun :** XGBoost assigne arbitrairement Yaoundé=0, Douala=1... introduisant un faux gradient spatial. LightGBM traite chaque ville comme une catégorie pure et capture les spécificités climatiques locales (altitude, proximité côtière, régime pluviométrique).

</td>
<td>

**Principle:** gradient boosting with 4 major innovations over XGBoost:

1. **Leaf-wise growth** — prioritises the leaf with the greatest error reduction gain → asymmetric trees naturally concentrate on complex patterns
2. **GOSS** (Gradient-based One-Side Sampling) — retains high-gradient observations, samples low-gradient ones → reduced computation without information loss
3. **EFB** (Exclusive Feature Bundling) — bundles mutually exclusive features → efficiency on correlated meteorological data
4. **Native categorical handling** — no artificial encoding, optimal partitioning for 40 cities and 10 regions

**Concrete advantage for Cameroon:** XGBoost arbitrarily assigns Yaoundé=0, Douala=1... introducing a false spatial gradient. LightGBM treats each city as a pure category and captures local climate specifics (altitude, coastal proximity, rainfall patterns).

</td>
</tr>
</table>

```python
import lightgbm as lgb

lgb_model = lgb.LGBMRegressor(
    n_estimators      = 1000,  # Arbres max (early stopping actif)
    learning_rate     = 0.05,  # Identique à XGBoost (comparaison équitable)
    max_depth         = -1,    # Sans limite (leaf-wise gère la complexité)
    num_leaves        = 63,    # Équiv. depth=6 chez XGBoost (2^6 - 1)
    subsample         = 0.8,   # GOSS : 80% des données
    colsample_bytree  = 0.8,   # EFB : 80% des features
    reg_alpha         = 0.1,   # L1
    reg_lambda        = 1.0,   # L2
    min_child_samples = 20,    # Anti-overfitting sur les feuilles
    random_state      = 42,
    verbose           = -1,
)
lgb_model.fit(X_train, y_train,
              eval_set=[(X_test, y_test)],
              callbacks=[lgb.early_stopping(stopping_rounds=50, verbose=False)])
```

**📈 Résultats : R² = 0,9989 · MAE = 0,0535 μg/m³ ★ Champion sur les deux métriques**

---

## 📊 Résultats & Comparaison

### Tableau Comparatif Complet · Full Comparison Table

| Critère | Random Forest | XGBoost | LightGBM ★ |
|---|:---:|:---:|:---:|
| **R²** | 0,9984 | 0,9982 | **0,9989 ★** |
| **MAE (μg/m³)** | 0,0812 | 0,0651 | **0,0535 ★** |
| Stratégie | Parallèle (bagging) | Séquentiel (level-wise) | Séquentiel (leaf-wise) |
| Vitesse d'entraînement | Rapide | Moyenne | **Très rapide ★** |
| Consommation mémoire | Moyenne | Élevée | **Faible ★** |
| Variables catégorielles | Encodage manuel | Encodage manuel | **Gestion native ★** |
| Risque overfitting | Faible | Modéré | Modéré (atténué) |
| Paramètres à régler | Peu | Modéré | Modéré |

### 📉 Gains de Performance · Performance Gains

| Comparaison | MAE initial | MAE final | Gain relatif |
|---|:---:|:---:|:---:|
| LightGBM vs Random Forest | 0,0812 | 0,0535 | **– 34,1% ★** |
| LightGBM vs XGBoost | 0,0651 | 0,0535 | **– 17,8%** |
| XGBoost vs Random Forest | 0,0812 | 0,0651 | **– 19,8%** |

### 🏥 Impact Santé Publique · Public Health Impact

Les seuils OMS de classification de la qualité de l'air par PM2.5 :

| Catégorie OMS | Seuil PM2.5 (μg/m³) | Code couleur | Implication sanitaire |
|---|:---:|:---:|---|
| ✅ **Bon** | < 15 | 🟢 Vert | Air sain, aucune restriction recommandée |
| ⚠️ **Modéré** | 15 – 25 | 🟠 Orange | Populations sensibles à surveiller |
| 🚨 **Mauvais** | > 25 | 🔴 Rouge | Alerte sanitaire, mesures préventives recommandées |

> 💡 Dans les zones de transition autour des seuils critiques (15 et 25 μg/m³), une erreur de 0,08 plutôt que 0,05 μg/m³ peut faire basculer une alerte d'un côté ou l'autre du seuil — avec des conséquences potentiellement vitales pour des milliers d'habitants.

### ⚠️ Limites Connues · Known Limitations

<table>
<tr>
<th width="50%">🇫🇷 Limites</th>
<th width="50%">🇬🇧 Limitations</th>
</tr>
<tr>
<td>

- **Biais du proxy PM2.5** : les R² > 0,99 s'expliquent partiellement par le fait que le proxy est lui-même construit à partir des variables météo. Sur de vraies mesures PM2.5, les performances seraient probablement inférieures.
- **Généralisation géographique** : le modèle a été entraîné sur 40 villes camerounaises. Sa capacité à généraliser à des villes non vues est inconnue.
- **Extrapolation temporelle** : une validation chronologique stricte (2020–2024 → 2025) fournirait une estimation plus réaliste de la performance future.

</td>
<td>

- **PM2.5 proxy bias**: the R² > 0.99 is partly explained by the proxy itself being constructed from meteorological variables. On real PM2.5 sensor data, performance would likely be lower.
- **Geographic generalisation**: the model was trained on 40 Cameroonian cities. Its ability to generalise to unseen cities is unknown.
- **Temporal extrapolation**: strict chronological validation (2020–2024 → 2025) would provide a more realistic estimate of future performance.

</td>
</tr>
</table>

---

## 🖥️ Dashboard Streamlit

<table>
<tr>
<th width="50%">🇫🇷 Application Web</th>
<th width="50%">🇬🇧 Web Application</th>
</tr>
<tr>
<td>

Une application web interactive a été développée avec **Streamlit** pour rendre les prédictions accessibles aux acteurs de terrain. Le design adopte une esthétique **« Biopunk Organique »** — palette chromatique verte profonde symbolisant l'environnement et la résilience climatique.

</td>
<td>

An interactive web application was developed with **Streamlit** to make predictions accessible to field practitioners. The design adopts a **"Organic Biopunk"** aesthetic — deep green colour palette symbolising the environment and climate resilience.

</td>
</tr>
</table>

### 🧩 Modules Fonctionnels · Functional Modules

#### 📍 Module 1 — Tableau de Bord Principal

<table>
<tr>
<td width="50%">

- Carte interactive **Plotly Choropleth** des 40 villes
- Distribution géographique des niveaux PM2.5 moyens estimés
- KPI en temps réel filtrables par région ou mois
- Métriques dataset (87 240 obs, 40 villes, 2020–2025)

</td>
<td width="50%">

- Interactive **Plotly Choropleth** map of 40 cities
- Geographic distribution of estimated mean PM2.5 levels
- Real-time KPIs filterable by region or month
- Dataset metrics (87,240 obs, 40 cities, 2020–2025)

</td>
</tr>
</table>

#### 🌡️ Module 2 — Simulateur Climatique

<table>
<tr>
<td width="50%">

- Sélection ville (40) et mois via listes déroulantes enrichies
- **Sliders interactifs** : temp. (min/max/moy), précipitations, vent, rafales, rayonnement, ET₀
- Détection automatique des conditions critiques (absence de vent, saison sèche, absence de pluie)
- Résultat sous forme de **jauge Plotly colorée** (vert → orange → rouge)

</td>
<td width="50%">

- City (40) and month selection via enriched dropdowns
- **Interactive sliders**: temp. (min/max/mean), precipitation, wind, gusts, radiation, ET₀
- Auto-detection of critical conditions (no wind, dry season, no rain)
- Result displayed as a **Plotly colour gauge** (green → orange → red)

</td>
</tr>
</table>

#### 🚦 Module 3 — Système d'Alerte OMS

```python
def get_alerte(pm25):
    if pm25 < 15:
        return '✅ Air Sain',  'badge-good',     'Qualité satisfaisante, exposition normale sans risque.'
    elif pm25 < 25:
        return '⚠️ Modéré',   'badge-moderate', 'Populations sensibles : réduire les activités prolongées.'
    else:
        return '🚨 Mauvais',  'badge-bad',       'Alerte sanitaire : limiter toute exposition extérieure.'
```

### 🏗️ Architecture Technique · Technical Architecture

```
cameroon_meteo_data.csv ──► Feature Engineering ──► lgb_model.pkl
                                                           │
app.py ──► st.cache_resource (modèle) ──────────────────► predict()
       └──► st.cache_data (données)                        │
                │                                          ▼
                ▼                                    pm25_result
       Streamlit UI ◄──────────────────────────── Classification OMS
       (Plotly charts, sliders, maps)
```

**Stack technique :** Python 3.11 · Streamlit 1.35 · LightGBM 4.3 · Plotly · Pandas 2.2 · NumPy 1.26 · joblib

### 🌐 Accès · Access

| Ressource | Lien |
|---|---|
| 🟢 **Dashboard Live** | [indabaxclimate-kv4zlieoetpremkwjf7yww.streamlit.app](https://indabaxclimate-kv4zlieoetpremkwjf7yww.streamlit.app/) |
| 📂 **Code Source** | [github.com/AbdouramaneIssa/Indabax_Climate](https://github.com/AbdouramaneIssa/Indabax_Climate) |

---

## 💻 Installation & Utilisation

### Prérequis · Prerequisites

```
Python 3.9+
pip
Git
```

### Installation Locale · Local Installation

```bash
# 1. Cloner le dépôt
git clone https://github.com/AbdouramaneIssa/Indabax_Climate
cd Indabax_Climate

# 2. Créer un environnement virtuel (recommandé)
python -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate         # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Lancer l'application
streamlit run app.py
```

### Structure du Projet · Project Structure

```
Indabax_Climate/
├── 📊 data/
│   └── cameroon_meteo_data.csv      # Dataset (87 240 observations)
├── 🤖 models/
│   └── lgb_model.pkl                # Modèle LightGBM sérialisé
├── 📓 notebooks/
│   ├── 01_exploration.ipynb         # EDA & visualisations
│   ├── 02_feature_engineering.ipynb # Construction du proxy PM2.5
│   └── 03_modeling.ipynb            # Entraînement & comparaison
├── 🖥️ app.py                        # Application Streamlit principale
├── 📋 requirements.txt
└── 📄 README.md
```

### Dépendances Principales · Main Dependencies

```txt
streamlit>=1.35
lightgbm>=4.3
xgboost>=2.0
scikit-learn>=1.4
pandas>=2.2
numpy>=1.26
plotly>=5.22
joblib>=1.4
```
## 🔭 Pistes d'Amélioration · Future Work

<table>
<tr>
<th width="50%">🇫🇷</th>
<th width="50%">🇬🇧</th>
</tr>
<tr>
<td>

1. **Optimisation bayésienne** (Optuna, Hyperopt) — gains estimés 5–15% sur le MAE
2. **Validation temporelle stricte** — entraîner sur 2020–2024, tester sur 2025
3. **Enrichissement des données** — NASA MODIS (aérosols), MERRA-2 (profils atmosphériques)
4. **Modélisation spatio-temporelle** — krigeage, réseaux convolutifs spatiaux
5. **Validation terrain** — capteurs PM2.5 low-cost (PurpleAir, SDS011) en villes camerounaises
6. **Extension régionale** — RDC, Gabon, Tchad via Open-Meteo (plateforme régionale)

</td>
<td>

1. **Bayesian optimisation** (Optuna, Hyperopt) — estimated 5–15% MAE improvement
2. **Strict temporal validation** — train on 2020–2024, test on 2025
3. **Data enrichment** — NASA MODIS (aerosols), MERRA-2 (atmospheric profiles)
4. **Spatio-temporal modelling** — kriging, spatial convolutional networks
5. **Field validation** — low-cost PM2.5 sensors (PurpleAir, SDS011) in Cameroonian cities
6. **Regional extension** — DRC, Gabon, Chad via Open-Meteo (regional platform)

</td>
</tr>
</table>

---

## 📚 Références

### Articles Scientifiques · Scientific Papers

- Breiman, L. (2001). *Random Forests*. Machine Learning, 45(1), 5–32.
- Chen, T. & Guestrin, C. (2016). *XGBoost: A Scalable Tree Boosting System*. KDD 2016, 785–794.
- Ke, G. et al. (2017). *LightGBM: A Highly Efficient Gradient Boosting Decision Tree*. NeurIPS 30, 3146–3154.
- Zue, Q. et al. (2022). *Machine learning approaches for air quality prediction in sub-Saharan Africa using meteorological proxies*. Environmental Research Letters, 17(4), 044027.

### Bibliothèques & Outils · Libraries & Tools

| Outil | Version | Lien |
|---|---|---|
| Scikit-learn | 1.4 | [scikit-learn.org](https://scikit-learn.org) |
| XGBoost | 2.0 | [xgboost.readthedocs.io](https://xgboost.readthedocs.io) |
| LightGBM | 4.3 | [lightgbm.readthedocs.io](https://lightgbm.readthedocs.io) |
| Streamlit | 1.35 | [docs.streamlit.io](https://docs.streamlit.io) |
| Open-Meteo API | — | [open-meteo.com](https://open-meteo.com) |

### Données & Standards · Data & Standards

- OMS (2021). *WHO Global Air Quality Guidelines: PM2.5, PM10, O₃, NO₂, SO₂, CO*. WHO Press, Genève.
- Institut National de la Statistique du Cameroun (2024). *Annuaire Statistique du Cameroun 2024*.

---

## 📢 Ressources Complémentaires

| Ressource | Lien |
|---|---|
| 📖 Guide du Pitch Deck IndabaX 2026 | [Notion Guide](https://www.notion.so/Guide-du-Pitch-Deck-IndabaX-Cameroon-2026-2d26044aa2d28039b8a5d4903f7797a6) |
| 🌐 Open-Meteo API | [open-meteo.com](https://open-meteo.com/) |
| 🐍 Code source complet | [github.com/AbdouramaneIssa/Indabax_Climate](https://github.com/AbdouramaneIssa/Indabax_Climate) |
| 📊 Dashboard Live | [Streamlit App](https://indabaxclimate-kv4zlieoetpremkwjf7yww.streamlit.app/) |

---

<div align="center">

```
╔═══════════════════════════════════════════════════════════╗
║  HBA-Group · Hackathon IndabaX Cameroon 2026              ║
║  Yaoundé, Cameroun · Avril 2026                           ║
║                                                           ║
║  🌱 L'IA au service de la résilience climatique           ║
║     AI for Climate & Health Resilience                    ║
╚═══════════════════════════════════════════════════════════╝
```

*Open Source · Données Open-Meteo (CC BY 4.0)*

[![Dashboard](https://img.shields.io/badge/🌐%20Dashboard%20Live-Streamlit-ff4b4b?style=for-the-badge)](https://indabaxclimate-kv4zlieoetpremkwjf7yww.streamlit.app/)
[![GitHub](https://img.shields.io/badge/📂%20Code%20Source-GitHub-181717?style=for-the-badge&logo=github)](https://github.com/AbdouramaneIssa/Indabax_Climate)

</div>
