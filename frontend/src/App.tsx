import Header from './components/Header'
import CompanySelector from './components/CompanySelector'
import {useState, useEffect } from 'react'
import type {Company} from './types/company'
import { getCompanies } from './services/api'


function App() {
  const [selectedCompany, setSelectedCompany] = useState("")
  const [companies,setCompanies] = useState<Company[]>([])

  useEffect(() =>{
    async function loadCompanies(){
      const data = await getCompanies()
        setCompanies(data)
    }
    loadCompanies()
  },[])
  return (
        <main>
          <Header title="Platform Stonks" 
                  subtitle="Stock market analysis platform"
          />
          <CompanySelector companies={companies}
              selectedCompany={selectedCompany}
              setSelectedCompany={setSelectedCompany}/>
          <p>App selected company: {selectedCompany}</p>
        </main>
    )
}

export default App
