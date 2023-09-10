from datetime import datetime
import pandas as pd
import calendar
import logging

FILENAME = "Datos_uptime_challenge.tsv"
QUARTERS = ["Q1", "Q2", "Q3", "Q4"]
MONTHS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

class DowntimeFileAnalyzer:
    def __init__(self):
        logging.basicConfig(filename="app.log",
                            format='%(asctime)s %(name)s - %(levelname)s - %(message)s',
                            filemode='w')

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        self.logger.info("DowntimeFileAnalyzer started")

        self.timestamp_lines = []
        self.other_lines = []
        self.date_formats_count = {}
        # Variable utilizada para estimar la fecha de ocurrencia de las lineas sin timestamp
        self.latest_date_end = None

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

    def get_quarter(self, timestamp):
        quarter = (timestamp.month - 1) // 3 + 1
        return f"Q{quarter}"

    def add_record(self, date_start, date_end, miliseconds_downtime, app_name):
        self.timestamp_lines.append(
            [date_start, self.get_quarter(date_start), miliseconds_downtime, app_name])
        self.latest_date_end = date_end

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

    def add_other_line(self, app_name, message):
        self.other_lines.append([app_name, self.latest_date_end, message])

    def process_line(self, line):
        columns = line.strip().split('\t')
        if len(columns) == 3:
            inicio, fin, app_name = self.parse_date(columns[0]), self.parse_date(columns[1]), columns[2]

            inicio, fin = self.sort_timestamps(inicio, fin)

            self.process_timestamp_line(app_name, inicio, fin)
        elif len(columns) == 1:
            # Supongo que este tipo de lineas tiene la estructura appX-MESSAGE
            app_name, message = columns[0].split("-")
            self.add_other_line(app_name, message)
        else:
            self.logger.error(f"Formato de linea desconocido: {line}")

    def analyze_file(self):
        # Abre el archivo en modo lectura
        with open(FILENAME, 'r') as f:
            # Itera a través de cada línea en el archivo
            for line in f:
                try:
                    self.process_line(line)
                except Exception as e:
                    self.logger.error(f"{e} prosessing line {line}")

        self.create_dataframe()

    def create_dataframe(self):
        data = pd.DataFrame(self.timestamp_lines,
                            columns=['start_date', 'quarter', 'miliseconds_downtime', 'app_name'])
        self.logger.info(f"Number of duplicated rows {data.duplicated().sum()}")
        self.dataframe = data.drop_duplicates()

    def export_cleaned_csv(self):
        self.dataframe.to_csv("downtimes.csv", index=False)

    def export_results(self):
        self.logger.info(f"Date formats counts: {self.date_formats_count}")
        self.export_cleaned_csv()
