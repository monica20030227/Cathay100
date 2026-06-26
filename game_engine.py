# game_engine.py
import random
from insurance_db import get_product_by_item

EVENT_POOL = [
    {"name":"過勞危機：連續加班讓身心急速下滑", "tag":"stress", "dh":-18, "dm":-16, "dw":-5},
    {"name":"股市黑天鵝：投資部位大幅震盪", "tag":"market", "dh":-3, "dm":-12, "dw":-28},
    {"name":"重大疾病風險：醫療支出突然增加", "tag":"critical", "dh":-28, "dm":-12, "dw":-25},
    {"name":"癌症治療挑戰：療程與收入中斷同時壓上來", "tag":"cancer", "dh":-32, "dm":-18, "dw":-32},
    {"name":"住院手術事件：短期醫療費用增加", "tag":"surgery", "dh":-20, "dm":-10, "dw":-22},
    {"name":"退休焦慮：收入轉換帶來不確定感", "tag":"retirement", "dh":-8, "dm":-22, "dw":-16},
    {"name":"長照需求出現：家庭照護與財務壓力同步上升", "tag":"longcare", "dh":-32, "dm":-18, "dw":-34},
    {"name":"親人離世：心理韌性遭受重大衝擊", "tag":"family", "dh":-5, "dm":-38, "dw":-5},
    {"name":"意外事故：突發醫療與工作中斷", "tag":"accident", "dh":-24, "dm":-10, "dw":-20},
    {"name":"健康習慣回饋：規律作息讓身心回升", "tag":"healthy", "dh":12, "dm":7, "dw":4},
    {"name":"資產配置成功：長期理財開始發酵", "tag":"income", "dh":0, "dm":6, "dw":22},
    {"name":"職涯升級：收入提升但壓力也增加", "tag":"income", "dh":-5, "dm":-8, "dw":24},
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
    dh, dm, dw, effect_logs = apply_item_effects(event["tag"], age, items, dh, dm, dw)
    new_health = clamp(health + dh)
    new_mind = clamp(mind + dm)
    new_wealth = clamp(wealth + dw)
    tree_gain = 0
    if new_health >= 75:
        tree_gain += 2
    if "FitBack 健康吧" in items and new_health >= 70:
        tree_gain += 1
    return event, new_health, new_mind, new_wealth, tree_gain, effect_logs
