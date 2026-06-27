# recommendation.py
from insurance_db import INSURANCE_LIBRARY

TAG_TO_TYPES = {
    "critical": ["重大傷病險", "重大疾病險", "重大傷病定期保險"],
    "cancer": ["癌症險", "重大疾病險"],
    "surgery": ["實支實付醫療險", "手術醫療險", "自負額實支實付"],
    "medical": ["實支實付醫療險", "手術醫療險"],
    "longcare": ["長期照顧險"],
    "market": ["變額年金保險", "變額萬能壽險", "投資連結型保險"],
    "retirement": ["變額年金保險", "長期照顧險"],
    "family": ["壽險", "變額萬能壽險"],
    "accident": ["意外傷害險"],
    "stress": ["外溢健康計畫"],
}

def recommend_products(health, mind, wealth, last_event_tag=None, owned=None, limit=3):
    owned = owned or []
    scores = []
    for p in INSURANCE_LIBRARY:
        if p["game_item"] in owned:
            continue
        score = 0
        reason = []
        if health < 60 and p["category"] in ["健康醫療", "重大疾病/傷病", "健康促進"]:
            score += 3; reason.append("你的Health偏低，需要健康醫療防線")
        if mind < 60 and p["category"] in ["健康促進", "人身保障"]:
            score += 2; reason.append("你的Mind偏低，需要降低照護/理賠壓力")
        if wealth < 60 and p["category"] in ["健康醫療", "重大疾病/傷病", "退休理財"]:
            score += 3; reason.append("你的Wealth偏低，需要財務風險轉嫁")
        if last_event_tag and p["type"] in TAG_TO_TYPES.get(last_event_tag, []):
            score += 5; reason.append("符合你剛遇到的人生事件")
        if score == 0:
            score = 1; reason.append("可作為基礎保障配置")
        scores.append((score, p, "、".join(reason)))
    scores.sort(key=lambda x: x[0], reverse=True)
    return scores[:limit]
