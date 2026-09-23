import Header from './components/Header'
import CompanySelector from './components/CompanySelector'
import {useState, useEffect } from 'react'
import type {Company} from './types/company'
import type { Price } from './types/price'
import {getCompanies, getPrices} from './services/api'
import PriceDisplay from './components/PriceDisplay'
import PriceChart from './components/PriceChart'
import AddCompany from './components/AddCompany'
import Login from './components/Login'
import { useAuth } from './context/AuthContext'


function App() {
  const [selectedCompany, setSelectedCompany] = useState("")
  const [companies,setCompanies] = useState<Company[]>([])
  const [prices, setPrices] = useState<Price[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const { user, logout } = useAuth();


  useEffect(() =>{
    async function loadCompanies(){
      const data = await getCompanies()
        setCompanies(data)
    } loadCompanies()
  },[])

  useEffect(() =>{
    if (!selectedCompany){
      return
    }
    
    async function loadPrices(){
      try{
        setLoading(true)
        setError(null)

        const data = await getPrices(selectedCompany)
          setPrices(data)
      }
      catch{
        console.error(error)
        setError("Failed to load price data")
        setPrices([])
      }
      finally {
      setLoading(false)
      }
    }loadPrices()
  },[selectedCompany])



  return (
        <main className='dashboard'>
          <Header title="Platform Stonks" 
                  subtitle="Stock market analysis platform"
          />
          <CompanySelector companies={companies}
              selectedCompany={selectedCompany}
              setSelectedCompany={setSelectedCompany}/>
              {loading && <p>Loading price data...</p>}

              {error && <p>{error}</p>}

              {!loading && !error && (
              <>
                <PriceDisplay prices={prices} />
                <PriceChart prices={prices} />
              </>
              )}
              {user?.role === "admin" && (
                <AddCompany />
              )}
          {!user ? (
          <Login />
          ) : (
          <div>
            <p>Logged in as: {user.email}</p>
            <p>Role: {user.role}</p>
            <button onClick={logout}>
              Logout
            </button>
          </div>
            )}
        </main>
    )
}

export default App
