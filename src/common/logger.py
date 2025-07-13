import logging
import sys
from common.config import LoggerConfig

def get_logger(name: str = LoggerConfig.NAME, log_file: str = LoggerConfig.LOG_FILE) -> logging.Logger:
    logger = logging.getLogger(name)

    # 문자열을 logging 레벨로 변환
    level = getattr(logging, LoggerConfig.LEVEL.upper(), logging.INFO)
    logger.setLevel(level)

    if not logger.handlers:
        formatter = logging.Formatter(LoggerConfig.FORMAT, LoggerConfig.DATE_FORMAT)

        # 콘솔 핸들러
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)

        # 파일 핸들러
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger
