# Intelligent Inventory and Fleet Router (IIFR)

# Database Design Document

**Version:** 1.0

**Domain:** Operations Research, Supply Chain Optimization, Logistics Intelligence

---

# 1. Introduction

## 1.1 Purpose

This document defines the database design for the Intelligent Inventory and Fleet Router (IIFR).

The database stores all operational information required for inventory management, transportation optimization, fleet routing, warehouse allocation, and analytics.

The database is designed to support:

- Inventory tracking.
- Supply chain network representation.
- Optimization model inputs.
- User operations.
- Historical analysis.

---

# 2. Database Architecture

The system follows a relational database architecture.

Development Database:

```
SQLite
```

Production Database:

```
PostgreSQL
```

ORM:

```
SQLAlchemy
```

---

# 3. Database Entity Overview


The major entities are:


```
                    Supplier

                       |

                       |

                  Warehouse

                       |

        ------------------------------

        |                            |

   Inventory                    Distribution Center

        |

        |

      Product


        |

        |

      Order

        |

        |

    Customer


        |

        |

      Truck

        |

        |

    Route


        |

        |

 Road Network
```

---

# 4. Entity Relationship Overview


## Main Entities


| Entity | Purpose |
|---|---|
| User | System users and roles |
| Supplier | Inventory suppliers |
| Warehouse | Storage locations |
| Distribution Center | Regional distribution points |
| Product | Items managed by system |
| Inventory | Stock information |
| Customer | Delivery locations |
| Order | Customer delivery requests |
| Truck | Fleet information |
| Route | Optimized delivery paths |
| Road Network | Graph representation of transportation network |
| Optimization Result | Stores solver outputs |

---

# 5. Database Tables


# 5.1 User Table


## Purpose

Stores system users and access roles.


Table:

```
users
```


Columns:


| Column | Type | Description |
|---|---|---|
| user_id | Integer | Primary Key |
| name | String | User name |
| email | String | Email address |
| password_hash | String | Encrypted password |
| role | String | User role |
| created_at | Timestamp | Account creation time |


Roles:


```
ADMIN

SUPPLY_CHAIN_MANAGER

WAREHOUSE_MANAGER

FLEET_MANAGER

ANALYST
```

---

# 5.2 Supplier Table


## Purpose

Stores supplier information.


Table:

```
suppliers
```


Columns:


| Column | Type | Description |
|---|---|---|
| supplier_id | Integer | Primary Key |
| name | String | Supplier name |
| location | String | Supplier location |
| contact | String | Contact details |
| lead_time | Integer | Delivery lead time |

---

# 5.3 Warehouse Table


## Purpose

Stores warehouse information.


Table:

```
warehouses
```


Columns:


| Column | Type | Description |
|---|---|---|
| warehouse_id | Integer | Primary Key |
| name | String | Warehouse name |
| latitude | Float | Latitude |
| longitude | Float | Longitude |
| capacity | Integer | Maximum storage |
| operating_cost | Float | Fixed operating cost |
| supplier_id | Integer | Foreign Key |


Relationships:

```
Supplier

1

|

Many

Warehouse
```

---

# 5.4 Distribution Center Table


## Purpose

Stores regional distribution locations.


Table:

```
distribution_centers
```


Columns:


| Column | Type |
|---|---|
| dc_id | Integer |
| name | String |
| latitude | Float |
| longitude | Float |
| capacity | Integer |
| warehouse_id | Integer |


Relationship:

```
Warehouse

1

|

Many

Distribution Centers
```

---

# 5.5 Product Table


## Purpose

Stores product information.


Table:

```
products
```


Columns:


| Column | Type |
|---|---|
| product_id | Integer |
| name | String |
| category | String |
| unit_cost | Float |

---

# 5.6 Inventory Table


## Purpose

Stores inventory levels at locations.


Table:

```
inventory
```


Columns:


| Column | Type |
|---|---|
| inventory_id | Integer |
| warehouse_id | Integer |
| product_id | Integer |
| on_hand_stock | Integer |
| reserved_stock | Integer |
| incoming_stock | Integer |
| safety_stock | Integer |
| reorder_point | Integer |


Relationship:


```
Warehouse

1

|

Many

Inventory

Many

|

1

Product
```

---

# 5.7 Customer Table


## Purpose

Stores customer information.


Table:

```
customers
```


Columns:


| Column | Type |
|---|---|
| customer_id | Integer |
| name | String |
| latitude | Float |
| longitude | Float |
| priority | String |

