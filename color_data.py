# -*- coding: utf-8 -*-
"""
Seasonal Color Palette Data Module
Contains curated color palettes for Spring, Summer, Autumn, and Winter
following the principles of seasonal color theory.
"""

from dataclasses import dataclass
from typing import List, Dict, Tuple


@dataclass
class SeasonColor:
    """Represents a single color in the seasonal palette"""
    id: str
    name: str
    hex_value: str
    description: str = ""


class SeasonalPalettes:
    """Complete seasonal color collection"""

    SPRING = [
        SeasonColor("SP01", "珊瑚粉", "#F4A198", "温暖甜美的春日花粉"),
        SeasonColor("SP02", "蜜桃橘", "#F8B88B", "活力满满的成熟蜜桃"),
        SeasonColor("SP03", "杏色", "#FDD9B5", "柔和自然的杏桃果香"),
        SeasonColor("SP04", "鹅黄色", "#F3E5AB", "明媚清新的初春嫩芽"),
        SeasonColor("SP05", "薄荷绿", "#98FF98", "清透自然的薄荷清新"),
        SeasonColor("SP06", "春芽绿", "#A8E6CF", "生机勃勃的新叶翠绿"),
        SeasonColor("SP07", "婴儿蓝", "#89CFF0", "澄澈明朗的天空蓝"),
        SeasonColor("SP08", "淡紫藤", "#C8A2C8", "浪漫优雅的紫藤花海"),
        SeasonColor("SP09", "樱花粉", "#FFB7C5", "柔美娇嫩的樱花飞舞"),
        SeasonColor("SP10", "奶油白", "#FFFDD0", "温润柔和的奶油质感"),
        SeasonColor("SP11", "浅驼色", "#D2B48C", "自然温暖的沙滩驼色"),
        SeasonColor("SP12", "玫瑰金", "#B76E79", "精致时尚的玫瑰金属"),
    ]

    SUMMER = [
        SeasonColor("SU01", "冰蓝色", "#A5F2F3", "清凉透彻的冰川水滴"),
        SeasonColor("SU02", "天空蓝", "#87CEEB", "万里晴空的澄澈天蓝"),
        SeasonColor("SU03", "海水蓝", "#5F9EA0", "深邃宁静的海滨湖水"),
        SeasonColor("SU04", "薄荷青", "#7FFFD4", "清爽宜人的薄荷凉意"),
        SeasonColor("SU05", "薰衣草紫", "#E6E6FA", "梦幻优雅的薰衣草田"),
        SeasonColor("SU06", "淡粉紫", "#DDA0DD", "温柔甜美的暮霭粉紫"),
        SeasonColor("SU07", "珍珠白", "#F0EAD6", "光泽温润的珍珠质感"),
        SeasonColor("SU08", "银灰色", "#C0C0C0", "高级清冷的金属光泽"),
        SeasonColor("SU09", "浅灰蓝", "#B0C4DE", "柔和淡雅的灰调天空"),
        SeasonColor("SU10", "水绿色", "#9ED9C0", "清透水润的碧波荡漾"),
        SeasonColor("SU11", "冷粉色", "#F0B8C8", "清新不甜腻的冷调粉"),
        SeasonColor("SU12", "雾紫色", "#B8A9C9", "朦胧神秘的雾霭紫调"),
    ]

    AUTUMN = [
        SeasonColor("AU01", "焦糖棕", "#C68E53", "温暖醇厚的焦糖甜香"),
        SeasonColor("AU02", "南瓜橘", "#E8913A", "丰收喜悦的南瓜暖橘"),
        SeasonColor("AU03", "枫叶红", "#C83C23", "浓烈绚烂的深秋枫叶"),
        SeasonColor("AU04", "酒红色", "#722F37", "醇厚优雅的红酒沉淀"),
        SeasonColor("AU05", "芥末黄", "#C7A33E", "复古知性的芥末浓郁"),
        SeasonColor("AU06", "橄榄绿", "#808000", "沉稳自然的橄榄成熟"),
        SeasonColor("AU07", "深金色", "#B8860B", "奢华耀眼的深秋金辉"),
        SeasonColor("AU08", "砖红色", "#B22222", "质朴温暖的砖墙色泽"),
        SeasonColor("AU09", "巧克力棕", "#7B3F00", "浓郁丝滑的巧克力深棕"),
        SeasonColor("AU10", "卡其色", "#C3B091", "经典百搭的自然卡其"),
        SeasonColor("AU11", "赤陶色", "#E2725B", "古朴质感的陶土暖红"),
        SeasonColor("AU12", "苔藓绿", "#8FBC8F", "静谧沉稳的苔藓深绿"),
    ]

    WINTER = [
        SeasonColor("WI01", "正红色", "#DC143C", "明艳夺目的纯正中国红"),
        SeasonColor("WI02", "宝石蓝", "#0F52BA", "深邃璀璨的蓝宝石光"),
        SeasonColor("WI03", "藏青色", "#000080", "沉稳大气的深夜藏蓝"),
        SeasonColor("WI04", "墨绿色", "#013220", "神秘深邃的墨玉翠绿"),
        SeasonColor("WI05", "深紫色", "#4B0082", "高贵神秘的紫罗兰深"),
        SeasonColor("WI06", "纯黑色", "#1A1A1A", "经典永恒的极致纯黑"),
        SeasonColor("WI07", "纯白色", "#FAFAFA", "纯净无瑕的皑皑白雪"),
        SeasonColor("WI08", "银白色", "#E8E8E8", "冷冽闪耀的冰霜银白"),
        SeasonColor("WI09", "冰灰色", "#A9A9A9", "冷静理性的冰晶灰调"),
        SeasonColor("WI10", "玫红色", "#C71585", "鲜艳热烈的玫瑰绽放"),
        SeasonColor("WI11", "青色", "#008B8B", "清冽独特的深青色调"),
        SeasonColor("WI12", "紫罗兰", "#8B00FF", "浓郁华丽的紫罗兰电光"),
    ]

    SEASONS = {
        "spring": {
            "name": "春",
            "subtitle": "Spring Collection",
            "description": "万物复苏，温暖清新的浅暖色调",
            "icon": "🌸",
            "colors": SPRING,
            "gradient": ["#FFF5F5", "#FFEBE0"],
        },
        "summer": {
            "name": "夏",
            "subtitle": "Summer Collection",
            "description": "清凉舒适，通透自然的冷浅色调",
            "icon": "🌊",
            "colors": SUMMER,
            "gradient": ["#F0F8FF", "#E6F3FF"],
        },
        "autumn": {
            "name": "秋",
            "subtitle": "Autumn Collection",
            "description": "硕果累累，醇厚浓郁的暖深色调",
            "icon": "🍁",
            "colors": AUTUMN,
            "gradient": ["#FFF8F0", "#FFF0E0"],
        },
        "winter": {
            "name": "冬",
            "subtitle": "Winter Collection",
            "description": "纯净冷冽，鲜明浓烈的冷深色调",
            "icon": "❄️",
            "colors": WINTER,
            "gradient": ["#F5F5F5", "#EBEBEB"],
        },
    }

    @classmethod
    def get_season(cls, season_key: str) -> Dict:
        """Get season data by key"""
        return cls.SEASONS.get(season_key, {})

    @classmethod
    def get_all_colors(cls) -> List[SeasonColor]:
        """Get all colors across all seasons"""
        all_colors = []
        for season in cls.SEASONS.values():
            all_colors.extend(season["colors"])
        return all_colors

    @classmethod
    def get_color_by_id(cls, color_id: str) -> SeasonColor:
        """Find a color by its ID"""
        for color in cls.get_all_colors():
            if color.id == color_id:
                return color
        return None

    @classmethod
    def get_color_suggestions_for_scene(cls, scene: str) -> List[str]:
        """Get color suggestions for common scenes"""
        scene_lower = scene.lower()
        suggestions = {
            "面试": ["WI06", "WI07", "WI09", "SU08", "SP10"],
            "上课": ["SU04", "SU07", "SP05", "SU10", "SP02"],
            "美术馆": ["WI07", "SU07", "WI09", "SU12", "WI06"],
            "海边": ["SU02", "SU01", "SP07", "SU10", "SU07"],
            "逛街": ["SP09", "SP01", "SU06", "SP12", "WI10"],
            "约会": ["SP01", "WI10", "SU06", "SP09", "SP12"],
            "运动": ["SU04", "SP05", "SU01", "SU10", "WI07"],
            "聚会": ["WI01", "WI10", "SP01", "AU03", "WI12"],
            "旅行": ["SP06", "SU02", "SP03", "AU10", "SU07"],
        }
        for key, colors in suggestions.items():
            if key in scene_lower:
                return colors
        return []


# Common outfit scene templates
SCENE_TEMPLATES = [
    "去参加面试",
    "下雨天去上课",
    "美术馆看展",
    "去海边骑车",
    "去商场逛街",
    "周末约会",
    "朋友聚会",
    "户外运动",
    "短途旅行",
    "图书馆自习",
    "咖啡馆写作",
    "正式晚宴",
    "日常通勤",
    "拍照打卡",
    "音乐节",
]

# Style keywords for multi-select
STYLE_KEYWORDS = [
    "华丽", "简约", "优雅", "活泼",
    "成熟", "可爱", "性感", "清纯",
    "保暖", "清凉",
]

# Income levels
INCOME_LEVELS = [
    "3000以下（学生/实习）",
    "3000-5000",
    "5000-8000",
    "8000-12000",
    "12000-20000",
    "20000-30000",
    "30000-50000",
    "50000以上（高收入）",
]
