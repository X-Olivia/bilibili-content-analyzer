# B站内容分析工具

这是一个通用的B站（哔哩哔哩）内容数据分析工具，默认用于分析"执行力"相关视频内容，但可以轻松配置为分析任何话题。通过收集和分析指定时间范围内的相关视频数据，深度洞察话题的热门程度变化、观众态度转变以及内容关注点的演进。

## 核心特色

### 高度可配置
- 支持任意关键词和话题分析
- 灵活的时间范围设置
- 可自定义分析参数和可视化样式

### 主要功能
- **智能数据采集**: 使用B站官方API批量采集视频数据
- **多维度分析**: 时间趋势、情感态度、内容主题、参与度等
- **丰富可视化**: 静态图表、交互式仪表板、词云图等
- **完整报告**: JSON、CSV、Excel格式的详细分析报告

### 分析维度
- **时间趋势**: 年度、季度、月度发布量和播放量变化
- **情感分析**: 积极、中性、消极态度分布和变化  
- **内容主题**: 关键词云图、热门标签、主题演进
- **参与度**: 点赞、投币、收藏、分享等互动数据分析
- **创作者**: 最活跃和最具影响力的内容创作者分析

##  快速开始

### 环境要求
- Python 3.8+
- 网络连接（用于访问B站API）

### 安装依赖
```bash
pip install -r requirements.txt
```

### 运行分析

#### 使用Python模块（推荐）
```bash
# 安装为可编辑包
pip install -e .

# 运行完整分析流程
bilibili-analyzer

# 或者分步执行
bilibili-analyzer --mode collect    # 仅数据采集
bilibili-analyzer --mode analyze    # 仅数据分析
bilibili-analyzer --mode visualize  # 仅生成图表

# 强制重新采集数据
bilibili-analyzer --force-recollect

# 使用自定义配置文件
bilibili-analyzer --config custom_config.py

# 详细日志输出
bilibili-analyzer --verbose
```

#### 直接运行脚本
```bash
# 从src目录运行
cd src
python -m bilibili_analyzer.main

# 或使用主程序文件
python src/bilibili_analyzer/main.py
```

## 项目结构

```
bilibili/
├── src/                          # 源代码目录
│   └── bilibili_analyzer/        # 主包
│       ├── __init__.py
│       ├── main.py              # 主程序入口
│       ├── cli.py               # 命令行接口
│       ├── config.py            # 配置文件
│       ├── data_collector.py    # 数据采集模块
│       ├── data_analyzer.py     # 数据分析模块
│       ├── visualizer.py        # 数据可视化模块
│       └── font_utils.py        # 字体工具模块
├── data/                         # 数据目录
│   ├── raw/                     # 原始数据（按关键词分文件）
│   │   ├── all_videos_data.csv  # 合并的原始数据
│   │   ├── 执行力_data.csv       # 各关键词的原始数据
│   │   └── ...                  
│   └── processed/               # 处理后数据
│       └── enhanced_videos_data.csv # 增强的视频数据
├── output/                      # 输出结果目录
│   ├── charts/                  # 图表文件
│   │   ├── growth_analysis.png
│   │   ├── sentiment_analysis_detailed.png
│   │   ├── time_trends_detailed.png
│   │   ├── wordcloud_analysis.png
│   │   └── interactive_dashboard.html
│   ├── analysis_report.json     # 详细分析报告
│   ├── analyzed_data.csv        # 分析数据（CSV格式）
│   └── analyzed_data.xlsx       # 分析数据（Excel格式，多工作表）
├── logs/                        # 日志文件
│   ├── main.log                # 主程序日志
│   ├── collector.log           # 数据采集日志
│   ├── analyzer.log            # 数据分析日志
│   └── visualizer.log          # 可视化日志
├── tests/                       # 测试文件
├── docs/                        # 文档目录
├── examples/                    # 示例文件
├── requirements.txt             # 项目依赖
├── pyproject.toml              # 项目配置文件
├── LICENSE                     # 许可证
└── README.md                   # 项目说明
```

## 输出文件说明

### 数据文件
- `analyzed_data.csv`: 完整的分析数据（CSV格式）
- `analyzed_data.xlsx`: 分析数据Excel文件（包含分年度工作表）
- `analysis_report.json`: 详细的JSON格式分析报告

### 图表文件
- `time_trends.png`: 时间趋势分析图
- `sentiment_analysis.png`: 情感态度分析图
- `content_analysis.png`: 内容主题分析图
- `engagement_analysis.png`: 参与度分析图
- `author_analysis.png`: 作者影响力分析图
- `wordcloud.png`: 关键词云图
- `interactive_dashboard.html`: 交互式仪表板

## 配置说明

### 如何修改分析话题

本工具最大的优势是可以轻松配置为分析任何话题。只需修改配置文件即可：

#### 1. 修改搜索关键词

编辑 `src/bilibili_analyzer/config.py` 文件中的 `SEARCH_KEYWORDS` 列表：

