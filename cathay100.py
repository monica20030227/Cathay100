# app.py
import streamlit as st
import random
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Life 100：新泰度生存指南", layout="wide")

# =====================
# 初始化
# =====================
if "page" not in st.session_state:
    st.session_state.page = "start"
    st.session_state.age = 25
    st.session_state.health = 80
    st.session_state.mind = 80
    st.session_state.wealth = 80
    st.session_state.tree = 0
    st.session_state.items = []
    st.session_state.logs = []

# =====================
# 工具函式
# =====================
def bar(label, value):
    st.progress(value / 100)
    st.write(f"{label}：{value}/100")

def clamp(x):
    return max(0, min(100, int(x)))

def add_log(text):
    st.session_state.logs.append(text)

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
        name="風險熱力圖"
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
        height=420
    )
    st.plotly_chart(fig, use_container_width=True)

# =====================
# 首頁
# =====================
if st.session_state.page == "start":
    st.title("🌳 Life 100：新泰度生存指南")
    st.subheader("你的百歲人生，能撐到最後嗎？")

    st.write("""
    這是一款 AI 人生決策模擬遊戲。
    你需要在 25 歲到 100 歲之間，維持「身、心、財」三大數值不歸零。
    """)

    if st.button("開始百歲天賦測驗"):
        st.session_state.page = "quiz"
        st.rerun()

# =====================
# 測驗頁
# =====================
elif st.session_state.page == "quiz":
    st.title("🧬 百歲天賦測驗")

    income = st.selectbox("1. 你的收入與理財狀態？", [
        "月光族", "有固定儲蓄", "積極投資", "財務規劃完整"
    ])

    goal = st.selectbox("2. 你最想達成的人生目標？", [
        "買房", "財富自由", "健康退休", "照顧家人"
    ])

    lifestyle = st.selectbox("3. 你嚮往的生活方式？", [
        "高壓拚事業", "自由斜槓", "穩定生活", "享樂優先"
    ])

    health = st.selectbox("4. 你的健康作息？", [
        "常熬夜少運動", "偶爾運動", "規律運動", "飲食睡眠都穩定"
    ])

    if st.button("生成我的人生面板"):
        if income == "月光族":
            st.session_state.wealth = 55
        elif income == "有固定儲蓄":
            st.session_state.wealth = 70
        elif income == "積極投資":
            st.session_state.wealth = 75
        else:
            st.session_state.wealth = 85

        if lifestyle == "高壓拚事業":
            st.session_state.mind = 60
        elif lifestyle == "享樂優先":
            st.session_state.mind = 75
            st.session_state.wealth -= 10
        else:
            st.session_state.mind = 80

        if health == "常熬夜少運動":
            st.session_state.health = 55
        elif health == "偶爾運動":
            st.session_state.health = 70
        elif health == "規律運動":
            st.session_state.health = 85
        else:
            st.session_state.health = 90

        add_log(f"你選擇的人生目標是：{goal}")
        st.session_state.page = "game"
        st.rerun()

