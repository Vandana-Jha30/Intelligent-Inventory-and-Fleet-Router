# Intelligent Inventory and Fleet Router (IIFR)

# Use Case Document

**Version:** 1.0

**Domain:** Operations Research, Supply Chain Optimization, Logistics Intelligence

---

# 1. Introduction

## 1.1 Purpose

This document describes the user interactions and operational workflows of the Intelligent Inventory and Fleet Router (IIFR).

The purpose of this document is to identify system actors, their responsibilities, and the major use cases supported by the platform.

The use cases define how different stakeholders interact with inventory management, fleet routing, optimization modules, and analytics dashboards.

---

# 2. System Actors

The system consists of the following primary actors:

| Actor | Description |
|---|---|
| System Administrator | Manages system configuration, users, and operational parameters |
| Supply Chain Manager | Monitors supply chain operations and executes optimization decisions |
| Warehouse Manager | Maintains warehouse inventory information |
| Fleet Manager | Manages vehicles and delivery operations |
| Logistics Planner | Executes transportation and routing optimization |
| Business Analyst | Analyzes reports and operational KPIs |

---

# 3. Actor Responsibilities


# 3.1 System Administrator

Responsibilities:

- Manage user accounts.
- Configure system parameters.
- Manage database configuration.
- Maintain system availability.
- Monitor system performance.

---

# 3.2 Supply Chain Manager

Responsibilities:

- Monitor overall supply chain status.
- View inventory analytics.
- Review optimization recommendations.
- Perform scenario analysis.
- Make strategic decisions.

---

# 3.3 Warehouse Manager

Responsibilities:

- Add warehouse information.
- Update inventory levels.
- Monitor stock availability.
- Receive replenishment alerts.
- Update incoming and outgoing inventory.

---

# 3.4 Fleet Manager

Responsibilities:

- Register vehicles.
- Monitor vehicle availability.
- Assign vehicles.
- Track optimized routes.
- Monitor delivery operations.

---

# 3.5 Logistics Planner

Responsibilities:

- Execute transportation optimization.
- Generate delivery routes.
- Run vehicle routing algorithms.
- Analyze optimization results.

---

# 3.6 Business Analyst

Responsibilities:

- View dashboards.
- Analyze operational metrics.
- Generate reports.
- Compare optimization scenarios.

---

# 4. Use Case Diagram (High Level)


```
                    System Administrator

                              |

                              |

                      Configure System


                              |

                              |

Supply Chain Manager ---- Dashboard ---- Business Analyst


                              |

                              |

                 Optimization Services


        /              |              \


Inventory          Routing          Allocation

Manager            Manager          Planner


        |              |              |


       EOQ            VRP          Transportation

       ROP            Dijkstra     Assignment

       Forecast       Routes       LP/MILP

```

---

# 5. Inventory Management Use Cases


# UC-01: Add Warehouse

## Actor

Warehouse Manager


## Description

Allows the user to add a new warehouse into the system.


## Preconditions

- User is authenticated.
- User has warehouse management permission.


## Main Flow

1. User opens warehouse management page.
2. User enters warehouse information.
3. System validates the data.
4. System stores warehouse details.
5. Warehouse becomes available for optimization.


## Input

- Warehouse name.
- Location.
- Storage capacity.
- Initial inventory.


## Output

New warehouse record created.


---

# UC-02: Update Inventory

## Actor

Warehouse Manager


## Description

Updates stock information after receiving or dispatching inventory.


## Main Flow

1. User selects warehouse.
2. User enters inventory changes.
3. System updates stock balance.
4. Inventory metrics are recalculated.


## Output

Updated inventory status.


---

# UC-03: Calculate EOQ


## Actor

Supply Chain Manager


## Description

Calculates optimal order quantity using Economic Order Quantity model.


## Input

- Annual demand.
- Ordering cost.
- Holding cost.


## Processing

System calculates:

```
EOQ = sqrt((2DS)/H)
```


## Output

Recommended order quantity.


---

# UC-04: Generate Reorder Alert


## Actor

Inventory Engine


## Description

Automatically generates alerts when inventory reaches reorder threshold.


