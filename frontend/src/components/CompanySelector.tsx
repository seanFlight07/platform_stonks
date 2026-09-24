import type { Company } from "../types/company";

interface CompanySelectorProps {
  companies: Company[];
  selectedCompany: string;
  setSelectedCompany: (code: string) => void;
}

function CompanySelector({
  companies,
  selectedCompany,
  setSelectedCompany,
}: CompanySelectorProps) {
  return (
    <section className="card company-selector">
      <div className="section-header">
        <div>
          <h2>Companies</h2>
          <p>Select a company to view its market data.</p>
        </div>

        <select
          value={selectedCompany}
          onChange={(event) => setSelectedCompany(event.target.value)}
        >
          <option value="">Select company</option>

          {companies.map((company) => (
            <option key={company.code} value={company.code}>
              {company.code} - {company.name}
            </option>
          ))}
        </select>
      </div>
    </section>
  );
}

export default CompanySelector;
