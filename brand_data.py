# -*- coding: utf-8 -*-
"""
Brand Recommendation Database
Contains brand data organized by price tier and style categories
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class Brand:
    """Represents a fashion brand"""
    name: str
    category: str  # clothing, shoes, bags, accessories
    price_tier: str  # budget, mid, premium, luxury
    price_range_cn: str  # Price range in RMB
    styles: List[str] = field(default_factory=list)
    description: str = ""
    target_audience: str = ""
    best_for: List[str] = field(default_factory=list)
    reasons_template: str = ""  # Template for recommendation reasons


class BrandDatabase:
    """Comprehensive brand database for recommendations"""

    BRANDS = [
        # === Budget Tier (学生/低收入) ===
        Brand(
            name="优衣库 UNIQLO",
            category="服装",
            price_tier="budget",
            price_range_cn="79-599",
            styles=["简约", "清纯", "保暖", "优雅"],
            description="日本快时尚品牌，以基础款和高品质面料著称",
            target_audience="学生、上班族、追求性价比的人群",
            best_for=["日常通勤", "基础搭配", " layering"],
            reasons_template="基础款经典耐穿，{styles}风格，品质稳定且不显廉价",
        ),
        Brand(
            name="MUJI无印良品",
            category="服装",
            price_tier="budget",
            price_range_cn="99-699",
            styles=["简约", "清纯", "优雅"],
            description="日式极简风格，天然材质，去品牌化设计",
            target_audience="喜欢极简自然风格的人群",
            best_for=["日常穿搭", "简约风格", "舒适穿着"],
            reasons_template="极简设计理念，天然面料{styles}，品质生活入门之选",
        ),
        Brand(
            name="ZARA",
            category="服装",
            price_tier="budget",
            price_range_cn="129-899",
            styles=["简约", "活泼", "可爱", "性感", "优雅"],
            description="西班牙快时尚，紧跟潮流，款式更新快",
            target_audience="年轻时尚人群，学生，初入职场的年轻人",
            best_for=["潮流穿搭", "约会", "聚会", "逛街"],
            reasons_template="全球连锁快时尚，{styles}款式丰富且有设计感",
        ),
        Brand(
            name="H&M",
            category="服装",
            price_tier="budget",
            price_range_cn="69-599",
            styles=["简约", "活泼", "可爱", "清纯"],
            description="瑞典快时尚品牌，与大牌联名频繁",
            target_audience="年轻学生，追求潮流但预算有限",
            best_for=["学生穿搭", "潮流入门", "日常休闲"],
            reasons_template="价格友好，{styles}风格选择多样，联名款有惊喜",
        ),
        Brand(
            name="Teenmix 天美意",
            category="鞋履",
            price_tier="budget",
            price_range_cn="200-800",
            styles=["可爱", "清纯", "活泼", "简约"],
            description="百丽旗下年轻鞋履品牌，款式多样",
            target_audience="年轻女性，学生，初入职场的女生",
            best_for=["日常穿搭", "校园", "休闲约会"],
            reasons_template="{styles}款式居多，运动鞋、休闲鞋、小皮鞋应有尽有",
        ),
        Brand(
            name="热风 Hotwind",
            category="鞋履",
            price_tier="budget",
            price_range_cn="79-399",
            styles=["简约", "活泼", "可爱", "清纯"],
            description="国产快时尚品牌，鞋履和配饰性价比高",
            target_audience="学生、年轻上班族",
            best_for=["日常通勤", "学生穿搭", "基础款"],
            reasons_template="国产品牌性价比之选，{styles}基础款丰富",
        ),
        Brand(
            name="Charles & Keith",
            category="包袋/鞋履",
            price_tier="budget",
            price_range_cn="369-799",
            styles=["优雅", "简约", "成熟"],
            description="新加坡快时尚品牌，设计精致",
            target_audience="年轻职场女性，追求精致但预算有限",
            best_for=["职场穿搭", "约会", "正式场合"],
            reasons_template="新加坡精致快时尚，{styles}设计，品质在线",
        ),
        Brand(
            name="Urban Revivo",
            category="服装",
            price_tier="budget",
            price_range_cn="199-899",
            styles=["简约", "优雅", "成熟", "性感"],
            description="国产快时尚品牌，设计感较强",
            target_audience="年轻职场女性",
            best_for=["职场穿搭", "日常精致", "约会"],
            reasons_template="国产设计感快时尚，{styles}风格品质在线",
        ),

        # === Mid Tier (中等收入) ===
        Brand(
            name="COS",
            category="服装",
            price_tier="mid",
            price_range_cn="300-1500",
            styles=["简约", "优雅", "成熟"],
            description="H&M集团旗下高端线，极简高级感设计",
            target_audience="追求品质和设计感的都市人群",
            best_for=["职场通勤", "极简风格", "高级感穿搭"],
            reasons_template="极简高级感代名词，{styles}风格彰显品味",
        ),
        Brand(
            name="Massimo Dutti",
            category="服装",
            price_tier="mid",
            price_range_cn="400-2000",
            styles=["优雅", "成熟", "简约"],
            description="ZARA集团旗下高端品牌，成熟优雅风格",
            target_audience="30+成熟职场女性，追求品质",
            best_for=["商务场合", "正式穿搭", "品质日常"],
            reasons_template="西班牙成熟优雅风，{styles}品质彰显气质",
        ),
        Brand(
            name="Sandro",
            category="服装",
            price_tier="mid",
            price_range_cn="1000-4000",
            styles=["优雅", "成熟", "简约", "活泼"],
            description="法式轻奢品牌，浪漫优雅风格",
            target_audience="都市白领，追求法式优雅",
            best_for=["职场", "约会", "下午茶", "派对"],
            reasons_template="法式轻奢浪漫，{styles}风格适合都市精致生活",
        ),
        Brand(
            name="Maje",
            category="服装",
            price_tier="mid",
            price_range_cn="1000-4000",
            styles=["优雅", "活泼", "成熟", "性感"],
            description="法式轻奢品牌，比Sandro更活泼时尚",
            target_audience="年轻都市女性，喜欢法式风格",
            best_for=["约会", "派对", "日常精致", "度假"],
            reasons_template="法式浪漫轻奢，{styles}风格更显年轻活力",
        ),
        Brand(
            name="Clarks",
            category="鞋履",
            price_tier="mid",
            price_range_cn="600-1500",
            styles=["优雅", "简约", "成熟"],
            description="英国经典鞋履品牌，舒适与优雅并重",
            target_audience="职场女性，追求舒适和品质",
            best_for=["职场通勤", "日常优雅", "长时间行走"],
            reasons_template="英国百年鞋履工艺，{styles}风格舒适耐穿",
        ),
        Brand(
            name="ECCO",
            category="鞋履",
            price_tier="mid",
            price_range_cn="800-2000",
            styles=["简约", "优雅", "成熟"],
            description="丹麦舒适鞋履品牌，北欧简约设计",
            target_audience="追求舒适和品质的都市人群",
            best_for=["职场", "日常", "旅行"],
            reasons_template="北欧舒适设计，{styles}风格久走不累",
        ),
        Brand(
            name="Coach",
            category="包袋",
            price_tier="mid",
            price_range_cn="1500-6000",
            styles=["优雅", "成熟", "简约"],
            description="美国轻奢皮具品牌，经典耐用",
            target_audience="职场女性，追求品质包袋",
            best_for=["职场", "日常", "送礼"],
            reasons_template="美国轻奢皮具经典，{styles}风格实用百搭",
        ),
        Brand(
            name="Michael Kors",
            category="包袋/服装",
            price_tier="mid",
            price_range_cn="1500-5000",
            styles=["优雅", "成熟", "简约", "华丽"],
            description="美国轻奢品牌，现代都市风格",
            target_audience="都市职业女性",
            best_for=["职场", "商务", "日常精致"],
            reasons_template="美式现代轻奢，{styles}风格气场十足",
        ),

        # === Premium Tier (高收入) ===
        Brand(
            name="Max Mara",
            category="服装",
            price_tier="premium",
            price_range_cn="5000-30000",
            styles=["优雅", "成熟", "简约", "华丽"],
            description="意大利高端大衣品牌，经典永恒",
            target_audience="高收入职业女性，追求经典",
            best_for=["商务", "重要场合", "投资型购买"],
            reasons_template="意大利经典大衣之王，{styles}风格一件永恒",
        ),
        Brand(
            name="Theory",
            category="服装",
            price_tier="premium",
            price_range_cn="1500-6000",
            styles=["简约", "优雅", "成熟"],
            description="美国高端职场装，精准剪裁",
            target_audience="高管、专业人士",
            best_for=["高端职场", "商务谈判", "正式场合"],
            reasons_template="美国精英职场装，{styles}风格剪裁精准利落",
        ),
        Brand(
            name="Vince",
            category="服装",
            price_tier="premium",
            price_range_cn="1500-5000",
            styles=["简约", "优雅", "成熟"],
            description="美国极简奢华品牌，面料顶级",
            target_audience="追求低调奢华的高收入人群",
            best_for=["日常奢华", "极简风格", "品质生活"],
            reasons_template="美国极简奢华，{styles}风格面料顶级触感",
        ),
        Brand(
            name="Stuart Weitzman",
            category="鞋履",
            price_tier="premium",
            price_range_cn="3000-6000",
            styles=["优雅", "成熟", "性感", "简约"],
            description="美国高端鞋履品牌，明星红毯之选",
            target_audience="高收入女性，追求品质鞋履",
            best_for=["重要场合", "红毯", "高端约会"],
            reasons_template="明星红毯御用，{styles}风格高级耐穿",
        ),
        Brand(
            name="Tory Burch",
            category="包袋/服装/鞋履",
            price_tier="premium",
            price_range_cn="2000-8000",
            styles=["优雅", "活泼", "成熟"],
            description="美式生活方式品牌，休闲优雅",
            target_audience="中高收入的成熟女性",
            best_for=["日常精致", "度假", "休闲商务"],
            reasons_template="美式休闲优雅，{styles}风格彰显生活品味",
        ),

        # === Luxury Tier (超高收入) ===
        Brand(
            name="Chanel",
            category="包袋/服装/鞋履",
            price_tier="luxury",
            price_range_cn="30000-100000+",
            styles=["优雅", "成熟", "华丽", "简约"],
            description="法国顶级奢侈品牌，永恒经典",
            target_audience="超高收入人群，追求极致品质",
            best_for=["所有重要场合", "投资收藏", "身份象征"],
            reasons_template="法国顶级奢侈，{styles}风格一件传家",
        ),
        Brand(
            name="Hermes",
            category="包袋/配饰",
            price_tier="luxury",
            price_range_cn="50000-200000+",
            styles=["优雅", "成熟", "华丽", "简约"],
            description="法国顶级奢侈品牌，手工皮具之王",
            target_audience="超高净值人群",
            best_for=["顶级场合", "收藏投资", "传承"],
            reasons_template="手工皮具之巅，{styles}风格百年传承",
        ),
        Brand(
            name="Ralph Lauren (紫标/黑标)",
            category="服装",
            price_tier="luxury",
            price_range_cn="5000-50000",
            styles=["优雅", "成熟", "简约", "华丽"],
            description="美式奢华生活品牌，老钱风代表",
            target_audience="超高收入人群，追求经典美式风格",
            best_for=["正式场合", "马术", "高端社交"],
            reasons_template="美式老钱风代表，{styles}风格彰显底蕴",
        ),
        Brand(
            name="Manolo Blahnik",
            category="鞋履",
            price_tier="luxury",
            price_range_cn="5000-15000",
            styles=["优雅", "成熟", "性感", "华丽"],
            description="英国顶级鞋履品牌，《欲望都市》经典",
            target_audience="超高收入女性，鞋履收藏家",
            best_for=["婚礼", "红毯", "重要晚宴"],
            reasons_template="顶级鞋履艺术，{styles}风格方扣经典永恒",
        ),
        Brand(
            name="Christian Louboutin",
            category="鞋履",
            price_tier="luxury",
            price_range_cn="5000-12000",
            styles=["性感", "华丽", "成熟", "优雅"],
            description="法国红底鞋，性感代名词",
            target_audience="追求性感奢华的高收入女性",
            best_for=["派对", "约会", "重要场合"],
            reasons_template="红底鞋性感传奇，{styles}风格每一步都是焦点",
        ),
        Brand(
            name="Gucci",
            category="包袋/服装/鞋履",
            price_tier="luxury",
            price_range_cn="15000-80000",
            styles=["华丽", "性感", "活泼", "成熟"],
            description="意大利奢侈品牌，复古华丽风格",
            target_audience="高收入时尚人群",
            best_for=["时尚场合", "派对", "潮流穿搭"],
            reasons_template="意大利复古华丽，{styles}风格摩登复古",
        ),
        Brand(
            name="Prada",
            category="包袋/服装/鞋履",
            price_tier="luxury",
            price_range_cn="15000-60000",
            styles=["简约", "优雅", "成熟", "华丽"],
            description="意大利顶级奢侈品牌，知识分子风",
            target_audience="高收入文化人群",
            best_for=["高端职场", "文化场合", "投资购买"],
            reasons_template="意大利知识分子风，{styles}风格低调有内涵",
        ),
        Brand(
            name="Dior",
            category="包袋/服装/鞋履",
            price_tier="luxury",
            price_range_cn="20000-80000",
            styles=["优雅", "华丽", "成熟", "性感"],
            description="法国顶级奢侈品牌，法式优雅巅峰",
            target_audience="超高收入女性",
            best_for=["顶级场合", "时装秀", "重要社交"],
            reasons_template="法式优雅巅峰，{styles}风格优雅入骨",
        ),
    ]

    @classmethod
    def get_by_price_tier(cls, tier: str) -> List[Brand]:
        """Get brands by price tier"""
        return [b for b in cls.BRANDS if b.price_tier == tier]

    @classmethod
    def get_by_style(cls, styles: List[str]) -> List[Brand]:
        """Get brands matching given styles"""
        matched = []
        for brand in cls.BRANDS:
            if any(s in brand.styles for s in styles):
                matched.append(brand)
        return matched

    @classmethod
    def get_by_category(cls, category: str) -> List[Brand]:
        """Get brands by category"""
        return [b for b in cls.BRANDS if category.lower() in b.category.lower()]

    @classmethod
    def recommend(
        cls,
        income_level: str,
        styles: List[str],
        categories: List[str] = None,
        limit: int = 3
    ) -> List[Dict]:
        """
        Generate brand recommendations based on income and style preferences
        """
        # Map income level to price tier
        income_tier_map = {
            "3000以下（学生/实习）": ["budget"],
            "3000-5000": ["budget"],
            "5000-8000": ["budget", "mid"],
            "8000-12000": ["mid"],
            "12000-20000": ["mid", "premium"],
            "20000-30000": ["premium"],
            "30000-50000": ["premium", "luxury"],
            "50000以上（高收入）": ["luxury"],
        }

        allowed_tiers = income_tier_map.get(income_level, ["budget", "mid"])

        # Filter by tier and styles
        candidates = []
        for brand in cls.BRANDS:
            if brand.price_tier in allowed_tiers:
                # Calculate style match score
                matching_styles = [s for s in styles if s in brand.styles]
                if matching_styles:
                    score = len(matching_styles) / max(len(styles), len(brand.styles))
                    candidates.append((brand, matching_styles, score))

        # Sort by score (descending) and tier priority
        tier_priority = {"luxury": 4, "premium": 3, "mid": 2, "budget": 1}
        candidates.sort(
            key=lambda x: (x[2], tier_priority.get(x[0].price_tier, 0)),
            reverse=True
        )

        # Diversify categories
        selected = []
        used_categories = set()

        for brand, matching_styles, score in candidates:
            if len(selected) >= limit:
                break
            # Try to pick different categories
            if categories and brand.category not in used_categories:
                selected.append({
                    "brand": brand,
                    "matching_styles": matching_styles,
                    "reason": brand.reasons_template.format(
                        styles="、".join(matching_styles)
                    ),
                })
                used_categories.add(brand.category)
            elif not categories:
                selected.append({
                    "brand": brand,
                    "matching_styles": matching_styles,
                    "reason": brand.reasons_template.format(
                        styles="、".join(matching_styles)
                    ),
                })

        # If we don't have enough, fill with top scored
        if len(selected) < limit:
            for brand, matching_styles, score in candidates:
                if len(selected) >= limit:
                    break
                if not any(s["brand"].name == brand.name for s in selected):
                    selected.append({
                        "brand": brand,
                        "matching_styles": matching_styles,
                        "reason": brand.reasons_template.format(
                            styles="、".join(matching_styles)
                        ),
                    })

        return selected[:limit]


# Occupation style mapping
OCCUPATION_STYLE_MAP = {
    "学生": ["可爱", "清纯", "活泼", "简约"],
    "教师": ["优雅", "简约", "成熟", "清纯"],
    "医生/护士": ["简约", "优雅", "成熟"],
    "律师": ["优雅", "成熟", "简约"],
    "金融从业者": ["优雅", "成熟", "简约", "华丽"],
    "程序员/工程师": ["简约", "活泼", "清纯"],
    "设计师": ["活泼", "简约", "优雅", "性感"],
    "销售": ["优雅", "成熟", "活泼", "华丽"],
    "市场营销": ["活泼", "优雅", "成熟"],
    "行政/文员": ["简约", "优雅", "清纯"],
    "自由职业": ["活泼", "简约", "可爱"],
    "企业高管": ["华丽", "优雅", "成熟", "简约"],
    "创业者": ["简约", "优雅", "成熟"],
    "其他": ["简约", "优雅"],
}

OCCUPATIONS = list(OCCUPATION_STYLE_MAP.keys())
