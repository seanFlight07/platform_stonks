import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

import Header from "./components/Header";
import Dashboard from "./pages/Dashboard";
import Admin from "./pages/Admin";
import { useAuth } from "./context/AuthContext";

function App() {
  const { user } = useAuth();

  return (
    <BrowserRouter>
      <Header title="Platform Stonks" />

      <Routes>
        <Route path="/" element={<Dashboard />} />

        <Route
          path="/admin"
          element={
            user?.role === "admin"
              ? <Admin />
              : <Navigate to="/" replace />
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
