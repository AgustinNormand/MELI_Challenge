# MELI_Challenge

## Soluciones

Utilizando el token enviado por correo, o el usuario y contraseña, se pueden probar las soluciones planteadas como respuesta al desafío. Se detallan las URL o endpoint en las siguiente secciones.

### Desafío 1

La API se encuentra disponible en el endpoint: 34.125.19.164:8000.

Acceder a la documentación en la dirección: http://34.125.19.164:8000/docs

Adicionalmente, se se encuentra disponible el [Dashboard](http://34.125.19.164:3000/d/d789e151-3b2f-41da-a6a4-d63afccd77fa/api-dashboard?orgId=1) de Grafana creado para la API.

### Desafío 2

Es posible coenctarse [Dashboard](http://34.125.19.164:3000/d/e8677d8e-67d0-4f6e-8415-f9c53619aba0/downtime-dashboard?orgId=1) de Grafana, para visualizar los resultados.

## Deploy en Cloud

Pasos para realizar el deploy de la solución:

* Levantar una instancia en un proveedor de cloud

* Agregar las reglas de firewall necesarias

* Instalar Docker (curl -fsSL get.docker.com -o get-docker.sh && sh get-docker.sh)

* Realizar los pasos post instalación (sudo groupadd docker && sudo usermod -aG docker $USER && newgrp docker)

* Instalar Docker-Compose (sudo apt install docker-compose -y)

* git clone https://github.com/AgustinNormand/MELI_Challenge.git

* Moverse al directorio "docker-compose" (cd MELI_Challenge/docker-compose)

* cp .env.example .env

* Completar el archivo .env

* docker-compose up -d

* Agregar en Grafana la fuente de datos InfluxDB (https://docs.influxdata.com/influxdb/v2.7/tools/grafana/?t=InfluxQL)
* * URL: http://influxdb:8086
* * Add "Custom HTTP Headers"
* * * X-Custom-Header = Authorization
* * * Header Value: Token DOCKER_INFLUXDB_INIT_ADMIN_TOKEN
* * Database: INFLUXDB_BUCKET
* * HTTP Method: GET

* Nota: Reemplazar los valores (DOCKER_INFLUXDB_INIT_ADMIN_TOKEN, INFLUXDB_BUCKET) con los definidos en el archivo .env. Además, debe agregarse una fuente de datos para cada bucket de InfluxDB

* Ingresar a Grafana, importar los dashboards usando los archivos json del desafío 1 y 2.


