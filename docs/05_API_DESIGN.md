# Intelligent Inventory and Fleet Router (IIFR)

# API Design Document

**Version:** 1.0

**Backend Framework:** FastAPI

**API Style:** RESTful Architecture

---

# 1. Introduction

## 1.1 Purpose

This document defines the REST API architecture for the Intelligent Inventory and Fleet Router (IIFR).

The API layer acts as a communication bridge between the frontend dashboard and backend services.

The API provides interfaces for:

- Inventory management.
- Warehouse management.
- Customer and order management.
- Fleet management.
- Optimization execution.
- Route generation.
- Analytics generation.

---

# 2. API Architecture


```
React Dashboard

        |

        |

REST API Requests

        |

        |

FastAPI Backend

        |

        |

Service Layer

        |

        |

Optimization Engines

        |

        |

Database
```

---

# 3. API Design Principles

The API follows:

- REST architecture.
- JSON request and response format.
- Stateless communication.
- Modular endpoint organization.
- Input validation using Pydantic models.

---

# 4. Base URL Structure

Development:

```
http://localhost:8000/api
```

Production:

```
https://domain.com/api
```

---

# 5. API Authentication

Future implementation:

Authentication method:

```
JWT Token Based Authentication
```

Each request will contain:

```
Authorization: Bearer <token>
```

---

# 6. API Modules

The API is divided into:

1. Authentication API
2. Warehouse API
3. Inventory API
4. Customer API
5. Order API
6. Fleet API
7. Optimization API
8. Routing API
9. Analytics API

---

# 7. Authentication APIs

---

## POST /auth/login

### Purpose

Authenticate user.


### Request

```json
{
    "email": "user@example.com",
    "password": "password"
}
```


### Response

```json
{
    "access_token": "jwt_token",
    "role": "ADMIN"
}
```

---

# 8. Warehouse APIs

---

## POST /warehouses

### Purpose

Create a new warehouse.


### Request

```json
{
    "name": "Warehouse A",
    "latitude": 12.9716,
    "longitude": 77.5946,
    "capacity": 5000
}
```


### Response

```json
{
    "warehouse_id":1,
    "status":"created"
}
```

---

## GET /warehouses

### Purpose

Retrieve all warehouses.


Response:

```json
[
 {
  "warehouse_id":1,
  "name":"Warehouse A",
  "capacity":5000
 }
]
```

---

## GET /warehouses/{id}

Retrieve warehouse details.


---

## PUT /warehouses/{id}

Update warehouse information.


---

## DELETE /warehouses/{id}

Delete warehouse.

---

# 9. Inventory APIs

---

## GET /inventory

### Purpose

Retrieve inventory status.


Response:

```json
{
 "warehouse":"Warehouse A",
 "product":"Laptop",
 "stock":500,
 "safety_stock":100,
 "reorder_point":150
}
```

---

## PUT /inventory/{id}

Update inventory.


Request:

```json
{
 "quantity":200
}
```

---

# 10. Inventory Optimization APIs


# POST /inventory/eoq


## Purpose

Calculate Economic Order Quantity.


Input:


```json
{
 "annual_demand":10000,
 "ordering_cost":500,
 "holding_cost":20
}
```


Processing:

```
EOQ = sqrt((2DS)/H)
```


Response:

```json
{
 "EOQ":707
}
```

---

# POST /inventory/safety-stock


## Purpose

Calculate safety stock.


Input:

```json
{
 "service_level":1.65,
 "demand_std":20,
 "lead_time":5
}
```


Response:

```json
{
 "safety_stock":74
}
```

---

# POST /inventory/reorder-point


## Purpose

Calculate reorder point.


Response:

```json
{
 "ROP":300
}
```

---

# 11. Customer APIs


## POST /customers

Create customer.


Request:

```json
{
"name":"Customer A",
"latitude":12.5,
"longitude":77.4,
"demand":100
}
```

---

## GET /customers

Retrieve customers.

---

# 12. Order APIs


## POST /orders


Create delivery order.


Request:

```json
{
"customer_id":1,
"product_id":5,
"quantity":100,
"deadline":"2026-08-20"
}
```


