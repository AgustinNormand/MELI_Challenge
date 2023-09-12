# MELI_Challenge

Se hizo un deploy de las soluciones a los desafíos en una instancia de Google Cloud Platform.

La misma se encuentra en la región us-west4, zona us-west4-a, se trata de una instancia de tipo e2-standard-8.
Configurada con un disco de 20GB y Ubuntu 22.04LTS.

Se configuraron las reglas de firewall necesarias para permitir el acceso a los diferentes servicios.

Se utilizó docker-compose para el manejo de los contenedores.

IP: 34.125.19.164


Pasos para realizar el deploy de la solución:

* Instalar Docker (curl -fsSL get.docker.com -o get-docker.sh && sh get-docker.sh)

* Realizar los pasos post instalación (sudo groupadd docker && sudo usermod -aG docker $USER && newgrp docker)

* Instalar Docker-Compose (sudo apt install docker-compose -y)

* git clone https://github.com/AgustinNormand/MELI_Challenge.git

* Moverse al directorio "docker-compose" (cd docker-compose)

* mv .env.example .env

* Completar el archivo .env

* docker-compose up -d


