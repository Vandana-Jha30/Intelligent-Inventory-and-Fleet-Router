import { useEffect, useMemo, useState } from "react";

import {
  Warehouse,
  Package,
  Search,
  RefreshCw,
  MapPin,
  Activity,
  AlertTriangle,
} from "lucide-react";

import {
  getWarehouses,
  getInventory,
} from "../services/api";

function Warehouses() {
  const [warehouses, setWarehouses] = useState([]);
  const [inventory, setInventory] = useState([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [search, setSearch] = useState("");

  const loadWarehouses = async () => {
    try {
      setLoading(true);
      setError("");

      const [
        warehouseData,
        inventoryData,
      ] = await Promise.all([
        getWarehouses(),
        getInventory(),
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
    } catch (err) {
      setError(
        err.message ||
          "Unable to load warehouse data."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadWarehouses();
  }, []);

  const inventoryByWarehouse = useMemo(() => {
    const result = {};

    inventory.forEach((item) => {
      const warehouseId =
        item.warehouse_id;

      if (!result[warehouseId]) {
        result[warehouseId] = 0;
      }

      result[warehouseId] +=
        Number(item.on_hand || 0) -
        Number(item.reserved || 0);
    });

    return result;
  }, [inventory]);

  const filteredWarehouses =
    useMemo(() => {
      const text = search
        .trim()
        .toLowerCase();

      if (!text) {
        return warehouses;
      }

      return warehouses.filter(
        (warehouse) =>
          warehouse.name
            ?.toLowerCase()
            .includes(text) ||
          String(
            warehouse.warehouse_id
          ).includes(text)
      );
    }, [warehouses, search]);

  const totalCapacity =
    warehouses.reduce(
      (sum, warehouse) =>
        sum +
        Number(warehouse.capacity || 0),
      0
    );

  const totalInventory =
    warehouses.reduce(
      (sum, warehouse) =>
        sum +
        Number(
          inventoryByWarehouse[
            warehouse.warehouse_id
          ] || 0
        ),
      0
    );

  const averageUtilization =
    totalCapacity > 0
      ? (totalInventory /
          totalCapacity) *
        100
      : 0;

  const getUtilization = (
    warehouse
  ) => {
    const capacity =
      Number(warehouse.capacity || 0);

    const inventoryAmount =
      Number(
        inventoryByWarehouse[
          warehouse.warehouse_id
        ] || 0
      );

    if (capacity <= 0) {
      return 0;
    }

    return (
      (inventoryAmount / capacity) *
      100
    );
  };

  const getWarehouseStatus =
    (utilization) => {
      if (utilization >= 90) {
        return {
          label: "High utilization",
          type: "warning",
        };
      }

      if (utilization >= 70) {
        return {
          label: "Healthy",
          type: "success",
        };
      }

      return {
        label: "Available capacity",
        type: "neutral",
      };
    };

  return (
    <main className="page">
      <div className="page-header">
        <div>
          <span className="page-label">
            WAREHOUSE NETWORK
          </span>

          <h2>Warehouses</h2>

          <p>
            Monitor warehouse capacity,
            inventory and utilization.
          </p>
        </div>

        <button
          className="secondary-button"
          onClick={loadWarehouses}
          disabled={loading}
        >
          <RefreshCw
            size={16}
            className={
              loading
                ? "spin"
                : ""
            }
          />

          Refresh
        </button>
      </div>

      {/* SUMMARY CARDS */}

      <section className="warehouse-stats">
        <div className="warehouse-stat-card">
          <div className="warehouse-stat-icon blue">
            <Warehouse size={19} />
          </div>

          <div>
            <span>Total Warehouses</span>
            <strong>
              {warehouses.length}
            </strong>
            <small>facilities</small>
          </div>
        </div>

        <div className="warehouse-stat-card">
          <div className="warehouse-stat-icon purple">
            <Package size={19} />
          </div>

          <div>
            <span>Total Capacity</span>
            <strong>
              {totalCapacity.toLocaleString()}
            </strong>
            <small>units</small>
          </div>
        </div>

        <div className="warehouse-stat-card">
          <div className="warehouse-stat-icon green">
            <Activity size={19} />
          </div>

          <div>
            <span>Inventory Stored</span>
            <strong>
              {totalInventory.toLocaleString()}
            </strong>
            <small>available units</small>
          </div>
        </div>

        <div className="warehouse-stat-card">
          <div className="warehouse-stat-icon orange">
            <Activity size={19} />
          </div>

          <div>
            <span>Average Utilization</span>
            <strong>
              {averageUtilization.toFixed(1)}%
            </strong>
            <small>network utilization</small>
          </div>
        </div>
      </section>

      {/* WAREHOUSE CARDS */}

      {loading ? (
        <div className="warehouse-page-state">
          <RefreshCw
            size={25}
            className="spin"
          />

          <p>
            Loading warehouses...
          </p>
        </div>
      ) : error ? (
        <div className="warehouse-page-state error-state">
          <AlertTriangle size={25} />

          <strong>
            Unable to load warehouses
          </strong>

          <p>{error}</p>

          <button
            className="primary-button"
            onClick={loadWarehouses}
          >
            Try Again
          </button>
        </div>
      ) : (
        <>
          <section className="warehouse-cards">
            {filteredWarehouses.map(
              (warehouse) => {
                const inventoryAmount =
                  Number(
                    inventoryByWarehouse[
                      warehouse
                        .warehouse_id
                    ] || 0
                  );

                const capacity =
                  Number(
                    warehouse.capacity ||
                      0
                  );

                const utilization =
                  getUtilization(
                    warehouse
                  );

                const remaining =
                  Math.max(
                    capacity -
                      inventoryAmount,
                    0
                  );

                const status =
                  getWarehouseStatus(
                    utilization
                  );

                return (
                  <div
                    className="warehouse-card"
                    key={
                      warehouse.warehouse_id
                    }
                  >
                    <div className="warehouse-card-header">
                      <div className="warehouse-card-title">
                        <div className="warehouse-card-icon">
                          <Warehouse
                            size={19}
                          />
                        </div>

                        <div>
                          <h3>
                            {warehouse.name}
                          </h3>

                          <span>
                            Warehouse #
                            {
                              warehouse.warehouse_id
                            }
                          </span>
                        </div>
                      </div>

                      <span
                        className={`warehouse-status ${status.type}`}
                      >
                        {status.label}
                      </span>
                    </div>

                    <div className="warehouse-location">
                      <MapPin size={14} />

                      <span>
                        {Number(
                          warehouse.latitude
                        ).toFixed(4)}
                        ,{" "}
                        {Number(
                          warehouse.longitude
                        ).toFixed(4)}
                      </span>
                    </div>

                    <div className="warehouse-capacity-heading">
                      <span>
                        Capacity utilization
                      </span>

                      <strong>
                        {utilization.toFixed(
                          0
                        )}
                        %
                      </strong>
                    </div>

                    <div className="warehouse-large-progress">
                      <div
                        className={
                          utilization >= 90
                            ? "warning"
                            : ""
                        }
                        style={{
                          width: `${Math.min(
                            utilization,
                            100
                          )}%`,
                        }}
                      />
                    </div>

                    <div className="warehouse-metrics">
                      <div>
                        <span>
                          Available inventory
                        </span>

                        <strong>
                          {inventoryAmount.toLocaleString()}
                        </strong>
                      </div>

                      <div>
                        <span>
                          Capacity
                        </span>

                        <strong>
                          {capacity.toLocaleString()}
                        </strong>
                      </div>

                      <div>
                        <span>
                          Remaining
                        </span>

                        <strong>
                          {remaining.toLocaleString()}
                        </strong>
                      </div>
                    </div>
                  </div>
                );
              }
            )}
          </section>

          {/* TABLE */}

          <section className="warehouse-table-panel">
            <div className="warehouse-toolbar">
              <div>
                <h3>
                  Warehouse Details
                </h3>

                <p>
                  {filteredWarehouses.length}{" "}
                  facilities displayed
                </p>
              </div>

              <div className="warehouse-search">
                <Search size={16} />

                <input
                  value={search}
                  onChange={(event) =>
                    setSearch(
                      event.target.value
                    )
                  }
                  placeholder="Search warehouse..."
                />
              </div>
            </div>

            <div className="warehouse-table-wrapper">
              <table className="warehouse-table">
                <thead>
                  <tr>
                    <th>WAREHOUSE</th>
                    <th>LOCATION</th>
                    <th>INVENTORY</th>
                    <th>CAPACITY</th>
                    <th>UTILIZATION</th>
                    <th>REMAINING</th>
                    <th>STATUS</th>
                  </tr>
                </thead>

                <tbody>
                  {filteredWarehouses.map(
                    (warehouse) => {
                      const inventoryAmount =
                        Number(
                          inventoryByWarehouse[
                            warehouse
                              .warehouse_id
                          ] || 0
                        );

                      const capacity =
                        Number(
                          warehouse.capacity ||
                            0
                        );

                      const utilization =
                        getUtilization(
                          warehouse
                        );

                      const remaining =
                        Math.max(
                          capacity -
                            inventoryAmount,
                          0
                        );

                      const status =
                        getWarehouseStatus(
                          utilization
                        );

                      return (
                        <tr
                          key={
                            warehouse.warehouse_id
                          }
                        >
                          <td>
                            <div className="warehouse-table-name">
                              <div>
                                <Warehouse
                                  size={15}
                                />
                              </div>

                              <strong>
                                {
                                  warehouse.name
                                }
                              </strong>
                            </div>
                          </td>

                          <td>
                            {Number(
                              warehouse.latitude
                            ).toFixed(4)}
                            ,{" "}
                            {Number(
                              warehouse.longitude
                            ).toFixed(4)}
                          </td>

                          <td>
                            <strong>
                              {inventoryAmount.toLocaleString()}
                            </strong>
                          </td>

                          <td>
                            {capacity.toLocaleString()}
                          </td>

                          <td>
                            <div className="table-utilization">
                              <div className="small-progress">
                                <div
                                  className={
                                    utilization >=
                                    90
                                      ? "warning"
                                      : ""
                                  }
                                  style={{
                                    width: `${Math.min(
                                      utilization,
                                      100
                                    )}%`,
                                  }}
                                />
                              </div>

                              <span>
                                {utilization.toFixed(
                                  0
                                )}
                                %
                              </span>
                            </div>
                          </td>

                          <td>
                            {remaining.toLocaleString()}
                          </td>

                          <td>
                            <span
                              className={`warehouse-status ${status.type}`}
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
            </div>
          </section>
        </>
      )}
    </main>
  );
}

export default Warehouses;