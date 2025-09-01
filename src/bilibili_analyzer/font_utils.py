"""
字体工具模块
处理matplotlib中文字体显示问题
"""

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import logging


def setup_chinese_font():
    """
    设置matplotlib的中文字体
    
    Returns:
        str: 使用的字体名称，如果没有找到中文字体则返回None
    """
    # 清除matplotlib字体缓存
    try:
        import shutil
        import os
        cache_dir = fm.get_cachedir()
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir)
        fm._rebuild()
    except:
        pass
    
    # 强制设置Hiragino Sans GB为首选字体
    plt.rcParams['font.sans-serif'] = ['Hiragino Sans GB', 'PingFang SC', 'Arial Unicode MS', 'STHeiti', 'SimHei', 'Microsoft YaHei']
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['axes.unicode_minus'] = False
    
    # 验证字体设置
    try:
        # 创建一个简单的测试
        import matplotlib.font_manager as fm
        font_prop = fm.FontProperties(family='sans-serif')
        actual_font = font_prop.get_name()
        logging.info(f"实际使用的字体: {actual_font}")
    except Exception as e:
        logging.warning(f"字体验证失败: {e}")
    
    return 'Hiragino Sans GB'


def get_available_chinese_fonts():
    """
    获取系统中所有可用的中文字体
    
    Returns:
        list: 中文字体名称列表
    """
    try:
        font_list = [f.name for f in fm.fontManager.ttflist]
        
        # 常见中文字体关键词
        chinese_keywords = [
            'Chinese', 'CJK', 'Han', 'Hei', 'Song', 'Kai', 'Fang',
            'PingFang', 'Hiragino', 'STHeiti', 'SimHei', 'Microsoft YaHei',
            'WenQuanYi', 'Noto', 'Source'
        ]
        
        chinese_fonts = []
        for font in font_list:
            for keyword in chinese_keywords:
                if keyword in font:
                    chinese_fonts.append(font)
                    break
        
        return list(set(chinese_fonts))  # 去重
        
    except Exception as e:
        logging.warning(f"获取中文字体列表时出错: {e}")
        return []


def print_font_info():
    """打印字体信息，用于调试"""
    print("=== 字体信息 ===")
    
    # 当前设置的字体
    current_font = plt.rcParams['font.sans-serif']
    print(f"当前设置字体: {current_font}")
    
    # 可用的中文字体
    chinese_fonts = get_available_chinese_fonts()
    if chinese_fonts:
        print(f"\n系统中可用的中文字体 ({len(chinese_fonts)} 个):")
        for i, font in enumerate(chinese_fonts[:10], 1):  # 只显示前10个
            print(f"  {i:2d}. {font}")
        if len(chinese_fonts) > 10:
            print(f"  ... 还有 {len(chinese_fonts) - 10} 个字体")
    else:
        print("\n未找到中文字体")
    
    print("=" * 20)


def create_font_test_chart():
    """
    创建字体测试图表
    用于检验中文字体是否正确显示
    """
    import matplotlib.pyplot as plt
    import numpy as np
    
    # 设置字体
    font_name = setup_chinese_font()
    
    # 创建测试图表
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 测试数据
    categories = ['执行力', '团队管理', '个人提升', '培训课程', '方法技巧']
    values = [85, 72, 90, 68, 77]
    
    # 创建柱状图
    bars = ax.bar(categories, values, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'])
    
    # 设置标题和标签
    ax.set_title('中文字体显示测试 - 执行力相关话题热度', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('话题类别', fontsize=12)
    ax.set_ylabel('热度指数', fontsize=12)
    
    # 添加数值标签
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f'{value}', ha='center', va='bottom', fontsize=10)
    
    # 添加网格
    ax.grid(axis='y', alpha=0.3)
    ax.set_ylim(0, 100)
    
    # 添加字体信息
    font_info = f"使用字体: {font_name if font_name else '默认字体 (中文可能显示为方框)'}"
    ax.text(0.02, 0.98, font_info, transform=ax.transAxes, 
            verticalalignment='top', fontsize=9, 
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    
    # 保存图表
    output_file = 'font_test_chart.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"字体测试图表已保存为: {output_file}")
    
    return font_name is not None


if __name__ == "__main__":
    # 运行字体测试
    print("检测中文字体支持...")
    
    # 打印字体信息
    print_font_info()
    
    # 设置字体
    font_name = setup_chinese_font()
    if font_name:
        print(f"成功设置中文字体: {font_name}")
    else:
        print("未找到合适的中文字体，图表中文可能显示为方框")
    
    # 创建测试图表
    print("\n创建字体测试图表...")
    success = create_font_test_chart()
    
    if success:
        print("字体测试完成，中文应该能正常显示")
    else:
        print("字体测试显示可能存在中文显示问题")