import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from datetime import datetime

def setup_production_logging():
    """Configure logging for production deployment"""
    
    # Create logs directory if it doesn't exist
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Configure root logger
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            # Console handler for Render logs
            logging.StreamHandler(sys.stdout),
            # File handler for persistent logs
            RotatingFileHandler(
                f"{log_dir}/bucket_production.log",
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5
            )
        ]
    )
    
    # Configure specific loggers
    loggers = {
        'uvicorn': logging.INFO,
        'uvicorn.access': logging.INFO,
        'fastapi': logging.INFO,
        'bucket': logging.INFO,
        'governance': logging.INFO,
        'integration': logging.INFO
    }
    
    for logger_name, level in loggers.items():
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)
    
    # Log startup message
    logger = logging.getLogger("bucket.startup")
    logger.info(f"Production logging configured - Level: {log_level}")
    logger.info(f"Environment: {os.getenv('ENVIRONMENT', 'unknown')}")
    logger.info(f"Port: {os.getenv('PORT', 'unknown')}")
    
    return logger

def get_production_logger(name):
    """Get a logger for production use"""
    return logging.getLogger(f"bucket.{name}")

# Auto-configure if imported
if os.getenv("ENVIRONMENT") == "production":
    setup_production_logging()