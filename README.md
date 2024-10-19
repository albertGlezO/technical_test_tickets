# Prueba técnica

El repositorio fue creado con la finalidad de realizar una prueba técnica, referente a un servicio que llevar a cabo la administración de boletos de eventos.


## Instalación

#### 1.- Usar la herramienta [docker-compose](https://docs.docker.com/compose/) para realizar la construcción y levantamiento de los contenedores.

```bash
docker-compose build
```
```bash
docker-compose up
```

#### 2.- Para la instalación de la base de datos deberemos acceder al contenedor

```bash
docker exec -it tickets_db bash
```
Después ejecutaremos el script que realizara la creación de la base de datos y sus tablas

```bash
mysql --host=127.0.0.1 --port=3306 -u root -p < usr/local/mysql/db.sql
```
Nos pedirá ingresar la contraseña

```bash
Enter password: p4ss_r007
```
Una vez finalizada la operación podemos salir del contenedor

```bash
exit
```
## Estructura del proyecto
    .
    ├── app                                            
    │   ├── controllers
    │   │   ├── base_controller.py
    │   │   ├── event_controller.py
    │   │   └── ticket_controller.py
    │   ├── database
    │   │   └── mysql_db.py
    │   ├── models
    │   │   ├── event_models.py
    │   │   └── ticket_models.py
    │   ├── routes
    │   │   ├── event_routes.py
    │   │   └── ticket_routes.py
    │   ├── test
    │   │   ├── unit
    │   │   │   ├── test_event_constroller.py
    │   │   │   ├── test_event_models.py
    │   │   │   ├── test_ticket_constroller.py
    │   │   │   ├── test_ticket_models.py
    │   └── __init__.py
    ├── tickets-db                                    
    │   └── db.sql                                    
    ├── .gitignore                                    
    ├── config.py                                     
    ├── docker-compose.yaml                           
    ├── Dockerfile                                    
    ├── README.md                                     
    ├── requirements.txt                              
    └── run.py             

## Estructura de la base de datos
![](utils/BD.png)   

## Pruebas unitarias
Para realizar la ejecución de las pruebas unitarias sera con el siguiente comando

```bash
python -m unittest app/test/unit/*.py
```

Como resultado mostrara la cantidad de pruebas ejecutadas y cuantas fueron exitosas

```bash
............
----------------------------------------------------------------------
Ran 12 tests in 0.400s

OK
```

## REST API
A continuación se describen los servicios rest contenidos

### Obtener todos los eventos

#### Petición
```bash
GET /events

curl --location 'http://127.0.0.1:5000/events'
```

#### Respuesta
```bash
{
    "status": true,
    "status_code": 200,
    "message": "Success",
    "data": [
        {
            "id": 1,
            "total_tickets": 300,
            "to_datetime": "2024-10-27 20:00:00",
            "total_ticket_redeem": 300,
            "name": "Gran premio de mexico",
            "from_datetime": "2024-10-25 08:00:00",
            "total_ticket_sales": 300
        }
    ]
}
```

### Obtener un evento

#### Petición
```bash
GET /events/{event_id}

curl --location 'http://127.0.0.1:5000/events/{event_id}'
```

#### Respuesta
```bash
{
    "status": true,
    "status_code": 200,
    "message": "Success",
    "data": {
        "id": 1,
        "total_tickets": 200,
        "to_datetime": "2024-10-27 20:00:00",
        "total_ticket_redeem": 0,
        "from_datetime": "2024-10-25 08:00:00",
        "name": "Gran premio de mexico",
        "total_ticket_sales": 0
    }
}
```

### Crear un evento

#### Petición
```bash
POST /events

curl --location 'http://127.0.0.1:5000/events' \
--header 'Content-Type: application/json' \
--data '{
    "to_datetime": "2024-10-27 20:00:00",
    "from_datetime": "2024-10-25 08:00:00"
    "name": "Gran premio de mexico",
    "total_tickets": 200,
}'
```

#### Respuesta
```bash
{
    "status": true,
    "status_code": 200,
    "message": "Create successful",
    "data": {
        "id": 3,
        "name": "Gran premio de mexico",
        "from_datetime": "2024-10-25 08:00:00",
        "to_datetime": "2024-10-27 20:00:00",
        "total_tickets": 200,
        "total_ticket_sales": 0,
        "total_ticket_redeem": 0
    }
}
```
### Actualizar un evento

#### Petición
```bash
PUT /events/{event_id}

curl --location --request PUT 'http://127.0.0.1:5000/events/{event_id}' \
--header 'Content-Type: application/json' \
--data '{
    "name": "Gran premio de mexico",
    "from_datetime": "2024-10-25 08:00:00",
    "to_datetime": "2024-10-27 20:00:00",
    "total_tickets": 200
}'
```

#### Respuesta
```bash
{
    "status": true,
    "status_code": 200,
    "message": "Update successful",
    "data": {
        "id": "1",
        "name": "Gran premio de mexico",
        "from_datetime": "2024-10-25 08:00:00",
        "to_datetime": "2024-10-27 20:00:00",
        "total_tickets": 200,
        "total_ticket_sales": 0,
        "total_ticket_redeem": 0
    }
}
```

### Eliminar un evento

#### Petición
```bash
DELETE /events/{event_id}

curl --location --request DELETE 'http://127.0.0.1:5000/events/{event_id}'
```

#### Respuesta
```bash
{
    "status": true,
    "status_code": 200,
    "message": "Destroy successful",
    "data": {
        "affected_rows": 1
    }
}
```

### Obtener boletos de un evento

#### Petición
```bash
GET /events/{event_id}/tickets

curl --location 'http://127.0.0.1:5000/events/{event_id}/tickets'
```

#### Respuesta
```bash
{
    "status": true,
    "status_code": 200,
    "message": "Success",
    "data": [
        {
            "event_id": 1,
            "id": 1,
            "redeem": 0,
            "ticket_hash": "cd2e3787-9afc-45ba-802f-093819fd7010"
        }
    ]
}
```

### Comprar boleto de un evento

#### Petición
```bash
POST /events/{event_id}/tickets

curl --location --request POST 'http://127.0.0.1:5000/events/{event_id}/tickets'
```

#### Respuesta
```bash
{
    "status": true,
    "status_code": 200,
    "message": "Create successful",
    "data": {
        "id": 1,
        "event_id": 1,
        "event_name": "Gran premio de mexico",
        "ticket_hash": "cd2e3787-9afc-45ba-802f-093819fd7010",
        "redeem": 0
    }
}
```

### Canjear boleto de evento

#### Petición
```bash
PATCH /events/{event_id}/tickets/{ticket_id}/redeem

curl --location --request PATCH 'http://127.0.0.1:5000/events/{event_id}/tickets/{ticket_id}/redeem'
```

#### Respuesta
```bash
{
    "status": true,
    "status_code": 200,
    "message": "Update successful",
    "data": {
        "id": 1,
        "event_id": 1,
        "event_name": "Gran premio de mexico",
        "ticket_hash": "cd2e3787-9afc-45ba-802f-093819fd7010",
        "redeem": 1
    }
}
```