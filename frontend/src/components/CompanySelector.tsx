import type { Company } from "../types/company"
import { useState } from 'react'

interface CompanySelectorProps{
  companies: Company[]
}

function CompanySelector({companies}: CompanySelectorProps){
  const [selectedCompany, setSelectedCompany] = useState("")
  return(
      <section>
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
