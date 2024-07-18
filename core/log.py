import logging
import logging.config
import yaml
from core.config import CONFIG


def get_logger(path='../logging_config.yaml'):
    with open(path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
        logging.config.dictConfig(config)
        app_logger = logging.getLogger('app')
        access_logger = logging.getLogger('app_access')
        return app_logger, access_logger
        #return app_logger


if __name__ == "__main__":
    logger, access_logger = get_logger(path=CONFIG.LOG_CONFIG_PATH)
    logger.info("Connect: logger + logging_config")
    logger.info("안녕하세요")
    logger.error('안녕에러')
    access_logger.info("어세스로거")
    #logger.debug('안녕디버그')
    #logger.warning('안녕워닝')
    # logger.fatal('안녕파탈')
    # logger.critical('안녕크리티컬')
else:
    logger, access_logger = get_logger(path=CONFIG.LOG_CONFIG_PATH)
    #logger.info("Connect: logger + logging_config")
    #access_logger.info('gd')
