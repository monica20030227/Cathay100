# recommendation.py
# AI 人生保障顧問：不更動 insurance_db.py 的商品內容，只根據資料庫欄位做推薦、覆蓋率與情境比較。
from insurance_db import INSURANCE_LIBRARY

TAG_TO_TYPES = {
    "critical": ["重大傷病險", "重大疾病險", "重大傷病定期保險"],
    "cancer": ["癌症險", "重大疾病險", "重大傷病險", "重大傷病定期保險"],
    "surgery": ["實支實付醫療險", "手術醫療險", "自負額實支實付", "意外傷害險"],
    "medical": ["實支實付醫療險", "手術醫療險", "自負額實支實付", "重大傷病險"],
    "longcare": ["長期照顧險"],
    "market": ["變額年金保險", "變額萬能壽險", "投資連結型保險"],
    "retirement": ["變額年金保險", "長期照顧險", "投資連結型保險"],
    "family": ["壽險", "變額萬能壽險", "重大傷病定期保險"],
    "accident": ["意外傷害險", "實支實付醫療險", "手術醫療險"],
    "stress": ["外溢健康計畫"],
    "income": ["變額萬能壽險", "變額年金保險", "投資連結型保險"],
}

TAG_TO_SCENARIO = {
    "critical": ("重大疾病風險", -28, -12, -25),
    "cancer": ("癌症治療挑戰", -32, -18, -32),
    "surgery": ("住院手術事件", -20, -10, -22),
    "medical": ("大型醫療事件", -24, -10, -24),
    "longcare": ("長照需求出現", -32, -18, -34),
    "market": ("股市黑天鵝", -3, -12, -28),
    "retirement": ("退休焦慮", -8, -22, -16),
    "family": ("家庭責任事件", -8, -16, -18),
    "accident": ("意外事故", -24, -10, -20),
    "stress": ("過勞危機", -18, -16, -5),
    "income": ("職涯與收入轉換", -5, -8, -10),
}

RISK_LABELS = {
    "health": "健康風險",
    "mind": "心理壓力",
    "wealth": "財務風險",
}


def clamp(x):
    return max(0, min(100, int(x)))


def status_level(value):
    if value < 45:
        return "高風險"
    if value < 65:
        return "需補強"
    if value < 80:
        return "普通"
    return "穩定"


def strongest_risk(health, mind, wealth):
    values = {"health": health, "mind": mind, "wealth": wealth}
    weakest_key = min(values, key=values.get)
    return RISK_LABELS[weakest_key]


def infer_tag_for_product(product):
    for tag, types in TAG_TO_TYPES.items():
        if product.get("type") in types:
            return tag
    effect = product.get("effect", {})
    if effect:
        return next(iter(effect.keys()))
    return "medical"


def score_product(p, health, mind, wealth, age=25, last_event_tag=None, owned=None, goal=""):
    owned = owned or []
    if p["game_item"] in owned:
        return 0, ["已配置，不重複推薦"]

    score = 35
    reasons = []
    category = p.get("category", "")
    ptype = p.get("type", "")

    if health < 60 and category in ["健康醫療", "重大疾病/傷病", "健康促進", "長照退休"]:
        score += 20
        reasons.append("Health偏低，優先補強健康與醫療防線")
    elif health < 75 and category in ["健康醫療", "重大疾病/傷病", "健康促進"]:
        score += 10
        reasons.append("Health尚未完全穩定，可降低未來疾病衝擊")

    if mind < 60 and category in ["健康促進", "人身保障", "長照退休"]:
        score += 14
        reasons.append("Mind偏低，需要降低家庭照護與突發事件壓力")
    elif mind < 75 and category in ["健康促進", "人身保障"]:
        score += 7
        reasons.append("Mind普通，適合增加心理韌性與安全感")

    if wealth < 60 and category in ["健康醫療", "重大疾病/傷病", "退休理財", "人身保障", "長照退休"]:
        score += 22
        reasons.append("Wealth偏低，需要把高額支出風險轉嫁出去")
    elif wealth < 75 and category in ["退休理財", "人身保障", "重大疾病/傷病"]:
        score += 9
        reasons.append("Wealth普通，可提前建立財務安全網")

    if age >= 60 and category in ["長照退休", "退休理財"]:
        score += 24
        reasons.append("已接近或進入退休階段，長照與退休現金流更重要")
    elif age >= 45 and category in ["重大疾病/傷病", "長照退休", "退休理財"]:
        score += 12
        reasons.append("中年後重症、長照與退休準備的重要性提高")
    elif age < 45 and ptype in ["實支實付醫療險", "重大傷病險", "壽險", "外溢健康計畫", "意外傷害險"]:
        score += 10
        reasons.append("年輕階段適合先建立保障基本盤")

    if last_event_tag and ptype in TAG_TO_TYPES.get(last_event_tag, []):
        score += 28
        reasons.append("符合你剛遇到的人生事件，可直接降低同類風險")

    if goal:
        if goal in ["健康退休", "財富自由"] and category in ["退休理財", "長照退休", "健康促進"]:
            score += 8
            reasons.append(f"符合你的人生目標：{goal}")
        if goal in ["照顧家人", "買房"] and category in ["人身保障", "重大疾病/傷病"]:
            score += 8
            reasons.append(f"符合你的人生責任：{goal}")

    if category == "健康促進" and "FitBack 健康吧" not in owned:
        score += 4
        reasons.append("可用健康行為累積長期回饋與小樹點")

    if not reasons:
        reasons.append("可作為長期人生規劃的基礎保障配置")

    return min(99, score), reasons[:4]


