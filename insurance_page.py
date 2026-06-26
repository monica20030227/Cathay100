# insurance_page.py
import streamlit as st
from insurance_db import INSURANCE_LIBRARY, CATEGORY_DESCRIPTIONS, get_products_by_category
from recommendation import product_scenario_preview, score_product


def add_product_from_card(p):
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
        st.success("已加入人生保障！")
        st.rerun()
    else:
        st.error("Wealth不足，暫時無法配置。")


def render_product_card(p, allow_add=True, key_prefix="wiki", show_ai_preview=True):
    final_cost = max(0, p["cost"] - st.session_state.get("tree", 0))
    st.markdown(f"""
    <div class="product-card">
      <div class="badge">{p['icon']} {p['category']}</div>
      <div class="product-title">{p['name']}</div>
      <div class="product-subtitle">{p['type']}｜成本 {p['cost']} Wealth｜折抵後 {final_cost} Wealth</div>
      <p class="small-text">{p['short']}</p>
      <div class="section-label">🛡️ 保障重點</div>
      <p class="small-text">{'、'.join(p['coverage'])}</p>
      <div class="section-label">🎯 適合族群</div>
      <p class="small-text">{'、'.join(p['suitable'])}</p>
      <div class="effect-box">🎮 Life100效果：{p['game_effect']}</div>
      <div class="section-label">📄 官方資料摘要</div>
      <p class="small-text">{p['source_note']}</p>
      <a href="{p['official_url']}" target="_blank">🔗 前往國泰官方商品頁</a>
    </div>
    """, unsafe_allow_html=True)

    if show_ai_preview and "health" in st.session_state:
        score, reasons = score_product(
            p,
            st.session_state.health,
            st.session_state.mind,
            st.session_state.wealth,
            age=st.session_state.age,
            last_event_tag=st.session_state.get("last_event_tag"),
            owned=st.session_state.game_items,
            goal=st.session_state.get("goal", ""),
        )
        event_name, without_vals, with_vals = product_scenario_preview(
            p,
            st.session_state.health,
            st.session_state.mind,
            st.session_state.wealth,
            st.session_state.get("last_event_tag"),
        )
        st.markdown(f"**AI適配度：{score}%｜情境：{event_name}**")
        st.progress(score / 100)
        st.caption("推薦理由：" + "、".join(reasons))
        c0, c1 = st.columns(2)
        with c0:
            st.caption(f"未配置：H{without_vals[0]} / M{without_vals[1]} / W{without_vals[2]}")
        with c1:
            st.caption(f"配置後：H{with_vals[0]} / M{with_vals[1]} / W{with_vals[2]}")

    c1, c2 = st.columns(2)
    with c1:
        if allow_add:
            if st.button(f"加入人生保障：{p['game_item']}", key=f"{key_prefix}_add_{p['id']}", use_container_width=True):
                add_product_from_card(p)
    with c2:
        st.link_button("查看官方頁面", p["official_url"], use_container_width=True)


def render_insurance_page():
    st.markdown('<div class="title">📚 Life100 保險百科</div>', unsafe_allow_html=True)
    st.write("依照人生風險分類，查看每一種實際保險商品在現實中的保障內容，以及在遊戲中的防禦效果。")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("← 回首頁", use_container_width=True):
            st.session_state.page = "start"
            st.rerun()
    with c2:
        if st.button("🎮 回到遊戲", use_container_width=True):
            st.session_state.page = "game"
            st.rerun()

    categories = list(CATEGORY_DESCRIPTIONS.keys())
    selected = st.selectbox("選擇保險分類", categories)
    st.markdown(f"""
    <div class="glass-card">
      <h2>{selected}</h2>
      <p class="small-text">{CATEGORY_DESCRIPTIONS[selected]}</p>
    </div>
    """, unsafe_allow_html=True)

    products = get_products_by_category(selected)
    query = st.text_input("搜尋商品/保障類型", placeholder="例如：實支實付、癌症、長照、年金")
    if query:
        products = [
            p for p in INSURANCE_LIBRARY
            if query in p["name"] or query in p["type"] or query in p["short"] or query in p["category"] or query in p["game_item"]
        ]

    cols = st.columns(2)
    for i, p in enumerate(products):
        with cols[i % 2]:
            render_product_card(p, allow_add=True, key_prefix=f"wiki_{i}")
