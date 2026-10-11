import { useEffect, useMemo, useState } from "react";

import {
  Users,
  Search,
  RefreshCw,
  MapPin,
  Package,
  TrendingUp,
  AlertTriangle,
} from "lucide-react";

import { getDeliveryLocations } from "../services/api";

function Customers() {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [search, setSearch] = useState("");

  const loadCustomers = async () => {
    try {
      setLoading(true);
      setError("");

      const data = await getDeliveryLocations();

      setCustomers(
        Array.isArray(data) ? data : []
      );
    } catch (err) {
      setError(
        err.message ||
          "Unable to load customer data."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCustomers();
  }, []);

  const filteredCustomers = useMemo(() => {
    const text = search
      .trim()
      .toLowerCase();

    if (!text) {
      return customers;
    }

    return customers.filter(
      (customer) =>
        customer.location_name
          ?.toLowerCase()
          .includes(text) ||
        String(
          customer.location_id
        ).includes(text)
    );
  }, [customers, search]);

  const totalDemand = customers.reduce(
    (sum, customer) =>
      sum +
      Number(
        customer.demand_quantity || 0
      ),
    0
  );

  const averageDemand =
    customers.length > 0
      ? totalDemand / customers.length
      : 0;

  const highestDemand =
    customers.length > 0
      ? Math.max(
          ...customers.map((customer) =>
            Number(
              customer.demand_quantity || 0
            )
          )
        )
      : 0;

  const highestDemandCustomer =
    customers.length > 0
      ? customers.reduce((highest, customer) =>
          Number(
            customer.demand_quantity || 0
          ) >
          Number(
            highest.demand_quantity || 0
          )
            ? customer
            : highest
        )
      : null;

  const getDemandStatus = (demand) => {
    if (demand >= 20) {
      return {
        label: "High demand",
        type: "warning",
      };
    }

    if (demand >= 10) {
      return {
        label: "Normal",
        type: "success",
      };
    }

    return {
      label: "Low demand",
      type: "neutral",
    };
  };

  return (
    <main className="page">

      {/* HEADER */}

      <div className="page-header">

        <div>
          <span className="page-label">
            DELIVERY NETWORK
          </span>

          <h2>Customers</h2>

          <p>
            Monitor customer demand and
            delivery locations.
          </p>
        </div>

        <button
          className="secondary-button"
          onClick={loadCustomers}
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

      {/* SUMMARY CARDS */}

      <section className="customer-stats">

        <div className="customer-stat-card">

          <div className="customer-stat-icon blue">
            <Users size={19} />
          </div>

          <div>
            <span>Total Customers</span>

            <strong>
              {customers.length}
            </strong>

            <small>
              delivery locations
            </small>
          </div>

        </div>

        <div className="customer-stat-card">

          <div className="customer-stat-icon purple">
            <Package size={19} />
          </div>

          <div>
            <span>Total Demand</span>

            <strong>
              {totalDemand.toLocaleString()}
            </strong>

            <small>
              units
            </small>
          </div>

        </div>

        <div className="customer-stat-card">

          <div className="customer-stat-icon green">
            <TrendingUp size={19} />
          </div>

          <div>
            <span>Average Demand</span>

            <strong>
              {averageDemand.toFixed(1)}
            </strong>

            <small>
              units / customer
            </small>
          </div>

        </div>

        <div className="customer-stat-card">

          <div className="customer-stat-icon orange">
            <Package size={19} />
          </div>

          <div>
            <span>Highest Demand</span>

            <strong>
              {highestDemand}
            </strong>

            <small>
              {highestDemandCustomer
                ?.location_name ||
                "customer"}
            </small>
          </div>

        </div>

      </section>


      {/* CUSTOMER TABLE */}

      {loading ? (

        <div className="customer-page-state">

          <RefreshCw
            size={25}
            className="spin"
          />

          <p>
            Loading customers...
          </p>

        </div>

      ) : error ? (

        <div className="customer-page-state error-state">

          <AlertTriangle size={25} />

          <strong>
            Unable to load customers
          </strong>

          <p>{error}</p>

          <button
            className="primary-button"
            onClick={loadCustomers}
          >
            Try Again
          </button>

        </div>

      ) : (

        <section className="customer-table-panel">

          <div className="customer-toolbar">

            <div>
              <h3>
                Delivery Locations
              </h3>

              <p>
                {filteredCustomers.length}{" "}
                customers displayed
              </p>
            </div>

            <div className="customer-search">

              <Search size={16} />

              <input
                value={search}
                onChange={(event) =>
                  setSearch(
                    event.target.value
                  )
                }
                placeholder="Search customer..."
              />

            </div>

          </div>

          <div className="customer-table-wrapper">

            <table className="customer-table">

              <thead>
                <tr>
                  <th>CUSTOMER</th>
                  <th>LOCATION</th>
                  <th>DEMAND</th>
                  <th>DEMAND LEVEL</th>
                  <th>STATUS</th>
                </tr>
              </thead>

              <tbody>

                {filteredCustomers.map(
                  (customer) => {

                    const demand = Number(
                      customer.demand_quantity ||
                        0
                    );

                    const status =
                      getDemandStatus(
                        demand
                      );

                    return (
                      <tr
                        key={
                          customer.location_id
                        }
                      >

                        <td>

                          <div className="customer-table-name">

                            <div className="customer-table-icon">
                              <Users
                                size={15}
                              />
                            </div>

                            <div>
                              <strong>
                                {
                                  customer.location_name
                                }
                              </strong>

                              <span>
                                Customer #
                                {
                                  customer.location_id
                                }
                              </span>
                            </div>

                          </div>

                        </td>

                        <td>

                          <div className="customer-location">

                            <MapPin
                              size={14}
                            />

                            <span>
                              {Number(
                                customer.latitude
                              ).toFixed(4)}
                              ,{" "}
                              {Number(
                                customer.longitude
                              ).toFixed(4)}
                            </span>

                          </div>

                        </td>

                        <td>

                          <strong>
                            {demand.toLocaleString()}
                          </strong>

                          <span className="customer-unit">
                            units
                          </span>

                        </td>

                        <td>

                          <div className="customer-demand-mini">

                            <div className="customer-mini-progress">

                              <div
                                style={{
                                  width: `${
                                    highestDemand >
                                    0
                                      ? Math.min(
                                          (demand /
                                            highestDemand) *
                                            100,
                                          100
                                        )
                                      : 0
                                  }%`,
                                }}
                              />

                            </div>

                            <span>
                              {highestDemand >
                              0
                                ? (
                                    (demand /
                                      highestDemand) *
                                    100
                                  ).toFixed(
                                    0
                                  )
                                : 0}
                              %
                            </span>

                          </div>

                        </td>

                        <td>

                          <span
                            className={`customer-status ${status.type}`}
                          >
                            {status.label}
                          </span>

                        </td>

                      </tr>
                    );
                  }
                )}

              </tbody>

            </table>

            {filteredCustomers.length ===
              0 && (
              <div className="customer-no-results">
                No customers found.
              </div>
            )}

          </div>

        </section>

      )}

    </main>
  );
}

export default Customers;