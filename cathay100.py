# cathay100.py
import streamlit as st
import random
import plotly.graph_objects as go

st.markdown("""
<style>

/* 最上方 Header */
header[data-testid="stHeader"]{
    background: rgba(0,0,0,0) !important;
}

/* Header底下那條 */
[data-testid="stToolbar"]{
    background: rgba(0,0,0,0) !important;
}

/* 主內容往上推 */
.block-container{
    padding-top: 1rem;
}

</style>
""", unsafe_allow_html=True)

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

html, body, [class*="css"] {
    font-family: 'Noto Sans TC', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 20% 20%, rgba(0, 255, 170, 0.25), transparent 30%),
        radial-gradient(circle at 80% 10%, rgba(38, 166, 91, 0.25), transparent 35%),
        linear-gradient(135deg, #06130d 0%, #0b1f17 45%, #07110d 100%);
    color: #f8fafc;
}

.block-container {
    padding-top: 2rem;
    max-width: 1200px;
}

.hero {
    padding: 42px;
    border-radius: 36px;
    background: linear-gradient(135deg, rgba(255,255,255,0.14), rgba(255,255,255,0.04));
    border: 1px solid rgba(255,255,255,0.18);
    box-shadow: 0 24px 80px rgba(0,0,0,0.35);
    backdrop-filter: blur(18px);
    position: relative;
    overflow: hidden;
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

@keyframes pulse {
    from { transform: scale(0.9); opacity: .55; }
    to { transform: scale(1.18); opacity: 1; }
}

.title {
    font-size: 64px;
    font-weight: 900;
    line-height: 1.1;
    letter-spacing: -1px;
}

.subtitle {
    font-size: 20px;
    color: #cbd5e1;
    margin-top: 12px;
}

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

.glass-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 26px 70px rgba(0,0,0,0.36);
}

.rpg-card {
    padding: 22px;
    border-radius: 24px;
    background: linear-gradient(135deg, rgba(0, 120, 72, .38), rgba(9, 25, 18, .68));
    border: 1px solid rgba(74, 222, 128, .35);
    box-shadow: inset 0 0 30px rgba(74, 222, 128, .08), 0 14px 42px rgba(0,0,0,.28);
    margin-bottom: 14px;
    animation: float 3.6s ease-in-out infinite;
}

@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-5px); }
    100% { transform: translateY(0px); }
}

.status-label {
    font-size: 15px;
    color: #bbf7d0;
    font-weight: 700;
}

.big-number {
    font-size: 38px;
    font-weight: 900;
}

.event-card {
    padding: 18px 20px;
    border-radius: 22px;
    background: linear-gradient(135deg, rgba(20, 83, 45, .55), rgba(15, 23, 42, .7));
    border-left: 6px solid #4ade80;
    border-top: 1px solid rgba(255,255,255,.14);
    margin-bottom: 12px;
    animation: pop .45s ease;
}

@keyframes pop {
    0% { opacity: 0; transform: scale(.95) translateY(8px); }
    100% { opacity: 1; transform: scale(1) translateY(0); }
}

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

.timeline {
    height: 12px;
    border-radius: 99px;
    background: rgba(255,255,255,.12);
    overflow: hidden;
    margin: 14px 0 8px 0;
}