```python
# 示例：分析"人工智能"话题
SEARCH_KEYWORDS = [
    '人工智能',
    'AI技术',
    '机器学习',
    '深度学习',
    '神经网络',
    'ChatGPT',
    'AI应用',
    '智能算法',
    '自动化',
    '机器人'
]

# 示例：分析"投资理财"话题  
SEARCH_KEYWORDS = [
    '投资理财',
    '股票投资',
    '基金理财',
    '财务管理',
    '理财规划',
    '投资策略',
    '资产配置',
    '金融知识',
    '价值投资',
    '财富自由'
]

# 示例：分析"健身减肥"话题
SEARCH_KEYWORDS = [
    '健身',
    '减肥',
    '瘦身',
    '锻炼',
    '健身房',
    '瑜伽',
    '跑步',
    '增肌',
    '塑形',
    '健康生活'
]
```

#### 2. 调整时间范围

```python
DATE_RANGE = {
    'start_year': 2020,        # 开始年份
    'end_year': 2024,          # 结束年份
    'start_timestamp': 1577808000,  # 2020-01-01 00:00:00
    'end_timestamp': 1704067200     # 2024-01-01 00:00:00
}
```

#### 3. 高级配置选项

```python
# 分析配置
ANALYSIS_CONFIG = {
    'sentiment_threshold': {
        'positive': 0.6,        # 积极情感阈值
        'negative': -0.1        # 消极情感阈值
    },
    'min_video_duration': 60,   # 最小视频时长（秒）
    'max_results_per_keyword': 1000,  # 每个关键词最大结果数
    'request_delay': 1,         # API请求间隔（秒）
    'batch_size': 50           # 批处理大小
}

# 可视化配置
VISUALIZATION_CONFIG = {
    'figure_size': (12, 8),     # 图表尺寸
    'font_family': 'SimHei',    # 中文字体
    'color_palette': 'viridis', # 颜色方案
    'wordcloud_config': {       # 词云配置
        'width': 800,
        'height': 400,
        'max_words': 100,
        'colormap': 'viridis'
    }
}
```

### 默认配置（执行力话题）

项目默认分析"执行力"相关内容，包含以下关键词：
- 执行力、执行力培训、执行力管理、团队执行力
- 提高执行力、执行力差、执行力强、执行力不足  
- 执行能力、执行方法、高效执行、落地执行
- 执行思维、执行技巧、执行文化

默认时间范围：2019年1月1日 - 2025年12月31日

## 实际应用场景

### 内容创作者
- **热点追踪**: 发现话题的热门趋势和最佳发布时机
- **内容策划**: 分析受欢迎的内容主题和关键词
- **竞品分析**: 了解同类型创作者的内容策略

### 品牌营销
- **市场洞察**: 分析目标用户对品牌相关话题的关注度
- **营销策略**: 确定最佳的内容营销方向和投放时机
- **舆情监控**: 跟踪品牌话题的情感变化趋势

### 学术研究
- **社会趋势**: 研究网络文化和社会话题的演变
- **用户行为**: 分析视频平台用户的内容偏好
- **传播效果**: 研究不同类型内容的传播规律

### 行业分析
- **市场研究**: 了解特定行业在B站的发展状况
- **趋势预测**: 基于历史数据预测话题发展趋势
- **用户画像**: 分析目标用户群体的兴趣特征

## 使用示例

### 示例1：分析"编程教育"话题

```bash
# 1. 修改配置文件
# 编辑 src/bilibili_analyzer/config.py
SEARCH_KEYWORDS = [
    'Python教程', 'Java编程', '前端开发', 'Vue教程', 
    'React学习', '算法入门', '数据结构', '编程基础'
]

# 2. 运行分析
bilibili-analyzer --force-recollect

# 3. 查看结果
# - 了解编程教育内容的年度增长趋势
# - 发现最受欢迎的编程语言和技术
# - 分析学习者的情感反馈和参与度
```

### 示例2：分析"美食制作"话题

```bash
# 配置关键词
SEARCH_KEYWORDS = [
    '美食制作', '烘焙教程', '家常菜', '甜品制作',
    '料理技巧', '食谱分享', '厨房技巧', '美食测评'
]

# 分析结果将显示：
# - 不同美食类型的热门程度变化
# - 观众对各类美食内容的偏好
# - 美食视频的最佳发布时间和参与度规律
```

### 示例3：分析"健身运动"话题

```bash
# 配置关键词
SEARCH_KEYWORDS = [
    '健身教程', '瑜伽练习', '跑步指南', '力量训练',
    '减脂增肌', '健身房', '居家锻炼', '运动营养'
]

# 可以获得：
# - 健身内容的季节性变化规律
# - 不同运动类型的受欢迎程度
# - 健身视频创作者的影响力分析
```

## 分析结果示例

### 数据概览
- **时间跨度**: 2019-2025年执行力话题发展轨迹
- **数据规模**: 15个关键词，10,000+视频数据
- **创作者**: 800+活跃UP主，涵盖商业、教育、职场等分区

