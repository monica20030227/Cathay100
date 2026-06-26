# shop.py
import streamlit as st
from insurance_db import INSURANCE_LIBRARY
from recommendation import (
    recommend_products_detailed,
    coverage_scores,
    product_scenario_preview,
    strongest_risk,
    status_level,
)
from insurance_page import render_product_card


def add_product(p):
    cost = p["cost"]
    used_tree = min(st.session_state.get("tree", 0), cost)
    final_cost = max(0, cost - used_tree)
    if p["game_item"] in st.session_state.game_items:
        st.warning("你已經配置過這項保障。")
    elif st.session_state.wealth >= final_cost:
        st.session_state.tree -= used_tree
        st.session_state.wealth -= final_cost
        st.session_state.game_items.append(p["game_item"])
        st.session_state.logs.append(
            f"{st.session_state.age}歲：配置保障「{p['game_item']}」，花費Wealth {final_cost}，使用小樹點 {used_tree}。"
        )
        st.success("配置成功！")
        st.rerun()
    else:
        st.error("Wealth不足，暫時無法配置。")


def render_coverage_dashboard():
    scores = coverage_scores(st.session_state.game_items)
    st.markdown(
        '<div class="glass-card"><h3>📊 保障覆蓋率</h3><p class="small-text">根據目前已配置的實際商品類型，推估你的保障缺口。</p></div>',
        unsafe_allow_html=True,
    )
    cols = st.columns(4)
    for i, (label, value) in enumerate(scores.items()):
        with cols[i]:
            st.metric(label, f"{value}%")
            st.progress(value / 100)


def render_ai_advisor():
    last_tag = st.session_state.get("last_event_tag")
    weakest = strongest_risk(st.session_state.health, st.session_state.mind, st.session_state.wealth)
    last_event = st.session_state.get("last_event", "尚未發生事件")
    st.markdown(
        f'''
        <div class="glass-card">
          <h2>🤖 AI 人生保障分析</h2>
          <p class="small-text">AI 依照你的年齡、Health / Mind / Wealth、最近事件、已配置保障與人生目標，從下方實際商品資料庫中推薦本回合保障。</p>
          <span class="badge">目前主要風險：{weakest}</span>
          <span class="badge">最近事件：{last_event}</span>
          <span class="badge">人生目標：{st.session_state.get('goal', '尚未設定')}</span><br>
          <span class="badge">Health {st.session_state.health}｜{status_level(st.session_state.health)}</span>
          <span class="badge">Mind {st.session_state.mind}｜{status_level(st.session_state.mind)}</span>
          <span class="badge">Wealth {st.session_state.wealth}｜{status_level(st.session_state.wealth)}</span>
        </div>
        ''',
        unsafe_allow_html=True,
    )

    render_coverage_dashboard()

    recs = recommend_products_detailed(
        st.session_state.health,
        st.session_state.mind,
        st.session_state.wealth,
        age=st.session_state.age,
        last_event_tag=last_tag,
        owned=st.session_state.game_items,
        limit=3,
        goal=st.session_state.get("goal", ""),
    )
    st.markdown(
        '<div class="glass-card"><h3>🎯 Top 3 推薦保障</h3><p class="small-text">每張卡片保留實際商品名稱，並顯示推薦分數、推薦理由與「未投保 vs 投保後」情境比較。</p></div>',
        unsafe_allow_html=True,
    )

    cols = st.columns(3)
    medals = ["🥇 第一推薦", "🥈 第二推薦", "🥉 第三推薦"]
    for i, row in enumerate(recs):
        p = row["product"]
        event_name, without_vals, with_vals = product_scenario_preview(
            p,
            st.session_state.health,
            st.session_state.mind,
            st.session_state.wealth,
            last_tag,
        )
        reason_html = "".join([f'<p class="small-text">✓ {r}</p>' for r in row["reasons"]])
        with cols[i]:
            st.markdown(
                f'''
                <div class="rpg-card">
                  <div class="badge">{medals[i]}</div>
                  <h3>{p['icon']} {p['game_item']}</h3>
                  <div class="badge">推薦度 {row['score']}%</div>
                  <div class="badge">{p['type']}</div>
                  {reason_html}
                  <div class="effect-box">{p['game_effect']}</div>
                </div>
                ''',
                unsafe_allow_html=True,
            )
            st.progress(row["score"] / 100)
            st.markdown(f"**情境比較：{event_name}**")
            c1, c2 = st.columns(2)
            with c1:
                st.caption("未投保後")
                st.write(f"Health {without_vals[0]}")
                st.write(f"Mind {without_vals[1]}")
                st.write(f"Wealth {without_vals[2]}")
            with c2:
                st.caption("投保後")
                st.write(f"Health {with_vals[0]}")
                st.write(f"Mind {with_vals[1]}")
                st.write(f"Wealth {with_vals[2]}")
            if st.button(f"配置推薦：{p['game_item']}", key=f"rec_{p['id']}", use_container_width=True):
                add_product(p)


def render_shop():
    st.markdown('<div class="title">🛡️ 人生規劃室</div>', unsafe_allow_html=True)
    st.write("每 10 年決策點，你可以配置保障。原本商城、分類、商品卡片全部保留，這裡只額外加入 AI 人生保障分析。")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("目前年齡", f"{st.session_state.age}歲")
    m2.metric("目前財富", st.session_state.wealth)
    m3.metric("小樹點", st.session_state.tree)
    m4.metric("已配置保障", len(st.session_state.game_items))

    render_ai_advisor()

    st.divider()
    st.markdown(
        '<div class="glass-card"><h3>🛒 所有保障商品</h3><p class="small-text">AI推薦只是輔助，下面保留完整商品庫，玩家仍可自由選擇。</p></div>',
        unsafe_allow_html=True,
    )
    categories = ["全部"] + list(dict.fromkeys([p["category"] for p in INSURANCE_LIBRARY]))
    category = st.selectbox("商城分類", categories)
    products = INSURANCE_LIBRARY if category == "全部" else [p for p in INSURANCE_LIBRARY if p["category"] == category]

    cols = st.columns(2)
    for idx, p in enumerate(products):
        with cols[idx % 2]:
            render_product_card(p, allow_add=True, key_prefix=f"shop_{idx}")

    st.divider()
    if st.button("返回人生輪轉", use_container_width=True):
        st.session_state.page = "game"
        st.rerun()
