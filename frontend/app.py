"""
Olist Analytics — Vision UI inspired dashboard
Fixed sidebar, gradient nav icons, glassmorphism cards, GradientSelector widget.
"""
import streamlit as st
import requests
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
from datetime import datetime

st.set_page_config(
    page_title="Olist Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_URL = os.getenv("API_URL", "http://localhost:8000")

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

dark = st.session_state.dark_mode

SB_BG = "#0b0e2e"

if dark:
    BG         = "#070a1f"
    CARD_RGB   = "13,17,50"
    GLASS      = f"rgba({CARD_RGB},0.58)"
    CARD_SOLID = "#0d1132"
    CARD2      = f"rgba({CARD_RGB},0.85)"
    BORDER     = "rgba(255,255,255,0.07)"
    BORDER_HV  = "rgba(92,111,245,0.45)"
    TEXT       = "#e2e8f0"
    SUB        = "#7a93b6"
    ACC        = "#5c6ff5"
    ACC2       = "#a855f7"
    GRID       = "rgba(255,255,255,0.035)"
    SHADOW     = "0 4px 30px rgba(0,0,0,0.6)"
    SHADOW_HV  = "0 14px 50px rgba(92,111,245,0.22),0 4px 20px rgba(0,0,0,0.6)"
    INSET      = "inset 0 1px 0 rgba(255,255,255,0.055)"
    T_LABEL    = "☀️  Modo Claro"
else:
    BG         = "#eef0fb"
    CARD_RGB   = "255,255,255"
    GLASS      = "rgba(255,255,255,0.70)"
    CARD_SOLID = "#ffffff"
    CARD2      = "rgba(255,255,255,0.92)"
    BORDER     = "rgba(180,190,240,0.55)"
    BORDER_HV  = "rgba(92,111,245,0.5)"
    TEXT       = "#0f172a"
    SUB        = "#546280"
    ACC        = "#4c6ef5"
    ACC2       = "#7c3aed"
    GRID       = "rgba(0,0,0,0.035)"
    SHADOW     = "0 2px 20px rgba(0,0,0,0.08)"
    SHADOW_HV  = "0 14px 44px rgba(76,110,245,0.18),0 2px 10px rgba(0,0,0,0.1)"
    INSET      = "inset 0 1px 0 rgba(255,255,255,0.9)"
    T_LABEL    = "🌙  Modo Escuro"

COLORS     = [ACC, ACC2, "#06b6d4", "#10b981", "#f59e0b", "#ef4444", "#ec4899"]
TIER_COLS  = ["#3b82f6", "#6366f1", "#8b5cf6", "#a855f7"]

# ── CSS injection ──────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
*,*::before,*::after{{font-family:'Inter',system-ui,sans-serif!important;box-sizing:border-box;}}

.stApp{{background:{BG}!important;}}
.main .block-container{{padding:1.5rem 2rem 2.5rem;max-width:1440px;}}
[data-testid="stHeader"]{{display:none!important;}}
#MainMenu,footer{{visibility:hidden!important;}}
::-webkit-scrollbar{{width:4px;}}
::-webkit-scrollbar-thumb{{background:{BORDER};border-radius:4px;}}

section[data-testid="stSidebar"]{{
    background:{SB_BG}!important;
    border-right:1px solid rgba(255,255,255,0.06)!important;
    transform:none!important;
    transition:none!important;
}}
section[data-testid="stSidebar"]>div{{background:transparent!important;}}
[data-testid="stSidebarContent"]{{background:transparent!important;padding:0!important;}}
[data-testid="stSidebarCollapseButton"]{{display:none!important;}}
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span{{color:rgba(255,255,255,0.6)!important;}}

section[data-testid="stSidebar"] [data-testid="stRadio"]>label{{display:none!important;}}
section[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"]{{flex-direction:column!important;gap:2px!important;}}
section[data-testid="stSidebar"] [data-testid="stRadio"] input[type="radio"]{{position:absolute;opacity:0;width:0;height:0;pointer-events:none;}}
section[data-testid="stSidebar"] [data-testid="stRadio"] label{{display:flex!important;align-items:center!important;padding:0.52rem 0.75rem!important;border-radius:10px!important;color:rgba(255,255,255,0.52)!important;font-size:0.84rem!important;font-weight:500!important;cursor:pointer!important;transition:all 0.15s!important;border-left:3px solid transparent!important;margin:0!important;}}
section[data-testid="stSidebar"] [data-testid="stRadio"] label:hover{{background:rgba(255,255,255,0.07)!important;color:rgba(255,255,255,0.88)!important;}}
section[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked){{background:rgba(92,111,245,0.2)!important;color:#a5b4ff!important;font-weight:600!important;border-left-color:#5c6ff5!important;}}

section[data-testid="stSidebar"] .stButton button{{background:rgba(255,255,255,0.05)!important;color:rgba(255,255,255,0.7)!important;border:1px solid rgba(255,255,255,0.09)!important;border-radius:20px!important;font-size:0.76rem!important;font-weight:500!important;transition:all 0.15s!important;}}
section[data-testid="stSidebar"] .stButton button:hover{{background:rgba(255,255,255,0.11)!important;color:#fff!important;border-color:rgba(255,255,255,0.18)!important;}}

h1,h2,h3,h4{{color:{TEXT}!important;font-weight:700!important;}}
p{{color:{TEXT};}}
.stMarkdown p{{color:{TEXT}!important;}}

.kpi-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin-bottom:1.4rem;}}
.kpi-card{{background:{GLASS};backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px);border:1px solid {BORDER};border-radius:18px;padding:1.3rem 1.4rem;box-shadow:{SHADOW},{INSET};cursor:pointer;position:relative;overflow:hidden;transition:transform 0.22s cubic-bezier(.4,0,.2,1),box-shadow 0.22s,border-color 0.22s;}}
.kpi-card::before{{content:'';position:absolute;top:0;left:-80%;width:50%;height:100%;background:linear-gradient(90deg,transparent,rgba(255,255,255,0.045),transparent);transition:left 0.55s ease;pointer-events:none;}}
.kpi-card:hover{{transform:translateY(-5px);box-shadow:{SHADOW_HV},{INSET};border-color:{BORDER_HV};}}
.kpi-card:hover::before{{left:160%;}}
.kpi-accent{{position:absolute;bottom:0;left:0;right:0;height:2px;background:linear-gradient(90deg,{ACC},{ACC2});opacity:0;transition:opacity 0.22s;border-radius:0 0 18px 18px;}}
.kpi-card:hover .kpi-accent{{opacity:1;}}
.kpi-icon{{font-size:1.3rem;margin-bottom:0.65rem;}}
.kpi-label{{color:{SUB};font-size:0.65rem;font-weight:700;text-transform:uppercase;letter-spacing:0.11em;margin-bottom:0.25rem;}}
.kpi-value{{color:{TEXT};font-size:1.78rem;font-weight:800;line-height:1.05;letter-spacing:-0.025em;}}
.kpi-delta{{font-size:0.7rem;font-weight:500;margin-top:0.3rem;color:{SUB};}}

.stPlotlyChart{{background:{GLASS}!important;backdrop-filter:blur(14px)!important;-webkit-backdrop-filter:blur(14px)!important;border:1px solid {BORDER}!important;border-radius:18px!important;padding:0.6rem!important;box-shadow:{SHADOW},{INSET}!important;transition:border-color 0.22s,box-shadow 0.22s!important;}}
.stPlotlyChart:hover{{border-color:{BORDER_HV}!important;box-shadow:{SHADOW_HV},{INSET}!important;}}

[data-testid="stMetric"]{{background:{GLASS}!important;backdrop-filter:blur(16px)!important;border:1px solid {BORDER}!important;border-radius:18px!important;padding:1.2rem 1.3rem!important;box-shadow:{SHADOW},{INSET}!important;transition:transform 0.2s,box-shadow 0.2s,border-color 0.2s!important;}}
[data-testid="stMetric"]:hover{{transform:translateY(-3px)!important;box-shadow:{SHADOW_HV},{INSET}!important;border-color:{BORDER_HV}!important;}}
[data-testid="stMetric"] label{{color:{SUB}!important;font-size:0.65rem!important;font-weight:700!important;text-transform:uppercase!important;letter-spacing:0.1em!important;}}
[data-testid="stMetricValue"]{{color:{TEXT}!important;font-size:1.78rem!important;font-weight:800!important;letter-spacing:-0.025em!important;}}

[data-testid="stSelectbox"]>div>div,[data-testid="stMultiSelect"]>div>div{{background:{GLASS}!important;backdrop-filter:blur(10px)!important;border:1px solid {BORDER}!important;border-radius:10px!important;color:{TEXT}!important;}}

[data-testid="stChatMessage"]{{background:{GLASS}!important;backdrop-filter:blur(12px)!important;border:1px solid {BORDER}!important;border-radius:14px!important;margin-bottom:0.5rem!important;}}
.stChatInput textarea{{background:{CARD2}!important;color:{TEXT}!important;border:1px solid {BORDER}!important;border-radius:12px!important;}}

[data-testid="stExpander"]{{background:{GLASS}!important;backdrop-filter:blur(10px)!important;border:1px solid {BORDER}!important;border-radius:10px!important;}}
[data-testid="stExpander"] summary{{color:{TEXT}!important;}}
.streamlit-expanderContent{{background:transparent!important;}}

.stAlert{{background:{GLASS}!important;backdrop-filter:blur(10px)!important;border:1px solid {BORDER}!important;border-radius:10px!important;}}

hr{{border-color:{BORDER};opacity:0.4;margin:0.8rem 0;}}

.section-label{{color:{SUB};font-size:0.64rem;font-weight:700;text-transform:uppercase;letter-spacing:0.11em;margin-bottom:0.4rem;padding:0 0.1rem;}}
.page-hdr{{margin-bottom:1.3rem;}}
.page-hdr h1{{color:{TEXT}!important;font-size:1.5rem!important;font-weight:800!important;margin:0!important;line-height:1.2!important;letter-spacing:-0.025em!important;}}
.page-hdr p{{color:{SUB}!important;font-size:0.84rem!important;margin:0.12rem 0 0!important;}}

.pay-row{{display:flex;justify-content:space-between;align-items:center;padding:0.6rem 0.9rem;background:{GLASS};backdrop-filter:blur(10px);border:1px solid {BORDER};border-radius:10px;margin-bottom:0.4rem;transition:border-color 0.18s,transform 0.18s;}}
.pay-row:hover{{border-color:{BORDER_HV};transform:translateX(3px);}}
.pay-label{{color:{TEXT};font-size:0.82rem;font-weight:500;}}
.pay-value{{color:{ACC};font-weight:700;font-size:0.88rem;}}
.pay-pct{{color:{SUB};font-size:0.72rem;margin-left:0.5rem;}}

.chip-btn .stButton button{{background:{GLASS}!important;backdrop-filter:blur(10px)!important;border:1px solid {BORDER}!important;border-radius:20px!important;color:{SUB}!important;font-size:0.75rem!important;font-weight:500!important;padding:0.28rem 0.8rem!important;transition:all 0.15s ease!important;white-space:nowrap!important;}}
.chip-btn .stButton button:hover{{background:rgba(92,111,245,0.14)!important;border-color:{BORDER_HV}!important;color:{ACC}!important;transform:translateY(-1px)!important;}}

.gs-card{{background:{GLASS};backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px);border:1px solid {BORDER};border-radius:18px;padding:1.4rem 1.5rem 1.1rem;box-shadow:{SHADOW},{INSET};margin-bottom:1rem;overflow:hidden;position:relative;}}
.gs-card::before{{content:'';position:absolute;top:-40px;right:-40px;width:120px;height:120px;background:radial-gradient(circle,rgba(92,111,245,0.14),transparent 70%);pointer-events:none;}}
.gs-track{{display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,0.18);border:1px solid {BORDER};border-radius:14px;padding:1.1rem 1.5rem;gap:0;margin-bottom:0.7rem;}}
</style>
""", unsafe_allow_html=True)


# ── Helpers ────────────────────────────────────────────────────────────────────
def kpi_card(icon, label, value, delta=""):
    d = f'<div class="kpi-delta">{delta}</div>' if delta else ""
    return (f'<div class="kpi-card"><div class="kpi-accent"></div>'
            f'<div class="kpi-icon">{icon}</div>'
            f'<div class="kpi-label">{label}</div>'
            f'<div class="kpi-value">{value}</div>{d}</div>')

def page_header(title, sub=""):
    s = f"<p>{sub}</p>" if sub else ""
    st.markdown(f'<div class="page-hdr"><h1>{title}</h1>{s}</div>',
                unsafe_allow_html=True)

def section(label):
    st.markdown(f'<div class="section-label">{label}</div>', unsafe_allow_html=True)

def chart_style(fig, height=340):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=TEXT, family="Inter, sans-serif", size=11),
        xaxis=dict(gridcolor=GRID, linecolor="rgba(0,0,0,0)",
                   tickfont=dict(color=SUB), zerolinecolor="rgba(0,0,0,0)", title=None),
        yaxis=dict(gridcolor=GRID, linecolor="rgba(0,0,0,0)",
                   tickfont=dict(color=SUB), zerolinecolor="rgba(0,0,0,0)", title=None),
        legend=dict(font=dict(color=SUB), bgcolor="rgba(0,0,0,0)",
                    bordercolor="rgba(0,0,0,0)"),
        margin=dict(l=5, r=5, t=36, b=5),
        hoverlabel=dict(bgcolor=CARD_SOLID, font_color=TEXT, bordercolor=BORDER,
                        font_size=12, font_family="Inter"),
        colorway=COLORS,
    )
    return fig

@st.cache_data(ttl=60)
def get_kpis():
    try:
        r = requests.get(f"{API_URL}/api/v1/kpi/", timeout=10)
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None

def ask_ia(q):
    try:
        r = requests.post(f"{API_URL}/api/v1/ia/perguntar",
                          json={"pergunta": q}, timeout=35)
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None

def gradient_selector_card(current_value: float) -> str:
    tiers = [
        {"label": "R$10K",  "threshold": 10_000,     "color": TIER_COLS[0], "next": TIER_COLS[1], "size": 11},
        {"label": "R$100K", "threshold": 100_000,    "color": TIER_COLS[1], "next": TIER_COLS[2], "size": 13},
        {"label": "R$1M",   "threshold": 1_000_000,  "color": TIER_COLS[2], "next": TIER_COLS[3], "size": 15},
        {"label": "R$10M+", "threshold": 10_000_000, "color": TIER_COLS[3], "next": TIER_COLS[3], "size": 17},
    ]
    reached = sum(1 for t in tiers if current_value >= t["threshold"])
    track = ""
    for i, t in enumerate(tiers):
        active = i < reached
        bg    = t["color"] if active else "#1e2860"
        glow  = f"box-shadow:0 0 18px {t['color']}55,0 0 38px {t['color']}28;" if active else ""
        sz    = t["size"]
        ring  = (f'<div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:{sz+14}px;height:{sz+14}px;border-radius:50%;border:1px dashed {t["color"]}44;"></div>'
                 if active else "")
        circle = (f'<div style="position:relative;width:{sz}px;height:{sz}px;'
                  f'border-radius:50%;background:{bg};{glow}flex-shrink:0;">{ring}</div>')
        track += circle
        if i < len(tiers) - 1:
            line_bg = (f"linear-gradient(90deg,{t['color']},{t['next']})"
                       if i < reached - 1 else "#1e2860")
            track += (f'<div style="flex:1;height:{2+i}px;background:{line_bg};'
                      f'border-radius:4px;min-width:36px;max-width:68px;"></div>')

    labels = "".join(
        f'<div style="flex:1;text-align:center;font-size:0.67rem;font-weight:700;'
        f'color:{t["color"] if i < reached else "#2a3870"};letter-spacing:0.04em;">'
        f'{t["label"]}</div>'
        for i, t in enumerate(tiers)
    )
    pct = min(100, int(reached / len(tiers) * 100))
    badge_bg = f"linear-gradient(135deg,{ACC},{ACC2})"
    return (
        f'<div class="gs-card">'
        f'<div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:1rem;">'
        f'<div style="color:{SUB};font-size:0.64rem;font-weight:700;text-transform:uppercase;letter-spacing:0.11em;">Tiers de Receita</div>'
        f'<div style="background:{badge_bg};color:#fff;font-size:0.64rem;font-weight:700;padding:0.18rem 0.6rem;border-radius:20px;letter-spacing:0.05em;">'
        f'{reached}/{len(tiers)} ALCANÇADOS</div></div>'
        f'<div class="gs-track">{track}</div>'
        f'<div style="display:flex;padding:0 0.4rem;">{labels}</div>'
        f'<div style="margin-top:0.85rem;height:3px;border-radius:4px;background:rgba(255,255,255,0.06);overflow:hidden;">'
        f'<div style="height:100%;width:{pct}%;background:linear-gradient(90deg,{TIER_COLS[0]},{TIER_COLS[-1]});border-radius:4px;"></div>'
        f'</div></div>'
    )

# ── Sidebar — Vision UI style ──────────────────────────────────────────────────
with st.sidebar:
    hoje = datetime.now().strftime("%a, %d/%m/%Y")

    # Logo block — single flat string, no HTML comments, no multi-line style attrs
    st.markdown(
        f'<div style="padding:1.2rem 0.6rem 0.2rem;">'
        f'<div style="display:flex;align-items:center;gap:0.65rem;margin-bottom:1.3rem;">'
        f'<div style="width:36px;height:36px;flex-shrink:0;background:linear-gradient(135deg,{ACC} 0%,{ACC2} 100%);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:1.1rem;box-shadow:0 4px 16px rgba(92,111,245,0.45);">📊</div>'
        f'<div>'
        f'<div style="color:#fff;font-size:0.9rem;font-weight:700;letter-spacing:-0.01em;">Olist Analytics</div>'
        f'<div style="color:rgba(255,255,255,0.3);font-size:0.58rem;text-transform:uppercase;letter-spacing:0.1em;margin-top:1px;">Business Intelligence</div>'
        f'</div></div>'
        f'<div style="display:flex;align-items:center;gap:0.6rem;padding:0.68rem 0.75rem;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.07);border-radius:12px;margin-bottom:1.15rem;">'
        f'<div style="width:30px;height:30px;flex-shrink:0;background:linear-gradient(135deg,{ACC},{ACC2});border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:0.82rem;">👤</div>'
        f'<div>'
        f'<div style="color:#e2e8f0;font-size:0.78rem;font-weight:600;">Bem-vindo!</div>'
        f'<div style="color:rgba(255,255,255,0.28);font-size:0.62rem;margin-top:1px;">{hoje}</div>'
        f'</div>'
        f'<div style="margin-left:auto;">'
        f'<div style="width:7px;height:7px;border-radius:50%;background:#10b981;box-shadow:0 0 6px #10b98177;"></div>'
        f'</div></div>'
        f'<div style="color:rgba(255,255,255,0.22);font-size:0.57rem;font-weight:700;text-transform:uppercase;letter-spacing:0.16em;padding:0 0.15rem 0.35rem;">Páginas</div>'
        f'</div>',
        unsafe_allow_html=True
    )

    pagina = st.radio(
        "nav",
        ["Dashboard", "Produtos", "Clientes e Geografia", "Assistente IA"],
        format_func=lambda x: {
            "Dashboard":            "📊   Visão Executiva",
            "Produtos":             "📦   Produtos",
            "Clientes e Geografia": "🌎   Clientes e Geo",
            "Assistente IA":        "🤖   Assistente IA",
        }[x],
        label_visibility="collapsed",
    )

    # Dados section + decorative items
    st.markdown(
        f'<div style="padding:0 0.6rem;">'
        f'<div style="height:1px;background:rgba(255,255,255,0.07);margin:0.85rem 0 0.65rem;"></div>'
        f'<div style="color:rgba(255,255,255,0.22);font-size:0.57rem;font-weight:700;text-transform:uppercase;letter-spacing:0.16em;margin-bottom:0.35rem;">Dados</div>'
        f'<div style="display:flex;align-items:center;gap:0.6rem;padding:0.48rem 0.7rem;border-radius:9px;cursor:default;">'
        f'<div style="width:26px;height:26px;border-radius:8px;background:linear-gradient(135deg,#06b6d4,#0891b2);display:flex;align-items:center;justify-content:center;font-size:0.75rem;flex-shrink:0;">⚙️</div>'
        f'<span style="color:rgba(255,255,255,0.38);font-size:0.8rem;">Configurações</span>'
        f'</div>'
        f'<div style="display:flex;align-items:center;gap:0.6rem;padding:0.48rem 0.7rem;border-radius:9px;cursor:default;">'
        f'<div style="width:26px;height:26px;border-radius:8px;background:linear-gradient(135deg,#10b981,#059669);display:flex;align-items:center;justify-content:center;font-size:0.75rem;flex-shrink:0;">📁</div>'
        f'<span style="color:rgba(255,255,255,0.38);font-size:0.8rem;">Dataset Olist</span>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True
    )

    st.markdown("<div style='height:0.7rem'></div>", unsafe_allow_html=True)
    if st.button(T_LABEL, use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

    # "Precisa de ajuda?" card
    st.markdown(
        f'<div style="margin:0.85rem 0.4rem 0.4rem;padding:1rem 1.05rem;background:linear-gradient(135deg,rgba(92,111,245,0.6) 0%,rgba(168,85,247,0.55) 100%);border:1px solid rgba(92,111,245,0.35);border-radius:14px;position:relative;overflow:hidden;">'
        f'<div style="position:absolute;top:-18px;right:-18px;width:72px;height:72px;background:rgba(255,255,255,0.06);border-radius:50%;"></div>'
        f'<div style="position:absolute;bottom:-28px;left:-8px;width:64px;height:64px;background:rgba(255,255,255,0.04);border-radius:50%;"></div>'
        f'<div style="position:relative;">'
        f'<div style="font-size:1rem;margin-bottom:0.3rem;">💡</div>'
        f'<div style="color:#fff;font-size:0.77rem;font-weight:700;margin-bottom:0.18rem;">Precisa de ajuda?</div>'
        f'<div style="color:rgba(255,255,255,0.6);font-size:0.67rem;line-height:1.4;margin-bottom:0.6rem;">Use o Assistente IA para consultar os dados</div>'
        f'<div style="background:rgba(255,255,255,0.18);color:#fff;font-size:0.67rem;font-weight:700;text-align:center;padding:0.32rem 0;border-radius:8px;letter-spacing:0.06em;border:1px solid rgba(255,255,255,0.22);">ASSISTENTE IA →</div>'
        f'</div></div>'
        f'<div style="color:rgba(255,255,255,0.16);font-size:0.57rem;text-align:center;padding:0.45rem 0;letter-spacing:0.04em;">v2.0 · Olist E-Commerce</div>',
        unsafe_allow_html=True
    )


# ── Página: Dashboard ──────────────────────────────────────────────────────────
if pagina == "Dashboard":
    page_header("Visão Executiva", "Métricas gerais do e-commerce Olist")
    kpis = get_kpis()

    if kpis:
        r = float(kpis["receita_total"])
        p = int(kpis["numero_pedidos"])
        c = int(kpis["clientes_unicos"])
        t = float(kpis["ticket_medio"])

        st.markdown(
            '<div class="kpi-grid">'
            + kpi_card("💰", "Receita Total",    f"R$ {r:,.2f}", "Dataset completo")
            + kpi_card("🛒", "Total de Pedidos", f"{p:,}",        "Pedidos realizados")
            + kpi_card("👥", "Clientes Únicos",  f"{c:,}",        "Cadastros únicos")
            + kpi_card("🎯", "Ticket Médio",     f"R$ {t:,.2f}", "Por pedido")
            + '</div>',
            unsafe_allow_html=True
        )

        st.markdown(gradient_selector_card(r), unsafe_allow_html=True)

        if kpis.get("receita_por_mes"):
            df_mes = pd.DataFrame(kpis["receita_por_mes"])
            df_mes["periodo"] = (df_mes["ano"].astype(str) + "-"
                                 + df_mes["mes"].astype(str).str.zfill(2))
            periodos = sorted(df_mes["periodo"].unique())

            if len(periodos) > 1:
                c1, c2, _ = st.columns([2, 2, 4])
                with c1:
                    inicio = st.selectbox("De", periodos, index=0, key="d_ini")
                with c2:
                    fim = st.selectbox("Até", periodos,
                                       index=len(periodos) - 1, key="d_fim")
                mask = (df_mes["periodo"] >= inicio) & (df_mes["periodo"] <= fim)
                df_f = df_mes[mask]
            else:
                df_f = df_mes

            col1, col2 = st.columns(2)
            with col1:
                section("Receita por Mês")
                fig = go.Figure(go.Scatter(
                    x=df_f["periodo"], y=df_f["receita"],
                    mode="lines+markers",
                    line=dict(color=ACC, width=2.5),
                    marker=dict(size=7, color=ACC,
                                line=dict(color=CARD_SOLID, width=2)),
                    fill="tozeroy", fillcolor="rgba(92,111,245,0.09)",
                    hovertemplate="<b>%{x}</b><br>R$ %{y:,.2f}<extra></extra>"
                ))
                st.plotly_chart(chart_style(fig), use_container_width=True)

            with col2:
                section("Receita por Estado")
                if kpis.get("receita_por_estado"):
                    df_e = pd.DataFrame(kpis["receita_por_estado"])
                    fig = px.bar(df_e, x="estado", y="receita", color="receita",
                                 color_continuous_scale=[[0, "rgba(92,111,245,0.3)"],
                                                         [1, ACC]])
                    fig.update_coloraxes(showscale=False)
                    fig.update_traces(
                        hovertemplate="<b>%{x}</b><br>R$ %{y:,.2f}<extra></extra>",
                        marker_line_width=0)
                    st.plotly_chart(chart_style(fig), use_container_width=True)

            section("Evolução Acumulada")
            df_f = df_f.copy()
            df_f["acumulado"] = df_f["receita"].cumsum()
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df_f["periodo"], y=df_f["receita"], name="Mensal",
                mode="lines+markers", line=dict(color=ACC2, width=2),
                marker=dict(size=5, color=ACC2),
                hovertemplate="<b>%{x}</b><br>Mensal: R$ %{y:,.2f}<extra></extra>"
            ))
            fig.add_trace(go.Scatter(
                x=df_f["periodo"], y=df_f["acumulado"], name="Acumulado",
                mode="lines", line=dict(color=ACC, width=2.5, dash="dot"),
                fill="tozeroy", fillcolor="rgba(92,111,245,0.06)",
                hovertemplate="<b>%{x}</b><br>Acumulado: R$ %{y:,.2f}<extra></extra>"
            ))
            st.plotly_chart(chart_style(fig, height=300), use_container_width=True)
    else:
        st.warning("Não foi possível carregar os KPIs. Verifique se a API está rodando.")


# ── Página: Produtos ───────────────────────────────────────────────────────────
elif pagina == "Produtos":
    page_header("Análise de Produtos", "Performance por produto e categoria")
    kpis = get_kpis()

    if kpis:
        top_n = st.slider("Exibir top", min_value=5, max_value=20, value=10,
                          step=5, key="top_n")

        col1, col2 = st.columns(2)
        with col1:
            section(f"Top {top_n} Produtos por Faturamento")
            if kpis.get("top_produtos"):
                df = pd.DataFrame(kpis["top_produtos"]).head(top_n)
                fig = px.bar(df, x="faturamento", y="product_id",
                             orientation="h", color="faturamento",
                             color_continuous_scale=[[0, "rgba(92,111,245,0.3)"],
                                                     [1, ACC]])
                fig.update_coloraxes(showscale=False)
                fig.update_yaxes(categoryorder="total ascending")
                fig.update_traces(
                    hovertemplate="<b>%{y}</b><br>R$ %{x:,.2f}<extra></extra>",
                    marker_line_width=0)
                st.plotly_chart(chart_style(fig, height=max(280, top_n * 28)),
                                use_container_width=True)

        with col2:
            section(f"Top {top_n} Categorias por Faturamento")
            if kpis.get("top_categorias"):
                df_c = pd.DataFrame(kpis["top_categorias"]).head(top_n)
                fig = px.bar(df_c, x="faturamento", y="categoria",
                             orientation="h", color="faturamento",
                             color_continuous_scale=[[0, "rgba(168,85,247,0.3)"],
                                                     [1, ACC2]])
                fig.update_coloraxes(showscale=False)
                fig.update_yaxes(categoryorder="total ascending")
                fig.update_traces(
                    hovertemplate="<b>%{y}</b><br>R$ %{x:,.2f}<extra></extra>",
                    marker_line_width=0)
                st.plotly_chart(chart_style(fig, height=max(280, top_n * 28)),
                                use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            section("Distribuição de Receita")
            if kpis.get("top_categorias"):
                df_p = pd.DataFrame(kpis["top_categorias"]).head(top_n)
                fig = px.pie(df_p, values="faturamento", names="categoria",
                             hole=0.58, color_discrete_sequence=COLORS)
                fig.update_traces(
                    textfont_size=11, textposition="inside",
                    hovertemplate="<b>%{label}</b><br>R$ %{value:,.2f}<br>%{percent}<extra></extra>",
                    marker=dict(line=dict(color=CARD_SOLID, width=2))
                )
                st.plotly_chart(chart_style(fig), use_container_width=True)

        with col2:
            section("Volume por Categoria")
            if kpis.get("top_categorias"):
                df_q = pd.DataFrame(kpis["top_categorias"]).head(top_n)
                fig = px.bar(df_q, x="categoria", y="quantidade",
                             color="quantidade",
                             color_continuous_scale=[[0, "rgba(6,182,212,0.3)"],
                                                     [1, "#06b6d4"]])
                fig.update_coloraxes(showscale=False)
                fig.update_traces(
                    hovertemplate="<b>%{x}</b><br>%{y} unidades<extra></extra>",
                    marker_line_width=0)
                st.plotly_chart(chart_style(fig), use_container_width=True)

        if kpis.get("top_categorias"):
            with st.expander("📋  Ver dados completos por categoria"):
                df_t = pd.DataFrame(kpis["top_categorias"])
                df_t["faturamento"] = df_t["faturamento"].apply(
                    lambda x: f"R$ {x:,.2f}")
                st.dataframe(df_t, use_container_width=True, hide_index=True)
    else:
        st.warning("Não foi possível carregar os dados.")


# ── Página: Clientes e Geografia ───────────────────────────────────────────────
elif pagina == "Clientes e Geografia":
    page_header("Clientes e Geografia",
                "Distribuição geográfica e comportamento de compra")
    kpis = get_kpis()

    if kpis:
        c   = int(kpis["clientes_unicos"])
        p   = int(kpis["numero_pedidos"])
        t   = float(kpis["ticket_medio"])
        ppc = p / c if c > 0 else 0

        st.markdown(
            '<div class="kpi-grid">'
            + kpi_card("👥", "Clientes Únicos",  f"{c:,}",        "Total cadastrado")
            + kpi_card("🛒", "Pedidos Totais",   f"{p:,}",        "Volume completo")
            + kpi_card("📈", "Pedidos/Cliente",  f"{ppc:.2f}",    "Frequência média")
            + kpi_card("💳", "Ticket Médio",     f"R$ {t:,.2f}", "Por pedido")
            + '</div>',
            unsafe_allow_html=True
        )

        estados_disp = []
        if kpis.get("pedidos_por_estado"):
            df_pe        = pd.DataFrame(kpis["pedidos_por_estado"])
            estados_disp = sorted(df_pe["estado"].unique().tolist())

        if estados_disp:
            sel = st.multiselect("Filtrar estados", estados_disp,
                                 default=estados_disp, key="estados_filtro",
                                 placeholder="Selecione estados...")
            estados_sel = sel if sel else estados_disp
        else:
            estados_sel = estados_disp

        col1, col2 = st.columns(2)
        with col1:
            section("Pedidos por Estado")
            if kpis.get("pedidos_por_estado"):
                df_pp = pd.DataFrame(kpis["pedidos_por_estado"])
                df_pp = df_pp[df_pp["estado"].isin(estados_sel)]
                fig = px.bar(df_pp, x="estado", y="quantidade",
                             color="quantidade",
                             color_continuous_scale=[[0, "rgba(92,111,245,0.3)"],
                                                     [1, ACC]])
                fig.update_coloraxes(showscale=False)
                fig.update_traces(
                    hovertemplate="<b>%{x}</b><br>%{y} pedidos<extra></extra>",
                    marker_line_width=0)
                st.plotly_chart(chart_style(fig), use_container_width=True)

        with col2:
            section("Receita por Estado")
            if kpis.get("receita_por_estado"):
                df_re = pd.DataFrame(kpis["receita_por_estado"])
                df_re = df_re[df_re["estado"].isin(estados_sel)]
                fig = px.bar(df_re, x="estado", y="receita", color="receita",
                             color_continuous_scale=[[0, "rgba(168,85,247,0.3)"],
                                                     [1, ACC2]])
                fig.update_coloraxes(showscale=False)
                fig.update_traces(
                    hovertemplate="<b>%{x}</b><br>R$ %{y:,.2f}<extra></extra>",
                    marker_line_width=0)
                st.plotly_chart(chart_style(fig), use_container_width=True)

        if kpis.get("metodos_pagamento"):
            st.markdown("<div style='height:0.2rem'></div>", unsafe_allow_html=True)
            section("Métodos de Pagamento")
            df_pay = pd.DataFrame(kpis["metodos_pagamento"])
            total  = df_pay["valor_total"].sum()

            col1, col2 = st.columns([1, 2])
            with col1:
                fig = px.pie(df_pay, values="valor_total", names="tipo",
                             hole=0.62, color_discrete_sequence=COLORS)
                fig.update_traces(
                    textposition="inside",
                    hovertemplate="<b>%{label}</b><br>R$ %{value:,.2f}<br>%{percent}<extra></extra>",
                    marker=dict(line=dict(color=CARD_SOLID, width=2))
                )
                st.plotly_chart(chart_style(fig, height=280), use_container_width=True)

            with col2:
                st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
                for _, row in df_pay.sort_values("valor_total",
                                                  ascending=False).iterrows():
                    pct   = row["valor_total"] / total * 100 if total > 0 else 0
                    label = row["tipo"].replace("_", " ").title()
                    st.markdown(
                        f'<div class="pay-row">'
                        f'<span class="pay-label">{label}</span>'
                        f'<div>'
                        f'<span class="pay-value">R$ {row["valor_total"]:,.2f}</span>'
                        f'<span class="pay-pct">{pct:.1f}%</span>'
                        f'</div></div>',
                        unsafe_allow_html=True
                    )
    else:
        st.warning("Não foi possível carregar os dados.")


# ── Página: Assistente IA ──────────────────────────────────────────────────────
elif pagina == "Assistente IA":
    page_header("Assistente de Dados",
                "Perguntas em linguagem natural sobre o dataset Olist")

    sugestoes = [
        "Qual estado gerou mais receita?",
        "Top 5 categorias?",
        "Produto mais vendido?",
        "Método de pagamento mais usado?",
    ]
    cols_chip     = st.columns(len(sugestoes))
    pergunta_chip = None
    for i, s in enumerate(sugestoes):
        with cols_chip[i]:
            st.markdown('<div class="chip-btn">', unsafe_allow_html=True)
            if st.button(s, key=f"chip_{i}", use_container_width=True):
                pergunta_chip = s
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    for msg in st.session_state.mensagens:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("sql"):
                with st.expander("Ver SQL gerado"):
                    st.code(msg["sql"], language="sql")
            if msg.get("dados"):
                with st.expander("Ver dados brutos"):
                    st.json(msg["dados"])

    pergunta_input = st.chat_input("Faça uma pergunta sobre os dados Olist...")
    pergunta       = pergunta_chip or pergunta_input

    if pergunta:
        st.session_state.mensagens.append({"role": "user", "content": pergunta})
        with st.chat_message("user"):
            st.markdown(pergunta)

        with st.chat_message("assistant"):
            with st.spinner("Analisando dados..."):
                resp = ask_ia(pergunta)

            if resp and resp.get("sucesso"):
                st.markdown(resp["resposta"])
                st.session_state.mensagens.append({
                    "role": "assistant",
                    "content": resp["resposta"],
                    "sql": resp.get("sql"),
                    "dados": resp.get("dados"),
                })
                if resp.get("sql"):
                    with st.expander("Ver SQL gerado"):
                        st.code(resp["sql"], language="sql")
                if resp.get("dados"):
                    with st.expander("Ver dados brutos"):
                        st.json(resp["dados"])
            else:
                m = (resp["resposta"] if resp
                     else "Erro ao processar. Verifique se a IA está configurada.")
                st.error(m)
                st.session_state.mensagens.append({"role": "assistant", "content": m})

        if pergunta_chip:
            st.rerun()

    if st.session_state.mensagens:
        st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
        if st.button("🗑  Limpar conversa", key="clear_chat"):
            st.session_state.mensagens = []
            st.rerun()
