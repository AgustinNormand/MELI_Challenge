from datetime import datetime
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

FILENAME = "Datos_uptime_challenge.tsv"

class DowntimeFileAnalyzer:
    def __init__(self):
        self.timestamp_lines = {}
        self.other_lines = {}

    # Función personalizada para analizar fechas y horas de diferentes formatos
    def parse_date(self, date_str):
        date_formats = ["%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"]
        for date_format in date_formats:
            try:
                if date_format == "%Y-%m-%dT%H:%M":
                    return datetime.strptime(date_str.replace("+00Z", ""), date_format)
                else:
                    return datetime.strptime(date_str, date_format)
            except ValueError:
                # logging.debug...
                pass

        print(f"Error: Formato de fecha desconocido: {date_str}")
        return date_str

    def sort_timestamps(self, inicio, fin):
        if inicio > fin:
            return fin, inicio
        else:
            return inicio, fin

    def add_timestamp_line(self, app_name, inicio, fin):
        duration = (fin - inicio).total_seconds() / 60
        if app_name in self.timestamp_lines:
            self.timestamp_lines[app_name].append([inicio, fin, duration])
        else:
            self.timestamp_lines[app_name] = [[inicio, fin, duration]]

    def add_other_line(self, app_name, message):
        if app_name in self.other_lines:
            self.other_lines[app_name].append(message)
        else:
            self.other_lines[app_name] = [message]

    def process_line(self, line):
        columns = line.strip().split('\t')
        if len(columns) == 3:
            inicio, fin, app_name = self.parse_date(columns[0]), self.parse_date(columns[1]), columns[2]

            inicio, fin = self.sort_timestamps(inicio, fin)

            self.add_timestamp_line(app_name, inicio, fin)
        elif len(columns) == 1:
            # Supongo que este tipo de lineas tiene la estructura appX-MESSAGE
            app_name, message = columns[0].split("-")
            self.add_other_line(app_name, message)
        else:
            print(f"Error: Formato de linea desconocido: {line}")

    def analyze_file(self):
        # Abre el archivo en modo lectura
        with open(FILENAME, 'r') as f:
            # Itera a través de cada línea en el archivo
            for line in f:
                try:
                    self.process_line(line)
                except Exception as e:
                    print(f"Error {e} prosessing line {line}")