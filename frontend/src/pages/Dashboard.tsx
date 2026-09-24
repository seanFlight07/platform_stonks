import { useEffect, useState } from "react";
import type { Company } from "../types/company";
import type { Price } from "../types/price";
import { getCompanies, getPrices } from "../services/api";
import CompanySelector from "../components/CompanySelector";
import PriceDisplay from "../components/PriceDisplay";
import PriceChart from "../components/PriceChart";

function Dashboard() {
  const [selectedCompany, setSelectedCompany] = useState("");
  const [companies, setCompanies] = useState<Company[]>([]);
  const [prices, setPrices] = useState<Price[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadCompanies() {
      const data = await getCompanies();
      setCompanies(data);
    }

    loadCompanies();
  }, []);

  useEffect(() => {
    if (!selectedCompany) {
      setPrices([]);
      return;
    }

    async function loadPrices() {
      try {
        setLoading(true);
        setError(null);

        const data = await getPrices(selectedCompany);
        setPrices(data);
      } catch (error) {
        console.error(error);
        setError("Failed to load price data");
        setPrices([]);
      } finally {
        setLoading(false);
      }
    }

    loadPrices();
  }, [selectedCompany]);

  return (
    <main className="dashboard">
      <CompanySelector
        companies={companies}
        selectedCompany={selectedCompany}
        setSelectedCompany={setSelectedCompany}
      />

      {loading && <p>Loading price data...</p>}

      {error && <p>{error}</p>}

      {!loading && !error && (
        <>
          <PriceDisplay prices={prices} />
          <PriceChart prices={prices} />
        </>
      )}
    </main>
  );
}

export default Dashboard;
