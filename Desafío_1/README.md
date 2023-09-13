# Desafío 1

## API - Secapp

Si bien, en otra oportunidad para llevar a cabo una tarea similar usé Flask, en este caso para resolver el desafío opté por utilizar FastAPI, si bien previamente investigué Django Rest Framework como otra alternativa, la documentación automatizada de FastAPI, su desempeño competitivo con otros framework de diferentes lenguajes y la flexibilidad con el esquema de bases de datos que se desee utilizar, hicieron que me decida a aprender a utilizarlo para resolver el desafío.

### Documentación

Se encuentra disponible un [sitio](http://34.125.19.164:8000/docs) que proporciona información de los endpoints disponibles, los diferentes métodos HTTP para cada uno de estos, como también los headers esperados.

Además, es posible probar la API dentro de dicho sitio.

### Tests

Se codificaron tests unitarios para la API, verificando el correcto funcionamiento de la misma en diferentes escenarios.

#### test_escenario_1

En este caso, se prueba que el escenario 1 de la consigna esté funcionando, es decir, que el usuario haga POST con los headers y body correspondientes, y que la respuesta de la API sea un status_code 200, y además se le retorne un process_id.

![Test1](https://github.com/AgustinNormand/MELI_Challenge/blob/main/assets/test_1.png)

#### test_escenario_2

Por otro lado, este test valida que el escenario 2 de la consigna esté funcionando, esto significa, que la API no solo permita cambios de criticidad con POST, sino también, obtenerlos mediante peticiones GET.

![Test2](https://github.com/AgustinNormand/MELI_Challenge/blob/main/assets/test_2.png)

#### test_escenario_3

El test_escenario_3, asegura que cuando una aplicación consumidora, ya se encuentra notificada del último estado, la API retorna un json vacío.

![Test3](https://github.com/AgustinNormand/MELI_Challenge/blob/main/assets/test_3.png)

## Producer y Consumer

Se crearon dos pequeñas aplicaciones adicionales, con el propósito de simular un escenario más realista al mantener la base de datos actualizada constantemente y permitir que los clientes de la API desempeñen el papel de consumidores y productores que operan de manera continua. Esto se traduce en gráficos de Grafana que ofrecen una apariencia más auténtica gracias a la constante incorporación de nuevos datos.

Los activé para probar el funcionamiento, sacar un screenshot del dashboard poblado de datos, pero los desactivé para no interferir en las pruebas una vez entregadas las soluciones propuestas.

## Pendientes

* Mejorar la calidad del código (Modularización, Comentarios, Documentación)
* Mejorar la arquitectura
* Agregar tests. (Caso cuando falta el header app_name, cuando falta el token)
* * Load Balancer
* * Queue de mensajes - RabbitMQ, Kafka, Celery
* * Redundancia
* * Orquestado de contenedores
* Tests de stress
* Generar alerta si pasaron más de N minutos y una determinada app consumidora no solicitó estado de criticidad
* En la entrevista hablamos sobre tecnologías como OpenTelemetry, New Relic, Datadog, hubiera sido deseable incluir alguna de estas en la solución.

## Asunciones / Dudas

* Como la consigna no indicaba que una aplicación debía cumplir su rol de productora o consumidora de manera fija, ni hacía una diferencia en el nombre de esta en los headers de ejemplo, asumí que una aplicación X puede tener ambos roles, es decir, puede hacer peticiones GET o POST, consultando o seteando estados.
* Entiendo que los escenarios de ejemplo, son independientes entre sí, sino el segundo de estos, debería haber retornado valor 5 de criticidad, por tener exactamente el mismo timestamp que el mensaje anterior. 