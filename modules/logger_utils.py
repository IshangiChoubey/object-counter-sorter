"""
logger_utils.py
----------------
Centralised logging setup. Every module in the pipeline logs through
this single logger so that a run can be fully audited from
output/pipeline.log (satisfies the 'logging/monitoring' and
'error handling strategy' non-functional requirements).
"""

import logging
import os


def get_logger(name: str, log_dir: str = "output", log_file: str = "pipeline.log") -> logging.Logger:
    """
    Return a configured logger that writes to both console and a log file.

    Parameters
    ----------
    name : str
        Usually __name__ of the calling module.
    log_dir : str
        Directory where the log file will be created.
    log_file : str
        Log file name.
    """
    os.makedirs(log_dir, exist_ok=True)
    logger = logging.getLogger(name)

    if not logger.handlers:  # avoid duplicate handlers on repeated calls
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File handler
        file_path = os.path.join(log_dir, log_file)
        file_handler = logging.FileHandler(file_path)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
