"""
数据可视化模块
生成各种图表和可视化分析结果
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from wordcloud import WordCloud
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import logging

from .config import DATA_STORAGE, VISUALIZATION_CONFIG


class Visualizer:
    """Data visualizer for Bilibili content analysis."""
    
    def __init__(self):
        self.logger = self._setup_logger()
        self._setup_style()
        self._ensure_directories()
    
    def _setup_logger(self) -> logging.Logger:
        """设置日志记录器"""
        logger = logging.getLogger('ExecutionDataVisualizer')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            log_file = os.path.join(DATA_STORAGE['logs_dir'], 'visualizer.log')
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
    
    def _setup_style(self):
        """设置绘图风格"""
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
        plt.rcParams['figure.figsize'] = VISUALIZATION_CONFIG['figure_size']
        sns.set_style("whitegrid")
        sns.set_palette(VISUALIZATION_CONFIG['color_palette'])
    
    def _ensure_directories(self):
        """确保目录存在"""
        charts_dir = os.path.join(DATA_STORAGE['output_dir'], 'charts')
        os.makedirs(charts_dir, exist_ok=True)
    
    def load_data_and_report(self) -> tuple:
        """
        加载数据和分析报告
        
        Returns:
            (DataFrame, Dict): 数据和报告的元组
        """
        # 加载数据
        data_file = os.path.join(DATA_STORAGE['output_dir'], 'analyzed_data.csv')
        if os.path.exists(data_file):
            df = pd.read_csv(data_file, encoding='utf-8-sig')
            df['pubdate_datetime'] = pd.to_datetime(df['pubdate'], unit='s', errors='coerce')
        else:
            self.logger.error(f"数据文件不存在: {data_file}")
            df = pd.DataFrame()
        
        # 加载报告
        report_file = os.path.join(DATA_STORAGE['output_dir'], 'analysis_report.json')
        if os.path.exists(report_file):
            with open(report_file, 'r', encoding='utf-8') as f:
                report = json.load(f)
        else:
            self.logger.error(f"报告文件不存在: {report_file}")
            report = {}
        
        return df, report
    
    def create_time_trend_charts(self, df: pd.DataFrame, report: Dict):
        """
        创建时间趋势图表
        
        Args:
            df: 数据DataFrame
            report: 分析报告
        """
        self.logger.info("创建时间趋势图表")
        
        # 1. 年度视频数量趋势
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        yearly_data = report.get('time_trends', {}).get('yearly_trends', {})
        if yearly_data:
            years = list(yearly_data.keys())
            video_counts = [yearly_data[year]['video_count'] for year in years]
            avg_views = [yearly_data[year]['avg_views'] for year in years]
            
            # 视频数量趋势
            ax1.plot(years, video_counts, marker='o', linewidth=2, markersize=8)
            ax1.set_title('年度执行力相关视频数量趋势', fontsize=14, fontweight='bold')
            ax1.set_xlabel('年份')
            ax1.set_ylabel('视频数量')
            ax1.grid(True, alpha=0.3)
            
            # 平均播放量趋势
            ax2.plot(years, avg_views, marker='s', linewidth=2, markersize=8, color='orange')
            ax2.set_title('年度平均播放量趋势', fontsize=14, fontweight='bold')
            ax2.set_xlabel('年份')
            ax2.set_ylabel('平均播放量')
            ax2.grid(True, alpha=0.3)
            ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1000:.0f}K' if x >= 1000 else f'{x:.0f}'))
        
        # 3. 月度发布量热力图
        if not df.empty and 'pubdate_datetime' in df.columns:
            df['year'] = df['pubdate_datetime'].dt.year
            df['month'] = df['pubdate_datetime'].dt.month
            monthly_counts = df.groupby(['year', 'month']).size().reset_index(name='count')
            pivot_data = monthly_counts.pivot(index='year', columns='month', values='count').fillna(0)
            
            sns.heatmap(pivot_data, annot=True, fmt='.0f', cmap='YlOrRd', ax=ax3)
            ax3.set_title('月度发布量热力图', fontsize=14, fontweight='bold')
            ax3.set_xlabel('月份')
            ax3.set_ylabel('年份')
        
        # 4. 参与度趋势
        if yearly_data:
            engagement_rates = [yearly_data[year].get('avg_engagement_rate', 0) for year in years]
            ax4.plot(years, engagement_rates, marker='^', linewidth=2, markersize=8, color='green')
            ax4.set_title('年度平均参与度趋势', fontsize=14, fontweight='bold')
            ax4.set_xlabel('年份')
            ax4.set_ylabel('参与度 (%)')
            ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(os.path.join(DATA_STORAGE['output_dir'], 'charts', 'time_trends_detailed.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
        self.logger.info("时间趋势图表已保存")
    
    def create_sentiment_charts(self, df: pd.DataFrame, report: Dict):
        """
        创建情感分析图表
        
        Args:
            df: 数据DataFrame
            report: 分析报告
        """
        self.logger.info("创建情感分析图表")
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        sentiment_data = report.get('sentiment_analysis', {})
        
        # 1. 情感分布饼图
        sentiment_dist = sentiment_data.get('sentiment_distribution', {})
        if sentiment_dist:
            colors = ['#ff9999', '#66b3ff', '#99ff99']
            labels = {'positive': '积极', 'neutral': '中性', 'negative': '消极'}
            
            plot_labels = [labels.get(k, k) for k in sentiment_dist.keys()]
            ax1.pie(sentiment_dist.values(), labels=plot_labels, autopct='%1.1f%%', 
                   colors=colors, startangle=90)
            ax1.set_title('情感态度分布', fontsize=14, fontweight='bold')
        
        # 2. 年度情感变化
        yearly_sentiment = sentiment_data.get('yearly_sentiment', {})
        if yearly_sentiment:
            years = list(yearly_sentiment.keys())
            positive_pct = [yearly_sentiment[year].get('positive', 0) for year in years]
            negative_pct = [yearly_sentiment[year].get('negative', 0) for year in years]
            
            ax2.plot(years, positive_pct, marker='o', label='积极', linewidth=2)
            ax2.plot(years, negative_pct, marker='s', label='消极', linewidth=2)
            ax2.set_title('年度情感态度变化', fontsize=14, fontweight='bold')
            ax2.set_xlabel('年份')
            ax2.set_ylabel('百分比 (%)')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
        
        # 3. 情感与参与度关系
        sentiment_engagement = sentiment_data.get('sentiment_engagement', {})
        if sentiment_engagement:
            sentiments = list(sentiment_engagement.keys())
            engagement_rates = [sentiment_engagement[s]['engagement_rate'] for s in sentiments]
            
            colors_map = {'positive': 'green', 'neutral': 'gray', 'negative': 'red'}
            colors = [colors_map.get(s, 'blue') for s in sentiments]
            
            bars = ax3.bar([labels.get(s, s) for s in sentiments], engagement_rates, color=colors, alpha=0.7)
            ax3.set_title('情感态度与参与度关系', fontsize=14, fontweight='bold')
            ax3.set_ylabel('平均参与度 (%)')
            
            # 添加数值标签
            for bar, rate in zip(bars, engagement_rates):
                ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                        f'{rate:.3f}%', ha='center', va='bottom')
        
        # 4. 情感分数分布
        if not df.empty and 'sentiment_score' in df.columns:
            ax4.hist(df['sentiment_score'], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
            ax4.set_title('情感分数分布', fontsize=14, fontweight='bold')
            ax4.set_xlabel('情感分数 (0-1, 越大越积极)')
            ax4.set_ylabel('视频数量')
            ax4.axvline(df['sentiment_score'].mean(), color='red', linestyle='--', 
                       label=f'平均值: {df["sentiment_score"].mean():.3f}')
            ax4.legend()
        
        plt.tight_layout()
        plt.savefig(os.path.join(DATA_STORAGE['output_dir'], 'charts', 'sentiment_analysis.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
        self.logger.info("情感分析图表已保存")
    
    def create_content_analysis_charts(self, df: pd.DataFrame, report: Dict):
        """
        创建内容分析图表
        
        Args:
            df: 数据DataFrame
            report: 分析报告
        """
        self.logger.info("创建内容分析图表")
        
        # 1. 词云图
        content_themes = report.get('content_themes', {})
        top_keywords = content_themes.get('top_keywords', [])
        
        if top_keywords:
            # 准备词云数据
            word_freq = {word: weight for word, weight in top_keywords}
            
            # 生成词云
            wordcloud = WordCloud(**VISUALIZATION_CONFIG['wordcloud_config']).generate_from_frequencies(word_freq)
            
            plt.figure(figsize=(12, 8))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.title('执行力相关内容关键词云', fontsize=16, fontweight='bold', pad=20)
            plt.tight_layout()
            plt.savefig(os.path.join(DATA_STORAGE['output_dir'], 'charts', 'wordcloud.png'), 
                       dpi=300, bbox_inches='tight')
            plt.close()
        
        # 2. 热门关键词条形图
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        if top_keywords:
            top_20_keywords = top_keywords[:20]
            words = [item[0] for item in top_20_keywords]
            weights = [item[1] for item in top_20_keywords]
            
            y_pos = np.arange(len(words))
            bars = ax1.barh(y_pos, weights, color='skyblue', alpha=0.8)
            ax1.set_yticks(y_pos)
            ax1.set_yticklabels(words)
            ax1.set_xlabel('权重')
            ax1.set_title('热门关键词 (Top 20)', fontsize=14, fontweight='bold')
            ax1.grid(axis='x', alpha=0.3)
            
            # 添加数值标签
            for i, (bar, weight) in enumerate(zip(bars, weights)):
                ax1.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2,
                        f'{weight:.3f}', va='center', ha='left', fontsize=9)
        
        # 3. 热门标签
        top_tags = content_themes.get('top_tags', [])
        if top_tags:
            top_15_tags = top_tags[:15]
            tag_names = [item[0] for item in top_15_tags if item[0]]  # 过滤空标签
            tag_counts = [item[1] for item in top_15_tags if item[0]]
            
            if tag_names:
                y_pos = np.arange(len(tag_names))
                bars = ax2.barh(y_pos, tag_counts, color='lightcoral', alpha=0.8)
                ax2.set_yticks(y_pos)
                ax2.set_yticklabels(tag_names)
                ax2.set_xlabel('出现次数')
                ax2.set_title('热门标签 (Top 15)', fontsize=14, fontweight='bold')
                ax2.grid(axis='x', alpha=0.3)
                
                # 添加数值标签
                for bar, count in zip(bars, tag_counts):
                    ax2.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                            str(count), va='center', ha='left', fontsize=9)
        
        plt.tight_layout()
        plt.savefig(os.path.join(DATA_STORAGE['output_dir'], 'charts', 'content_analysis.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
        self.logger.info("内容分析图表已保存")
    
    def create_engagement_charts(self, df: pd.DataFrame, report: Dict):
        """
        创建参与度分析图表
        
        Args:
            df: 数据DataFrame
            report: 分析报告
        """
        self.logger.info("创建参与度分析图表")
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        engagement_data = report.get('engagement_patterns', {})
        
        # 1. 参与度分布直方图
        if not df.empty and 'engagement_rate' in df.columns:
            # 过滤异常值
            engagement_clean = df['engagement_rate'][df['engagement_rate'] < df['engagement_rate'].quantile(0.99)]
            
            ax1.hist(engagement_clean, bins=50, alpha=0.7, color='lightblue', edgecolor='black')
            ax1.set_title('参与度分布', fontsize=14, fontweight='bold')
            ax1.set_xlabel('参与度 (%)')
            ax1.set_ylabel('视频数量')
            ax1.axvline(engagement_clean.mean(), color='red', linestyle='--', 
                       label=f'平均值: {engagement_clean.mean():.3f}%')
            ax1.legend()
        
        # 2. 年度参与度变化
        engagement_by_year = engagement_data.get('engagement_by_year', {})
        if engagement_by_year:
            years = list(engagement_by_year.keys())
            avg_engagement = [engagement_by_year[year]['engagement_rate']['mean'] for year in years]
            avg_views = [engagement_by_year[year]['view']['mean'] for year in years]
            
            ax2_twin = ax2.twinx()
            
            line1 = ax2.plot(years, avg_engagement, 'b-o', label='平均参与度', linewidth=2)
            line2 = ax2_twin.plot(years, avg_views, 'r-s', label='平均播放量', linewidth=2)
            
            ax2.set_title('年度参与度与播放量趋势', fontsize=14, fontweight='bold')
            ax2.set_xlabel('年份')
            ax2.set_ylabel('参与度 (%)', color='b')
            ax2_twin.set_ylabel('播放量', color='r')
            
            # 合并图例
            lines = line1 + line2
            labels = [l.get_label() for l in lines]
            ax2.legend(lines, labels, loc='upper left')
            
            ax2.grid(True, alpha=0.3)
        
        # 3. 播放量vs参与度散点图
        if not df.empty:
            # 取样本避免图表过于密集
            sample_size = min(1000, len(df))
            sample_df = df.sample(n=sample_size) if len(df) > sample_size else df
            
            scatter = ax3.scatter(sample_df['view'], sample_df['engagement_rate'], 
                                alpha=0.6, c=sample_df['sentiment_score'], 
                                cmap='RdYlBu', s=30)
            ax3.set_title('播放量 vs 参与度', fontsize=14, fontweight='bold')
            ax3.set_xlabel('播放量')
            ax3.set_ylabel('参与度 (%)')
            ax3.set_xscale('log')
            
            # 添加颜色条
            cbar = plt.colorbar(scatter, ax=ax3)
            cbar.set_label('情感分数')
        
        # 4. 时长与参与度关系（如果有数据）
        duration_engagement = engagement_data.get('duration_engagement', {})
        if duration_engagement:
            durations = list(duration_engagement.keys())
            engagement_rates = [duration_engagement[d]['engagement_rate'] for d in durations]
            
            bars = ax4.bar(durations, engagement_rates, color='lightgreen', alpha=0.8)
            ax4.set_title('视频时长与参与度关系', fontsize=14, fontweight='bold')
            ax4.set_xlabel('视频时长')
            ax4.set_ylabel('平均参与度 (%)')
            ax4.tick_params(axis='x', rotation=45)
            
            # 添加数值标签
            for bar, rate in zip(bars, engagement_rates):
                ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                        f'{rate:.3f}%', ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        plt.savefig(os.path.join(DATA_STORAGE['output_dir'], 'charts', 'engagement_analysis.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
        self.logger.info("参与度分析图表已保存")
    
    def create_author_analysis_charts(self, df: pd.DataFrame, report: Dict):
        """
        创建作者分析图表
        
        Args:
            df: 数据DataFrame
            report: 分析报告
        """
        self.logger.info("创建作者分析图表")
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        content_themes = report.get('content_themes', {})
        top_authors = content_themes.get('top_authors', {})
        
        if top_authors:
            # 1. 最活跃作者（视频数量）
            authors = list(top_authors.keys())[:15]
            video_counts = [top_authors[author]['bvid'] for author in authors]
            
            y_pos = np.arange(len(authors))
            bars1 = ax1.barh(y_pos, video_counts, color='orange', alpha=0.8)
            ax1.set_yticks(y_pos)
            ax1.set_yticklabels(authors, fontsize=10)
            ax1.set_xlabel('视频数量')
            ax1.set_title('最活跃的执行力内容创作者 (Top 15)', fontsize=14, fontweight='bold')
            
            # 添加数值标签
            for bar, count in zip(bars1, video_counts):
                ax1.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                        str(count), va='center', ha='left', fontsize=9)
        
        # 2. 作者影响力（总播放量）
        if top_authors:
            total_views = [top_authors[author]['view'] for author in authors]
            
            bars2 = ax2.barh(y_pos, total_views, color='lightcoral', alpha=0.8)
            ax2.set_yticks(y_pos)
            ax2.set_yticklabels(authors, fontsize=10)
            ax2.set_xlabel('总播放量')
            ax2.set_title('最具影响力的执行力内容创作者 (Top 15)', fontsize=14, fontweight='bold')
            
            # 添加数值标签
            for bar, views in zip(bars2, total_views):
                if views >= 1000000:
                    label = f'{views/1000000:.1f}M'
                elif views >= 1000:
                    label = f'{views/1000:.0f}K'
                else:
                    label = str(int(views))
                
                ax2.text(bar.get_width() + max(total_views)*0.01, bar.get_y() + bar.get_height()/2,
                        label, va='center', ha='left', fontsize=9)
        
        plt.tight_layout()
        plt.savefig(os.path.join(DATA_STORAGE['output_dir'], 'charts', 'author_analysis.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
        self.logger.info("作者分析图表已保存")
    
    def create_interactive_dashboard(self, df: pd.DataFrame, report: Dict):
        """
        创建交互式仪表板
        
        Args:
            df: 数据DataFrame
            report: 分析报告
        """
        self.logger.info("创建交互式仪表板")
        
        # 创建子图
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=('年度趋势', '情感分布', '月度热力图', '关键词排行', '参与度分布', '作者影响力'),
            specs=[[{"secondary_y": True}, {"type": "pie"}],
                   [{"type": "heatmap"}, {"type": "bar"}],
                   [{"type": "histogram"}, {"type": "bar"}]]
        )
        
        # 1. 年度趋势
        yearly_data = report.get('time_trends', {}).get('yearly_trends', {})
        if yearly_data:
            years = list(yearly_data.keys())
            video_counts = [yearly_data[year]['video_count'] for year in years]
            avg_views = [yearly_data[year]['avg_views'] for year in years]
            
            fig.add_trace(
                go.Scatter(x=years, y=video_counts, name='视频数量', line=dict(color='blue')),
                row=1, col=1
            )
            fig.add_trace(
                go.Scatter(x=years, y=avg_views, name='平均播放量', line=dict(color='red'), yaxis='y2'),
                row=1, col=1, secondary_y=True
            )
        
        # 2. 情感分布饼图
        sentiment_dist = report.get('sentiment_analysis', {}).get('sentiment_distribution', {})
        if sentiment_dist:
            labels = {'positive': '积极', 'neutral': '中性', 'negative': '消极'}
            fig.add_trace(
                go.Pie(labels=[labels.get(k, k) for k in sentiment_dist.keys()], 
                      values=list(sentiment_dist.values()),
                      name="情感分布"),
                row=1, col=2
            )
        
        # 3. 参与度分布
        if not df.empty and 'engagement_rate' in df.columns:
            fig.add_trace(
                go.Histogram(x=df['engagement_rate'], name='参与度分布', nbinsx=30),
                row=3, col=1
            )
        
        # 更新布局
        fig.update_layout(
            height=1200,
            title_text="执行力内容分析仪表板",
            title_x=0.5,
            showlegend=True
        )
        
        # 保存交互式图表
        fig.write_html(os.path.join(DATA_STORAGE['output_dir'], 'charts', 'interactive_dashboard.html'))
        
        self.logger.info("交互式仪表板已保存")
    
    def generate_all_visualizations(self):
        """
        生成所有可视化图表
        """
        self.logger.info("开始生成所有可视化图表")
        
        # 加载数据和报告
        df, report = self.load_data_and_report()
        
        if df.empty or not report:
            self.logger.error("数据或报告为空，无法生成图表")
            return
        
        try:
            # 生成各种图表
            self.create_time_trend_charts(df, report)
            self.create_sentiment_charts(df, report)
            self.create_content_analysis_charts(df, report)
            self.create_engagement_charts(df, report)
            self.create_author_analysis_charts(df, report)
            self.create_interactive_dashboard(df, report)
            
            self.logger.info("所有可视化图表生成完成")
            print("\n=== 可视化图表生成完成 ===")
            print(f"图表保存位置: {os.path.join(DATA_STORAGE['output_dir'], 'charts')}")
            print("生成的图表包括:")
            print("- time_trends_detailed.png: 时间趋势详细分析")
            print("- sentiment_analysis.png: 情感态度分析")
            print("- content_analysis.png: 内容主题分析")
            print("- engagement_analysis.png: 参与度分析")
            print("- author_analysis.png: 作者影响力分析")
            print("- wordcloud.png: 关键词云图")
            print("- interactive_dashboard.html: 交互式仪表板")
            
        except Exception as e:
            self.logger.error(f"生成可视化图表时出错: {e}")


def main():
    """主函数"""
    visualizer = ExecutionDataVisualizer()
    visualizer.generate_all_visualizations()


if __name__ == "__main__":
    main()