const apiRequest = async (endpoint, options = {}) => {
  const response = await fetch(endpoint, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    let message = `Request failed with status ${response.status}`;

    try {
      const errorData = await response.json();

      if (typeof errorData.detail === "string") {
        message = errorData.detail;
      }
    } catch {
      // Keep the default error message.
    }

    throw new Error(message);
  }

  return response.json();
};

/* =========================
   WAREHOUSES
========================= */

export const getWarehouses = () =>
  apiRequest("/api/warehouses");

/* =========================
   PRODUCTS
========================= */

export const getProducts = () =>
  apiRequest("/api/products");

/* =========================
   INVENTORY
========================= */

export const getInventory = () =>
  apiRequest("/api/inventory");

export const getInventoryAnalysis = (
  productId,
  warehouseId
) =>
  apiRequest(
    `/api/inventory/analysis/${productId}/${warehouseId}`
  );

export const getInventoryForecastAnalysis = (
  productId,
  warehouseId
) =>
  apiRequest(
    `/api/inventory/forecast-analysis/${productId}/${warehouseId}`
  );

/* =========================
   DEMAND
========================= */

export const getDemandHistory = () =>
  apiRequest("/api/demand");

export const getDemandForecast = (
  productId,
  warehouseId
) =>
  apiRequest(
    `/api/demand/forecast/${productId}/${warehouseId}`
  );

/* =========================
   CUSTOMERS
========================= */

export const getDeliveryLocations = () =>
  apiRequest("/api/delivery-locations");

/* =========================
   VEHICLES
========================= */

export const getVehicles = () =>
  apiRequest("/api/vehicles");

/* =========================
   DEPOTS
========================= */

export const getDepots = () =>
  apiRequest("/api/depots");

/* =========================
   SUPPLY CHAIN PLAN
========================= */

export const createSupplyChainPlan = (plan) =>
  apiRequest("/api/supply-chain/plan", {
    method: "POST",
    body: JSON.stringify(plan),
  });

/* =========================
   VEHICLE ROUTING
========================= */

export const solveVehicleRouting = (depotId) =>
  apiRequest("/api/vehicle-routing/solve", {
    method: "POST",
    body: JSON.stringify({
      depot_id: depotId,
    }),
  });

export const compareVehicleRouting = (depotId) =>
  apiRequest("/api/vehicle-routing/compare", {
    method: "POST",
    body: JSON.stringify({
      depot_id: depotId,
    }),
  });