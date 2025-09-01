# Bilibili Content Analyzer

A comprehensive and highly configurable data analysis tool for Bilibili video content. Originally designed for analyzing "execution capability" topics but easily adaptable to analyze any subject matter through simple configuration changes.

## Key Features

### Highly Configurable
- Support for analyzing any keywords and topics
- Flexible time range settings  
- Customizable analysis parameters and visualization styles

### Core Functionality
- **Intelligent Data Collection**: Batch collection of video data using Bilibili's official API
- **Multi-dimensional Analysis**: Time trends, sentiment analysis, content themes, engagement patterns
- **Rich Visualizations**: Static charts, interactive dashboards, word clouds
- **Comprehensive Reports**: Detailed analysis reports in JSON, CSV, and Excel formats

### Analysis Dimensions
- **Time Trends**: Annual, quarterly, monthly publication and view count changes
- **Sentiment Analysis**: Distribution and changes of positive, neutral, negative attitudes  
- **Content Themes**: Keyword clouds, trending tags, topic evolution
- **Engagement**: Analysis of likes, coins, favorites, shares and other interaction data
- **Creators**: Most active and influential content creator analysis

## Quick Start

### Requirements
- Python 3.8+
- Internet connection (for Bilibili API access)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/bilibili-content-analyzer.git
cd bilibili-content-analyzer

# Install dependencies
pip install -r requirements.txt

# Install as editable package (recommended)
pip install -e .
```

### Basic Usage

```bash
# Run complete analysis pipeline
bilibili-analyzer

# Run individual modules
bilibili-analyzer --mode collect    # Data collection only
bilibili-analyzer --mode analyze    # Data analysis only  
bilibili-analyzer --mode visualize  # Generate charts only

# Force re-collection of data
bilibili-analyzer --force-recollect

# Use custom configuration
bilibili-analyzer --config custom_config.py

# Verbose logging
bilibili-analyzer --verbose
```

## Configuration

### How to Analyze Different Topics

The tool's biggest advantage is its ability to easily analyze any topic by modifying the configuration file:

#### 1. Modify Search Keywords

Edit the `SEARCH_KEYWORDS` list in `src/bilibili_analyzer/config.py`:

```python
# Example: Analyzing "Artificial Intelligence" topic
SEARCH_KEYWORDS = [
    'artificial intelligence',
    'AI technology', 
    'machine learning',
    'deep learning',
    'neural networks',
    'ChatGPT',
    'AI applications',
    'algorithms',
    'automation',
    'robotics'
]

