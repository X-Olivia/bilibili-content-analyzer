"""
数据分析模块
分析执行力相关内容的趋势、情感态度和关注点变化
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import jieba
import jieba.analyse
from wordcloud import WordCloud
from collections import Counter
import json
import os
from datetime import datetime, timedelta
import re
from typing import Dict, List, Tuple, Optional
import logging
from textblob import TextBlob
from snownlp import SnowNLP
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from .config import DATA_STORAGE, ANALYSIS_CONFIG, VISUALIZATION_CONFIG


class DataAnalyzer:
    """Data analyzer for Bilibili content analysis."""
    
    def __init__(self):
        self.logger = self._setup_logger()
        self._setup_chinese_font()
        self._load_stopwords()
        self._ensure_directories()
    
    def _setup_logger(self) -> logging.Logger:
        """设置日志记录器"""
        logger = logging.getLogger('ExecutionDataAnalyzer')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            log_file = os.path.join(DATA_STORAGE['logs_dir'], 'analyzer.log')
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.INFO)
            
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)
            
        return logger
    
    def _setup_chinese_font(self):
        """设置中文字体"""
        import matplotlib.font_manager as fm
        
        # 尝试找到系统中可用的中文字体
        chinese_fonts = ['Arial Unicode MS', 'PingFang SC', 'Hiragino Sans GB', 'STHeiti', 'SimHei', 'Microsoft YaHei']
        available_font = None
        
        for font_name in chinese_fonts:
            try:
                font_list = [f.name for f in fm.fontManager.ttflist]
                if font_name in font_list:
                    available_font = font_name
                    break
            except:
                continue
        
        if available_font:
            plt.rcParams['font.sans-serif'] = [available_font]
            self.logger.info(f"使用字体: {available_font}")
        else:
            plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
            self.logger.warning("未找到中文字体，图表中文可能显示为方框")
        
        plt.rcParams['axes.unicode_minus'] = False
    
    def _load_stopwords(self):
        """加载停用词"""
        self.stopwords = set([
            '的', '了', '是', '在', '我', '有', '和', '就', '不', '人', '都', '一', '个',
            '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看',
            '好', '自己', '这', '哔哩', 'bilibili', 'B站', '视频', '观看', '点赞',
            '投币', '收藏', '分享', '弹幕', '评论', '关注', 'UP主', 'up主', '播放',
            '更新', '发布', '上传', '链接', '地址', '网站', '平台', '用户', '内容'
        ])
    
    def _ensure_directories(self):
        """确保目录存在"""
        for dir_path in DATA_STORAGE.values():
            os.makedirs(dir_path, exist_ok=True)
    
    def load_data(self, filepath: str = None) -> pd.DataFrame:
        """
        加载数据
        
        Args:
            filepath: 数据文件路径，如果为None则加载默认增强数据
            
        Returns:
            DataFrame
        """
        if filepath is None:
            filepath = os.path.join(DATA_STORAGE['processed_data_dir'], 'enhanced_videos_data.csv')
        
        try:
            if not os.path.exists(filepath):
                self.logger.error(f"数据文件不存在: {filepath}")
                return pd.DataFrame()
            
            df = pd.read_csv(filepath, encoding='utf-8-sig')
            self.logger.info(f"成功加载数据，共 {len(df)} 条记录")
            
            # 数据预处理
            df = self._preprocess_data(df)
            
            return df
            
        except Exception as e:
            self.logger.error(f"加载数据失败: {e}")
            return pd.DataFrame()
    
    def _preprocess_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        数据预处理
        
        Args:
            df: 原始DataFrame
            
        Returns:
            预处理后的DataFrame
        """
        # 转换时间戳为日期
        if 'pubdate' in df.columns:
            df['pubdate_datetime'] = pd.to_datetime(df['pubdate'], unit='s', errors='coerce')
            df['year'] = df['pubdate_datetime'].dt.year
            df['month'] = df['pubdate_datetime'].dt.month
            df['quarter'] = df['pubdate_datetime'].dt.quarter
        
        # 处理数值类型
        numeric_columns = ['view', 'danmaku', 'reply', 'favorite', 'coin', 'like', 'share']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # 清理文本数据
        text_columns = ['title', 'description', 'author', 'tag']
        for col in text_columns:
            if col in df.columns:
                df[col] = df[col].astype(str).fillna('')
        
        # 计算参与度指标
        df['engagement_score'] = (
            df.get('like', 0) * 3 +
            df.get('coin', 0) * 5 +
            df.get('favorite', 0) * 4 +
            df.get('share', 0) * 6 +
            df.get('reply', 0) * 2
        )
        
        # 计算互动率
        df['engagement_rate'] = np.where(
            df.get('view', 0) > 0,
            df['engagement_score'] / df['view'] * 100,
            0
        )
        
        self.logger.info("数据预处理完成")
        return df
    
    def analyze_time_trends(self, df: pd.DataFrame) -> Dict:
        """
        分析时间趋势
        
        Args:
            df: 数据DataFrame
            
        Returns:
            趋势分析结果
        """
        self.logger.info("开始分析时间趋势")
        
        results = {}
        
        # 按年统计
        yearly_stats = df.groupby('year').agg({
            'bvid': 'count',
            'view': ['sum', 'mean'],
            'engagement_score': 'mean',
            'engagement_rate': 'mean'
        }).round(2)
        
        yearly_stats.columns = ['video_count', 'total_views', 'avg_views', 'avg_engagement_score', 'avg_engagement_rate']
        results['yearly_trends'] = yearly_stats.to_dict('index')
        
        # 按季度统计
        df['year_quarter'] = df['year'].astype(str) + '-Q' + df['quarter'].astype(str)
        quarterly_stats = df.groupby('year_quarter').agg({
            'bvid': 'count',
            'view': 'mean',
            'engagement_rate': 'mean'
        }).round(2)
        
        quarterly_stats.columns = ['video_count', 'avg_views', 'avg_engagement_rate']
        results['quarterly_trends'] = quarterly_stats.to_dict('index')
        
        # 按月统计
        df['year_month'] = df['pubdate_datetime'].dt.to_period('M')
        monthly_stats = df.groupby('year_month').agg({
            'bvid': 'count',
            'view': 'mean'
        }).round(2)
        
        monthly_stats.columns = ['video_count', 'avg_views']
        results['monthly_trends'] = monthly_stats.to_dict('index')
        
        self.logger.info("时间趋势分析完成")
        return results
    
    def analyze_content_themes(self, df: pd.DataFrame) -> Dict:
        """
        分析内容主题和关注点变化
        
        Args:
            df: 数据DataFrame
            
        Returns:
            主题分析结果
        """
        self.logger.info("开始分析内容主题")
        
        results = {}
        
        # 提取关键词
        all_text = ' '.join(df['title'].fillna('') + ' ' + df['description'].fillna(''))
        
        # 使用jieba分词和关键词提取
        keywords = jieba.analyse.extract_tags(all_text, topK=100, withWeight=True)
        
        # 过滤停用词
        filtered_keywords = [(word, weight) for word, weight in keywords 
                           if word not in self.stopwords and len(word) > 1]
        
        results['top_keywords'] = filtered_keywords[:50]
        
        # 按年分析关键词变化
        yearly_keywords = {}
        for year in df['year'].unique():
            if pd.isna(year):
                continue
            
            year_data = df[df['year'] == year]
            year_text = ' '.join(year_data['title'].fillna('') + ' ' + year_data['description'].fillna(''))
            
            if year_text.strip():
                year_keywords = jieba.analyse.extract_tags(year_text, topK=20, withWeight=True)
                filtered_year_keywords = [(word, weight) for word, weight in year_keywords 
                                        if word not in self.stopwords and len(word) > 1]
                yearly_keywords[int(year)] = filtered_year_keywords[:10]
        
        results['yearly_keywords'] = yearly_keywords
        
        # 分析标签
        all_tags = []
        for tags in df['tag'].fillna(''):
            if tags:
                tag_list = [tag.strip() for tag in str(tags).split(',')]
                all_tags.extend(tag_list)
        
        tag_counter = Counter(all_tags)
        results['top_tags'] = tag_counter.most_common(30)
        
        # 分析作者类型
        author_stats = df.groupby('author').agg({
            'bvid': 'count',
            'view': 'sum',
            'engagement_score': 'mean'
        }).sort_values('bvid', ascending=False).head(20)
        
        results['top_authors'] = author_stats.to_dict('index')
        
        self.logger.info("内容主题分析完成")
        return results
    
    def analyze_sentiment(self, df: pd.DataFrame) -> Dict:
        """
        分析情感态度
        
        Args:
            df: 数据DataFrame
            
        Returns:
            情感分析结果
        """
        self.logger.info("开始分析情感态度")
        
        results = {}
        
        # 对标题进行情感分析
        sentiments = []
        sentiment_scores = []
        
        for title in df['title'].fillna(''):
            if title.strip():
                try:
                    # 使用SnowNLP进行中文情感分析
                    s = SnowNLP(title)
                    sentiment_score = s.sentiments
                    sentiment_scores.append(sentiment_score)
                    
                    # 分类情感
                    if sentiment_score > ANALYSIS_CONFIG['sentiment_threshold']['positive']:
                        sentiments.append('positive')
                    elif sentiment_score < ANALYSIS_CONFIG['sentiment_threshold']['negative']:
                        sentiments.append('negative')
                    else:
                        sentiments.append('neutral')
                except:
                    sentiments.append('neutral')
                    sentiment_scores.append(0.5)
            else:
                sentiments.append('neutral')
                sentiment_scores.append(0.5)
        
        df['sentiment'] = sentiments
        df['sentiment_score'] = sentiment_scores
        
        # 统计情感分布
        sentiment_dist = df['sentiment'].value_counts()
        results['sentiment_distribution'] = sentiment_dist.to_dict()
        
        # 按年分析情感变化
        yearly_sentiment = df.groupby(['year', 'sentiment']).size().unstack(fill_value=0)
        yearly_sentiment_pct = yearly_sentiment.div(yearly_sentiment.sum(axis=1), axis=0) * 100
        results['yearly_sentiment'] = yearly_sentiment_pct.round(2).to_dict('index')
        
        # 情感与参与度关系
        sentiment_engagement = df.groupby('sentiment').agg({
            'view': 'mean',
            'engagement_rate': 'mean',
            'sentiment_score': 'mean'
        }).round(3)
        results['sentiment_engagement'] = sentiment_engagement.to_dict('index')
        
        # 积极/消极词汇分析
        positive_titles = df[df['sentiment'] == 'positive']['title'].tolist()
        negative_titles = df[df['sentiment'] == 'negative']['title'].tolist()
        
        if positive_titles:
            positive_text = ' '.join(positive_titles)
            positive_keywords = jieba.analyse.extract_tags(positive_text, topK=20)
            results['positive_keywords'] = [kw for kw in positive_keywords if kw not in self.stopwords]
        
        if negative_titles:
            negative_text = ' '.join(negative_titles)
            negative_keywords = jieba.analyse.extract_tags(negative_text, topK=20)
            results['negative_keywords'] = [kw for kw in negative_keywords if kw not in self.stopwords]
        
        self.logger.info("情感态度分析完成")
        return results
    
    def analyze_engagement_patterns(self, df: pd.DataFrame) -> Dict:
        """
        分析参与度模式
        
        Args:
            df: 数据DataFrame
            
        Returns:
            参与度分析结果
        """
        self.logger.info("开始分析参与度模式")
        
        results = {}
        
        # 基础统计
        engagement_stats = df.agg({
            'view': ['mean', 'median', 'std'],
            'like': ['mean', 'median', 'std'],
            'coin': ['mean', 'median', 'std'],
            'favorite': ['mean', 'median', 'std'],
            'share': ['mean', 'median', 'std'],
            'reply': ['mean', 'median', 'std'],
            'engagement_rate': ['mean', 'median', 'std']
        }).round(2)
        
        results['engagement_stats'] = engagement_stats.to_dict()
        
        # 高参与度视频特征
        high_engagement = df[df['engagement_rate'] > df['engagement_rate'].quantile(0.8)]
        
        if not high_engagement.empty:
            high_engagement_keywords = []
            for title in high_engagement['title']:
                keywords = jieba.analyse.extract_tags(title, topK=5)
                high_engagement_keywords.extend(keywords)
            
            results['high_engagement_keywords'] = Counter(high_engagement_keywords).most_common(20)
        
        # 参与度与时间关系
        engagement_by_year = df.groupby('year').agg({
            'engagement_rate': ['mean', 'median'],
            'view': 'mean'
        }).round(2)
        
        results['engagement_by_year'] = engagement_by_year.to_dict('index')
        
        # 视频时长与参与度关系（如果有duration数据）
        if 'duration_seconds' in df.columns:
            df['duration_minutes'] = df['duration_seconds'] / 60
            duration_bins = pd.cut(df['duration_minutes'], bins=[0, 5, 15, 30, 60, float('inf')], 
                                 labels=['0-5分钟', '5-15分钟', '15-30分钟', '30-60分钟', '60分钟以上'])
            
            duration_engagement = df.groupby(duration_bins).agg({
                'engagement_rate': 'mean',
                'view': 'mean',
                'bvid': 'count'
            }).round(2)
            
            results['duration_engagement'] = duration_engagement.to_dict('index')
        
        self.logger.info("参与度模式分析完成")
        return results
    
    def generate_comprehensive_report(self, df: pd.DataFrame) -> Dict:
        """
        生成综合分析报告
        
        Args:
            df: 数据DataFrame
            
        Returns:
            综合报告
        """
        self.logger.info("生成综合分析报告")
        
        report = {
            'overview': {
                'total_videos': len(df),
                'date_range': f"{df['year'].min():.0f} - {df['year'].max():.0f}",
                'total_views': int(df['view'].sum()),
                'avg_views': round(df['view'].mean(), 2),
                'total_engagement': int(df['engagement_score'].sum()),
                'avg_engagement_rate': round(df['engagement_rate'].mean(), 3)
            },
            'time_trends': self.analyze_time_trends(df),
            'content_themes': self.analyze_content_themes(df),
            'sentiment_analysis': self.analyze_sentiment(df),
            'engagement_patterns': self.analyze_engagement_patterns(df)
        }
        
        # 处理数据以便JSON序列化
        def convert_for_json(obj):
            """转换对象为JSON可序列化格式"""
            if hasattr(obj, 'to_dict'):
                return obj.to_dict()
            elif hasattr(obj, 'strftime'):  # 处理时间对象
                return str(obj)
            elif isinstance(obj, (pd.Period, pd.Timestamp)):
                return str(obj)
            elif isinstance(obj, tuple):
                return list(obj)
            elif isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            return str(obj)
        
        # 深度转换report
        def deep_convert(data):
            if isinstance(data, dict):
                return {str(k): deep_convert(v) for k, v in data.items()}
            elif isinstance(data, list):
                return [deep_convert(item) for item in data]
            else:
                return convert_for_json(data)
        
        json_safe_report = deep_convert(report)
        
        # 保存报告
        report_file = os.path.join(DATA_STORAGE['output_dir'], 'analysis_report.json')
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(json_safe_report, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"综合报告已保存到: {report_file}")
        return report
    
    def save_processed_data(self, df: pd.DataFrame):
        """
        保存处理后的数据
        
        Args:
            df: 处理后的DataFrame
        """
        # 保存CSV
        csv_file = os.path.join(DATA_STORAGE['output_dir'], 'analyzed_data.csv')
        df.to_csv(csv_file, index=False, encoding='utf-8-sig')
        
        # 保存Excel
        excel_file = os.path.join(DATA_STORAGE['output_dir'], 'analyzed_data.xlsx')
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='全部数据', index=False)
            
            # 按年分组
            for year in sorted(df['year'].unique()):
                if not pd.isna(year):
                    year_data = df[df['year'] == year]
                    year_data.to_excel(writer, sheet_name=f'{int(year)}年数据', index=False)
        
        self.logger.info(f"处理后数据已保存到: {csv_file} 和 {excel_file}")


