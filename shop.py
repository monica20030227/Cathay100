# shop.py
import streamlit as st
from insurance_db import INSURANCE_LIBRARY
from recommendation import recommend_products
from insurance_page import render_product_card

def render_shop():
    st.markdown('<div class="title">🛡️ 國泰神盾商城</div>', unsafe_allow_html=True)
    st.write("每 10 年決策點，你可以配置一項保障。原本商城功能保留，卡片加入更完整的保險介紹與官方連結。")

    m1, m2, m3 = st.columns(3)
    m1.metric("目前年齡", f"{st.session_state.age}歲")
    m2.metric("目前財富", st.session_state.wealth)
    m3.metric("小樹點", st.session_state.tree)

    last_tag = st.session_state.last_event_tag
    recs = recommend_products(st.session_state.health, st.session_state.mind, st.session_state.wealth, last_tag, st.session_state.game_items, limit=3)
    st.markdown('<div class="glass-card"><h3>🤖 AI推薦保障</h3><p class="small-text">依照你目前的身、心、財與最近事件推薦。</p></div>', unsafe_allow_html=True)
    rec_cols = st.columns(3)
    for i, (_, p, reason) in enumerate(recs):
        with rec_cols[i]:
            st.markdown(f"""
            <div class="rpg-card">
              <h3>{p['icon']} {p['game_item']}</h3>
              <div class="badge">{p['type']}</div>
              <p class="small-text">{reason}</p>
              <div class="effect-box">{p['game_effect']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"配置推薦 {p['game_item']}", key=f"rec_{p['id']}", use_container_width=True):
                add_product(p)

    st.divider()
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
