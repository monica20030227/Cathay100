# app.py
import streamlit as st
import plotly.graph_objects as go

from insurance_db import INSURANCE_LIBRARY, get_product_by_item
from game_engine import next_event, clamp
from recommendation import recommend_products_detailed, coverage_scores, strongest_risk, status_level
from insurance_page import render_insurance_page
from shop import render_shop

st.set_page_config(
    page_title="Life 100：新泰度生存指南",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="collapsed",
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
    padding: 42px; border-radius: 36px;
    background: linear-gradient(135deg, rgba(255,255,255,0.14), rgba(255,255,255,0.04));
    border: 1px solid rgba(255,255,255,0.18);
    box-shadow: 0 24px 80px rgba(0,0,0,0.35);
    backdrop-filter: blur(18px); position: relative; overflow: hidden; margin-bottom: 20px;
}
.hero:before {
    content: ""; position: absolute; width: 280px; height: 280px; right: -80px; top: -80px;
    background: radial-gradient(circle, rgba(0, 220, 130, 0.4), transparent 65%);
    border-radius: 50%; animation: pulse 4s infinite alternate;
}
@keyframes pulse { from { transform: scale(0.9); opacity: .55; } to { transform: scale(1.18); opacity: 1; } }
.title { font-size: 58px; font-weight: 900; line-height: 1.1; letter-spacing: -1px; }
.subtitle { font-size: 19px; color: #cbd5e1; margin-top: 12px; line-height: 1.8; }
.glass-card {
    padding: 24px; border-radius: 28px;
    background: linear-gradient(135deg, rgba(255,255,255,0.13), rgba(255,255,255,0.045));
    border: 1px solid rgba(255,255,255,0.16);
    box-shadow: 0 18px 50px rgba(0,0,0,0.25);
    backdrop-filter: blur(16px); margin-bottom: 18px; transition: .25s ease;
}
.glass-card:hover { transform: translateY(-3px); box-shadow: 0 26px 70px rgba(0,0,0,0.36); }
.rpg-card, .product-card {
    padding: 22px; border-radius: 24px;
    background: linear-gradient(135deg, rgba(0, 120, 72, .38), rgba(9, 25, 18, .68));
    border: 1px solid rgba(74, 222, 128, .35);
    box-shadow: inset 0 0 30px rgba(74, 222, 128, .08), 0 14px 42px rgba(0,0,0,.28);
    margin-bottom: 14px; min-height: 170px;
}
.rpg-card:hover, .product-card:hover { transform: translateY(-4px); }
.product-title { font-size: 22px; font-weight: 900; margin-top: 10px; }
.product-subtitle { color:#bbf7d0; font-weight:700; margin: 6px 0 10px 0; }
.section-label { color:#bbf7d0; font-weight:900; margin-top:12px; }
.small-text { color:#d1d5db; font-size:15px; line-height:1.7; }
.status-label { font-size: 15px; color: #bbf7d0; font-weight: 700; }
.big-number { font-size: 38px; font-weight: 900; }
.event-card, .effect-box {
    padding: 18px 20px; border-radius: 22px;
    background: linear-gradient(135deg, rgba(20, 83, 45, .55), rgba(15, 23, 42, .7));
    border-left: 6px solid #4ade80; border-top: 1px solid rgba(255,255,255,.14);
    margin-bottom: 12px; animation: pop .45s ease;
}
@keyframes pop { 0% { opacity: 0; transform: scale(.95) translateY(8px); } 100% { opacity: 1; transform: scale(1) translateY(0); } }
.badge {
    display: inline-block; padding: 7px 12px; border-radius: 999px;
    background: rgba(34, 197, 94, .18); border: 1px solid rgba(74, 222, 128, .35);
    color: #bbf7d0; font-weight: 700; margin: 4px 6px 4px 0;
}
.timeline { height: 12px; border-radius: 99px; background: rgba(255,255,255,.12); overflow: hidden; margin: 14px 0 8px 0; }
.timeline-fill { height: 100%; border-radius: 99px; background: linear-gradient(90deg, #22c55e, #84cc16, #facc15); box-shadow: 0 0 24px rgba(34,197,94,.65); }
.stButton > button {
    border-radius: 999px !important; border: 1px solid rgba(74, 222, 128, .5) !important;
    background: linear-gradient(135deg, #16a34a, #22c55e) !important;
    color: white !important; font-weight: 800 !important; padding: 0.75rem 1.3rem !important;
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
# 初始化
# =========================
def init_state():
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
        "last_event_tag": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# =========================
# 工具函式
# =========================
def goto(page, **kwargs):
    for k, v in kwargs.items():
        st.session_state[k] = v
    st.session_state.page = page
    st.rerun()


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


def product_badges():
    if not st.session_state.game_items:
        st.write("尚未配置任何保障。下一個人生規劃室可以開始選擇。")
        return
    for item in st.session_state.game_items:
        p = get_product_by_item(item)
        if p:
            st.markdown(f'<span class="badge">{p["icon"]} {p["game_item"]}</span>', unsafe_allow_html=True)
        else:
            st.markdown(f'<span class="badge">{item}</span>', unsafe_allow_html=True)


def simple_ai_recommendation_panel():
    recs = recommend_products_detailed(
        st.session_state.health,
        st.session_state.mind,
        st.session_state.wealth,
        age=st.session_state.age,
        last_event_tag=st.session_state.get("last_event_tag"),
        owned=st.session_state.game_items,
        limit=3,
        goal=st.session_state.get("goal", ""),
    )
    st.markdown('<div class="glass-card"><h3>🤖 AI 推薦保障</h3><p class="small-text">根據目前狀態與最近事件，推薦下次人生規劃室可優先考慮的實際商品。</p>', unsafe_allow_html=True)
    for row in recs:
        p = row["product"]
        st.markdown(f'<span class="badge">{p["icon"]} {p["game_item"]}｜{row["score"]}%</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def coverage_panel():
    scores = coverage_scores(st.session_state.game_items)
    st.markdown('<div class="glass-card"><h3>📊 目前保障覆蓋率</h3></div>', unsafe_allow_html=True)
    cols = st.columns(4)
    for i, (label, value) in enumerate(scores.items()):
        with cols[i]:
            st.metric(label, f"{value}%")
            st.progress(value / 100)

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
            這版保留所有實際國泰保險商品資料，並加入 AI 人生保障顧問。
        </div>
        <br>
        <span class="badge">🎮 人生遊戲</span><span class="badge">📚 保險百科</span><span class="badge">🤖 AI保障分析</span>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="rpg-card"><h2>🎮 人生遊戲模式</h2>
        <p class="small-text">從 25 歲開始，面對疾病、投資、長照、退休與家庭風險，挑戰活到 100 歲。</p>
        <p class="small-text"><b>流程：</b>測驗 → 每 5 年前進 → 10 年決策點 → AI推薦保障 → 百歲結算</p></div>
        """, unsafe_allow_html=True)
        if st.button("🚀 開始人生遊戲", use_container_width=True):
            goto("quiz")
    with col2:
        st.markdown("""
        <div class="rpg-card"><h2>📚 Life100 保險百科</h2>
        <p class="small-text">查看實際商品用途、保障內容、適合族群、遊戲效果與國泰官方商品連結。</p></div>
        """, unsafe_allow_html=True)
        if st.button("📖 查看保險百科", use_container_width=True):
            goto("insurance_wiki")
    with col3:
        st.markdown("""
        <div class="rpg-card"><h2>🧭 遊戲說明</h2>
        <p class="small-text">第一次使用建議先看玩法。了解身、心、財三大數值、小樹點與人生規劃室。</p></div>
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
        <p class="small-text">從 25 歲開始一路走到 100 歲，並讓三個核心數值都不要歸零：</p>
        <span class="badge">💪 身 Health</span><span class="badge">🧠 心 Mind</span><span class="badge">💰 財 Wealth</span>
    </div>
    <div class="glass-card">
        <h2>怎麼玩？</h2>
        <div class="event-card">Step 1：完成 4 題百歲天賦測驗，生成初始人生面板。</div>
        <div class="event-card">Step 2：點擊「前進 5 年」，觸發人生事件，例如過勞、股災、重大疾病、癌症、長照、意外。</div>
        <div class="event-card">Step 3：每 10 年進入「人生規劃室」，AI 會根據你目前狀態推薦實際保險商品。</div>
        <div class="event-card">Step 4：保險會在未來事件中抵銷 Health、Mind 或 Wealth 的損失。</div>
        <div class="event-card">Step 5：到 100 歲後產出人生結算報告。</div>
    </div>
    <div class="glass-card">
        <h2>AI 人生保障顧問</h2>
        <p class="small-text">AI 顧問會產出保障覆蓋率、Top 3 推薦、推薦原因、推薦分數，以及「未投保 vs 投保後」的情境比較。商品內容仍完全來自保險百科資料庫。</p>
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
    <p class="small-text">回答 4 題，系統會生成你的初始身、心、財數值。之後你將從 25 歲開始挑戰百歲人生。</p></div>
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
    <p class="small-text">點擊 <b>「前進 5 年」</b> 讓人生繼續推進。每 10 年會進入 <b>人生規劃室</b>，你可以配置保障，降低未來事件造成的損失。</p></div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("年齡", f"{st.session_state.age} 歲")
    col2.metric("小樹點", st.session_state.tree)
    col3.metric("已配置保障", len(st.session_state.game_items))
    col4.metric("主要風險", strongest_risk(st.session_state.health, st.session_state.mind, st.session_state.wealth))
    age_timeline()

    left, right = st.columns([1.05, 0.95])
    with left:
        st.markdown('<div class="glass-card"><h3>🧍 角色狀態面板</h3></div>', unsafe_allow_html=True)
        stat_card("💪", "身 Health", st.session_state.health, f"健康狀態：{status_level(st.session_state.health)}")
        stat_card("🧠", "心 Mind", st.session_state.mind, f"心理韌性：{status_level(st.session_state.mind)}")
        stat_card("💰", "財 Wealth", st.session_state.wealth, f"財務安全：{status_level(st.session_state.wealth)}")
    with right:
        st.markdown('<div class="glass-card"><h3>📡 人生風險雷達</h3></div>', unsafe_allow_html=True)
        risk_chart()

    simple_ai_recommendation_panel()
    coverage_panel()

    st.markdown('<div class="glass-card"><h3>🎒 目前已配置保障</h3>', unsafe_allow_html=True)
    product_badges()
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.get("last_event"):
        st.markdown('<div class="glass-card"><h3>🧾 最近事件</h3>', unsafe_allow_html=True)
        st.markdown(f'<div class="event-card">{st.session_state.last_event}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-card"><h3>📜 人生事件紀錄</h3>', unsafe_allow_html=True)
    for log in st.session_state.logs[-6:]:
        st.markdown(f'<div class="event-card">🎴 {log}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("⏩ 前進 5 年", use_container_width=True):
            st.session_state.age += 5
            event, h, m, w, tree_gain, effect_logs = next_event(
                st.session_state.age,
                st.session_state.health,
                st.session_state.mind,
                st.session_state.wealth,
                st.session_state.game_items,
            )
            st.session_state.health = h
            st.session_state.mind = m
            st.session_state.wealth = w
            st.session_state.tree += tree_gain
            st.session_state.last_event = event["name"]
            st.session_state.last_event_tag = event["tag"]
            add_log(f"{st.session_state.age}歲：{event['name']}")
            for e in effect_logs:
                add_log(f"{st.session_state.age}歲：{e}")
            if tree_gain:
                add_log(f"{st.session_state.age}歲：健康狀態良好，獲得小樹點 +{tree_gain}。")
            if st.session_state.health <= 0 or st.session_state.mind <= 0 or st.session_state.wealth <= 0 or st.session_state.age >= 100:
                goto("result")
            if st.session_state.age % 10 == 5:
                goto("shop")
            st.rerun()
    with c2:
        if st.button("🛡️ 進入人生規劃室", use_container_width=True):
            goto("shop")
    with c3:
        if st.button("📚 查看保險百科", use_container_width=True):
            goto("insurance_wiki")
    with c4:
        if st.button("🧭 遊戲說明", use_container_width=True):
            goto("game_guide")

# =========================
# 頁面：人生規劃室
# =========================
elif st.session_state.page == "shop":
    render_shop()

# =========================
# 頁面：保險百科
# =========================
elif st.session_state.page == "insurance_wiki":
    render_insurance_page()

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
    with c1:
        stat_card("💪", "身 Health", st.session_state.health, "最終健康狀態")
    with c2:
        stat_card("🧠", "心 Mind", st.session_state.mind, "最終心理韌性")
    with c3:
        stat_card("💰", "財 Wealth", st.session_state.wealth, "最終財務安全")

    coverage_panel()

    st.markdown('<div class="glass-card"><h2>🔍 你的主要風險痛點</h2>', unsafe_allow_html=True)
    st.write(f"你的最大弱點是：**{strongest_risk(st.session_state.health, st.session_state.mind, st.session_state.wealth)}**")
    st.write("建議優先查看以下實際保障商品：")
    recs = recommend_products_detailed(
        st.session_state.health,
        st.session_state.mind,
        st.session_state.wealth,
        age=st.session_state.age,
        last_event_tag=st.session_state.get("last_event_tag"),
        owned=st.session_state.game_items,
        limit=3,
        goal=st.session_state.get("goal", ""),
    )
    for row in recs:
        p = row["product"]
        st.markdown(f'<span class="badge">{p["icon"]} {p["game_item"]}｜推薦度 {row["score"]}%</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-card"><h2>🎒 你配置過的保障</h2>', unsafe_allow_html=True)
    product_badges()
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
