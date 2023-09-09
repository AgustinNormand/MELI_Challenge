from datetime import datetime
import pandas as pd
import calendar

FILENAME = "Datos_uptime_challenge.tsv"
class DowntimeFileAnalyzer:
    def __init__(self):
        self.timestamp_lines = []
        self.other_lines = []

        # Variable utilizada para estimar la fecha de ocurrencia de las lineas sin timestamp
        self.latest_start_timestamp = None

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

    def sort_timestamps(self, timestamp_1, timestamp_2):
        if timestamp_1 > timestamp_2:
            return timestamp_2, timestamp_1
        else:
            return timestamp_1, timestamp_2

    def add_timestamp_line(self, app_name, inicio, fin):
        if inicio.year != fin.year or inicio.month != fin.month or inicio.day != fin.day:
            print(f"Warning: Timestamps from different years, months or days: {inicio} - {fin}")
            current_date = inicio
            while current_date < fin:
                if (fin - current_date) < pd.Timedelta(days=1):
                    incremented_date = fin
                else:
                    incremented_date = current_date + pd.Timedelta(days=1)

                duration = (incremented_date - current_date).total_seconds() / 60
                self.timestamp_lines.append([current_date, incremented_date, duration, app_name])
                self.latest_start_timestamp = current_date

                current_date = incremented_date
        else:
            duration = (fin - inicio).total_seconds() / 60
            self.timestamp_lines.append([inicio, fin, duration, app_name])
            self.latest_start_timestamp = inicio

    def add_other_line(self, app_name, message):
        self.other_lines.append([app_name, self.latest_start_timestamp, message])

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

        self.create_dataframe()

    def create_dataframe(self):
        data = pd.DataFrame(self.timestamp_lines, columns=['inicio', 'fin', 'duration', 'app_name'])
        print(f"Number of duplicated rows {data.duplicated().sum()}")
        self.dataframe = data.drop_duplicates()

    def get_uptime(self, dataframe, year):
        if dataframe.empty:
            return 100
        else:
            days = 366 if calendar.isleap(year) else 365
            duracion_total = days * 24 * 60 * 60
            duracion_downtime = (dataframe["fin"] - dataframe["inicio"]).sum().total_seconds()
            return ((duracion_total - duracion_downtime) / duracion_total) * 100

    def get_available_years(self):
        return list(range(self.dataframe["inicio"].min().year, self.dataframe["fin"].max().year + 1))

    def get_available_apps(self):
        return self.dataframe["app_name"].unique()

    def select_data(self, year, app_name):
        selected_data = self.dataframe[
            ((self.dataframe["inicio"].dt.year == year) | (self.dataframe["fin"].dt.year == year)) & (
                        self.dataframe["app_name"] == app_name)]

        return selected_data

    def export_year_csv(self):
        with open("year_downtimes.csv", 'w') as f:
            f.write("app_name,year,uptime\n")
            for year in self.get_available_years():
                for app_name in self.get_available_apps():
                    seleced_data = self.select_data(year, app_name)
                    f.write(f"{app_name},{year},{self.get_uptime(seleced_data, year)}\n")

    def export_cleaned_csv(self):
        self.dataframe.to_csv("downtimes.csv", index=False)

    def export_results(self):
        self.export_year_csv()
        return
