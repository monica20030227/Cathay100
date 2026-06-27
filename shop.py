# shop.py
import streamlit as st
from insurance_db import INSURANCE_LIBRARY
from recommendation import recommend_products
from insurance_page import render_product_card

def render_shop():
    st.markdown('<div class="title">🛡️ 人生規劃室</div>', unsafe_allow_html=True)
    st.markdown('<div class="glass-card"><h3>Step 3：選擇保障</h3><p class="small-text">這裡是每 10 年一次的人生決策點。請根據目前的身、心、財狀態，選擇適合的保障。小樹點會自動折抵配置成本。</p></div>', unsafe_allow_html=True)

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
              <div class="effect-box">{p['game_effect']}</div><p class='small-text'>原成本 {p['cost']}｜折抵後 {max(0, p['cost'] - st.session_state.tree)}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"配置推薦 {p['game_item']}", key=f"rec_{p['id']}", use_container_width=True):
                add_product(p)

    st.divider()
    categories = ["全部"] + sorted(set(p['category'] for p in INSURANCE_LIBRARY))
    category = st.selectbox("商城分類", categories)
    products = INSURANCE_LIBRARY if category == "全部" else [p for p in INSURANCE_LIBRARY if p['category'] == category]

    cols = st.columns(3)
    for idx, p in enumerate(products):
        with cols[idx % 3]:
            render_product_card(p, allow_add=True, key_prefix=f"shop_{idx}")

    st.divider()
    if st.button("返回人生輪轉", use_container_width=True):
        st.session_state.page = "game"
        st.rerun()

def add_product(p):
    if p['game_item'] in st.session_state.game_items:
        st.warning("你已經配置過這項保障。")
    elif st.session_state.wealth >= max(0, p['cost'] - st.session_state.get('tree', 0)):
        used_tree = min(st.session_state.get('tree', 0), p['cost'])
        final_cost = max(0, p['cost'] - used_tree)
        st.session_state.tree -= used_tree
        st.session_state.wealth -= final_cost
        st.session_state.game_items.append(p['game_item'])
        st.session_state.logs.append(f"{st.session_state.age}歲：配置保障「{p['game_item']}」，花費財富 {final_cost}，使用小樹點 {used_tree}。")
        st.success("配置成功！")
    else:
        st.error("財富不足，無法配置。")
