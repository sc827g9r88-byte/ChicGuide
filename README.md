# ChicGuide 穿搭顾问

一个专为女性打造的智能穿搭建议桌面软件，基于 Python + PySide6 开发，支持 AI 大模型驱动的场景穿搭建议和品牌推荐功能。

## 功能概览

### 1. 四季色卡
- 春、夏、秋、冬四季色彩灵感库
- 每季 12 款精选颜色，配有编号和名称
- 颜色按色调渐变排序，相邻颜色彼此协调
- 点击季节标签即可切换浏览

**春季**：暖色浅色系（珊瑚粉、蜜桃橘、杏色、鹅黄、薄荷绿等）  
**夏季**：冷色浅色系（冰蓝、天空蓝、海水蓝、薰衣草紫、珍珠白等）  
**秋季**：暖色深色系（焦糖棕、南瓜橘、枫叶红、酒红、芥末黄等）  
**冬季**：冷色深色系（正红、宝石蓝、藏青、墨绿、纯黑、纯白等）

### 2. 场合穿搭顾问（AI 驱动）
- 输入出行场景（如"去参加面试"、"下雨天去上课"等）
- AI 为你生成 1-2 套完整搭配方案
- 每套方案从色彩、款式、风格、场合逻辑四个维度分析
- 支持选择季节和风格偏好进行更精准的推荐
- 提供 15 个常见场景快捷标签

### 3. 品牌选购指南
- 根据职业、月薪/可支配收入、穿搭风格智能推荐 2-3 个服装品牌
- 内置 29 个品牌数据库，覆盖快时尚到奢侈品：
  - 平价层：优衣库、ZARA、H&M、热风、天美意、Charles & Keith
  - 中端层：COS、Massimo Dutti、Sandro、Maje、Coach、MK
  - 高端层：Max Mara、Theory、Stuart Weitzman
  - 奢侈层：Chanel、Hermes、Ralph Lauren、Manolo Blahnik、Christian Louboutin
- 支持对推荐结果进行反馈调整
- 可向 AI 咨询更个性化的品牌推荐

### 4. AI API 支持
- 支持主流大模型 API：OpenAI (GPT-4o/4o-mini)、通义千问 (Qwen)、Kimi (Moonshot)、DeepSeek
- 自定义 API Base URL 支持其他兼容 OpenAI 格式的模型
- API Key 安全存储在本地配置文件
- 支持 Temperature 参数调节 AI 创造性

## 安装与运行

### 环境要求
- Python 3.8+
- PySide6
- requests

### 安装步骤

1. 克隆或下载本项目：
```bash
cd fashion-advisor
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 运行应用：
```bash
python main.py
```

### 首次使用

1. 点击左侧边栏底部的「API 设置」
2. 选择你要使用的 AI 提供商（OpenAI / 通义千问 / Kimi / DeepSeek / 自定义）
3. 输入你的 API Key
4. 点击「测试连接」验证配置
5. 点击「保存」完成设置

配置完成后即可使用「场合穿搭顾问」和「品牌选购指南」中的 AI 功能。

## 项目结构

```
fashion-advisor/
    main.py              # 主程序入口，UI 界面
    color_data.py        # 四季色卡数据
    brand_data.py        # 品牌推荐数据库
    ai_client.py         # AI API 统一客户端
    requirements.txt     # Python 依赖
    README.md            # 项目说明
```

## 使用示例

### 场景穿搭
- 场景："去参加面试"
- AI 输出：推荐黑白灰简约搭配，从色彩、款式、风格、场合逻辑四方面解析

- 场景："下雨天去上课"
- AI 输出：建议加入雨具，选择清新简约自然的颜色款式

- 场景："美术馆看展"
- AI 输出：推荐优雅成熟有设计感的款式，基础色系点缀金属饰品

### 品牌推荐
- 职业：投行从业者 / 收入：6万 / 风格：优雅、成熟、简约
- 推荐：Chanel 手袋 + Ralph Lauren 紫标服装 + Manolo Blahnik 鞋履

- 职业：学生 / 收入：3千 / 风格：简约、清纯、可爱
- 推荐：优衣库 + ZARA + Teenmix 天美意

## API 提供商说明

| 提供商 | 默认 API Base | 模型示例 |
|--------|--------------|----------|
| OpenAI | https://api.openai.com/v1 | gpt-4o, gpt-4o-mini |
| 通义千问 | https://dashscope.aliyuncs.com/compatible-mode/v1 | qwen-turbo, qwen-plus |
| Kimi | https://api.moonshot.cn/v1 | moonshot-v1-8k |
| DeepSeek | https://api.deepseek.com/v1 | deepseek-chat |
| 自定义 | 用户填写 | 用户填写 |

## 技术特性

- 精美女性化 UI 设计，柔粉色调主题
- 侧边栏导航，三个子系统切换
- 多线程 AI 调用，界面不卡顿
- 本地配置文件持久化存储
- 圆角卡片、渐变色、阴影效果等现代 UI 元素
- 响应式布局，适配不同窗口大小