# =====================
# 遊戲主頁
# =====================
elif st.session_state.page == "game":
    st.title("🎮 Life 100：人生輪轉中")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("年齡", f"{st.session_state.age} 歲")
    col2.metric("小樹點", st.session_state.tree)
    col3.metric("已配置道具", len(st.session_state.items))
    col4.metric("目前狀態", "存活中")

    st.divider()

    c1, c2 = st.columns([1, 1])

    with c1:
        bar("💪 身 Health", st.session_state.health)
        bar("🧠 心 Mind", st.session_state.mind)
        bar("💰 財 Wealth", st.session_state.wealth)

        st.subheader("📜 人生事件紀錄")
        for log in st.session_state.logs[-6:]:
            st.write("・" + log)

    with c2:
        st.subheader("📡 3D 人生風險雷達")
        risk_chart()

    st.divider()

    if st.button("前進 5 年"):
        st.session_state.age += 5

        event_pool = [
            ("35歲過勞危機", -18, -15, -5),
            ("45歲股市崩盤", -5, -10, -25),
            ("55歲重大疾病風險", -25, -10, -20),
            ("65歲退休壓力", -10, -20, -15),
            ("75歲長照需求出現", -30, -15, -30),
            ("親人離世造成心理衝擊", -5, -35, -5),
            ("健康習慣帶來正向回饋", 10, 5, 5),
            ("投資配置成功增值", 0, 5, 20),
        ]

        event = random.choice(event_pool)
        name, dh, dm, dw = event

        # 道具效果
        if "FitBack 健康吧" in st.session_state.items:
            dh += 8
        if "國泰長照險 / 失智險" in st.session_state.items and st.session_state.age >= 70:
            dh += 20
            dw += 25
        if "CVX 泰好保 & 理賠聯盟鏈" in st.session_state.items:
            dm += 8
        if "心理關懷服務" in st.session_state.items and dm < -20:
            dm += 25
        if "外溢型重大傷病險" in st.session_state.items and dh < -20:
            dw += 25
        if "國泰智能投資" in st.session_state.items and dw < -20:
            dw += 20

        st.session_state.health = clamp(st.session_state.health + dh)
        st.session_state.mind = clamp(st.session_state.mind + dm)
        st.session_state.wealth = clamp(st.session_state.wealth + dw)

        if st.session_state.health >= 75:
            st.session_state.tree += 2

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

# =====================
# 商城
# =====================
elif st.session_state.page == "shop":
    st.title("🛡️ 國泰神盾商城")
    st.write("每 10 年可以配置一次防禦道具。")

    products = {
        "FitBack 健康吧": 10,
        "國泰長照險 / 失智險": 20,
        "CVX 泰好保 & 理賠聯盟鏈": 12,
        "心理關懷服務": 15,
        "外溢型重大傷病險": 20,
        "國泰智能投資": 18,
    }

    choice = st.selectbox("選擇要配置的道具", list(products.keys()))
    cost = products[choice]

    st.write(f"需要財富成本：{cost}")

    if st.button("購買 / 配置"):
        if st.session_state.wealth >= cost:
            st.session_state.wealth -= cost
            if choice not in st.session_state.items:
                st.session_state.items.append(choice)
            add_log(f"配置國泰神盾：{choice}")
            st.success("配置成功！")
        else:
            st.error("財富不足，無法配置。")

    if st.button("回到人生輪轉"):
        st.session_state.page = "game"
        st.rerun()

# =====================
# 結算頁
# =====================
elif st.session_state.page == "result":
    st.title("🏁 百歲人生結算報告")

    st.metric("最終年齡", f"{st.session_state.age} 歲")
    st.write(f"💪 身：{st.session_state.health}")
    st.write(f"🧠 心：{st.session_state.mind}")
    st.write(f"💰 財：{st.session_state.wealth}")

    if st.session_state.age >= 100:
        st.success("恭喜你成功活到 100 歲！")
    else:
        st.error("人生挑戰失敗，有一項核心數值歸零。")

    weakest = min(
        {
            "健康風險": st.session_state.health,
            "心理壓力": st.session_state.mind,
            "財務風險": st.session_state.wealth,
        },
        key={
            "健康風險": st.session_state.health,
            "心理壓力": st.session_state.mind,
            "財務風險": st.session_state.wealth,
        }.get
    )

    st.subheader("你的主要風險痛點")
    st.write(f"你的最大弱點是：**{weakest}**")

    st.subheader("專屬攻略建議")
    if weakest == "健康風險":
        st.write("建議優先配置 FitBack 健康吧、長照險或重大傷病險。")
    elif weakest == "心理壓力":
        st.write("建議優先配置心理關懷服務與 CVX 泰好保。")
    else:
        st.write("建議優先配置國泰智能投資與外溢型重大傷病險。")

    if st.button("重新開始"):
        st.session_state.clear()
        st.rerun()