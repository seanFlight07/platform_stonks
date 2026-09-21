import type { Company } from "../types/company"

interface CompanySelectorProps{
  companies: Company[]
  selectedCompany: string
  setSelectedCompany: (code: string) => void
}

function CompanySelector({companies, selectedCompany, setSelectedCompany}: CompanySelectorProps){
  return(
      <section className=" card CompanySelector">
        <h2>Select Company</h2>
          <select
            value={selectedCompany}
            onChange={(event)=> setSelectedCompany(event.target.value)}>
          {companies.map((company)=>(
            <option key={company.code}
                    value={company.code}>
          {`${company.code} - ${company.name}`}
            </option>
        ))}
          </select>
      </section>
    )
  } 

export default CompanySelector
