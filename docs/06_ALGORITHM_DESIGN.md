# Intelligent Inventory and Fleet Router (IIFR)

# Algorithm Design Document

**Version:** 1.0

**Domain:** Operations Research, Supply Chain Optimization, Logistics Intelligence

---

# 1. Introduction

## 1.1 Purpose

This document describes the mathematical models, optimization techniques, and algorithms used in the Intelligent Inventory and Fleet Router.

The system applies Operations Research techniques to solve supply chain optimization problems including:

- Inventory planning.
- Transportation optimization.
- Resource assignment.
- Route optimization.
- Fleet management.

The algorithms are implemented using Python optimization libraries such as:

- PuLP.
- Google OR-Tools.
- NetworkX.
- NumPy.
- Pandas.

---

# 2. Algorithm Architecture

The optimization workflow follows:

```
Operational Data

       |

       |

Mathematical Model Construction

       |

       |

Optimization Algorithm

       |

       |

Optimal / Near Optimal Solution

       |

       |

Dashboard Visualization
```

---

# 3. Inventory Optimization Algorithms

The Inventory Engine uses classical inventory models.

---

# 3.1 Economic Order Quantity (EOQ)

## Objective

Determine the optimal order quantity that minimizes total inventory cost.

The total inventory cost consists of:

- Ordering cost.
- Holding cost.

---

## Mathematical Model


EOQ formula:

\[
EOQ = \sqrt{\frac{2DS}{H}}
\]


Where:


D = Annual demand


S = Ordering cost per order


H = Holding cost per unit per year


---

## Input

- Annual demand.
- Ordering cost.
- Holding cost.


---

## Output

- Optimal order quantity.

---

## Implementation


Python:

```
calculate_eoq()
```

---

# 3.2 Safety Stock Calculation


## Objective

Determine additional inventory required to handle demand uncertainty.


Formula:


\[
SS = Z \times \sigma_d \times \sqrt L
\]


Where:


Z = Service level factor


σd = Standard deviation of demand


L = Lead time


---

## Input

- Demand variation.
- Service level.
- Lead time.


## Output

- Safety stock quantity.

---

# 3.3 Reorder Point (ROP)


## Objective

Determine when inventory replenishment should be triggered.


Formula:


\[
ROP = (\bar d \times L)+SS
\]


Where:


\bar d = Average daily demand


L = Lead time


SS = Safety stock


---

## Decision Rule


```
IF Inventory Position <= ROP

THEN Generate Reorder Alert
```

---

# 3.4 Demand Forecasting


## Objective

Predict future customer demand.


The system supports:

---

## Moving Average Forecasting


Formula:


\[
F_t=\frac{D_{t-1}+D_{t-2}+...+D_{t-n}}{n}
\]


---

## Exponential Smoothing


Formula:


\[
F_t=\alpha D_t+(1-\alpha)F_{t-1}
\]


---

## Output

Predicted demand for future periods.

---

# 4. Transportation Optimization

## Objective

Determine optimal shipment quantities from warehouses to customers while minimizing transportation cost.

---

# 4.1 Transportation Problem Formulation


Given:

m warehouses

n customers


Decision variable:


\[
x_{ij}
\]


represents quantity shipped from warehouse i to customer j.


---

## Objective Function


Minimize:


\[
Z=\sum_i\sum_j c_{ij}x_{ij}
\]


Where:


cij = transportation cost from warehouse i to customer j


---

## Constraints


## Supply Constraint


\[
\sum_j x_{ij}\leq S_i
\]


Warehouse supply cannot be exceeded.


---

## Demand Constraint


\[
\sum_i x_{ij}\geq D_j
\]


Customer demand must be satisfied.


---

## Non-Negativity Constraint


\[
x_{ij}\geq0
\]


---

# Implementation


Library:

```
PuLP
```


Workflow:

```
Input Data

↓

Create LP Variables

↓

Define Objective Function

↓

Add Constraints

↓

Call Solver

↓

Return Allocation
```

---

# Output

- Shipment quantity.
- Warehouse assignment.
- Minimum transportation cost.

---

# 5. Assignment Optimization

## Objective

Assign resources optimally.

Examples:

- Truck to order.
- Driver to route.


---

# 5.1 Mathematical Formulation


Decision Variable:


\[
x_{ij}
\]


where:


xij = 1 if resource i assigned to task j


otherwise:

xij = 0


---

## Objective


Minimize:


\[
Z=\sum_i\sum_j c_{ij}x_{ij}
\]


---

## Constraints


Each resource assigned once:


\[
\sum_jx_{ij}=1
\]


