import logging
from pathlib import Path

def get_logger(name: str, log_file: str, level: int = logging.DEBUG) -> logging.Logger:
    """
    Configures and returns a logger instance.

    Parameters:
    - name (str): Name of the logger (usually __name__).
    - log_file (str): Path to the log file.
    - level (int): Logging level (e.g., logging.DEBUG, logging.INFO).

    Returns:
    - logging.Logger: Configured logger instance.
    """

    BASEDIR = Path().parent.parent.parent
    file_handler = logging.FileHandler(BASEDIR / 'log' / log_file)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger