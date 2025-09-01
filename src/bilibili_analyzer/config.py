"""
配置文件 - B站执行力内容分析项目
"""

# B站搜索API配置
BILIBILI_SEARCH_API = {
    'base_url': 'https://api.bilibili.com/x/web-interface/search/all/v2',
    'search_type_url': 'https://api.bilibili.com/x/web-interface/search/all/v2',
    'video_info_url': 'https://api.bilibili.com/x/web-interface/view',
    'headers': {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.bilibili.com/',
        'Origin': 'https://www.bilibili.com',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"macOS"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Cookie': ''  # 可能需要添加cookie
    }
}

# 搜索关键词配置
SEARCH_KEYWORDS = [
    '执行力',
    '执行力培训',
    '执行力管理',
    '团队执行力',
    '提高执行力',
    '执行力差',
    '执行力强',
    '执行力不足',
    '执行能力',
    '执行方法',
    '高效执行',
    '落地执行',
    '执行思维',
    '执行技巧',
    '执行文化'
]

# 时间范围配置
DATE_RANGE = {
    'start_year': 2019,
    'end_year': 2025,
    'start_timestamp': 1546272000,  # 2019-01-01 00:00:00
    'end_timestamp': 1767225600     # 2026-01-01 00:00:00
}

# 数据存储配置
DATA_STORAGE = {
    'raw_data_dir': 'data/raw',
    'processed_data_dir': 'data/processed',
    'output_dir': 'output',
    'logs_dir': 'logs'
}

# 分析配置
ANALYSIS_CONFIG = {
    'sentiment_threshold': {
        'positive': 0.6,
        'negative': -0.1
    },
    'min_video_duration': 60,    # 最小视频时长（秒）
    'max_results_per_keyword': 1000,  # 每个关键词最大结果数
    'request_delay': 1,          # 请求间隔（秒）
    'batch_size': 50             # 批处理大小
}

# 可视化配置
VISUALIZATION_CONFIG = {
    'figure_size': (12, 8),
    'font_family': 'SimHei',     # 中文字体
    'color_palette': 'viridis',
    'wordcloud_config': {
        'width': 800,
        'height': 400,
        'background_color': 'white',
        'font_path': None,       # 如需要可设置中文字体路径
        'max_words': 100,
        'relative_scaling': 0.5,
        'colormap': 'viridis'
    }
}

# 输出配置
OUTPUT_CONFIG = {
    'report_format': ['html', 'pdf'],
    'chart_format': 'png',
    'excel_output': True,
    'json_output': True
}