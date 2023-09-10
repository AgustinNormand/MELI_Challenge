# Desafío 2

## Descripción

### Formatos de lineas

El archivo 'Datos_uptime_challenge.tsv' contiene 2 tipos de lienas:

#### Lineas con datos de downtime

Estas lineas tienen el siguiente formato:

{timestamp_inicio_downtime}\t{timestamp_fin_downtime}\t{nombre_app}

Ejemplo: 2023-03-21T20:32:00.295181	2023-03-21T20:32:01.295181	app3

En total, el archivo contiene 60006 lineas de este tipo.

Los timestamps, a lo largo del archivo, tienen 4 formatos distintos:
* %Y-%m-%dT%H:%M:%S.%f: 119998 ocurrencias.
* %Y-%m-%dT%H:%M+00Z: 8 ocurrencias.
* %Y-%m-%dT%H:%M: 3 ocurrencias.
* %Y-%m-%d %H:%M: 3 ocurrencias.

Sumando dichos valores y dividiendolos por 2, obtenemos la cantidad de "Lineas con datos de downtime."

119998 + 8 + 3 + 3 = 120012 / 2 = 60006

#### Lineas con datos de errores

Estas lineas tienen el siguiente formato:

{nombre_app}-{mensaje_error}

Ejemplo: app4-error

En total, el archivo contiene 1 linea de este tipo.

### Orden de timestamps

De las 60006 lineas con datos de downtime, 60005 tienen el timestamp de inicio de downtime antes que el de fin de downtime.

Salvo una linea:

2023-03-21T16:50	2022-02-11 20:00	app4

Además, esta linea, es la única que abarca un intervalo de tiempo superior a un día.

### Duplicados

La app2 es la única que tiene una linea duplicada:

2022-02-21T15:50+00Z	2022-02-21T15:51+00Z	app2

2022-02-21T15:50	2022-02-21 15:51	app2

## Build
### Docker
```bash
docker-compose up -d
```

Instalé la extensión de csv

Agregé las lineas al grafana.ini
[plugin.marcusolsson-csv-datasource]
allow_local_mode = true

Hice las transformaciones necesarias dentro de grafana para los tipos de datos