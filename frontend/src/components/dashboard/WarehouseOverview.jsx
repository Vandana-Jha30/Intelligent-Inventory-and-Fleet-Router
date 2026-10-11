import { Warehouse } from "lucide-react";

const warehouses = [
  {
    name: "Warehouse 1",
    location: "Central Distribution",
    inventory: 220,
    capacity: 300,
  },
  {
    name: "Warehouse 2",
    location: "East Distribution",
    inventory: 270,
    capacity: 300,
  },
];

function WarehouseOverview() {
  return (
    <div className="dashboard-panel">
      <div className="panel-header">
        <div>
          <h3>Warehouse Capacity</h3>
          <p>Current inventory utilization</p>
        </div>

        <Warehouse size={20} />
      </div>

      <div className="warehouse-list">
        {warehouses.map((warehouse) => {
          const utilization =
            (warehouse.inventory / warehouse.capacity) * 100;

          const remaining =
            warehouse.capacity - warehouse.inventory;

          return (
            <div
              className="warehouse-item"
              key={warehouse.name}
            >
              <div className="warehouse-info">
                <div>
                  <strong>{warehouse.name}</strong>
                  <span>{warehouse.location}</span>
                </div>

                <strong>
                  {Math.round(utilization)}%
                </strong>
              </div>

              <div className="progress-background">
                <div
                  className={`progress-value ${
                    utilization >= 85 ? "warning" : ""
                  }`}
                  style={{
                    width: `${utilization}%`,
                  }}
                />
              </div>

              <div className="warehouse-footer">
                <span>
                  {warehouse.inventory} /{" "}
                  {warehouse.capacity} units
                </span>

                <span>
                  {remaining} available
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default WarehouseOverview;