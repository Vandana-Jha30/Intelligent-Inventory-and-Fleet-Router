import { useEffect, useMemo, useState } from "react";

import {
  Package,
  Search,
  RefreshCw,
  AlertTriangle,
  CheckCircle2,
  Warehouse,
} from "lucide-react";

import {
  getInventory,
  getProducts,
  getWarehouses,
} from "../services/api";

function Inventory() {
  const [inventory, setInventory] = useState([]);
  const [products, setProducts] = useState([]);
  const [warehouses, setWarehouses] = useState([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [search, setSearch] = useState("");
  const [warehouseFilter, setWarehouseFilter] =
    useState("all");

  const loadInventory = async () => {
    try {
      setLoading(true);
      setError("");

      const [
        inventoryData,
        productsData,
        warehousesData,
      ] = await Promise.all([
        getInventory(),
        getProducts(),
        getWarehouses(),
      ]);

      setInventory(
        Array.isArray(inventoryData)
          ? inventoryData
          : []
      );

      setProducts(
        Array.isArray(productsData)
          ? productsData
          : []
      );

      setWarehouses(
        Array.isArray(warehousesData)
          ? warehousesData
          : []
      );
    } catch (err) {
      setError(
        err.message ||
          "Unable to load inventory data."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadInventory();
  }, []);

  const productMap = useMemo(() => {
    return Object.fromEntries(
      products.map((product) => [
        product.product_id,
        product,
      ])
    );
  }, [products]);

  const warehouseMap = useMemo(() => {
    return Object.fromEntries(
      warehouses.map((warehouse) => [
        warehouse.warehouse_id,
        warehouse,
      ])
    );
  }, [warehouses]);

  const filteredInventory = useMemo(() => {
    const searchText = search
      .trim()
      .toLowerCase();

    return inventory.filter((item) => {
      const product =
        productMap[item.product_id];

      const warehouse =
        warehouseMap[item.warehouse_id];

      const productName =
        product?.name || "";

      const sku =
        product?.sku || "";

      const warehouseName =
        warehouse?.name || "";

      const matchesSearch =
        !searchText ||
        productName
          .toLowerCase()
          .includes(searchText) ||
        sku
          .toLowerCase()
          .includes(searchText) ||
        warehouseName
          .toLowerCase()
          .includes(searchText);

      const matchesWarehouse =
        warehouseFilter === "all" ||
        String(item.warehouse_id) ===
          warehouseFilter;

      return (
        matchesSearch &&
        matchesWarehouse
      );
    });
  }, [
    inventory,
    productMap,
    warehouseMap,
    search,
    warehouseFilter,
  ]);

  const totalOnHand = inventory.reduce(
    (sum, item) =>
      sum + Number(item.on_hand || 0),
    0
  );

  const totalReserved = inventory.reduce(
    (sum, item) =>
      sum + Number(item.reserved || 0),
    0
  );

  const totalOnOrder = inventory.reduce(
    (sum, item) =>
      sum + Number(item.on_order || 0),
    0
  );

  const availableInventory =
    totalOnHand - totalReserved;

  const getStatus = (item) => {
    const available =
      Number(item.on_hand || 0) -
      Number(item.reserved || 0);

    if (available <= 0) {
      return {
        label: "Out of stock",
        type: "danger",
      };
    }

    if (available < 20) {
      return {
        label: "Low stock",
        type: "warning",
      };
    }

    return {
      label: "Healthy",
      type: "success",
    };
  };

  return (
    <main className="page">
      <div className="page-header">
        <div>
          <span className="page-label">
            INVENTORY MANAGEMENT
          </span>

          <h2>Inventory</h2>

          <p>
            Monitor stock levels across your
            warehouse network.
          </p>
        </div>

        <button
          className="secondary-button"
          onClick={loadInventory}
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

      {/* SUMMARY */}

      <section className="inventory-stats">
        <div className="inventory-stat-card">
          <div className="inventory-stat-icon blue">
            <Package size={19} />
          </div>

          <div>
            <span>Total On Hand</span>
            <strong>
              {totalOnHand.toLocaleString()}
            </strong>
            <small>units</small>
          </div>
        </div>

        <div className="inventory-stat-card">
          <div className="inventory-stat-icon orange">
            <AlertTriangle size={19} />
          </div>

          <div>
            <span>Reserved</span>
            <strong>
              {totalReserved.toLocaleString()}
            </strong>
            <small>units</small>
          </div>
        </div>

        <div className="inventory-stat-card">
          <div className="inventory-stat-icon green">
            <CheckCircle2 size={19} />
          </div>

          <div>
            <span>Available</span>
            <strong>
              {availableInventory.toLocaleString()}
            </strong>
            <small>units</small>
          </div>
        </div>

        <div className="inventory-stat-card">
          <div className="inventory-stat-icon purple">
            <Warehouse size={19} />
          </div>

          <div>
            <span>On Order</span>
            <strong>
              {totalOnOrder.toLocaleString()}
            </strong>
            <small>units</small>
          </div>
        </div>
      </section>

      {/* INVENTORY TABLE */}

      <section className="inventory-panel">
        <div className="inventory-toolbar">
          <div>
            <h3>Inventory Records</h3>
            <p>
              {filteredInventory.length} records
              displayed
            </p>
          </div>

          <div className="inventory-filters">
            <div className="inventory-search">
              <Search size={16} />

              <input
                value={search}
                onChange={(event) =>
                  setSearch(
                    event.target.value
                  )
                }
                placeholder="Search product or warehouse..."
              />
            </div>

            <select
              value={warehouseFilter}
              onChange={(event) =>
                setWarehouseFilter(
                  event.target.value
                )
              }
            >
              <option value="all">
                All warehouses
              </option>

              {warehouses.map(
                (warehouse) => (
                  <option
                    key={
                      warehouse.warehouse_id
                    }
                    value={
                      warehouse.warehouse_id
                    }
                  >
                    {warehouse.name}
                  </option>
                )
              )}
            </select>
          </div>
        </div>

        {loading ? (
          <div className="page-state">
            <RefreshCw
              size={24}
              className="spin"
            />

            <p>
              Loading inventory...
            </p>
          </div>
        ) : error ? (
          <div className="page-state error-state">
            <AlertTriangle size={25} />

            <strong>
              Unable to load inventory
            </strong>

            <p>{error}</p>

            <button
              className="primary-button"
              onClick={loadInventory}
            >
              Try Again
            </button>
          </div>
        ) : filteredInventory.length ===
          0 ? (
          <div className="page-state">
            <Package size={28} />

            <strong>
              No inventory found
            </strong>

            <p>
              Try changing your search or
              warehouse filter.
            </p>
          </div>
        ) : (
          <div className="inventory-table-wrapper">
            <table className="inventory-table">
              <thead>
                <tr>
                  <th>PRODUCT</th>
                  <th>WAREHOUSE</th>
                  <th>ON HAND</th>
                  <th>RESERVED</th>
                  <th>AVAILABLE</th>
                  <th>ON ORDER</th>
                  <th>STATUS</th>
                </tr>
              </thead>

              <tbody>
                {filteredInventory.map(
                  (item) => {
                    const product =
                      productMap[
                        item.product_id
                      ];

                    const warehouse =
                      warehouseMap[
                        item.warehouse_id
                      ];

                    const available =
                      Number(
                        item.on_hand || 0
                      ) -
                      Number(
                        item.reserved || 0
                      );

                    const status =
                      getStatus(item);

                    return (
                      <tr
                        key={
                          item.inventory_id
                        }
                      >
                        <td>
                          <div className="product-cell">
                            <div className="product-icon">
                              <Package
                                size={16}
                              />
                            </div>

                            <div>
                              <strong>
                                {product?.name ||
                                  `Product ${item.product_id}`}
                              </strong>

                              <span>
                                {product?.sku ||
                                  `ID-${item.product_id}`}
                              </span>
                            </div>
                          </div>
                        </td>

                        <td>
                          <div className="warehouse-cell">
                            <Warehouse
                              size={15}
                            />

                            {warehouse?.name ||
                              `Warehouse ${item.warehouse_id}`}
                          </div>
                        </td>

                        <td>
                          <strong>
                            {Number(
                              item.on_hand || 0
                            ).toLocaleString()}
                          </strong>
                        </td>

                        <td>
                          {Number(
                            item.reserved || 0
                          ).toLocaleString()}
                        </td>

                        <td>
                          <strong>
                            {available.toLocaleString()}
                          </strong>
                        </td>

                        <td>
                          {Number(
                            item.on_order || 0
                          ).toLocaleString()}
                        </td>

                        <td>
                          <span
                            className={`inventory-status ${status.type}`}
                          >
                            <span></span>
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
        )}
      </section>
    </main>
  );
}

export default Inventory;