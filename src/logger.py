import logging, os

def setup_logger(name) -> logging.Logger:
    logger = logging.getLogger(name)
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    logger.setLevel(getattr(logging, level, logging.INFO))
    stream_handler = logging.StreamHandler()
    file_handler = logging.FileHandler("pipeline.log")
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter) 
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger