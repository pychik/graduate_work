import time

from etl_process import EtlProcess
from loguru import logger


INTERVAL = 60


if __name__ == '__main__':
    etl = EtlProcess()
    while True:
        logger.info('Started etl process')
        etl.process()
        logger.info(f'Etl process successfully finished,'
                    f' waiting {INTERVAL} seconds for next run')
        time.sleep(INTERVAL)
