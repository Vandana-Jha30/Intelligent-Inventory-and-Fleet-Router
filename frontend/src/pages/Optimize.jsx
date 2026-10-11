import { useState } from "react";
import {
  Zap,
  Package,
  Warehouse,
  MapPin,
  Truck,
  Route,
  IndianRupee,
  RefreshCw,
  AlertTriangle,
  CheckCircle2,
} from "lucide-react";

import {
  createSupplyChainPlan,
} from "../services/api";

function Optimize() {
  const [form, setForm] = useState({
    product_id: 1,
    warehouse_id: 1,
    depot_id: 1,
    window: 3,
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (event) => {
    const { name, value } = event.target;

    setForm((current) => ({
      ...current,
      [name]: Number(value),
    }));
  };

  const runOptimization = async (event) => {
    event.preventDefault();

    try {
      setLoading(true);
      setError("");
      setResult(null);

      const response =
        await createSupplyChainPlan({
            product_id: form.product_id,
            warehouse_id: form.warehouse_id,
            depot_id: form.depot_id,
            window: form.window,
        });

        setResult(response);

        localStorage.setItem(
        "iifr_last_optimization",
        JSON.stringify(response)
        );
    } catch (err) {
    setError(
        err.message ||
        "Optimization could not be completed."
    );
    } finally {
    setLoading(false);
    }
};

  const formatNumber = (value, digits = 2) => {
    return Number(value || 0).toLocaleString(
      undefined,
      {
        minimumFractionDigits: digits,
        maximumFractionDigits: digits,
      }
    );
  };

  return (
    <main className="page">
      <div className="page-header">
        <div>
          <span className="page-label">
            OPERATIONS RESEARCH
          </span>

          <h2>Optimization</h2>

          <p>
            Generate an integrated inventory,
            allocation and fleet routing plan.
          </p>
        </div>
      </div>

      {/* OPTIMIZATION INPUT */}

      <section className="optimization-input-panel">
        <div className="optimization-panel-heading">
          <div className="optimization-heading-icon">
            <Zap size={20} />
          </div>

          <div>
            <h3>Optimization Scenario</h3>

            <p>
              Configure the planning parameters and
              run the optimization model.
            </p>
          </div>
        </div>

        <form
          className="optimization-form"
          onSubmit={runOptimization}
        >
          <div className="optimization-field">
            <label>
              <Package size={14} />
              Product ID
            </label>

            <input
              type="number"
              name="product_id"
              min="1"
              value={form.product_id}
              onChange={handleChange}
            />
          </div>

          <div className="optimization-field">
            <label>
              <Warehouse size={14} />
              Warehouse ID
            </label>

            <input
              type="number"
              name="warehouse_id"
              min="1"
              value={form.warehouse_id}
              onChange={handleChange}
            />
          </div>

          <div className="optimization-field">
            <label>
              <MapPin size={14} />
              Depot ID
            </label>

            <input
              type="number"
              name="depot_id"
              min="1"
              value={form.depot_id}
              onChange={handleChange}
            />
          </div>

          <div className="optimization-field">
            <label>
              Forecast Window
            </label>

            <input
              type="number"
              name="window"
              min="1"
              value={form.window}
              onChange={handleChange}
            />
          </div>

          <button
            className="optimization-run-button"
            type="submit"
            disabled={loading}
          >
            {loading ? (
              <>
                <RefreshCw
                  size={16}
                  className="spin"
                />
                Optimizing...
              </>
            ) : (
              <>
                <Zap size={16} />
                Run Optimization
              </>
            )}
          </button>
        </form>
      </section>

      {/* ERROR */}

      {error && (
        <div className="optimization-error">
          <AlertTriangle size={18} />

          <div>
            <strong>
              Optimization failed
            </strong>

            <p>{error}</p>
          </div>
        </div>
      )}

      {/* RESULTS */}

      {result && (
        <>
          <div className="optimization-result-heading">
            <div>
              <span className="page-label">
                OPTIMIZATION RESULT
              </span>

              <h3>Supply Chain Plan</h3>
            </div>

            <div className="optimization-success">
              <CheckCircle2 size={16} />
              Plan generated
            </div>
          </div>

          {/* KPI CARDS */}

          <section className="optimization-kpis">
            <div className="optimization-kpi">
              <div className="optimization-kpi-icon blue">
                <Package size={18} />
              </div>

              <div>
                <span>Delivery Demand</span>
                <strong>
                  {formatNumber(
                    result.delivery_demand,
                    0
                  )}
                </strong>
                <small>units</small>
              </div>
            </div>

            <div className="optimization-kpi">
              <div className="optimization-kpi-icon purple">
                <Warehouse size={18} />
              </div>

              <div>
                <span>Available Inventory</span>
                <strong>
                  {formatNumber(
                    result.available_inventory,
                    0
                  )}
                </strong>
                <small>units</small>
              </div>
            </div>

            <div className="optimization-kpi">
              <div className="optimization-kpi-icon green">
                <IndianRupee size={18} />
              </div>

              <div>
                <span>Optimized Allocation</span>
                <strong>
                  ₹
                  {formatNumber(
                    result.optimized_cost
                  )}
                </strong>
                <small>transportation cost</small>
              </div>
            </div>

            <div className="optimization-kpi">
              <div className="optimization-kpi-icon orange">
                <Route size={18} />
              </div>

              <div>
                <span>Routing Cost</span>
                <strong>
                  ₹
                  {formatNumber(
                    result.routing?.total_cost
                  )}
                </strong>
                <small>fleet cost</small>
              </div>
            </div>
          </section>

          {/* COST COMPARISON */}

          <section className="optimization-result-grid">
            <div className="optimization-result-card">
              <div className="result-card-header">
                <div>
                  <h3>Allocation Cost</h3>

                  <p>
                    Warehouse-to-customer
                    allocation
                  </p>
                </div>

                <Package size={18} />
              </div>

              <div className="cost-comparison">
                <div>
                  <span>Baseline</span>

                  <strong>
                    ₹
                    {formatNumber(
                      result.baseline_cost
                    )}
                  </strong>
                </div>

                <div>
                  <span>Optimized</span>

                  <strong className="optimized-value">
                    ₹
                    {formatNumber(
                      result.optimized_cost
                    )}
                  </strong>
                </div>
              </div>

              <div className="improvement-box">
                <span>
                  Cost improvement
                </span>

                <strong>
                  {formatNumber(
                    result.cost_improvement_percent
                  )}
                  %
                </strong>
              </div>
            </div>

            <div className="optimization-result-card">
              <div className="result-card-header">
                <div>
                  <h3>Inventory Analysis</h3>

                  <p>
                    Inventory planning indicators
                  </p>
                </div>

                <Warehouse size={18} />
              </div>

              <div className="inventory-result-grid">
                <div>
                  <span>Forecast / Day</span>

                  <strong>
                    {formatNumber(
                      result.inventory_analysis
                        ?.forecast_daily_demand
                    )}
                  </strong>
                </div>

                <div>
                  <span>EOQ</span>

                  <strong>
                    {formatNumber(
                      result.inventory_analysis?.eoq
                    )}
                  </strong>
                </div>

                <div>
                  <span>Safety Stock</span>

                  <strong>
                    {formatNumber(
                      result.inventory_analysis
                        ?.safety_stock
                    )}
                  </strong>
                </div>

                <div>
                  <span>Reorder Point</span>

                  <strong>
                    {formatNumber(
                      result.inventory_analysis
                        ?.reorder_point
                    )}
                  </strong>
                </div>
              </div>
            </div>
          </section>

          {/* ROUTING */}

          <section className="optimization-result-card routing-result-card">
            <div className="result-card-header">
              <div>
                <h3>Fleet Routing</h3>

                <p>
                  Optimized vehicle routes generated
                  by the CVRP solver
                </p>
              </div>

              <Truck size={19} />
            </div>

            <div className="routing-summary">
              <div>
                <span>Total Distance</span>

                <strong>
                  {formatNumber(
                    result.routing?.total_distance
                  )}{" "}
                  km
                </strong>
              </div>

              <div>
                <span>Total Routing Cost</span>

                <strong>
                  ₹
                  {formatNumber(
                    result.routing?.total_cost
                  )}
                </strong>
              </div>

              <div>
                <span>Vehicles Used</span>

                <strong>
                  {result.routing?.routes
                    ?.length || 0}
                </strong>
              </div>
            </div>

            <div className="route-list">
              {result.routing?.routes?.map(
                (route) => (
                  <div
                    className="route-row"
                    key={route.vehicle_id}
                  >
                    <div className="route-vehicle">
                      <div>
                        <Truck size={15} />
                      </div>

                      <strong>
                        Vehicle #{route.vehicle_id}
                      </strong>
                    </div>

                    <div>
                      <span>Customers</span>

                      <strong>
                        {route.location_ids
                          ?.length || 0}
                      </strong>
                    </div>

                    <div>
                      <span>Demand</span>

                      <strong>
                        {formatNumber(
                          route.total_demand,
                          0
                        )}
                      </strong>
                    </div>

                    <div>
                      <span>Distance</span>

                      <strong>
                        {formatNumber(
                          route.route_distance
                        )}{" "}
                        km
                      </strong>
                    </div>

                    <div>
                      <span>Route Cost</span>

                      <strong>
                        ₹
                        {formatNumber(
                          route.route_cost
                        )}
                      </strong>
                    </div>

                    <div>
                      <span>Remaining</span>

                      <strong>
                        {formatNumber(
                          route.remaining_capacity,
                          0
                        )}
                      </strong>
                    </div>
                  </div>
                )
              )}
            </div>
          </section>

          {/* ALLOCATION */}

          <section className="optimization-result-card">
            <div className="result-card-header">
              <div>
                <h3>Warehouse Allocation</h3>

                <p>
                  Optimized inventory allocation
                  across delivery locations
                </p>
              </div>

              <Warehouse size={18} />
            </div>

            <div className="allocation-table-wrapper">
              <table className="allocation-table">
                <thead>
                  <tr>
                    <th>WAREHOUSE</th>
                    <th>CUSTOMER</th>
                    <th>QUANTITY</th>
                    <th>DISTANCE</th>
                    <th>TRANSPORT COST</th>
                  </tr>
                </thead>

                <tbody>
                  {result.allocation?.map(
                    (item, index) => (
                      <tr key={index}>
                        <td>
                          {item.warehouse_name}
                        </td>

                        <td>
                          {item.location_name}
                        </td>

                        <td>
                          {formatNumber(
                            item.quantity,
                            0
                          )}
                        </td>

                        <td>
                          {formatNumber(
                            item.distance_km
                          )}{" "}
                          km
                        </td>

                        <td>
                          ₹
                          {formatNumber(
                            item.transportation_cost
                          )}
                        </td>
                      </tr>
                    )
                  )}
                </tbody>
              </table>
            </div>
          </section>
        </>
      )}
    </main>
  );
}

export default Optimize;