## Processing

System checks:

```
Inventory Position <= Reorder Point
```


## Output

Alert:

- Critical
- Warning
- Information


---

# 6. Transportation Optimization Use Cases


# UC-05: Optimize Warehouse Allocation


## Actor

Logistics Planner


## Description

Determines the optimal warehouse-to-customer shipment plan.


## Preconditions

- Warehouse data available.
- Customer demand available.
- Transportation cost matrix available.


## Main Flow

1. User selects optimization request.
2. System loads supply and demand data.
3. Transportation model is generated.
4. Linear Programming solver executes.
5. Results are returned.


## Input

- Warehouse capacity.
- Customer demand.
- Shipping cost.


## Processing

Optimization model:

```
Minimize:

Z = ΣΣ cij*xij
```


## Output

- Shipment quantity.
- Selected warehouse.
- Minimum transportation cost.


---

# 7. Fleet Routing Use Cases


# UC-06: Generate Shortest Route


## Actor

Fleet Manager


## Description

Finds the shortest path between two locations.


## Input

- Source location.
- Destination location.
- Road network.


## Processing

Algorithm:

- Dijkstra Algorithm.
- A* Search.


## Output

- Shortest route.
- Distance.
- Estimated travel time.


---

# UC-07: Optimize Vehicle Routes


## Actor

Logistics Planner


## Description

Generates optimal routes for multiple vehicles.


## Preconditions

- Vehicle information available.
- Customer orders available.


## Main Flow

1. User starts routing optimization.
2. System creates routing model.
3. OR-Tools solves CVRP.
4. Optimized routes are generated.


## Constraints

- Vehicle capacity.
- Customer demand.
- Depot constraints.


## Output

- Vehicle assignment.
- Route sequence.
- Total distance.
- Estimated cost.


---

# 8. Assignment Optimization Use Cases


# UC-08: Assign Vehicle to Order


## Actor

Fleet Manager


## Description

Assigns vehicles to delivery orders optimally.


## Input

- Available vehicles.
- Delivery orders.
- Cost matrix.


## Processing

Techniques:

- Hungarian Algorithm.
- MILP.


## Output

Optimal vehicle-order assignment.


---

# 9. Dashboard Use Cases


# UC-09: View Supply Chain Dashboard


## Actor

Supply Chain Manager


## Description

Provides overall visibility of system operations.


## Displays

Inventory:

- Current stock.
- Low stock items.
- Reorder alerts.


Fleet:

- Active vehicles.
- Routes.
- Delivery status.


Optimization:

- Cost savings.
- Route efficiency.


---

# UC-10: Perform Scenario Analysis


## Actor

Supply Chain Manager


## Description

Allows users to evaluate different operational scenarios.


## Examples

Scenario 1:

Increase customer demand by 20%.


Scenario 2:

Disable one warehouse.


Scenario 3:

Increase fuel cost.


## Output

System displays:

- New optimized routes.
- Cost changes.
- Inventory impact.

---

# 10. Use Case Summary Table


| ID | Use Case | Actor | Module |
|---|---|---|---|
| UC-01 | Add Warehouse | Warehouse Manager | Inventory |
| UC-02 | Update Inventory | Warehouse Manager | Inventory |
| UC-03 | Calculate EOQ | Supply Chain Manager | Inventory |
| UC-04 | Reorder Alert | Inventory Engine | Inventory |
| UC-05 | Warehouse Allocation | Logistics Planner | Optimization |
| UC-06 | Shortest Route | Fleet Manager | Routing |
| UC-07 | Vehicle Routing | Logistics Planner | Routing |
| UC-08 | Vehicle Assignment | Fleet Manager | Optimization |
| UC-09 | Dashboard Monitoring | Manager | Dashboard |
| UC-10 | Scenario Analysis | Manager | Dashboard |

---

# 11. Conclusion

The use cases define how different stakeholders interact with the Intelligent Inventory and Fleet Router.

These workflows establish the foundation for:

- API design.
- Database design.
- Frontend interfaces.
- Testing scenarios.

The next design phase will convert these use cases into database models and REST API specifications.

---

**End of Use Case Document v1.0**