def recommend_products(health, mind, wealth, last_event_tag=None, owned=None, limit=3, age=25, goal=""):
    rows = recommend_products_detailed(health, mind, wealth, age, last_event_tag, owned, limit, goal)
    return [(r["score"], r["product"], "、".join(r["reasons"])) for r in rows]


def recommend_products_detailed(health, mind, wealth, age=25, last_event_tag=None, owned=None, limit=3, goal=""):
    owned = owned or []
    rows = []
    for p in INSURANCE_LIBRARY:
        if p["game_item"] in owned:
            continue
        score, reasons = score_product(p, health, mind, wealth, age, last_event_tag, owned, goal)
        rows.append({"score": score, "product": p, "reasons": reasons})
    rows.sort(key=lambda x: x["score"], reverse=True)
    return rows[:limit]


def coverage_scores(owned):
    owned = owned or []
    owned_products = [p for p in INSURANCE_LIBRARY if p["game_item"] in owned]
    health = finance = retirement = claim = 8

    for p in owned_products:
        cat = p["category"]
        typ = p["type"]
        if cat in ["健康醫療", "重大疾病/傷病"]:
            health += 22
            finance += 12
            claim += 5
        if typ in ["實支實付醫療險", "手術醫療險", "自負額實支實付"]:
            health += 12
            finance += 6
        if typ in ["癌症險", "重大傷病險", "重大疾病險", "重大傷病定期保險"]:
            health += 14
            finance += 12
        if cat == "人身保障":
            finance += 25
            claim += 8
        if cat in ["長照退休", "退休理財"]:
            retirement += 28
            finance += 8
        if cat == "健康促進":
            health += 18
            claim += 16
        if typ in ["變額年金保險", "變額萬能壽險", "投資連結型保險"]:
            retirement += 12
            finance += 12

    return {
        "健康醫療保障": clamp(health),
        "財務安全保障": clamp(finance),
        "退休長照保障": clamp(retirement),
        "理賠便利保障": clamp(claim),
    }


def product_scenario_preview(product, health, mind, wealth, last_event_tag=None):
    event_tag = last_event_tag
    if not event_tag or event_tag == "healthy":
        event_tag = infer_tag_for_product(product)
    event_name, dh, dm, dw = TAG_TO_SCENARIO.get(event_tag, ("人生風險事件", -15, -10, -15))

    without_vals = (clamp(health + dh), clamp(mind + dm), clamp(wealth + dw))
    effect = product.get("effect", {})
    bonus = {}
    if event_tag in effect:
        bonus.update(effect[event_tag])
    if "all" in effect:
        for k, v in effect["all"].items():
            bonus[k] = bonus.get(k, 0) + v

    with_vals = (
        clamp(health + dh + bonus.get("health", 0)),
        clamp(mind + dm + bonus.get("mind", 0)),
        clamp(wealth + dw + bonus.get("wealth", 0)),
    )
    return event_name, without_vals, with_vals
