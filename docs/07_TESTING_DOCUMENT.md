# Intelligent Inventory and Fleet Router (IIFR)

# Testing Document

**Version:** 1.0

**Domain:** Operations Research, Supply Chain Optimization, Logistics Intelligence

---

# 1. Introduction

## 1.1 Purpose

This document defines the testing strategy for the Intelligent Inventory and Fleet Router (IIFR).

The purpose of testing is to ensure:

- Correct implementation of Operations Research models.
- Reliable API behavior.
- Accuracy of optimization results.
- Stability of the complete system.
- Proper integration between modules.

---

# 2. Testing Objectives

The testing process aims to verify:

- Inventory calculations are mathematically correct.
- Optimization models generate feasible solutions.
- Routing algorithms produce valid paths.
- APIs return correct responses.
- Database operations maintain consistency.
- Dashboard displays accurate information.

---

# 3. Testing Strategy

The system follows a layered testing approach.


```
                System Testing

                      |

              Integration Testing

                      |

                Unit Testing

                      |

             Algorithm Validation
```

---

# 4. Unit Testing

## Purpose

Unit testing validates individual components independently.

Framework:

```
pytest
```

---

# 4.1 Inventory Engine Testing

## Test Cases


### Test: EOQ Calculation


Input:

```
Annual Demand = 10000

Ordering Cost = 500

Holding Cost = 20
```


Expected:


```
EOQ = sqrt((2DS)/H)
```


Verify:

- Returned value matches mathematical calculation.


---

### Test: Safety Stock Calculation


Input:

```
Service Level = 1.65

Demand Standard Deviation = 20

Lead Time = 5
```


Expected:

Correct safety stock quantity.


---

### Test: Reorder Point


Input:

```
Average Daily Demand

Lead Time

Safety Stock
```


Expected:


```
ROP = Demand During Lead Time + Safety Stock
```

---

# 4.2 Transportation Optimization Testing

## Objective

Verify Linear Programming model.


Test:


Input:


```
Warehouses:

W1 Supply = 100

W2 Supply = 150


Customers:

C1 Demand = 50

C2 Demand = 200
```


Expected:

- All demand satisfied.
- Supply constraints respected.
- Minimum cost generated.

---

Validation:

Check:


```
Σ Shipment <= Supply

Σ Shipment >= Demand
```

---

# 4.3 Assignment Algorithm Testing


Test:


Input:

Cost matrix:

```
[
[10,20],

[15,5]
]
```


Expected:


Optimal assignment:


```
Resource 1 -> Task 1

Resource 2 -> Task 2
```


---

# 4.4 Graph Algorithm Testing


## Dijkstra Testing


Input:

Graph:

```
A-B = 5

B-C = 3

A-C = 10
```


Expected:

Shortest path:


```
A-B-C
```


Distance:

```
8
```

---

# 4.5 Vehicle Routing Testing


Test:

Input:

```
Vehicles = 2

Customers = 5

Capacity = 100
```


Verify:

- Every customer visited.
- Vehicle capacity not exceeded.
- Route starts from depot.
- Route ends at depot.

---

# 5. Integration Testing

## Purpose

Verify interaction between multiple modules.

---

# 5.1 Inventory and Optimization Integration


Workflow:


```
Inventory Status

        |

Demand Requirement

        |

Transportation Optimization

        |

Replenishment Decision
```


Verify:

Inventory information correctly reaches optimization engine.

---

# 5.2 Routing and Fleet Integration


Workflow:


```
Orders

 |

Vehicle Assignment

 |

Route Optimization

 |

Delivery Plan
```


Verify:

- Correct truck assignment.
- Valid routes.
- Capacity constraints satisfied.

---

# 5.3 Database Integration Testing


Verify:

- Data insertion.
- Data retrieval.
- Data updates.
- Relationship consistency.

---

# 6. API Testing


Framework:

```
FastAPI TestClient
```

---

# 6.1 Warehouse API Testing


## POST /warehouses


Verify:

- Valid warehouse creation.
- Invalid input rejection.


---

## GET /warehouses


Verify:

- Correct warehouse list returned.

---

# 6.2 Inventory API Testing


Endpoints:

```
GET /inventory

POST /inventory/eoq

POST /inventory/reorder-point
```


Verify:

- Correct calculations.
- Correct response format.

---

# 6.3 Optimization API Testing


Endpoint:

```
POST /optimization/transportation
```


Verify:

- Correct input validation.
- Solver execution.
- Optimization result returned.

---

# 6.4 Routing API Testing


Endpoints:

```
POST /routing/shortest-path

POST /routing/optimize
```


Verify:

- Valid route generation.
- Correct distance calculation.

---

# 7. System Testing

## Purpose

Validate complete end-to-end workflow.


Scenario:


```
Customer Order Created

        |

Inventory Checked

        |

Warehouse Selected

        |

Transportation Optimized

        |

Truck Assigned

        |

Route Generated

        |

Dashboard Updated
```


Expected:

Complete successful delivery plan generated.

---

# 8. Performance Testing

The system should satisfy:


## API Performance


Requirement:


```
Normal API response < 200 ms
```


---

## Transportation Solver


Target:


```
50 warehouses/customers

Execution < 2 seconds
```

---

## Vehicle Routing Solver


Target:


```
100 customers

10 vehicles

Execution < 10 seconds
```

---

# 9. Optimization Validation

Optimization results are validated using:


## Feasibility Checking


Verify:

- All constraints satisfied.
- No negative variables.
- Demand fulfilled.


---

## Cost Validation


Compare:

```
Optimized Cost

vs

Baseline Cost
```


Example baseline:

Nearest warehouse assignment.

---

## Solution Quality


Measure:

- Cost reduction.
- Distance reduction.
- Fleet utilization improvement.

---

# 10. Error Handling Testing


The system should handle:


## Invalid Input

Example:

Negative inventory.


Expected:

```
400 Bad Request
```


---

## Infeasible Optimization


Example:

Demand greater than total supply.


Expected:

Return:

```
Optimization infeasible

Supply deficit report
```

---

## Solver Failure


Expected:

Return best available solution or error message.

---

# 11. Security Testing


Verify:

- Authentication.
- Authorization.
- Input validation.
- SQL injection prevention.
- Secure password storage.

---

# 12. User Acceptance Testing


Users verify:


## Supply Chain Manager

- Dashboard visibility.
- Optimization recommendations.


## Warehouse Manager

- Inventory updates.
- Alerts.


## Fleet Manager

- Route visualization.
- Vehicle assignment.


---

# 13. Testing Tools


| Purpose | Tool |
|-|-|
| Unit Testing | pytest |
| API Testing | FastAPI TestClient |
| Code Quality | pylint |
| API Documentation | Swagger/OpenAPI |
| Database Testing | SQLAlchemy Testing Tools |

---

# 14. Testing Deliverables


The project will maintain:

- Test cases.
- Test reports.
- Performance results.
- Optimization validation results.
- Bug tracking records.

---

# Conclusion

The testing strategy ensures that the Intelligent Inventory and Fleet Router is mathematically correct, functionally reliable, and suitable for practical supply chain optimization scenarios.

---

**End of Testing Document v1.0**