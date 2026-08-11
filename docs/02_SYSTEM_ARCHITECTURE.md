# Intelligent Inventory and Fleet Router (IIFR)

# System Architecture Document

**Version:** 1.0

**Domain:** Operations Research, Supply Chain Optimization, Logistics Intelligence

---

# 1. Introduction

## 1.1 Purpose

This document describes the system architecture of the Intelligent Inventory and Fleet Router (IIFR).

The architecture defines the major software components, their responsibilities, communication flow, data flow, and interaction between inventory management, routing optimization, mathematical optimization engines, database systems, and visualization layers.

The architecture is designed to support modular development, scalability, maintainability, and integration of additional Operations Research algorithms in the future.

---

# 2. Architectural Overview

The Intelligent Inventory and Fleet Router follows a layered modular architecture.

The major layers are:

1. Presentation Layer
2. API Layer
3. Business Logic Layer
4. Optimization Engine Layer
5. Data Access Layer
6. Database Layer


High-level architecture:

```
                         USER

                           |

                  Presentation Layer

                           |

                 React Dashboard

                           |

                    API Layer

                           |

                  FastAPI Backend

                           |

              Business Logic Layer

                           |

        -----------------------------------

        |                |                |

 Inventory Service   Routing Service   Optimization Service

        |                |                |

        -----------------------------------

                  Optimization Engine

        -----------------------------------

        |                |                |

 Inventory Models   Graph Algorithms   OR Solvers

 EOQ              Dijkstra            PuLP

 ROP              A*                  OR-Tools

 Forecasting      VRP                 MILP


                           |

                  Data Access Layer

                           |

                    Database Layer

                           |

              SQLite / PostgreSQL
```

---

# 3. Architecture Principles

The system follows the following design principles.

---

## 3.1 Modularity

Each major functionality is implemented as an independent module.

Examples:

- Inventory Engine
- Routing Engine
- Optimization Engine
- Dashboard

This allows individual components to be modified or extended without affecting the complete system.

---

## 3.2 Separation of Concerns

Each layer has a specific responsibility.

Example:

Frontend:

- User interaction.
- Visualization.

Backend API:

- Request handling.
- Response generation.

Optimization Layer:

- Mathematical computation.

Database:

- Data storage.

---

## 3.3 Extensibility

The architecture allows future integration of:

- Machine Learning forecasting models.
- Real-time traffic data.
- Advanced optimization algorithms.
- IoT inventory sensors.

---

# 4. System Components

---

# 4.1 Presentation Layer

## Technology

- React
- Leaflet
- Chart.js
- Material UI


## Responsibility

The presentation layer provides an interactive interface for users.

It communicates with the backend through REST APIs.


## Features

### Dashboard

Displays:

- Inventory status.
- Fleet status.
- Optimization results.
- Supply chain KPIs.


### Map Visualization

Displays:

- Warehouses.
- Customers.
- Vehicle routes.


### Scenario Analysis

Allows users to modify:

- Demand.
- Fuel cost.
- Inventory parameters.

and observe optimization changes.

---

# 4.2 API Layer

## Technology

FastAPI


## Responsibility

The API layer acts as the communication bridge between frontend and backend services.


## Responsibilities

- Receive user requests.
- Validate input data.
- Call appropriate services.
- Return optimization results.


Example:

```
User Request

POST /optimize/transportation


↓

FastAPI


↓

Optimization Service


↓

PuLP Solver


↓

Response
```

---

# 4.3 Business Logic Layer

## Purpose

The business logic layer manages operational workflows.

The API layer should not directly communicate with optimization algorithms.

Instead:

```
API

↓

Service Layer

↓

Optimization Engine
```


This improves:

- Maintainability.
- Testing.
- Code organization.


---

# 4.3.1 Inventory Service

Responsibilities:

- Manage inventory operations.
- Calculate inventory metrics.
- Trigger replenishment workflows.


Functions:

```
calculate_eoq()

calculate_safety_stock()

calculate_reorder_point()

generate_alert()
```

---

# 4.3.2 Routing Service

Responsibilities:

- Manage delivery requests.
- Create route optimization requests.
- Process route results.


Functions:

```
create_route()

calculate_shortest_path()

optimize_vehicle_routes()
```

---

# 4.3.3 Optimization Service

Responsibilities:

- Prepare optimization inputs.
- Execute mathematical models.
- Process solver outputs.


Functions:

```
solve_transportation_problem()

solve_assignment_problem()

solve_facility_location()
```

---

# 5. Optimization Engine Layer

