def save_to_influx(self):
    token = "ypsvgA1Dye6EXvK"
    bucket = "downtimes"
    org = "MELI"

    from influxdb_client import InfluxDBClient, Point, WriteOptions
    from influxdb_client.client.write_api import SYNCHRONOUS

    self.dataframe = self.dataframe.set_index('start_date')
    client = InfluxDBClient(url="http://localhost:8086", token=token, org=org, debug=True)
    write_client = client.write_api(write_options=SYNCHRONOUS)

    write_client.write(bucket, record=self.dataframe, data_frame_measurement_name='downtimes',
                       data_frame_tag_columns=['app_name', 'quarter'])