import {
  User,
  Shield,
  Mail,
  Briefcase,
} from "lucide-react";

function Profile() {
  return (
    <main className="page profile-page">
      <div className="page-header">
        <div>
          <span className="page-label">ACCOUNT</span>
          <h2>Profile</h2>
          <p>
            View your account information and access details.
          </p>
        </div>
      </div>

      <section className="profile-card">
        <div className="profile-card-header">
          <div className="profile-large-avatar">
            VJ
          </div>

          <div>
            <h3>Operations</h3>
            <p>Administrator</p>
          </div>
        </div>

        <div className="profile-divider"></div>

        <div className="profile-information">

          <div className="profile-information-item">
            <div className="profile-information-icon">
              <User size={16} />
            </div>

            <div>
              <span>Name</span>
              <strong>Operations</strong>
            </div>
          </div>

          <div className="profile-information-item">
            <div className="profile-information-icon">
              <Briefcase size={16} />
            </div>

            <div>
              <span>Role</span>
              <strong>Administrator</strong>
            </div>
          </div>

          <div className="profile-information-item">
            <div className="profile-information-icon">
              <Mail size={16} />
            </div>

            <div>
              <span>Email</span>
              <strong>Administrator account</strong>
            </div>
          </div>

          <div className="profile-information-item">
            <div className="profile-information-icon">
              <Shield size={16} />
            </div>

            <div>
              <span>Access</span>
              <strong>Full platform access</strong>
            </div>
          </div>

        </div>
      </section>
    </main>
  );
}

export default Profile;