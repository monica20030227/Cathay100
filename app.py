# app.py
import streamlit as st
import random
import plotly.graph_objects as go
from insurance_db import get_product_by_item
from game_engine import next_event, clamp, analyze_life_risk, protection_score
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
.light-ai-card {padding:24px; border-radius:20px; background:linear-gradient(135deg,#f8fafc,#e2e8f0); color:#0f172a; border:1px solid #cbd5e1; box-shadow:0 10px 30px rgba(0,0,0,.15); margin-top:15px; font-size:16px; line-height:1.7;}
.light-ai-card h4 {color:#16a34a; margin-top:0; font-weight:900;}
.protection-score {text-align:center; margin:18px 0; padding:18px; border-radius:22px; background:rgba(255,255,255,.07); border:1px solid rgba(255,255,255,.15);}
.protection-score span {font-size:50px; font-weight:900; color:#4ade80;}
.guide-step {padding:16px 18px; border-radius:20px; background:rgba(20,83,45,.42); border-left:5px solid #86efac; margin:10px 0; color:#dcfce7;}
.rpg-card {min-height:170px;}
</style>
""", unsafe_allow_html=True)

def init_state():
    defaults = {"page":"start","age":25,"health":80,"mind":80,"wealth":80,"tree":0,"game_items":[],"logs":[],"persona":"尚未生成","goal":"","last_event":None,"last_event_tag":None,"previous_page":"start","defense_notice":"", "history":{"age":[25],"health":[80],"mind":[80],"wealth":[80]}}
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

def goto(page):
    st.session_state.page = page
    st.rerun()

def top_nav():
    c1,c2,c3,c4=st.columns(4)
    with c1:
        if st.button("🏠 首頁", use_container_width=True): goto("start")
    with c2:
        if st.button("🎮 回到遊戲", use_container_width=True): goto("game")
    with c3:
        if st.button("📚 保險百科", use_container_width=True): goto("insurance")
    with c4:
        if st.button("🧭 遊戲說明", use_container_width=True): goto("guide")

def render_ai_review(weakest, recs, scores):
    last_event = st.session_state.last_event or "尚未發生重大事件"
    rec_name = recs[0][1]["game_item"] if recs else "FitBack 健康吧"
    
    weakest_val = scores.get(weakest, 0)
    what_if_score = min(100, weakest_val + 45) # 模擬配置保險後的平行宇宙得分
    
    st.markdown(f"""
    <div class='light-ai-card'>
      <h4>【AI 軌跡分析報告】</h4>
      <p>你以「<b>{st.session_state.persona}</b>」的開局走到 {st.session_state.age} 歲，人生目標是「<b>{st.session_state.goal}</b>」。</p>
      <p>系統追蹤到最近一次關鍵衝擊為：「<b>{last_event}</b>」，目前最大的防禦缺口是 <b>{weakest}</b>。</p>
      <hr style='border-color:#cbd5e1;margin:14px 0;'>
      <h4>【國泰新泰度建議】</h4>
      <p>建議優先補強 <span style='background:#bbf7d0;padding:2px 8px;border-radius:6px;font-weight:900;color:#166534;'>{rec_name}</span>，讓未來遇到疾病、退休、照護或財務波動時，身、心、財不會一次被打穿。</p>
      <hr style='border-color:#cbd5e1;margin:14px 0;'>
      <h4>【What-If 平行宇宙推演】</h4>
      <p>💡 若在早期花費少量資源配置該保障，您的最終 {weakest} 將會是 <b style='color:#ea580c;font-size:18px;'>{what_if_score}</b> 分，而不是現在的危機狀態！數據證明，提早防禦能帶來極高的風險報酬率 (ROI)。</p>
    </div>
    """, unsafe_allow_html=True)

if st.session_state.page == "start":
    st.markdown("""
    <div class="hero"><div class="badge">Cathay Life OS 100</div><div class="title">Life 100<br>新泰度生存指南</div><div class="subtitle">你可以選擇進入人生模擬遊戲，或先查看 Life100 保險百科。<br>遊戲與百科分開，讓玩家更清楚知道自己正在「玩遊戲」還是「查資料」。</div><br><div><span class="badge">🎮 人生遊戲</span><span class="badge">📚 保險百科</span><span class="badge">🧭 遊戲說明</span><span class="badge">🤖 AI 復盤</span></div></div>
    """, unsafe_allow_html=True)
    c1,c2,c3=st.columns(3)
    with c1:
        st.markdown("<div class='rpg-card'><h2>🎮 人生遊戲模式</h2><p>從25歲開始，面對疾病、投資、長照、退休與家庭風險，挑戰活到100歲。</p><p><b>流程：</b>測驗 → 前進5年 → 人生規劃室 → 百歲結算</p></div>", unsafe_allow_html=True)
        if st.button("🚀 開始人生遊戲", use_container_width=True): goto("quiz")
    with c2:
        st.markdown("<div class='rpg-card'><h2>📚 Life100 保險百科</h2><p>查看不同保險的用途、保障內容、適合族群、遊戲效果與國泰官方商品連結。</p></div>", unsafe_allow_html=True)
        if st.button("📖 查看保險百科", use_container_width=True): goto("insurance")
    with c3:
        st.markdown("<div class='rpg-card'><h2>🧭 遊戲說明</h2><p>第一次使用建議先看玩法。了解身、心、財三大數值與人生規劃室的作用。</p></div>", unsafe_allow_html=True)
        if st.button("🧭 查看遊戲說明", use_container_width=True): goto("guide")

elif st.session_state.page == "guide":
    top_nav()
    st.markdown('<div class="title">🧭 Life100 遊戲說明</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="glass-card"><h2>遊戲目標</h2><p>從25歲一路走到100歲，並讓三個核心數值都不要歸零：</p><span class="badge">💪 身 Health</span><span class="badge">🧠 心 Mind</span><span class="badge">💰 財 Wealth</span></div>
    <div class="glass-card"><h2>怎麼玩？</h2>
    <div class="guide-step">Step 1：完成4題百歲天賦測驗，生成初始人生面板。</div>
    <div class="guide-step">Step 2：點擊「前進5年」，觸發過勞、股災、重大疾病、長照等人生事件。</div>
    <div class="guide-step">Step 3：每10年會進入「人生規劃室」，可以配置國泰神盾。</div>
    <div class="guide-step">Step 4：保險會在未來事件中抵銷 Health、Mind 或 Wealth 的損失。</div>
    <div class="guide-step">Step 5：到100歲或數值歸零時，產出 AI 人生復盤報告。</div></div>

    <div class="glass-card"><h2>📊 扣分與加分標準</h2>
    <p class="small-text">每次前進 5 年會抽取一個人生事件。事件會同時影響 Health、Mind、Wealth，分數最低 0、最高 100。</p>
    <div class="guide-step"><b>一般負面事件：</b>約扣 3～16 分。例如過勞、退休焦慮、家庭責任增加。這類事件會慢慢消耗身心財，但通常不會一次擊倒玩家。</div>
    <div class="guide-step"><b>高衝擊事件：</b>約扣 10～24 分。例如重大疾病、癌症、長照、股市黑天鵝、親人離世。這類事件仍有明顯威脅，但已調低，不會連續兩三次就幾乎必輸。</div>
    <div class="guide-step"><b>正向事件：</b>約加 4～28 分。例如健康習慣回饋、資產配置成功、職涯升級。正向事件可以幫助玩家把數值拉回安全區。</div>
    <div class="guide-step"><b>保險防禦：</b>若已配置對應保障，事件發生時會額外補回 Health、Mind 或 Wealth。例如醫療險可降低住院/手術造成的 Wealth 損失，重大傷病/癌症保障可降低重症事件衝擊。</div>
    <div class="guide-step"><b>小樹點：</b>事件後 Health 若維持 75 以上，獲得小樹點 +2；若有 FitBack 健康吧且 Health 仍在 70 以上，額外 +1。小樹點可在商城折抵保障成本。</div>
    </div>

    <div class="glass-card"><h2>🧮 目前事件分數範例</h2>
    <span class="badge">過勞危機：Health -12、Mind -12、Wealth -3</span>
    <span class="badge">股市黑天鵝：Health -2、Mind -8、Wealth -20</span>
    <span class="badge">重大疾病：Health -20、Mind -8、Wealth -18</span>
    <span class="badge">癌症治療：Health -24、Mind -12、Wealth -22</span>
    <span class="badge">長照需求：Health -24、Mind -12、Wealth -24</span>
    <span class="badge">親人離世：Health -3、Mind -26、Wealth -3</span>
    <span class="badge">健康習慣：Health +16、Mind +12、Wealth +8</span>
    <span class="badge">資產配置成功：Health +4、Mind +8、Wealth +26</span>
    <span class="badge">職涯升級：Health -3、Mind -5、Wealth +28</span>
    </div>

    <div class="glass-card"><h2>保險百科與遊戲的關係</h2><p>百科是查資料用；遊戲是做決策用。你可以先看百科理解每項保障，再回到遊戲中配置。</p></div>
    """, unsafe_allow_html=True)
    if st.button("🚀 我懂了，開始遊戲", use_container_width=True): goto("quiz")

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
    st.markdown('<div class="glass-card"><h3>🎯 目前任務</h3><p>點擊 <b>「前進 5 年」</b> 讓人生繼續推進。每 10 年會進入 <b>人生規劃室</b>，你可以配置保險神盾，降低未來事件造成的損失。</p></div>', unsafe_allow_html=True)
    if st.session_state.defense_notice:
        st.info(st.session_state.defense_notice)
        st.session_state.defense_notice = ""
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
        event, h, m, w, tree_gain, effect_logs, defense = next_event(st.session_state.age, st.session_state.health, st.session_state.mind, st.session_state.wealth, st.session_state.game_items)
        st.session_state.health=h; st.session_state.mind=m; st.session_state.wealth=w; st.session_state.tree += tree_gain
        
        st.session_state.history["age"].append(st.session_state.age)
        st.session_state.history["health"].append(h)
        st.session_state.history["mind"].append(m)
        st.session_state.history["wealth"].append(w)
        
        st.session_state.last_event=event["name"]; st.session_state.last_event_tag=event["tag"]
        add_log(f"{st.session_state.age}歲：{event['name']}")
        for e in effect_logs: add_log(e)
        if defense:
            st.session_state.defense_notice = defense
            add_log(defense)
        elif event.get('severity','') == 'high':
            st.session_state.defense_notice = f"🚨 缺乏防護網！「{event['name'].split('：')[0]}」造成嚴重打擊。"
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
    
    beat_percent = clamp(int((st.session_state.health + st.session_state.mind + st.session_state.wealth) / 300 * 100) + random.randint(5, 15))
    st.markdown(f"""
    <div class="glass-card" style="text-align: center;">
        <h3 style="color:#cbd5e1; margin-bottom: 5px;">🏆 全國同齡人存活榜</h3>
        <div style="font-size: 22px;">您的百歲決策，成功擊敗了 <span style="font-size: 38px; color: #facc15; font-weight: 900;">{beat_percent}%</span> 的同世代玩家！</div>
    </div>
    """, unsafe_allow_html=True)

    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.markdown('<div class="glass-card"><h2>📡 最終狀態雷達</h2>', unsafe_allow_html=True)
        risk_chart()
        st.markdown('</div>', unsafe_allow_html=True)
    with col_chart2:
        st.markdown('<div class="glass-card"><h2>📈 百歲人生軌跡走勢</h2>', unsafe_allow_html=True)
        hist = st.session_state.history
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(x=hist["age"], y=hist["health"], mode='lines+markers', name='身 Health', line=dict(color='#22c55e', width=3)))
        fig_line.add_trace(go.Scatter(x=hist["age"], y=hist["mind"], mode='lines+markers', name='心 Mind', line=dict(color='#3b82f6', width=3)))
        fig_line.add_trace(go.Scatter(x=hist["age"], y=hist["wealth"], mode='lines+markers', name='財 Wealth', line=dict(color='#facc15', width=3)))
        fig_line.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#f8fafc"), xaxis=dict(title="年齡 (歲)", gridcolor="rgba(255,255,255,.1)"), yaxis=dict(title="數值", range=[0, 105], gridcolor="rgba(255,255,255,.1)"), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1), height=430, margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig_line, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    recs=recommend_products(st.session_state.health, st.session_state.mind, st.session_state.wealth, st.session_state.last_event_tag, st.session_state.game_items, limit=3)
    score = protection_score(st.session_state.game_items, st.session_state.health, st.session_state.mind, st.session_state.wealth)
    st.markdown(f"""<div class='protection-score'><div style='color:#cbd5e1;font-size:18px;'>你的國泰神盾防護力</div><span>{score}</span> / 100</div>""", unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card"><h2>🔍 你的主要風險痛點</h2>', unsafe_allow_html=True)
    st.write(f"你的最大弱點是：**{weakest}**")
    st.write("建議補強：" + "、".join([p['game_item'] for _,p,_ in recs]))
    insights = analyze_life_risk(st.session_state.health, st.session_state.mind, st.session_state.wealth, st.session_state.age, st.session_state.game_items)
    for msg in insights:
        st.markdown(f"<div class='event-card'>🤖 {msg}</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card"><h2>🤖 AI 專屬人生復盤</h2><p class="small-text">讓 AI 分析你這段人生的決策軌跡，找出潛在盲點與轉機。</p>', unsafe_allow_html=True)
    if st.button("✨ 啟動 AI 深度復盤分析", type="primary", use_container_width=True):
        render_ai_review(weakest, recs, scores)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card"><h2>📣 下一步：將戰略化為現實</h2><p class="small-text">這裡可作為 Demo 的名單收集與專屬規劃入口。</p></div>', unsafe_allow_html=True)
    with st.expander("🙋 聯絡專屬規劃師（Demo 表單）"):
        st.info("🛡️ Demo 隱私提示：此區塊僅示範安全對接流程，未實際送出個資。")
        with st.form("lead_gen_form"):
            st.text_input("您的稱呼", placeholder="例如：王同學")
            st.text_input("聯絡信箱或手機", placeholder="Demo 可留空")
            if st.form_submit_button("🔒 送出我的專屬防護需求", use_container_width=True):
                st.success("✅ Demo 已送出！")
    st.markdown('<div class="glass-card"><h2>📜 人生回顧</h2>', unsafe_allow_html=True)
    for log in st.session_state.logs: st.markdown(f'<div class="event-card">{log}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("🔄 重新開始", use_container_width=True): reset_game()
