import { useState } from "react";
import { useAuth } from "../hooks/useAuth";

import { createUser } from "../services/api";

function CreateUser() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const [creating, setCreating] = useState(false);

  const { token } = useAuth();

  async function handleSubmit(
    event: React.FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();

    setMessage("");
    setError("");
    setCreating(true);

    try {
      const message = await createUser(
        email,
        password,
        token
      );

      setMessage(message);

      // Clear the form after successful creation
      setEmail("");
      setPassword("");
    } catch (error) {
      if (error instanceof Error) {
        setError(error.message);
      } else {
        setError("Unable to connect to server");
      }
    } finally {
      setCreating(false);
    }
  }

  return (
    <div className="create-user">
      <form
        className="create-user-form"
        onSubmit={handleSubmit}
      >
        <div className="form-field">
          <label htmlFor="user-email">
            Email
          </label>

          <input
            id="user-email"
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            placeholder="user@example.com"
            required
          />
        </div>

        <div className="form-field">
          <label htmlFor="user-password">
            Password
          </label>

          <input
            id="user-password"
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            required
          />
        </div>

        <button
          type="submit"
          disabled={creating}
        >
          {creating ? "Creating..." : "Create User"}
        </button>
      </form>

      {message && (
        <p className="success-message">
          {message}
        </p>
      )}

      {error && (
        <p className="error-message">
          {error}
        </p>
      )}
    </div>
  );
}

export default CreateUser;
