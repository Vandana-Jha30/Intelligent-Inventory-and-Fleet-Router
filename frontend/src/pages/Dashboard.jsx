import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import {
  Package,
  Warehouse,
  Users,
  Truck,
  TrendingDown,
  Route,
  Zap,
  ArrowRight,
  RefreshCw,
} from "lucide-react";

import {
  getWarehouses,
  getInventory,
  getDeliveryLocations,
  getVehicles,
} from "../services/api";

function Dashboard() {
  const [warehouses, setWarehouses] = useState([]);
  const [inventory, setInventory] = useState([]);
  const [customers, setCustomers] = useState([]);
  const [vehicles, setVehicles] = useState([]);
  const [lastOptimization, setLastOptimization] =
    useState(null);
  const [loading, setLoading] = useState(true);

  const loadDashboard = async () => {
    try {
      setLoading(true);

      const [
        warehouseData,
        inventoryData,
        customerData,
        vehicleData,
      ] = await Promise.all([
        getWarehouses(),
        getInventory(),
        getDeliveryLocations(),
        getVehicles(),
      ]);

      setWarehouses(
        Array.isArray(warehouseData)
          ? warehouseData
          : []
      );

      setInventory(
        Array.isArray(inventoryData)
          ? inventoryData
          : []
      );

      setCustomers(
        Array.isArray(customerData)
          ? customerData
          : []
      );

      setVehicles(
        Array.isArray(vehicleData)
          ? vehicleData
          : []
      );

      const savedResult = localStorage.getItem(
        "iifr_last_optimization"
      );

      if (savedResult) {
        setLastOptimization(
          JSON.parse(savedResult)
        );
      }
    } catch (error) {
      console.error(
        "Dashboard loading error:",
        error
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDashboard();
  }, []);

  const totalInventory = inventory.reduce(
    (sum, item) =>
      sum +
      Math.max(
        Number(item.on_hand || 0) -
          Number(item.reserved || 0),
        0
      ),
    0
  );

  const totalCapacity = warehouses.reduce(
    (sum, warehouse) =>
      sum + Number(warehouse.capacity || 0),
    0
  );

  const totalDemand = customers.reduce(
    (sum, customer) =>
      sum +
      Number(customer.demand_quantity || 0),
    0
  );

  const totalFleetCapacity = vehicles.reduce(
    (sum, vehicle) =>
      sum + Number(vehicle.capacity || 0),
    0
  );

  const warehouseUtilization =
    totalCapacity > 0
      ? (totalInventory / totalCapacity) * 100
      : 0;

  const fleetUtilization =
    totalFleetCapacity > 0
      ? (totalDemand / totalFleetCapacity) * 100
      : 0;

  const formatNumber = (
    value,
    digits = 0
  ) => {
    return Number(value || 0).toLocaleString(
      undefined,
      {
        minimumFractionDigits: digits,
        maximumFractionDigits: digits,
      }
    );
  };

  /*
   * REAL DEMAND GRAPH
   *
   * Uses the actual customer demand returned
   * by the backend.
   */
  const chartCustomers = [...customers].sort(
    (a, b) =>
      Number(a.location_id) -
      Number(b.location_id)
  );

  const chartWidth = 900;
  const chartHeight = 300;

  const chartPadding = {
    top: 20,
    right: 25,
    bottom: 45,
    left: 50,
  };

  const innerWidth =
    chartWidth -
    chartPadding.left -
    chartPadding.right;

  const innerHeight =
    chartHeight -
    chartPadding.top -
    chartPadding.bottom;

  const maxChartDemand =
    Math.ceil(
      Math.max(
        ...chartCustomers.map((customer) =>
          Number(
            customer.demand_quantity || 0
          )
        ),
        25
      ) / 5
    ) * 5;

  const getX = (index) => {
    if (chartCustomers.length <= 1) {
      return chartPadding.left;
    }

    return (
      chartPadding.left +
      (index / (chartCustomers.length - 1)) *
        innerWidth
    );
  };

  const getY = (demand) => {
    return (
      chartPadding.top +
      innerHeight -
      (demand / maxChartDemand) *
        innerHeight
    );
  };

  const chartPoints = chartCustomers.map(
    (customer, index) => ({
      x: getX(index),
      y: getY(
        Number(customer.demand_quantity || 0)
      ),
      demand: Number(
        customer.demand_quantity || 0
      ),
      name: customer.location_name,
      id: customer.location_id,
    })
  );

  const linePath = chartPoints
    .map(
      (point, index) =>
        `${index === 0 ? "M" : "L"} ${point.x} ${point.y}`
    )
    .join(" ");

  const areaPath =
    chartPoints.length > 0
      ? `${linePath} L ${
          chartPoints[chartPoints.length - 1].x
        } ${
          chartPadding.top +
          innerHeight
        } L ${chartPoints[0].x} ${
          chartPadding.top +
          innerHeight
        } Z`
      : "";

  return (
    <main className="page dashboard-page">

      {/* HEADER */}

      <div className="page-header">
        <div>
          <span className="page-label">
            SUPPLY CHAIN
          </span>

          <h2>Dashboard</h2>

          <p>
            Overview of inventory, warehouses,
            customer demand and fleet operations.
          </p>
        </div>

        <button
          className="secondary-button"
          onClick={loadDashboard}
          disabled={loading}
        >
          <RefreshCw
            size={16}
            className={
              loading ? "spin" : ""
            }
          />
          Refresh
        </button>
      </div>

      {/* KPI CARDS */}

      <section className="dashboard-kpis">

        <div className="dashboard-kpi-card">
          <div className="dashboard-kpi-icon blue">
            <Package size={19} />
          </div>

          <div>
            <span>Available Inventory</span>

            <strong>
              {formatNumber(totalInventory)}
            </strong>

            <small>units</small>
          </div>
        </div>

        <div className="dashboard-kpi-card">
          <div className="dashboard-kpi-icon purple">
            <Warehouse size={19} />
          </div>

          <div>
            <span>
              Warehouse Utilization
            </span>

            <strong>
              {formatNumber(
                warehouseUtilization,
                1
              )}
              %
            </strong>

            <small>
              {warehouses.length} facilities
            </small>
          </div>
        </div>

        <div className="dashboard-kpi-card">
          <div className="dashboard-kpi-icon orange">
            <Users size={19} />
          </div>

          <div>
            <span>Customer Demand</span>

            <strong>
              {formatNumber(totalDemand)}
            </strong>

            <small>
              {customers.length} locations
            </small>
          </div>
        </div>

        <div className="dashboard-kpi-card">
          <div className="dashboard-kpi-icon green">
            <Truck size={19} />
          </div>

          <div>
            <span>Fleet Capacity</span>

            <strong>
              {formatNumber(
                totalFleetCapacity
              )}
            </strong>

            <small>
              {vehicles.length} vehicles
            </small>
          </div>
        </div>

      </section>

      {/* OPERATIONAL OVERVIEW */}

      <section className="dashboard-grid">

        <div className="dashboard-panel">

          <div className="dashboard-panel-header">
            <div>
              <h3>
                Operational Overview
              </h3>

              <p>
                Current supply-chain network
                status
              </p>
            </div>

            <Package size={18} />
          </div>

          <div className="dashboard-overview-list">

            <div className="dashboard-overview-row">
              <div className="dashboard-overview-label">
                <Warehouse size={15} />
                <span>
                  Warehouse capacity
                </span>
              </div>

              <strong>
                {formatNumber(totalCapacity)} units
              </strong>
            </div>

            <div className="dashboard-overview-row">
              <div className="dashboard-overview-label">
                <Package size={15} />
                <span>
                  Inventory available
                </span>
              </div>

              <strong>
                {formatNumber(totalInventory)} units
              </strong>
            </div>

            <div className="dashboard-overview-row">
              <div className="dashboard-overview-label">
                <Users size={15} />
                <span>
                  Delivery demand
                </span>
              </div>

              <strong>
                {formatNumber(totalDemand)} units
              </strong>
            </div>

            <div className="dashboard-overview-row">
              <div className="dashboard-overview-label">
                <Truck size={15} />
                <span>
                  Fleet capacity
                </span>
              </div>

              <strong>
                {formatNumber(
                  totalFleetCapacity
                )} units
              </strong>
            </div>

          </div>
        </div>

        {/* CAPACITY UTILIZATION */}

        <div className="dashboard-panel">

          <div className="dashboard-panel-header">
            <div>
              <h3>
                Capacity Utilization
              </h3>

              <p>
                Current network load
              </p>
            </div>

            <TrendingDown size={18} />
          </div>

          <div className="dashboard-utilization-block">

            <div className="dashboard-utilization-heading">
              <span>Warehouse</span>

              <strong>
                {formatNumber(
                  warehouseUtilization,
                  1
                )}
                %
              </strong>
            </div>

            <div className="dashboard-progress">
              <div
                style={{
                  width: `${Math.min(
                    warehouseUtilization,
                    100
                  )}%`,
                }}
              />
            </div>

          </div>

          <div className="dashboard-utilization-block">

            <div className="dashboard-utilization-heading">
              <span>Fleet</span>

              <strong>
                {formatNumber(
                  fleetUtilization,
                  1
                )}
                %
              </strong>
            </div>

            <div className="dashboard-progress">
              <div
                style={{
                  width: `${Math.min(
                    fleetUtilization,
                    100
                  )}%`,
                }}
              />
            </div>

          </div>

          <div className="dashboard-capacity-note">
            <span>
              Inventory surplus
            </span>

            <strong>
              {formatNumber(
                Math.max(
                  totalInventory -
                    totalDemand,
                  0
                )
              )} units
            </strong>
          </div>

        </div>

      </section>

      {/* REAL LINE GRAPH */}

      <section className="dashboard-panel dashboard-chart-panel">

        <div className="dashboard-panel-header">

          <div>
            <h3>
              Customer Demand
            </h3>

            <p>
              Demand across all delivery
              locations
            </p>
          </div>

          <Users size={18} />

        </div>

        <div className="dashboard-chart-container">

          {chartCustomers.length === 0 ? (
            <div className="dashboard-chart-empty">
              No demand data available.
            </div>
          ) : (
            <svg
              viewBox={`0 0 ${chartWidth} ${chartHeight}`}
              className="dashboard-line-chart"
              preserveAspectRatio="none"
            >

              {/* GRID */}

              {[0, 5, 10, 15, 20, 25].map(
                (value) => {

                  if (
                    value >
                    maxChartDemand
                  ) {
                    return null;
                  }

                  const y = getY(value);

                  return (
                    <g key={value}>

                      <line
                        x1={
                          chartPadding.left
                        }
                        y1={y}
                        x2={
                          chartWidth -
                          chartPadding.right
                        }
                        y2={y}
                        className="chart-grid-line"
                      />

                      <text
                        x={
                          chartPadding.left -
                          10
                        }
                        y={y + 4}
                        textAnchor="end"
                        className="chart-axis-text"
                      >
                        {value}
                      </text>

                    </g>
                  );
                }
              )}

              {/* X AXIS */}

              <line
                x1={chartPadding.left}
                y1={
                  chartPadding.top +
                  innerHeight
                }
                x2={
                  chartWidth -
                  chartPadding.right
                }
                y2={
                  chartPadding.top +
                  innerHeight
                }
                className="chart-axis-line"
              />

              {/* Y AXIS */}

              <line
                x1={chartPadding.left}
                y1={chartPadding.top}
                x2={chartPadding.left}
                y2={
                  chartPadding.top +
                  innerHeight
                }
                className="chart-axis-line"
              />

              {/* AREA */}

              <path
                d={areaPath}
                className="chart-area"
              />

              {/* LINE */}

              <path
                d={linePath}
                className="chart-line"
                fill="none"
              />

              {/* POINTS */}

              {chartPoints.map(
                (point) => (
                  <g key={point.id}>

                    <circle
                      cx={point.x}
                      cy={point.y}
                      r="4"
                      className="chart-point"
                    />

                    <title>
                      {point.name}:{" "}
                      {point.demand} units
                    </title>

                  </g>
                )
              )}

              {/* X LABELS */}

              {chartPoints
                .filter(
                  (_, index) =>
                    index % 5 === 0 ||
                    index ===
                      chartPoints.length - 1
                )
                .map((point) => (
                  <text
                    key={`label-${point.id}`}
                    x={point.x}
                    y={
                      chartPadding.top +
                      innerHeight +
                      25
                    }
                    textAnchor="middle"
                    className="chart-axis-text"
                  >
                    {point.id}
                  </text>
                ))}

              {/* AXIS TITLES */}

              <text
                x={
                  chartPadding.left +
                  innerWidth / 2
                }
                y={chartHeight - 5}
                textAnchor="middle"
                className="chart-axis-title"
              >
                Delivery Location
              </text>

              <text
                x="14"
                y={
                  chartPadding.top +
                  innerHeight / 2
                }
                textAnchor="middle"
                transform={`rotate(-90 14 ${
                  chartPadding.top +
                  innerHeight / 2
                })`}
                className="chart-axis-title"
              >
                Demand (units)
              </text>

            </svg>
          )}

        </div>

      </section>

      {/* LATEST OPTIMIZATION */}

      <section className="dashboard-optimization">

        <div className="dashboard-panel-header">

          <div>
            <span className="page-label">
              OPTIMIZATION
            </span>

            <h3>
              Optimization Result
            </h3>

            <p>
              Most recent supply-chain
              optimization run.
            </p>
          </div>

          <div className="dashboard-optimization-icon">
            <Zap size={19} />
          </div>

        </div>

        {lastOptimization ? (
          <>

            <div className="dashboard-optimization-kpis">

              <div>
                <span>
                  Baseline Cost
                </span>

                <strong>
                  ₹
                  {formatNumber(
                    lastOptimization.baseline_cost,
                    2
                  )}
                </strong>
              </div>

              <div>
                <span>
                  Optimized Cost
                </span>

                <strong className="saving">
                  ₹
                  {formatNumber(
                    lastOptimization.optimized_cost,
                    2
                  )}
                </strong>
              </div>

              <div>
                <span>
                  Cost Improvement
                </span>

                <strong className="saving">
                  {formatNumber(
                    lastOptimization
                      .cost_improvement_percent,
                    2
                  )}
                  %
                </strong>
              </div>

              <div>
                <span>
                  Routing Cost
                </span>

                <strong>
                  ₹
                  {formatNumber(
                    lastOptimization
                      .routing?.total_cost,
                    2
                  )}
                </strong>
              </div>

            </div>

            <div className="dashboard-optimization-footer">

              <div>
                <Route size={15} />

                <span>
                  {formatNumber(
                    lastOptimization
                      .routing?.total_distance,
                    2
                  )}{" "}
                  km routed using{" "}
                  {lastOptimization
                    .routing?.routes
                    ?.length || 0}{" "}
                  vehicles
                </span>
              </div>

              <Link to="/optimize">
                View full optimization
                <ArrowRight size={14} />
              </Link>

            </div>

          </>
        ) : (

          <div className="dashboard-no-optimization">

            <Zap size={24} />

            <strong>
              No optimization run yet
            </strong>

            <p>
              Run the optimization model to
              generate a supply-chain plan.
            </p>

            <Link to="/optimize">
                Run Optimization
                <ArrowRight size={14} />
            </Link>

          </div>

        )}

      </section>

      {/* QUICK ACCESS */}

      <section className="dashboard-quick">

        <div className="dashboard-panel-header">

          <div>
            <h3>
              Quick Access
            </h3>

            <p>
              Navigate to operational modules
            </p>
          </div>

        </div>

        <div className="dashboard-quick-grid">

          <Link to="/inventory">
            <Package size={18} />

            <div>
              <strong>
                Inventory
              </strong>

              <span>
                Stock and inventory analysis
              </span>
            </div>

            <ArrowRight size={15} />
          </Link>

          <Link href="/warehouses">
            <Warehouse size={18} />

            <div>
              <strong>
                Warehouses
              </strong>

              <span>
                Capacity and utilization
              </span>
            </div>

            <ArrowRight size={15} />
          </Link>

          <Link href="/customers">
            <Users size={18} />

            <div>
              <strong>
                Customers
              </strong>

              <span>
                Demand and delivery locations
              </span>
            </div>

            <ArrowRight size={15} />
          </Link>

          <Link href="/fleet">
            <Truck size={18} />

            <div>
              <strong>
                Fleet
              </strong>

              <span>
                Vehicles and routing resources
              </span>
            </div>

            <ArrowRight size={15} />
          </Link>

        </div>

      </section>

    </main>
  );
}

export default Dashboard;