.timeline-fill {
    height: 100%;
    border-radius: 99px;
    background: linear-gradient(90deg, #22c55e, #84cc16, #facc15);
    box-shadow: 0 0 24px rgba(34,197,94,.65);
}

button[kind="primary"], .stButton > button {
    border-radius: 999px !important;
    border: 1px solid rgba(74, 222, 128, .5) !important;
    background: linear-gradient(135deg, #16a34a, #22c55e) !important;
    color: white !important;
    font-weight: 800 !important;
    padding: 0.75rem 1.3rem !important;
    box-shadow: 0 12px 34px rgba(34, 197, 94, .28);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 18px 44px rgba(34, 197, 94, .38);
}

[data-testid="stMetricValue"] {
    color: #f8fafc;
    font-size: 34px;
}

[data-testid="stMetricLabel"] {
    color: #bbf7d0;
    font-weight: 700;
}

hr {
    border-color: rgba(255,255,255,.12);
}
</style>
""", unsafe_allow_html=True)

# =========================
# 初始化
# =========================
defaults = {
    "page": "start",
    "age": 25,
    "health": 80,
    "mind": 80,
    "wealth": 80,
    "tree": 0,
    "game_items": [],
    "logs": [],
    "persona": "尚未生成",
    "goal": "",
    "last_event": None,
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

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
    values = [
        100 - st.session_state.health,
        100 - st.session_state.mind,
        100 - st.session_state.wealth,
    ]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=labels + [labels[0]],
        fill="toself",
        name="Life Risk"
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f8fafc"),
        polar=dict(
            bgcolor="rgba(255,255,255,0.03)",
            radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(255,255,255,.15)"),
            angularaxis=dict(gridcolor="rgba(255,255,255,.15)")
        ),
        showlegend=False,
        height=430,
        margin=dict(l=40, r=40, t=30, b=30)
    )
    st.plotly_chart(fig, use_container_width=True)

def age_timeline():
    percent = int((st.session_state.age - 25) / 75 * 100)
    percent = clamp(percent)
    st.markdown(f"""
    <div class="glass-card">
        <div class="status-label">🕰️ 人生進度</div>
        <div class="timeline">
            <div class="timeline-fill" style="width:{percent}%"></div>
        </div>
        <div style="display:flex; justify-content:space-between; color:#cbd5e1;">
            <span>25歲</span><span>{st.session_state.age}歲</span><span>100歲</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def product_info(name):
    data = {
        "FitBack 健康吧": ("💪", "健康被動增益", "每回合降低健康損耗，並提高小樹點取得機率。"),
        "國泰長照險 / 失智險": ("🌳", "長期守護", "70 歲後遇到失能或長照危機時，大幅降低財務傷害。"),
        "CVX 泰好保 & 理賠聯盟鏈": ("⚡", "理賠效率升級", "遭遇疾病事件時，降低行政壓力造成的心理扣分。"),
        "心理關懷服務": ("🧠", "心理韌性護盾", "遭遇重大心理打擊時，將心力拉回安全線。"),
        "外溢型重大傷病險": ("🛡️", "重症財務護盾", "重大疾病發生時，抵擋大量財富損失。"),
        "國泰智能投資": ("💰", "AI 資產防禦", "市場黑天鵝事件時，降低財富波動。"),
    }
    return data[name]

# =========================
# 頁面：首頁
# =========================
if st.session_state.page == "start":
    st.markdown("""
    <div class="hero">
        <div class="badge">Cathay Life OS 100</div>
        <div class="title">Life 100<br>新泰度生存指南</div>
        <div class="subtitle">
            一場 5 分鐘的人生 RPG。從 25 歲走向 100 歲，<br>
            你能否維持「身、心、財」三大數值不歸零？
        </div>
        <br>
        <div>
            <span class="badge">🌳 國泰神盾</span>
            <span class="badge">🎮 人生模擬</span>
            <span class="badge">📡 風險雷達</span>
            <span class="badge">🛡️ RPG 道具</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""<div class="rpg-card"><h3>💪 身</h3><p>健康、體力、疾病風險。</p></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="rpg-card"><h3>🧠 心</h3><p>壓力、情緒、心理韌性。</p></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class="rpg-card"><h3>💰 財</h3><p>收入、保險、資產配置。</p></div>""", unsafe_allow_html=True)

    if st.button("🚀 開始百歲天賦測驗", use_container_width=True):
        st.session_state.page = "quiz"
        st.rerun()

# =========================
# 頁面：測驗
# =========================
elif st.session_state.page == "quiz":
    st.markdown('<div class="title">🧬 百歲天賦測驗</div>', unsafe_allow_html=True)
    st.write("回答 4 題，系統會生成你的初始人生面板。")

    with st.container():
        income = st.selectbox("1. 你的收入與理財狀態？", ["月光族", "有固定儲蓄", "積極投資", "財務規劃完整"])
        goal = st.selectbox("2. 你最想達成的人生目標？", ["買房", "財富自由", "健康退休", "照顧家人"])
        lifestyle = st.selectbox("3. 你嚮往的生活方式？", ["高壓拚事業", "自由斜槓", "穩定生活", "享樂優先"])
        sleep = st.selectbox("4. 你的健康作息？", ["常熬夜少運動", "偶爾運動", "規律運動", "飲食睡眠都穩定"])

    if st.button("✨ 生成我的人生面板", use_container_width=True):
        if income == "月光族":
            st.session_state.wealth = 55
            money_trait = "高波動財務型"
        elif income == "有固定儲蓄":
            st.session_state.wealth = 70
            money_trait = "穩健儲蓄型"
        elif income == "積極投資":
            st.session_state.wealth = 78
            money_trait = "進攻投資型"
        else:
            st.session_state.wealth = 88
            money_trait = "完整規劃型"

        if lifestyle == "高壓拚事業":
            st.session_state.mind = 58
            mind_trait = "燃燒型工作者"
        elif lifestyle == "享樂優先":
            st.session_state.mind = 78
            st.session_state.wealth -= 10
            mind_trait = "即時快樂型"
        elif lifestyle == "自由斜槓":
            st.session_state.mind = 72
            mind_trait = "自由探索型"
        else:
            st.session_state.mind = 82
            mind_trait = "穩定生活型"

        if sleep == "常熬夜少運動":
            st.session_state.health = 55
            health_trait = "健康警戒型"
        elif sleep == "偶爾運動":
            st.session_state.health = 70
            health_trait = "普通續航型"
        elif sleep == "規律運動":
            st.session_state.health = 85
            health_trait = "高續航型"
        else:
            st.session_state.health = 92
            health_trait = "黃金體質型"

        st.session_state.goal = goal
        st.session_state.persona = f"{health_trait} × {mind_trait} × {money_trait}"
        add_log(f"25歲：你的人生目標是「{goal}」，人格為「{st.session_state.persona}」。")
        st.session_state.page = "game"
        st.rerun()

# =========================
# 頁面：主遊戲
# =========================
elif st.session_state.page == "game":
    st.markdown('<div class="title">🎮 Life 100：人生輪轉中</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("年齡", f"{st.session_state.age} 歲")
    col2.metric("小樹點", st.session_state.tree)
    col3.metric("已配置神盾", len(st.session_state.game_items))
    col4.metric("人生人格", st.session_state.persona[:8] + "...")

    age_timeline()

    left, right = st.columns([1.05, 0.95])

    with left:
        st.markdown('<div class="glass-card"><h3>🧍 角色狀態面板</h3></div>', unsafe_allow_html=True)
        stat_card("💪", "身 Health", st.session_state.health, "健康、疾病、體力與長照風險")
        stat_card("🧠", "心 Mind", st.session_state.mind, "壓力、情緒、心理韌性")
        stat_card("💰", "財 Wealth", st.session_state.wealth, "收入、資產、醫療支出承受力")

    with right:
        st.markdown('<div class="glass-card"><h3>📡 3D 人生風險雷達</h3></div>', unsafe_allow_html=True)
        risk_chart()

    st.markdown('<div class="glass-card"><h3>🎒 目前裝備</h3>', unsafe_allow_html=True)
    if st.session_state.game_items:
        for item in st.session_state.game_items:
            icon, tag, desc = product_info(item)
            st.markdown(f'<span class="badge">{icon} {item}</span>', unsafe_allow_html=True)
    else:
        st.write("尚未配置任何國泰神盾。")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-card"><h3>📜 人生事件紀錄</h3>', unsafe_allow_html=True)
    for log in st.session_state.logs[-5:]:
        st.markdown(f'<div class="event-card">🎴 {log}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("⏩ 前進 5 年", use_container_width=True):
        st.session_state.age += 5

        event_pool = [
            ("過勞危機：連續加班讓身心急速下滑", -18, -16, -5),
            ("股市黑天鵝：投資部位大幅震盪", -3, -12, -28),
            ("重大疾病風險：醫療支出突然增加", -28, -12, -25),
            ("退休焦慮：收入轉換帶來不確定感", -8, -22, -16),
            ("長照需求出現：家庭照護與財務壓力同步上升", -32, -18, -34),
            ("親人離世：心理韌性遭受重大衝擊", -5, -38, -5),
            ("健康習慣回饋：規律作息讓身心回升", 12, 7, 4),
            ("資產配置成功：長期理財開始發酵", 0, 6, 22),
            ("家庭責任增加：照顧與支出壓力同步提高", -8, -16, -18),
            ("職涯升級：收入提升但壓力也增加", -5, -8, 24),
        ]

        name, dh, dm, dw = random.choice(event_pool)

        if "FitBack 健康吧" in st.session_state.game_items:
            dh += 8

        if "國泰長照險 / 失智險" in st.session_state.game_items and st.session_state.age >= 70:
            dh += 22
            dw += 28

        if "CVX 泰好保 & 理賠聯盟鏈" in st.session_state.game_items:
            dm += 8

        if "心理關懷服務" in st.session_state.game_items and dm < -20:
            dm += 26

        if "外溢型重大傷病險" in st.session_state.game_items and dh < -20:
            dw += 28

        if "國泰智能投資" in st.session_state.game_items and dw < -20:
            dw += 22

        st.session_state.health = clamp(st.session_state.health + dh)
        st.session_state.mind = clamp(st.session_state.mind + dm)
        st.session_state.wealth = clamp(st.session_state.wealth + dw)

        if st.session_state.health >= 75:
            st.session_state.tree += 2

        st.session_state.last_event = name
        add_log(f"{st.session_state.age}歲：{name}")

        if st.session_state.age % 10 == 5:
            st.session_state.page = "shop"

        if (
            st.session_state.health <= 0
            or st.session_state.mind <= 0
            or st.session_state.wealth <= 0
            or st.session_state.age >= 100
        ):
            st.session_state.page = "result"

        st.rerun()

# =========================
# 頁面：商城
# =========================
elif st.session_state.page == "shop":
    st.markdown('<div class="title">🛡️ 國泰神盾商城</div>', unsafe_allow_html=True)
    st.write("每 10 年決策點，你可以配置一項國泰資源，作為人生防禦裝備。")

    products = {
        "FitBack 健康吧": 10,
        "國泰長照險 / 失智險": 20,
        "CVX 泰好保 & 理賠聯盟鏈": 12,
        "心理關懷服務": 15,
        "外溢型重大傷病險": 20,
        "國泰智能投資": 18,
    }

    st.metric("目前財富", st.session_state.wealth)
    st.metric("目前小樹點", st.session_state.tree)

    cols = st.columns(3)
    product_names = list(products.keys())

    for idx, name in enumerate(product_names):
        icon, tag, desc = product_info(name)
        cost = products[name]

        with cols[idx % 3]:
            st.markdown(f"""
            <div class="rpg-card">
                <h2>{icon} {name}</h2>
                <div class="badge">{tag}</div>
                <p style="color:#d1d5db;">{desc}</p>
                <h3>💰 成本：{cost}</h3>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"配置 {name}", key=name, use_container_width=True):
                if name in st.session_state.game_items:
                    st.warning("你已經配置過這項神盾。")
                elif st.session_state.wealth >= cost:
                    st.session_state.wealth -= cost
                    st.session_state.game_items.append(name)
                    add_log(f"{st.session_state.age}歲：配置國泰神盾「{name}」。")
                    st.success("配置成功！")
                else:
                    st.error("財富不足，無法配置。")

    st.divider()

    if st.button("返回人生輪轉", use_container_width=True):
        st.session_state.page = "game"
        st.rerun()

# =========================
# 頁面：結算
# =========================
elif st.session_state.page == "result":
    st.markdown('<div class="title">🏁 百歲人生結算報告</div>', unsafe_allow_html=True)

    survived = st.session_state.age >= 100 and min(
        st.session_state.health,
        st.session_state.mind,
        st.session_state.wealth
    ) > 0

    if survived:
        st.success("恭喜你成功完成百歲人生挑戰！")
        ending = "百歲神盾王"
    else:
        st.error("挑戰結束：你的核心數值有一項歸零。")
        ending = "風險警戒者"

    st.markdown(f"""
    <div class="hero">
        <div class="badge">你的結局稱號</div>
        <div class="title">{ending}</div>
        <div class="subtitle">
            最終年齡：{st.session_state.age} 歲<br>
            人生人格：{st.session_state.persona}
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        stat_card("💪", "身 Health", st.session_state.health, "最終健康狀態")
    with c2:
        stat_card("🧠", "心 Mind", st.session_state.mind, "最終心理韌性")
    with c3:
        stat_card("💰", "財 Wealth", st.session_state.wealth, "最終財務安全")

    scores = {
        "健康風險": st.session_state.health,
        "心理壓力": st.session_state.mind,
        "財務風險": st.session_state.wealth,
    }
    weakest = min(scores, key=scores.get)

    st.markdown('<div class="glass-card"><h2>🔍 你的主要風險痛點</h2>', unsafe_allow_html=True)
    st.write(f"你的最大弱點是：**{weakest}**")

    if weakest == "健康風險":
        st.write("建議優先配置：FitBack 健康吧、長照險、外溢型重大傷病險。")
    elif weakest == "心理壓力":
        st.write("建議優先配置：心理關懷服務、CVX 泰好保與理賠聯盟鏈。")
    else:
        st.write("建議優先配置：國泰智能投資、重大傷病險與完整財務規劃。")

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-card"><h2>📜 人生回顧</h2>', unsafe_allow_html=True)
    for log in st.session_state.logs:
        st.markdown(f'<div class="event-card">{log}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔄 重新開始", use_container_width=True):
        reset_game()