def main():
    """主函数"""
    analyzer = ExecutionDataAnalyzer()
    
    # 加载数据
    df = analyzer.load_data()
    
    if df.empty:
        print("没有可分析的数据")
        return
    
    # 生成综合报告
    report = analyzer.generate_comprehensive_report(df)
    
    # 保存处理后的数据
    analyzer.save_processed_data(df)
    
    # 打印概览
    print("\n=== 执行力内容分析报告 ===")
    print(f"分析期间: {report['overview']['date_range']}")
    print(f"视频总数: {report['overview']['total_videos']}")
    print(f"总播放量: {report['overview']['total_views']:,}")
    print(f"平均播放量: {report['overview']['avg_views']:,}")
    print(f"平均参与度: {report['overview']['avg_engagement_rate']:.3f}%")
    
    print("\n=== 情感分布 ===")
    sentiment_dist = report['sentiment_analysis']['sentiment_distribution']
    for sentiment, count in sentiment_dist.items():
        percentage = count / sum(sentiment_dist.values()) * 100
        print(f"{sentiment}: {count} ({percentage:.1f}%)")
    
    print("\n=== 热门关键词 ===")
    top_keywords = report['content_themes']['top_keywords'][:10]
    for i, (keyword, weight) in enumerate(top_keywords, 1):
        print(f"{i}. {keyword} (权重: {weight:.3f})")


if __name__ == "__main__":
    main()