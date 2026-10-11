import { useEffect, useMemo, useState } from "react";

import {
  Truck,
  Search,
  RefreshCw,
  IndianRupee,
  Gauge,
  CircleDollarSign,
  CheckCircle,
} from "lucide-react";

import { getVehicles } from "../services/api";

function Fleet() {
  const [vehicles, setVehicles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [search, setSearch] = useState("");

  const loadVehicles = async () => {
    try {
      setLoading(true);
      setError("");

      const data = await getVehicles();

      setVehicles(
        Array.isArray(data) ? data : []
      );
    } catch (err) {
      setError(
        err.message ||
          "Unable to load fleet data."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadVehicles();
  }, []);

  const filteredVehicles = useMemo(() => {
    const text = search.trim().toLowerCase();

    if (!text) {
      return vehicles;
    }

    return vehicles.filter(
      (vehicle) =>
        vehicle.vehicle_number
          ?.toLowerCase()
          .includes(text) ||
        String(vehicle.vehicle_id).includes(text)
    );
  }, [vehicles, search]);

  const totalCapacity = vehicles.reduce(
    (sum, vehicle) =>
      sum + Number(vehicle.capacity || 0),
    0
  );

  const averageCapacity =
    vehicles.length > 0
      ? totalCapacity / vehicles.length
      : 0;

  const averageCostPerKm =
    vehicles.length > 0
      ? vehicles.reduce(
          (sum, vehicle) =>
            sum +
            Number(
              vehicle.cost_per_km || 0
            ),
          0
        ) / vehicles.length
      : 0;

  const totalFixedCost = vehicles.reduce(
    (sum, vehicle) =>
      sum +
      Number(vehicle.fixed_cost || 0),
    0
  );

  return (
    <main className="page">

      {/* HEADER */}

      <div className="page-header">

        <div>
          <span className="page-label">
            FLEET MANAGEMENT
          </span>

          <h2>Fleet</h2>

          <p>
            Manage vehicles and their routing
            cost parameters.
          </p>
        </div>

        <button
          className="secondary-button"
          onClick={loadVehicles}
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

      {/* SUMMARY */}

      <section className="fleet-stats">

        <div className="fleet-stat-card">

          <div className="fleet-stat-icon blue">
            <Truck size={19} />
          </div>

          <div>
            <span>Total Vehicles</span>

            <strong>
              {vehicles.length}
            </strong>

            <small>
              routing resources
            </small>
          </div>

        </div>

        <div className="fleet-stat-card">

          <div className="fleet-stat-icon purple">
            <Gauge size={19} />
          </div>

          <div>
            <span>Total Capacity</span>

            <strong>
              {totalCapacity.toLocaleString()}
            </strong>

            <small>
              units
            </small>
          </div>

        </div>

        <div className="fleet-stat-card">

          <div className="fleet-stat-icon green">
            <IndianRupee size={19} />
          </div>

          <div>
            <span>Average Cost / km</span>

            <strong>
              ₹
              {averageCostPerKm.toFixed(2)}
            </strong>

            <small>
              per kilometer
            </small>
          </div>

        </div>

        <div className="fleet-stat-card">

          <div className="fleet-stat-icon orange">
            <CircleDollarSign size={19} />
          </div>

          <div>
            <span>Total Fixed Cost</span>

            <strong>
              ₹
              {totalFixedCost.toLocaleString(
                undefined,
                {
                  minimumFractionDigits: 0,
                  maximumFractionDigits: 0,
                }
              )}
            </strong>

            <small>
              fleet fixed cost
            </small>
          </div>

        </div>

      </section>

      {/* VEHICLES */}

      {loading ? (

        <div className="fleet-page-state">

          <RefreshCw
            size={25}
            className="spin"
          />

          <p>
            Loading fleet...
          </p>

        </div>

      ) : error ? (

        <div className="fleet-page-state">

          <Truck size={25} />

          <strong>
            Unable to load fleet
          </strong>

          <p>{error}</p>

          <button
            className="primary-button"
            onClick={loadVehicles}
          >
            Try Again
          </button>

        </div>

      ) : (

        <section className="fleet-table-panel">

          <div className="fleet-toolbar">

            <div>
              <h3>
                Fleet Vehicles
              </h3>

              <p>
                {filteredVehicles.length} vehicles
                displayed
              </p>
            </div>

            <div className="fleet-search">

              <Search size={16} />

              <input
                value={search}
                onChange={(event) =>
                  setSearch(
                    event.target.value
                  )
                }
                placeholder="Search vehicle..."
              />

            </div>

          </div>

          <div className="fleet-table-wrapper">

            <table className="fleet-table">

              <thead>

                <tr>
                  <th>VEHICLE</th>
                  <th>CAPACITY</th>
                  <th>FIXED COST</th>
                  <th>COST / KM</th>
                  <th>STATUS</th>
                </tr>

              </thead>

              <tbody>

                {filteredVehicles.map(
                  (vehicle) => (

                    <tr
                      key={vehicle.vehicle_id}
                    >

                      <td>

                        <div className="fleet-name">

                          <div className="fleet-vehicle-icon">
                            <Truck size={15} />
                          </div>

                          <div>

                            <strong>
                              {
                                vehicle.vehicle_number
                              }
                            </strong>

                            <span>
                              Vehicle #
                              {
                                vehicle.vehicle_id
                              }
                            </span>

                          </div>

                        </div>

                      </td>

                      <td>

                        <div className="fleet-value">

                          <strong>
                            {
                              Number(
                                vehicle.capacity ||
                                  0
                              ).toLocaleString()
                            }
                          </strong>

                          <span>
                            units
                          </span>

                        </div>

                      </td>

                      <td>

                        <strong className="fleet-money">
                          ₹
                          {Number(
                            vehicle.fixed_cost ||
                              0
                          ).toLocaleString(
                            undefined,
                            {
                              minimumFractionDigits: 0,
                              maximumFractionDigits: 0,
                            }
                          )}
                        </strong>

                      </td>

                      <td>

                        <strong className="fleet-money">
                          ₹
                          {Number(
                            vehicle.cost_per_km ||
                              0
                          ).toFixed(2)}
                        </strong>

                        <span className="fleet-unit">
                          / km
                        </span>

                      </td>

                      <td>

                        <span className="fleet-status">
                          <CheckCircle size={12} />
                          Available
                        </span>

                      </td>

                    </tr>

                  )
                )}

              </tbody>

            </table>

            {filteredVehicles.length ===
              0 && (
              <div className="fleet-no-results">
                No vehicles found.
              </div>
            )}

          </div>

        </section>

      )}

    </main>
  );
}

export default Fleet;