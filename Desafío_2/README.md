# Desafío 2

## Detalle de la solución planteada

Para resovler el ejercicio en primer lugar analicé el archivo enviado para entender su estructura y los datos que contenía.

Luego preprocesé los datos, para poder cargarlos en una base de datos.

La herramienta elegida para el almacenamiento de los datos fue InfluxDB, ya que es una base de datos orientada a series de tiempo, y los datos que se estaban analizando eran de ese tipo.

Por otro lado, para la visualización de los datos, se utilizó Grafana

## Análisis exploratorio

En esta seccion de describe lo aprendido sobre el archivo 'Datos_uptime_challenge.tsv'.

### Formatos de lineas

Dicho archivo contiene 2 tipos de lienas:

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

### Fecha de los datos

Los timestamps de las lineas del archivo van desde:

2019-09-07 15:50:00

Hasta:

2023-08-17 18:31:01.295181

## Preprocesado de los datos

En esta sección, se detallan los pasos seguidos para lograr el preprocesado de los datos.

* Se llevaron los timestamps a un formato común.
* Se descartó la linea de error "app4-error".
* Se invirtó el orden de los timestamps de la linea con el timestamp de inicio de downtime posterior al de fin de downtime.
* Se desagregó la linea que abarca un intervalo de tiempo grande, en lines de un día de duración.
* Se eliminó la linea duplicada.

## Visualización de los datos

Utilizando Grafana, se creó un dashboard separado por secciones:
* Uptime Generales
* Uptime Por Aplicación
* Uptime vinculando Aplicaciones
* Downtimes Generales

Utilizando estos, y el selector de fechas de Grafana se pueden responder las preguntas planteadas en el enunciado.

Cabe destacar que Grafana indica un valor preestablecido para cuando no hay datos disponibles, que hace referencia a 100% de uptime. 

Tal como en las preguntas 2, 4, y 5.

### 1. ¿Cuál fue el uptime de la aplicación app1 en 2019?

Estableciendo el intervalo de tiempo:

![timerange_question_1](https://github.com/AgustinNormand/MELI_Challenge/assets/48933518/28e27d5f-70d3-4724-9c26-5e3cd15d8ab3)

Obtenemos:

![answer_question_1](https://github.com/AgustinNormand/MELI_Challenge/assets/48933518/2959c9d6-c8f2-4569-b40d-15a49357030f)

### 2. ¿Cuál fue el uptime total de las aplicaciones app2 y app5 en Q1 2021?

Estableciendo el intervalo de tiempo:

![timerange_question_2_4](https://github.com/AgustinNormand/MELI_Challenge/assets/48933518/cbfce106-e4a7-436d-b0a3-38947508c14e)

Obtenemos:

![answer_question_2](https://github.com/AgustinNormand/MELI_Challenge/assets/48933518/ee2ca7f2-3ef1-4f52-9ebe-222ad5222116)


### 3. ¿Cuál fue el uptime de la aplicación app4 durante Febrero de 2023?

Estableciendo el intervalo de tiempo:

![timerange_question_3](https://github.com/AgustinNormand/MELI_Challenge/assets/48933518/c126c2b0-3f6f-44b6-a586-6fa604f7c898)

Obtenemos:

![answer_question_3](https://github.com/AgustinNormand/MELI_Challenge/assets/48933518/adbd4344-caa7-4135-a95c-79600e4cf06c)

### 4. ¿Cuál fue el uptime de la aplicación app5 durante Q1 del año 2021?

Estableciendo el intervalo de tiempo:

![timerange_question_2_4](https://github.com/AgustinNormand/MELI_Challenge/assets/48933518/dd4d7fcc-2c6c-43a7-841f-8675151c3175)

Obtenemos:

![answer_question_4](https://github.com/AgustinNormand/MELI_Challenge/assets/48933518/b2333338-7fe8-4fcb-8ae9-a175a9adcfba)

### 5. ¿Cuál fue el porcentaje de Downtime para la aplicación app3 el día 20 de Febrero de 2020?

Estableciendo el intervalo de tiempo:

![timerange_question_5](https://github.com/AgustinNormand/MELI_Challenge/assets/48933518/f93b4d19-b9c9-4907-9ba6-983b397d925d)

Obtenemos:

![answer_question_5](https://github.com/AgustinNormand/MELI_Challenge/assets/48933518/3645e56d-89e8-404d-965e-edf432f1d5de)

### Preguntas adicionales

Algunas preguntas similares a las anteriores, pero que si se pueden calcular, por haber datos disponibles, serían por ejemplo:

#### 6. ¿Cuál fue el uptime total de las aplicaciones app2 y app5 en Q1 2022?

Estableciendo el intervalo de tiempo:

![image](https://github.com/AgustinNormand/MELI_Challenge/assets/48933518/b7af7784-f606-4325-a795-2b28689bb700)

Obtenemos:

![image](https://github.com/AgustinNormand/MELI_Challenge/assets/48933518/d933aebd-1540-4c33-9bfe-bdeffc51d3d3)




## Pendientes / Trabajos Futuros

* Usando los timestamps de los registros anteriores a la linea de error "app4-error", estimar la fecha de dicha linea, agregarlo a un bucket de InfluxDB y graficarlo en Grafana.
* Documentar el build del proyecto.

[//]: # (## Build)

[//]: # (### Docker)

[//]: # (```bash)

[//]: # (docker-compose up -d)

[//]: # (```)

[//]: # ()
[//]: # (Instalé la extensión de csv)

[//]: # ()
[//]: # (Agregé las lineas al grafana.ini)

[//]: # ([plugin.marcusolsson-csv-datasource])

[//]: # (allow_local_mode = true)

[//]: # ()
[//]: # (Hice las transformaciones necesarias dentro de grafana para los tipos de datos)

[//]: # ()
[//]: # (https://docs.influxdata.com/influxdb/v2.7/tools/grafana/?t=InfluxQL)