### 核心发现
- **内容增长**: 执行力相关视频年均增长35%
- **情感分布**: 积极内容占68%，中性25%，消极7%
- **热门时段**: 工作日晚间8-10点发布效果最佳
- **参与度**: 实用技巧类视频平均点赞率最高(8.5%)

### 趋势洞察
- **2019-2020**: 基础概念普及期，理论内容占主导
- **2021-2022**: 实践应用爆发期，案例分享激增
- **2023-2025**: 个性化定制期，细分场景内容增多

### 内容特征
- **热门关键词**: "提高执行力"、"执行方法"、"团队管理"
- **优质特征**: 时长3-8分钟，结构化内容，实用性强
- **创作者类型**: 企业培训师(35%)、职场博主(28%)、管理顾问(25%)

## 技术栈

- **数据采集**: requests, aiohttp
- **数据处理**: pandas, numpy
- **中文分词**: jieba
- **情感分析**: snownlp, textblob
- **静态图表**: matplotlib, seaborn
- **交互图表**: plotly
- **词云生成**: wordcloud
- **数据存储**: CSV, Excel, JSON

## 快速入门指南

### 30秒快速体验

```bash
# 1. 克隆项目
git clone https://github.com/your-repo/bilibili-content-analyzer.git
cd bilibili-content-analyzer

# 2. 安装依赖
pip install -r requirements.txt

# 3. 安装项目（推荐）
pip install -e .

# 4. 运行分析（使用默认配置）
bilibili-analyzer

# 5. 查看结果
# 结果将保存在 output/ 目录下
# 打开 output/charts/interactive_dashboard.html 查看交互式报告
```

### 自定义话题分析

```bash
# 1. 复制配置文件
cp src/bilibili_analyzer/config.py my_custom_config.py

# 2. 修改关键词（以分析"美食"话题为例）
# 编辑 my_custom_config.py
SEARCH_KEYWORDS = [
    '美食制作', '烘焙教程', '家常菜', '甜品制作',
    '料理技巧', '食谱分享', '厨房技巧', '美食测评',
    '中式料理', '西式料理'
]

# 3. 使用自定义配置运行
bilibili-analyzer --config my_custom_config.py --force-recollect

# 4. 等待完成并查看结果
```

## 故障排除

### 常见问题及解决方案

#### 问题1：无法安装依赖包

```bash
# 解决方案：升级pip并使用国内镜像
python -m pip install --upgrade pip
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

#### 问题2：中文字体显示为方块

```bash
# 解决方案1：安装中文字体（macOS）
# 系统已有字体，检查配置文件中的字体设置

# 解决方案2：手动指定字体路径
# 在config.py中设置：
VISUALIZATION_CONFIG['font_family'] = '/System/Library/Fonts/Arial Unicode MS.ttf'
```

#### 问题3：API请求失败

```bash
# 解决方案：检查网络连接和请求频率
# 1. 确保网络连接正常
# 2. 增加请求间隔时间（在config.py中设置）
ANALYSIS_CONFIG['request_delay'] = 2  # 增加到2秒

# 3. 减少单次请求数据量
ANALYSIS_CONFIG['max_results_per_keyword'] = 500
```

#### 问题4：内存不足

```bash
# 解决方案：减少批处理大小
# 在config.py中设置：
ANALYSIS_CONFIG['batch_size'] = 25  # 减少批处理大小
```

#### 问题5：没有生成图表

```bash
# 解决方案：检查输出目录权限
chmod 755 output/
mkdir -p output/charts

# 重新运行可视化模块
bilibili-analyzer --mode visualize
```

### 调试模式

```bash
# 启用详细日志
bilibili-analyzer --verbose

# 检查配置而不执行
bilibili-analyzer --dry-run

# 查看日志文件
tail -f logs/main.log
```

### 获取帮助

```bash
# 查看所有可用选项
bilibili-analyzer --help

# 查看版本信息
bilibili-analyzer --version
```

## 注意事项

### 重要提醒

1. **API限制**: 
   - 严格遵守B站API使用规范和频率限制
   - 项目已设置合理的请求间隔，请勿随意缩短
   - 大量数据采集可能触发反爬限制，建议分批进行

2. **数据采集时间**: 
   - 完整数据采集可能需要30分钟至数小时
   - 采集时长取决于关键词数量和每个关键词的结果数
   - 建议在网络稳定且无需频繁使用电脑时运行

3. **系统资源**: 
   - 数据分析过程会占用一定内存和CPU资源
   - 建议在配置较好的设备上运行大规模分析
   - 可通过调整批处理大小来控制资源占用

4. **数据存储**: 
   - 原始数据和分析结果会占用磁盘空间
   - 定期清理不需要的历史数据文件
   - 重要分析结果建议备份到云存储

5. **法律合规**: 
   - 本工具仅用于学习研究和个人分析用途
   - 请勿用于商业用途或恶意数据采集
   - 使用时请遵守相关法律法规和平台服务条款

## 贡献

欢迎提交问题报告和功能请求。如果您想贡献代码，请：

1. Fork 本项目
2. 创建您的功能分支
3. 提交您的更改
4. 推送到分支
5. 创建 Pull Request

