#!/usr/bin/env python3
"""
Command-line interface for Bilibili Content Analyzer.
"""

import argparse
import sys
import logging
from pathlib import Path

from .main import BilibiliAnalyzer


def setup_logging(verbose: bool = False):
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('logs/bilibili_analyzer.log')
        ]
    )


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Bilibili Content Analyzer - Analyze Bilibili video content data'
    )
    
    parser.add_argument(
        '--mode',
        choices=['collect', 'analyze', 'visualize', 'full'],
        default='full',
        help='Analysis mode to run (default: full)'
    )
    
    parser.add_argument(
        '--force-recollect',
        action='store_true',
        help='Force re-collection of data even if cached data exists'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        help='Path to custom configuration file'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default='output',
        help='Output directory for results (default: output)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Perform a dry run without executing actions'
    )
    
    args = parser.parse_args()
    
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    try:
        # Create necessary directories
        Path('logs').mkdir(exist_ok=True)
        Path(args.output_dir).mkdir(exist_ok=True)
        
        analyzer = BilibiliAnalyzer(
            config_path=args.config,
            output_dir=args.output_dir
        )
        
        if args.dry_run:
            logger.info("Dry run mode - checking configuration...")
            analyzer.validate_config()
            logger.info("Configuration validation passed")
            return
        
        logger.info(f"Starting Bilibili Content Analyzer in {args.mode} mode")
        
        if args.mode == 'collect':
            analyzer.collect_only(force_recollect=args.force_recollect)
        elif args.mode == 'analyze':
            analyzer.analyze_only()
        elif args.mode == 'visualize':
            analyzer.visualize_only()
        else:
            analyzer.run_full_analysis(force_recollect=args.force_recollect)
            
        logger.info("Analysis completed successfully")
        
    except KeyboardInterrupt:
        logger.info("Analysis interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        if args.verbose:
            logger.exception("Full traceback:")
        sys.exit(1)


if __name__ == '__main__':
    main()