"""
Bilibili Content Analyzer - Main Analysis Module

This module provides the main orchestration for the Bilibili content analysis
workflow, including data collection, analysis, and visualization.
"""

import os
import sys
import argparse
import time
from datetime import datetime
import logging
from typing import Optional, Dict, Any

from .data_collector import BilibiliDataCollector
from .data_analyzer import DataAnalyzer
from .visualizer import Visualizer
from .config import DATA_STORAGE, SEARCH_KEYWORDS, DATE_RANGE


class BilibiliAnalyzer:
    """Main orchestrator for Bilibili content analysis workflow."""
    
    def __init__(self, config_path: Optional[str] = None, output_dir: Optional[str] = None):
        self.logger = self._setup_logger()
        self.collector = BilibiliDataCollector()
        self.analyzer = DataAnalyzer()
        self.visualizer = Visualizer()
        self.output_dir = output_dir or DATA_STORAGE['output_dir']
        self._ensure_directories()
    
    def _setup_logger(self) -> logging.Logger:
        """Setup main application logger."""
        logger = logging.getLogger('BilibiliAnalyzer')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            log_file = os.path.join(DATA_STORAGE['logs_dir'], 'main.log')
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
    
    def _ensure_directories(self):
        """Ensure all necessary directories exist."""
        for dir_path in DATA_STORAGE.values():
            os.makedirs(dir_path, exist_ok=True)
    
    def collect_only(self, force_recollect: bool = False) -> bool:
        """Run data collection only.
        
        Args:
            force_recollect: Whether to force re-collection of data
            
        Returns:
            bool: True if successful, False otherwise
        """
        print("\n" + "="*60)
        print("Starting Data Collection Phase")
        print("="*60)
        
        enhanced_data_file = os.path.join(DATA_STORAGE['processed_data_dir'], 'enhanced_videos_data.csv')
        
        if os.path.exists(enhanced_data_file) and not force_recollect:
            print(f"Found existing data file: {enhanced_data_file}")
            print("Use --force-recollect to re-collect data")
            return True
        
        self.logger.info("Starting data collection")
        start_time = time.time()
        
        try:
            # Collect basic data
            print(f"Collecting keywords: {', '.join(SEARCH_KEYWORDS)}")
            print(f"Time range: {DATE_RANGE['start_year']}-{DATE_RANGE['end_year']}")
            
            df = self.collector.collect_all_data()
            
            if df.empty:
                print("Data collection failed - no data retrieved")
                return False
            
            print(f"Basic data collection completed: {len(df)} videos")
            
            # Enhance data
            print("Enhancing video data...")
            enhanced_df = self.collector.enhance_video_data(df)
            
            elapsed_time = time.time() - start_time
            print(f"Data collection completed! Time: {elapsed_time/60:.1f} minutes")
            print(f"Data saved to: {DATA_STORAGE['processed_data_dir']}")
            
            self.logger.info(f"Data collection completed: {len(enhanced_df)} videos")
            return True
            
        except Exception as e:
            self.logger.error(f"Data collection failed: {e}")
            print(f"Data collection failed: {e}")
            return False
    
    def run_data_analysis(self):
        """运行数据分析"""
        print("\n" + "="*60)
        print("开始数据分析阶段")
        print("="*60)
        
        self.logger.info("开始数据分析")
        start_time = time.time()
        
        try:
            # 加载数据
            print("📂 加载数据...")
            df = self.analyzer.load_data()
            
            if df.empty:
                print("没有可分析的数据，请先运行数据采集")
                return False
            
            print(f"数据加载完成，共 {len(df)} 条记录")
            
            # 生成分析报告
            print("正在进行综合分析...")
            report = self.analyzer.generate_comprehensive_report(df)
            
            # 保存处理后的数据
            print("保存分析结果...")
            self.analyzer.save_processed_data(df)
            
            elapsed_time = time.time() - start_time
            print(f"数据分析完成！耗时: {elapsed_time:.1f} 秒")
            
            # 显示分析概览
            self._display_analysis_summary(report)
            
            self.logger.info("数据分析完成")
            return True
            
        except Exception as e:
            self.logger.error(f"数据分析失败: {e}")
            print(f"数据分析失败: {e}")
            return False
    
    def run_visualization(self):
        """运行数据可视化"""
        print("\n" + "="*60)
        print("开始数据可视化阶段")
        print("="*60)
        
        self.logger.info("开始生成可视化图表")
        start_time = time.time()
        
        try:
            self.visualizer.generate_all_visualizations()
            
            elapsed_time = time.time() - start_time
            print(f"可视化生成完成！耗时: {elapsed_time:.1f} 秒")
            
            charts_dir = os.path.join(DATA_STORAGE['output_dir'], 'charts')
            print(f"图表保存位置: {charts_dir}")
            
            self.logger.info("可视化生成完成")
            return True
            
        except Exception as e:
            self.logger.error(f"可视化生成失败: {e}")
            print(f"可视化生成失败: {e}")
            return False
    
    def _display_analysis_summary(self, report: dict):
        """显示分析摘要"""
        print("\n" + "="*60)
        print("分析结果摘要")
        print("="*60)
        
        overview = report.get('overview', {})
        
        print(f"分析期间: {overview.get('date_range', 'N/A')}")
        print(f"视频总数: {overview.get('total_videos', 0):,}")
        print(f"总播放量: {overview.get('total_views', 0):,}")
        print(f"平均播放量: {overview.get('avg_views', 0):,.0f}")
        print(f"平均参与度: {overview.get('avg_engagement_rate', 0):.3f}%")
        
        # 情感分布
        sentiment_dist = report.get('sentiment_analysis', {}).get('sentiment_distribution', {})
        if sentiment_dist:
            print(f"\n情感分布:")
            total_videos = sum(sentiment_dist.values())
            for sentiment, count in sentiment_dist.items():
                percentage = count / total_videos * 100
                sentiment_name = {"positive": "积极", "neutral": "中性", "negative": "消极"}.get(sentiment, sentiment)
                print(f"   {sentiment_name}: {count:,} ({percentage:.1f}%)")
        
        # 热门关键词
        top_keywords = report.get('content_themes', {}).get('top_keywords', [])
        if top_keywords:
            print(f"\n热门关键词 (Top 10):")
            for i, (keyword, weight) in enumerate(top_keywords[:10], 1):
                print(f"   {i:2d}. {keyword} (权重: {weight:.3f})")
        
        # 年度趋势
        yearly_trends = report.get('time_trends', {}).get('yearly_trends', {})
        if yearly_trends:
            print(f"\n年度趋势:")
            for year, data in yearly_trends.items():
                print(f"   {year}: {data.get('video_count', 0)} 个视频, "
                      f"平均播放量 {data.get('avg_views', 0):,.0f}")
    
    def run_full_analysis(self, force_recollect: bool = False):
        """运行完整分析流程"""
        print("B站执行力内容分析项目")
        print(f"🕒 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        overall_start_time = time.time()
        
        # 数据采集
        if not self.run_data_collection(force_recollect):
            print("数据采集失败，停止执行")
            return False
        
        # 数据分析
        if not self.run_data_analysis():
            print("数据分析失败，停止执行")
            return False
        
        # 数据可视化
        if not self.run_visualization():
            print("数据可视化失败，停止执行")
            return False
        
        # 完成
        total_time = time.time() - overall_start_time
        print("\n" + "="*60)
        print("分析项目完成！")
        print("="*60)
        print(f"总耗时: {total_time/60:.1f} 分钟")
        print(f"结果文件位置: {DATA_STORAGE['output_dir']}")
        print("\n生成的文件:")
        print(f"   • 分析报告: analysis_report.json")
        print(f"   • 数据文件: analyzed_data.csv, analyzed_data.xlsx")
        print(f"   • 图表目录: charts/")
        print(f"   • 交互式仪表板: charts/interactive_dashboard.html")
        
        return True


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='B站执行力内容分析项目')
    parser.add_argument('--mode', choices=['collect', 'analyze', 'visualize', 'full'], 
                       default='full', help='运行模式')
    parser.add_argument('--force-recollect', action='store_true', 
                       help='强制重新采集数据')
    
    args = parser.parse_args()
    
    project = ExecutionAnalysisProject()
    
    try:
        if args.mode == 'collect':
            success = project.run_data_collection(args.force_recollect)
        elif args.mode == 'analyze':
            success = project.run_data_analysis()
        elif args.mode == 'visualize':
            success = project.run_visualization()
        else:  # full
            success = project.run_full_analysis(args.force_recollect)
        
        if success:
            print("\n程序执行成功")
            sys.exit(0)
        else:
            print("\n程序执行失败")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n程序被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 程序执行过程中发生错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()