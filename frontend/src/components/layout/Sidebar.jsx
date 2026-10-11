import {
  LayoutDashboard,
  Package,
  Warehouse,
  Users,
  Truck,
  Route,
  ClipboardList,
  Settings,
} from "lucide-react";

import { NavLink } from "react-router-dom";

const navigationItems = [
  {
    label: "Dashboard",
    icon: LayoutDashboard,
    path: "/",
  },
  {
    label: "Inventory",
    icon: Package,
    path: "/inventory",
  },
  {
    label: "Warehouses",
    icon: Warehouse,
    path: "/warehouses",
  },
  {
    label: "Customers",
    icon: Users,
    path: "/customers",
  },
  {
    label: "Fleet",
    icon: Truck,
    path: "/fleet",
  },
  {
    label: "Optimize",
    icon: Route,
    path: "/optimization",
  },
  {
    label: "Plans",
    icon: ClipboardList,
    path: "/plans",
  },
];

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
            <div className="brand-logo">
                <Route size={21} />
            </div>

            <div>
                <h1>Inventory & Fleet</h1>
                <span>Operations Platform</span>
            </div>
        </div>

      <div className="sidebar-section">
        <p className="sidebar-section-title">
          OPERATIONS
        </p>

        <nav>
          {navigationItems.map(
            (item) => {
              const Icon = item.icon;

              return (
                <NavLink
                  to={item.path}
                  key={item.label}
                  end={item.path === "/"}
                  className={({ isActive }) =>
                    `sidebar-link ${
                      isActive
                        ? "active"
                        : ""
                    }`
                  }
                >
                  <Icon size={19} />
                  <span>{item.label}</span>
                </NavLink>
              );
            }
          )}
        </nav>
      </div>

      <div className="sidebar-bottom">
        <div className="system-status">
          <span className="status-indicator"></span>

          <div>
            <strong>
              System Online
            </strong>

            <span>
              All services operational
            </span>
          </div>
        </div>

        <NavLink
          to="/settings"
          className="sidebar-link"
        >
          <Settings size={19} />
          <span>Settings</span>
        </NavLink>
      </div>
    </aside>
  );
}

export default Sidebar;