import logging
import logging.config
import yaml
from core.config import CONFIG


def get_logger(path='../logging_config.yaml'):
    with open(path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
        logging.config.dictConfig(config)
        return logging.getLogger('app')


if __name__ == "__main__":
    logger = get_logger()
    #logger.debug('안녕디버그6')
    logger.info("안녕하세요")
    #logger.warning('안녕워닝')
    logger.error('안녕에러')
    #logger.fatal('안녕파탈')
    #logger.critical('안녕크리티컬')
else:
    logger = get_logger(path=CONFIG.LOG_CONFIG_PATH)
    logger.info("Connect: logger + logging_config")