---

# 5.8 Order Table


## Purpose

Stores customer delivery requests.


Table:

```
orders
```


Columns:


| Column | Type |
|---|---|
| order_id | Integer |
| customer_id | Integer |
| product_id | Integer |
| quantity | Integer |
| order_date | Date |
| deadline | Date |
| status | String |


Order Status:


```
CREATED

ALLOCATED

DISPATCHED

DELIVERED

CANCELLED
```

---

# 5.9 Truck Table


## Purpose

Stores fleet information.


Table:

```
trucks
```


Columns:


| Column | Type |
|---|---|
| truck_id | Integer |
| vehicle_number | String |
| capacity | Integer |
| fuel_efficiency | Float |
| status | String |
| current_location | String |


Truck Status:


```
AVAILABLE

BUSY

MAINTENANCE
```

---

# 5.10 Driver Table


## Purpose

Stores driver information.


Table:

```
drivers
```


Columns:


| Column | Type |
|---|---|
| driver_id | Integer |
| name | String |
| license_number | String |
| availability | Boolean |

---

# 5.11 Route Table


## Purpose

Stores optimized routes generated by routing engine.


Table:

```
routes
```


Columns:


| Column | Type |
|---|---|
| route_id | Integer |
| truck_id | Integer |
| start_location | String |
| end_location | String |
| total_distance | Float |
| estimated_time | Float |
| total_cost | Float |

---

# 5.12 Route Node Table


## Purpose

Stores individual stops in a route.


Table:

```
route_nodes
```


Columns:


| Column | Type |
|---|---|
| route_node_id | Integer |
| route_id | Integer |
| node_order | Integer |
| latitude | Float |
| longitude | Float |

---

# 5.13 Road Network Table


## Purpose

Stores graph edges for routing algorithms.


Table:

```
road_network
```


Columns:


| Column | Type |
|---|---|
| edge_id | Integer |
| source_node | String |
| destination_node | String |
| distance | Float |
| travel_time | Float |
| fuel_cost | Float |


Used by:

- Dijkstra
- A*
- VRP

---

# 5.14 Optimization Result Table


## Purpose

Stores optimization outputs.


Table:

```
optimization_results
```


Columns:


| Column | Type |
|---|---|
| result_id | Integer |
| optimization_type | String |
| input_data | JSON |
| output_data | JSON |
| total_cost | Float |
| created_at | Timestamp |


Optimization Types:


```
TRANSPORTATION

ASSIGNMENT

VRP

FACILITY_LOCATION
```

---

# 6. Entity Relationships


## Supplier-Warehouse


```
Supplier

1

|

Many

Warehouse
```


---

## Warehouse-Inventory


```
Warehouse

1

|

Many

Inventory
```


---

## Product-Inventory


```
Product

1

|

Many

Inventory
```


---

## Customer-Order


```
Customer

1

|

Many

Orders
```


---

## Truck-Route


```
Truck

1

|

Many

Routes
```


---

## Route-Route Node


```
Route

1

|

Many

Route Nodes
```

---

# 7. Optimization Data Flow


```
Database

    |

    |

Optimization Service

    |

    |

Prepare Mathematical Model

    |

    |

Solver

(PuLP / OR-Tools)

    |

    |

Optimization Result

    |

    |

Database + Dashboard
```

---

# 8. Indexing Strategy


Indexes should be created on:


Frequently searched fields:


```
warehouse_id

customer_id

product_id

truck_id

order_id

route_id
```


Purpose:

- Faster queries.
- Improved optimization data retrieval.

---

# 9. Data Validation Rules


## Inventory

- Stock cannot be negative.
- Safety stock cannot exceed warehouse capacity.


## Orders

- Quantity must be positive.
- Customer must exist.


## Trucks

- Capacity must be positive.
- Vehicle status must be valid.


## Routes

- Distance cannot be negative.
- Route must contain valid nodes.

---

# 10. Future Database Extensions


Possible future additions:

- Real-time GPS tracking table.
- IoT sensor data table.
- Historical demand table.
- Machine learning forecast table.
- Carbon emission tracking table.
- Blockchain transaction logs.

---

# Conclusion

The proposed database design provides a structured foundation for the Intelligent Inventory and Fleet Router.

The design supports inventory management, supply chain optimization, routing algorithms, and future scalability while maintaining clear relationships between operational entities.

---

**End of Database Design Document v1.0**