import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";

import Sidebar from "./components/layout/Sidebar";
import Topbar from "./components/layout/Topbar";

import Dashboard from "./pages/Dashboard";
import Inventory from "./pages/Inventory";
import Warehouses from "./pages/Warehouses";
import Customers from "./pages/Customers";
import Fleet from "./pages/Fleet";
import Optimize from "./pages/Optimize";
import Plans from "./pages/Plans";
import Settings from "./pages/Settings";
import Profile from "./pages/Profile";

function App() {
  return (
    <BrowserRouter>
      <div className="app-layout">
        <Sidebar />

        <div className="main-content">
          <Topbar />

          <Routes>
            <Route
              path="/"
              element={<Dashboard />}
            />

            <Route
              path="/inventory"
              element={<Inventory />}
            />

            <Route
              path="/warehouses"
              element={<Warehouses />}
            />

            <Route
              path="/customers"
              element={<Customers />}
            />

            <Route
              path="/fleet"
              element={<Fleet />}
            />

            <Route
              path="/optimize"
              element={<Optimize />}
            />

            <Route
              path="/plans"
              element={<Plans />}
            />

            <Route
              path="/settings"
              element={<Settings />}
            />

            <Route
              path="/profile"
              element={<Profile />}
            />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;
