import Login from "./Login";
import { useAuth } from "../context/AuthContext";

interface HeaderProps {
  title: string;
}

function Header(props: HeaderProps) {
  const { user, logout } = useAuth();

  return (
    <header className="header">
      <div className="header-brand">
        <h1>{props.title}</h1>
      </div>

      <div className="header-auth">
        {!user ? (
          <Login />
        ) : (
          <>
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
