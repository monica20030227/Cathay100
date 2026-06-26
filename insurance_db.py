# insurance_db.py
# 國泰 Life100 保險百科資料庫
# 注意：此處為競賽 Demo 用摘要，正式投保資訊請以國泰人壽官方商品頁與保單條款為準。

INSURANCE_LIBRARY = [
    {
        "id": "cv4",
        "category": "健康醫療",
        "icon": "🏥",
        "game_item": "新實全心意PLUS住院醫療",
        "type": "實支實付醫療險",
        "name": "新實全心意PLUS住院醫療健康保險附約（外溢型）",
        "short": "住院醫療實支實付及日額給付方式擇優，補強住院、手術與自費醫療支出風險。",
        "coverage": ["住院給付", "手術給付", "其他給付", "加護或燒燙傷病房慰問金", "FitBack保費折減"],
        "suitable": ["剛出社會、想先補醫療基本盤", "擔心自費醫材、住院雜費", "希望降低疾病造成財務壓力"],
        "game_effect": "住院/手術事件：Wealth損失-70%；若Health低於50，額外回復Health +5。",
        "effect": {"medical": {"health": 5, "wealth": 22}, "surgery": {"health": 4, "wealth": 20}},
        "cost": 14,
        "official_url": "https://www.cathaylife.com.tw/official/products/health-reimbursement-benefits/cv4",
        "source_note": "官方頁說明此商品含住院給付、手術給付與其他給付；住院給付採實支實付型與日額給付型擇優。"
    },
    {
        "id": "wv4",
        "category": "健康醫療",
        "icon": "🏥",
        "game_item": "超實在自負額住院醫療",
        "type": "自負額實支實付",
        "name": "超實在自負額住院醫療健康保險附約（外溢型）",
        "short": "適合已有基本醫療保障、想用自負額設計補強高額醫療風險的人。",
        "coverage": ["住院給付", "手術給付", "健康促進回饋", "自負額設計", "FitBack保費折減"],
        "suitable": ["已有基礎實支實付者", "想補強高額住院醫療費", "希望用較有策略的方式提高醫療防線"],
        "game_effect": "大型醫療事件：Wealth傷害-55%；若已有實支實付，額外降低10點損失。",
        "effect": {"medical": {"wealth": 18}, "surgery": {"wealth": 16}},
        "cost": 12,
        "official_url": "https://www.cathaylife.com.tw/official/products/health-reimbursement-benefits/wv4",
        "source_note": "官方頁說明此商品提供住院醫療實支實付，須扣除自負額，並含門診手術費用實支實付。"
    },
    {
        "id": "b93",
        "category": "健康醫療",
        "icon": "🩺",
        "game_item": "真大心PLUS手術醫療",
        "type": "手術醫療險",
        "name": "真大心PLUS住院醫療健康保險附約（外溢型）",
        "short": "主打住院手術、門診手術與特定處置保險金，適合補強手術風險。",
        "coverage": ["住院手術", "門診手術", "101項特定處置", "FitBack保費折減"],
        "suitable": ["擔心手術費用者", "想補門診手術保障者", "希望醫療保障更完整者"],
        "game_effect": "手術事件：Wealth損失-65%，Mind壓力-6。",
        "effect": {"surgery": {"wealth": 20, "mind": 6}, "medical": {"wealth": 8}},
        "cost": 13,
        "official_url": "https://www.cathaylife.com.tw/official/products/health-surgery/b93",
        "source_note": "官方頁說明此商品含住院手術、門診手術及101項特定處置保險金。"
    },
    {
        "id": "cfr",
        "category": "重大疾病/傷病",
        "icon": "🛡️",
        "game_item": "自由配重大傷病",
        "type": "重大傷病險",
        "name": "自由配一年定期初次罹患重大傷病健康保險（外溢型）",
        "short": "經診斷初次罹患重大傷病時，提供一次性保險金，協助治療與收入中斷風險。",
        "coverage": ["重大傷病一次金", "保證續保至80歲", "FitBack最高折減3%", "保額30萬至200萬"],
        "suitable": ["擔心重大疾病造成財務斷崖", "家庭經濟支柱", "想先建立重症防線者"],
        "game_effect": "重大疾病事件：Wealth傷害-80%，Health最低保留20。",
        "effect": {"critical": {"health": 15, "wealth": 28}, "medical": {"wealth": 12}},
        "cost": 20,
        "official_url": "https://www.cathaylife.com.tw/official/products/health-illness/cfr",
        "source_note": "官方頁說明此商品經診斷初次罹患重大傷病時，給付一次性保險金，並可加入FitBack。"
    },
    {
        "id": "px5",
        "category": "重大疾病/傷病",
        "icon": "🧬",
        "game_item": "鍾溢祝福重大疾病",
        "type": "重大疾病險",
        "name": "鍾溢祝福重大疾病健康保險附約(乙型)(外溢型)",
        "short": "一次擁有重疾與輕度重疾保障，適合補強癌症、心腦血管等重大疾病風險。",
        "coverage": ["重大疾病", "輕度重大疾病", "FitBack最高折減3%", "一年期"],
        "suitable": ["擔心重疾治療費", "有家族病史風險者", "想用一次金補收入中斷者"],
        "game_effect": "重大疾病事件：Wealth +24防禦，Mind +5穩定。",
        "effect": {"critical": {"wealth": 24, "mind": 5}, "cancer": {"wealth": 18}},
        "cost": 18,
        "official_url": "https://www.cathaylife.com.tw/official/products/health-illness/px5",
        "source_note": "官方頁說明此商品提供重疾/輕度重疾保障，加入FitBack最高折減3%。"
    },
    {
        "id": "zco",
        "category": "重大疾病/傷病",
        "icon": "❤️",
        "game_item": "新鍾心滿福重大傷病",
        "type": "重大傷病定期保險",
        "name": "新鍾心滿福重大傷病定期保險(外溢型)",
        "short": "結合身故/完全失能與重大傷病保障，並加碼心血管疾病與特定重大傷病。",
        "coverage": ["身故/完全失能", "重大傷病", "心血管疾病保障", "特定重大傷病額外給付", "外溢保單"],
        "suitable": ["中高齡健康風險上升者", "重視心血管風險者", "想同時兼顧壽險與重症保障者"],
        "game_effect": "心血管/重大傷病事件：Health +18防禦，Wealth +26防禦。",
        "effect": {"critical": {"health": 18, "wealth": 26}, "family": {"wealth": 12}},
        "cost": 22,
        "official_url": "https://www.cathaylife.com.tw/official/products/health-illness/zco",
        "source_note": "官方頁說明保障範圍主要參照全民健保重大傷病，並提供心血管疾病保障及特定重大傷病額外給付。"
    },
    {
        "id": "cancer_cfq",
        "category": "重大疾病/傷病",
        "icon": "🎗️",
        "game_item": "自由配癌症保障",
        "type": "癌症險",
        "name": "自由配一年定期初次罹患癌症健康保險附約（外溢型）",
        "short": "針對初次罹患癌症提供一次性保險金，適合補強癌症治療與收入中斷風險。",
        "coverage": ["癌症給付", "初期/輕度/重度癌症", "FitBack最高折減3%"],
        "suitable": ["擔心癌症治療費者", "想以一次金彈性運用者", "已有基本醫療但缺癌症保障者"],
        "game_effect": "癌症事件：Wealth傷害-75%，Mind壓力-8。",
        "effect": {"cancer": {"wealth": 26, "mind": 8}, "critical": {"wealth": 12}},
        "cost": 18,
        "official_url": "https://www.cathaylife.com.tw/official/products/health-illness",
        "source_note": "官方重大疾病/傷病分類頁列出自由配一年定期初次罹患癌症健康保險附約（外溢型），提供癌症給付。"
    },
    {
        "id": "ltc",
        "category": "長照退休",
        "icon": "🌳",
        "game_item": "國泰長照守護",
        "type": "長期照顧險",
        "name": "國泰長期照顧保險商品",
        "short": "當年老、失能或需要長期照顧時，協助支付看護、照護機構與家庭照顧成本。",
        "coverage": ["長期照顧給付", "照護費用支援", "長照狀態保障", "高齡風險防線"],
        "suitable": ["40歲後開始規劃長照風險者", "擔心老後拖累家人者", "家庭照顧壓力高者"],
        "game_effect": "70歲後長照事件：Wealth傷害-85%，Health最低保留30。",
        "effect": {"longcare": {"health": 25, "wealth": 32}, "aging": {"wealth": 15}},
        "cost": 22,
        "official_url": "https://www.cathaylife.com.tw/official/products/health-long-term-care",
        "source_note": "國泰長照商品頁列出長期照顧相關健康保險，作為老後照顧風險規劃。"
    },
    {
        "id": "accident",
        "category": "人身保障",
        "icon": "⚠️",
        "game_item": "意外傷害防護",
        "type": "意外傷害險",
        "name": "國泰人壽意外傷害險",
        "short": "面對意外造成的身故、完全失能或醫療支出，提供事故型風險轉嫁。",
        "coverage": ["意外身故", "完全失能", "意外醫療", "實支實付規劃"],
        "suitable": ["通勤族", "常旅遊或戶外活動者", "家庭經濟責任者"],
        "game_effect": "意外事件：Health傷害-40%，Wealth傷害-60%。",
        "effect": {"accident": {"health": 16, "wealth": 22}, "surgery": {"wealth": 8}},
        "cost": 10,
        "official_url": "https://www.cathaylife.com.tw/official/products/accident",
        "source_note": "國泰意外傷害險頁面說明提供疾病或意外所造成之身故或完全失能保障，也提供意外險實支實付規劃。"
    },
    {
        "id": "life",
        "category": "人身保障",
        "icon": "👨‍👩‍👧",
        "game_item": "家庭壽險守護",
        "type": "壽險",
        "name": "國泰人壽壽險商品",
        "short": "當家庭主要收入者發生身故或完全失能時，協助家人維持生活與財務安全。",
        "coverage": ["身故保障", "完全失能保障", "家庭責任轉嫁", "資產傳承"],
        "suitable": ["家庭主要經濟來源", "有房貸/子女教育責任者", "想保護家人生活者"],
        "game_effect": "家庭責任事件：Wealth不會歸零，Mind壓力-10。",
        "effect": {"family": {"wealth": 26, "mind": 10}, "income": {"wealth": 10}},
        "cost": 16,
        "official_url": "https://www.cathaylife.com.tw/official/products/life-caring",
        "source_note": "國泰壽險商品分類頁提供定期壽險、終身壽險等人身保障商品。"
    },
    {
        "id": "va",
        "category": "退休理財",
        "icon": "💰",
        "game_item": "變額年金退休金流",
        "type": "變額年金保險",
        "name": "國泰人壽變額年金投資型保險",
        "short": "兼具保障與資產配置功能，適合退休規劃與未來現金流安排。",
        "coverage": ["年金給付", "投資標的累積帳戶價值", "退休現金流", "資產配置"],
        "suitable": ["想規劃退休現金流者", "願意承擔投資波動者", "有長期資產配置需求者"],
        "game_effect": "65歲後每回合 Wealth +8；市場事件 Wealth傷害-35%。",
        "effect": {"retirement": {"wealth": 24}, "market": {"wealth": 18}, "aging": {"wealth": 10}},
        "cost": 20,
        "official_url": "https://www.cathaylife.com.tw/official/products/investment-va",
        "source_note": "官方頁說明變額年金保險具備保障與資產配置功能，並強調年金給付與退休規劃。"
    },
    {
        "id": "vul",
        "category": "退休理財",
        "icon": "📈",
        "game_item": "變額萬能壽險配置",
        "type": "變額萬能壽險",
        "name": "國泰人壽變額萬能壽險",
        "short": "繳費時間與金額較彈性，可依人生階段調整保障與資產配置。",
        "coverage": ["壽險保障", "彈性繳費", "投資帳戶價值", "人生階段調整"],
        "suitable": ["收入成長型族群", "想同時兼顧保障與投資者", "重視彈性規劃者"],
        "game_effect": "職涯升級或市場事件：Wealth波動-40%，家庭責任事件額外防禦。",
        "effect": {"market": {"wealth": 20}, "income": {"wealth": 14}, "family": {"wealth": 10}},
        "cost": 20,
        "official_url": "https://www.cathaylife.com.tw/official/products/investment-vul",
        "source_note": "官方頁說明變額萬能壽險繳費時間與金額彈性，保額會隨投資內容價值變化。"
    },
    {
        "id": "unit_linked",
        "category": "退休理財",
        "icon": "🔗",
        "game_item": "投資連結型保險",
        "type": "投資連結型保險",
        "name": "國泰人壽投資連(鏈)結型保險",
        "short": "多與公司債或結構型債券連結，偏向固定收益與資產配置需求。",
        "coverage": ["投資連結", "固定收益規劃", "資產配置", "身故/完全失能等依商品設計"],
        "suitable": ["有一次性資金配置需求者", "重視收益規劃者", "想將保險與投資結合者"],
        "game_effect": "市場黑天鵝事件：Wealth傷害-45%；退休階段額外+6 Wealth。",
        "effect": {"market": {"wealth": 22}, "retirement": {"wealth": 14}},
        "cost": 22,
        "official_url": "https://www.cathaylife.com.tw/official/products/investment-unit-linked",
        "source_note": "官方頁說明投資連(鏈)結型保單多連結公司債與結構型債券，常見為一次繳清保費。"
    },
    {
        "id": "fitback",
        "category": "健康促進",
        "icon": "🌱",
        "game_item": "FitBack 健康吧",
        "type": "外溢健康計畫",
        "name": "FitBack健康吧",
        "short": "透過健康任務與會員等級，將健康行為轉化為保費折減或健康促進回饋。",
        "coverage": ["健康任務", "會員等級", "保費折減", "健康促進回饋"],
        "suitable": ["願意運動與健康管理者", "想降低保費負擔者", "適合與外溢型商品搭配"],
        "game_effect": "每回合Health +6；Health高於75時小樹點+2；慢性病事件機率下降。",
        "effect": {"all": {"health": 6}, "health_bonus": {"tree": 2}},
        "cost": 8,
        "official_url": "https://www.cathaylife.com.tw/cathaylife/services/health/fitback",
        "source_note": "多項國泰外溢型商品頁說明加入FitBack健康計劃可依會員等級享保費折減。"
    }
]

CATEGORY_DESCRIPTIONS = {
    "健康醫療": "面對住院、手術、自費醫材與醫療支出風險，協助維持財務安全。",
    "重大疾病/傷病": "面對癌症、重大傷病、心腦血管等高衝擊事件，提供一次金或重症防線。",
    "長照退休": "面對高齡、失能、長期照顧與退休現金流風險，建立老後防護網。",
    "人身保障": "面對意外、身故、完全失能與家庭責任，保護家人與生活穩定。",
    "退休理財": "兼顧保障與資產配置，支援退休、投資與長期財務規劃。",
    "健康促進": "透過健康任務、外溢回饋與行為鼓勵，將健康管理轉化為保障加值。"
}

def get_product_by_item(item_name):
    for p in INSURANCE_LIBRARY:
        if p["game_item"] == item_name:
            return p
    return None

def get_products_by_category(category):
    return [p for p in INSURANCE_LIBRARY if p["category"] == category]

def product_names():
    return [p["game_item"] for p in INSURANCE_LIBRARY]
