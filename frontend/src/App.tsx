import Header from './components/Header'
import CompanySelector from './components/CompanySelector'
const companies = [
    {
        code: "CCP",
        name: "Credit Corp",
        exchange: "AX",
        active: true
    },
    {
        code: "WBC",
        name: "Westpac",
        exchange: "AX",
        active: true
    },
    {
        code: "NAB",
        name: "National Australia Bank",
        exchange: "AX",
        active: true
    }
]

function App() {
    return (
        <main>
          <Header title="Platform Stonks" 
                  subtitle="Stock market analysis platform"
          />
          <CompanySelector companies={companies}/>

        </main>
    )
}

export default App
