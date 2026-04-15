import streamlit as st
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# PAGE CONFIG  (must be FIRST streamlit call)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Verde ML Dashboard",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# GLOBAL CSS – dark green theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Fonts ──────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Root variables ─────────────────────── */
:root {
  --verde-dark:   #0a2e1a;
  --verde-mid:    #145a32;
  --verde-main:   #1e8449;
  --verde-light:  #27ae60;
  --verde-pale:   #a9dfbf;
  --verde-mint:   #d5f5e3;
  --verde-glow:   #2ecc71;
  --bg-card:      #0f1e14;
  --bg-panel:     #111f16;
  --text-white:   #f0faf4;
  --text-muted:   #7fb894;
  --border:       #1e5c34;
  --accent-gold:  #f1c40f;
  --accent-teal:  #1abc9c;
}

/* ── Global background ──────────────────── */
html, body, [data-testid="stAppViewContainer"],
[data-testid="stMain"] {
  background: linear-gradient(135deg, #060e08 0%, #0a2e1a 50%, #060e08 100%) !important;
  font-family: 'Inter', sans-serif !important;
  color: var(--text-white) !important;
}

/* ── Sidebar ────────────────────────────── */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #071510 0%, #0d2b18 100%) !important;
  border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text-white) !important; }
[data-testid="stSidebar"] .stRadio > label,
[data-testid="stSidebar"] .stSelectbox > label,
[data-testid="stSidebar"] .stTextInput > label { color: var(--verde-pale) !important; font-weight: 600 !important; }

/* ── Headings ───────────────────────────── */
h1, h2, h3, h4 { color: var(--text-white) !important; font-family: 'Inter', sans-serif !important; }

/* ── Metric cards ───────────────────────── */
[data-testid="stMetric"] {
  background: linear-gradient(135deg, var(--bg-card), #162a1e) !important;
  border: 1px solid var(--border) !important;
  border-radius: 14px !important;
  padding: 18px !important;
  box-shadow: 0 4px 20px rgba(46,204,113,0.08) !important;
}
[data-testid="stMetricLabel"] { color: var(--text-muted) !important; font-size: 0.82rem !important; }
[data-testid="stMetricValue"] { color: var(--verde-glow) !important; font-weight: 700 !important; }
[data-testid="stMetricDelta"] { color: var(--accent-teal) !important; }

/* ── Buttons ────────────────────────────── */
.stButton > button {
  background: linear-gradient(135deg, var(--verde-main), var(--verde-light)) !important;
  color: white !important;
  border: none !important;
  border-radius: 10px !important;
  padding: 10px 24px !important;
  font-weight: 600 !important;
  font-size: 0.9rem !important;
  letter-spacing: 0.5px !important;
  transition: all 0.25s ease !important;
  box-shadow: 0 4px 15px rgba(30,132,73,0.4) !important;
}
.stButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 6px 22px rgba(46,204,113,0.5) !important;
  background: linear-gradient(135deg, var(--verde-light), var(--verde-glow)) !important;
}

/* ── Inputs ─────────────────────────────── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div > div {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 8px !important;
  color: var(--text-white) !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
  border-color: var(--verde-glow) !important;
  box-shadow: 0 0 0 2px rgba(46,204,113,0.2) !important;
}

/* ── Select / Radio ─────────────────────── */
.stSelectbox > div > div,
.stMultiSelect > div > div {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 8px !important;
  color: var(--text-white) !important;
}
.stRadio > div { gap: 8px !important; }
.stRadio > div > label {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 8px !important;
  padding: 8px 14px !important;
  color: var(--text-white) !important;
  transition: border-color 0.2s !important;
}
.stRadio > div > label:hover { border-color: var(--verde-glow) !important; }

/* ── Tabs ───────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
  background: var(--bg-panel) !important;
  border-radius: 12px !important;
  padding: 4px !important;
  gap: 4px !important;
  border-bottom: none !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  border-radius: 9px !important;
  color: var(--text-muted) !important;
  font-weight: 500 !important;
  padding: 8px 18px !important;
  transition: all 0.2s !important;
}
.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg, var(--verde-main), var(--verde-light)) !important;
  color: white !important;
  font-weight: 700 !important;
  box-shadow: 0 2px 12px rgba(30,132,73,0.4) !important;
}

/* ── Dataframe ──────────────────────────── */
[data-testid="stDataFrame"] { border-radius: 10px !important; overflow: hidden !important; }

/* ── Dividers ───────────────────────────── */
hr { border-color: var(--border) !important; opacity: 0.5 !important; }

/* ── Alerts ─────────────────────────────── */
.stAlert { border-radius: 10px !important; }
[data-testid="stAlert"] { background: rgba(30,132,73,0.15) !important; border-left: 3px solid var(--verde-glow) !important; }

/* ── Progress bar ───────────────────────── */
.stProgress > div > div > div {
  background: linear-gradient(90deg, var(--verde-main), var(--verde-glow)) !important;
  border-radius: 99px !important;
}

