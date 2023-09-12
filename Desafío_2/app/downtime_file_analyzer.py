import os
from datetime import datetime
import pandas as pd
import logging
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from dotenv import load_dotenv
import os
import time

class DowntimeFileAnalyzer:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('DowntimeFileAnalyzerLogger')
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

        if os.path.exists(".env"):
            load_dotenv(verbose=True)

        self.logger.info("DowntimeFileAnalyzer started")

        self.timestamp_lines = []
        self.error_lines = []
        self.date_formats_count = {}

        # Variable utilizada para estimar la fecha de ocurrencia de las lineas sin timestamp
        self.latest_date_end = None

        self.min_date = None
        self.max_date = None

    def get_config(self, key):
        return os.getenv(key)

    # Función personalizada para analizar fechas y horas de diferentes formatos
    def parse_date(self, date_str):
        date_formats = ["%Y-%m-%dT%H:%M+00Z", "%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"]

        for date_format in date_formats:
            try:
                formated_date = datetime.strptime(date_str, date_format)
                self.date_formats_count[date_format] = self.date_formats_count.get(date_format, 0) + 1
                return formated_date
            except ValueError:
                pass

        self.logger.error(f"Formato de fecha desconocido: {date_str}")
        return date_str

    def sort_timestamps(self, timestamp_1, timestamp_2):
        if timestamp_1 > timestamp_2:
            self.logger.info(f"Timestamps out of order. {timestamp_1} - {timestamp_2}")
            return timestamp_2, timestamp_1
        else:
            return timestamp_1, timestamp_2

    def add_record(self, date_start, date_end, miliseconds_downtime, app_name):
        self.timestamp_lines.append(
            [date_start, miliseconds_downtime, app_name])
        self.latest_date_end = date_end

        if self.min_date is None or date_start < self.min_date:
            self.min_date = date_start

        if self.max_date is None or date_end > self.max_date:
            self.max_date = date_end

    def process_timestamp_line(self, app_name, inicio, fin):
        if inicio.year != fin.year or inicio.month != fin.month or inicio.day != fin.day:
            self.logger.info(f"Timestamps from different years, months or days: {inicio} - {fin}")
            current_date = inicio
            while current_date < fin:
                if (fin - current_date) < pd.Timedelta(days=1):
                    incremented_date = fin
                else:
                    incremented_date = current_date + pd.Timedelta(days=1)

                miliseconds_downtime = (incremented_date - current_date).total_seconds() * 1000

                self.add_record(current_date, incremented_date, miliseconds_downtime, app_name)

                current_date = incremented_date
        else:
            miliseconds_downtime = (fin - inicio).total_seconds() * 1000
            self.add_record(inicio, fin, miliseconds_downtime, app_name)

    def process_error_line(self, app_name, message):
        self.error_lines.append([app_name, self.latest_date_end, message])

    def process_line(self, line):
        columns = line.strip().split('\t')
        if len(columns) == 3:
            inicio, fin, app_name = self.parse_date(columns[0]), self.parse_date(columns[1]), columns[2]

            inicio, fin = self.sort_timestamps(inicio, fin)

            self.process_timestamp_line(app_name, inicio, fin)
        elif len(columns) == 1:
            app_name, message = columns[0].split("-")
            self.process_error_line(app_name, message)
        else:
            self.logger.error(f"Formato de linea desconocido: {line}")

    def analyze_file(self):
        # Abre el archivo en modo lectura
        with open(self.get_config("DATA_FILENAME"), 'r') as f:
            # Itera a través de cada línea en el archivo
            for line in f:
                try:
                    self.process_line(line)
                except Exception as e:
                    self.logger.error(f"{e} prosessing line {line}")

    def create_dataframe(self):
        data = pd.DataFrame(self.timestamp_lines,
                            columns=['start_date', 'miliseconds_downtime', 'app_name'])
        self.logger.info(f"Number of duplicated rows {data.duplicated().sum()}")
        self.dataframe = data.drop_duplicates()

    def export_to_influx(self):
        token = self.get_config("DOCKER_INFLUXDB_INIT_ADMIN_TOKEN")
        bucket = self.get_config("INFLUXDB_BUCKET")
        org = self.get_config("INFLUXDB_ORG")

        self.dataframe = self.dataframe.set_index('start_date')

        client = InfluxDBClient(url=self.get_config("INFLUXDB_URL"), token=token, org=org, debug=False)

        health = client.health()
        while health.status != "pass":
            self.logger.warning("InfluxDB is not ready yet. Waiting 10 seconds...")
            time.sleep(10)
            health = client.health()

        write_client = client.write_api(write_options=SYNCHRONOUS)

        write_client.write(bucket, record=self.dataframe, data_frame_measurement_name='downtimes',
                           data_frame_tag_columns=['app_name'])

    def export_results(self):
        self.create_dataframe()

        self.logger.info(f"Date formats counts: {self.date_formats_count}")
        self.logger.info(f"Min date in dataframe: {self.min_date}")
        self.logger.info(f"Max date in dataframe: {self.max_date}")

        self.export_to_influx()
