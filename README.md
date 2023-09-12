# MELI_Challenge

IP: 34.125.19.164


Pasos para realizar el deploy de la solución:

* Levantar una instancia en un proveedor de cloud

* Agregar las reglas de firewall necesarias

* Instalar Docker (curl -fsSL get.docker.com -o get-docker.sh && sh get-docker.sh)

* Realizar los pasos post instalación (sudo groupadd docker && sudo usermod -aG docker $USER && newgrp docker)

* Instalar Docker-Compose (sudo apt install docker-compose -y)

* git clone https://github.com/AgustinNormand/MELI_Challenge.git

* Moverse al directorio "docker-compose" (cd MELI_Challenge/docker-compose)

* mv .env.example .env

* Completar el archivo .env

* docker-compose up -d

* Agregar la fuente de datos InfluxDB

* Ingresar a Grafana, importar el dashboard usando el archivo .json del Desafío_2.


