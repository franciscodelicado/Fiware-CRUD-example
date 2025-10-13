# Ejemplos de operaciones por lotes en NGSI-v2
Para este ejemplo simularemos un escenario de una tienda de alimentación que quiere gestionar la información de sus productos utilizando Fiware y NGSI-v2. La tienda tiene varios productos, cada uno con atributos como nombre, categoría, precio y cantidad en stock. Queremos realizar varias operaciones por lotes para gestionar estos productos de manera eficiente.

## Requisitos

- Tener un entorno Fiware con Orion Context Broker y MongoDB en funcionamiento.

- Herramienta para realizar peticiones HTTP, como Postman o cUrl.

- Herramienta `git` para clonar el repositorio con los ejemplos.

Para desplegar un entorno Fiware con Orion y MongoDB, realizaremos las siguientes acciones:

```bash
git clone https://github.com/franciscodelicado/Fiware-CRUD-example.git
cd Fiware-CRUD-example
git checkout batch

./services start
```

## Crear entidades por lotes
Agregaremos varios productos a la tienda en una sola operación. Crearemos tres productos con sus respectivos atributos, según las especificaciones de la siguiente tabla:

| `id`          | `type`    | Atributos                                      |
|---------------|-----------|------------------------------------------------|
| `0001`       | `Product` | `name`: "Manzana", `category`: "Frutas", `price`: 0.5, `stock`: 100 |
| `0002`       | `Product` | `name`: "Leche", `category`: "Lácteos", `price`: 1.0, `stock`: 50   |
| `0003`       | `Product` | `name`: "Pan", `category`: "Panadería", `price`: 1.5, `stock`: 30   |

Realizaremos una petición **POST** al endpoint **`/v2/op/update`** con el siguiente "_payload_":

```json
{
  "actionType": "append",
  "entities": [
    {
      "id": "urn:ngsi-ld:Product:0001",
      "type": "Product",
      "name": { "value": "Manzana", "type": "Text" },
      "category": { "value": "Frutas", "type": "Text" },
      "price": { "value": 0.5, "type": "Number", "metadata": { "unitCode": { "value": "EUR", "type": "Text" } } },
      "stock": { "value": 100, "type": "Number" }
    },
    {
      "id": "urn:ngsi-ld:Product:0002",
      "type": "Product",
      "name": { "value": "Leche", "type": "Text" },
      "category": { "value": "Lácteos", "type": "Text" },
      "price": { "value": 1.0, "type": "Number", "metadata": { "unitCode": { "value": "EUR", "type": "Text" } } },
      "stock": { "value": 50, "type": "Number" }
    },
    {
      "id": "urn:ngsi-ld:Product:0003",
      "type": "Product",
      "name": { "value": "Pan", "type": "Text" },
      "category": { "value": "Panadería", "type": "Text" },
      "price": { "value": 1.5, "type": "Number", "metadata": { "unitCode": { "value": "EUR", "type": "Text" } } },
      "stock": { "value": 30, "type": "Number" }
    }
  ]
}
```

## Añadir atributos por lotes
Supongamos que queremos añadir un nuevo atributo `supplier` (proveedor) a todos los productos existentes. Realizaremos una petición **POST** al endpoint **`/v2/op/update`** con el siguiente "_payload_":  

```json
{
  "actionType": "append_strict",
  "entities": [
    {
      "id": "urn:ngsi-ld:Product:0001",
      "type": "Product",
      "supplier": { "value": "Proveedor A", "type": "Text" }
    },
    {
      "id": "urn:ngsi-ld:Product:0002",
      "type": "Product",
      "supplier": { "value": "Proveedor B", "type": "Text" }
    },
    {
      "id": "urn:ngsi-ld:Product:0003",
      "type": "Product",
      "supplier": { "value": "Proveedor C", "type": "Text" }
    }
  ]
}
```

## Añadir distintos atributos a cada entidad por lotes
Añadiremos distintos atributos a cada producto. En concreto a los `Lácteos` le añadiremos el atributo `expirationDate` (fecha de caducidad), y a los productos de la categoría `Panadería` le añadiremos el atributo `weight` (peso). Realizaremos una petición **POST** al endpoint **`/v2/op/update`** con el siguiente "_payload_":  

```json
{
  "actionType": "append_strict",
  "entities": [
    {
      "id": "urn:ngsi-ld:Product:0002",
      "type": "Product",
      "expirationDate": { "value": "2027-12-31", "type": "DateTime" }
    },
    {
      "id": "urn:ngsi-ld:Product:0003",
      "type": "Product",
      "weight": { "value": 0.250, "type": "Number", "metadata": { "unitCode": { "value": "KGM", "type": "Text" } } }
    }
  ]
}
```

## Actualizar atributos por lotes
Supongamos que queremos actualizar el precio y el stock de varios productos. Realizaremos una petición **POST** al endpoint **`/v2/op/update`** con el siguiente "_payload_":

```json
{
  "actionType": "update",
  "entities": [
    {
      "id": "urn:ngsi-ld:Product:0001",
      "type": "Product",
      "price": { 
        "value": 0.6
        }
    },
    {
      "id": "urn:ngsi-ld:Product:0002",
      "type": "Product",
      "price": { 
        "value": 1.1 
      }
    },
    {
      "id": "urn:ngsi-ld:Product:0003",
      "type": "Product",
      "stock": { 
        "value": 25 
      }
    }
  ]
}
```

## Eliminar atributos por lotes
Supongamos que queremos eliminar el atributo `supplier` de todas las frutas, y el stock de los productos de panadería. Realizaremos una petición **POST** al endpoint **`/v2/op/update`** con el siguiente "_payload_":

```json
{
  "actionType": "delete",
  "entities": [
    {
      "id": "urn:ngsi-ld:Product:0001",
      "type": "Product",
      "supplier": {}
    },
    {
      "id": "urn:ngsi-ld:Product:0003",
      "type": "Product",
      "stock": {}
    }
  ]
}
```

# CONSULTAS por lotes
Supongamos que queremos recuperar información de todos los productos cuyo precio sea inferior a 1 euro, pero solo los atributos `name`, `price` y `stock`. Realizaremos una petición **POST** al endpoint **`/v2/op/query`** con el siguiente "_payload_":

```json
{
  "entities": [
    {
      "idPattern" : ".*",
      "type": "Product"
    }
  ],
  "attrs": ["name", "price", "stock"],
  "expression": { "q" : "price<1" }
}
```
