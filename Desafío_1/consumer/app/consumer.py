import os
import random
import time
import requests
import logging


class Consumer():
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger('DowntimeFileAnalyzerLogger')
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

        self.logger.info('Starting Consumer')

        self.headers = {
            'App-name': self.get_config('APPNAME'),
            'token': self.get_config('APIKEY')
        }

    def get_config(self, key):
        return os.environ.get(key)

    def run(self):
        while True:
            response = requests.get(self.get_config("API_URL"), headers=self.headers)
            self.logger.info(f"Response text: {response.text}")
            # Genera un valor aleatorio entre 3 y 7 minutos en segundos
            seconds_random_time = random.randrange(3 * 60, 7 * 60 + 1)
            time.sleep(seconds_random_time)
