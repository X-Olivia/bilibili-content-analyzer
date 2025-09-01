"""
B站数据采集模块
用于获取与执行力相关的视频和内容数据
"""

import requests
import json
import time
import logging
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import os
from urllib.parse import urlencode
import asyncio
import aiohttp
from tqdm import tqdm

from config import BILIBILI_SEARCH_API, SEARCH_KEYWORDS, DATE_RANGE, ANALYSIS_CONFIG, DATA_STORAGE


class BilibiliDataCollector:
    """B站数据采集器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(BILIBILI_SEARCH_API['headers'])
        self.logger = self._setup_logger()
        self._ensure_directories()
        
    def _setup_logger(self) -> logging.Logger:
        """设置日志记录器"""
        logger = logging.getLogger('BilibiliDataCollector')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            # 创建文件处理器
            log_file = os.path.join(DATA_STORAGE['logs_dir'], 'collector.log')
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.INFO)
            
            # 创建控制台处理器
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            # 创建格式器
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)
            
        return logger
    
    def _ensure_directories(self):
        """确保目录存在"""
        for dir_path in DATA_STORAGE.values():
            os.makedirs(dir_path, exist_ok=True)
    
    def search_videos(self, keyword: str, page: int = 1, 
                     order: str = 'totalrank') -> Dict:
        """
        搜索视频
        
        Args:
            keyword: 搜索关键词
            page: 页码
            order: 排序方式 ('totalrank', 'click', 'pubdate', 'dm', 'stow')
            
        Returns:
            搜索结果字典
        """
        params = {
            'keyword': keyword,
            'page': page,
            'order': order,
            'duration': 0,  # 时长筛选
            'tids': 0,      # 分区筛选
            'search_type': 'video'
        }
        
        try:
            url = BILIBILI_SEARCH_API['search_type_url']
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data.get('code') == 0:
                # 新API格式的数据结构
                result_data = data.get('data', {})
                if 'result' in result_data:
                    # 查找视频结果
                    for item in result_data['result']:
                        if item.get('result_type') == 'video':
                            return {'result': item.get('data', [])}
                    
                    # 如果没有找到video类型，返回第一个结果
                    if result_data['result']:
                        first_result = result_data['result'][0]
                        return {'result': first_result.get('data', [])}
                
                return {'result': []}
            else:
                self.logger.error(f"API返回错误: {data.get('message', '未知错误')}")
                return {}
                
        except requests.RequestException as e:
            self.logger.error(f"搜索请求失败: {e}")
            return {}
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON解析失败: {e}")
            return {}
    
    def get_video_info(self, bvid: str) -> Dict:
        """
        获取视频详细信息
        
        Args:
            bvid: 视频BV号
            
        Returns:
            视频信息字典
        """
        params = {'bvid': bvid}
        
        try:
            url = BILIBILI_SEARCH_API['video_info_url']
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data.get('code') == 0:
                return data.get('data', {})
            else:
                self.logger.warning(f"获取视频信息失败 {bvid}: {data.get('message', '未知错误')}")
                return {}
                
        except requests.RequestException as e:
            self.logger.error(f"获取视频信息请求失败 {bvid}: {e}")
            return {}
        except json.JSONDecodeError as e:
            self.logger.error(f"视频信息JSON解析失败 {bvid}: {e}")
            return {}
    
    def extract_video_data(self, video_item: Dict) -> Dict:
        """
        从搜索结果中提取视频数据
        
        Args:
            video_item: 视频项目数据
            
        Returns:
            提取的视频数据字典
        """
        try:
            # 清理标题中的HTML标签
            title = video_item.get('title', '')
            title = title.replace('<em class="keyword">', '').replace('</em>', '')
            
            # 提取作者信息
            author = ''
            if 'author' in video_item:
                author = video_item['author']
            elif 'owner' in video_item:
                owner = video_item['owner']
                if isinstance(owner, dict):
                    author = owner.get('name', '')
                else:
                    author = str(owner)
            
            return {
                'bvid': video_item.get('bvid', ''),
                'aid': video_item.get('aid', 0),
                'title': title,
                'author': author,
                'mid': video_item.get('mid', 0),
                'description': video_item.get('description', ''),
                'duration': video_item.get('duration', ''),
                'pubdate': video_item.get('pubdate', 0),
                'created': video_item.get('created', 0),
                'view': video_item.get('play', 0),
                'danmaku': video_item.get('video_review', 0),
                'reply': video_item.get('review', 0),
                'favorite': video_item.get('favorites', 0),
                'coin': video_item.get('coins', 0),
                'like': video_item.get('like', 0),
                'share': video_item.get('share', 0),
                'tag': video_item.get('tag', ''),
                'typeid': video_item.get('typeid', 0),
                'typename': video_item.get('typename', ''),
                'pic': video_item.get('pic', ''),
                'arcurl': video_item.get('arcurl', ''),
                'pts': video_item.get('pts', 0),
                'arcrank': video_item.get('arcrank', ''),
                'badgepay': video_item.get('badgepay', False)
            }
        except Exception as e:
            self.logger.error(f"提取视频数据失败: {e}")
            return {}
    
    def filter_by_date(self, videos: List[Dict], 
                      start_timestamp: int, end_timestamp: int) -> List[Dict]:
        """
        按时间范围过滤视频
        
        Args:
            videos: 视频列表
            start_timestamp: 开始时间戳
            end_timestamp: 结束时间戳
            
        Returns:
            过滤后的视频列表
        """
        filtered_videos = []
        for video in videos:
            pubdate = video.get('pubdate', 0)
            created = video.get('created', 0)
            
            # 使用发布时间或创建时间
            timestamp = pubdate if pubdate > 0 else created
            
            if start_timestamp <= timestamp <= end_timestamp:
                filtered_videos.append(video)
                
        return filtered_videos
    
    def collect_keyword_data(self, keyword: str, max_pages: int = 20) -> List[Dict]:
        """
        收集单个关键词的数据
        
        Args:
            keyword: 搜索关键词
            max_pages: 最大页数
            
        Returns:
            视频数据列表
        """
        self.logger.info(f"开始收集关键词 '{keyword}' 的数据")
        
        all_videos = []
        page = 1
        
        with tqdm(desc=f"收集 {keyword}", unit="页") as pbar:
            while page <= max_pages:
                try:
                    # 搜索视频
                    search_result = self.search_videos(keyword, page)
                    
                    if not search_result or 'result' not in search_result:
                        self.logger.warning(f"第{page}页搜索结果为空，停止收集")
                        break
                    
                    videos = search_result.get('result', [])
                    if not videos:
                        self.logger.info(f"第{page}页无更多结果，收集完成")
                        break
                    
                    # 提取视频数据
                    for video_item in videos:
                        video_data = self.extract_video_data(video_item)
                        if video_data:
                            video_data['search_keyword'] = keyword
                            video_data['collected_at'] = int(time.time())
                            all_videos.append(video_data)
                    
                    page += 1
                    pbar.update(1)
                    
                    # 请求间隔
                    time.sleep(ANALYSIS_CONFIG['request_delay'])
                    
                    # 检查是否达到最大结果数
                    if len(all_videos) >= ANALYSIS_CONFIG['max_results_per_keyword']:
                        self.logger.info(f"达到最大结果数限制，停止收集")
                        break
                        
                except Exception as e:
                    self.logger.error(f"收集第{page}页数据时出错: {e}")
                    break
        
        # 按时间过滤
        filtered_videos = self.filter_by_date(
            all_videos, 
            DATE_RANGE['start_timestamp'], 
            DATE_RANGE['end_timestamp']
        )
        
        self.logger.info(f"关键词 '{keyword}' 收集完成，共 {len(filtered_videos)} 个有效视频")
        return filtered_videos
    
    def collect_all_data(self) -> pd.DataFrame:
        """
        收集所有关键词的数据
        
        Returns:
            包含所有数据的DataFrame
        """
        self.logger.info("开始收集所有关键词数据")
        
        all_data = []
        
        for keyword in SEARCH_KEYWORDS:
            try:
                keyword_data = self.collect_keyword_data(keyword)
                all_data.extend(keyword_data)
                
                # 保存单个关键词的数据
                if keyword_data:
                    keyword_df = pd.DataFrame(keyword_data)
                    filename = f"{keyword.replace(' ', '_')}_data.csv"
                    filepath = os.path.join(DATA_STORAGE['raw_data_dir'], filename)
                    keyword_df.to_csv(filepath, index=False, encoding='utf-8-sig')
                    self.logger.info(f"已保存关键词 '{keyword}' 数据到 {filepath}")
                
            except Exception as e:
                self.logger.error(f"收集关键词 '{keyword}' 数据时出错: {e}")
                continue
        
        if all_data:
            # 创建DataFrame并去重
            df = pd.DataFrame(all_data)
            
            # 按bvid去重，保留最新的记录
            df = df.drop_duplicates(subset=['bvid'], keep='last')
            
            # 保存完整数据
            filepath = os.path.join(DATA_STORAGE['raw_data_dir'], 'all_videos_data.csv')
            df.to_csv(filepath, index=False, encoding='utf-8-sig')
            self.logger.info(f"已保存完整数据到 {filepath}")
            
            self.logger.info(f"数据收集完成，共收集 {len(df)} 个唯一视频")
            return df
        else:
            self.logger.warning("未收集到任何有效数据")
            return pd.DataFrame()
    
    def enhance_video_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        增强视频数据，获取更详细的信息
        
        Args:
            df: 视频数据DataFrame
            
        Returns:
            增强后的DataFrame
        """
        self.logger.info("开始增强视频数据")
        
        enhanced_data = []
        
        for idx, row in tqdm(df.iterrows(), total=len(df), desc="增强数据"):
            try:
                bvid = row['bvid']
                if not bvid:
                    continue
                
                # 获取详细视频信息
                video_info = self.get_video_info(bvid)
                
                if video_info:
                    # 合并数据
                    enhanced_row = row.to_dict()
                    
                    # 更新更详细的信息
                    enhanced_row.update({
                        'view': video_info.get('stat', {}).get('view', row['view']),
                        'danmaku': video_info.get('stat', {}).get('danmaku', row['danmaku']),
                        'reply': video_info.get('stat', {}).get('reply', row['reply']),
                        'favorite': video_info.get('stat', {}).get('favorite', row['favorite']),
                        'coin': video_info.get('stat', {}).get('coin', row['coin']),
                        'like': video_info.get('stat', {}).get('like', row['like']),
                        'share': video_info.get('stat', {}).get('share', row['share']),
                        'duration_seconds': video_info.get('duration', 0),
                        'cid': video_info.get('cid', 0),
                        'pages': video_info.get('pages', 1),
                        'owner_name': video_info.get('owner', {}).get('name', row['author']),
                        'owner_mid': video_info.get('owner', {}).get('mid', row['mid']),
                        'owner_face': video_info.get('owner', {}).get('face', ''),
                        'tname': video_info.get('tname', row['typename']),
                        'copyright': video_info.get('copyright', 0),
                        'desc': video_info.get('desc', row['description']),
                        'dynamic': video_info.get('dynamic', ''),
                        'subtitle': video_info.get('subtitle', {}),
                        'staff': video_info.get('staff', []),
                        'argue_info': video_info.get('argue_info', {}),
                        'honor_reply': video_info.get('honor_reply', {})
                    })
                    
                    enhanced_data.append(enhanced_row)
                else:
                    enhanced_data.append(row.to_dict())
                
                # 请求间隔
                time.sleep(ANALYSIS_CONFIG['request_delay'])
                
            except Exception as e:
                self.logger.error(f"增强数据时出错 (bvid: {row.get('bvid', 'unknown')}): {e}")
                enhanced_data.append(row.to_dict())
        
        enhanced_df = pd.DataFrame(enhanced_data)
        
        # 保存增强后的数据
        filepath = os.path.join(DATA_STORAGE['processed_data_dir'], 'enhanced_videos_data.csv')
        enhanced_df.to_csv(filepath, index=False, encoding='utf-8-sig')
        self.logger.info(f"已保存增强数据到 {filepath}")
        
        return enhanced_df


def main():
    """主函数"""
    collector = BilibiliDataCollector()
    
    # 收集基础数据
    df = collector.collect_all_data()
    
    if not df.empty:
        # 增强数据
        enhanced_df = collector.enhance_video_data(df)
        print(f"\n数据收集完成！")
        print(f"共收集 {len(enhanced_df)} 个视频")
        print(f"时间范围: {DATE_RANGE['start_year']}-{DATE_RANGE['end_year']}")
        print(f"搜索关键词: {', '.join(SEARCH_KEYWORDS)}")
    else:
        print("未收集到任何数据")


if __name__ == "__main__":
    main()