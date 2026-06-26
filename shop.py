# shop.py
import streamlit as st
from insurance_db import INSURANCE_LIBRARY
from recommendation import (
    recommend_products,
    recommend_products_detailed,
    coverage_scores,
    product_scenario_preview,
    strongest_risk,
    status_level,
)
from insurance_page import render_product_card


def render_coverage_dashboard():
    scores = coverage_scores(st.session_state.game_items)
    st.markdown('<div class="glass-card"><h3>📊 保障覆蓋率</h3><p class="small-text">根據目前已配置商品，推估你的保障缺口。</p></div>', unsafe_allow_html=True)
    cols = st.columns(4)
    for i, (label, value) in enumerate(scores.items()):
        with cols[i]:
            st.metric(label, f"{value}%")
            st.progress(value / 100)


def render_ai_advisor():
    last_tag = st.session_state.get("last_event_tag", None)
    weakest = strongest_risk(st.session_state.health, st.session_state.mind, st.session_state.wealth)
    st.markdown(f'''
    <div class="glass-card">
      <h2>🤖 AI 人生保障分析</h2>
      <p class="small-text">目前你的主要風險是 <b>{weakest}</b>。AI會依照年齡、Health/Mind/Wealth、最近事件與已配置保障，推薦本回合更適合的保險。</p>
      <span class="badge">Health：{st.session_state.health}｜{status_level(st.session_state.health)}</span>
      <span class="badge">Mind：{st.session_state.mind}｜{status_level(st.session_state.mind)}</span>
      <span class="badge">Wealth：{st.session_state.wealth}｜{status_level(st.session_state.wealth)}</span>
    </div>
    ''', unsafe_allow_html=True)
    render_coverage_dashboard()

    recs = recommend_products_detailed(
        st.session_state.health,
        st.session_state.mind,
        st.session_state.wealth,
        age=st.session_state.age,
        last_event_tag=last_tag,
        owned=st.session_state.game_items,
        limit=3,
    )
    st.markdown('<div class="glass-card"><h3>🎯 Top 3 推薦保障</h3><p class="small-text">加入推薦分數、推薦理由，以及「未投保 vs 投保後」的遊戲數值差異。</p></div>', unsafe_allow_html=True)
    cols = st.columns(3)
    medals = ["🥇 第一推薦", "🥈 第二推薦", "🥉 第三推薦"]
    for i, row in enumerate(recs):
        p = row["product"]
        score = row["score"]
        reasons = row["reasons"]
        event_name, without_vals, with_vals = product_scenario_preview(
            p,
            st.session_state.health,
            st.session_state.mind,
            st.session_state.wealth,
            last_tag,
        )
        reason_html = "".join([f'<p class="small-text">✓ {r}</p>' for r in reasons])
        with cols[i]:
            st.markdown(f'''
            <div class="rpg-card">
              <div class="badge">{medals[i]}</div>
              <h3>{p['icon']} {p['game_item']}</h3>
              <div class="badge">推薦度 {score}%</div>
              <div class="badge">{p['type']}</div>
              {reason_html}
              <div class="effect-box">{p['game_effect']}</div>
            </div>
            ''', unsafe_allow_html=True)
            st.progress(score / 100)
            st.markdown(f"**情境比較：{event_name}**")
            compare_cols = st.columns(2)
            with compare_cols[0]:
                st.caption("未投保後")
                st.write(f"Health {without_vals[0]}")
                st.write(f"Mind {without_vals[1]}")
                st.write(f"Wealth {without_vals[2]}")
            with compare_cols[1]:
                st.caption("投保後")
                st.write(f"Health {with_vals[0]}")
                st.write(f"Mind {with_vals[1]}")
                st.write(f"Wealth {with_vals[2]}")
            if st.button(f"配置推薦 {p['game_item']}", key=f"rec_{p['id']}", use_container_width=True):
                add_product(p)


def render_shop():
    st.markdown('<div class="title">🛡️ 國泰神盾商城</div>', unsafe_allow_html=True)
    st.write("每 10 年決策點，你可以配置一項保障。原本商城功能保留，並加入 AI 人生保障分析。")

    m1, m2, m3 = st.columns(3)
    m1.metric("目前年齡", f"{st.session_state.age}歲")
    m2.metric("目前財富", st.session_state.wealth)
    m3.metric("小樹點", st.session_state.tree)

    render_ai_advisor()

    st.divider()
    st.markdown('<div class="glass-card"><h3>🛒 所有保障商品</h3><p class="small-text">AI 推薦是輔助，這裡保留原本完整商城與分類瀏覽功能。</p></div>', unsafe_allow_html=True)
    categories = ["全部"] + sorted(set(p['category'] for p in INSURANCE_LIBRARY))
    category = st.selectbox("商城分類", categories)
    products = INSURANCE_LIBRARY if category == "全部" else [p for p in INSURANCE_LIBRARY if p['category'] == category]

    cols = st.columns(2)
    for idx, p in enumerate(products):
        with cols[idx % 2]:
            render_product_card(p, allow_add=True, key_prefix=f"shop_{idx}")

    st.divider()
    if st.button("返回人生輪轉", use_container_width=True):
        st.session_state.page = "game"
        st.rerun()


def add_product(p):
    if p['game_item'] in st.session_state.game_items:
        st.warning("你已經配置過這項保障。")
    elif st.session_state.wealth >= p['cost']:
        st.session_state.wealth -= p['cost']
        st.session_state.game_items.append(p['game_item'])
        st.session_state.logs.append(f"{st.session_state.age}歲：配置保障「{p['game_item']}」。")
        st.success("配置成功！")
    else:
        st.error("財富不足，無法配置。")
