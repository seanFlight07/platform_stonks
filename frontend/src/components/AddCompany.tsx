import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { searchCompany, addCompany } from "../services/api";
import type { CompanySearchResult } from "../types/company";

function AddCompany() {
  const [code, setCode] = useState("");
  const [exchange, setExchange] = useState("");
  const [company, setCompany] = useState<CompanySearchResult | null>(null);

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const [searching, setSearching] = useState(false);
  const [adding, setAdding] = useState(false);

  const { token } = useAuth();

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    setMessage("");
    setError("");
    setCompany(null);
    setSearching(true);

    try {
      const company = await searchCompany(
        code,
        exchange,
        token
      );

      setCompany(company);
    } catch (error) {
      if (error instanceof Error) {
        setError(error.message);
      } else {
        setError("Unable to connect to server");
      }
    } finally {
      setSearching(false);
    }
  }

  async function handleAddCompany() {
    if (!company) {
      return;
    }

    setMessage("");
    setError("");
    setAdding(true);

    try {
      const message = await addCompany(
        company,
        token
      );

      setMessage(message);
    } catch (error) {
      if (error instanceof Error) {
        setError(error.message);
      } else {
        setError("Unable to connect to server");
      }
    } finally {
      setAdding(false);
    }
  }

  return (
    <div className="add-company">
      <form
        className="company-search-form"
        onSubmit={handleSubmit}
      >
        <div className="form-field">
          <label htmlFor="company-code">
            Company code
          </label>

          <input
            id="company-code"
            type="text"
            value={code}
            onChange={(event) => setCode(event.target.value)}
            placeholder="e.g. CBA"
            required
          />
        </div>

        <div className="form-field">
          <label htmlFor="exchange">
            Exchange
          </label>

          <input
            id="exchange"
            type="text"
            value={exchange}
            onChange={(event) => setExchange(event.target.value)}
            placeholder="e.g. AX"
            required
          />
        </div>

        <button
          type="submit"
          disabled={searching}
        >
          {searching ? "Searching..." : "Search"}
        </button>
      </form>

      {company && (
        <div className="company-result">
          <div>
            <h3>{company.long_name}</h3>

            <p className="company-code">
              {company.code}.{company.exchange}
            </p>
          </div>

          <div className="company-result-details">
            <span>Sector</span>
            <strong>{company.sector}</strong>

            <span>Previous close</span>
            <strong>
              ${company.previous_close.toFixed(2)}
            </strong>
          </div>

          <button
            type="button"
            onClick={handleAddCompany}
            disabled={adding}
          >
            {adding ? "Adding..." : "Add Company"}
          </button>
        </div>
      )}

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

export default AddCompany;