The optimization engine contains all Operations Research algorithms.

---

# 5.1 Inventory Optimization Module

## Algorithms

### Economic Order Quantity

Formula:

```
EOQ = sqrt((2DS)/H)
```

where:

D = Annual demand

S = Ordering cost

H = Holding cost


---

### Safety Stock

Formula:

```
SS = Z × σd × √L
```

where:

Z = Service level factor

σd = Demand variation

L = Lead time


---

### Reorder Point

Formula:

```
ROP = (Average Daily Demand × Lead Time) + Safety Stock
```

---

# 5.2 Network Optimization Module

## Graph Representation

The supply chain network is represented as:

```
G = (V,E)
```

where:

V:

- Warehouses
- Depots
- Customers


E:

- Roads
- Transportation links


---

## Algorithms

### Dijkstra Algorithm

Purpose:

Find shortest path between two nodes.


Input:

- Source node.
- Destination node.


Output:

- Minimum distance route.


---

### A* Algorithm

Purpose:

Heuristic-based shortest path search.


---

# 5.3 Vehicle Routing Module

## Technology

Google OR-Tools


## Problem

Capacitated Vehicle Routing Problem (CVRP)


Objective:

Minimize:

```
Total Distance + Transportation Cost
```


Constraints:

- Vehicle capacity.
- Customer demand.
- Depot starting point.
- Depot return.


Output:

- Vehicle assignment.
- Route sequence.
- Total distance.

---

# 5.4 Mathematical Optimization Module

## Linear Programming

Technology:

PuLP


Used for:

- Transportation problem.
- Resource allocation.


Model:

```
Minimize:

Z = ΣΣ cij*xij
```


Constraints:

- Supply constraints.
- Demand constraints.


---

## Assignment Optimization

Used for:

- Truck assignment.
- Order assignment.


Techniques:

- Hungarian Algorithm.
- MILP.


---

## Facility Location Optimization

Future extension:

Used for:

- Warehouse selection.
- Distribution center planning.


Technique:

Mixed Integer Linear Programming.

---

# 6. Data Access Layer

## Purpose

Provides communication between application logic and database.


Responsibilities:

- Database queries.
- Data insertion.
- Data updates.
- Data retrieval.


Technology:

- SQLAlchemy ORM.


---

# 7. Database Layer

## Development Database

SQLite


## Production Database

PostgreSQL


---

# Database Entities


## Warehouse

Stores:

- Warehouse information.
- Location.
- Capacity.
- Inventory.


---

## Customer

Stores:

- Customer details.
- Demand.
- Location.


---

## Truck

Stores:

- Vehicle information.
- Capacity.
- Availability.


---

## Order

Stores:

- Delivery requests.
- Customer requirements.


---

## Inventory

Stores:

- Product quantity.
- Stock levels.
- Reorder information.


---

## Road Network

Stores:

- Nodes.
- Edges.
- Distance.
- Travel time.


---

# 8. Complete System Workflow


```
Customer Order Generated

          |

          ↓

Demand Analysis

          |

          ↓

Inventory Availability Check

          |

          ↓

Warehouse Allocation Optimization

          |

          ↓

Transportation Optimization

          |

          ↓

Vehicle Assignment

          |

          ↓

Route Optimization

          |

          ↓

Delivery Execution

          |

          ↓

Inventory Update

          |

          ↓

Dashboard Update
```

---

# 9. Backend Folder Mapping


```
backend/

│

├── app/

│   ├── api/

│   │    └── REST endpoints

│   │

│   ├── services/

│   │    ├── inventory_service.py

│   │    ├── routing_service.py

│   │    └── optimization_service.py

│   │

│   ├── optimization/

│   │    ├── inventory/

│   │    ├── routing/

│   │    └── allocation/

│   │

│   ├── models/

│   │    ├── warehouse.py

│   │    ├── customer.py

│   │    ├── truck.py

│   │    └── order.py

│   │

│   ├── database/

│   │

│   └── main.py
```

---

# 10. Future Architecture Extensions

Future versions may include:

- Message queue for asynchronous optimization.
- Cloud deployment.
- Distributed optimization.
- Real-time traffic services.
- Machine learning forecasting service.
- IoT inventory monitoring.


---

# Conclusion

The proposed architecture provides a modular, scalable, and maintainable foundation for the Intelligent Inventory and Fleet Router.

The separation between user interface, business logic, optimization algorithms, and data storage enables independent development and future extension of advanced supply chain optimization capabilities.

---

**End of System Architecture Document v1.0**