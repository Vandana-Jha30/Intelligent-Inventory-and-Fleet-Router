import { useState } from "react";

import {
  Search,
  Bell,
  ChevronDown,
  User,
  Settings,
  LogOut,
  Check,
} from "lucide-react";

import { useNavigate } from "react-router-dom";

function Topbar() {
  const navigate = useNavigate();

  const [showNotifications, setShowNotifications] =
    useState(false);

  const [showProfile, setShowProfile] =
    useState(false);

  const handleNotificationClick = () => {
    setShowNotifications((previous) => !previous);
    setShowProfile(false);
  };

  const handleProfileClick = () => {
    setShowProfile((previous) => !previous);
    setShowNotifications(false);
  };

  const handleProfile = () => {
    setShowProfile(false);
    navigate("/profile");
  };

  const handleSettings = () => {
    setShowProfile(false);
    navigate("/settings");
  };

  const handleSignOut = () => {
    setShowProfile(false);

    // There is currently no authentication backend.
    // For now, return the user to the dashboard.
    navigate("/");
  };

  return (
    <header className="topbar">

      <div className="search-box">
        <Search size={18} />

        <input
          type="text"
          placeholder="Search inventory, warehouses, customers..."
        />
      </div>

      <div className="topbar-right">

        {/* Notifications */}

        <div className="topbar-menu">
          <button
            className="notification-button"
            onClick={handleNotificationClick}
            aria-label="Notifications"
          >
            <Bell size={19} />

            <span className="notification-dot"></span>
          </button>

          {showNotifications && (
            <div className="notification-dropdown">

              <div className="dropdown-header">
                <strong>Notifications</strong>
                <span>1 new</span>
              </div>

              <div className="notification-item">

                <div className="notification-icon">
                  <Check size={15} />
                </div>

                <div>
                  <strong>
                    Optimization completed
                  </strong>

                  <p>
                    Your latest supply chain plan is ready.
                  </p>

                  <span>Just now</span>
                </div>

              </div>

              <div className="notification-footer">
                No other notifications
              </div>

            </div>
          )}
        </div>

        <div className="topbar-divider"></div>

        {/* Profile */}

        <div className="topbar-menu">

          <button
            className="profile-button"
            onClick={handleProfileClick}
            aria-label="Profile menu"
          >

            <div className="profile-avatar">
              VJ
            </div>

            <div className="profile-details">
              <strong>Operations</strong>
              <span>Administrator</span>
            </div>

            <ChevronDown
              size={16}
              className={
                showProfile
                  ? "profile-chevron open"
                  : "profile-chevron"
              }
            />

          </button>

          {showProfile && (
            <div className="profile-dropdown">

              <div className="profile-dropdown-header">

                <div className="profile-avatar large">
                  VJ
                </div>

                <div>
                  <strong>Operations</strong>
                  <span>Administrator</span>
                </div>

              </div>

              <div className="dropdown-divider"></div>

              <button
                className="dropdown-item"
                onClick={handleProfile}
              >
                <User size={15} />
                <span>Profile</span>
              </button>

              <button
                className="dropdown-item"
                onClick={handleSettings}
              >
                <Settings size={15} />
                <span>Settings</span>
              </button>

              <div className="dropdown-divider"></div>

              <button
                className="dropdown-item logout"
                onClick={handleSignOut}
              >
                <LogOut size={15} />
                <span>Sign out</span>
              </button>

            </div>
          )}

        </div>

      </div>
    </header>
  );
}

export default Topbar;