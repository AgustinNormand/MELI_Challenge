import os
import random
import time
import requests

class Consumer():
    def __init__(self):
        self.headers = {
            'App_name': self.get_config('APPNAME'),
            'token': self.get_config('APIKEY')
        }

    def get_config(self, key):
        return os.environ.get(key)

    def run(self):
        while True:
            requests.get(self.get_config("API_URL"), headers=self.headers)
            # Genera un valor aleatorio entre 3 y 7 minutos en segundos
            seconds_random_time = random.randrange(3 * 60, 7 * 60 + 1)
            time.sleep(seconds_random_time)
