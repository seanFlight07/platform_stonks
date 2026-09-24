import AddCompany from "../components/AddCompany";
import CreateUser from "../components/CreateUser";

function Admin() {
  return (
    <main className="dashboard">
      <div className="page-header">
        <h2>Admin</h2>
        <p>Manage companies and users.</p>
      </div>

      <div className="admin-grid">
        <section className="card admin-section">
          <h2>Companies</h2>
          <p>Search for and add companies to Platform Stonks.</p>

          <AddCompany />
        </section>

        <section className="card admin-section">
          <h2>Users</h2>
          <p>Create and manage Platform Stonks users.</p>

          <CreateUser />
        </section>
      </div>
    </main>
  );
}

export default Admin;
