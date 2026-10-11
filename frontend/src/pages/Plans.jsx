import {
  Check,
  Package,
  Route,
  Warehouse,
  BarChart3,
  Truck,
} from "lucide-react";

function Plans() {
  const features = [
    {
      icon: Package,
      title: "Inventory Analysis",
      description:
        "Forecast demand and evaluate inventory requirements.",
    },
    {
      icon: Warehouse,
      title: "Warehouse Allocation",
      description:
        "Allocate customer demand across available warehouses.",
    },
    {
      icon: Route,
      title: "Minimum-Cost Flow",
      description:
        "Optimize supply allocation using network flow.",
    },
    {
      icon: Truck,
      title: "Vehicle Routing",
      description:
        "Generate capacity-constrained delivery routes.",
    },
    {
      icon: BarChart3,
      title: "Optimization Analysis",
      description:
        "Compare baseline and optimized transportation costs.",
    },
  ];

  return (
    <main className="page plans-page">

      <div className="page-header">
        <div>
          <span className="page-label">
            PLATFORM
          </span>

          <h2>Plans</h2>

          <p>
            Current optimization capabilities available in the system.
          </p>
        </div>
      </div>

      <section className="plans-main-card">

        <div className="plans-card-header">
          <div>
            <span className="plans-status">
              ACTIVE
            </span>

            <h3>Operations Research Plan</h3>

            <p>
              Full access to the inventory and fleet optimization
              workflow implemented in the platform.
            </p>
          </div>

          <div className="plans-current">
            Current Plan
          </div>
        </div>

        <div className="plans-divider" />

        <div className="plans-features">

          {features.map((feature) => {
            const Icon = feature.icon;

            return (
              <div
                className="plans-feature"
                key={feature.title}
              >
                <div className="plans-feature-icon">
                  <Icon size={17} />
                </div>

                <div>
                  <div className="plans-feature-title">
                    <span>{feature.title}</span>
                    <Check size={15} />
                  </div>

                  <p>
                    {feature.description}
                  </p>
                </div>
              </div>
            );
          })}

        </div>

      </section>

      <section className="plans-note">
        <strong>Optimization workflow</strong>

        <span>
          Demand → Inventory → Warehouse Allocation → Vehicle Routing
        </span>
      </section>

    </main>
  );
}

export default Plans;