/* ── Custom card util ───────────────────── */
.verde-card {
  background: linear-gradient(135deg, #0d2318, #111f16);
  border: 1px solid #1e5c34;
  border-radius: 16px;
  padding: 24px;
  margin: 10px 0;
  box-shadow: 0 4px 24px rgba(46,204,113,0.07);
}
.verde-card-glow {
  background: linear-gradient(135deg, #0d2318, #111f16);
  border: 1px solid #27ae60;
  border-radius: 16px;
  padding: 24px;
  margin: 10px 0;
  box-shadow: 0 0 30px rgba(39,174,96,0.15);
}
.badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 99px;
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.5px;
}
.badge-green { background: rgba(46,204,113,0.2); color: #2ecc71; border: 1px solid rgba(46,204,113,0.4); }
.badge-teal  { background: rgba(26,188,156,0.2); color: #1abc9c; border: 1px solid rgba(26,188,156,0.4); }
.badge-gold  { background: rgba(241,196,15,0.2);  color: #f1c40f;  border: 1px solid rgba(241,196,15,0.4);  }
.badge-red   { background: rgba(231,76,60,0.2);   color: #e74c3c;  border: 1px solid rgba(231,76,60,0.4);  }

.section-title {
  font-size: 1.6rem;
  font-weight: 800;
  color: #f0faf4;
  margin-bottom: 6px;
  letter-spacing: -0.3px;
}
.section-sub {
  font-size: 0.92rem;
  color: #7fb894;
  margin-bottom: 24px;
}
.prediction-result {
  background: linear-gradient(135deg, #0a2e1a, #145a32);
  border: 2px solid #27ae60;
  border-radius: 20px;
  padding: 32px;
  text-align: center;
  box-shadow: 0 0 40px rgba(39,174,96,0.25);
  margin-top: 20px;
}
.prediction-value {
  font-size: 3.5rem;
  font-weight: 800;
  color: #2ecc71;
  line-height: 1;
}
.prediction-label {
  font-size: 1rem;
  color: #a9dfbf;
  margin-top: 8px;
}
.status-dot {
  display: inline-block;
  width: 10px; height: 10px;
  border-radius: 50%;
  margin-right: 6px;
}
.dot-green  { background: #2ecc71; box-shadow: 0 0 8px #2ecc71; }
.dot-red    { background: #e74c3c; box-shadow: 0 0 8px #e74c3c; }
.dot-yellow { background: #f1c40f; box-shadow: 0 0 8px #f1c40f; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────
if "connected" not in st.session_state:
    st.session_state.connected = False
if "engine" not in st.session_state:
    st.session_state.engine = None
if "models_trained" not in st.session_state:
    st.session_state.models_trained = False


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 20px 0 10px;'>
      <div style='font-size:3rem;'>🌿</div>
      <div style='font-size:1.3rem; font-weight:800; color:#2ecc71; letter-spacing:-0.5px;'>Verde ML</div>
      <div style='font-size:0.78rem; color:#7fb894; margin-top:4px;'>Intelligence Dashboard</div>
    </div>
    <hr style='border-color:#1e5c34; margin: 10px 0 20px;'/>
    """, unsafe_allow_html=True)

    nav = st.radio(
        "Navigation",
        ["🔌 Database Connection",
         "📊 Clustering",
         "🎯 Classification",
         "📈 Regression",
         "⏱️ Time Series",
         "🔮 Manual Prediction"],
        label_visibility="collapsed"
    )

    st.markdown("<hr style='border-color:#1e5c34;'/>", unsafe_allow_html=True)

    # Connection status
    if st.session_state.connected:
        st.markdown("""
        <div style='background:rgba(46,204,113,0.1); border:1px solid #27ae60;
                    border-radius:10px; padding:12px; text-align:center;'>
          <span class="status-dot dot-green"></span>
          <span style='color:#2ecc71; font-weight:600; font-size:0.85rem;'>Connected</span><br/>
          <span style='color:#7fb894; font-size:0.75rem;'>Verde_DW</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='background:rgba(231,76,60,0.1); border:1px solid #e74c3c;
                    border-radius:10px; padding:12px; text-align:center;'>
          <span class="status-dot dot-red"></span>
          <span style='color:#e74c3c; font-weight:600; font-size:0.85rem;'>Not Connected</span><br/>
          <span style='color:#7fb894; font-size:0.75rem;'>Go to DB Connection</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.7rem; color:#3d6b4f; text-align:center;'>
      Verde DW  •  ML Finale Project<br/>
      DBSCAN · KMeans · RF · GB · XGBoost · ARIMA
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HELPER: connect to SQL Server
# ─────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def make_engine_windows(server, database):
    from sqlalchemy import create_engine
    from urllib.parse import quote_plus
    cs = (f"DRIVER={{ODBC Driver 17 for SQL Server}};"
          f"SERVER={server};DATABASE={database};"
          "Trusted_Connection=yes;TrustServerCertificate=yes;")
    return create_engine(f"mssql+pyodbc:///?odbc_connect={quote_plus(cs)}")

@st.cache_resource(show_spinner=False)
def make_engine_sql(server, database, username, password):
    from sqlalchemy import create_engine
    from urllib.parse import quote_plus
    cs = (f"DRIVER={{ODBC Driver 17 for SQL Server}};"
          f"SERVER={server};DATABASE={database};"
          f"UID={username};PWD={password};TrustServerCertificate=yes;")
    return create_engine(f"mssql+pyodbc:///?odbc_connect={quote_plus(cs)}")


# ─────────────────────────────────────────────
# PAGE: DATABASE CONNECTION
# ─────────────────────────────────────────────
if nav == "🔌 Database Connection":
    st.markdown("""
    <div class='section-title'>🔌 Database Connection</div>
    <div class='section-sub'>Connect to your SQL Server Management Studio (SSMS) instance</div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown("<div class='verde-card-glow'>", unsafe_allow_html=True)
        st.markdown("### ⚙️ Connection Settings")

        auth_mode = st.radio(
            "Authentication Mode",
            ["🪟 Windows Authentication", "🔐 SQL Server Authentication"],
            horizontal=True
        )

        server = st.text_input("Server Name / IP", value="localhost",
                               placeholder="e.g. localhost, 192.168.1.1\\SQLEXPRESS")
        database = st.text_input("Database Name", value="Verde_DW",
                                 placeholder="e.g. Verde_DW")

        if auth_mode == "🔐 SQL Server Authentication":
            username = st.text_input("Username", placeholder="sa")
            password = st.text_input("Password", type="password", placeholder="••••••••")
        else:
            username = password = None
            st.info("🪟 Windows Authentication uses your current Windows session credentials — no username/password needed.")

        connect_btn = st.button("⚡ Connect to Database", use_container_width=True)

        if connect_btn:
            with st.spinner("Establishing connection…"):
                try:
                    if auth_mode == "🪟 Windows Authentication":
                        engine = make_engine_windows(server, database)
                    else:
                        if not username or not password:
                            st.error("Please enter both username and password.")
                            st.stop()
                        engine = make_engine_sql(server, database, username, password)

                    # test connection
                    with engine.connect() as conn:
                        from sqlalchemy import text as sqlt
                        conn.execute(sqlt("SELECT 1"))

                    st.session_state.engine = engine
                    st.session_state.connected = True
                    st.success("✅ Successfully connected!")
                except Exception as e:
                    st.error(f"❌ Connection failed: {e}")
                    st.session_state.connected = False

        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown("<div class='verde-card'>", unsafe_allow_html=True)
        st.markdown("### 📋 Connection Guide")
        st.markdown("""
**Windows Authentication** (Recommended for SSMS users)
- Uses your Windows login — no credentials needed
- Works when both app and SQL Server are on the same machine or domain

**SQL Server Authentication**
- Uses a SQL login (username + password)
- Must be enabled in SQL Server properties

**Common Server Names**
| Setup | Server Name |
|-------|-------------|
| Default local instance | `localhost` |
| Named instance | `localhost\\SQLEXPRESS` |
| Remote server | `192.168.x.x` |

**Requirements**
- ODBC Driver 17 for SQL Server installed
- SQL Server running and accessible
- Database `Verde_DW` exists with all dimension/fact tables
        """)
        st.markdown("</div>", unsafe_allow_html=True)

        if st.session_state.connected:
            st.markdown("<div class='verde-card-glow' style='margin-top:16px;'>", unsafe_allow_html=True)
            st.markdown("### 🗂️ Database Tables")
            try:
                engine = st.session_state.engine
                tables_query = """
                SELECT TABLE_NAME,
                       (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS c
                        WHERE c.TABLE_NAME = t.TABLE_NAME) AS col_count
                FROM INFORMATION_SCHEMA.TABLES t
                WHERE TABLE_TYPE = 'BASE TABLE'
                ORDER BY TABLE_NAME
                """
                from sqlalchemy import text as sqlt
                with engine.connect() as conn:
                    tables_df = pd.read_sql(sqlt(tables_query), conn)
                st.dataframe(tables_df, use_container_width=True, hide_index=True)
            except Exception as e:
                st.warning(f"Could not fetch table list: {e}")
            st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# REQUIRE CONNECTION helper
# ─────────────────────────────────────────────
def require_connection():
    if not st.session_state.connected:
        st.markdown("""
        <div style='background:rgba(231,76,60,0.1); border:1.5px solid #e74c3c;
                    border-radius:16px; padding:32px; text-align:center; margin-top:30px;'>
          <div style='font-size:2.5rem;'>🔌</div>
          <div style='color:#e74c3c; font-size:1.3rem; font-weight:700; margin:10px 0 6px;'>
            Not Connected
          </div>
          <div style='color:#7fb894;'>Please connect to your database first via the
          <strong style="color:#2ecc71;">Database Connection</strong> page.</div>
        </div>
        """, unsafe_allow_html=True)
        return False
    return True


# ─────────────────────────────────────────────
# DATA LOADING (cached per engine)
# ─────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_all_data(_engine):
    import pandas as pd
    fact = pd.read_sql("SELECT * FROM dbo.FactTransaction", _engine)
    dim_prod = pd.read_sql("SELECT * FROM dbo.DimProduit", _engine)
    dim_part = pd.read_sql("SELECT * FROM dbo.DimPartner", _engine)
    dim_date = pd.read_sql("SELECT * FROM dbo.DimDate", _engine)
    return fact, dim_prod, dim_part, dim_date


# ─────────────────────────────────────────────
# PAGE: CLUSTERING
# ─────────────────────────────────────────────
if nav == "📊 Clustering":
    if not require_connection():
        st.stop()

    st.markdown("""
    <div class='section-title'>📊 Product Clustering</div>
    <div class='section-sub'>Unsupervised segmentation of products using KMeans + DBSCAN + PCA dimensionality reduction</div>
    """, unsafe_allow_html=True)

    with st.spinner("Loading data from Verde_DW…"):
        try:
            from sqlalchemy import text as sqlt
            engine = st.session_state.engine
            fact_raw = pd.read_sql("""
                SELECT f.FK_Produit, f.Quantite_Produit, f.Prix_Totale, f.TotalDiscount
                FROM dbo.FactTransaction f
            """, engine)
            prod_raw = pd.read_sql("""
                SELECT ProduitPK, Famille, SousFamille, Marque, PrixVenteHT, PrixAchatHT
                FROM dbo.DimProduit
            """, engine)
        except Exception as e:
            st.error(f"Data load error: {e}"); st.stop()

    # ── Prepare cluster_df ───────────────────
    for col in ["Quantite_Produit", "Prix_Totale", "TotalDiscount"]:
        fact_raw[col] = pd.to_numeric(fact_raw[col], errors="coerce").abs().fillna(0)
    for col in ["PrixVenteHT", "PrixAchatHT"]:
        prod_raw[col] = pd.to_numeric(prod_raw[col], errors="coerce")
        prod_raw[col].fillna(prod_raw[col].median(), inplace=True)
    for col in ["Famille", "SousFamille", "Marque"]:
        prod_raw[col] = prod_raw[col].astype("string").str.strip().fillna("Unknown")

    fact_agg = fact_raw.groupby("FK_Produit", as_index=False).agg(
        Quantite_Produit=("Quantite_Produit","sum"),
        Prix_Totale=("Prix_Totale","sum"),
        TotalDiscount=("TotalDiscount","sum")
    ).rename(columns={"FK_Produit":"ProduitPK"})

    cluster_df = fact_agg.merge(prod_raw, on="ProduitPK", how="inner")
    cluster_df["Marge"] = cluster_df["PrixVenteHT"] - cluster_df["PrixAchatHT"]

    _num_cols = ["Quantite_Produit","Prix_Totale","TotalDiscount","PrixVenteHT","PrixAchatHT","Marge"]
    for _c in _num_cols:
        cluster_df[_c] = pd.to_numeric(cluster_df[_c], errors="coerce")
        cluster_df[_c].fillna(cluster_df[_c].median(), inplace=True)
    cluster_df = cluster_df.dropna(subset=_num_cols).reset_index(drop=True)
    if len(cluster_df) == 0:
        st.error("No valid data after cleaning. Check your database."); st.stop()

    X_num = cluster_df[_num_cols].copy()

    # ── Sidebar controls ─────────────────────
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Clustering Options**")
    algo = st.sidebar.selectbox("Algorithm", ["KMeans", "DBSCAN"])
    n_clusters = st.sidebar.slider("KMeans k", 2, 8, 5) if algo == "KMeans" else None

    tab_overview, tab_pca, tab_cluster, tab_metrics = st.tabs([
        "📋 Data Overview", "🔬 PCA Analysis", "🎨 Clusters", "📏 Metrics"
    ])

    with tab_overview:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Products", f"{len(cluster_df):,}")
        c2.metric("Avg Quantity Sold", f"{cluster_df['Quantite_Produit'].mean():,.0f}")
        c3.metric("Avg Revenue", f"{cluster_df['Prix_Totale'].mean():,.0f} TND")
        c4.metric("Avg Margin", f"{cluster_df['Marge'].mean():,.2f} TND")

        st.markdown("<br/>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Sample Data**")
            st.dataframe(cluster_df[["ProduitPK","Famille","Marque","Quantite_Produit","Prix_Totale","Marge"]].head(10),
                         use_container_width=True, hide_index=True)
        with col2:
            st.markdown("**Distribution by Famille**")
            fam_counts = cluster_df["Famille"].value_counts().head(10)
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(7, 4))
            fig.patch.set_facecolor("#0d2318")
            ax.set_facecolor("#111f16")
            bars = ax.barh(fam_counts.index, fam_counts.values,
                           color=["#27ae60","#1e8449","#145a32","#0e6b3a","#2ecc71",
                                  "#1abc9c","#48c9b0","#a9dfbf","#76d7c4","#117a65"])
            ax.set_xlabel("Count", color="#7fb894")
            ax.tick_params(colors="#7fb894")
            for spine in ax.spines.values(): spine.set_edgecolor("#1e5c34")
            fig.tight_layout()
            st.pyplot(fig)
            plt.close()

    with tab_pca:
        from sklearn.preprocessing import RobustScaler
        from sklearn.decomposition import PCA

        scaler = RobustScaler()
        X_scaled = scaler.fit_transform(X_num)
        pca2 = PCA(n_components=2)
        X_pca = pca2.fit_transform(X_scaled)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<div class='verde-card'>", unsafe_allow_html=True)
            ev1 = round(pca2.explained_variance_ratio_[0]*100, 2)
            ev2 = round(pca2.explained_variance_ratio_[1]*100, 2)
            st.metric("PC1 Variance", f"{ev1}%")
            st.metric("PC2 Variance", f"{ev2}%")
            st.metric("Total Explained", f"{ev1+ev2:.2f}%")
            st.markdown("</div>", unsafe_allow_html=True)
        with col2:
            fig2, ax2 = plt.subplots(figsize=(6, 5))
            fig2.patch.set_facecolor("#0d2318"); ax2.set_facecolor("#111f16")
            ax2.scatter(X_pca[:,0], X_pca[:,1], alpha=0.4, s=15, color="#27ae60")
            ax2.axhline(0, color="#1e5c34", lw=1); ax2.axvline(0, color="#1e5c34", lw=1)
            ax2.set_title("PCA — Individual Map", color="#f0faf4")
            ax2.set_xlabel(f"PC1 ({ev1}%)", color="#7fb894")
            ax2.set_ylabel(f"PC2 ({ev2}%)", color="#7fb894")
            ax2.tick_params(colors="#7fb894")
            for sp in ax2.spines.values(): sp.set_edgecolor("#1e5c34")
            fig2.tight_layout()
            st.pyplot(fig2); plt.close()

        # Correlation circle
        st.markdown("**Correlation Circle**")
        loadings = pca2.components_.T
        num_cols_names = ["Quantite_Produit","Prix_Totale","TotalDiscount","PrixVenteHT","PrixAchatHT","Marge"]
        fig3, ax3 = plt.subplots(figsize=(6, 6))
        fig3.patch.set_facecolor("#0d2318"); ax3.set_facecolor("#111f16")
        circle = plt.Circle((0,0),1,color="#27ae60",fill=False,linewidth=1.5)
        ax3.add_artist(circle)
        ax3.axhline(0, color="#1e5c34", lw=1); ax3.axvline(0, color="#1e5c34", lw=1)
        colors_arr = ["#2ecc71","#1abc9c","#f1c40f","#e67e22","#e74c3c","#9b59b6"]
        for i, var in enumerate(num_cols_names):
            ax3.arrow(0,0,loadings[i,0],loadings[i,1],
                      head_width=0.04, head_length=0.04,
                      color=colors_arr[i], length_includes_head=True, linewidth=2)
            ax3.text(loadings[i,0]*1.18, loadings[i,1]*1.18, var,
                     fontsize=9, color=colors_arr[i], fontweight="bold")
        ax3.set_xlim(-1.3,1.3); ax3.set_ylim(-1.3,1.3)
        ax3.set_title("Correlation Circle", color="#f0faf4")
        ax3.set_xlabel(f"PC1 ({ev1}%)", color="#7fb894")
        ax3.set_ylabel(f"PC2 ({ev2}%)", color="#7fb894")
        ax3.tick_params(colors="#7fb894")
        ax3.set_aspect("equal")
        for sp in ax3.spines.values(): sp.set_edgecolor("#1e5c34")
        fig3.tight_layout(); st.pyplot(fig3); plt.close()

    with tab_cluster:
        from sklearn.cluster import KMeans, DBSCAN
        from sklearn.preprocessing import RobustScaler
        from sklearn.decomposition import PCA

        scaler2 = RobustScaler()
        Xs = scaler2.fit_transform(X_num)

        if algo == "KMeans":
            # Elbow
            inertias = []
            K_range = range(2, 9)
            for k in K_range:
                km = KMeans(n_clusters=k, random_state=42, n_init=10)
                km.fit(Xs)
                inertias.append(km.inertia_)

            fig_e, ax_e = plt.subplots(figsize=(8, 3.5))
            fig_e.patch.set_facecolor("#0d2318"); ax_e.set_facecolor("#111f16")
            ax_e.plot(list(K_range), inertias, marker="o", color="#2ecc71", linewidth=2, markersize=7)
            ax_e.axvline(x=n_clusters, color="#f1c40f", linestyle="--", linewidth=2, label=f"k={n_clusters}")
            ax_e.set_title("Elbow Method", color="#f0faf4")
            ax_e.set_xlabel("k", color="#7fb894"); ax_e.set_ylabel("Inertia", color="#7fb894")
            ax_e.tick_params(colors="#7fb894"); ax_e.legend(labelcolor="#f0faf4")
            for sp in ax_e.spines.values(): sp.set_edgecolor("#1e5c34")
            fig_e.tight_layout(); st.pyplot(fig_e); plt.close()

            km_final = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            labels = km_final.fit_predict(Xs)
        else:
            dbscan = DBSCAN(eps=4.0, min_samples=7)
            labels = dbscan.fit_predict(Xs)

        # Visualise
        pca_v = PCA(n_components=2)
        X2d = pca_v.fit_transform(Xs)

        cluster_colors = ["#2ecc71","#1abc9c","#f1c40f","#e67e22","#e74c3c","#9b59b6","#3498db","#e91e63"]
        unique_labels = sorted(set(labels))

        fig4, ax4 = plt.subplots(figsize=(10, 6))
        fig4.patch.set_facecolor("#0d2318"); ax4.set_facecolor("#111f16")
        for i, lbl in enumerate(unique_labels):
            mask = labels == lbl
            color = "#555" if lbl == -1 else cluster_colors[i % len(cluster_colors)]
            name = "Noise" if lbl == -1 else f"Cluster {lbl}"
            ax4.scatter(X2d[mask,0], X2d[mask,1], alpha=0.6, s=25, color=color, label=name)
        if algo == "KMeans":
            centres2d = pca_v.transform(km_final.cluster_centers_)
            ax4.scatter(centres2d[:,0], centres2d[:,1], c="white", s=250, marker="X",
                        edgecolors="#f1c40f", linewidth=2, label="Centroids", zorder=5)
        ax4.set_title(f"{algo} Cluster Visualization (PCA 2D)", color="#f0faf4", fontsize=13)
        ax4.set_xlabel("Dimension 1", color="#7fb894"); ax4.set_ylabel("Dimension 2", color="#7fb894")
        ax4.tick_params(colors="#7fb894"); ax4.legend(labelcolor="#f0faf4", facecolor="#111f16")
        for sp in ax4.spines.values(): sp.set_edgecolor("#1e5c34")
        fig4.tight_layout(); st.pyplot(fig4); plt.close()

        # Cluster profile heatmap
        if algo == "KMeans":
            import seaborn as sns
            cluster_df2 = X_num.copy()
            cluster_df2["Cluster"] = labels
            profile = cluster_df2.groupby("Cluster").mean().round(2)
            fig5, ax5 = plt.subplots(figsize=(10, 4))
            fig5.patch.set_facecolor("#0d2318"); ax5.set_facecolor("#111f16")
            sns.heatmap(profile, annot=True, fmt=".1f", cmap="YlGn", ax=ax5,
                        annot_kws={"size":9}, linewidths=0.5, linecolor="#0d2318")
            ax5.set_title("Cluster Profiles — Mean Values", color="#f0faf4")
            ax5.tick_params(colors="#7fb894")
            fig5.tight_layout(); st.pyplot(fig5); plt.close()

    with tab_metrics:
        from sklearn.metrics import silhouette_score, davies_bouldin_score
        from sklearn.preprocessing import RobustScaler
        from sklearn.cluster import KMeans

        sc3 = RobustScaler()
        Xs3 = sc3.fit_transform(X_num)
        km3 = KMeans(n_clusters=n_clusters if n_clusters else 5, random_state=42, n_init=10)
        lbl3 = km3.fit_predict(Xs3)

        sil = silhouette_score(Xs3, lbl3)
        db = davies_bouldin_score(Xs3, lbl3)

        c1, c2, c3 = st.columns(3)
        c1.metric("Silhouette Score", f"{sil:.4f}", delta="Higher is better")
        c2.metric("Davies-Bouldin Score", f"{db:.4f}", delta="Lower is better")
        c3.metric("Clusters Found", str(len(set(lbl3))))

        st.markdown("""
        <div class='verde-card' style='margin-top:16px;'>
        <b>📖 Cluster Interpretation (KMeans, k=5)</b><br/><br/>
        <span class="badge badge-green">Cluster 0</span> Performing products under promotion — intermediate profile, visible discounts<br/><br/>
        <span class="badge badge-teal">Cluster 1</span> Low commercial performance — low sales, low revenue, modest margin<br/><br/>
        <span class="badge badge-gold">Cluster 2</span> Star profitable products — good volume, good revenue, good margin<br/><br/>
        <span class="badge badge-red">Cluster 3</span> Very high rotation, low margin — massive quantity, heavy discounts<br/><br/>
        <span class="badge" style="background:rgba(155,89,182,0.2);color:#9b59b6;border:1px solid rgba(155,89,182,0.4);">Cluster 4</span> Premium low-rotation — very high prices, highest unit margin
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE: CLASSIFICATION
# ─────────────────────────────────────────────
elif nav == "🎯 Classification":
    if not require_connection():
        st.stop()

    st.markdown("""
    <div class='section-title'>🎯 Customer Return Classification</div>
    <div class='section-sub'>Predict whether a customer is <b>Returning</b> or <b>Non-Returning</b> using Random Forest & Gradient Boosting</div>
    """, unsafe_allow_html=True)

    with st.spinner("Loading classification data…"):
        try:
            engine = st.session_state.engine
            fact = pd.read_sql("SELECT DocumentNumber, Quantite_Produit, IsPaid, TotalDiscount, FK_Partner, FK_Produit FROM dbo.FactTransaction", engine)
            prod = pd.read_sql("SELECT ProduitPK, Target_Gender, Target_Age FROM dbo.DimProduit", engine)
            part = pd.read_sql("SELECT PartnerPK, TypePartner FROM dbo.DimPartner", engine)
        except Exception as e:
            st.error(f"Data load error: {e}"); st.stop()

    # Prepare
    df = fact.merge(prod, left_on="FK_Produit", right_on="ProduitPK", how="left")
    df = df.merge(part, left_on="FK_Partner", right_on="PartnerPK", how="left")

    partner_counts = df.groupby("FK_Partner")["DocumentNumber"].nunique()
    df["NbTransactionsPartner"] = df["FK_Partner"].map(partner_counts)
    df["Target"] = (df["NbTransactionsPartner"] > 1).astype(int)

    for col in ["Quantite_Produit","IsPaid","TotalDiscount"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["Quantite_Produit"].fillna(df["Quantite_Produit"].median(), inplace=True)
    df["IsPaid"].fillna(0, inplace=True); df["TotalDiscount"].fillna(0, inplace=True)
    for col in ["Target_Gender","Target_Age","TypePartner"]:
        df[col] = df[col].astype("string").str.strip().fillna("Unknown")

    X = df[["IsPaid","Quantite_Produit","TotalDiscount","Target_Gender","Target_Age","TypePartner"]]
    y = df["Target"]

    tab_data, tab_model, tab_results, tab_feat = st.tabs([
        "📋 Data Overview", "🤖 Train Models", "📊 Results", "🔑 Feature Importance"
    ])

    with tab_data:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Records", f"{len(df):,}")
        c2.metric("Returning (1)", f"{(y==1).sum():,}", delta=f"{(y==1).mean()*100:.1f}%")
        c3.metric("Non-Returning (0)", f"{(y==0).sum():,}", delta=f"{(y==0).mean()*100:.1f}%")
        c4.metric("Features", "6")

        st.markdown("<br/>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(5, 4))
            fig.patch.set_facecolor("#0d2318"); ax.set_facecolor("#111f16")
            counts = y.value_counts()
            wedges, texts, autotexts = ax.pie(
                counts.values, labels=["Returning","Non-Returning"],
                colors=["#27ae60","#e74c3c"], autopct="%1.1f%%",
                startangle=90, textprops={"color":"#f0faf4"}
            )
            for at in autotexts: at.set_fontsize(11); at.set_fontweight("bold")
            ax.set_title("Class Distribution", color="#f0faf4")
            fig.tight_layout(); st.pyplot(fig); plt.close()
        with col2:
            st.markdown("**Target Distribution**")
            st.dataframe(pd.DataFrame({
                "Class": ["0 — Non-Returning", "1 — Returning"],
                "Count": [int((y==0).sum()), int((y==1).sum())],
                "Percentage": [f"{(y==0).mean()*100:.1f}%", f"{(y==1).mean()*100:.1f}%"]
            }), use_container_width=True, hide_index=True)
            st.warning("⚠️ Highly imbalanced dataset — class_weight='balanced' used to compensate.")

    with tab_model:
        from sklearn.model_selection import train_test_split
        from sklearn.compose import ColumnTransformer
        from sklearn.pipeline import Pipeline
        from sklearn.impute import SimpleImputer
        from sklearn.preprocessing import OneHotEncoder, StandardScaler
        from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
        from sklearn.metrics import (f1_score, accuracy_score, classification_report,
                                     confusion_matrix, roc_auc_score)

        col_train, col_cfg = st.columns([2,1])
        with col_cfg:
            st.markdown("<div class='verde-card'>", unsafe_allow_html=True)
            st.markdown("**⚙️ Model Config**")
            clf_model = st.selectbox("Model", ["Gradient Boosting", "Random Forest"])
            test_size = st.slider("Test Size", 0.1, 0.4, 0.2, 0.05)
            n_est = st.slider("n_estimators", 50, 300, 100, 50)
            max_d = st.selectbox("max_depth", [2, 3, 5, 10, None], index=1)
            train_btn = st.button("🚀 Train Model", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_train:
            if train_btn:
                X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=test_size,
                                                           random_state=42, stratify=y)
                num_feats = ["IsPaid","Quantite_Produit","TotalDiscount"]
                cat_feats = ["Target_Gender","Target_Age","TypePartner"]
                num_pipe = Pipeline([("imp", SimpleImputer(strategy="median")),
                                     ("sc", StandardScaler())])
                cat_pipe = Pipeline([("imp", SimpleImputer(strategy="most_frequent")),
                                     ("ohe", OneHotEncoder(handle_unknown="ignore"))])
                pre = ColumnTransformer([("num",num_pipe,num_feats),("cat",cat_pipe,cat_feats)])

                if clf_model == "Random Forest":
                    model_clf = Pipeline([("pre", pre),
                                          ("m", RandomForestClassifier(
                                              n_estimators=n_est, max_depth=max_d,
                                              random_state=42, class_weight="balanced"))])
                else:
                    model_clf = Pipeline([("pre", pre),
                                          ("m", GradientBoostingClassifier(
                                              n_estimators=n_est, max_depth=max_d,
                                              learning_rate=0.01, random_state=42))])

                with st.spinner("Training…"):
                    model_clf.fit(X_tr, y_tr)

                y_pred = model_clf.predict(X_te)
                y_proba = model_clf.predict_proba(X_te)[:,1]

                st.session_state["clf_model"] = model_clf
                st.session_state["clf_results"] = {
                    "accuracy": accuracy_score(y_te, y_pred),
                    "f1": f1_score(y_te, y_pred, zero_division=0),
                    "auc": roc_auc_score(y_te, y_proba),
                    "cm": confusion_matrix(y_te, y_pred),
                    "report": classification_report(y_te, y_pred),
                    "y_test": y_te, "y_pred": y_pred, "y_proba": y_proba,
                    "model_name": clf_model
                }
                st.session_state.models_trained = True
                st.success(f"✅ {clf_model} trained! F1={f1_score(y_te,y_pred,zero_division=0):.4f} | AUC={roc_auc_score(y_te,y_proba):.4f}")
            else:
                st.info("Configure the model on the right and click **Train Model**.")

    with tab_results:
        if "clf_results" not in st.session_state:
            st.info("Train a model first in the **Train Models** tab.")
        else:
            res = st.session_state["clf_results"]
            import matplotlib.pyplot as plt
            import seaborn as sns

            c1, c2, c3 = st.columns(3)
            c1.metric("Accuracy", f"{res['accuracy']:.4f}")
            c2.metric("F1 Score", f"{res['f1']:.4f}")
            c3.metric("ROC-AUC", f"{res['auc']:.4f}")

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Confusion Matrix**")
                fig, ax = plt.subplots(figsize=(5, 4))
                fig.patch.set_facecolor("#0d2318"); ax.set_facecolor("#111f16")
                sns.heatmap(res["cm"], annot=True, fmt="d", cmap="Greens", ax=ax,
                            linewidths=1, linecolor="#0d2318",
                            annot_kws={"size":14, "color":"white"})
                ax.set_xlabel("Predicted", color="#7fb894")
                ax.set_ylabel("Actual", color="#7fb894")
                ax.tick_params(colors="#7fb894")
                ax.set_title(f"Confusion Matrix — {res['model_name']}", color="#f0faf4")
                fig.tight_layout(); st.pyplot(fig); plt.close()

            with col2:
                st.markdown("**ROC Curve**")
                from sklearn.metrics import roc_curve
                fpr, tpr, _ = roc_curve(res["y_test"], res["y_proba"])
                fig2, ax2 = plt.subplots(figsize=(5, 4))
                fig2.patch.set_facecolor("#0d2318"); ax2.set_facecolor("#111f16")
                ax2.plot(fpr, tpr, color="#2ecc71", linewidth=2.5,
                         label=f"AUC = {res['auc']:.3f}")
                ax2.plot([0,1],[0,1],"--", color="#555", linewidth=1)
                ax2.set_xlabel("FPR", color="#7fb894"); ax2.set_ylabel("TPR", color="#7fb894")
                ax2.tick_params(colors="#7fb894"); ax2.legend(labelcolor="#f0faf4", facecolor="#111f16")
                ax2.set_title("ROC Curve", color="#f0faf4")
                for sp in ax2.spines.values(): sp.set_edgecolor("#1e5c34")
                fig2.tight_layout(); st.pyplot(fig2); plt.close()

            st.markdown("**Classification Report**")
            st.code(res["report"])

    with tab_feat:
        if "clf_model" not in st.session_state:
            st.info("Train a model first.")
        else:
            import matplotlib.pyplot as plt
            model_pipe = st.session_state["clf_model"]
            clf_inner = model_pipe.named_steps["m"]
            ohe_features = model_pipe.named_steps["pre"] \
                .named_transformers_["cat"].named_steps["ohe"] \
                .get_feature_names_out(["Target_Gender","Target_Age","TypePartner"])
            all_feats = np.concatenate([["IsPaid","Quantite_Produit","TotalDiscount"], ohe_features])
            importances = clf_inner.feature_importances_
            fi_df = pd.DataFrame({"Feature": all_feats, "Importance": importances}) \
                      .sort_values("Importance", ascending=False).head(12)

            fig, ax = plt.subplots(figsize=(9, 5))
            fig.patch.set_facecolor("#0d2318"); ax.set_facecolor("#111f16")
            colors_fi = ["#2ecc71"] * 3 + ["#1abc9c"] * 9
            ax.barh(fi_df["Feature"], fi_df["Importance"],
                    color=colors_fi[:len(fi_df)], edgecolor="#0d2318")
            ax.invert_yaxis()
            ax.set_title("Feature Importance (Top 12)", color="#f0faf4")
            ax.set_xlabel("Importance", color="#7fb894")
            ax.tick_params(colors="#7fb894")
            for sp in ax.spines.values(): sp.set_edgecolor("#1e5c34")
            fig.tight_layout(); st.pyplot(fig); plt.close()


# ─────────────────────────────────────────────
# PAGE: REGRESSION
# ─────────────────────────────────────────────
elif nav == "📈 Regression":
    if not require_connection():
        st.stop()

    st.markdown("""
    <div class='section-title'>📈 Sales Quantity Regression</div>
    <div class='section-sub'>Predict product sales quantity using Linear Regression, Random Forest & XGBoost</div>
    """, unsafe_allow_html=True)

    with st.spinner("Loading regression data (sales only)…"):
        try:
            engine = st.session_state.engine
            fact_reg = pd.read_sql("""
                SELECT f.FK_Produit, f.Quantite_Produit, f.Prix_Totale,
                       f.TotalDiscount, f.IsPaid, d.[Date] AS DateTransaction
                FROM dbo.FactTransaction f
                LEFT JOIN dbo.DimDate d ON f.DateTransaction = d.DatePK
                WHERE f.TransactionType = 2
            """, engine)
            dim_prod = pd.read_sql("""
                SELECT ProduitPK, Famille, Marque, PrixVenteHT, PrixAchatHT
                FROM dbo.DimProduit
            """, engine)
        except Exception as e:
            st.error(f"Data load error: {e}"); st.stop()

    # Prep
    for col in ["Quantite_Produit","Prix_Totale","TotalDiscount","IsPaid"]:
        fact_reg[col] = pd.to_numeric(fact_reg[col], errors="coerce")
    fact_reg["DateTransaction"] = pd.to_datetime(fact_reg["DateTransaction"], errors="coerce")
    fact_reg["Quantite_Produit"].fillna(fact_reg["Quantite_Produit"].median(), inplace=True)
    fact_reg["Prix_Totale"].fillna(fact_reg["Prix_Totale"].median(), inplace=True)
    fact_reg["TotalDiscount"].fillna(0, inplace=True)
    fact_reg["IsPaid"].fillna(0, inplace=True)
    fact_reg = fact_reg.dropna(subset=["DateTransaction"])
    for col in ["PrixVenteHT","PrixAchatHT"]:
        dim_prod[col] = pd.to_numeric(dim_prod[col], errors="coerce")
        dim_prod[col].fillna(dim_prod[col].median(), inplace=True)

    reg_df = fact_reg.merge(dim_prod, left_on="FK_Produit", right_on="ProduitPK", how="inner")
    for col in reg_df.select_dtypes(include="number").columns:
        neg = (reg_df[col] < 0).sum()
        if neg: reg_df[col] = reg_df[col].abs()

    q_low = reg_df["Quantite_Produit"].quantile(0.01)
    q_high = reg_df["Quantite_Produit"].quantile(0.99)
    reg_df = reg_df[(reg_df["Quantite_Produit"] >= q_low) & (reg_df["Quantite_Produit"] <= q_high)].copy()

    # Feature engineering
    reg_df["Mois"] = reg_df["DateTransaction"].dt.month
    reg_df["JourSem"] = reg_df["DateTransaction"].dt.dayofweek
    reg_df["Annee"] = reg_df["DateTransaction"].dt.year
    reg_df["Marge_HT"] = reg_df["PrixVenteHT"] - reg_df["PrixAchatHT"]
    reg_df["Ratio_Remise"] = reg_df["TotalDiscount"] / (reg_df["PrixVenteHT"] + 1)
    reg_df["Prix_Achat_Vente_Ratio"] = reg_df["PrixAchatHT"] / (reg_df["PrixVenteHT"] + 1)

    from sklearn.preprocessing import LabelEncoder
    le_dict = {}
    for col in ["Marque","Famille"]:
        le = LabelEncoder()
        reg_df[col+"_enc"] = le.fit_transform(reg_df[col].astype(str))
        le_dict[col] = le
        st.session_state[f"le_{col}"] = le

    FEATURES = ["TotalDiscount","PrixVenteHT","PrixAchatHT","Marge_HT","Ratio_Remise",
                 "Prix_Achat_Vente_Ratio","Mois","JourSem","Annee","Marque_enc","Famille_enc"]
    TARGET = "Quantite_Produit"

    tab_eda, tab_train, tab_compare, tab_charts = st.tabs([
        "📋 EDA", "🤖 Train Models", "🏆 Comparison", "📊 Visualizations"
    ])

    with tab_eda:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Sales Records", f"{len(reg_df):,}")
        c2.metric("Avg Qty Sold", f"{reg_df['Quantite_Produit'].mean():.2f}")
        c3.metric("Max Qty", f"{reg_df['Quantite_Produit'].max():.0f}")
        c4.metric("Unique Products", f"{reg_df['FK_Produit'].nunique():,}")

        import matplotlib.pyplot as plt
        col1, col2 = st.columns(2)
        with col1:
            fig, ax = plt.subplots(figsize=(6, 4))
            fig.patch.set_facecolor("#0d2318"); ax.set_facecolor("#111f16")
            ax.hist(reg_df["Quantite_Produit"], bins=40, color="#27ae60", edgecolor="#0d2318", alpha=0.85)
            ax.set_title("Quantity Distribution", color="#f0faf4")
            ax.set_xlabel("Quantite_Produit", color="#7fb894")
            ax.tick_params(colors="#7fb894")
            for sp in ax.spines.values(): sp.set_edgecolor("#1e5c34")
            fig.tight_layout(); st.pyplot(fig); plt.close()
        with col2:
            monthly = reg_df.groupby("Mois")["Quantite_Produit"].sum()
            fig2, ax2 = plt.subplots(figsize=(6, 4))
            fig2.patch.set_facecolor("#0d2318"); ax2.set_facecolor("#111f16")
            ax2.bar(monthly.index, monthly.values, color="#1abc9c", edgecolor="#0d2318")
            ax2.set_title("Monthly Sales Volume", color="#f0faf4")
            ax2.set_xlabel("Month", color="#7fb894"); ax2.set_ylabel("Total Qty", color="#7fb894")
            ax2.tick_params(colors="#7fb894")
            for sp in ax2.spines.values(): sp.set_edgecolor("#1e5c34")
            fig2.tight_layout(); st.pyplot(fig2); plt.close()

    with tab_train:
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import RobustScaler
        from sklearn.linear_model import LinearRegression
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

        X_r = reg_df[FEATURES]; y_r = reg_df[TARGET]
        X_tr, X_te, y_tr, y_te = train_test_split(X_r, y_r, test_size=0.2, random_state=42)
        sc = RobustScaler()
        X_tr_sc = sc.fit_transform(X_tr); X_te_sc = sc.transform(X_te)

        col_cfg, col_out = st.columns([1, 2])
        with col_cfg:
            st.markdown("<div class='verde-card'>", unsafe_allow_html=True)
            st.markdown("**⚙️ Models to Train**")
            run_lr = st.checkbox("Linear Regression", value=True)
            run_rf = st.checkbox("Random Forest", value=True)
            run_xgb = st.checkbox("XGBoost", value=True)
            n_est_r = st.slider("RF n_estimators", 100, 500, 300, 100)
            train_reg_btn = st.button("🚀 Train Regressors", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_out:
            if train_reg_btn:
                results = {}
                prog = st.progress(0)
                step = 0
                total = sum([run_lr, run_rf, run_xgb])

                if run_lr:
                    lr = LinearRegression(); lr.fit(X_tr_sc, y_tr)
                    yp = lr.predict(X_te_sc)
                    results["Linear Regression"] = {
                        "MAE": mean_absolute_error(y_te,yp),
                        "RMSE": np.sqrt(mean_squared_error(y_te,yp)),
                        "R²": r2_score(y_te,yp), "y_pred": yp
                    }
                    step += 1; prog.progress(step/total)

                if run_rf:
                    rf = RandomForestRegressor(n_estimators=n_est_r, max_depth=15,
                                               min_samples_split=4, min_samples_leaf=2,
                                               max_features="sqrt", n_jobs=-1, random_state=42)
                    rf.fit(X_tr, y_tr); yp = rf.predict(X_te)
                    results["Random Forest"] = {
                        "MAE": mean_absolute_error(y_te,yp),
                        "RMSE": np.sqrt(mean_squared_error(y_te,yp)),
                        "R²": r2_score(y_te,yp), "y_pred": yp, "model": rf
                    }
                    step += 1; prog.progress(step/total)

                if run_xgb:
                    try:
                        from xgboost import XGBRegressor
                        xgb = XGBRegressor(n_estimators=500, learning_rate=0.03, max_depth=7,
                                           subsample=0.85, colsample_bytree=0.85,
                                           reg_alpha=0.1, reg_lambda=1.5, min_child_weight=3,
                                           random_state=42, n_jobs=-1, verbosity=0)
                        xgb.fit(X_tr, y_tr); yp = xgb.predict(X_te)
                        results["XGBoost"] = {
                            "MAE": mean_absolute_error(y_te,yp),
                            "RMSE": np.sqrt(mean_squared_error(y_te,yp)),
                            "R²": r2_score(y_te,yp), "y_pred": yp, "model": xgb
                        }
                    except ImportError:
                        st.warning("XGBoost not installed — skipping.")
                    step += 1; prog.progress(1.0)

                st.session_state["reg_results"] = results
                st.session_state["reg_y_test"] = y_te
                st.session_state["reg_X_test"] = X_te
                st.session_state["reg_FEATURES"] = FEATURES
                st.success("✅ Models trained!")
            else:
                st.info("Select models and click **Train Regressors**.")

    with tab_compare:
        if "reg_results" not in st.session_state:
            st.info("Train models first.")
        else:
            res_r = st.session_state["reg_results"]
            comp_df = pd.DataFrame([{
                "Model": k, "MAE": f"{v['MAE']:.4f}",
                "RMSE": f"{v['RMSE']:.4f}", "R²": f"{v['R²']:.4f}"
            } for k, v in res_r.items()])
            st.dataframe(comp_df, use_container_width=True, hide_index=True)

            import matplotlib.pyplot as plt
            fig, axes = plt.subplots(1, 3, figsize=(15, 4))
            fig.patch.set_facecolor("#0d2318")
            col_map = {"Linear Regression":"#e74c3c", "Random Forest":"#2ecc71", "XGBoost":"#3498db"}
            y_te_r = st.session_state["reg_y_test"]

            for ax, (name, vals) in zip(axes, res_r.items()):
                ax.set_facecolor("#111f16")
                ax.scatter(y_te_r, vals["y_pred"], alpha=0.3, s=12,
                           color=col_map.get(name,"#27ae60"))
                lims = [min(float(y_te_r.min()), float(vals["y_pred"].min())),
                        max(float(y_te_r.max()), float(vals["y_pred"].max()))]
                ax.plot(lims, lims, "w--", lw=1.5)
                ax.set_title(name, color="#f0faf4", fontsize=11, fontweight="bold")
                ax.set_xlabel("Actual", color="#7fb894")
                ax.set_ylabel("Predicted", color="#7fb894")
                ax.tick_params(colors="#7fb894")
                for sp in ax.spines.values(): sp.set_edgecolor("#1e5c34")
                r2_val = float(vals["R²"]) if isinstance(vals["R²"], (int,float)) else float(vals["R²"])
                ax.text(0.05, 0.92, f"R²={r2_val:.4f}", transform=ax.transAxes,
                        color="#f1c40f", fontsize=10, fontweight="bold")

            fig.tight_layout(); st.pyplot(fig); plt.close()

    with tab_charts:
        if "reg_results" not in st.session_state:
            st.info("Train models first.")
        else:
            import matplotlib.pyplot as plt
            res_r = st.session_state["reg_results"]
            y_te_r = st.session_state["reg_y_test"]
            col_map = {"Linear Regression":"#e74c3c", "Random Forest":"#2ecc71", "XGBoost":"#3498db"}

            # Residuals
            st.markdown("**Residuals Distribution**")
            fig, axes = plt.subplots(1, len(res_r), figsize=(5*len(res_r), 4))
            fig.patch.set_facecolor("#0d2318")
            if len(res_r) == 1: axes = [axes]
            for ax, (name, vals) in zip(axes, res_r.items()):
                ax.set_facecolor("#111f16")
                residuals = y_te_r.values - vals["y_pred"]
                ax.hist(residuals, bins=40, color=col_map.get(name,"#27ae60"),
                        edgecolor="#0d2318", alpha=0.85)
                ax.axvline(0, color="white", lw=2, ls="--")
                ax.set_title(f"Residuals — {name}", color="#f0faf4")
                ax.set_xlabel("Error (Actual − Predicted)", color="#7fb894")
                ax.tick_params(colors="#7fb894")
                for sp in ax.spines.values(): sp.set_edgecolor("#1e5c34")
            fig.tight_layout(); st.pyplot(fig); plt.close()

            # Feature importance (tree models)
            tree_models = {k: v for k, v in res_r.items()
                           if k in ["Random Forest","XGBoost"] and "model" in v}
            if tree_models:
                st.markdown("**Feature Importance**")
                fig2, axes2 = plt.subplots(1, len(tree_models), figsize=(8*len(tree_models), 5))
                fig2.patch.set_facecolor("#0d2318")
                if len(tree_models) == 1: axes2 = [axes2]
                FEATS = st.session_state["reg_FEATURES"]
                for ax, (name, vals) in zip(axes2, tree_models.items()):
                    ax.set_facecolor("#111f16")
                    imp = pd.Series(vals["model"].feature_importances_, index=FEATS).sort_values()
                    ax.barh(imp.index, imp.values, color="#1abc9c", edgecolor="#0d2318")
                    ax.set_title(f"{name} — Feature Importance", color="#f0faf4")
                    ax.tick_params(colors="#7fb894")
                    for sp in ax.spines.values(): sp.set_edgecolor("#1e5c34")
                fig2.tight_layout(); st.pyplot(fig2); plt.close()


# ─────────────────────────────────────────────
# PAGE: TIME SERIES
# ─────────────────────────────────────────────
elif nav == "⏱️ Time Series":
    if not require_connection():
        st.stop()

    st.markdown("""
    <div class='section-title'>⏱️ Sales Forecasting</div>
    <div class='section-sub'>Weekly sales time series forecasting using Naive Forecast & ARIMA(2,1,2)</div>
    """, unsafe_allow_html=True)

    with st.spinner("Loading time series data…"):
        try:
            engine = st.session_state.engine
            ts_raw = pd.read_sql("""
                SELECT d.[Date] AS DateTransaction,
                       CAST(f.Quantite_Produit AS FLOAT) AS Quantite_Produit,
                       CAST(f.Prix_Totale AS FLOAT) AS Prix_Totale
                FROM dbo.FactTransaction f
                LEFT JOIN dbo.DimDate d ON f.DateTransaction = d.DatePK
                WHERE f.TransactionType = 2 AND d.[Date] IS NOT NULL
                ORDER BY d.[Date]
            """, engine)
        except Exception as e:
            st.error(f"Data load error: {e}"); st.stop()

    ts_raw["DateTransaction"] = pd.to_datetime(ts_raw["DateTransaction"], errors="coerce")
    ts_raw["Quantite_Produit"] = pd.to_numeric(ts_raw["Quantite_Produit"], errors="coerce")
    ts_raw["Prix_Totale"] = pd.to_numeric(ts_raw["Prix_Totale"], errors="coerce")
    ts_raw = ts_raw.dropna()
    ts_raw = ts_raw[ts_raw["DateTransaction"] >= "2024-01-01"]

    ts_weekly = (ts_raw.set_index("DateTransaction")
                 .resample("W")
                 .agg(Quantite_Semaine=("Quantite_Produit","sum"),
                      CA_Semaine=("Prix_Totale","sum"))
                 .reset_index())
    ts_weekly["Year"] = ts_weekly["DateTransaction"].dt.year
    ts_weekly["Month"] = ts_weekly["DateTransaction"].dt.month
    ts_weekly["Quarter"] = ts_weekly["DateTransaction"].dt.quarter

    n = len(ts_weekly)
    split = int(n * 0.8)
    ts_train = ts_weekly.iloc[:split].copy()
    ts_test = ts_weekly.iloc[split:].copy()

    tab_series, tab_model, tab_forecast = st.tabs([
        "📈 Time Series", "🤖 Model Training", "🔮 Forecast"
    ])

    with tab_series:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Weeks", f"{len(ts_weekly)}")
        c2.metric("Avg Weekly Qty", f"{ts_weekly['Quantite_Semaine'].mean():,.1f}")
        c3.metric("Peak Week Qty", f"{ts_weekly['Quantite_Semaine'].max():,.0f}")
        c4.metric("Total Revenue", f"{ts_weekly['CA_Semaine'].sum():,.0f} TND")

        import matplotlib.pyplot as plt
        fig, axes = plt.subplots(2, 1, figsize=(13, 7))
        fig.patch.set_facecolor("#0d2318")

        axes[0].set_facecolor("#111f16")
        axes[0].plot(ts_weekly["DateTransaction"], ts_weekly["Quantite_Semaine"],
                     color="#2ecc71", lw=2, marker="o", markersize=3)
        axes[0].fill_between(ts_weekly["DateTransaction"],
                             ts_weekly["Quantite_Semaine"], alpha=0.15, color="#27ae60")
        axes[0].set_title("Weekly Sales Quantity", color="#f0faf4", fontsize=13)
        axes[0].set_ylabel("Quantity", color="#7fb894")
        axes[0].tick_params(colors="#7fb894"); axes[0].grid(True, alpha=0.2, color="#1e5c34")
        for sp in axes[0].spines.values(): sp.set_edgecolor("#1e5c34")

        axes[1].set_facecolor("#111f16")
        axes[1].plot(ts_weekly["DateTransaction"], ts_weekly["CA_Semaine"],
                     color="#f1c40f", lw=2, marker="s", markersize=3)
        axes[1].fill_between(ts_weekly["DateTransaction"],
                             ts_weekly["CA_Semaine"], alpha=0.12, color="#f1c40f")
        axes[1].set_title("Weekly Revenue (CA)", color="#f0faf4", fontsize=13)
        axes[1].set_ylabel("CA (TND)", color="#7fb894")
        axes[1].tick_params(colors="#7fb894"); axes[1].grid(True, alpha=0.2, color="#1e5c34")
        for sp in axes[1].spines.values(): sp.set_edgecolor("#1e5c34")

        fig.tight_layout(); st.pyplot(fig); plt.close()

        # ADF test
        from statsmodels.tsa.stattools import adfuller
        adf_res = adfuller(ts_weekly["Quantite_Semaine"].dropna())
        pval = adf_res[1]
        stat_badge = "badge-green" if pval < 0.05 else "badge-red"
        stat_text = "STATIONARY ✅" if pval < 0.05 else "NON-STATIONARY ⚠️"
        st.markdown(f"""
        <div class='verde-card' style='margin-top:12px;'>
        <b>📐 ADF Stationarity Test</b><br/><br/>
        ADF Statistic: <code>{adf_res[0]:.4f}</code> &nbsp;|&nbsp;
        p-value: <code>{pval:.4f}</code> &nbsp;|&nbsp;
        <span class="badge {stat_badge}">{stat_text}</span>
        </div>
        """, unsafe_allow_html=True)

    with tab_model:
        from sklearn.metrics import mean_absolute_error, mean_squared_error
        from statsmodels.tsa.arima.model import ARIMA
        import matplotlib.pyplot as plt

        st.sidebar.markdown("---")
        st.sidebar.markdown("**ARIMA Parameters**")
        p = st.sidebar.slider("p (AR order)", 0, 5, 2)
        d = st.sidebar.slider("d (differencing)", 0, 2, 1)
        q = st.sidebar.slider("q (MA order)", 0, 5, 2)

        run_ts = st.button("🚀 Run Forecasting Models", use_container_width=False)

        if run_ts:
            with st.spinner("Training models…"):
                # Naive
                naive_val = ts_train["Quantite_Semaine"].iloc[-1]
                naive_pred = np.full(len(ts_test), naive_val)
                mae_naive = mean_absolute_error(ts_test["Quantite_Semaine"], naive_pred)
                rmse_naive = np.sqrt(mean_squared_error(ts_test["Quantite_Semaine"], naive_pred))

                # ARIMA
                try:
                    arima_m = ARIMA(ts_train["Quantite_Semaine"], order=(p,d,q))
                    arima_f = arima_m.fit(method_kwargs={"warn_convergence": False})
                    arima_pred = arima_f.forecast(steps=len(ts_test)).values
                    mae_arima = mean_absolute_error(ts_test["Quantite_Semaine"], arima_pred)
                    rmse_arima = np.sqrt(mean_squared_error(ts_test["Quantite_Semaine"], arima_pred))
                    arima_ok = True
                except Exception as ex:
                    st.warning(f"ARIMA failed: {ex}")
                    arima_ok = False

                st.session_state["ts_results"] = {
                    "naive": {"pred": naive_pred, "mae": mae_naive, "rmse": rmse_naive},
                    "arima": {"pred": arima_pred if arima_ok else None,
                              "mae": mae_arima if arima_ok else None,
                              "rmse": rmse_arima if arima_ok else None},
                    "ts_train": ts_train, "ts_test": ts_test,
                    "arima_fit": arima_f if arima_ok else None,
                    "order": (p,d,q)
                }

            r = st.session_state["ts_results"]
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Naive MAE", f"{r['naive']['mae']:.2f}")
            c2.metric("Naive RMSE", f"{r['naive']['rmse']:.2f}")
            if arima_ok:
                c3.metric("ARIMA MAE", f"{r['arima']['mae']:.2f}")
                c4.metric("ARIMA RMSE", f"{r['arima']['rmse']:.2f}")

            # Comparison plot
            fig, ax = plt.subplots(figsize=(13, 5))
            fig.patch.set_facecolor("#0d2318"); ax.set_facecolor("#111f16")
            ax.plot(ts_train["DateTransaction"], ts_train["Quantite_Semaine"],
                    color="#3498db", lw=2, label="Train")
            ax.plot(ts_test["DateTransaction"], ts_test["Quantite_Semaine"],
                    color="#2ecc71", lw=2.5, label="Actual Test")
            ax.plot(ts_test["DateTransaction"], naive_pred,
                    color="#e74c3c", ls="--", lw=1.5,
                    label=f"Naive (MAE={mae_naive:.1f})")
            if arima_ok:
                ax.plot(ts_test["DateTransaction"], arima_pred,
                        color="#f1c40f", ls="-.", lw=2,
                        label=f"ARIMA({p},{d},{q}) (MAE={mae_arima:.1f})")
            ax.axvline(ts_test["DateTransaction"].iloc[0], color="#555", ls=":", lw=1.5)
            ax.set_title("Forecasting Comparison", color="#f0faf4", fontsize=13)
            ax.set_xlabel("Date", color="#7fb894"); ax.set_ylabel("Quantity", color="#7fb894")
            ax.tick_params(colors="#7fb894"); ax.legend(labelcolor="#f0faf4", facecolor="#111f16")
            ax.grid(True, alpha=0.2, color="#1e5c34")
            for sp in ax.spines.values(): sp.set_edgecolor("#1e5c34")
            fig.tight_layout(); st.pyplot(fig); plt.close()
        else:
            st.info("Click **Run Forecasting Models** to train and evaluate.")

    with tab_forecast:
        if "ts_results" not in st.session_state:
            st.info("Run models first in the **Model Training** tab.")
        else:
            from statsmodels.tsa.arima.model import ARIMA
            import matplotlib.pyplot as plt

            r = st.session_state["ts_results"]
            horizon = st.slider("Forecast horizon (weeks)", 4, 12, 4)

            if st.button("🔮 Generate Future Forecast"):
                with st.spinner("Forecasting…"):
                    order = r["order"]
                    final_m = ARIMA(ts_weekly["Quantite_Semaine"], order=order)
                    final_f = final_m.fit(method_kwargs={"warn_convergence": False})
                    future_pred = final_f.forecast(steps=horizon)

                    last_date = ts_weekly["DateTransaction"].iloc[-1]
                    future_dates = pd.date_range(
                        start=last_date + pd.Timedelta(weeks=1), periods=horizon, freq="W")

                    future_df = pd.DataFrame({
                        "Week": future_dates.strftime("%Y-%m-%d"),
                        "Forecasted Quantity": future_pred.values.round(2)
                    })

                c1, c2 = st.columns([1, 2])
                with c1:
                    st.markdown("**📅 Future Predictions**")
                    st.dataframe(future_df, use_container_width=True, hide_index=True)

                with c2:
                    fig, ax = plt.subplots(figsize=(9, 5))
                    fig.patch.set_facecolor("#0d2318"); ax.set_facecolor("#111f16")
                    ax.plot(ts_weekly["DateTransaction"], ts_weekly["Quantite_Semaine"],
                            color="#2ecc71", lw=2, label="Historical")
                    ax.plot(future_dates, future_pred.values,
                            color="#f1c40f", lw=2.5, ls="--", marker="o",
                            markersize=6, label=f"Forecast ({horizon}w)")
                    ax.axvline(ts_weekly["DateTransaction"].iloc[-1],
                               color="#555", ls=":", lw=1.5, label="Today")
                    ax.set_title(f"ARIMA Forecast — Next {horizon} Weeks", color="#f0faf4", fontsize=13)
                    ax.set_xlabel("Date", color="#7fb894"); ax.set_ylabel("Quantity", color="#7fb894")
                    ax.tick_params(colors="#7fb894"); ax.legend(labelcolor="#f0faf4", facecolor="#111f16")
                    ax.grid(True, alpha=0.2, color="#1e5c34")
                    for sp in ax.spines.values(): sp.set_edgecolor("#1e5c34")
                    fig.tight_layout(); st.pyplot(fig); plt.close()



# ─────────────────────────────────────────────
# PAGE: MANUAL PREDICTION  ★★★ HERO SECTION ★★★
# ─────────────────────────────────────────────
elif nav == "🔮 Manual Prediction":
    if not require_connection():
        st.stop()

    # ══ FUTURISTIC CSS ══════════════════════════════════════════════════
    st.markdown("""
    <style>
    @keyframes pulseGlow {
      0%,100%{ box-shadow:0 0 24px rgba(46,204,113,.3),0 0 60px rgba(46,204,113,.08); }
      50%    { box-shadow:0 0 48px rgba(46,204,113,.6),0 0 100px rgba(46,204,113,.18); }
    }
    @keyframes fadeUp {
      from{ opacity:0; transform:translateY(14px); }
      to  { opacity:1; transform:translateY(0); }
    }
    @keyframes borderPulse {
      0%,100%{ border-color:rgba(46,204,113,.35); }
      50%    { border-color:rgba(46,204,113,.85); }
    }
    @keyframes borderPulseRed {
      0%,100%{ border-color:rgba(231,76,60,.35); }
      50%    { border-color:rgba(231,76,60,.85); }
    }
    .pred-hero{
      background:linear-gradient(135deg,#040c07 0%,#091a0f 45%,#0d2318 100%);
      border:1px solid rgba(46,204,113,.3); border-radius:24px;
      padding:36px 40px; margin-bottom:28px; position:relative; overflow:hidden;
      animation:pulseGlow 4s ease-in-out infinite;
    }
    .pred-hero::before{
      content:''; position:absolute; inset:0;
      background:repeating-linear-gradient(0deg,transparent,transparent 2px,
                  rgba(46,204,113,.012) 2px,rgba(46,204,113,.012) 4px);
      pointer-events:none;
    }
    .pred-hero-title{
      font-size:2.1rem; font-weight:900; letter-spacing:-1px;
      background:linear-gradient(90deg,#2ecc71,#1abc9c,#f1c40f);
      -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
    }
    .pred-panel{
      background:linear-gradient(160deg,#060e08,#0d2318);
      border:1px solid rgba(46,204,113,.18); border-radius:20px;
      padding:28px 30px; animation:fadeUp .4s ease forwards;
    }
    .grp-label{
      font-size:.68rem; font-weight:700; letter-spacing:2.5px;
      text-transform:uppercase; color:#3d9b60; margin-bottom:14px;
      display:flex; align-items:center; gap:10px;
    }
    .grp-label::after{
      content:''; flex:1; height:1px;
      background:linear-gradient(90deg,rgba(46,204,113,.3),transparent);
    }
    /* Result cards */
    .res-card{
      border-radius:20px; padding:30px 24px; text-align:center;
      position:relative; overflow:hidden; animation:fadeUp .5s ease forwards;
    }
    .res-card-yes{
      background:linear-gradient(135deg,#040f07,#0b2312);
      border:2px solid rgba(46,204,113,.5);
      box-shadow:0 0 60px rgba(46,204,113,.2),inset 0 0 30px rgba(46,204,113,.04);
      animation:borderPulse 3s ease-in-out infinite, fadeUp .5s ease forwards;
    }
    .res-card-no{
      background:linear-gradient(135deg,#0f0404,#230b0b);
      border:2px solid rgba(231,76,60,.5);
      box-shadow:0 0 60px rgba(231,76,60,.2),inset 0 0 30px rgba(231,76,60,.04);
      animation:borderPulseRed 3s ease-in-out infinite, fadeUp .5s ease forwards;
    }
    .res-card-reg{
      background:linear-gradient(135deg,#04090f,#0b1a23);
      border:2px solid rgba(26,188,156,.5);
      box-shadow:0 0 60px rgba(26,188,156,.2),inset 0 0 30px rgba(26,188,156,.04);
    }
    .res-card-clust{
      background:linear-gradient(135deg,#0f0c04,#231e0b);
      border:2px solid rgba(241,196,15,.5);
      box-shadow:0 0 60px rgba(241,196,15,.15),inset 0 0 30px rgba(241,196,15,.03);
    }
    .res-big-num{
      font-size:3.6rem; font-weight:900; line-height:1;
      letter-spacing:-2px; margin:10px 0 6px;
    }
    .res-lbl{ font-size:.68rem; text-transform:uppercase; letter-spacing:2.5px; font-weight:700; opacity:.55; }
    .res-sub{ font-size:.86rem; margin-top:10px; opacity:.72; line-height:1.55; }
    .conf-track{
      background:rgba(255,255,255,.07); border-radius:99px;
      height:7px; margin:14px 0 5px; overflow:hidden;
    }
    .conf-fill{
      height:100%; border-radius:99px;
      background:linear-gradient(90deg,#1e8449,#2ecc71);
    }
    .sum-grid{ display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin-top:18px; }
    .sum-cell{
      background:rgba(255,255,255,.025); border:1px solid rgba(46,204,113,.1);
      border-radius:14px; padding:15px 10px; text-align:center;
    }
    .sum-val{ font-size:1.2rem; font-weight:800; color:#f0faf4; }
    .sum-lbl{ font-size:.64rem; text-transform:uppercase; letter-spacing:1.5px; color:#3d9b60; margin-top:4px; }
    .insight-box{
      background:rgba(46,204,113,.04); border:1px solid rgba(46,204,113,.18);
      border-left:3px solid #2ecc71; border-radius:12px;
      padding:18px 22px; margin-top:18px;
    }
    .clust-pill{
      display:inline-block; padding:5px 16px; border-radius:99px;
      font-size:.78rem; font-weight:700; letter-spacing:.5px; margin-top:10px;
    }
    .tab-header{
      font-size:1.05rem; font-weight:700; color:#f0faf4;
      margin-bottom:20px; display:flex; align-items:center; gap:10px;
    }
    .model-pill{
      display:inline-flex; align-items:center; gap:6px;
      background:rgba(46,204,113,.1); border:1px solid rgba(46,204,113,.25);
      border-radius:99px; padding:4px 12px; font-size:.72rem; font-weight:600;
      color:#2ecc71; letter-spacing:.5px;
    }
    .divider-line{
      border:none; height:1px;
      background:linear-gradient(90deg,transparent,rgba(46,204,113,.3),transparent);
      margin:24px 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # ══ HERO BANNER ══════════════════════════════════════════════════════
    st.markdown("""
    <div class='pred-hero'>
      <div style='display:flex; align-items:center; gap:18px;'>
        <div style='font-size:3rem; filter:drop-shadow(0 0 12px #2ecc71);'>🔮</div>
        <div>
          <div class='pred-hero-title'>Manual Prediction Studio</div>
          <div style='color:#5ab87a; font-size:.9rem; margin-top:6px; letter-spacing:.3px;'>
            Three independent ML engines — each with its own inputs, logic, and live results
          </div>
        </div>
        <div style='margin-left:auto; display:flex; gap:10px; flex-wrap:wrap;'>
          <span class='model-pill'>🎯 GBClassifier</span>
          <span class='model-pill' style='color:#1abc9c;border-color:rgba(26,188,156,.3);background:rgba(26,188,156,.1);'>📦 RandomForest</span>
          <span class='model-pill' style='color:#f1c40f;border-color:rgba(241,196,15,.3);background:rgba(241,196,15,.1);'>🔵 KMeans</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ══ LOAD DATA & TRAIN MODELS ══════════════════════════════════════════
    with st.spinner("⚙️ Loading data & training models…"):
        try:
            engine = st.session_state.engine
            fact_all = pd.read_sql("SELECT * FROM dbo.FactTransaction", engine)
            dim_prod = pd.read_sql("SELECT * FROM dbo.DimProduit", engine)
            dim_part = pd.read_sql("SELECT * FROM dbo.DimPartner", engine)
        except Exception as e:
            st.error(f"Data load error: {e}"); st.stop()

    from sklearn.preprocessing import LabelEncoder, StandardScaler, RobustScaler
    from sklearn.compose import ColumnTransformer
    from sklearn.pipeline import Pipeline
    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import OneHotEncoder
    from sklearn.ensemble import GradientBoostingClassifier, RandomForestRegressor
    from sklearn.cluster import KMeans
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mticker

    # Clean dim_prod
    for col in ["PrixVenteHT", "PrixAchatHT"]:
        dim_prod[col] = pd.to_numeric(dim_prod[col], errors="coerce")
        dim_prod[col].fillna(dim_prod[col].median(), inplace=True)
    for col in ["Famille", "SousFamille", "Marque"]:
        if col in dim_prod.columns:
            dim_prod[col] = dim_prod[col].astype("string").str.strip().fillna("Unknown")

    familles      = sorted(dim_prod["Famille"].dropna().unique().tolist()) if "Famille" in dim_prod.columns else ["Unknown"]
    marques       = sorted(dim_prod["Marque"].dropna().unique().tolist())  if "Marque"  in dim_prod.columns else ["Unknown"]
    genders       = sorted(dim_prod["Target_Gender"].dropna().unique().tolist()) if "Target_Gender" in dim_prod.columns else ["M","F","Unisex","Unknown"]
    ages          = sorted(dim_prod["Target_Age"].dropna().unique().tolist())    if "Target_Age"    in dim_prod.columns else ["Child","Adults(18+)","Senior","Unknown"]
    type_partners = sorted(dim_part["TypePartner"].dropna().unique().tolist())   if "TypePartner"   in dim_part.columns else ["Retail","Wholesale","Online","Unknown"]

    # ── Model 1: GBClassifier — predicts if customer RETURNS ────────────
    @st.cache_resource(show_spinner=False)
    def train_clf(_fact, _prod, _part):
        df = _fact.copy()
        for col in ["Quantite_Produit","IsPaid","TotalDiscount"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        df["Quantite_Produit"].fillna(df["Quantite_Produit"].median(), inplace=True)
        df["IsPaid"].fillna(0, inplace=True)
        df["TotalDiscount"].fillna(0, inplace=True)
        if "FK_Partner" in df.columns and "PartnerPK" in _part.columns:
            df = df.merge(_part[["PartnerPK","TypePartner"]], left_on="FK_Partner", right_on="PartnerPK", how="left")
        if "FK_Produit" in df.columns and "ProduitPK" in _prod.columns:
            df = df.merge(_prod[["ProduitPK","Target_Gender","Target_Age"]], left_on="FK_Produit", right_on="ProduitPK", how="left")
        if "DocumentNumber" in df.columns and "FK_Partner" in df.columns:
            pc = df.groupby("FK_Partner")["DocumentNumber"].nunique()
            df["NbT"] = df["FK_Partner"].map(pc)
            df["Target"] = (df["NbT"] > 1).astype(int)
        else:
            df["Target"] = 1
        for col in ["Target_Gender","Target_Age","TypePartner"]:
            if col not in df.columns: df[col] = "Unknown"
            df[col] = df[col].astype("string").str.strip().fillna("Unknown")
        X = df[["IsPaid","Quantite_Produit","TotalDiscount","Target_Gender","Target_Age","TypePartner"]]
        y = df["Target"]
        pre = ColumnTransformer([
            ("num", Pipeline([("imp", SimpleImputer(strategy="median")),("sc", StandardScaler())]),
             ["IsPaid","Quantite_Produit","TotalDiscount"]),
            ("cat", Pipeline([("imp", SimpleImputer(strategy="most_frequent")),
                              ("ohe", OneHotEncoder(handle_unknown="ignore"))]),
             ["Target_Gender","Target_Age","TypePartner"])
        ])
        mdl = Pipeline([("pre", pre), ("m", GradientBoostingClassifier(
            n_estimators=150, learning_rate=0.05, max_depth=3, random_state=42))])
        mdl.fit(X, y)
        return mdl

    # ── Model 2: RandomForestRegressor — predicts QUANTITY SOLD ──────────
    # Features: product price/cost/discount/margin ratios + brand + family + date
    # (Quantity is the TARGET — we do NOT use it as input here)
    @st.cache_resource(show_spinner=False)
    def train_reg(_fact, _prod):
        fr = _fact.copy()
        if "TransactionType" in fr.columns:
            fr = fr[fr["TransactionType"] == 2]
        for col in ["Quantite_Produit","Prix_Totale","TotalDiscount"]:
            fr[col] = pd.to_numeric(fr[col], errors="coerce")
        fr["Quantite_Produit"].fillna(fr["Quantite_Produit"].median(), inplace=True)
        fr["Prix_Totale"].fillna(fr["Prix_Totale"].median(), inplace=True)
        fr["TotalDiscount"].fillna(0, inplace=True)
        pc = _prod.copy()
        for col in ["PrixVenteHT","PrixAchatHT"]:
            pc[col] = pd.to_numeric(pc[col], errors="coerce")
            pc[col].fillna(pc[col].median(), inplace=True)
        for col in ["Famille","Marque"]:
            if col in pc.columns:
                pc[col] = pc[col].astype("string").str.strip().fillna("Unknown")
        if "FK_Produit" not in fr.columns or "ProduitPK" not in pc.columns:
            return None, None, None
        rdf = fr.merge(pc[["ProduitPK","Famille","Marque","PrixVenteHT","PrixAchatHT"]],
                       left_on="FK_Produit", right_on="ProduitPK", how="inner")
        for col in rdf.select_dtypes(include="number").columns:
            if (rdf[col] < 0).any(): rdf[col] = rdf[col].abs()
        rdf = rdf[rdf["Quantite_Produit"] > 0]
        q01, q99 = rdf["Quantite_Produit"].quantile([0.01, 0.99])
        rdf = rdf[(rdf["Quantite_Produit"] >= q01) & (rdf["Quantite_Produit"] <= q99)]
        if "DateTransaction" in rdf.columns:
            rdf["DateTransaction"] = pd.to_datetime(rdf["DateTransaction"], errors="coerce")
            rdf["Mois"]   = rdf["DateTransaction"].dt.month.fillna(1).astype(int)
            rdf["JourSem"] = rdf["DateTransaction"].dt.dayofweek.fillna(0).astype(int)
            rdf["Annee"]  = rdf["DateTransaction"].dt.year.fillna(2024).astype(int)
        else:
            rdf["Mois"] = 1; rdf["JourSem"] = 0; rdf["Annee"] = 2024
        rdf["Marge_HT"]             = rdf["PrixVenteHT"] - rdf["PrixAchatHT"]
        rdf["Ratio_Remise"]         = rdf["TotalDiscount"] / (rdf["PrixVenteHT"] + 1)
        rdf["Prix_Achat_Vente_Ratio"] = rdf["PrixAchatHT"]  / (rdf["PrixVenteHT"] + 1)
        le_m = LabelEncoder(); le_m.fit(rdf["Marque"].astype(str))
        le_f = LabelEncoder(); le_f.fit(rdf["Famille"].astype(str))
        rdf["Marque_enc"]  = le_m.transform(rdf["Marque"].astype(str))
        rdf["Famille_enc"] = le_f.transform(rdf["Famille"].astype(str))
        FEATS = ["TotalDiscount","PrixVenteHT","PrixAchatHT","Marge_HT",
                 "Ratio_Remise","Prix_Achat_Vente_Ratio","Mois","JourSem","Annee",
                 "Marque_enc","Famille_enc"]
        mdl = RandomForestRegressor(n_estimators=200, max_depth=12, random_state=42, n_jobs=-1)
        mdl.fit(rdf[FEATS], rdf["Quantite_Produit"])
        return mdl, le_m, le_f

    # ── Model 3: KMeans — trains on product aggregates ────────────────────
    @st.cache_resource(show_spinner=False)
    def train_kmeans(_fact, _prod, k=5):
        fa = _fact.copy()
        for col in ["Quantite_Produit","Prix_Totale","TotalDiscount"]:
            fa[col] = pd.to_numeric(fa[col], errors="coerce").abs().fillna(0)
        if "FK_Produit" not in fa.columns: return None, None
        agg = fa.groupby("FK_Produit", as_index=False).agg(
            Quantite_Produit=("Quantite_Produit","sum"),
            Prix_Totale=("Prix_Totale","sum"),
            TotalDiscount=("TotalDiscount","sum")
        ).rename(columns={"FK_Produit":"ProduitPK"})
        pc = _prod.copy()
        for col in ["PrixVenteHT","PrixAchatHT"]:
            pc[col] = pd.to_numeric(pc[col], errors="coerce")
            pc[col].fillna(pc[col].median(), inplace=True)
        cdf = agg.merge(pc[["ProduitPK","PrixVenteHT","PrixAchatHT"]], on="ProduitPK", how="inner")
        cdf["Marge"] = cdf["PrixVenteHT"] - cdf["PrixAchatHT"]
        COLS = ["Quantite_Produit","Prix_Totale","TotalDiscount","PrixVenteHT","PrixAchatHT","Marge"]
        for c in COLS:
            cdf[c] = pd.to_numeric(cdf[c], errors="coerce")
            cdf[c].fillna(cdf[c].median(), inplace=True)
        cdf = cdf.dropna(subset=COLS).reset_index(drop=True)
        if len(cdf) == 0: return None, None
        sc = RobustScaler()
        Xs = sc.fit_transform(cdf[COLS])
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        km.fit(Xs)
        return km, sc

    clf_model            = train_clf(fact_all, dim_prod, dim_part)
    reg_model, le_m, le_f = train_reg(fact_all, dim_prod)
    km_model, km_scaler  = train_kmeans(fact_all, dim_prod)

    def safe_enc(le, val):
        try: return int(le.transform([str(val)])[0])
        except: return 0

    # cluster name map
    CLUSTER_MAP = {
        0: ("Promo Performer",        "#2ecc71", "rgba(46,204,113,.15)",  "rgba(46,204,113,.35)"),
        1: ("Low Performance",        "#e74c3c", "rgba(231,76,60,.15)",   "rgba(231,76,60,.35)"),
        2: ("Star Product ⭐",         "#f1c40f", "rgba(241,196,15,.15)",  "rgba(241,196,15,.35)"),
        3: ("High Rotation Low Margin","#1abc9c", "rgba(26,188,156,.15)", "rgba(26,188,156,.35)"),
        4: ("Premium Low Rotation",   "#9b59b6", "rgba(155,89,182,.15)", "rgba(155,89,182,.35)"),
    }

    # ══ THREE TABS — one per model ═════════════════════════════════════════
    tab_clf, tab_reg, tab_clust = st.tabs([
        "🎯  Customer Return  (Classifier)",
        "📦  Sales Quantity  (Regressor)",
        "🔵  Product Segment  (Clustering)",
    ])

    # ───────────────────────────────────────────────────────────────────
    # TAB 1 — CLASSIFICATION
    # ───────────────────────────────────────────────────────────────────
    with tab_clf:
        st.markdown("""
        <div style='background:rgba(46,204,113,.04);border:1px solid rgba(46,204,113,.15);
                    border-radius:14px;padding:14px 18px;margin-bottom:22px;'>
          <b style='color:#2ecc71;'>What this model does:</b>
          <span style='color:#a9dfbf;font-size:.88rem;'>
            Predicts whether a customer will <b>return</b> for another purchase based on their
            transaction profile. Uses <b>Gradient Boosting</b> trained on IsPaid, Quantity,
            Discount, Gender, Age group and Partner type.
          </span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='pred-panel'>", unsafe_allow_html=True)

        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.markdown("<div class='grp-label'>🛒 Transaction</div>", unsafe_allow_html=True)
            clf_ispaid  = st.selectbox("IsPaid", [1, 0], format_func=lambda x: "✅ Paid" if x else "❌ Unpaid", key="clf_paid")
            clf_qty     = st.number_input("Quantity Sold", min_value=0.0, max_value=10000.0, value=10.0, step=1.0, key="clf_qty",
                                          help="How many units were bought in this transaction")
            clf_disc    = st.number_input("Total Discount (TND)", min_value=0.0, max_value=100000.0, value=5.0, step=1.0, key="clf_disc")

            if clf_disc == 1:
                clf_disc = 50
            elif clf_disc >= 10:  # Note: elif, not if
                clf_disc = 1

        with col_b:
            st.markdown("<div class='grp-label'>👤 Customer Profile</div>", unsafe_allow_html=True)
            clf_gender  = st.selectbox("Target Gender",  genders,       key="clf_gender")
            clf_age     = st.selectbox("Target Age Group", ages,         key="clf_age")
            clf_partner = 2

        with col_c:
            st.markdown("<div class='grp-label'>🧠 Live Feature Preview</div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div style='background:rgba(0,0,0,.3);border:1px solid rgba(46,204,113,.1);
                        border-radius:12px;padding:16px;font-size:.82rem;color:#7fb894;line-height:2;'>
              <b style='color:#2ecc71;'>IsPaid</b> → {clf_ispaid}<br/>
              <b style='color:#2ecc71;'>Quantity</b> → {clf_qty:.0f} units<br/>
              <b style='color:#2ecc71;'>Discount</b> → {clf_disc:.2f} TND<br/>
              <b style='color:#2ecc71;'>Gender</b> → {clf_gender}<br/>
              <b style='color:#2ecc71;'>Age</b> → {clf_age}<br/>
              <b style='color:#2ecc71;'>Partner</b> → {clf_partner}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<br/>", unsafe_allow_html=True)

        if st.button("⚡ Predict Customer Return", use_container_width=True, key="run_clf"):
            clf_input = pd.DataFrame([{
                "IsPaid": clf_ispaid, "Quantite_Produit": clf_qty,
                "TotalDiscount": clf_disc, "Target_Gender": clf_gender,
                "Target_Age": clf_age, "TypePartner": clf_partner
            }])
            clf_pred  = int(clf_model.predict(clf_input)[0])
            clf_proba = float(clf_model.predict_proba(clf_input)[0][1])

            card_cls  = "res-card-yes" if clf_pred == 1 else "res-card-no"
            main_col  = "#2ecc71"      if clf_pred == 1 else "#e74c3c"
            icon      = "🔄"           if clf_pred == 1 else "🚪"
            label     = "RETURNING"    if clf_pred == 1 else "NON-RETURNING"
            verdict   = ("This customer is highly likely to come back. Consider loyalty rewards, upsell campaigns and premium offers."
                         if clf_pred == 1 else
                         "This customer shows churn patterns. Trigger a win-back campaign with a personalised discount.")
            bar_pct   = int(clf_proba * 100)

            r1, r2, r3 = st.columns([1.4, 1, 1])
            with r1:
                st.markdown(f"""
                <div class='res-card {card_cls}'>
                  <div style='font-size:3rem;filter:drop-shadow(0 0 10px {main_col});'>{icon}</div>
                  <div class='res-big-num' style='color:{main_col};'>{label}</div>
                  <div class='res-lbl' style='color:{main_col};margin-top:6px;'>Customer Classification</div>
                  <div style='margin-top:18px;'>
                    <div class='res-lbl'>Returning Probability</div>
                    <div class='conf-track'>
                      <div class='conf-fill' style='width:{bar_pct}%;background:linear-gradient(90deg,#1e8449,{main_col});'></div>
                    </div>
                    <div style='font-size:2rem;font-weight:900;color:{main_col};'>{clf_proba*100:.1f}%</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

            with r2:
                st.markdown(f"""
                <div class='res-card' style='background:rgba(255,255,255,.02);
                     border:1px solid rgba(46,204,113,.15);border-radius:18px;
                     padding:24px;text-align:left;height:100%;'>
                  <div class='res-lbl' style='margin-bottom:12px;'>Model Details</div>
                  <div style='font-size:.83rem;color:#a9dfbf;line-height:1.9;'>
                    <b style='color:#f0faf4;'>Algorithm</b><br/>Gradient Boosting<br/><br/>
                    <b style='color:#f0faf4;'>Features Used</b><br/>
                    IsPaid · Qty · Discount<br/>Gender · Age · Partner<br/><br/>
                    <b style='color:#f0faf4;'>Training Target</b><br/>
                    Repeat purchase (>1 doc)
                  </div>
                </div>
                """, unsafe_allow_html=True)

            with r3:
                conf_level = "HIGH" if clf_proba > 0.75 or clf_proba < 0.25 else "MEDIUM" if clf_proba > 0.55 or clf_proba < 0.45 else "LOW"
                conf_col   = "#2ecc71" if conf_level == "HIGH" else "#f1c40f" if conf_level == "MEDIUM" else "#e74c3c"
                st.markdown(f"""
                <div class='res-card' style='background:rgba(255,255,255,.02);
                     border:1px solid rgba(46,204,113,.15);border-radius:18px;
                     padding:24px;text-align:center;height:100%;'>
                  <div class='res-lbl'>Confidence Level</div>
                  <div style='font-size:2.2rem;font-weight:900;color:{conf_col};margin:14px 0 6px;'>{conf_level}</div>
                  <div style='font-size:.8rem;color:#7fb894;'>
                    {"Model is very confident in this prediction." if conf_level=="HIGH" else
                     "Moderate confidence — borderline case." if conf_level=="MEDIUM" else
                     "Low confidence — result is near 50/50."}
                  </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class='insight-box'>
              <div style='font-size:.78rem;font-weight:700;color:#2ecc71;letter-spacing:1.5px;
                          text-transform:uppercase;margin-bottom:8px;'>💡 Business Insight</div>
              <div style='color:#d5f5e3;font-size:.9rem;line-height:1.65;'>{verdict}</div>
            </div>
            """, unsafe_allow_html=True)

    # ───────────────────────────────────────────────────────────────────
    # TAB 2 — REGRESSION
    # ───────────────────────────────────────────────────────────────────
    with tab_reg:
        st.markdown("""
        <div style='background:rgba(26,188,156,.04);border:1px solid rgba(26,188,156,.15);
                    border-radius:14px;padding:14px 18px;margin-bottom:22px;'>
          <b style='color:#1abc9c;'>What this model does:</b>
          <span style='color:#a9dfbf;font-size:.88rem;'>
            Given a product's <b>price, cost, discount, brand, family and the sale date</b>,
            it predicts <b>how many units will be sold</b>.
            Uses <b>Random Forest Regressor</b>. Quantity is the output — <em>not</em> an input.
          </span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='pred-panel'>", unsafe_allow_html=True)
        col_a, col_b, col_c = st.columns(3)

        with col_a:
            st.markdown("<div class='grp-label'>💰 Pricing</div>", unsafe_allow_html=True)
            reg_pvente = st.number_input("Selling Price HT (TND)", min_value=0.0, max_value=1e6, value=50.0, step=0.5, key="reg_pv")
            reg_pachat = st.number_input("Purchase Price HT (TND)", min_value=0.0, max_value=1e6, value=35.0, step=0.5, key="reg_pa")
            reg_disc = st.number_input("Total Discount (TND)", min_value=0.0, max_value=1e5, value=5.0, step=1.0, key="reg_disc")

        



        with col_b:
            st.markdown("<div class='grp-label'>📦 Product</div>", unsafe_allow_html=True)
            reg_famille = st.selectbox("Famille", familles, key="reg_fam")
            reg_marque  = st.selectbox("Marque",  marques,  key="reg_marq")

        with col_c:
            st.markdown("<div class='grp-label'>📅 Date Context</div>", unsafe_allow_html=True)
            reg_mois    = st.slider("Month", 1, 12, 6, key="reg_mois")
            reg_joursem = st.selectbox("Day of Week", [0,1,2,3,4,5,6],
                                       format_func=lambda x: ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"][x],
                                       key="reg_jour")
            reg_annee   = st.number_input("Year", min_value=2020, max_value=2030, value=2025, step=1, key="reg_year")

        # Computed preview
        reg_marge = reg_pvente - reg_pachat
        reg_ratio_remise = reg_disc / (reg_pvente + 1)
        reg_ratio_av     = reg_pachat / (reg_pvente + 1)

        st.markdown("<hr class='divider-line'/>", unsafe_allow_html=True)
        pc1, pc2, pc3, pc4 = st.columns(4)
        pc1.metric("Margin / Unit", f"{reg_marge:.2f} TND")
        pc2.metric("Margin %", f"{(reg_marge/reg_pvente*100) if reg_pvente>0 else 0:.1f}%")
        pc3.metric("Discount Rate", f"{reg_ratio_remise*100:.1f}%")
        pc4.metric("Cost/Price Ratio", f"{reg_ratio_av:.3f}")

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<br/>", unsafe_allow_html=True)

        if st.button("⚡ Predict Sales Quantity", use_container_width=True, key="run_reg"):
            if reg_model is None:
                st.error("Regression model could not be trained — check FK_Produit column in FactTransaction.")
            else:
                me  = safe_enc(le_m, reg_marque)
                fe  = safe_enc(le_f, reg_famille)
                reg_input = pd.DataFrame([{
                    "TotalDiscount": reg_disc, "PrixVenteHT": reg_pvente,
                    "PrixAchatHT": reg_pachat, "Marge_HT": reg_marge,
                    "Ratio_Remise": reg_ratio_remise, "Prix_Achat_Vente_Ratio": reg_ratio_av,
                    "Mois": reg_mois, "JourSem": reg_joursem, "Annee": reg_annee,
                    "Marque_enc": me, "Famille_enc": fe
                }])
                reg_pred    = float(reg_model.predict(reg_input)[0])
                rev_est     = reg_pred * reg_pvente
                profit_est  = reg_pred * reg_marge
                net_margin  = (reg_marge / reg_pvente * 100) if reg_pvente > 0 else 0

                r1, r2 = st.columns([1.2, 1])
                with r1:
                    st.markdown(f"""
                    <div class='res-card res-card-reg'>
                      <div style='font-size:2.8rem;filter:drop-shadow(0 0 10px #1abc9c);'>📦</div>
                      <div class='res-lbl' style='color:#1abc9c;margin-top:8px;'>Predicted Units to Sell</div>
                      <div class='res-big-num' style='color:#1abc9c;'>{reg_pred:.1f}</div>
                      <div class='res-sub' style='color:#76d7c4;'>units expected for this product profile</div>
                      <div class='conf-track'>
                        <div class='conf-fill' style='width:70%;background:linear-gradient(90deg,#0e6655,#1abc9c);'></div>
                      </div>
                    </div>
                    """, unsafe_allow_html=True)

                with r2:
                    fi_pairs = list(zip(
                        ["TotalDiscount","PrixVenteHT","PrixAchatHT","Marge_HT","Ratio_Remise","Prix_Achat_Vente_Ratio","Mois","JourSem","Annee","Marque_enc","Famille_enc"],
                        reg_model.feature_importances_
                    ))
                    fi_pairs.sort(key=lambda x: x[1], reverse=True)
                    top5 = fi_pairs[:5]
                    fig_fi, ax_fi = plt.subplots(figsize=(5, 3))
                    fig_fi.patch.set_facecolor("#060e08"); ax_fi.set_facecolor("#0a1a0f")
                    names_fi  = [p[0] for p in top5]
                    vals_fi   = [p[1] for p in top5]
                    colors_fi = ["#1abc9c","#27ae60","#2ecc71","#48c9b0","#76d7c4"]
                    ax_fi.barh(names_fi[::-1], vals_fi[::-1], color=colors_fi)
                    ax_fi.set_title("Top Feature Importances", color="#f0faf4", fontsize=10)
                    ax_fi.tick_params(colors="#7fb894", labelsize=8)
                    ax_fi.set_xlabel("Importance", color="#7fb894", fontsize=8)
                    for sp in ax_fi.spines.values(): sp.set_edgecolor("#1e5c34")
                    fig_fi.tight_layout()
                    st.pyplot(fig_fi); plt.close()

                st.markdown(f"""
                <div class='sum-grid'>
                  <div class='sum-cell'>
                    <div class='sum-val' style='color:#1abc9c;'>{reg_pred:.1f}</div>
                    <div class='sum-lbl'>Predicted Units</div>
                  </div>
                  <div class='sum-cell'>
                    <div class='sum-val' style='color:#2ecc71;'>{rev_est:,.0f} TND</div>
                    <div class='sum-lbl'>Est. Revenue</div>
                  </div>
                  <div class='sum-cell'>
                    <div class='sum-val' style='color:#f1c40f;'>{profit_est:,.0f} TND</div>
                    <div class='sum-lbl'>Est. Gross Profit</div>
                  </div>
                  <div class='sum-cell'>
                    <div class='sum-val' style='color:#e67e22;'>{net_margin:.1f}%</div>
                    <div class='sum-lbl'>Net Margin</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

                margin_note = (f"Healthy margin at {net_margin:.0f}% — pricing is well calibrated."
                               if net_margin > 25 else
                               f"Tight margin at {net_margin:.0f}% — consider reviewing cost structure or pricing."
                               if net_margin > 10 else
                               f"Very low margin ({net_margin:.0f}%) — this product may be loss-making. Review urgently.")

                st.markdown(f"""
                <div class='insight-box' style='border-left-color:#1abc9c;'>
                  <div style='font-size:.78rem;font-weight:700;color:#1abc9c;letter-spacing:1.5px;
                              text-transform:uppercase;margin-bottom:8px;'>📊 Sales Insight</div>
                  <div style='color:#d5f5e3;font-size:.9rem;line-height:1.65;'>
                    The model predicts <b>{reg_pred:.1f} units</b> sold for <b>{reg_marque}</b>
                    in the <b>{reg_famille}</b> family at <b>{reg_pvente:.2f} TND</b> sell price
                    in month <b>{reg_mois}</b>.
                    This generates an estimated revenue of <b>{rev_est:,.0f} TND</b>
                    and gross profit of <b>{profit_est:,.0f} TND</b>.<br/>
                    {margin_note}
                  </div>
                </div>
                """, unsafe_allow_html=True)

    # ───────────────────────────────────────────────────────────────────
    # TAB 3 — CLUSTERING
    # ───────────────────────────────────────────────────────────────────
    with tab_clust:
        st.markdown("""
        <div style='background:rgba(241,196,15,.04);border:1px solid rgba(241,196,15,.15);
                    border-radius:14px;padding:14px 18px;margin-bottom:22px;'>
          <b style='color:#f1c40f;'>What this model does:</b>
          <span style='color:#a9dfbf;font-size:.88rem;'>
            Assigns a product to one of <b>5 KMeans clusters</b> based on its sales volume,
            revenue, discounts, sell price, purchase price and margin.
            Tells you <b>what segment this product belongs to</b>.
          </span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='pred-panel'>", unsafe_allow_html=True)
        col_a, col_b, col_c = st.columns(3)

        with col_a:
            st.markdown("<div class='grp-label'>📊 Sales Volume</div>", unsafe_allow_html=True)
            cl_qty    = st.number_input("Total Quantity Sold", min_value=0.0, max_value=1e7, value=500.0, step=10.0, key="cl_qty",
                                        help="Aggregated quantity sold across all transactions for this product")
            cl_rev    = st.number_input("Total Revenue (TND)", min_value=0.0, max_value=1e9, value=25000.0, step=100.0, key="cl_rev",
                                        help="Total Prix_Totale summed across all transactions")
            cl_disc   = st.number_input("Total Discounts (TND)", min_value=0.0, max_value=1e8, value=1000.0, step=50.0, key="cl_disc")

        with col_b:
            st.markdown("<div class='grp-label'>💲 Unit Economics</div>", unsafe_allow_html=True)
            cl_pvente = st.number_input("Unit Selling Price HT (TND)", min_value=0.0, max_value=1e6, value=50.0, step=0.5, key="cl_pv")
            cl_pachat = st.number_input("Unit Purchase Price HT (TND)", min_value=0.0, max_value=1e6, value=35.0, step=0.5, key="cl_pa")

        cl_marge = cl_pvente - cl_pachat

        with col_c:
            st.markdown("<div class='grp-label'>📐 Computed Metrics</div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div style='background:rgba(241,196,15,.04);border:1px solid rgba(241,196,15,.12);
                        border-radius:12px;padding:18px;font-size:.85rem;line-height:2.1;color:#a9dfbf;'>
              <b style='color:#f1c40f;'>Margin / Unit</b> → {cl_marge:.2f} TND<br/>
              <b style='color:#f1c40f;'>Margin %</b> → {(cl_marge/cl_pvente*100) if cl_pvente>0 else 0:.1f}%<br/>
              <b style='color:#f1c40f;'>Disc/Rev Ratio</b> → {(cl_disc/cl_rev*100) if cl_rev>0 else 0:.1f}%<br/>
              <b style='color:#f1c40f;'>Avg Unit Rev</b> → {(cl_rev/cl_qty) if cl_qty>0 else 0:.2f} TND
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<br/>", unsafe_allow_html=True)

        if st.button("⚡ Assign Product Cluster", use_container_width=True, key="run_clust"):
            if km_model is None or km_scaler is None:
                st.error("KMeans model could not be trained — check your data.")
            else:
                user_pt = km_scaler.transform([[cl_qty, cl_rev, cl_disc, cl_pvente, cl_pachat, cl_marge]])
                user_cluster = int(km_model.predict(user_pt)[0])
                c_name, c_col, c_bg, c_border = CLUSTER_MAP.get(user_cluster, ("Unknown","#7fb894","rgba(127,184,148,.15)","rgba(127,184,148,.35)"))

                # Distance to all centroids (how close to each cluster)
                dists = np.linalg.norm(km_model.cluster_centers_ - user_pt, axis=1)
                closest_order = np.argsort(dists)

                r1, r2 = st.columns([1.2, 1])
                with r1:
                    st.markdown(f"""
                    <div class='res-card res-card-clust' style='border-color:{c_border};
                         box-shadow:0 0 60px {c_bg};'>
                      <div style='font-size:2.8rem;filter:drop-shadow(0 0 10px {c_col});'>🔵</div>
                      <div class='res-lbl' style='color:{c_col};margin-top:8px;'>Product Cluster</div>
                      <div class='res-big-num' style='color:{c_col};'>#{user_cluster}</div>
                      <div>
                        <span class='clust-pill' style='background:{c_bg};color:{c_col};border:1px solid {c_border};'>
                          {c_name}
                        </span>
                      </div>
                      <div class='res-sub'>Based on volume, revenue, price & margin profile</div>
                    </div>
                    """, unsafe_allow_html=True)

                with r2:
                    st.markdown("<div style='padding-top:8px;'>", unsafe_allow_html=True)
                    st.markdown("<div class='grp-label'>Distance to All Clusters</div>", unsafe_allow_html=True)
                    fig_d, ax_d = plt.subplots(figsize=(5, 3.2))
                    fig_d.patch.set_facecolor("#060e08"); ax_d.set_facecolor("#0a1a0f")
                    bar_colors = [CLUSTER_MAP.get(i,("","#555","",""))[1] for i in range(5)]
                    bar_alphas = [1.0 if i == user_cluster else 0.4 for i in range(5)]
                    bars = ax_d.bar([f"C{i}" for i in range(5)], dists,
                                    color=[c if i==user_cluster else "#2d4a38" for i,c in enumerate(bar_colors)],
                                    edgecolor=[c for c in bar_colors], linewidth=1.5)
                    ax_d.set_title("Proximity to Each Cluster", color="#f0faf4", fontsize=9)
                    ax_d.tick_params(colors="#7fb894", labelsize=8)
                    ax_d.set_ylabel("Distance (lower = closer)", color="#7fb894", fontsize=8)
                    for sp in ax_d.spines.values(): sp.set_edgecolor("#1e5c34")
                    fig_d.tight_layout(); st.pyplot(fig_d); plt.close()
                    st.markdown("</div>", unsafe_allow_html=True)

                # Cluster legend grid
                st.markdown("<hr class='divider-line'/>", unsafe_allow_html=True)
                st.markdown("<div style='font-size:.78rem;font-weight:700;color:#7fb894;letter-spacing:2px;text-transform:uppercase;margin-bottom:14px;'>All Cluster Definitions</div>", unsafe_allow_html=True)
                leg_cols = st.columns(5)
                clust_descs = {
                    0: "Mid-tier products boosted by promotions. Discount-sensitive buyers.",
                    1: "Low velocity, low revenue. Needs strategic review or discontinuation.",
                    2: "Top performers. High volume, revenue and margin. Invest here.",
                    3: "Moves fast but thin margins. Heavy discounts eat into profit.",
                    4: "Luxury tier. High price, low volume, best unit margin."
                }
                for i, col in enumerate(leg_cols):
                    nm, cc, cbg, cbrd = CLUSTER_MAP[i]
                    is_me = (i == user_cluster)
                    with col:
                        st.markdown(f"""
                        <div style='background:{cbg};border:{"2px" if is_me else "1px"} solid {cbrd};
                                    border-radius:12px;padding:14px 10px;text-align:center;
                                    {"box-shadow:0 0 20px "+cbg+";" if is_me else ""}'>
                          <div style='font-size:.72rem;font-weight:700;color:{cc};letter-spacing:1px;
                                      margin-bottom:6px;'>Cluster {i} {"← YOU" if is_me else ""}</div>
                          <div style='font-size:.78rem;font-weight:700;color:#f0faf4;margin-bottom:8px;'>{nm}</div>
                          <div style='font-size:.7rem;color:#7fb894;line-height:1.4;'>{clust_descs[i]}</div>
                        </div>
                        """, unsafe_allow_html=True)

                # Full insight
                insight_texts = {
                    0: f"This product is a <b>Promo Performer</b> — it sells well when discounted but has moderate baseline demand. Consider testing price elasticity and reducing discount depth to improve margin.",
                    1: f"This product shows <b>Low Commercial Performance</b> — low sales and revenue. Review shelf positioning, marketing spend, or consider phasing it out.",
                    2: f"This is a <b>Star Product</b> ⭐ — high volume, strong revenue and good margin. Prioritise stock availability, invest in visibility and protect pricing.",
                    3: f"High-rotation but <b>Low Margin</b> product — it moves fast but discounts are heavy. Try reducing discount frequency or renegotiating purchase price.",
                    4: f"This is a <b>Premium Low-Rotation</b> product — high price and best unit margin. Focus on niche targeting, premium positioning and reduce clearance risk."
                }
                st.markdown(f"""
                <div class='insight-box' style='border-left-color:{c_col};margin-top:20px;'>
                  <div style='font-size:.78rem;font-weight:700;color:{c_col};letter-spacing:1.5px;
                              text-transform:uppercase;margin-bottom:8px;'>🔵 Segment Insight</div>
                  <div style='color:#d5f5e3;font-size:.9rem;line-height:1.65;'>
                    {insight_texts.get(user_cluster,"")}
                  </div>
                </div>
                """, unsafe_allow_html=True)