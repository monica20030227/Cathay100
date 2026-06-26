# recommendation.py
from insurance_db import INSURANCE_LIBRARY

TAG_TO_TYPES = {
    "critical": ["重大傷病險", "重大疾病險", "重大傷病定期保險"],
    "cancer": ["癌症險", "重大疾病險"],
    "surgery": ["實支實付醫療險", "手術醫療險", "自負額實支實付"],
    "medical": ["實支實付醫療險", "手術醫療險", "自負額實支實付"],
    "longcare": ["長期照顧險"],
    "market": ["變額年金保險", "變額萬能壽險", "投資連結型保險"],
    "retirement": ["變額年金保險", "長期照顧險", "投資連結型保險"],
    "family": ["壽險", "變額萬能壽險"],
    "accident": ["意外傷害險"],
    "stress": ["外溢健康計畫"],
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
}

CATEGORY_COVERAGE_MAP = {
    "健康醫療保障": ["健康醫療", "重大疾病/傷病", "健康促進"],
    "財務安全保障": ["健康醫療", "重大疾病/傷病", "人身保障", "退休理財"],
    "退休長照保障": ["長照退休", "退休理財"],
    "理賠便利保障": ["健康促進"],
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
    risks = {
        "健康風險": 100 - health,
        "心理壓力": 100 - mind,
        "財務風險": 100 - wealth,
    }
    return max(risks, key=risks.get)


def score_product(p, health, mind, wealth, age=25, last_event_tag=None, owned=None):
    owned = owned or []
    if p["game_item"] in owned:
        return 0, ["已配置，不重複推薦"]

    score = 45
    reasons = []

    if health < 60 and p["category"] in ["健康醫療", "重大疾病/傷病", "健康促進", "長照退休"]:
        score += 18
        reasons.append("Health偏低，需要健康醫療防線")
    if mind < 60 and p["category"] in ["健康促進", "人身保障"]:
        score += 12
        reasons.append("Mind偏低，需要降低照護與家庭壓力")
    if wealth < 60 and p["category"] in ["健康醫療", "重大疾病/傷病", "退休理財", "人身保障"]:
        score += 18
        reasons.append("Wealth偏低，需要財務風險轉嫁")
    if age >= 60 and p["category"] in ["長照退休", "退休理財"]:
        score += 22
        reasons.append("已接近/進入退休階段，長照與退休現金流更重要")
    if age < 45 and p["type"] in ["實支實付醫療險", "重大傷病險", "壽險", "外溢健康計畫"]:
        score += 8
        reasons.append("年輕階段適合先建立基本盤")
    if last_event_tag and p["type"] in TAG_TO_TYPES.get(last_event_tag, []):
        score += 25
        reasons.append("符合你剛遇到的人生事件")

    if not reasons:
        reasons.append("可作為長期人生規劃的基礎保障配置")
    return min(99, score), reasons


def recommend_products(health, mind, wealth, last_event_tag=None, owned=None, limit=3, age=25):
    owned = owned or []
    scores = []
    for p in INSURANCE_LIBRARY:
        if p["game_item"] in owned:
            continue
        score, reasons = score_product(p, health, mind, wealth, age, last_event_tag, owned)
        scores.append((score, p, "、".join(reasons)))
    scores.sort(key=lambda x: x[0], reverse=True)
    return scores[:limit]


def recommend_products_detailed(health, mind, wealth, age=25, last_event_tag=None, owned=None, limit=3):
    owned = owned or []
    rows = []
    for p in INSURANCE_LIBRARY:
        if p["game_item"] in owned:
            continue
        score, reasons = score_product(p, health, mind, wealth, age, last_event_tag, owned)
        rows.append({"score": score, "product": p, "reasons": reasons})
    rows.sort(key=lambda x: x["score"], reverse=True)
    return rows[:limit]


def coverage_scores(owned):
    owned = owned or []
    owned_products = [p for p in INSURANCE_LIBRARY if p["game_item"] in owned]

    health = 10
    finance = 10
    retirement = 10
    claim = 10

    for p in owned_products:
        cat = p["category"]
        typ = p["type"]
        if cat in ["健康醫療", "重大疾病/傷病"]:
            health += 22
            finance += 12
        if typ in ["實支實付醫療險", "手術醫療險", "自負額實支實付"]:
            health += 10
        if typ in ["癌症險", "重大傷病險", "重大疾病險", "重大傷病定期保險"]:
            health += 12
            finance += 10
        if cat == "人身保障":
            finance += 25
        if cat in ["長照退休", "退休理財"]:
            retirement += 28
            finance += 8
        if cat == "健康促進":
            health += 18
            claim += 12

    return {
        "健康醫療保障": clamp(health),
        "財務安全保障": clamp(finance),
        "退休長照保障": clamp(retirement),
        "理賠便利保障": clamp(claim),
    }


def product_scenario_preview(product, health, mind, wealth, last_event_tag=None):
    event_tag = last_event_tag
    if not event_tag:
        for tag, types in TAG_TO_TYPES.items():
            if product["type"] in types:
                event_tag = tag
                break
    event_tag = event_tag or "medical"
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
