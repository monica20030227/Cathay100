# app.py
import streamlit as st
import plotly.graph_objects as go
from insurance_db import get_product_by_item
from game_engine import next_event, clamp
from insurance_page import render_insurance_page
from shop import render_shop
from recommendation import recommend_products

st.set_page_config(page_title="Life 100：新泰度生存指南", page_icon="🌳", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;600;700;900&display=swap');
html, body, [class*="css"] {font-family:'Noto Sans TC',sans-serif;}
.stApp {background: radial-gradient(circle at 20% 20%, rgba(0,255,170,.25), transparent 30%), radial-gradient(circle at 80% 10%, rgba(38,166,91,.25), transparent 35%), linear-gradient(135deg,#06130d 0%,#0b1f17 45%,#07110d 100%); color:#f8fafc;}
header[data-testid="stHeader"], [data-testid="stToolbar"] {background:rgba(0,0,0,0)!important;}
#MainMenu, footer {visibility:hidden;}
.block-container {padding-top:1rem; max-width:1200px;}
.hero {padding:42px; border-radius:36px; background:linear-gradient(135deg,rgba(255,255,255,.14),rgba(255,255,255,.04)); border:1px solid rgba(255,255,255,.18); box-shadow:0 24px 80px rgba(0,0,0,.35); backdrop-filter:blur(18px); position:relative; overflow:hidden; margin-bottom:20px;}
.hero:before {content:""; position:absolute; width:280px; height:280px; right:-80px; top:-80px; background:radial-gradient(circle,rgba(0,220,130,.4),transparent 65%); border-radius:50%; animation:pulse 4s infinite alternate;}
@keyframes pulse {from{transform:scale(.9);opacity:.55;} to{transform:scale(1.18);opacity:1;}}
.title {font-size:60px; font-weight:900; line-height:1.1; letter-spacing:-1px;}
.subtitle {font-size:20px; color:#cbd5e1; margin-top:12px; line-height:1.7;}
.glass-card,.product-card {padding:24px; border-radius:28px; background:linear-gradient(135deg,rgba(255,255,255,.13),rgba(255,255,255,.045)); border:1px solid rgba(255,255,255,.16); box-shadow:0 18px 50px rgba(0,0,0,.25); backdrop-filter:blur(16px); margin-bottom:18px; transition:.25s ease;}
.glass-card:hover,.product-card:hover {transform:translateY(-4px); box-shadow:0 26px 70px rgba(0,0,0,.36);}
.rpg-card {padding:22px; border-radius:24px; background:linear-gradient(135deg,rgba(0,120,72,.38),rgba(9,25,18,.68)); border:1px solid rgba(74,222,128,.35); box-shadow:inset 0 0 30px rgba(74,222,128,.08),0 14px 42px rgba(0,0,0,.28); margin-bottom:14px; animation:float 3.6s ease-in-out infinite;}
@keyframes float {0%{transform:translateY(0)}50%{transform:translateY(-5px)}100%{transform:translateY(0)}}
.status-label,.product-subtitle,.section-label {font-size:15px; color:#bbf7d0; font-weight:800;}
.big-number {font-size:38px; font-weight:900;}
.event-card {padding:18px 20px; border-radius:22px; background:linear-gradient(135deg,rgba(20,83,45,.55),rgba(15,23,42,.7)); border-left:6px solid #4ade80; border-top:1px solid rgba(255,255,255,.14); margin-bottom:12px; animation:pop .45s ease;}
@keyframes pop {0%{opacity:0;transform:scale(.95) translateY(8px)}100%{opacity:1;transform:scale(1) translateY(0)}}
.badge {display:inline-block; padding:7px 12px; border-radius:999px; background:rgba(34,197,94,.18); border:1px solid rgba(74,222,128,.35); color:#bbf7d0; font-weight:800; margin:4px 6px 4px 0; font-size:13px;}
.timeline {height:12px; border-radius:99px; background:rgba(255,255,255,.12); overflow:hidden; margin:14px 0 8px;}
.timeline-fill {height:100%; border-radius:99px; background:linear-gradient(90deg,#22c55e,#84cc16,#facc15); box-shadow:0 0 24px rgba(34,197,94,.65);}
.product-title {font-size:24px; font-weight:900; margin:8px 0;}
.small-text {color:#d1d5db; font-size:14px; line-height:1.8;}
.effect-box {padding:14px 16px; border-radius:18px; background:rgba(34,197,94,.13); border:1px solid rgba(74,222,128,.32); color:#dcfce7; margin-top:12px; font-weight:700;}
button[kind="primary"], .stButton>button {border-radius:999px!important; border:1px solid rgba(74,222,128,.5)!important; background:linear-gradient(135deg,#16a34a,#22c55e)!important; color:white!important; font-weight:800!important; padding:.75rem 1.3rem!important; box-shadow:0 12px 34px rgba(34,197,94,.28);}
.stButton>button:hover {transform:translateY(-2px); box-shadow:0 18px 44px rgba(34,197,94,.38);}
[data-testid="stMetricValue"] {color:#f8fafc; font-size:34px;} [data-testid="stMetricLabel"] {color:#bbf7d0; font-weight:700;} a {color:#86efac!important; font-weight:800; text-decoration:none;} hr {border-color:rgba(255,255,255,.12);}
</style>
""", unsafe_allow_html=True)

def init_state():
    defaults = {"page":"start","age":25,"health":80,"mind":80,"wealth":80,"tree":0,"game_items":[],"logs":[],"persona":"尚未生成","goal":"","last_event":None,"last_event_tag":None}
    for k,v in defaults.items():
        if k not in st.session_state: st.session_state[k]=v
init_state()

def add_log(text): st.session_state.logs.append(text)
def reset_game():
    for k in list(st.session_state.keys()): del st.session_state[k]
    st.rerun()

def stat_card(icon,label,value,desc):
    st.markdown(f"<div class='glass-card'><div class='status-label'>{icon} {label}</div><div class='big-number'>{value}/100</div><div class='small-text'>{desc}</div></div>", unsafe_allow_html=True)
    st.progress(value/100)

def risk_chart():
    labels=["健康風險","心理壓力","財務風險"]
    values=[100-st.session_state.health,100-st.session_state.mind,100-st.session_state.wealth]
    fig=go.Figure()
    fig.add_trace(go.Scatterpolar(r=values+[values[0]], theta=labels+[labels[0]], fill="toself", name="Life Risk"))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#f8fafc"), polar=dict(bgcolor="rgba(255,255,255,.03)", radialaxis=dict(visible=True, range=[0,100], gridcolor="rgba(255,255,255,.15)"), angularaxis=dict(gridcolor="rgba(255,255,255,.15)")), showlegend=False, height=430, margin=dict(l=40,r=40,t=30,b=30))
    st.plotly_chart(fig, use_container_width=True)

def age_timeline():
    percent=clamp(int((st.session_state.age-25)/75*100))
    st.markdown(f"<div class='glass-card'><div class='status-label'>🕰️ 人生進度</div><div class='timeline'><div class='timeline-fill' style='width:{percent}%'></div></div><div style='display:flex;justify-content:space-between;color:#cbd5e1;'><span>25歲</span><span>{st.session_state.age}歲</span><span>100歲</span></div></div>", unsafe_allow_html=True)

def product_info(name):
    p=get_product_by_item(name)
    if p: return p["icon"], p["type"], p["short"]
    return "🛡️","保障道具","人生防禦裝備"

def top_nav():
    c1,c2,c3=st.columns(3)
    with c1:
        if st.button("🏠 首頁", use_container_width=True): st.session_state.page="start"; st.rerun()
    with c2:
        if st.button("🎮 回到遊戲", use_container_width=True): st.session_state.page="game"; st.rerun()
    with c3:
        if st.button("📚 保險百科", use_container_width=True): st.session_state.page="insurance"; st.rerun()

if st.session_state.page == "start":
    st.markdown("""
    <div class="hero"><div class="badge">Cathay Life OS 100</div><div class="title">Life 100<br>新泰度生存指南</div><div class="subtitle">一場 5 分鐘的人生 RPG。從 25 歲走向 100 歲，<br>你能否維持「身、心、財」三大數值不歸零？</div><br><div><span class="badge">🌳 國泰神盾</span><span class="badge">🎮 人生模擬</span><span class="badge">📡 風險雷達</span><span class="badge">🛡️ 保險百科</span></div></div>
    """, unsafe_allow_html=True)
    c1,c2,c3=st.columns(3)
    with c1: st.markdown("<div class='rpg-card'><h3>💪 身</h3><p>健康、體力、疾病風險。</p></div>", unsafe_allow_html=True)
    with c2: st.markdown("<div class='rpg-card'><h3>🧠 心</h3><p>壓力、情緒、心理韌性。</p></div>", unsafe_allow_html=True)
    with c3: st.markdown("<div class='rpg-card'><h3>💰 財</h3><p>收入、保險、資產配置。</p></div>", unsafe_allow_html=True)
    a,b=st.columns(2)
    with a:
        if st.button("🚀 開始百歲天賦測驗", use_container_width=True): st.session_state.page="quiz"; st.rerun()
    with b:
        if st.button("📚 先看 Life100 保險百科", use_container_width=True): st.session_state.page="insurance"; st.rerun()

elif st.session_state.page == "quiz":
    top_nav()
    st.markdown('<div class="title">🧬 百歲天賦測驗</div>', unsafe_allow_html=True)
    st.write("回答 4 題，系統會生成你的初始人生面板。")
    income=st.selectbox("1. 你的收入與理財狀態？", ["月光族","有固定儲蓄","積極投資","財務規劃完整"])
    goal=st.selectbox("2. 你最想達成的人生目標？", ["買房","財富自由","健康退休","照顧家人"])
    lifestyle=st.selectbox("3. 你嚮往的生活方式？", ["高壓拚事業","自由斜槓","穩定生活","享樂優先"])
    sleep=st.selectbox("4. 你的健康作息？", ["常熬夜少運動","偶爾運動","規律運動","飲食睡眠都穩定"])
    if st.button("✨ 生成我的人生面板", use_container_width=True):
        wealth_map={"月光族":(55,"高波動財務型"),"有固定儲蓄":(70,"穩健儲蓄型"),"積極投資":(78,"進攻投資型"),"財務規劃完整":(88,"完整規劃型")}
        st.session_state.wealth, money_trait=wealth_map[income]
        if lifestyle=="高壓拚事業": st.session_state.mind=58; mind_trait="燃燒型工作者"
        elif lifestyle=="享樂優先": st.session_state.mind=78; st.session_state.wealth-=10; mind_trait="即時快樂型"
        elif lifestyle=="自由斜槓": st.session_state.mind=72; mind_trait="自由探索型"
        else: st.session_state.mind=82; mind_trait="穩定生活型"
        health_map={"常熬夜少運動":(55,"健康警戒型"),"偶爾運動":(70,"普通續航型"),"規律運動":(85,"高續航型"),"飲食睡眠都穩定":(92,"黃金體質型")}
        st.session_state.health, health_trait=health_map[sleep]
        st.session_state.goal=goal; st.session_state.persona=f"{health_trait} × {mind_trait} × {money_trait}"
        add_log(f"25歲：你的人生目標是「{goal}」，人格為「{st.session_state.persona}」。")
        st.session_state.page="game"; st.rerun()

elif st.session_state.page == "game":
    top_nav()
    st.markdown('<div class="title">🎮 Life 100：人生輪轉中</div>', unsafe_allow_html=True)
    col1,col2,col3,col4=st.columns(4)
    col1.metric("年齡",f"{st.session_state.age} 歲"); col2.metric("小樹點",st.session_state.tree); col3.metric("已配置神盾",len(st.session_state.game_items)); col4.metric("人生人格",st.session_state.persona[:8]+"...")
    age_timeline()
    left,right=st.columns([1.05,.95])
    with left:
        st.markdown('<div class="glass-card"><h3>🧍 角色狀態面板</h3></div>', unsafe_allow_html=True)
        stat_card("💪","身 Health",st.session_state.health,"健康、疾病、體力與長照風險")
        stat_card("🧠","心 Mind",st.session_state.mind,"壓力、情緒、心理韌性")
        stat_card("💰","財 Wealth",st.session_state.wealth,"收入、資產、醫療支出承受力")
    with right:
        st.markdown('<div class="glass-card"><h3>📡 3D 人生風險雷達</h3></div>', unsafe_allow_html=True); risk_chart()
    st.markdown('<div class="glass-card"><h3>🎒 目前裝備</h3>', unsafe_allow_html=True)
    if st.session_state.game_items:
        for item in st.session_state.game_items:
            icon,tag,desc=product_info(item); st.markdown(f'<span class="badge">{icon} {item}</span>', unsafe_allow_html=True)
    else: st.write("尚未配置任何國泰神盾。")
    st.markdown('</div>', unsafe_allow_html=True)
    if st.session_state.last_event_tag:
        recs = recommend_products(st.session_state.health, st.session_state.mind, st.session_state.wealth, st.session_state.last_event_tag, st.session_state.game_items, limit=2)
        st.markdown('<div class="glass-card"><h3>📖 根據最近事件的推薦保障</h3>', unsafe_allow_html=True)
        for _, p, reason in recs:
            st.markdown(f"<span class='badge'>{p['icon']} {p['game_item']}｜{reason}</span>", unsafe_allow_html=True)
        if st.button("查看推薦保障商城", use_container_width=True): st.session_state.page="shop"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="glass-card"><h3>📜 人生事件紀錄</h3>', unsafe_allow_html=True)
    for log in st.session_state.logs[-5:]: st.markdown(f'<div class="event-card">🎴 {log}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("⏩ 前進 5 年", use_container_width=True):
        st.session_state.age += 5
        event, h, m, w, tree_gain, effect_logs = next_event(st.session_state.age, st.session_state.health, st.session_state.mind, st.session_state.wealth, st.session_state.game_items)
        st.session_state.health=h; st.session_state.mind=m; st.session_state.wealth=w; st.session_state.tree += tree_gain
        st.session_state.last_event=event["name"]; st.session_state.last_event_tag=event["tag"]
        add_log(f"{st.session_state.age}歲：{event['name']}")
        for e in effect_logs: add_log(e)
        if tree_gain: add_log(f"健康水位良好，獲得小樹點 +{tree_gain}。")
        if st.session_state.age % 10 == 5: st.session_state.page="shop"
        if st.session_state.health<=0 or st.session_state.mind<=0 or st.session_state.wealth<=0 or st.session_state.age>=100: st.session_state.page="result"
        st.rerun()

elif st.session_state.page == "shop":
    top_nav(); render_shop()

elif st.session_state.page == "insurance":
    top_nav(); render_insurance_page()

elif st.session_state.page == "result":
    top_nav()
    st.markdown('<div class="title">🏁 百歲人生結算報告</div>', unsafe_allow_html=True)
    survived = st.session_state.age>=100 and min(st.session_state.health, st.session_state.mind, st.session_state.wealth)>0
    ending = "百歲神盾王" if survived else "風險警戒者"
    if survived: st.success("恭喜你成功完成百歲人生挑戰！")
    else: st.error("挑戰結束：你的核心數值有一項歸零。")
    st.markdown(f"<div class='hero'><div class='badge'>你的結局稱號</div><div class='title'>{ending}</div><div class='subtitle'>最終年齡：{st.session_state.age} 歲<br>人生人格：{st.session_state.persona}</div></div>", unsafe_allow_html=True)
    c1,c2,c3=st.columns(3)
    with c1: stat_card("💪","身 Health",st.session_state.health,"最終健康狀態")
    with c2: stat_card("🧠","心 Mind",st.session_state.mind,"最終心理韌性")
    with c3: stat_card("💰","財 Wealth",st.session_state.wealth,"最終財務安全")
    scores={"健康風險":st.session_state.health,"心理壓力":st.session_state.mind,"財務風險":st.session_state.wealth}
    weakest=min(scores,key=scores.get)
    st.markdown('<div class="glass-card"><h2>🔍 你的主要風險痛點</h2>', unsafe_allow_html=True)
    st.write(f"你的最大弱點是：**{weakest}**")
    recs=recommend_products(st.session_state.health, st.session_state.mind, st.session_state.wealth, st.session_state.last_event_tag, st.session_state.game_items, limit=3)
    st.write("建議補強：" + "、".join([p['game_item'] for _,p,_ in recs]))
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="glass-card"><h2>📜 人生回顧</h2>', unsafe_allow_html=True)
    for log in st.session_state.logs: st.markdown(f'<div class="event-card">{log}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("🔄 重新開始", use_container_width=True): reset_game()
