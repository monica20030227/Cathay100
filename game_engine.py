# game_engine.py
import random
from insurance_db import get_product_by_item

EVENT_POOL = [
    {"name":"過勞危機：連續加班讓身心急速下滑", "tag":"stress", "dh":-18, "dm":-16, "dw":-5, "severity":"medium"},
    {"name":"股市黑天鵝：投資部位大幅震盪", "tag":"market", "dh":-3, "dm":-12, "dw":-28, "severity":"high"},
    {"name":"重大疾病風險：醫療支出突然增加", "tag":"critical", "dh":-28, "dm":-12, "dw":-25, "severity":"high"},
    {"name":"癌症治療挑戰：療程與收入中斷同時壓上來", "tag":"cancer", "dh":-32, "dm":-18, "dw":-32, "severity":"high"},
    {"name":"住院手術事件：短期醫療費用增加", "tag":"surgery", "dh":-20, "dm":-10, "dw":-22, "severity":"high"},
    {"name":"退休焦慮：收入轉換帶來不確定感", "tag":"retirement", "dh":-8, "dm":-22, "dw":-16, "severity":"medium"},
    {"name":"長照需求出現：家庭照護與財務壓力同步上升", "tag":"longcare", "dh":-32, "dm":-18, "dw":-34, "severity":"high"},
    {"name":"失智照護：高齡照護需求增加", "tag":"longcare", "dh":-20, "dm":-25, "dw":-30, "severity":"high"},
    {"name":"親人離世：心理韌性遭受重大衝擊", "tag":"family", "dh":-5, "dm":-38, "dw":-5, "severity":"high"},
    {"name":"意外事故：突發醫療與工作中斷", "tag":"accident", "dh":-24, "dm":-10, "dw":-20, "severity":"high"},
    {"name":"家庭責任增加：照顧與支出壓力同步提高", "tag":"family", "dh":-8, "dm":-16, "dw":-18, "severity":"medium"},
    {"name":"健康習慣回饋：規律作息讓身心回升", "tag":"healthy", "dh":12, "dm":7, "dw":4, "severity":"good"},
    {"name":"資產配置成功：長期理財開始發酵", "tag":"income", "dh":0, "dm":6, "dw":22, "severity":"good"},
    {"name":"職涯升級：收入提升但壓力也增加", "tag":"income", "dh":-5, "dm":-8, "dw":24, "severity":"good"},
]

def clamp(x):
    return max(0, min(100, int(x)))

def apply_item_effects(event_tag, age, items, dh, dm, dw):
    effect_logs = []
    for item in items:
        p = get_product_by_item(item)
        if not p:
            continue
        effect = p.get("effect", {})
        bonus = {}
        if event_tag in effect:
            bonus.update(effect[event_tag])
        if "all" in effect:
            for k, v in effect["all"].items():
                bonus[k] = bonus.get(k, 0) + v
        if item == "國泰長照守護" and age < 70 and event_tag == "longcare":
            bonus = {"wealth": 12, "mind": 5}
        if bonus:
            dh += bonus.get("health", 0)
            dm += bonus.get("mind", 0)
            dw += bonus.get("wealth", 0)
            effect_logs.append(f"{p['icon']} {item} 啟動：{p['type']}防禦生效")
    return dh, dm, dw, effect_logs

def next_event(age, health, mind, wealth, items):
    event = random.choice(EVENT_POOL)
    dh, dm, dw = event["dh"], event["dm"], event["dw"]
    original = (dh, dm, dw)
    dh, dm, dw, effect_logs = apply_item_effects(event["tag"], age, items, dh, dm, dw)
    defended = dh > original[0] or dm > original[1] or dw > original[2]
    defense_notice = ""
    if defended:
        blocked = (dh-original[0]) + (dm-original[1]) + (dw-original[2])
        defense_notice = f"🛡️ 國泰神盾主動攔截！「{event['name'].split('：')[0]}」減輕了約 {blocked} 點總衝擊。"
    new_health = clamp(health + dh)
    new_mind = clamp(mind + dm)
    new_wealth = clamp(wealth + dw)
    tree_gain = 0
    if new_health >= 75:
        tree_gain += 2
    if "FitBack 健康吧" in items and new_health >= 70:
        tree_gain += 1
    return event, new_health, new_mind, new_wealth, tree_gain, effect_logs, defense_notice

def analyze_life_risk(health, mind, wealth, age, items):
    insights = []
    if health < 60:
        insights.append("Health 偏低，代表醫療、疾病或長照風險可能成為主要破口。")
    if mind < 60:
        insights.append("Mind 偏低，代表壓力、照護負擔或理賠流程可能造成二次傷害。")
    if wealth < 60:
        insights.append("Wealth 偏低，代表遇到住院、癌症、股災或退休轉換時，財務緩衝不足。")
    if age >= 60 and not any(x in items for x in ["國泰長照守護", "變額年金退休金流"]):
        insights.append("你已進入退休與高齡風險區，但長照或退休現金流配置仍不足。")
    if not items:
        insights.append("目前沒有配置任何保障，真實人生中容易讓單一事件造成連鎖衝擊。")
    if not insights:
        insights.append("你的身、心、財相對均衡，已具備基本的人生風險防護網。")
    return insights

def protection_score(items, health, mind, wealth):
    base = min(70, len(items) * 9)
    balance = int((health + mind + wealth) / 3 * 0.3)
    diversity = len(set(items)) * 2
    return clamp(base + balance + diversity)
