import streamlit as st
import random
import plotly.graph_objects as go

st.set_page_config(
    page_title="Life 100：新泰度生存指南",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# CSS：Figma / Glassmorphism / RPG
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;600;700;900&display=swap');

html, body, [class*="css"] { font-family: 'Noto Sans TC', sans-serif; }

.stApp {
    background:
        radial-gradient(circle at 20% 20%, rgba(0, 255, 170, 0.25), transparent 30%),
        radial-gradient(circle at 80% 10%, rgba(38, 166, 91, 0.25), transparent 35%),
        linear-gradient(135deg, #06130d 0%, #0b1f17 45%, #07110d 100%);
    color: #f8fafc;
}
header[data-testid="stHeader"], [data-testid="stToolbar"] { background: rgba(0,0,0,0) !important; }
#MainMenu, footer { visibility: hidden; }
.block-container { padding-top: 1rem; max-width: 1240px; }

.hero {
    padding: 42px;
    border-radius: 36px;
    background: linear-gradient(135deg, rgba(255,255,255,0.14), rgba(255,255,255,0.04));
    border: 1px solid rgba(255,255,255,0.18);
    box-shadow: 0 24px 80px rgba(0,0,0,0.35);
    backdrop-filter: blur(18px);
    position: relative;
    overflow: hidden;
    margin-bottom: 20px;
}
.hero:before {
    content: "";
    position: absolute;
    width: 280px;
    height: 280px;
    right: -80px;
    top: -80px;
    background: radial-gradient(circle, rgba(0, 220, 130, 0.4), transparent 65%);
    border-radius: 50%;
    animation: pulse 4s infinite alternate;
}
@keyframes pulse { from { transform: scale(0.9); opacity: .55; } to { transform: scale(1.18); opacity: 1; } }

.title { font-size: 58px; font-weight: 900; line-height: 1.1; letter-spacing: -1px; }
.subtitle { font-size: 19px; color: #cbd5e1; margin-top: 12px; line-height: 1.8; }

.glass-card {
    padding: 24px;
    border-radius: 28px;
    background: linear-gradient(135deg, rgba(255,255,255,0.13), rgba(255,255,255,0.045));
    border: 1px solid rgba(255,255,255,0.16);
    box-shadow: 0 18px 50px rgba(0,0,0,0.25);
    backdrop-filter: blur(16px);
    margin-bottom: 18px;
    transition: .25s ease;
}
.glass-card:hover { transform: translateY(-3px); box-shadow: 0 26px 70px rgba(0,0,0,0.36); }

.rpg-card {
    padding: 22px;
    border-radius: 24px;
    background: linear-gradient(135deg, rgba(0, 120, 72, .38), rgba(9, 25, 18, .68));
    border: 1px solid rgba(74, 222, 128, .35);
    box-shadow: inset 0 0 30px rgba(74, 222, 128, .08), 0 14px 42px rgba(0,0,0,.28);
    margin-bottom: 14px;
    min-height: 170px;
}
.rpg-card:hover { transform: translateY(-4px); }

.status-label { font-size: 15px; color: #bbf7d0; font-weight: 700; }
.big-number { font-size: 38px; font-weight: 900; }
.event-card {
    padding: 18px 20px;
    border-radius: 22px;
    background: linear-gradient(135deg, rgba(20, 83, 45, .55), rgba(15, 23, 42, .7));
    border-left: 6px solid #4ade80;
    border-top: 1px solid rgba(255,255,255,.14);
    margin-bottom: 12px;
    animation: pop .45s ease;
}
@keyframes pop { 0% { opacity: 0; transform: scale(.95) translateY(8px); } 100% { opacity: 1; transform: scale(1) translateY(0); } }
.badge {
    display: inline-block;
    padding: 7px 12px;
    border-radius: 999px;
    background: rgba(34, 197, 94, .18);
    border: 1px solid rgba(74, 222, 128, .35);
    color: #bbf7d0;
    font-weight: 700;
    margin: 4px 6px 4px 0;
}
.timeline { height: 12px; border-radius: 99px; background: rgba(255,255,255,.12); overflow: hidden; margin: 14px 0 8px 0; }
.timeline-fill { height: 100%; border-radius: 99px; background: linear-gradient(90deg, #22c55e, #84cc16, #facc15); box-shadow: 0 0 24px rgba(34,197,94,.65); }
.stButton > button {
    border-radius: 999px !important;
    border: 1px solid rgba(74, 222, 128, .5) !important;
    background: linear-gradient(135deg, #16a34a, #22c55e) !important;
    color: white !important;
    font-weight: 800 !important;
    padding: 0.75rem 1.3rem !important;
    box-shadow: 0 12px 34px rgba(34, 197, 94, .28);
}
.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 18px 44px rgba(34, 197, 94, .38); }
[data-testid="stMetricValue"] { color: #f8fafc; font-size: 34px; }
[data-testid="stMetricLabel"] { color: #bbf7d0; font-weight: 700; }
a { color: #86efac !important; font-weight: 800; text-decoration: none; }
hr { border-color: rgba(255,255,255,.12); }
</style>
""", unsafe_allow_html=True)

# =========================
# 保險百科資料庫
# =========================
INSURANCE_DETAIL = {
    "實支實付醫療險": {
        "title": "🏥 實支實付醫療險",
        "category": "健康醫療",
        "short": "住院、手術、自費醫材等醫療支出的核心防線。",
        "desc": "住院或手術時，依照實際醫療支出協助補貼費用，降低自費醫材、手術費、住院費造成的財務壓力。",
        "coverage": ["住院醫療費", "手術費", "門診手術", "特定處置", "加護病房或燒燙傷病房慰問金"],
        "suitable": ["剛出社會者", "醫療保障不足者", "擔心自費醫療支出者", "想建立基本醫療防線者"],
        "effect": "住院或手術事件發生時，Wealth 損失降低 70%。",
        "cost": 14,
        "item_name": "實支實付醫療險",
        "url": "https://www.cathaylife.com.tw/official/products/health-reimbursement-benefits/cv4"
    },
    "住院日額醫療險": {
        "title": "🛏️ 住院日額醫療險",
        "category": "健康醫療",
        "short": "住院期間以天數計算給付，支援照護與生活支出。",
        "desc": "住院日額醫療險以住院天數作為給付依據，讓玩家在住院期間仍有現金流支援生活與照護需求。",
        "coverage": ["住院日額", "住院生活支出", "照護費用補貼", "短期醫療現金流"],
        "suitable": ["想補足住院期間收入缺口者", "自由工作者", "家庭主要照顧者"],
        "effect": "住院事件發生時，Wealth 額外恢復 +10。",
        "cost": 10,
        "item_name": "住院日額醫療險",
        "url": "https://www.cathaylife.com.tw/official/products/health-surgery"
    },
    "手術醫療險": {
        "title": "🔪 手術醫療險",
        "category": "健康醫療",
        "short": "針對手術與處置給付，降低突發開刀支出。",
        "desc": "當玩家面臨手術、治療或特定處置時，手術醫療險可協助減少一次性醫療支出。",
        "coverage": ["手術醫療", "特定處置", "門診手術", "住院手術"],
        "suitable": ["擔心突發手術支出者", "醫療保障不足者", "想強化醫療防線者"],
        "effect": "手術事件發生時，Wealth 損失降低 60%。",
        "cost": 12,
        "item_name": "手術醫療險",
        "url": "https://www.cathaylife.com.tw/official/products/health-surgery"
    },
    "重大傷病險": {
        "title": "🛡️ 重大傷病險",
        "category": "健康醫療",
        "short": "重大疾病來臨時，提供一次性大額保障。",
        "desc": "當罹患重大傷病時，提供一次性保險金，可支應治療費、生活費與收入中斷風險。",
        "coverage": ["重大傷病一次金", "治療費用", "生活費補貼", "收入中斷支援"],
        "suitable": ["家庭經濟支柱", "擔心重大疾病造成財務衝擊者", "想補足醫療一次金者"],
        "effect": "重大疾病事件發生時，Wealth 損失降低 80%，Health 最低保留 20。",
        "cost": 20,
        "item_name": "重大傷病險",
        "url": "https://www.cathaylife.com.tw/official/products/health-illness"
    },
    "癌症險": {
        "title": "🦠 癌症險",
        "category": "健康醫療",
        "short": "針對癌症治療長期化與高額支出設計。",
        "desc": "癌症治療可能包含手術、化療、放療、標靶藥物與免疫治療，癌症險用來降低長期治療造成的財務壓力。",
        "coverage": ["癌症診斷", "癌症治療", "癌症住院", "標靶或自費療程支援"],
        "suitable": ["有家族病史者", "重視癌症保障者", "想降低長期治療財務壓力者"],
        "effect": "癌症事件發生時，Health 損失降低 25，Wealth 損失降低 65%。",
        "cost": 18,
        "item_name": "癌症險",
        "url": "https://www.cathaylife.com.tw/official/products/health-illness"
    },
    "長期照顧險": {
        "title": "🌳 長期照顧險",
        "category": "長照退休",
        "short": "面對高齡失能與長期照護費用的守護。",
        "desc": "當年老或疾病造成長期照護需求時，協助支付照護、看護與生活支出。",
        "coverage": ["長照給付", "照護費用", "看護支出", "高齡失能風險"],
        "suitable": ["想規劃高齡生活者", "擔心失能照護支出者", "家庭照顧者"],
        "effect": "70 歲後遇到長照事件時，Wealth 損失降低 80%，Health 額外恢復 +15。",
        "cost": 22,
        "item_name": "長期照顧險",
        "url": "https://www.cathaylife.com.tw/official/products/health-long-term-care"
    },
    "失智險": {
        "title": "🧓 失智險",
        "category": "長照退休",
        "short": "高齡認知退化與照護需求的專項防線。",
        "desc": "針對失智或認知功能退化造成的長期照顧需求，提供高齡照護與家庭財務支援。",
        "coverage": ["失智照護", "長期照顧", "家庭照護支出", "高齡照護風險"],
        "suitable": ["擔心高齡失智風險者", "有長輩照護經驗者", "想提前規劃老後照護者"],
        "effect": "75 歲後發生失智或長照事件時，Mind 損失降低 20，Wealth 損失降低 70%。",
        "cost": 20,
        "item_name": "失智險",
        "url": "https://www.cathaylife.com.tw/official/products/health-long-term-care"
    },
    "年金險": {
        "title": "👴 年金險",
        "category": "長照退休",
        "short": "退休後建立穩定現金流。",
        "desc": "年金險可用於退休後的現金流規劃，協助玩家降低長壽風險與退休收入中斷風險。",
        "coverage": ["退休現金流", "長壽風險", "老後生活費", "資產分配"],
        "suitable": ["想規劃退休收入者", "擔心活太久錢不夠者", "重視穩定現金流者"],
        "effect": "65 歲後每回合 Wealth +8。",
        "cost": 22,
        "item_name": "年金險",
        "url": "https://www.cathaylife.com.tw/official/products/investment-va/sra"
    },
    "定期壽險": {
        "title": "❤️ 定期壽險",
        "category": "財務保障",
        "short": "家庭責任期的基本人身保障。",
        "desc": "定期壽險可在特定期間內提供身故保障，協助家庭面對主要收入者中斷帶來的生活風險。",
        "coverage": ["身故保障", "家庭生活費", "房貸與子女教育", "責任期保障"],
        "suitable": ["家庭經濟支柱", "有房貸者", "有子女或扶養責任者"],
        "effect": "家庭責任事件發生時，Wealth 損失降低 60%，Mind 損失降低 10。",
        "cost": 16,
        "item_name": "定期壽險",
        "url": "https://www.cathaylife.com.tw/official/products/life-caring"
    },
    "投資型保單": {
        "title": "📈 投資型保單",
        "category": "財務投資",
        "short": "結合保障與投資配置，建立長期資產規劃。",
        "desc": "投資型保單兼具保障與投資連結特性，適合有中長期資產配置需求的人。",
        "coverage": ["壽險保障", "投資連結", "資產配置", "長期理財"],
        "suitable": ["想兼顧保障與投資者", "願意承擔投資波動者", "有長期理財需求者"],
        "effect": "投資成功事件 Wealth 額外 +10；市場震盪時損失降低 30%。",
        "cost": 18,
        "item_name": "投資型保單",
        "url": "https://www.cathaylife.com.tw/official/products/investment-va"
    },
    "國泰智能投資": {
        "title": "💰 國泰智能投資",
        "category": "財務投資",
        "short": "以數位工具協助資產配置與長期投資。",
        "desc": "協助使用者進行資產配置與長期投資規劃，降低退休與市場波動風險。",
        "coverage": ["資產配置", "市場波動管理", "長期投資", "退休準備"],
        "suitable": ["想建立退休現金流者", "長期資產配置者", "擔心市場波動者"],
        "effect": "市場黑天鵝事件發生時，Wealth 損失降低 60%。",
        "cost": 18,
        "item_name": "國泰智能投資",
        "url": "https://www.cathaylife.com.tw/official/products/investment-va"
    },
    "FitBack 健康吧": {
        "title": "💪 FitBack 健康吧",
        "category": "健康促進",
        "short": "用健康任務與回饋機制，讓保障從事後轉向事前預防。",
        "desc": "透過健康任務與健康促進機制，鼓勵使用者維持良好生活習慣。",
        "coverage": ["健康任務", "保費回饋", "健康促進", "生活習慣管理"],
        "suitable": ["想透過健康管理降低疾病風險者", "規律運動者", "願意完成健康任務者"],
        "effect": "每回合 Health 額外 +8，並提高小樹點取得機率。",
        "cost": 10,
        "item_name": "FitBack 健康吧",
        "url": "https://www.cathaylife.com.tw/official/products/health-surgery"
    },
    "小樹點": {
        "title": "🌱 小樹點",
        "category": "健康促進",
        "short": "跨場景回饋點數，將健康行為轉為遊戲資源。",
        "desc": "小樹點在 Life100 中被設計為跨界通用貨幣，玩家可透過維持健康值取得，用於減少保障配置成本。",
        "coverage": ["行為回饋", "數位互動", "品牌生態系", "任務獎勵"],
        "suitable": ["喜歡任務回饋者", "願意持續互動者", "健康狀態穩定者"],
        "effect": "Health 高於 75 時，每回合獲得小樹點；可折抵部分配置成本。",
        "cost": 0,
        "item_name": "小樹點",
        "url": "https://www.cathaylife.com.tw/cathaylife/"
    },
    "CVX 泰好保": {
        "title": "⚡ CVX 泰好保",
        "category": "理賠服務",
        "short": "數位保險服務，降低投保與理賠的流程壓力。",
        "desc": "以數位化服務提升保險互動效率，讓玩家在疾病或理賠事件中減少行政壓力。",
        "coverage": ["數位服務", "保單管理", "流程便利", "互動體驗"],
        "suitable": ["偏好線上服務者", "擔心理賠流程麻煩者", "想提高保單管理效率者"],
        "effect": "疾病或理賠事件發生時，Mind 損失降低 12。",
        "cost": 12,
        "item_name": "CVX 泰好保",
        "url": "https://www.cathaylife.com.tw/cathaylife/"
    },
    "理賠聯盟鏈": {
        "title": "⛓️ 理賠聯盟鏈",
        "category": "理賠服務",
        "short": "讓理賠流程更順暢，降低繁瑣文件造成的心理負擔。",
        "desc": "理賠流程越順暢，玩家在疾病事件後越能快速恢復心力，減少行政流程造成的二次壓力。",
        "coverage": ["理賠流程", "資料串接", "文件減量", "服務效率"],
        "suitable": ["重視理賠效率者", "擔心文件繁瑣者", "有醫療保障需求者"],
        "effect": "遭遇疾病事件時，Mind 損失降低 15。",
        "cost": 12,
        "item_name": "理賠聯盟鏈",
        "url": "https://www.cathaylife.com.tw/cathaylife/services/claim/claim-docs"
    },
    "AI 理賠顧問": {
        "title": "🤖 AI 理賠顧問",
        "category": "理賠服務",
        "short": "在事件發生後協助玩家理解下一步該怎麼做。",
        "desc": "AI 理賠顧問在 Life100 中扮演個人化保險助理，協助玩家理解事件風險、建議保障搭配與理賠方向。",
        "coverage": ["個人化建議", "理賠指引", "事件分析", "保障推薦"],
        "suitable": ["不了解保險者", "需要快速理解保障者", "想要個人化建議者"],
        "effect": "每次重大事件後，自動推薦最適合的保障；Mind 額外 +5。",
        "cost": 8,
        "item_name": "AI 理賠顧問",
        "url": "https://www.cathaylife.com.tw/cathaylife/services/claim/claim-docs"
    },
}

SHOP_ITEMS = [
    "FitBack 健康吧", "實支實付醫療險", "重大傷病險", "癌症險",
    "長期照顧險", "年金險", "定期壽險", "國泰智能投資", "CVX 泰好保", "理賠聯盟鏈", "AI 理賠顧問"
]

CATEGORIES = {
    "健康醫療": ["實支實付醫療險", "住院日額醫療險", "手術醫療險", "重大傷病險", "癌症險"],
    "長照退休": ["長期照顧險", "失智險", "年金險"],
    "財務保障": ["定期壽險"],
    "財務投資": ["投資型保單", "國泰智能投資"],
    "健康促進": ["FitBack 健康吧", "小樹點"],
    "理賠服務": ["CVX 泰好保", "理賠聯盟鏈", "AI 理賠顧問"],
}

# =========================
# 初始化
# =========================
def init_state():
    defaults = {
        "page": "start", "age": 25, "health": 80, "mind": 80, "wealth": 80,
        "tree": 0, "game_items": [], "logs": [], "persona": "尚未生成",
        "goal": "", "last_event": None, "selected_insurance": None, "previous_page": "start",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# =========================
# 工具函式
# =========================
def clamp(x):
    return max(0, min(100, int(x)))

def add_log(text):
    st.session_state.logs.append(text)

def reset_game():
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.rerun()

def goto(page, **kwargs):
    for k, v in kwargs.items():
        st.session_state[k] = v
    st.session_state.page = page
    st.rerun()

def product_info(name):
    d = INSURANCE_DETAIL.get(name, {})
    title = d.get("title", name)
    icon = title.split(" ")[0]
    return icon, d.get("short", "降低特定人生風險。"), d.get("effect", "依事件降低損失。")

def stat_card(icon, label, value, desc):
    st.markdown(f"""
    <div class="glass-card">
        <div class="status-label">{icon} {label}</div>
        <div class="big-number">{value}/100</div>
        <div style="color:#cbd5e1; font-size:14px;">{desc}</div>
    </div>
    """, unsafe_allow_html=True)
    st.progress(value / 100)

def risk_chart():
    labels = ["健康風險", "心理壓力", "財務風險"]
    values = [100 - st.session_state.health, 100 - st.session_state.mind, 100 - st.session_state.wealth]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=values + [values[0]], theta=labels + [labels[0]], fill="toself", name="Life Risk"))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#f8fafc"),
        polar=dict(bgcolor="rgba(255,255,255,0.03)", radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(255,255,255,.15)"), angularaxis=dict(gridcolor="rgba(255,255,255,.15)")),
        showlegend=False, height=430, margin=dict(l=40, r=40, t=30, b=30)
    )
    st.plotly_chart(fig, use_container_width=True)

def age_timeline():
    percent = clamp(int((st.session_state.age - 25) / 75 * 100))
    st.markdown(f"""
    <div class="glass-card">
        <div class="status-label">🕰️ 人生進度</div>
        <div class="timeline"><div class="timeline-fill" style="width:{percent}%"></div></div>
        <div style="display:flex; justify-content:space-between; color:#cbd5e1;">
            <span>25歲</span><span>{st.session_state.age}歲</span><span>100歲</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def recommend_items():
    rec = []
    if st.session_state.health < 65:
        rec += ["實支實付醫療險", "重大傷病險", "FitBack 健康吧"]
    if st.session_state.mind < 65:
        rec += ["CVX 泰好保", "理賠聯盟鏈", "AI 理賠顧問"]
    if st.session_state.wealth < 65:
        rec += ["國泰智能投資", "年金險", "定期壽險"]
    if st.session_state.age >= 60:
        rec += ["長期照顧險", "年金險"]
    if not rec:
        rec = ["FitBack 健康吧", "實支實付醫療險", "國泰智能投資"]
    out = []
    for r in rec:
        if r not in out and r not in st.session_state.game_items:
            out.append(r)
    return out[:3]

def apply_item_effects(name, dh, dm, dw):
    items = st.session_state.game_items
    if "FitBack 健康吧" in items:
        dh += 8
    if "實支實付醫療險" in items and any(x in name for x in ["住院", "手術", "醫療"]):
        dw += 20
    if "住院日額醫療險" in items and "住院" in name:
        dw += 10
    if "手術醫療險" in items and "手術" in name:
        dw += 15
    if "重大傷病險" in items and any(x in name for x in ["重大疾病", "重大傷病"]):
        dw += 28
        dh += 12
    if "癌症險" in items and "癌症" in name:
        dw += 25
        dh += 15
    if "長期照顧險" in items and ("長照" in name or "失能" in name or st.session_state.age >= 70):
        dh += 22
        dw += 28
    if "失智險" in items and ("失智" in name or st.session_state.age >= 75):
        dm += 20
        dw += 24
    if "年金險" in items and st.session_state.age >= 65:
        dw += 8
    if "定期壽險" in items and "家庭" in name:
        dw += 18
        dm += 10
    if "國泰智能投資" in items and any(x in name for x in ["股市", "市場", "投資"]):
        dw += 22
    if "投資型保單" in items and any(x in name for x in ["股市", "投資", "資產"]):
        dw += 12
    if "CVX 泰好保" in items and any(x in name for x in ["疾病", "醫療", "住院", "理賠"]):
        dm += 12
    if "理賠聯盟鏈" in items and any(x in name for x in ["疾病", "醫療", "住院", "理賠"]):
        dm += 15
    if "AI 理賠顧問" in items:
        dm += 5
    return dh, dm, dw

def insurance_detail_block(selected, show_back=True, allow_equip=False):
    data = INSURANCE_DETAIL.get(selected)
    if not data:
        st.warning("找不到此保險資料。")
        return
    st.markdown(f'<div class="title">{data["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="glass-card">
        <span class="badge">{data['category']}</span>
        <span class="badge">成本 {data['cost']}</span>
        <h3>📖 這是什麼？</h3>
        <p>{data['desc']}</p>
        <h3>🛡️ 主要保障內容</h3>
        {''.join([f'<span class="badge">{x}</span>' for x in data['coverage']])}
        <h3>🎯 適合誰？</h3>
        {''.join([f'<span class="badge">{x}</span>' for x in data['suitable']])}
        <h3>🎮 Life100 遊戲效果</h3>
        <div class="event-card">{data['effect']}</div>
        <h3>🔗 國泰官方商品頁</h3>
        <p><a href="{data['url']}" target="_blank">前往國泰人壽官方頁面</a></p>
    </div>
    """, unsafe_allow_html=True)
    cols = st.columns(3 if allow_equip else 2)
    if show_back:
        with cols[0]:
            if st.button("⬅ 返回上一頁", use_container_width=True):
                goto(st.session_state.get("previous_page", "start"))
    if allow_equip:
        with cols[1]:
            if st.button("🛡️ 加入人生保障", use_container_width=True):
                equip_item(selected)
    with cols[-1]:
        if st.button("🏠 回首頁", use_container_width=True):
            goto("start")

def equip_item(name):
    data = INSURANCE_DETAIL.get(name)
    if not data:
        st.error("此商品無法配置。")
        return
    cost = data["cost"]
    final_cost = max(0, cost - st.session_state.tree)
    if name in st.session_state.game_items:
        st.warning("你已經配置過這項保障。")
    elif st.session_state.wealth >= final_cost:
        used_tree = min(st.session_state.tree, cost)
        st.session_state.tree -= used_tree
        st.session_state.wealth -= final_cost
        st.session_state.game_items.append(name)
        add_log(f"{st.session_state.age}歲：配置保障「{name}」，花費財富 {final_cost}，使用小樹點 {used_tree}。")
        st.success("配置成功！")
    else:
        st.error("財富不足，無法配置。")

# =========================
# 頁面：首頁
# =========================
if st.session_state.page == "start":
    st.markdown("""
    <div class="hero">
        <div class="badge">Cathay Life OS 100</div>
        <div class="title">Life 100<br>新泰度生存指南</div>
        <div class="subtitle">
            你可以選擇進入人生模擬遊戲，或先查看 Life100 保險百科。<br>
            遊戲與百科分開，讓玩家更清楚知道自己正在「玩遊戲」還是「查資料」。
        </div>
        <br>
        <span class="badge">🎮 人生遊戲</span><span class="badge">📚 保險百科</span><span class="badge">🧭 遊戲說明</span>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="rpg-card"><h2>🎮 人生遊戲模式</h2>
        <p>從 25 歲開始，面對疾病、投資、長照、退休與家庭風險，挑戰活到 100 歲。</p>
        <p><b>流程：</b>測驗 → 每 5 年前進 → 10 年決策點 → 配置保障 → 百歲結算</p></div>
        """, unsafe_allow_html=True)
        if st.button("🚀 開始人生遊戲", use_container_width=True):
            goto("quiz")
    with col2:
        st.markdown("""
        <div class="rpg-card"><h2>📚 Life100 保險百科</h2>
        <p>查看不同保險的用途、保障內容、適合族群、遊戲效果與國泰官方商品連結。</p></div>
        """, unsafe_allow_html=True)
        if st.button("📖 查看保險百科", use_container_width=True):
            goto("insurance_wiki")
    with col3:
        st.markdown("""
        <div class="rpg-card"><h2>🧭 遊戲說明</h2>
        <p>第一次使用建議先看玩法。了解身、心、財三大數值與人生規劃室的作用。</p></div>
        """, unsafe_allow_html=True)
        if st.button("🧭 查看遊戲說明", use_container_width=True):
            goto("game_guide")

# =========================
# 頁面：遊戲說明
# =========================
elif st.session_state.page == "game_guide":
    st.markdown('<div class="title">🧭 Life100 遊戲說明</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="glass-card">
        <h2>遊戲目標</h2>
        <p>從 25 歲開始一路走到 100 歲，並讓三個核心數值都不要歸零：</p>
        <span class="badge">💪 身 Health</span><span class="badge">🧠 心 Mind</span><span class="badge">💰 財 Wealth</span>
    </div>
    <div class="glass-card">
        <h2>怎麼玩？</h2>
        <div class="event-card">Step 1：完成 4 題百歲天賦測驗，生成初始人生面板。</div>
        <div class="event-card">Step 2：點擊「前進 5 年」，觸發人生事件，例如過勞、股災、重大疾病、長照需求。</div>
        <div class="event-card">Step 3：每 10 年會進入「人生規劃室」，你可以配置保險保障。</div>
        <div class="event-card">Step 4：保險會在未來事件中抵銷 Health、Mind 或 Wealth 的損失。</div>
        <div class="event-card">Step 5：到 100 歲後產出人生結算報告。</div>
    </div>
    <div class="glass-card">
        <h2>保險百科與遊戲的關係</h2>
        <p>百科是查資料用；遊戲是做決策用。你可以先看百科理解每項保障，再進遊戲配置。遊戲中的「查看詳細百科」也會帶你查看完整說明與國泰官方連結。</p>
    </div>
    """, unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🚀 我懂了，開始遊戲", use_container_width=True):
            goto("quiz")
    with c2:
        if st.button("🏠 回首頁", use_container_width=True):
            goto("start")

# =========================
# 頁面：測驗
# =========================
elif st.session_state.page == "quiz":
    st.markdown('<div class="title">🧬 百歲天賦測驗</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="glass-card"><h3>Step 1：建立你的角色</h3>
    <p>回答 4 題，系統會生成你的初始身、心、財數值。之後你將從 25 歲開始挑戰百歲人生。</p></div>
    """, unsafe_allow_html=True)
    income = st.selectbox("1. 你的收入與理財狀態？", ["月光族", "有固定儲蓄", "積極投資", "財務規劃完整"])
    goal = st.selectbox("2. 你最想達成的人生目標？", ["買房", "財富自由", "健康退休", "照顧家人"])
    lifestyle = st.selectbox("3. 你嚮往的生活方式？", ["高壓拚事業", "自由斜槓", "穩定生活", "享樂優先"])
    sleep = st.selectbox("4. 你的健康作息？", ["常熬夜少運動", "偶爾運動", "規律運動", "飲食睡眠都穩定"])

    c1, c2 = st.columns(2)
    with c1:
        if st.button("✨ 生成我的人生面板", use_container_width=True):
            if income == "月光族":
                st.session_state.wealth = 55; money_trait = "高波動財務型"
            elif income == "有固定儲蓄":
                st.session_state.wealth = 70; money_trait = "穩健儲蓄型"
            elif income == "積極投資":
                st.session_state.wealth = 78; money_trait = "進攻投資型"
            else:
                st.session_state.wealth = 88; money_trait = "完整規劃型"
            if lifestyle == "高壓拚事業":
                st.session_state.mind = 58; mind_trait = "燃燒型工作者"
            elif lifestyle == "享樂優先":
                st.session_state.mind = 78; st.session_state.wealth -= 10; mind_trait = "即時快樂型"
            elif lifestyle == "自由斜槓":
                st.session_state.mind = 72; mind_trait = "自由探索型"
            else:
                st.session_state.mind = 82; mind_trait = "穩定生活型"
            if sleep == "常熬夜少運動":
                st.session_state.health = 55; health_trait = "健康警戒型"
            elif sleep == "偶爾運動":
                st.session_state.health = 70; health_trait = "普通續航型"
            elif sleep == "規律運動":
                st.session_state.health = 85; health_trait = "高續航型"
            else:
                st.session_state.health = 92; health_trait = "黃金體質型"
            st.session_state.goal = goal
            st.session_state.persona = f"{health_trait} × {mind_trait} × {money_trait}"
            add_log(f"25歲：你的人生目標是「{goal}」，人格為「{st.session_state.persona}」。")
            goto("game")
    with c2:
        if st.button("⬅ 回首頁", use_container_width=True):
            goto("start")

# =========================
# 頁面：主遊戲
# =========================
elif st.session_state.page == "game":
    st.markdown('<div class="title">🎮 Life 100：人生輪轉中</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="glass-card"><h3>🎯 目前任務</h3>
    <p>點擊 <b>「前進 5 年」</b> 讓人生繼續推進。每 10 年會進入 <b>人生規劃室</b>，你可以配置保險神盾，降低未來事件造成的損失。目標是在 100 歲前，讓「身、心、財」都不要歸零。</p></div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("年齡", f"{st.session_state.age} 歲")
    col2.metric("小樹點", st.session_state.tree)
    col3.metric("已配置保障", len(st.session_state.game_items))
    col4.metric("人生人格", st.session_state.persona[:8] + "...")
    age_timeline()

    left, right = st.columns([1.05, 0.95])
    with left:
        st.markdown('<div class="glass-card"><h3>🧍 角色狀態面板</h3></div>', unsafe_allow_html=True)
        stat_card("💪", "身 Health", st.session_state.health, "健康、疾病、體力與長照風險")
        stat_card("🧠", "心 Mind", st.session_state.mind, "壓力、情緒、心理韌性")
        stat_card("💰", "財 Wealth", st.session_state.wealth, "收入、資產、醫療支出承受力")
    with right:
        st.markdown('<div class="glass-card"><h3>📡 人生風險雷達</h3></div>', unsafe_allow_html=True)
        risk_chart()

    st.markdown('<div class="glass-card"><h3>🤖 AI 推薦保障</h3><p>根據你目前的身、心、財狀態，系統推薦以下保障：</p>', unsafe_allow_html=True)
    for r in recommend_items():
        st.markdown(f'<span class="badge">{r}</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-card"><h3>🎒 目前已配置保障</h3>', unsafe_allow_html=True)
    if st.session_state.game_items:
        for item in st.session_state.game_items:
            icon, tag, desc = product_info(item)
            st.markdown(f'<span class="badge">{icon} {item}</span>', unsafe_allow_html=True)
    else:
        st.write("尚未配置任何保障。下一個人生規劃室可以開始選擇。")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-card"><h3>📜 人生事件紀錄</h3>', unsafe_allow_html=True)
    for log in st.session_state.logs[-5:]:
        st.markdown(f'<div class="event-card">🎴 {log}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("⏩ 前進 5 年", use_container_width=True):
            st.session_state.age += 5
            event_pool = [
                ("過勞危機：連續加班讓身心急速下滑", -18, -16, -5),
                ("股市黑天鵝：市場震盪導致投資部位下跌", -3, -12, -28),
                ("重大疾病風險：醫療支出突然增加", -28, -12, -25),
                ("癌症治療：長期治療與自費療程造成壓力", -35, -16, -32),
                ("住院手術：突發手術造成醫療支出", -20, -8, -22),
                ("退休焦慮：收入轉換帶來不確定感", -8, -22, -16),
                ("長照需求出現：家庭照護與財務壓力同步上升", -32, -18, -34),
                ("失智照護：高齡照護需求增加", -20, -25, -30),
                ("親人離世：心理韌性遭受重大衝擊", -5, -38, -5),
                ("健康習慣回饋：規律作息讓身心回升", 12, 7, 4),
                ("資產配置成功：長期理財開始發酵", 0, 6, 22),
                ("家庭責任增加：照顧與支出壓力同步提高", -8, -16, -18),
                ("職涯升級：收入提升但壓力也增加", -5, -8, 24),
            ]
            name, dh, dm, dw = random.choice(event_pool)
            dh, dm, dw = apply_item_effects(name, dh, dm, dw)
            st.session_state.health = clamp(st.session_state.health + dh)
            st.session_state.mind = clamp(st.session_state.mind + dm)
            st.session_state.wealth = clamp(st.session_state.wealth + dw)
            if st.session_state.health >= 75:
                st.session_state.tree += 2
            st.session_state.last_event = name
            add_log(f"{st.session_state.age}歲：{name}")
            if st.session_state.age % 10 == 5:
                goto("shop")
            if st.session_state.health <= 0 or st.session_state.mind <= 0 or st.session_state.wealth <= 0 or st.session_state.age >= 100:
                goto("result")
            st.rerun()
    with c2:
        if st.button("📚 查看保險百科", use_container_width=True):
            goto("insurance_wiki")
    with c3:
        if st.button("🧭 遊戲說明", use_container_width=True):
            goto("game_guide")

# =========================
# 頁面：人生規劃室
# =========================
elif st.session_state.page == "shop":
    st.markdown('<div class="title">🛡️ 人生規劃室</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="glass-card"><h3>Step 3：選擇保障</h3>
    <p>這裡是每 10 年一次的人生決策點。請根據目前的身、心、財狀態，選擇適合的保障。卡片只放簡短資訊，想看完整內容可點「查看詳細百科」。</p></div>
    """, unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("目前財富", st.session_state.wealth)
    c2.metric("小樹點", st.session_state.tree)
    c3.metric("已配置保障", len(st.session_state.game_items))

    st.markdown('<div class="glass-card"><h3>🤖 本回合推薦</h3>', unsafe_allow_html=True)
    for r in recommend_items():
        st.markdown(f'<span class="badge">{r}</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    cols = st.columns(3)
    for idx, name in enumerate(SHOP_ITEMS):
        data = INSURANCE_DETAIL[name]
        icon = data["title"].split(" ")[0]
        final_cost = max(0, data["cost"] - st.session_state.tree)
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="rpg-card">
                <h2>{icon} {name}</h2>
                <div class="badge">{data['category']}</div>
                <p style="color:#d1d5db;">{data['short']}</p>
                <p><b>遊戲效果：</b>{data['effect']}</p>
                <h3>💰 成本：{data['cost']}　折抵後：{final_cost}</h3>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"配置 {name}", key=f"equip_{name}", use_container_width=True):
                equip_item(name)
            if st.button(f"📖 查看 {name} 詳細百科", key=f"wiki_{name}", use_container_width=True):
                goto("insurance_detail", selected_insurance=name, previous_page="shop")

    st.divider()
    if st.button("返回人生輪轉", use_container_width=True):
        goto("game")

# =========================
# 頁面：保險百科
# =========================
elif st.session_state.page == "insurance_wiki":
    st.markdown('<div class="title">📚 Life100 保險百科</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="glass-card"><h3>百科模式</h3>
    <p>這裡是保險知識圖鑑。你可以先了解各種保險在真實人生中的用途，再回到遊戲中配置適合自己的保障。</p></div>
    """, unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⬅ 回首頁", use_container_width=True):
            goto("start")
    with c2:
        if st.button("🎮 回到遊戲", use_container_width=True):
            goto("game")
    st.divider()
    for category, items in CATEGORIES.items():
        st.markdown(f"<h2>{category}</h2>", unsafe_allow_html=True)
        cols = st.columns(3)
        for i, item in enumerate(items):
            data = INSURANCE_DETAIL[item]
            with cols[i % 3]:
                st.markdown(f"""
                <div class="rpg-card">
                    <h3>{data['title']}</h3>
                    <p>{data['short']}</p>
                    <p><b>Life100：</b>{data['effect']}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"查看 {item}", key=f"open_{item}", use_container_width=True):
                    goto("insurance_detail", selected_insurance=item, previous_page="insurance_wiki")

# =========================
# 頁面：保險詳細
# =========================
elif st.session_state.page == "insurance_detail":
    selected = st.session_state.get("selected_insurance", "實支實付醫療險")
    insurance_detail_block(selected, show_back=True, allow_equip=True)

# =========================
# 頁面：結算
# =========================
elif st.session_state.page == "result":
    st.markdown('<div class="title">🏁 百歲人生結算報告</div>', unsafe_allow_html=True)
    survived = st.session_state.age >= 100 and min(st.session_state.health, st.session_state.mind, st.session_state.wealth) > 0
    if survived:
        st.success("恭喜你成功完成百歲人生挑戰！")
        ending = "百歲神盾王"
    else:
        st.error("挑戰結束：你的核心數值有一項歸零。")
        ending = "風險警戒者"
    st.markdown(f"""
    <div class="hero"><div class="badge">你的結局稱號</div>
    <div class="title">{ending}</div>
    <div class="subtitle">最終年齡：{st.session_state.age} 歲<br>人生人格：{st.session_state.persona}</div></div>
    """, unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: stat_card("💪", "身 Health", st.session_state.health, "最終健康狀態")
    with c2: stat_card("🧠", "心 Mind", st.session_state.mind, "最終心理韌性")
    with c3: stat_card("💰", "財 Wealth", st.session_state.wealth, "最終財務安全")
    scores = {"健康風險": st.session_state.health, "心理壓力": st.session_state.mind, "財務風險": st.session_state.wealth}
    weakest = min(scores, key=scores.get)
    st.markdown('<div class="glass-card"><h2>🔍 你的主要風險痛點</h2>', unsafe_allow_html=True)
    st.write(f"你的最大弱點是：**{weakest}**")
    st.write("建議優先查看以下保障：")
    for r in recommend_items():
        st.markdown(f'<span class="badge">{r}</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="glass-card"><h2>📜 人生回顧</h2>', unsafe_allow_html=True)
    for log in st.session_state.logs:
        st.markdown(f'<div class="event-card">{log}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🔄 重新開始", use_container_width=True):
            reset_game()
    with c2:
        if st.button("📚 查看保險百科", use_container_width=True):
            goto("insurance_wiki")
    with c3:
        if st.button("🏠 回首頁", use_container_width=True):
            goto("start")
