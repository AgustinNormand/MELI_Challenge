# Desafío 2

## Detalle de la solución planteada

Para resovler el ejercicio en primer lugar analicé el archivo enviado para entender su estructura y los datos que contenía.

Luego preprocesé los datos, para poder cargarlos en una base de datos.

La herramienta elegida para el almacenamiento de los datos fue InfluxDB, ya que es una base de datos orientada a series de tiempo, y los datos que se estaban analizando eran de ese tipo.

Por otro lado, para la visualización de los datos, se utilizó Grafana. Ya que en la entrevista se dijo que estaban utilizando esta herramienta para tareas similares.

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

Obtenemos:

![answer_question_1](https://github.com/AgustinNormand/MELI_Challenge/blob/main/assets/question_1.png)

### 2. ¿Cuál fue el uptime total de las aplicaciones app2 y app5 en Q1 2021?

Obtenemos:

![answer_question_2](https://github.com/AgustinNormand/MELI_Challenge/blob/main/assets/question_2.png)


### 3. ¿Cuál fue el uptime de la aplicación app4 durante Febrero de 2023?

Obtenemos:

![answer_question_3](https://github.com/AgustinNormand/MELI_Challenge/blob/main/assets/question_3.png)

### 4. ¿Cuál fue el uptime de la aplicación app5 durante Q1 del año 2021?

Obtenemos:

![answer_question_4](https://github.com/AgustinNormand/MELI_Challenge/blob/main/assets/question_4.png)

### 5. ¿Cuál fue el porcentaje de Downtime para la aplicación app3 el día 20 de Febrero de 2020?

Obtenemos:

![answer_question_5](https://github.com/AgustinNormand/MELI_Challenge/blob/main/assets/question_5.png)

### Preguntas adicionales

Algunas preguntas similares a las anteriores, pero que si se pueden calcular, por haber datos disponibles, serían por ejemplo:

#### 6. ¿Cuál fue el uptime total de las aplicaciones app2 y app5 en Q1 2022?

Obtenemos:

![image](https://github.com/AgustinNormand/MELI_Challenge/blob/main/assets/question_6.png)

### 7. ¿Cuál fue el uptime de la aplicación app5 durante Q1 del año 2022?

Obtenemos:

![image](https://github.com/AgustinNormand/MELI_Challenge/blob/main/assets/question_7.png)

### 8. ¿Cuál fue el porcentaje de Downtime para la aplicación app3 el día 20 de Febrero de 2023?

Obtenemos:

![image](https://github.com/AgustinNormand/MELI_Challenge/blob/main/assets/question_8.png)

## Build

### Docker

Los pasos que seguí para armar las imagenes de docker fueron:

* docker build -t agustinnormand/app_desafio_2:tag .

* docker push agustinnormand/app_desafio_2:tag

## Pendientes

* Usando los timestamps de los registros anteriores a la linea de error "app4-error", estimar la fecha de dicha linea, agregarlo a un bucket de InfluxDB y graficarlo en Grafana.
* Automatizar la importación del dashboard y la configuración de InfluxDB.
* Mejorar la calidad del código (Modularización, Comentarios, Documentación)

