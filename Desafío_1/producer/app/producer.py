import os
import random
import time
import requests
import logging
from datetime import datetime

class Producer():
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger('ProducerLogger')
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

        self.logger.info('Starting Producer')

        self.headers = {
            'App-name': self.get_config('APPNAME'),
            'token': self.get_config('APIKEY')
        }

    def get_config(self, key):
        return os.environ.get(key)

    def run(self):
        while True:
            # Genero un valor aleatorio entre 1 y 10
            random_value = random.randrange(1, 10 + 1)

            data = {
                'current_status': random_value,
                'Change_at': datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
            }

            response = requests.post(url=self.get_config("API_URL"), headers=self.headers, json=data)
            self.logger.info(f"Response text: {response.text}")

            # Genera un valor aleatorio entre 3 y 7 minutos en segundos
            seconds_random_time = random.randrange(3 * 60, 7 * 60 + 1)
            time.sleep(seconds_random_time)
