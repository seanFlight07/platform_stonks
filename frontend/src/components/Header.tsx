import Login from "./Login";
import { useAuth } from "../context/AuthContext";
import { Link } from "react-router-dom";

interface HeaderProps {
  title: string;
}

function Header(props: HeaderProps) {
  const { user, logout } = useAuth();

  return (
    <header className="header">
      <div className="header-brand">
        <Link to="/" className="brand-link">
          <h1>{props.title}</h1>
        </Link>
      </div>

      <div className="header-auth">
        {!user ? (
          <Login />
        ) : (
          <>
            {user.role === "admin" && (
              <Link to="/admin" className="header-link">
                Admin
              </Link>
            )}

            <div className="user-details">
              <span>{user.email}</span>
              <span className="user-role">{user.role}</span>
            </div>

            <button onClick={logout}>
              Logout
            </button>
          </>
        )}
      </div>
    </header>
  );
}

export default Header;
