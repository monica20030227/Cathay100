# shop.py
import streamlit as st
from insurance_db import INSURANCE_LIBRARY
from recommendation import recommend_products


def _is_initial_mode():
    return st.session_state.get("shop_mode") == "initial" and not st.session_state.get("initial_planning_done", False)


def _display_cost(p):
    if _is_initial_mode():
        budget = st.session_state.get("initial_budget", 0)
        return p["cost"], max(0, budget - p["cost"]), "初始保障預算"
    used_tree = min(st.session_state.get("tree", 0), p["cost"])
    return p["cost"], max(0, p["cost"] - used_tree), "Wealth"


def render_shop_product_card(p, key_prefix="shop"):
    original_cost, final_cost, pay_source = _display_cost(p)
    if _is_initial_mode():
        cost_text = f"成本 {original_cost}｜配置後預算剩 {final_cost}"
    else:
        cost_text = f"原成本 {original_cost}｜小樹點折抵後 {final_cost} Wealth"

    st.markdown(f"""
    <div class="product-card">
      <div class="badge">{p['icon']} {p['category']}</div>
      <div class="product-title">{p['game_item']}</div>
      <div class="product-subtitle">{p['type']}｜{cost_text}</div>
      <p class="small-text">{p['short']}</p>
      <div class="section-label">🎮 Life100 效果</div>
      <div class="effect-box">{p['game_effect']}</div>
      <div class="section-label">🎯 適合族群</div>
      <p class="small-text">{'、'.join(p['suitable'])}</p>
      <a href="{p['official_url']}" target="_blank">🔗 查看官方商品頁</a>
    </div>
    """, unsafe_allow_html=True)

    button_label = f"配置 {p['game_item']}"
    if st.button(button_label, key=f"{key_prefix}_add_{p['id']}", use_container_width=True):
        add_product(p)


def render_shop():
    initial_mode = _is_initial_mode()

    if initial_mode:
        st.markdown('<div class="title">🛡️ 初始人生規劃</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="glass-card">
          <h3>Step 2：先建立第一道保障</h3>
          <p class="small-text">
          在人生轉盤開始前，你可以先用 <b>30 點初始保障預算</b> 配置保險。
          這筆預算只限第一次使用，不會扣你的 Wealth。AI 會先推薦適合你的保障，
          但你也可以在下方自由選擇所有商品。
          </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="title">🛡️ 人生規劃室</div>', unsafe_allow_html=True)
        st.markdown('<div class="glass-card"><h3>Step 3：選擇保障</h3><p class="small-text">這裡是每 10 年一次的人生決策點。請根據目前的身、心、財狀態，選擇適合的保障。小樹點會自動折抵配置成本。</p></div>', unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("目前年齡", f"{st.session_state.age}歲")
    m2.metric("目前財富", st.session_state.wealth)
    m3.metric("小樹點", st.session_state.tree)
    if initial_mode:
        m4.metric("初始保障預算", st.session_state.get("initial_budget", 0))
    else:
        m4.metric("已配置保障", len(st.session_state.game_items))

    last_tag = st.session_state.last_event_tag
    recs = recommend_products(
        st.session_state.health,
        st.session_state.mind,
        st.session_state.wealth,
        last_tag,
        st.session_state.game_items,
        limit=3,
    )

    if initial_mode:
        rec_title = "🤖 AI 初始推薦保障"
        rec_desc = "依照你的百歲天賦測驗結果，先推薦適合開局配置的保障。"
    else:
        rec_title = "🤖 AI 推薦保障"
        rec_desc = "依照你目前的身、心、財與最近事件推薦。"

    st.markdown(f'<div class="glass-card"><h3>{rec_title}</h3><p class="small-text">{rec_desc}</p></div>', unsafe_allow_html=True)
    rec_cols = st.columns(3)
    for i, (_, p, reason) in enumerate(recs):
        with rec_cols[i]:
            original_cost, final_cost, pay_source = _display_cost(p)
            if initial_mode:
                cost_line = f"成本 {original_cost}｜配置後預算剩 {final_cost}"
            else:
                cost_line = f"原成本 {original_cost}｜折抵後 {final_cost}"
            st.markdown(f"""
            <div class="rpg-card">
              <h3>{p['icon']} {p['game_item']}</h3>
              <div class="badge">{p['type']}</div>
              <p class="small-text">{reason}</p>
              <div class="effect-box">{p['game_effect']}</div>
              <p class="small-text">{cost_line}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"配置推薦 {p['game_item']}", key=f"rec_{p['id']}", use_container_width=True):
                add_product(p)

    st.divider()

    if st.session_state.game_items:
        st.markdown('<div class="glass-card"><h3>🎒 目前已配置保障</h3>', unsafe_allow_html=True)
        for item in st.session_state.game_items:
            st.markdown(f'<span class="badge">🛡️ {item}</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-card"><h3>🧭 自由選擇所有保障</h3><p class="small-text">除了 AI 推薦，你也可以依照自己的想法選擇其他保險商品。</p></div>', unsafe_allow_html=True)

    categories = ["全部"] + sorted(set(p["category"] for p in INSURANCE_LIBRARY))
    category = st.selectbox("保障分類", categories)
    products = INSURANCE_LIBRARY if category == "全部" else [p for p in INSURANCE_LIBRARY if p["category"] == category]

    cols = st.columns(3)
    for idx, p in enumerate(products):
        with cols[idx % 3]:
            render_shop_product_card(p, key_prefix=f"shop_{idx}")

    st.divider()

    if initial_mode:
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🎮 開始人生轉盤", use_container_width=True):
                st.session_state.initial_planning_done = True
                st.session_state.shop_mode = "normal"
                st.session_state.page = "game"
                st.rerun()
        with c2:
            if st.button("📚 先看保險百科", use_container_width=True):
                st.session_state.page = "insurance"
                st.rerun()
    else:
        if st.button("返回人生轉盤", use_container_width=True):
            st.session_state.page = "game"
            st.rerun()


def add_product(p):
    if p["game_item"] in st.session_state.game_items:
        st.warning("你已經配置過這項保障。")
        return

    if _is_initial_mode():
        budget = st.session_state.get("initial_budget", 0)
        cost = p["cost"]
        if budget >= cost:
            st.session_state.initial_budget = budget - cost
            st.session_state.game_items.append(p["game_item"])
            st.session_state.logs.append(
                f"{st.session_state.age}歲：使用初始保障預算配置「{p['game_item']}」，花費預算 {cost}，剩餘預算 {st.session_state.initial_budget}。"
            )
            st.success("配置成功！這次使用初始保障預算，不會扣 Wealth。")
        else:
            st.error("初始保障預算不足，請選擇成本較低的保障，或直接開始人生轉盤。")
        return

    used_tree = min(st.session_state.get("tree", 0), p["cost"])
    final_cost = max(0, p["cost"] - used_tree)

    if st.session_state.wealth >= final_cost:
        st.session_state.tree -= used_tree
        st.session_state.wealth -= final_cost
        st.session_state.game_items.append(p["game_item"])
        st.session_state.logs.append(
            f"{st.session_state.age}歲：配置保障「{p['game_item']}」，花費財富 {final_cost}，使用小樹點 {used_tree}。"
        )
        st.success("配置成功！")
    else:
        st.error("財富不足，無法配置。")