Each task assigned once:


\[
\sum_ix_{ij}=1
\]


---

## Solution Methods


- Hungarian Algorithm.
- Mixed Integer Linear Programming.


---

# 6. Network Optimization Algorithms


The supply chain network is modeled as:


\[
G=(V,E)
\]


Where:


V = nodes


Examples:

- Warehouse.
- Depot.
- Customer.


E = edges


Examples:

- Roads.
- Transportation links.


---

# 6.1 Dijkstra Algorithm


## Objective

Find shortest path between two nodes.


---

## Algorithm Steps


1. Initialize distance of source node as 0.
2. Assign infinity distance to other nodes.
3. Select minimum distance unvisited node.
4. Update neighboring nodes.
5. Repeat until destination reached.


---

## Complexity


Using priority queue:


\[
O((V+E)\log V)
\]


---

## Input

- Graph.
- Source node.
- Destination node.


---

## Output

- Shortest route.
- Minimum distance.

---

# 6.2 A* Search Algorithm


## Objective

Find shortest path using heuristic guidance.


Evaluation function:


\[
f(n)=g(n)+h(n)
\]


Where:


g(n) = cost from start node


h(n) = estimated cost to goal


---

## Advantage

Usually faster than Dijkstra for large geographical networks.

---

# 7. Vehicle Routing Optimization

# Capacitated Vehicle Routing Problem (CVRP)


## Objective

Find optimal routes for multiple vehicles while satisfying customer demand and vehicle capacity constraints.


---

# Mathematical Model


Given:

Vehicles:

K


Customers:

N


Decision Variable:


\[
x_{ijk}
\]


where:


xijk = 1 if vehicle k travels from i to j.


---

# Objective Function


Minimize:


\[
\sum_k\sum_i\sum_j c_{ij}x_{ijk}
\]


Where:


cij = travel cost.


---

# Constraints


## Customer Visit Constraint


Each customer must be visited once.


\[
\sum_k\sum_i x_{ijk}=1
\]


---

## Vehicle Capacity Constraint


\[
\sum_i d_i \leq C_k
\]


Where:


di = customer demand


Ck = vehicle capacity


---

## Depot Constraint


Every vehicle:

- Starts from depot.
- Returns to depot.


---

# Implementation


Library:


```
Google OR-Tools
```


Workflow:


```
Load Customers

↓

Create Distance Matrix

↓

Create Vehicle Model

↓

Add Constraints

↓

Solve Routing Problem

↓

Return Routes
```

---

# Output


- Vehicle assignment.
- Delivery sequence.
- Total distance.
- Estimated cost.

---

# 8. Facility Location Optimization (Future Module)


## Objective

Select optimal warehouses/distribution centers.


---

Decision Variable:


\[
y_i
\]


where:


yi = 1 if facility i is selected.


---

Objective:


Minimize:


\[
\sum_i f_i y_i+\sum_i\sum_j c_{ij}x_{ij}
\]


Where:


fi = fixed facility cost


cij = transportation cost


---

# 9. Scenario Simulation


The system supports what-if analysis.

Examples:


## Demand Increase Scenario

Input:

```
Demand +20%
```


Process:

Recalculate:

- Inventory requirements.
- Transportation plan.
- Routes.


---

## Warehouse Failure Scenario


Input:

```
Warehouse W1 unavailable
```


Process:

Recalculate:

- Allocation.
- Routes.
- Costs.


---

# 10. Algorithm Selection Summary


| Problem | Algorithm | Library |
|-|-|-|
| EOQ | Inventory Model | Python |
| Safety Stock | Statistical Model | Python |
| Forecasting | Moving Average, Exponential Smoothing | Python |
| Transportation | Linear Programming | PuLP |
| Assignment | Hungarian/MILP | PuLP |
| Shortest Path | Dijkstra | NetworkX |
| Heuristic Routing | A* | NetworkX |
| Vehicle Routing | CVRP | OR-Tools |
| Facility Selection | MILP | PuLP |

---

# 11. Testing Strategy


Each algorithm will be tested using:


## Unit Testing

Example:

```
test_eoq()

test_transportation_solver()

test_dijkstra()

test_vrp()
```


---

## Validation

Optimization results will be verified against:

- Known textbook examples.
- Manual calculations.
- Solver output consistency.


---

# Conclusion

The algorithm design provides the mathematical foundation for the Intelligent Inventory and Fleet Router.

Each supply chain problem is mapped to an appropriate Operations Research model, ensuring that the implemented system provides optimized and explainable decisions.

---

**End of Algorithm Design Document v1.0**