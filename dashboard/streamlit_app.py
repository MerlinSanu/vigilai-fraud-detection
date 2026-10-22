import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="VigilAI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');

* { font-family: 'Inter', sans-serif !important; }

html, body, [class*="css"], .stApp, section[data-testid="stSidebar"] {
    background-color: #06060f !important;
    color: #e0e0e0 !important;
}

/* Hide sidebar toggle */
button[kind="header"] { display: none !important; }
div[data-testid="collapsedControl"] { display: none !important; }

/* Input fields */
input[type="number"], div[data-baseweb="input"] input {
    background-color: #0f0f1e !important;
    color: #e0e0e0 !important;
    border: 1px solid #D4AF37 !important;
    border-radius: 8px !important;
}

div[data-baseweb="input"] {
    background-color: #0f0f1e !important;
    border: 1px solid #D4AF37 !important;
    border-radius: 8px !important;
}

/* Labels */
label, p, span, div[data-testid="stMarkdownContainer"] p {
    color: #e0e0e0 !important;
}

/* Slider */
div[data-testid="stSlider"] label { color: #e0e0e0 !important; }
div[data-testid="stSelectSlider"] label { color: #e0e0e0 !important; }

/* Button */
div[data-testid="stButton"] button {
    background: linear-gradient(135deg, #B8860B, #D4AF37) !important;
    color: #06060f !important;
    font-weight: 800 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 16px !important;
    font-size: 1rem !important;
    width: 100% !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
}

/* Dataframe */
div[data-testid="stDataFrame"] { background-color: #0f0f1e !important; }
div[data-testid="stDataFrame"] * { color: #e0e0e0 !important; }

/* Number input buttons */
div[data-testid="stNumberInput"] button {
    background-color: #1a1a2e !important;
    color: #D4AF37 !important;
    border: 1px solid #D4AF37 !important;
}

/* Divider */
hr { border-color: #D4AF37 !important; opacity: 0.3 !important; }

/* Remove top padding */
div[data-testid="stAppViewContainer"] { padding-top: 0 !important; }
div[data-testid="block-container"] { padding-top: 1rem !important; }

.hero {
    background: linear-gradient(135deg, #06060f 0%, #0f0f1e 50%, #1a1a2e 100%);
    border-bottom: 1px solid #D4AF37;
    padding: 30px 40px;
    margin: -1rem -4rem 2rem -4rem;
}

.hero-title {
    font-size: 3.5rem;
    font-weight: 900;
    background: linear-gradient(90deg, #D4AF37, #FFD700, #FFA500, #D4AF37);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -1px;
    line-height: 1;
    margin: 0;
}

.hero-sub {
    color: #666 !important;
    font-size: 0.85rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 6px;
}

.hero-badge {
    display: inline-block;
    background: rgba(212,175,55,0.1);
    border: 1px solid #D4AF37;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.75rem;
    color: #D4AF37 !important;
    letter-spacing: 1px;
    margin-right: 8px;
    margin-top: 12px;
}

.stat-card {
    background: linear-gradient(135deg, #0f0f1e, #1a1a2e);
    border: 1px solid #1e1e3a;
    border-top: 3px solid #D4AF37;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
}

.stat-label {
    color: #555 !important;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 2px;
}

.stat-value {
    font-size: 2.2rem;
    font-weight: 800;
    color: #D4AF37 !important;
    line-height: 1.1;
    margin: 6px 0 2px;
}

.stat-sub {
    color: #444 !important;
    font-size: 0.75rem;
}

.panel {
    background: linear-gradient(135deg, #0a0a18, #0f0f1e);
    border: 1px solid #1e1e3a;
    border-radius: 16px;
    padding: 28px;
}

.panel-title {
    color: #D4AF37 !important;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 3px;
    margin-bottom: 20px;
    padding-bottom: 12px;
    border-bottom: 1px solid #1e1e3a;
}

.result-fraud {
    background: linear-gradient(135deg, #1a0000, #2d0000);
    border: 1px solid #ff3333;
    border-left: 4px solid #ff3333;
    border-radius: 12px;
    padding: 24px;
    text-align: center;
    margin-bottom: 16px;
}

.result-safe {
    background: linear-gradient(135deg, #001a00, #002d00);
    border: 1px solid #00cc44;
    border-left: 4px solid #00cc44;
    border-radius: 12px;
    padding: 24px;
    text-align: center;
    margin-bottom: 16px;
}

.result-label-fraud {
    color: #ff4444 !important;
    font-size: 1.6rem;
    font-weight: 800;
    letter-spacing: 2px;
}

.result-label-safe {
    color: #00cc44 !important;
    font-size: 1.6rem;
    font-weight: 800;
    letter-spacing: 2px;
}

.result-prob {
    font-size: 2.5rem;
    font-weight: 900;
    margin: 8px 0 4px;
}

.result-desc {
    color: #555 !important;
    font-size: 0.8rem;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.info-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid #1e1e3a;
}

.info-label { color: #555 !important; font-size: 0.8rem; }
.info-value { color: #D4AF37 !important; font-size: 0.9rem; font-weight: 600; }

.empty-state {
    background: #0a0a18;
    border: 1px dashed #1e1e3a;
    border-radius: 12px;
    padding: 60px 20px;
    text-align: center;
}

.footer {
    text-align: center;
    color: #222 !important;
    font-size: 0.75rem;
    padding: 20px 0;
    letter-spacing: 1px;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'total_checked' not in st.session_state:
    st.session_state.total_checked = 0
if 'total_fraud' not in st.session_state:
    st.session_state.total_fraud = 0

# ── HERO ──
st.markdown("""
<div class="hero">
    <div class="hero-title">VigilAI</div>
    <div class="hero-sub">Real-Time Transaction Fraud Detection System</div>
    <div style="margin-top:10px">
        <span class="hero-badge">XGBoost</span>
        <span class="hero-badge">SHAP Explainability</span>
        <span class="hero-badge">FastAPI</span>
        <span class="hero-badge">MLflow</span>
        <span class="hero-badge">ROC-AUC 0.9419</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── STATS ROW ──
s1, s2, s3, s4, s5 = st.columns(5)
fraud_rate = (st.session_state.total_fraud / st.session_state.total_checked * 100) if st.session_state.total_checked > 0 else 0
safe = st.session_state.total_checked - st.session_state.total_fraud

with s1:
    st.markdown(f"""<div class="stat-card">
        <div class="stat-label">Transactions</div>
        <div class="stat-value">{st.session_state.total_checked}</div>
        <div class="stat-sub">Analysed this session</div>
    </div>""", unsafe_allow_html=True)

with s2:
    st.markdown(f"""<div class="stat-card">
        <div class="stat-label">Fraud Detected</div>
        <div class="stat-value" style="color:#ff4444 !important">{st.session_state.total_fraud}</div>
        <div class="stat-sub">Flagged transactions</div>
    </div>""", unsafe_allow_html=True)

with s3:
    st.markdown(f"""<div class="stat-card">
        <div class="stat-label">Fraud Rate</div>
        <div class="stat-value">{fraud_rate:.1f}%</div>
        <div class="stat-sub">vs 3.5% dataset avg</div>
    </div>""", unsafe_allow_html=True)

with s4:
    st.markdown(f"""<div class="stat-card">
        <div class="stat-label">Legitimate</div>
        <div class="stat-value" style="color:#00cc44 !important">{safe}</div>
        <div class="stat-sub">Clean transactions</div>
    </div>""", unsafe_allow_html=True)

with s5:
    st.markdown(f"""<div class="stat-card">
        <div class="stat-label">Model Score</div>
        <div class="stat-value">0.94</div>
        <div class="stat-sub">ROC-AUC</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── MAIN CONTENT ──
left, right = st.columns([1, 1.3], gap="large")

with left:
    st.markdown('<div class="panel-title">🔍 Transaction Input</div>', unsafe_allow_html=True)

    transaction_amt = st.number_input("💰 Transaction Amount ($)", min_value=0.0, value=50.0, step=10.0)
    card1_avg_amt = st.number_input("📊 Card Average Amount ($)", min_value=0.0, value=200.0, step=10.0)

    col_a, col_b = st.columns(2)
    with col_a:
        card1_txn_count = st.number_input("🔢 Card Usage Count", min_value=1, value=10)
    with col_b:
        hour = st.slider("🕐 Hour", 0, 23, 12)

    email_risk_score = st.select_slider(
        "📧 Email Domain Risk Score",
        options=[2.2, 2.3, 2.8, 3.1, 3.5, 4.4, 5.3, 5.5, 9.5, 19.0],
        value=3.5,
        format_func=lambda x: f"{x}% — {'🔴 High Risk' if x > 8 else '🟡 Medium' if x > 4 else '🟢 Low Risk'}"
    )

    st.markdown("<br>", unsafe_allow_html=True)
    analyse_btn = st.button("⚡ ANALYSE TRANSACTION", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""<div class="panel-title">ℹ️ Model Info</div>""", unsafe_allow_html=True)
    st.markdown("""
    <div class="info-row"><span class="info-label">Best Model</span><span class="info-value">XGBoost</span></div>
    <div class="info-row"><span class="info-label">ROC-AUC Score</span><span class="info-value">0.9419</span></div>
    <div class="info-row"><span class="info-label">Fraud Recall</span><span class="info-value">81.8%</span></div>
    <div class="info-row"><span class="info-label">Training Samples</span><span class="info-value">472,432</span></div>
    <div class="info-row"><span class="info-label">Dataset</span><span class="info-value">IEEE-CIS</span></div>
    <div class="info-row"><span class="info-label">Total Transactions</span><span class="info-value">590,540</span></div>
    <div class="info-row" style="border:none"><span class="info-label">Decision Threshold</span><span class="info-value">70%</span></div>
    """, unsafe_allow_html=True)

with right:
    st.markdown('<div class="panel-title">📊 Detection Result</div>', unsafe_allow_html=True)

    if analyse_btn:
        payload = {
            "TransactionAmt": transaction_amt,
            "hour": hour,
            "email_risk_score": email_risk_score,
            "card1_avg_amt": card1_avg_amt,
            "card1_txn_count": card1_txn_count,
            "amt_diff_from_avg": transaction_amt - card1_avg_amt,
            "amt_ratio_to_avg": transaction_amt / (card1_avg_amt + 1)
        }

        try:
            response = requests.post("http://127.0.0.1:8001/predict", json=payload)
            result = response.json()
            fraud_prob = result["fraud_probability"]
            is_fraud = result["is_fraud"]

            st.session_state.total_checked += 1
            if is_fraud:
                st.session_state.total_fraud += 1

            st.session_state.history.append({
                "Time": datetime.now().strftime("%H:%M:%S"),
                "Amount ($)": f"${transaction_amt:,.2f}",
                "Fraud Prob": f"{fraud_prob*100:.1f}%",
                "Verdict": "🚨 FRAUD" if is_fraud else "✅ SAFE",
                "Email Risk": f"{email_risk_score}%"
            })

            if is_fraud:
                st.markdown(f"""
                <div class="result-fraud">
                    <div class="result-label-fraud">🚨 FRAUD DETECTED</div>
                    <div class="result-prob" style="color:#ff4444">{fraud_prob*100:.1f}%</div>
                    <div class="result-desc">Fraud Probability · Transaction Blocked</div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="result-safe">
                    <div class="result-label-safe">✅ LEGITIMATE</div>
                    <div class="result-prob" style="color:#00cc44">{fraud_prob*100:.1f}%</div>
                    <div class="result-desc">Fraud Probability · Transaction Approved</div>
                </div>""", unsafe_allow_html=True)

            # Gauge
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=fraud_prob * 100,
                title={'text': "Fraud Risk Score", 'font': {'color': '#D4AF37', 'size': 14}},
                number={'suffix': "%", 'font': {'color': '#e0e0e0', 'size': 32}},
                gauge={
                    'axis': {'range': [0, 100], 'tickcolor': '#333', 'tickfont': {'color': '#555'}},
                    'bar': {'color': '#ff4444' if is_fraud else '#00cc44', 'thickness': 0.3},
                    'bgcolor': '#0a0a18',
                    'borderwidth': 0,
                    'steps': [
                        {'range': [0, 30], 'color': '#002200'},
                        {'range': [30, 70], 'color': '#1a1a00'},
                        {'range': [70, 100], 'color': '#1a0000'}
                    ],
                    'threshold': {
                        'line': {'color': '#D4AF37', 'width': 2},
                        'thickness': 0.8,
                        'value': 70
                    }
                }
            ))
            fig_gauge.update_layout(
                paper_bgcolor='#0a0a18',
                plot_bgcolor='#0a0a18',
                font={'color': '#e0e0e0'},
                height=220,
                margin=dict(l=20, r=20, t=40, b=10)
            )
            st.plotly_chart(fig_gauge, use_container_width=True)

            # Risk factors
            st.markdown('<div class="panel-title">⚠️ Risk Factor Analysis</div>', unsafe_allow_html=True)
            amt_ratio = transaction_amt / (card1_avg_amt + 1)
            factors = {
                "Amount vs Card Average": min(amt_ratio / 5 * 100, 100),
                "Email Domain Risk": min(email_risk_score / 19 * 100, 100),
                "Transaction Frequency": min((1 / card1_txn_count) * 100, 100),
                "Late Night Activity": 85 if hour < 6 or hour > 22 else 15
            }
            for factor, score in factors.items():
                color = "#ff4444" if score > 65 else "#D4AF37" if score > 35 else "#00cc44"
                st.markdown(f"""
                <div style="margin-bottom:14px">
                    <div style="display:flex;justify-content:space-between;margin-bottom:5px">
                        <span style="color:#888;font-size:0.8rem">{factor}</span>
                        <span style="color:{color};font-size:0.8rem;font-weight:700">{score:.0f}%</span>
                    </div>
                    <div style="background:#0f0f1e;border-radius:3px;height:5px;overflow:hidden">
                        <div style="background:linear-gradient(90deg,{color}88,{color});width:{score}%;height:5px;border-radius:3px;transition:width 0.5s"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"⚠️ API Error: Make sure FastAPI is running on port 8001!")

    else:
        st.markdown("""
        <div class="empty-state">
            <div style="font-size:4rem;margin-bottom:16px">🛡️</div>
            <div style="color:#D4AF37;font-size:1.1rem;font-weight:700;letter-spacing:2px">VIGILAI</div>
            <div style="color:#333;font-size:0.85rem;margin-top:8px;letter-spacing:1px">
                Enter transaction details and click<br>ANALYSE TRANSACTION
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── HISTORY ──
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="panel-title">📋 Transaction History</div>', unsafe_allow_html=True)

if st.session_state.history:
    df_history = pd.DataFrame(st.session_state.history)
    st.dataframe(df_history, use_container_width=True, hide_index=True)

    if len(st.session_state.history) > 1:
        probs = [float(h["Fraud Prob"].replace("%", "")) for h in st.session_state.history]
        times = [h["Time"] for h in st.session_state.history]

        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=times, y=probs,
            mode='lines+markers',
            line=dict(color='#D4AF37', width=2),
            marker=dict(
                color=['#ff4444' if p >= 70 else '#00cc44' for p in probs],
                size=10, line=dict(color='#D4AF37', width=1)
            ),
            fill='tozeroy',
            fillcolor='rgba(212,175,55,0.05)'
        ))
        fig_line.add_hline(y=70, line_dash="dash", line_color="#D4AF37",
                           annotation_text="Decision Threshold (70%)",
                           annotation_font_color="#D4AF37")
        fig_line.update_layout(
            title=dict(text="Fraud Probability Trend", font=dict(color='#D4AF37', size=14)),
            paper_bgcolor='#0a0a18',
            plot_bgcolor='#0a0a18',
            font=dict(color='#e0e0e0'),
            xaxis=dict(gridcolor='#1e1e3a', title="Time", titlefont=dict(color='#555')),
            yaxis=dict(gridcolor='#1e1e3a', title="Fraud Probability (%)",
                       range=[0, 100], titlefont=dict(color='#555')),
            height=280,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_line, use_container_width=True)
else:
    st.markdown("""
    <div style="background:#0a0a18;border:1px dashed #1e1e3a;border-radius:8px;
                padding:30px;text-align:center;color:#333;font-size:0.85rem;letter-spacing:1px">
        NO TRANSACTIONS ANALYSED YET
    </div>
    """, unsafe_allow_html=True)

# ── FOOTER ──
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div class="footer">
    VIGILAI · REAL-TIME FRAUD DETECTION · XGBOOST + SHAP + FASTAPI + MLFLOW · MERLIN © 2026
</div>
""", unsafe_allow_html=True)