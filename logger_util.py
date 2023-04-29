import logging


def get_logger(level='info', name=None, file_name=None):
    level_dict = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'critical': logging.CRITICAL,
        'error': logging.ERROR,
        'fatal': logging.FATAL
    }
    level = level_dict.get(level, logging.INFO)

    if name:
        logger = logging.getLogger(name)
    else:
        logger = logging.getLogger()
    logger.setLevel(level)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s')

    # 使用StreamHandle输出到屏幕
    sh = logging.StreamHandler()
    sh.setLevel(level)
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    # 使用FileHander输出到文件
    if file_name:
        fh = logging.FileHandler()
        fh.setLevel(level)
        fh.setFormatter(format)
        logger.addHandler(fh)

    return logger