# Example: Analyzing "Investment & Finance" topic  
SEARCH_KEYWORDS = [
    'investment',
    'stock trading',
    'mutual funds', 
    'financial planning',
    'investment strategy',
    'asset allocation',
    'financial knowledge',
    'value investing',
    'financial freedom'
]
```

#### 2. Adjust Time Range

```python
DATE_RANGE = {
    'start_year': 2020,        # Start year
    'end_year': 2024,          # End year
    'start_timestamp': 1577808000,  # 2020-01-01 00:00:00
    'end_timestamp': 1704067200     # 2024-01-01 00:00:00
}
```

#### 3. Advanced Configuration Options

```python
# Analysis configuration
ANALYSIS_CONFIG = {
    'sentiment_threshold': {
        'positive': 0.6,        # Positive sentiment threshold
        'negative': -0.1        # Negative sentiment threshold
    },
    'min_video_duration': 60,   # Minimum video duration (seconds)
    'max_results_per_keyword': 1000,  # Maximum results per keyword
    'request_delay': 1,         # API request interval (seconds)
    'batch_size': 50           # Batch processing size
}
```

## Use Cases

### Content Creators
- **Trend Tracking**: Discover trending topics and optimal posting times
- **Content Planning**: Analyze popular content themes and keywords
- **Competitive Analysis**: Understand competitor content strategies

### Brand Marketing
- **Market Insights**: Analyze target audience engagement with brand-related topics
- **Marketing Strategy**: Determine optimal content marketing directions and timing
- **Sentiment Monitoring**: Track sentiment changes around brand topics

### Academic Research
- **Social Trends**: Study evolution of internet culture and social topics
- **User Behavior**: Analyze video platform user content preferences
- **Communication Effects**: Research propagation patterns of different content types

### Industry Analysis
- **Market Research**: Understand specific industry development on Bilibili
- **Trend Prediction**: Predict topic development trends based on historical data
- **User Profiling**: Analyze target user group interest characteristics

## Project Structure

```
bilibili-content-analyzer/
├── src/                          # Source code directory
│   └── bilibili_analyzer/        # Main package
│       ├── __init__.py
│       ├── main.py              # Main entry point
│       ├── cli.py               # Command line interface
│       ├── config.py            # Configuration file
│       ├── data_collector.py    # Data collection module
│       ├── data_analyzer.py     # Data analysis module
│       ├── visualizer.py        # Data visualization module
│       └── font_utils.py        # Font utility module
├── data/                         # Data directory
│   ├── raw/                     # Raw data (by keyword)
│   └── processed/               # Processed data
├── output/                      # Output results directory
│   ├── charts/                  # Chart files
│   ├── analysis_report.json     # Detailed analysis report
│   ├── analyzed_data.csv        # Analysis data (CSV format)
│   └── analyzed_data.xlsx       # Analysis data (Excel format)
├── logs/                        # Log files
├── tests/                       # Test files
├── requirements.txt             # Project dependencies
├── pyproject.toml              # Project configuration
└── README.md                   # Project documentation
```

## Output Files

### Data Files
- `analyzed_data.csv`: Complete analysis data (CSV format)
- `analyzed_data.xlsx`: Analysis data Excel file (with annual worksheets)
- `analysis_report.json`: Detailed JSON format analysis report

### Chart Files
- `time_trends_detailed.png`: Detailed time trend analysis chart
- `sentiment_analysis_detailed.png`: Sentiment analysis chart
- `content_analysis.png`: Content theme analysis chart
- `engagement_analysis.png`: Engagement analysis chart
- `author_analysis.png`: Author influence analysis chart
- `wordcloud_analysis.png`: Keyword cloud chart
- `interactive_dashboard.html`: Interactive dashboard

## Tech Stack

- **Data Collection**: requests, aiohttp
- **Data Processing**: pandas, numpy
- **Chinese Text Processing**: jieba
- **Sentiment Analysis**: snownlp, textblob
- **Static Charts**: matplotlib, seaborn
- **Interactive Charts**: plotly
- **Word Cloud**: wordcloud
- **Data Storage**: CSV, Excel, JSON

## Troubleshooting

### Common Issues

#### Cannot Install Dependencies
```bash
# Solution: Upgrade pip and use mirror
python -m pip install --upgrade pip
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

#### Chinese Font Display Issues
```bash
# Solution: Manually specify font path in config.py
VISUALIZATION_CONFIG['font_family'] = '/System/Library/Fonts/Arial Unicode MS.ttf'
```

#### API Request Failures
```bash
# Solution: Increase request delay in config.py
ANALYSIS_CONFIG['request_delay'] = 2  # Increase to 2 seconds
```

### Debug Mode
```bash
# Enable verbose logging
bilibili-analyzer --verbose

# Dry run to check configuration
bilibili-analyzer --dry-run

# View log files
tail -f logs/main.log
```

## Contributing

We welcome contributions of all kinds! Whether it's new features, bug fixes, documentation improvements, or usage feedback.

### How to Contribute

1. **Submit Issues**: Create detailed issue reports for bugs or feature requests
2. **Code Contributions**:
   ```bash
   # Fork the project
   # Create feature branch
   git checkout -b feature/amazing-feature
   
   # Commit changes
   git commit -m "Add amazing feature"
   
   # Push to branch
   git push origin feature/amazing-feature
   
   # Create Pull Request
   ```

3. **Documentation**: Improve README, code comments, or add usage examples
4. **Testing**: Test the project in different environments and share feedback

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### Usage Terms
- ✅ Personal learning and research use
- ✅ Non-commercial data analysis
- ✅ Code modification and derivative works
- ❌ Commercial use requires additional authorization
- ❌ Malicious data collection or abuse

## Contact

- **GitHub Issues**: [Submit Issue](https://github.com/yourusername/bilibili-content-analyzer/issues)
- **Discussions**: [Join Discussion](https://github.com/yourusername/bilibili-content-analyzer/discussions)

## Disclaimer

This project is an open-source data analysis tool for educational and research purposes only. Users must:

1. **Comply with Laws**: Follow local laws and platform terms of service
2. **Reasonable Use**: Avoid malicious data collection or commercial abuse
3. **Assume Risks**: Users bear full responsibility for any risks from tool usage
4. **Data Responsibility**: Users are fully responsible for collected and analyzed data

**Important**: This tool provides no warranties. Developers are not liable for any damages caused by using this tool.

---

*If this project helps you, please give it a ⭐ Star!*