Response:

```json
{
"order_id":10,
"status":"created"
}
```

---

## GET /orders


Retrieve orders.

---

## PUT /orders/{id}/status


Update order status.


Example:


```json
{
"status":"DISPATCHED"
}
```

---

# 13. Fleet APIs


## POST /trucks


Add vehicle.


Request:

```json
{
"vehicle_number":"KA01AB1234",
"capacity":500,
"fuel_efficiency":15
}
```

---

## GET /trucks


Retrieve fleet information.


---

## PUT /trucks/{id}/status


Update truck availability.


Example:


```json
{
"status":"AVAILABLE"
}
```

---

# 14. Transportation Optimization APIs


# POST /optimization/transportation


## Purpose

Solve warehouse-to-customer allocation problem.


Input:

```json
{
"warehouses":[
{
"id":1,
"supply":500
}
],

"customers":[
{
"id":1,
"demand":200
}
],

"cost_matrix":[
[5,7],
[6,4]
]
}
```


Processing:

Linear Programming Model:


```
Minimize:

Z = ΣΣ cij*xij
```


Constraints:

- Supply constraints.
- Demand constraints.
- Non-negative variables.


Response:

```json
{
"minimum_cost":4500,

"allocation":[

{
"warehouse":1,
"customer":2,
"quantity":200
}

]
}
```

---

# 15. Assignment Optimization API


# POST /optimization/assignment


## Purpose

Assign resources optimally.


Examples:

- Truck to order.
- Driver to route.


Input:

```json
{
"cost_matrix":[
[10,20],
[15,5]
]
}
```


Response:

```json
{
"assignment":[

{
"truck":1,
"order":2
}

]
}
```

---

# 16. Routing APIs


# POST /routing/shortest-path


## Purpose

Find shortest route.


Input:

```json
{
"source":"Warehouse A",
"destination":"Customer B"
}
```


Processing:

Algorithms:

- Dijkstra.
- A*.


Response:

```json
{
"path":[
"A",
"B",
"C"
],

"distance":25
}
```

---

# POST /routing/optimize


## Purpose

Solve Vehicle Routing Problem.


Input:


```json
{
"vehicles":10,

"customers":100,

"capacity":500
}
```


Processing:

Google OR-Tools CVRP.


Response:


```json
{
"routes":[

{
"vehicle":1,
"path":[1,5,7,1],
"distance":45
}

]
}
```

---

# 17. Analytics APIs


# GET /analytics/dashboard


Purpose:

Return dashboard metrics.


Response:

```json
{
"inventory_value":500000,

"transport_cost":25000,

"fleet_utilization":85,

"stockouts":3
}
```

---

# GET /analytics/inventory-trend


Returns inventory history.


---

# GET /analytics/cost-analysis


Returns:


- Transportation cost.
- Holding cost.
- Stockout cost.

---

# 18. Scenario Analysis API


# POST /scenario/simulate


Purpose:

Perform what-if analysis.


Input:


```json
{
"demand_change":20,

"fuel_cost_change":10,

"warehouse_failure":"W2"
}
```


Output:


```json
{
"new_cost":45000,

"new_routes":[]
}
```

---

# 19. Error Handling


All APIs follow common error format.


Example:


```json
{
"error":"Warehouse not found",

"status_code":404
}
```

---

# 20. HTTP Status Codes


| Code | Meaning |
|---|---|
|200|Successful Request|
|201|Created|
|400|Bad Request|
|401|Unauthorized|
|404|Resource Not Found|
|500|Internal Server Error|

---

# 21. API Versioning


Future versions:

```
/api/v1/

/api/v2/
```

Example:

```
/api/v1/inventory/eoq
```

---

# 22. Future API Extensions

Possible future APIs:

- Real-time GPS tracking.
- IoT inventory updates.
- Machine learning forecasting.
- Carbon emission optimization.
- Blockchain supply chain tracking.

---

# Conclusion

The API design provides a structured communication interface between the frontend dashboard, backend services, optimization engines, and database.

The modular API structure allows independent development and future extension of additional supply chain optimization capabilities.

---

**End of API Design Document v1.0**