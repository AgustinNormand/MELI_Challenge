from itertools import count
import os


class Initializer():
    def __init__(self, influxdb_client, logger):
        self.client = influxdb_client
        self.logger = logger

    def get_config(self, key):
        return os.getenv(key)

    def process_id(self):
        try:
            # Consulta InfluxDB para obtener el mayor valor de process_id en el bucket secapp_producers
            query = f'from(bucket: "{self.get_config("INFLUXDB_BUCKET_PRODUCERS")}") ' \
                    f'|> range(start: 0) ' \
                    f'|> filter(fn: (r) => r["_field"] == "process_id") ' \
                    f'|> group() ' \
                    f'|> max(column: "_value")'

            result = self.client.query_api().query(query=query)

            # Procesa el resultado para obtener el valor máximo de process_id
            max_process_id = result[0].records[0].get_value()
            return count(max_process_id + 1)
        except Exception as e:
            return count(1)

    def criticity(self):
        try:
            # Consulta InfluxDB para obtener el mayor valor de process_id en el bucket secapp_producers
            query = f'from(bucket: "{self.get_config("INFLUXDB_BUCKET_PRODUCERS")}") ' \
                    f'|> range(start: 0) ' \
                    f'|> filter(fn: (r) => r._field == "criticity_value") ' \
                    f'|> group() ' \
                    f'|> last(column: "_value")'

            result = self.client.query_api().query(query=query)

            last_criticity_value = result[0].records[0].get_value()

            last_criticity_date = result[0].records[0].get_time()

            last_criticity_process_id = result[0].records[0]["process_id_tag"]

            return last_criticity_value, last_criticity_date, last_criticity_process_id
        except Exception as e:
            return None, None, None

    def clients_apps_last_update_timestamps(self):
        try:
            result_dictionary = {}

            query = f'from(bucket:"{self.get_config("INFLUXDB_BUCKET_CONSUMERS")}") ' \
                    f'|> range(start: 0) ' \
                    f'|> distinct(column: "app_name")'

            # Ejecuta la consulta
            result = self.client.query_api().query(query=query)

            for table in result:
                for record in table.records:
                    app_name = record.get_value()
                    result_dictionary[app_name] = None

            for app_name in result_dictionary.keys():
                query = f'from(bucket:"{self.get_config("INFLUXDB_BUCKET_CONSUMERS")}") ' \
                        f'|> range(start: 0) ' \
                        f'|> filter(fn: (r) => r["_measurement"] == "requests" and r.app_name == "{app_name}") ' \
                        f'|> group()' \
                        f'|> last(column: "_time")'

                result = self.client.query_api().query(query=query)

                result_dictionary[app_name] = result[0].records[0].get_time()

            return result_dictionary
        except Exception as e:
            self.logger.error(e)
            return {}
