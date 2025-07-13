import os
import logging
from src.logger import get_logger
from src.config import LoggerConfig

def test_logger_returns_logger_instance():
    logger = get_logger()
    assert isinstance(logger, logging.Logger)

def test_logger_level_matches_config():
    logger = get_logger()
    expected_level = getattr(logging, LoggerConfig.LEVEL.upper(), logging.INFO)
    assert logger.level == expected_level

def test_logger_writes_to_log_file(tmp_path):
    # 테스트용 로그 파일 경로
    test_log_file = tmp_path / "test_app.log"

    # 테스트용 로거 생성
    logger = get_logger(name="test_logger", log_file=str(test_log_file))
    test_message = "This is a test log entry."
    logger.info(test_message)

    # 파일이 생성되고 로그 메시지가 포함되어 있는지 확인
    assert test_log_file.exists()
    content = test_log_file.read_text(encoding="utf-8")
    assert test_message in content

def test_logger_no_duplicate_handlers():
    logger = get_logger()
    num_handlers_first = len(logger.handlers)

    # 다시 불러와도 핸들러 수는 유지되어야 함
    logger2 = get_logger()
    num_handlers_second = len(logger2.handlers)

    assert logger is logger2
    assert num_handlers_first == num_handlers_second
