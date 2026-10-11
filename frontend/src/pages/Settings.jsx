import { useEffect, useState } from "react";
import {
  Settings as SettingsIcon,
  Route,
  Monitor,
  RotateCcw,
  Check,
} from "lucide-react";

function Settings() {
  const defaultSettings = {
    planningWindow: "3",
    currency: "INR",
    inventoryAnalysis: true,
    warehouseAllocation: true,
    vehicleRouting: true,
  };

  const [settings, setSettings] = useState(defaultSettings);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    const savedSettings = localStorage.getItem("iifr_settings");

    if (savedSettings) {
      setSettings(JSON.parse(savedSettings));
    }
  }, []);


  const updateSetting = (key, value) => {
    setSettings((previous) => ({
      ...previous,
      [key]: value,
    }));

    setSaved(false);
  };

  const handleSave = () => {
  localStorage.setItem("iifr_settings", JSON.stringify(settings));

  document.body.classList.remove(
    "density-comfortable",
    "density-compact"
  );

  document.body.classList.add(
    `density-${settings.displayDensity}`
  );

  setSaved(true);

  setTimeout(() => {
    setSaved(false);
  }, 2000);
};

  const handleReset = () => {
  localStorage.removeItem("iifr_settings");
  setSettings(defaultSettings);

  document.body.classList.remove(
    "density-compact"
  );

  document.body.classList.add(
    "density-comfortable"
  );

  setSaved(false);
};

  return (
    <main className="page settings-page">
      <div className="page-header">
        <div>
          <span className="page-label">CONFIGURATION</span>
          <h2>Settings</h2>
          <p>
            Configure the operational preferences for the platform.
          </p>
        </div>
      </div>

      <div className="settings-grid">

        {/* GENERAL */}
        <section className="settings-section">
          <div className="settings-section-header">
            <div className="settings-section-icon">
              <SettingsIcon size={17} />
            </div>

            <div>
              <h3>General</h3>
              <p>Basic application preferences.</p>
            </div>
          </div>

          <div className="settings-fields">

            <div className="settings-field">
              <label>Application Name</label>

              <input
                type="text"
                value="Intelligent Inventory and Fleet Router"
                readOnly
              />
            </div>

            <div className="settings-field">
              <label>Planning Window</label>

              <select
                value={settings.planningWindow}
                onChange={(e) =>
                  updateSetting("planningWindow", e.target.value)
                }
              >
                <option value="1">1 day</option>
                <option value="3">3 days</option>
                <option value="7">7 days</option>
                <option value="14">14 days</option>
              </select>
            </div>

            <div className="settings-field">
              <label>Currency</label>

              <select
                value={settings.currency}
                onChange={(e) =>
                  updateSetting("currency", e.target.value)
                }
              >
                <option value="INR">INR (₹)</option>
                <option value="USD">USD ($)</option>
              </select>
            </div>

          </div>
        </section>

        {/* OPTIMIZATION */}
        <section className="settings-section">
          <div className="settings-section-header">
            <div className="settings-section-icon">
              <Route size={17} />
            </div>

            <div>
              <h3>Optimization</h3>
              <p>Control the optimization workflow.</p>
            </div>
          </div>

          <div className="settings-options">

            <label className="settings-option">
              <div>
                <strong>Inventory Analysis</strong>
                <span>
                  Include inventory forecasting in planning.
                </span>
              </div>

              <input
                type="checkbox"
                checked={settings.inventoryAnalysis}
                onChange={(e) =>
                  updateSetting(
                    "inventoryAnalysis",
                    e.target.checked
                  )
                }
              />
            </label>

            <label className="settings-option">
              <div>
                <strong>Warehouse Allocation</strong>
                <span>
                  Optimize allocation between warehouses and customers.
                </span>
              </div>

              <input
                type="checkbox"
                checked={settings.warehouseAllocation}
                onChange={(e) =>
                  updateSetting(
                    "warehouseAllocation",
                    e.target.checked
                  )
                }
              />
            </label>

            <label className="settings-option">
              <div>
                <strong>Vehicle Routing</strong>
                <span>
                  Generate capacity-constrained delivery routes.
                </span>
              </div>

              <input
                type="checkbox"
                checked={settings.vehicleRouting}
                onChange={(e) =>
                  updateSetting(
                    "vehicleRouting",
                    e.target.checked
                  )
                }
              />
            </label>

          </div>
        </section>

        {/* INTERFACE */}
        

      </div>

      {/* ACTIONS */}
      <div className="settings-actions">

        <button
          className="secondary-button"
          onClick={handleReset}
        >
          <RotateCcw size={15} />
          Reset
        </button>

        <button
          className="primary-button"
          onClick={handleSave}
        >
          {saved ? <Check size={15} /> : null}
          {saved ? "Saved" : "Save Changes"}
        </button>

      </div>
    </main>
  );
}

export default Settings;