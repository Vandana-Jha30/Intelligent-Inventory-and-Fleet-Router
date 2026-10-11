import csv
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
VRP_FILE = BASE_DIR / "A-n32-k5.vrp"


def read_vrp_file(path):
    coordinates = {}
    demands = {}
    depot_id = None
    capacity = None

    section = None

    with open(path, "r") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            if line.startswith("CAPACITY"):
                capacity = int(line.split(":")[1].strip())

            elif line == "NODE_COORD_SECTION":
                section = "coordinates"

            elif line == "DEMAND_SECTION":
                section = "demands"

            elif line == "DEPOT_SECTION":
                section = "depot"

            elif line == "EOF":
                break

            elif section == "coordinates":
                parts = line.split()
                node_id = int(parts[0])
                x = float(parts[1])
                y = float(parts[2])
                coordinates[node_id] = (x, y)

            elif section == "demands":
                parts = line.split()
                node_id = int(parts[0])
                demand = float(parts[1])
                demands[node_id] = demand

            elif section == "depot":
                node_id = int(line)

                if node_id == -1:
                    section = None
                else:
                    depot_id = node_id

    return coordinates, demands, depot_id, capacity


def write_customers(coordinates, demands, depot_id):
    output = BASE_DIR / "customers.csv"

    with open(output, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "location_id",
            "location_name",
            "x",
            "y",
            "demand"
        ])

        for node_id in sorted(coordinates):
            if node_id == depot_id:
                continue

            x, y = coordinates[node_id]

            writer.writerow([
                node_id,
                f"Customer {node_id}",
                x,
                y,
                demands[node_id]
            ])

    return output


def write_depot(coordinates, depot_id):
    output = BASE_DIR / "depot.csv"

    x, y = coordinates[depot_id]

    with open(output, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "depot_id",
            "depot_name",
            "x",
            "y"
        ])

        writer.writerow([
            depot_id,
            "Main Depot",
            x,
            y
        ])

    return output


def write_warehouses():
    output = BASE_DIR / "warehouses.csv"

    with open(output, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "warehouse_id",
            "name",
            "x",
            "y",
            "capacity",
            "operating_cost"
        ])

        writer.writerow([
            1,
            "Warehouse 1",
            21,
            43,
            300,
            25000
        ])

        writer.writerow([
            2,
            "Warehouse 2",
            82,
            38,
            300,
            25000
        ])

    return output


def write_vehicles(capacity):
    output = BASE_DIR / "vehicles.csv"

    with open(output, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "vehicle_number",
            "capacity",
            "fixed_cost",
            "cost_per_km"
        ])

        for i in range(1, 6):
            writer.writerow([
                f"TRUCK-{i:03d}",
                capacity,
                500,
                20
            ])

    return output


def write_inventory():
    output = BASE_DIR / "inventory.csv"

    with open(output, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "warehouse_id",
            "product_id",
            "on_hand",
            "reserved",
            "on_order"
        ])

        writer.writerow([
            1,
            1,
            220,
            0,
            100
        ])

        writer.writerow([
            2,
            1,
            270,
            0,
            100
        ])

    return output


def main():
    print("Reading benchmark...")
    coordinates, demands, depot_id, capacity = read_vrp_file(VRP_FILE)

    print(f"Customers: {len(coordinates) - 1}")
    print(f"Depot: {depot_id}")
    print(f"Vehicle capacity: {capacity}")

    total_demand = sum(
        demand
        for node_id, demand in demands.items()
        if node_id != depot_id
    )

    print(f"Total customer demand: {total_demand}")

    customers_file = write_customers(
        coordinates,
        demands,
        depot_id
    )

    depot_file = write_depot(
        coordinates,
        depot_id
    )

    warehouses_file = write_warehouses()
    vehicles_file = write_vehicles(capacity)
    inventory_file = write_inventory()

    print("\nCreated:")
    print(customers_file)
    print(depot_file)
    print(warehouses_file)
    print(vehicles_file)
    print(inventory_file)


if __name__ == "__main__":
    main()