import { useState } from "react";
import { useAuth } from "../context/AuthContext";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  
  const { login } = useAuth();

    async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
      event.preventDefault();
      setMessage("");
      setError("");

    try {
      const response = await fetch("http://localhost:8000/user/login", {
        method:"POST",
        headers: {
        "Content-type": "application/json"
        },
        body: JSON.stringify({
          email: email,
          password: password,
        })
      })
      const data = await response.json()

      if(!response.ok){
        setError(data.detail);
        return;
      }
      await login(data.access_token);
      setMessage("Login successful");
    
    } catch {
      setError("Unable to connect to server");
    }
  }




  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <input type="email" placeholder="Email" value={email} onChange={(event) => setEmail(event.target.value)} />

        <input type="password" placeholder="Password" value={password} onChange={(event) => setPassword(event.target.value)} />

        <button type="submit">
          Login
        </button>
      </form>
      {message && <p>{message}</p>}
      {error && <p>{error}</p>}
    </div>
  );
}
export default Login;

